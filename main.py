from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import mediapipe as mp

from recommendations import get_recommendation

app = FastAPI(
    title="FrameHub API",
    description="Face shape detection and glasses frame recommendations.",
    version="0.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

mp_face_mesh = mp.solutions.face_mesh

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}

# Styles excluded from recommendations for likely-male users.
# Checked as a case-insensitive substring against the style name.
_CAT_EYE_TERMS = {"cat-eye", "cat eye"}


def _estimate_gender(jaw_ratio: float, height_ratio: float) -> str:
    """
    Estimates likely gender from facial geometry ratios extracted by MediaPipe.

    Returns 'male', 'female', or 'unknown'. Conservative by design —
    returns 'unknown' whenever signals are ambiguous so that frame
    recommendations are never incorrectly narrowed.

    Never exposed in the app interface or API response.
    """
    # Wide jaw + face not too elongated → strong male indicator.
    # jaw_ratio ≥ 0.90 sits well above the female mean (~0.80–0.86)
    # and catches most structurally square / broad male faces.
    if jaw_ratio >= 0.90 and height_ratio < 1.50:
        return "male"

    # Distinctly narrow jaw → female indicator (heart / soft oval faces).
    if jaw_ratio < 0.79:
        return "female"

    # Ambiguous mid-range — default to unknown to avoid false exclusions.
    return "unknown"


def _is_cat_eye(style: str) -> bool:
    s = style.lower()
    return any(term in s for term in _CAT_EYE_TERMS)


def _analyse_face(image_bytes: bytes) -> tuple[str, str]:
    """
    Runs MediaPipe FaceMesh on the image and returns (shape, gender).

    shape  — one of: oval | round | square | heart | oblong | no_face_detected
    gender — one of: male | female | unknown
    """
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image. Make sure you upload a valid JPEG, PNG, or WebP file.")

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as face_mesh:
        results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return "no_face_detected", "unknown"

        landmarks = results.multi_face_landmarks[0].landmark
        h, w, _ = img.shape

        # ── Landmark indices ─────────────────────────────────────────────────
        # 10  = forehead top centre
        # 152 = chin bottom
        # 234 = widest left cheek point  (bizygomatic baseline)
        # 454 = widest right cheek point
        # 172 = left jaw angle
        # 397 = right jaw angle
        # 54  = left outer forehead/brow
        # 284 = right outer forehead/brow
        face_top   = landmarks[10]
        face_bot   = landmarks[152]
        cheek_l    = landmarks[234]
        cheek_r    = landmarks[454]
        jaw_l      = landmarks[172]
        jaw_r      = landmarks[397]
        forehead_l = landmarks[54]
        forehead_r = landmarks[284]

        face_height    = abs(face_top.y   - face_bot.y)   * h
        cheek_width    = abs(cheek_l.x    - cheek_r.x)    * w
        jaw_width      = abs(jaw_l.x      - jaw_r.x)      * w
        forehead_width = abs(forehead_l.x - forehead_r.x) * w

        height_ratio   = face_height    / cheek_width
        jaw_ratio      = jaw_width      / cheek_width
        forehead_ratio = forehead_width / cheek_width

        # ── Face shape ───────────────────────────────────────────────────────
        if height_ratio > 1.55:
            shape = "oblong"
        elif jaw_ratio < 0.76 and forehead_ratio > (jaw_ratio + 0.08):
            shape = "heart"
        elif jaw_ratio > 0.87 and height_ratio < 1.40:
            shape = "square"
        elif height_ratio < 1.25:
            shape = "round"
        else:
            shape = "oval"

        # ── Gender estimation (internal only) ────────────────────────────────
        gender = _estimate_gender(jaw_ratio, height_ratio)

        return shape, gender


def detect_face_shape(image_bytes: bytes) -> str:
    """Public helper used by /detect — returns shape only."""
    shape, _ = _analyse_face(image_bytes)
    return shape


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    return {"status": "FrameHub backend running", "version": "0.3.0"}


@app.post("/detect", tags=["Detection"])
async def detect(file: UploadFile = File(...)):
    """
    Upload a face photo and get back the detected face shape.

    Returns: `{ "face_shape": "<shape>" }`
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{file.content_type}'. Please upload JPEG, PNG, or WebP.",
        )

    contents = await file.read()

    try:
        shape = detect_face_shape(contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"face_shape": shape}


@app.post("/recommend", tags=["Recommendations"])
async def recommend(face_shape: str):
    """
    Get frame style recommendations for a known face shape.

    Pass `face_shape` as a query parameter:  `/recommend?face_shape=oval`

    Supported shapes: `oval`, `round`, `square`, `heart`, `oblong`
    """
    valid_shapes = {"oval", "round", "square", "heart", "oblong"}
    if face_shape.lower() not in valid_shapes:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown face shape '{face_shape}'. Valid options: {', '.join(sorted(valid_shapes))}",
        )

    return get_recommendation(face_shape)


@app.post("/scan", tags=["Scan"])
async def scan(file: UploadFile = File(...)):
    """
    All-in-one endpoint: upload a photo and get back the full frame recommendations.

    Returns:
    ```json
    {
      "face_shape": "oval",
      "description": "...",
      "recommended": [ { "style": "Aviator", "reason": "..." }, ... ],
      "avoid":       [ { "style": "Narrow frames", "reason": "..." }, ... ],
      "tip": "..."
    }
    ```
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{file.content_type}'. Please upload JPEG, PNG, or WebP.",
        )

    contents = await file.read()

    try:
        shape, gender = _analyse_face(contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if shape == "no_face_detected":
        raise HTTPException(
            status_code=422,
            detail="No face detected in the image. Please upload a clear, well-lit photo facing the camera.",
        )

    reco = get_recommendation(shape)

    # Remove cat-eye styles for likely-male users. All gender logic stays
    # server-side; gender is never included in the response.
    if gender == "male":
        reco["recommended"] = [
            item for item in reco["recommended"]
            if not _is_cat_eye(item["style"])
        ]

    return reco

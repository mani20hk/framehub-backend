from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import mediapipe as mp

from recommendations import get_recommendation

app = FastAPI(
    title="FrameHub API",
    description="Face shape detection and glasses frame recommendations.",
    version="0.2.0",
)

# Allow requests from the mobile app / browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

mp_face_mesh = mp.solutions.face_mesh

# ---------------------------------------------------------------------------
# Face shape detection
# ---------------------------------------------------------------------------

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


def detect_face_shape(image_bytes: bytes) -> str:
    """
    Runs MediaPipe FaceMesh on the image bytes and returns one of:
    oval | round | square | heart | oblong | no_face_detected
    """
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image. Make sure you upload a valid JPEG, PNG, or WebP file.")

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as face_mesh:
        results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return "no_face_detected"

        landmarks = results.multi_face_landmarks[0].landmark
        h, w, _ = img.shape

        # Key landmark indices (calibrated against real MediaPipe measurements)
        # 10  = forehead top centre
        # 152 = chin bottom
        # 234 = widest left cheek point  (reference width baseline)
        # 454 = widest right cheek point
        # 172 = left jaw angle
        # 397 = right jaw angle
        # 54  = left outer brow/forehead  (NOT 21 — that's the temple, ~96 % of cheek width)
        # 284 = right outer brow/forehead (mirror of 54)
        face_top      = landmarks[10]
        face_bot      = landmarks[152]
        cheek_l       = landmarks[234]
        cheek_r       = landmarks[454]
        jaw_l         = landmarks[172]
        jaw_r         = landmarks[397]
        forehead_l    = landmarks[54]
        forehead_r    = landmarks[284]

        face_height    = abs(face_top.y   - face_bot.y)   * h
        cheek_width    = abs(cheek_l.x    - cheek_r.x)    * w
        jaw_width      = abs(jaw_l.x      - jaw_r.x)      * w
        forehead_width = abs(forehead_l.x - forehead_r.x) * w

        # All ratios are normalised to cheek_width so they are scale-invariant.
        height_ratio   = face_height    / cheek_width   # typical selfie: 1.20–1.55
        jaw_ratio      = jaw_width      / cheek_width   # typical selfie: 0.76–0.92
        forehead_ratio = forehead_width / cheek_width   # typical selfie: 0.83–0.93

        # Decision tree — oval is the *fallback*, not an easy-hit middle branch.
        #
        # oblong : noticeably tall face
        if height_ratio > 1.55:
            return "oblong"

        # heart  : narrow jaw, wide forehead  (pointy-chin / widow's-peak look)
        if jaw_ratio < 0.76 and forehead_ratio > (jaw_ratio + 0.08):
            return "heart"

        # square : strong wide jaw, face not too tall
        if jaw_ratio > 0.87 and height_ratio < 1.40:
            return "square"

        # round  : face is short / wide relative to cheeks
        if height_ratio < 1.25:
            return "round"

        # oval   : proportionate — taller than round, no dominant jaw or narrow chin
        return "oval"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    return {"status": "FrameHub backend running", "version": "0.2.0"}


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

    Returns a full style profile with recommended frames, frames to avoid, and a tip.
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
    All-in-one endpoint: upload a photo and get back both the detected
    face shape **and** the full frame recommendations in one call.

    Returns:
    ```json
    {
      "face_shape": "oval",
      "description": "...",
      "recommended": [ { "style": "Aviator", "reason": "..." }, ... ],
      "avoid":       [ { "style": "Oversized frames", "reason": "..." }, ... ],
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
        shape = detect_face_shape(contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if shape == "no_face_detected":
        raise HTTPException(
            status_code=422,
            detail="No face detected in the image. Please upload a clear, well-lit photo facing the camera.",
        )

    return get_recommendation(shape)

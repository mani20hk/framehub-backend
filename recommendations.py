"""
FrameHub — Frame recommendation data by face shape.

Each entry contains:
  - description: short blurb about the face shape
  - recommended: list of {style, reason} dicts
  - avoid: list of {style, reason} dicts
  - tip: one actionable styling tip
"""

FRAME_RECOMMENDATIONS = {
    "oval": {
        "description": (
            "Oval faces have balanced proportions with a slightly wider forehead "
            "that gently tapers to a rounded chin. Almost any frame works — "
            "the goal is to preserve that natural balance."
        ),
        "recommended": [
            {
                "style": "Aviator",
                "reason": "Teardrop lenses complement the soft curves of an oval face and add a classic, versatile look.",
            },
            {
                "style": "Wayfarer",
                "reason": "The bold, angular top edge adds definition without overpowering balanced features.",
            },
            {
                "style": "Square / Rectangle",
                "reason": "Geometric angles create a nice contrast with the oval's soft lines, adding sharpness.",
            },
            {
                "style": "Geometric",
                "reason": "Hexagonal or other angular shapes highlight the face's natural symmetry beautifully.",
            },
        ],
        "avoid": [
            {
                "style": "Oversized frames",
                "reason": "Very large frames overwhelm balanced proportions and hide your face's natural harmony.",
            },
            {
                "style": "Extremely narrow frames",
                "reason": "Tiny lenses look disproportionate on an oval face and break its balanced silhouette.",
            },
        ],
        "tip": "Focus on frame width — look for a pair that matches or slightly exceeds your face width for the most balanced look.",
    },

    "round": {
        "description": (
            "Round faces have soft curves with a face width and length that are "
            "nearly equal and full cheeks. Angular, elongating frames help add "
            "definition and make the face appear longer and slimmer."
        ),
        "recommended": [
            {
                "style": "Square / Rectangle",
                "reason": "Sharp corners and straight lines add strong angles that contrast the face's soft curves.",
            },
            {
                "style": "Browline (Club Master)",
                "reason": "The bold top bar draws the eye upward, creating the illusion of length and adding structure.",
            },
            {
                "style": "Cat-Eye",
                "reason": "Upswept outer edges lift the face visually and add angles that slim rounded features.",
            },
            {
                "style": "Geometric",
                "reason": "Angular or hexagonal shapes break up the roundness and give the face more definition.",
            },
        ],
        "avoid": [
            {
                "style": "Round frames",
                "reason": "Circular lenses mirror the face shape and emphasize its roundness rather than balancing it.",
            },
            {
                "style": "Small / narrow frames",
                "reason": "Undersized frames sit in the middle of a round face and make it appear larger by comparison.",
            },
        ],
        "tip": "Look for frames that are wider than they are tall — the horizontal emphasis lengthens the face.",
    },

    "square": {
        "description": (
            "Square faces have a strong, defined jawline with a broad forehead "
            "and nearly equal face width and length. Rounded or curved frames "
            "soften the angular features and add balance."
        ),
        "recommended": [
            {
                "style": "Round",
                "reason": "Circular frames directly contrast the jaw's hard angles and soften the overall look.",
            },
            {
                "style": "Oval / Rimless",
                "reason": "Gently curved lenses and minimal frames soften a strong jawline without adding bulk.",
            },
            {
                "style": "Aviator",
                "reason": "The teardrop curve introduces softness while the browbar maintains a confident look.",
            },
            {
                "style": "Cat-Eye",
                "reason": "Upswept curves draw attention upward and away from the jaw, softening overall structure.",
            },
        ],
        "avoid": [
            {
                "style": "Square / Rectangle",
                "reason": "Angular frames echo the jawline's sharpness and make square features look harsher.",
            },
            {
                "style": "Geometric (sharp angles)",
                "reason": "Hard hexagonal or angular shapes amplify the face's existing strong structure.",
            },
        ],
        "tip": "Frames that sit high on the nose with a narrow or rimless bottom draw the eye upward and create a more balanced silhouette.",
    },

    "heart": {
        "description": (
            "Heart-shaped faces are wider at the forehead and temples, tapering "
            "to a narrower chin. The goal is to balance the wider top half by "
            "adding visual weight to the lower half of the face."
        ),
        "recommended": [
            {
                "style": "Aviator",
                "reason": "Wider at the bottom than the top, aviators perfectly balance a wider forehead with a narrow chin.",
            },
            {
                "style": "Round",
                "reason": "Curved lower rims add fullness near the chin area, visually balancing the narrow jaw.",
            },
            {
                "style": "Light / Rimless",
                "reason": "Thin or rimless frames minimise top-of-face emphasis, keeping the forehead from looking dominant.",
            },
            {
                "style": "Oval",
                "reason": "Gentle width at the middle and soft curves create harmony between the wide forehead and pointed chin.",
            },
        ],
        "avoid": [
            {
                "style": "Cat-Eye",
                "reason": "Upswept frames add more visual weight to an already wide forehead, exaggerating the imbalance.",
            },
            {
                "style": "Decorative top-heavy frames",
                "reason": "Embellishments or thick top rims draw the eye upward, emphasising forehead width.",
            },
        ],
        "tip": "Look for frames that are wider at the bottom or have a low bridge — this shifts visual focus to the lower half of your face.",
    },

    "oblong": {
        "description": (
            "Oblong (also called 'long') faces are noticeably longer than they "
            "are wide, with a straight cheekline. Wide, oversized frames add "
            "width and help shorten the appearance of the face."
        ),
        "recommended": [
            {
                "style": "Oversized / Wide frames",
                "reason": "Large, wide lenses span more of the face horizontally, visually shortening its length.",
            },
            {
                "style": "Round",
                "reason": "Wide round frames add breadth and break up the vertical length of an oblong face.",
            },
            {
                "style": "Browline (Club Master)",
                "reason": "The horizontal bar across the top creates a strong width line that interrupts the face's length.",
            },
            {
                "style": "Butterfly / Wayfarer",
                "reason": "Flared outer edges and wide silhouettes add horizontal presence and reduce the face's apparent length.",
            },
        ],
        "avoid": [
            {
                "style": "Narrow / small frames",
                "reason": "Tiny lenses leave lots of empty face around them, making the face look even longer.",
            },
            {
                "style": "Rimless",
                "reason": "Invisible frames provide no horizontal visual anchor, letting the face's length go unbroken.",
            },
            {
                "style": "Very tall lenses",
                "reason": "Tall rectangular lenses add vertical height and elongate the face further.",
            },
        ],
        "tip": "Choose frames with a strong horizontal line — thick top bars, wide temples, or decorative sides all add visual presence.",
    },
}


def get_recommendation(face_shape: str) -> dict:
    """
    Returns the full style profile for a given face shape.
    Falls back to a generic response if the shape is unknown.
    """
    shape = face_shape.lower()
    if shape in FRAME_RECOMMENDATIONS:
        return {
            "face_shape": shape,
            **FRAME_RECOMMENDATIONS[shape],
        }

    # Fallback for unrecognised shapes
    return {
        "face_shape": shape,
        "description": "Face shape could not be classified with confidence.",
        "recommended": [],
        "avoid": [],
        "tip": "Try uploading a clearer, well-lit photo looking straight at the camera.",
    }

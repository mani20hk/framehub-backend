"""
FrameHub — Frame recommendation data by face shape.
Expanded to 15 recommended styles per shape for varied, non-repetitive results.
"""

FRAME_RECOMMENDATIONS = {
    "oval": {
        "description": (
            "Oval faces have balanced proportions with a slightly wider forehead "
            "that gently tapers to a rounded chin. Almost any frame works — "
            "the goal is to preserve that natural balance."
        ),
        "recommended": [
            {"style": "Aviator",        "reason": "The teardrop lens adds a classic, versatile quality that plays well with balanced features."},
            {"style": "Wayfarer",       "reason": "The bold angular top edge adds definition and a confident look without overpowering."},
            {"style": "Square / Rectangle", "reason": "Geometric angles create a striking contrast with soft, balanced proportions."},
            {"style": "Geometric",      "reason": "Hexagonal or angular shapes highlight natural symmetry and add a modern edge."},
            {"style": "Cat-Eye",        "reason": "Upswept outer corners add flair and a stylish retro-modern contrast."},
            {"style": "Browline",       "reason": "The bold top bar adds structure and a classic statement without overwhelming balance."},
            {"style": "Round",          "reason": "Circular frames bring a softer quality that plays nicely against proportionate features."},
            {"style": "Oval",           "reason": "Gently curved lenses echo natural proportions for an effortlessly polished look."},
            {"style": "Oversized",      "reason": "Large frames make a bold fashion statement while maintaining visual harmony."},
            {"style": "Rimless",        "reason": "The barely-there aesthetic keeps the focus entirely on natural features."},
            {"style": "Semi-Rimless",   "reason": "A partial frame creates a modern floating effect with understated style."},
            {"style": "Butterfly",      "reason": "Dramatically flared outer edges create an eye-catching look that stays balanced."},
            {"style": "Navigator",      "reason": "The large teardrop shape commands presence with a classic, confident appeal."},
            {"style": "Wire Frame",     "reason": "Delicate metal wires offer a refined, intellectual minimalism."},
            {"style": "D-Frame",        "reason": "The flat inner edge adds a geometric detail that looks sharp and distinctly modern."},
            {"style": "Horn-Rimmed",    "reason": "Bold acetate top rims add vintage character and strong visual definition."},
        ],
        "avoid": [
            {"style": "Extremely narrow frames", "reason": "Tiny lenses appear disproportionate and disrupt the natural visual balance."},
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
            {"style": "Square / Rectangle", "reason": "Sharp corners and straight lines provide a strong contrast to softer curves."},
            {"style": "Browline",         "reason": "The bold top bar draws the eye upward, creating an elongating visual effect."},
            {"style": "Cat-Eye",          "reason": "Upswept corners add sharp angles that create definition and lift."},
            {"style": "Geometric",        "reason": "Angular hexagonal or polygonal shapes break symmetry and add structure."},
            {"style": "Wayfarer",         "reason": "The angular frame adds bold definition and creates a slimming visual elongation."},
            {"style": "Navigator",        "reason": "The strong angular silhouette adds definition and upward-drawing presence."},
            {"style": "D-Frame",          "reason": "The flat top edge creates a strong horizontal structure with visual impact."},
            {"style": "Wide Rectangle",   "reason": "Horizontal emphasis stretches the visual silhouette, creating a longer appearance."},
            {"style": "Semi-Rimless",     "reason": "The visible top bar adds structure while the open bottom keeps the look light."},
            {"style": "Horn-Rimmed",      "reason": "Bold angular acetate frames add strong definition and vintage character."},
            {"style": "Angular Browline", "reason": "A sharper browline adds pronounced definition and visually lifts the upper face."},
            {"style": "Flat Top",         "reason": "The strong flat upper edge creates a clear horizontal structure and sharp look."},
            {"style": "Keyhole Bridge",   "reason": "The vertical bridge detail adds a point of interest that interrupts softness."},
            {"style": "Rectangular Rimless", "reason": "The elongated minimal shape adds width without adding visual weight."},
            {"style": "Bold Geometric",   "reason": "Strong angular polygonal shapes add dramatic contrast to smooth curves."},
        ],
        "avoid": [
            {"style": "Round frames",         "reason": "Circular lenses mirror and emphasise existing softness rather than balancing it."},
            {"style": "Small / narrow frames","reason": "Undersized frames sit in the centre of the face and make surrounding features appear larger."},
        ],
        "tip": "Look for frames that are wider than they are tall — the horizontal emphasis creates a more elongated silhouette.",
    },

    "square": {
        "description": (
            "Square faces have a strong, defined jawline with a broad forehead "
            "and nearly equal face width and length. Rounded or curved frames "
            "soften the angular features and add balance."
        ),
        "recommended": [
            {"style": "Round",             "reason": "Circular frames directly contrast strong angular features and soften the overall look."},
            {"style": "Oval / Rimless",    "reason": "Gently curved lenses minimise frame presence while softening angular lines."},
            {"style": "Aviator",           "reason": "The teardrop curve introduces softness while the browbar keeps a confident look."},
            {"style": "Cat-Eye",           "reason": "Upswept curves draw the eye upward and away from the lower face."},
            {"style": "Semi-Rimless",      "reason": "An open lower frame lightens the look and reduces angular emphasis."},
            {"style": "Wire Frame Oval",   "reason": "Ultra-thin metal wires with oval lenses offer a delicate, softening look."},
            {"style": "Round Acetate",     "reason": "Bold round acetate creates strong circular contrast to angular lines."},
            {"style": "Butterfly",         "reason": "The graceful flared shape introduces softness while adding an expressive flair."},
            {"style": "D-Frame Round",     "reason": "A semi-circular shape softens lines while the subtle flat edge maintains balance."},
            {"style": "Oval Titanium",     "reason": "Ultra-lightweight titanium oval frames offer a refined and minimal softening."},
            {"style": "Soft Rectangular",  "reason": "Rounded corners on a rectangular frame offer softening without losing structure."},
            {"style": "Round Tortoiseshell","reason": "Warm tortoiseshell acetate in a round shape adds both softness and character."},
            {"style": "Oval Metal",        "reason": "Thin metal oval frames provide a subtle, understated softening effect."},
            {"style": "Clear Round",       "reason": "Transparent round frames add modern, minimalist softness."},
            {"style": "Browline Oval",     "reason": "Soft oval lenses with a browline frame balance structure with curvature."},
        ],
        "avoid": [
            {"style": "Square / Rectangle",     "reason": "Angular frames echo existing hard lines and make the overall look feel harsher."},
            {"style": "Geometric (sharp angles)","reason": "Hard hexagonal or angular shapes amplify existing strong structural features."},
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
            {"style": "Aviator",           "reason": "Wider at the bottom than the top, the teardrop shape perfectly balances proportions."},
            {"style": "Round",             "reason": "Curved lower rims add fullness in the lower face area for visual balance."},
            {"style": "Light / Rimless",   "reason": "Minimal frames reduce visual emphasis at the top of the face."},
            {"style": "Oval",              "reason": "Gentle oval width at the midpoint creates softness and natural harmony."},
            {"style": "Semi-Rimless",      "reason": "The lighter top half reduces emphasis in the upper face area."},
            {"style": "Teardrop",          "reason": "The bottom-heavy teardrop shape naturally shifts visual weight toward the lower face."},
            {"style": "Low Bridge Oval",   "reason": "A low-set bridge shifts the visual centre of the frame downward."},
            {"style": "Round Metal",       "reason": "Lightweight metal circles add lower face fullness with minimal top presence."},
            {"style": "Oval Acetate",      "reason": "Warm acetate oval frames bring fullness to the mid-lower face area."},
            {"style": "Butterfly",         "reason": "Wider at the middle, butterfly frames add breadth through the mid face."},
            {"style": "Round Titanium",    "reason": "Ultra-light titanium rounds add circular fullness without weight or bulk."},
            {"style": "Oval Rimless",      "reason": "Nearly invisible frames eliminate top-heavy visual emphasis entirely."},
            {"style": "Soft Round",        "reason": "Gentle curves provide lower face fullness in an understated way."},
            {"style": "Wide Bottom Frame", "reason": "Frames wider at the base maximise visual weight in the lower face."},
            {"style": "Round Tortoiseshell","reason": "Warm rounded frames add both fullness and character to the lower face."},
        ],
        "avoid": [
            {"style": "Cat-Eye",                  "reason": "Upswept frames add more visual weight to the already-wider upper face area."},
            {"style": "Decorative top-heavy frames","reason": "Embellishments or thick top rims draw the eye upward, exaggerating the upper-lower imbalance."},
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
            {"style": "Oversized / Wide",   "reason": "Large wide lenses add horizontal presence and visually shorten the face."},
            {"style": "Round",              "reason": "Wide circular frames add breadth and interrupt vertical length."},
            {"style": "Browline",           "reason": "The bold horizontal bar creates a strong width line across the face."},
            {"style": "Butterfly / Wayfarer","reason": "Flared outer edges and wide silhouettes add horizontal presence."},
            {"style": "Wide Rectangle",     "reason": "A broad rectangular frame adds strong horizontal emphasis."},
            {"style": "Navigator",          "reason": "The large, wide teardrop shape adds both breadth and bold presence."},
            {"style": "Bold Browline",      "reason": "A thick dominant browbar creates maximum horizontal visual impact."},
            {"style": "Round Acetate",      "reason": "Large round acetate frames add significant circular breadth."},
            {"style": "Wide Cat-Eye",       "reason": "The horizontal wing adds width while the upswept corners add dimension."},
            {"style": "Retro Oversized",    "reason": "Vintage-inspired large frames deliver strong horizontal width."},
            {"style": "Club Master Wide",   "reason": "A broad club master frame maximises the width-creating effect."},
            {"style": "Decorative Top Bar", "reason": "Embellishments on the top rim create a strong horizontal visual anchor."},
            {"style": "Wide Tortoiseshell", "reason": "Bold wide acetate in tortoiseshell adds width and warm visual depth."},
            {"style": "Hexagonal Wide",     "reason": "A wide geometric hexagonal frame adds structured horizontal breadth."},
            {"style": "Square Wide",        "reason": "A broad angular frame delivers both horizontal and structural presence."},
        ],
        "avoid": [
            {"style": "Narrow / small frames","reason": "Small lenses emphasise surrounding space and make the face appear even longer."},
            {"style": "Rimless",              "reason": "Invisible frames provide no horizontal visual anchor."},
            {"style": "Very tall lenses",     "reason": "Tall rectangular lenses add vertical emphasis, extending length further."},
        ],
        "tip": "Choose frames with a strong horizontal line — thick top bars, wide temples, or decorative sides all add visual presence.",
    },
}


def get_recommendation(face_shape: str) -> dict:
    """Returns the full style profile for a given face shape."""
    shape = face_shape.lower()
    if shape in FRAME_RECOMMENDATIONS:
        return {
            "face_shape": shape,
            **FRAME_RECOMMENDATIONS[shape],
        }
    return {
        "face_shape": shape,
        "description": "Face shape could not be classified with confidence.",
        "recommended": [],
        "avoid": [],
        "tip": "Try uploading a clearer, well-lit photo looking straight at the camera.",
    }

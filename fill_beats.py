"""
fill_beats.py

WHAT THIS DOES:
Reads your example-script.json (the one generate_multivoice.py already
made, with your REAL audio timing baked in) and fills in sensible visual
"beats" for every scene, based on keywords in the caption text. Your
timing is never touched — only the "beat" field of each scene is updated.

HOW TO USE:
1. Make sure example-script.json already exists (from generate_multivoice.py)
2. Run: python fill_beats.py
3. It overwrites example-script.json in place, now with visuals filled in
4. Preview with `npm start`, and hand-edit any individual scene's beat in
   the JSON afterward if something doesn't feel right - this script gets
   you 90% of the way, not a perfect final cut.
"""

import json
import re
from pathlib import Path

SCRIPT_FILE = Path("src/scripts/example-script.json")

# Order matters - first matching rule wins. Add your own rules here over
# time as you write more scripts; this list is meant to grow.
RULES = [
    # (regex pattern, beat-building function)
    (r"\bepictetus\b", lambda m: {"type": "singleFigure", "label": "Epictetus", "icon": "📜"}),
    (r"\bmarcus aurelius\b", lambda m: {"type": "singleFigure", "label": "Marcus Aurelius", "icon": "👑"}),
    (r"\bemperor\b", lambda m: {"type": "singleFigure", "label": "Marcus Aurelius", "icon": "👑"}),
    (r"\bslave|slavery\b", lambda m: {"type": "singleFigure", "label": "Epictetus", "icon": "⛓️"}),
    (r"\bjournal|wrote\b", lambda m: {"type": "singleFigure", "label": "Marcus Aurelius", "icon": "📖"}),
    (r"\bdichotomy of control|up to you|not up to you\b",
     lambda m: {"type": "twoFigures", "leftLabel": "Yours", "rightLabel": "Not Yours",
                "leftIcon": "✅", "rightIcon": "❌"}),
    (r"\bcontrol\b.*\bcan't control|can't control\b",
     lambda m: {"type": "twoFigures", "leftLabel": "Yours", "rightLabel": "Not Yours",
                "leftIcon": "✅", "rightIcon": "❌"}),
    (r"\banxiety|anxious|afraid|fear|worry|worrying|worried\b",
     lambda m: {"type": "singleFigure", "label": "You", "icon": "😰"}),
    (r"\bpremeditatio malorum|worst case|worst version|rehearse\b",
     lambda m: {"type": "singleFigure", "label": "You", "icon": "🌩️"}),
    (r"\bdecatastrophizing|psycholog|research|clinical\b",
     lambda m: {"type": "singleFigure", "label": "Research", "icon": "🔬"}),
    (r"\bview from above|zoom out|planet|space\b",
     lambda m: {"type": "singleFigure", "label": "You", "icon": "🌍"}),
    (r"\bpresentation|interview|job\b",
     lambda m: {"type": "singleFigure", "label": "You", "icon": "💼"}),
    (r"\brelationship|loves you\b",
     lambda m: {"type": "singleFigure", "label": "You", "icon": "❤️"}),
    (r"\bsubscribe|next week|cognitive bias\b",
     lambda m: {"type": "singleFigure", "label": "Wired Wrong", "icon": "💡"}),
    (r"\bschool|teaching|free man\b",
     lambda m: {"type": "singleFigure", "label": "Epictetus", "icon": "🎓"}),
]

DEFAULT_BEAT = {"type": "singleFigure", "label": "You", "icon": "🧠"}


def choose_beat(caption: str):
    lowered = caption.lower()
    for pattern, builder in RULES:
        if re.search(pattern, lowered):
            beat = builder(None)
            beat["animation"] = "bounceIn"
            return beat
    beat = dict(DEFAULT_BEAT)
    beat["animation"] = "bounceIn"
    return beat


def main():
    if not SCRIPT_FILE.exists():
        print(f"ERROR: {SCRIPT_FILE} not found. Run generate_multivoice.py first.")
        raise SystemExit(1)

    data = json.loads(SCRIPT_FILE.read_text(encoding="utf-8"))
    scenes = data["scenes"]

    for scene in scenes:
        scene["beat"] = choose_beat(scene["caption"])

    SCRIPT_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Filled in beats for {len(scenes)} scenes.")
    print("Preview with `npm start`, then hand-tune any scene that feels off.")


if __name__ == "__main__":
    main()

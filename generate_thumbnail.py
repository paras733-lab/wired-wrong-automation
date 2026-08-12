"""
generate_thumbnail.py

WHAT THIS DOES:
Picks the single most attention-grabbing short line from the episode
(reusing the same "hookiness" scoring used for Shorts), wraps it onto
2-3 short lines for a thumbnail, picks a fitting icon based on keywords
in the episode, and writes thumbnail-data.json for the Thumbnail
composition to render.

RUN THIS AFTER generate_multivoice.py (needs example-script.json to exist).
"""

import json
import re
import textwrap
from pathlib import Path

SOURCE_SCRIPT = Path("src/scripts/example-script.json")
OUTPUT_DATA = Path("src/scripts/thumbnail-data.json")

ICON_RULES = [
    (r"\bepictetus|marcus aurelius|seneca|stoic|philosoph", "📜"),
    (r"\bbias|fallacy|brain|psycholog|cognitive", "🧠"),
    (r"\bmoney|cost|lose|loss|financ", "💰"),
    (r"\bdeath|mortal|memento", "⏳"),
    (r"\bconfiden|dunning|kruger", "🎯"),
]
DEFAULT_ICON = "⚡"


def pick_icon(title: str) -> str:
    lowered = title.lower()
    for pattern, icon in ICON_RULES:
        if re.search(pattern, lowered):
            return icon
    return DEFAULT_ICON


def score_line(text: str) -> float:
    score = 0.0
    word_count = len(text.split())
    if word_count <= 8:
        score += 3
    if "?" in text:
        score += 1.5
    if re.search(r"\byou\b|\byour\b", text.lower()):
        score += 1
    if word_count <= 4:
        score += 1  # extra-short lines make the boldest thumbnail text
    return score


def wrap_headline(text: str) -> str:
    # Keep it big and punchy - wrap to at most 3 short lines.
    words = text.rstrip(".").split()
    lines = textwrap.wrap(" ".join(words), width=14, max_lines=3, placeholder="")
    return "\n".join(lines)


def main():
    data = json.loads(SOURCE_SCRIPT.read_text(encoding="utf-8"))
    scenes = data["scenes"]

    best_scene = max(scenes, key=lambda s: score_line(s["caption"]))
    headline = wrap_headline(best_scene["caption"])
    icon = pick_icon(data.get("title", ""))

    OUTPUT_DATA.write_text(json.dumps({"headline": headline, "icon": icon}, indent=2), encoding="utf-8")
    print(f"Thumbnail headline: {headline!r}")
    print(f"Icon: {icon}")


if __name__ == "__main__":
    main()

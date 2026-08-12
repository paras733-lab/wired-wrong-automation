"""
enrich_metadata.py

WHAT THIS DOES:
Takes the short description already written in video_metadata.json and
expands it into a full 150-220 word SEO-friendly description, built from
the episode's own script content - no external AI call, fully
deterministic, fully free. Overwrites the "description" field in
video_metadata.json in place.

RUN THIS after generate_multivoice.py (needs example-script.json) and
after video_metadata.json has been copied in from the queue.
"""

import json
import re
from pathlib import Path

SOURCE_SCRIPT = Path("src/scripts/example-script.json")
METADATA_FILE = Path("video_metadata.json")
TARGET_WORDS = (150, 220)


def pick_teaser_sentences(scenes, count=3):
    """Pick a few substantial, spaced-out M-tagged sentences from the
    middle of the episode to use as a content teaser in the description -
    gives search engines real topical text without spoiling the ending."""
    mid_scenes = [s for s in scenes if s.get("speaker") == "M" and len(s["caption"].split()) >= 12]
    if not mid_scenes:
        mid_scenes = [s for s in scenes if len(s["caption"].split()) >= 12]

    # Spread picks across the middle 60% of the episode, not the very
    # start (already used as the hook) or very end (spoiler territory).
    n = len(mid_scenes)
    if n == 0:
        return []
    start_idx = int(n * 0.2)
    end_idx = int(n * 0.8)
    pool = mid_scenes[start_idx:end_idx] or mid_scenes
    step = max(1, len(pool) // count)
    return [pool[i]["caption"] for i in range(0, len(pool), step)][:count]


def build_description(existing_desc, title, tags, teaser_sentences):
    keyword_line = "Topics covered: " + ", ".join(tags[:6]) + "."

    teaser_para = " ".join(teaser_sentences)

    parts = [
        existing_desc.strip(),
        teaser_para,
        keyword_line,
        "New videos every week, alternating between the psychology of cognitive bias "
        "and practical Stoic philosophy. Subscribe to Wired Wrong for the full series.",
    ]
    full = "\n\n".join(p for p in parts if p)

    word_count = len(full.split())
    if word_count < TARGET_WORDS[0]:
        full += ("\n\nIf you found this useful, the best way to catch every new video "
                 "is to subscribe and turn on notifications.")
    return full


def main():
    if not METADATA_FILE.exists():
        print("No video_metadata.json found, skipping enrichment.")
        return

    data = json.loads(SOURCE_SCRIPT.read_text(encoding="utf-8"))
    metadata = json.loads(METADATA_FILE.read_text(encoding="utf-8"))

    teaser_sentences = pick_teaser_sentences(data["scenes"])
    enriched = build_description(
        metadata.get("description", ""),
        metadata.get("title", ""),
        metadata.get("tags", []),
        teaser_sentences,
    )

    metadata["description"] = enriched
    METADATA_FILE.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print(f"Description enriched: {len(enriched.split())} words")


if __name__ == "__main__":
    main()

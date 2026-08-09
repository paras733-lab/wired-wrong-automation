"""
generate_short.py

WHAT THIS DOES:
Scans the full long-form episode and finds several strong ~45-second
windows to turn into Shorts - not just the opening. Each window is scored
on how "hook-worthy" it is: short punchy lines, direct "you" address,
questions, and a strong opening line. The single best-scoring window
starting at the very beginning is always included (the real intro hook is
almost always strong, since that's how these scripts are written), plus
the next best non-overlapping windows found elsewhere in the episode.

CHANGE NUM_SHORTS BELOW to produce more or fewer clips per episode.

OUTPUTS (one set per short, numbered 1, 2, 3...):
src/scripts/short-script.json      (overwritten before each render)
public/audio/short-voiceover.mp3   (overwritten before each render)
short_metadata.json                (overwritten before each render)

USAGE (called once per short, from the workflow):
    python generate_short.py --index 1
    python generate_short.py --index 2
    python generate_short.py --index 3
"""

import argparse
import json
import re
import subprocess
from pathlib import Path

SOURCE_SCRIPT = Path("src/scripts/example-script.json")
SOURCE_AUDIO = Path("public/audio/voiceover.mp3")
SOURCE_METADATA = Path("video_metadata.json")
OUTPUT_SCRIPT = Path("src/scripts/short-script.json")
OUTPUT_AUDIO = Path("public/audio/short-voiceover.mp3")
OUTPUT_METADATA = Path("short_metadata.json")

NUM_SHORTS = 3
MAX_SHORT_SECONDS = 48  # leaves comfortable room under YouTube's 60s ceiling
CLOSING_LINE = "Full breakdown on the channel."
CLOSING_DURATION = 3.5


def build_windows(scenes, max_seconds):
    """Every possible contiguous run of scenes starting at each index,
    stopping once adding the next scene would exceed max_seconds."""
    windows = []
    n = len(scenes)
    for start in range(n):
        cum = 0.0
        end = start
        while end < n and cum + scenes[end]["durationInSeconds"] <= max_seconds:
            cum += scenes[end]["durationInSeconds"]
            end += 1
        if end > start and cum >= 15:  # skip windows that are too short to be worth it
            windows.append({"start": start, "end": end, "duration": cum})
    return windows


def score_window(scenes, start, end):
    score = 0.0
    for i in range(start, end):
        s = scenes[i]
        caption = s["caption"]
        if s.get("speaker") == "F":  # already-flagged emphasis/punch lines
            score += 2
        if "?" in caption:
            score += 1.5
        if re.search(r"\byou\b|\byour\b", caption.lower()):
            score += 0.5
    # A strong, short opening line matters most - that's the first thing
    # a viewer hears in the first second.
    first_words = len(scenes[start]["caption"].split())
    if first_words <= 12:
        score += 3
    return score


def windows_overlap(a, b):
    return not (a["end"] <= b["start"] or b["end"] <= a["start"])


def select_top_windows(scenes, num_shorts, max_seconds):
    windows = build_windows(scenes, max_seconds)

    # The hook short is always the best-scoring window that starts at
    # scene 0 - the actual cold open of the episode.
    hook_candidates = [w for w in windows if w["start"] == 0]
    hook_window = max(hook_candidates, key=lambda w: score_window(scenes, w["start"], w["end"]))

    selected = [hook_window]
    remaining = [w for w in windows if w["start"] != 0]
    remaining.sort(key=lambda w: score_window(scenes, w["start"], w["end"]), reverse=True)

    for w in remaining:
        if len(selected) >= num_shorts:
            break
        if not any(windows_overlap(w, s) for s in selected):
            selected.append(w)

    return selected[:num_shorts]


def trim_audio(start_seconds, duration_seconds, output_path):
    subprocess.run(
        ["ffmpeg", "-y", "-ss", str(start_seconds), "-i", str(SOURCE_AUDIO),
         "-t", str(duration_seconds), "-c", "copy", str(output_path)],
        capture_output=True, check=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int, required=True, help="Which short to generate (1-based)")
    args = parser.parse_args()

    data = json.loads(SOURCE_SCRIPT.read_text(encoding="utf-8"))
    scenes = data["scenes"]

    windows = select_top_windows(scenes, NUM_SHORTS, MAX_SHORT_SECONDS)
    if args.index > len(windows):
        print(f"Only {len(windows)} short(s) available for this episode, index {args.index} requested.")
        raise SystemExit(1)

    window = windows[args.index - 1]
    hook_scenes = scenes[window["start"]:window["end"]]

    # Figure out the actual start time (in seconds) of this window within
    # the full voiceover, so we trim the right slice of audio.
    start_seconds = sum(s["durationInSeconds"] for s in scenes[:window["start"]])

    scenes_out = list(hook_scenes) + [{
        "id": "short-closer",
        "durationInSeconds": CLOSING_DURATION,
        "caption": CLOSING_LINE,
        "beat": {"type": "singleFigure", "label": "Wired Wrong", "icon": "🎬", "animation": "bounceIn"},
    }]

    output = {
        "title": data.get("title", "Untitled Short"),
        "voiceoverFile": f"audio/{OUTPUT_AUDIO.name}",
        "fps": data["fps"],
        "scenes": scenes_out,
    }
    OUTPUT_SCRIPT.write_text(json.dumps(output, indent=2), encoding="utf-8")
    trim_audio(start_seconds, window["duration"], OUTPUT_AUDIO)

    # Metadata: use this window's actual opening line as the hook-driven
    # title, so each short gets a distinct, relevant title instead of all
    # three sharing the long-form video's title.
    source_meta = json.loads(SOURCE_METADATA.read_text(encoding="utf-8")) if SOURCE_METADATA.exists() else {}
    hook_line = hook_scenes[0]["caption"]
    short_title = hook_line if len(hook_line) <= 80 else hook_line[:77].rstrip() + "..."
    short_title += " #Shorts"

    short_metadata = {
        "title": short_title,
        "description": f"From the full video: {data.get('title', '')}\n\nFull breakdown on the channel.\n#Shorts",
        "tags": list(set(source_meta.get("tags", []) + ["shorts"])),
        "privacyStatus": source_meta.get("privacyStatus", "private"),
    }
    OUTPUT_METADATA.write_text(json.dumps(short_metadata, indent=2), encoding="utf-8")

    print(f"Short {args.index}/{len(windows)}: scenes {window['start']}-{window['end']}, "
          f"~{round(window['duration'] + CLOSING_DURATION, 1)}s, title: {short_title}")


if __name__ == "__main__":
    main()

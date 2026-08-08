"""
generate_scene_timing.py

WHAT THIS SCRIPT DOES (in plain English):
You give it a voiceover audio file (mp3/wav) and your script broken into
sentences. It listens to the audio using Whisper (a free, local speech
recognition tool made by OpenAI) and figures out exactly WHEN each sentence
is spoken. It then writes out a scene JSON file with accurate timing —
so your captions and animations line up with the narration automatically,
no matter how long the video ends up being.

You do NOT need to understand the code to use this. You only need to run
one command (explained in GETTING-STARTED.md) and edit the two input files
described below.

HOW TO USE IT:
1. Put your voiceover file in:      public/audio/voiceover.mp3
2. Put your script sentences in:    src/scripts/narration.txt
   (one sentence per line — this is literally just your script, split
   into lines wherever you'd naturally pause)
3. Run: python generate_scene_timing.py
4. It creates: src/scripts/example-script.json automatically, with real
   timing filled in.
"""

import json
import sys
from pathlib import Path

# whisper is installed via: pip install -U openai-whisper
# (full instructions are in GETTING-STARTED.md)
import whisper

AUDIO_FILE = Path("public/audio/voiceover.mp3")
NARRATION_FILE = Path("src/scripts/narration.txt")
OUTPUT_SCRIPT_FILE = Path("src/scripts/example-script.json")
FPS = 30


def load_sentences() -> list[str]:
    if not NARRATION_FILE.exists():
        print(f"ERROR: Could not find {NARRATION_FILE}")
        print("Create this file with one sentence of your script per line.")
        sys.exit(1)

    lines = [
        line.strip()
        for line in NARRATION_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not lines:
        print("ERROR: narration.txt is empty.")
        sys.exit(1)
    return lines


def transcribe_with_timestamps(audio_path: Path):
    print("Loading Whisper model (first run downloads it, ~150MB, one-time)...")
    # "small" is a good free balance of accuracy vs. speed for this use case.
    # If your machine is slow, you can change this to "base" (faster, slightly
    # less accurate). If you want max accuracy, use "medium" (slower).
    model = whisper.load_model("small")

    print(f"Transcribing {audio_path} — this can take a few minutes...")
    result = model.transcribe(str(audio_path), word_timestamps=True)
    return result


def match_sentences_to_timestamps(sentences, whisper_result):
    """
    Whisper gives us word-by-word timestamps. This walks through your
    original script sentence by sentence and finds where each one starts
    and ends in the audio, by matching words in order.
    """
    all_words = []
    for segment in whisper_result["segments"]:
        for w in segment.get("words", []):
            all_words.append(w)

    scenes = []
    word_cursor = 0

    for i, sentence in enumerate(sentences):
        sentence_word_count = len(sentence.split())
        matched_words = all_words[word_cursor: word_cursor + sentence_word_count]

        if not matched_words:
            print(f"WARNING: ran out of audio words to match sentence {i+1}: '{sentence}'")
            continue

        start_time = matched_words[0]["start"]
        end_time = matched_words[-1]["end"]
        duration = round(end_time - start_time, 2)

        scenes.append({
            "id": f"scene-{i+1}",
            "durationInSeconds": max(duration, 1.5),  # never shorter than 1.5s
            "caption": sentence,
            # Default beat — you or an LLM can customize these per scene
            # afterward. See GETTING-STARTED.md step 6 for how.
            "beat": {
                "type": "singleFigure",
                "label": "",
                "animation": "bounceIn",
            },
        })

        word_cursor += sentence_word_count

    return scenes


def main():
    sentences = load_sentences()
    whisper_result = transcribe_with_timestamps(AUDIO_FILE)
    scenes = match_sentences_to_timestamps(sentences, whisper_result)

    output = {
        "title": "Untitled Video",
        "voiceoverFile": f"audio/{AUDIO_FILE.name}",
        "fps": FPS,
        "scenes": scenes,
    }

    OUTPUT_SCRIPT_FILE.write_text(json.dumps(output, indent=2), encoding="utf-8")
    total_seconds = sum(s["durationInSeconds"] for s in scenes)
    print(f"\nDone. Wrote {len(scenes)} scenes to {OUTPUT_SCRIPT_FILE}")
    print(f"Estimated video length: {round(total_seconds / 60, 1)} minutes")
    print("\nNext: open example-script.json and fill in the 'beat' details")
    print("for each scene (or ask an LLM to do it — see GETTING-STARTED.md).")


if __name__ == "__main__":
    main()

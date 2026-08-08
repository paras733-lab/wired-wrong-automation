"""
generate_multivoice.py

WHAT THIS DOES:
Reads a script where each line is tagged with a speaker ([M] or [F]),
generates each line as a separate audio clip, stitches them together with
SAMPLE-ACCURATE timing (using WAV, not MP3, to avoid encoder padding drift
that accumulates over many clips), and writes out scene timing that is
perfectly accurate.

HOW TO USE:
1. Put your voiceover file in:      src/scripts/narration_tagged.txt
2. Run: python generate_multivoice.py
3. It creates:
   - public/audio/voiceover.mp3
   - src/scripts/example-script.json
"""

import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

NARRATION_FILE = Path("src/scripts/narration_tagged.txt")
TEMP_DIR = Path("temp_voice_clips")
OUTPUT_AUDIO = Path("public/audio/voiceover.mp3")
OUTPUT_SCRIPT = Path("src/scripts/example-script.json")
FPS = 30
PAUSE_BETWEEN_LINES_MS = 250

# Both tags currently point to the same voice - single narrator only.
# If you want to bring back a second voice later, just point "F" at a
# different voice name here, nothing else needs to change.
VOICES = {
    "M": "en-US-ChristopherNeural",
    "F": "en-US-ChristopherNeural",
}
RATE = "+15%"


def parse_tagged_lines():
    if not NARRATION_FILE.exists():
        print(f"ERROR: {NARRATION_FILE} not found.")
        raise SystemExit(1)
    lines = []
    for raw in NARRATION_FILE.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith("[M]"):
            speaker, text = "M", raw[3:].strip()
        elif raw.startswith("[F]"):
            speaker, text = "F", raw[3:].strip()
        else:
            speaker, text = "M", raw
        lines.append((speaker, text))
    return lines


async def synthesize_line_to_wav(text: str, voice: str, wav_path: Path):
    mp3_temp = wav_path.with_suffix(".raw.mp3")
    communicate = edge_tts.Communicate(text, voice, rate=RATE)
    await communicate.save(str(mp3_temp))
    # Convert immediately to WAV - this re-encode gives us a clean,
    # sample-accurate file with no compressed-format boundary artifacts.
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(mp3_temp), "-ar", "24000", "-ac", "1", str(wav_path)],
        capture_output=True, check=True,
    )
    mp3_temp.unlink()


def get_duration_seconds(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def make_silence_clip(path: Path, duration_ms: int):
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
         "-t", str(duration_ms / 1000), str(path)],
        capture_output=True, check=True,
    )


def concatenate_wavs(clip_paths, output_wav: Path):
    list_file = TEMP_DIR / "concat_list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for p in clip_paths:
            f.write(f"file '{p.resolve().as_posix()}'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-c", "copy", str(output_wav)],
        capture_output=True, check=True,
    )


def convert_wav_to_mp3(wav_path: Path, mp3_path: Path):
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav_path), "-codec:a", "libmp3lame",
         "-qscale:a", "2", str(mp3_path)],
        capture_output=True, check=True,
    )


async def main():
    TEMP_DIR.mkdir(exist_ok=True)
    OUTPUT_AUDIO.parent.mkdir(parents=True, exist_ok=True)

    lines = parse_tagged_lines()
    print(f"Found {len(lines)} lines to synthesize...")

    silence_path = TEMP_DIR / "pause.wav"
    make_silence_clip(silence_path, PAUSE_BETWEEN_LINES_MS)

    clip_paths = []
    scenes = []
    cumulative_seconds = 0.0

    for i, (speaker, text) in enumerate(lines):
        voice = VOICES[speaker]
        wav_path = TEMP_DIR / f"line_{i:03d}.wav"
        print(f"  [{i+1}/{len(lines)}] ({speaker}) {text[:60]}...")
        await synthesize_line_to_wav(text, voice, wav_path)

        duration = get_duration_seconds(wav_path)

        scenes.append({
            "id": f"scene-{i+1}",
            "durationInSeconds": round(duration + (PAUSE_BETWEEN_LINES_MS / 1000), 2),
            "caption": text,
            "speaker": speaker,
            "beat": {"type": "singleFigure", "label": "", "animation": "bounceIn"},
        })

        clip_paths.append(wav_path)
        clip_paths.append(silence_path)
        cumulative_seconds += duration + (PAUSE_BETWEEN_LINES_MS / 1000)

    print("Stitching all clips together (sample-accurate WAV concat)...")
    final_wav = TEMP_DIR / "final_stitched.wav"
    concatenate_wavs(clip_paths, final_wav)

    print("Converting final result to MP3...")
    convert_wav_to_mp3(final_wav, OUTPUT_AUDIO)

    output = {
        "title": "Untitled Video",
        "voiceoverFile": f"audio/{OUTPUT_AUDIO.name}",
        "fps": FPS,
        "scenes": scenes,
    }
    OUTPUT_SCRIPT.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"\nDone. Total narration length: {round(cumulative_seconds/60, 1)} minutes")
    print(f"Voiceover saved to: {OUTPUT_AUDIO}")
    print(f"Scene timing saved to: {OUTPUT_SCRIPT}")
    print("\nNext: run fill_beats.py to fill in visuals for each scene.")


if __name__ == "__main__":
    asyncio.run(main())

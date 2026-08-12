"""
upload_to_youtube.py

WHAT THIS DOES:
Uploads out/video.mp4 to your YouTube channel, using the metadata (title,
description, tags) from video_metadata.json. Works both on your own
computer and inside GitHub Actions - it reads credentials from environment
variables either way, so no secrets are ever hardcoded in this file.

REQUIRED ENVIRONMENT VARIABLES (set as GitHub Secrets in Actions, or as
regular environment variables if running this locally):
    YOUTUBE_CLIENT_ID
    YOUTUBE_CLIENT_SECRET
    YOUTUBE_REFRESH_TOKEN
"""

import argparse
import json
import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", default="out/video.mp4", help="Path to the video file to upload")
    parser.add_argument("--metadata", default="video_metadata.json", help="Path to the metadata JSON file")
    parser.add_argument("--thumbnail", default=None, help="Optional path to a custom thumbnail image")
    return parser.parse_args()


def load_credentials():
    client_id = os.environ["YOUTUBE_CLIENT_ID"]
    client_secret = os.environ["YOUTUBE_CLIENT_SECRET"]
    refresh_token = os.environ["YOUTUBE_REFRESH_TOKEN"]

    return Credentials(
        token=None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )


def load_metadata(metadata_file: Path):
    if not metadata_file.exists():
        print(f"WARNING: {metadata_file} not found, using placeholder metadata.")
        return {
            "title": "Untitled Video",
            "description": "",
            "tags": [],
            "privacyStatus": "private",
        }
    return json.loads(metadata_file.read_text(encoding="utf-8"))


def main():
    args = parse_args()
    video_file = Path(args.video)
    metadata_file = Path(args.metadata)

    if not video_file.exists():
        print(f"ERROR: {video_file} not found. Render the video first.")
        raise SystemExit(1)

    metadata = load_metadata(metadata_file)
    credentials = load_credentials()
    youtube = build("youtube", "v3", credentials=credentials)

    body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata.get("tags", []),
            "categoryId": "27",  # Education category
        },
        "status": {
            "privacyStatus": metadata.get("privacyStatus", "private"),
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(str(video_file), chunksize=-1, resumable=True, mimetype="video/mp4")

    print(f"Uploading '{metadata['title']}' as {metadata.get('privacyStatus', 'private')}...")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Upload progress: {int(status.progress() * 100)}%")

    video_id = response["id"]
    print(f"\nDone. Video uploaded: https://youtube.com/watch?v={video_id}")
    print(f"Privacy status: {metadata.get('privacyStatus', 'private')}")

    if args.thumbnail and Path(args.thumbnail).exists():
        print(f"Setting custom thumbnail from {args.thumbnail}...")
        try:
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(args.thumbnail, mimetype="image/png"),
            ).execute()
            print("Thumbnail set successfully.")
        except Exception as e:
            # Custom thumbnails require a phone-verified channel. If this
            # fails, the upload itself still succeeded - just log it and
            # move on rather than failing the whole run.
            print(f"WARNING: could not set custom thumbnail ({e}). "
                  f"This usually means the channel isn't phone-verified yet. "
                  f"The video uploaded fine, YouTube just picked a default thumbnail.")

    print("Review it and switch to Public in YouTube Studio when you're ready.")


if __name__ == "__main__":
    main()

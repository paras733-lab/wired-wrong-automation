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

import json
import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

VIDEO_FILE = Path("out/video.mp4")
METADATA_FILE = Path("video_metadata.json")


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


def load_metadata():
    if not METADATA_FILE.exists():
        print(f"WARNING: {METADATA_FILE} not found, using placeholder metadata.")
        return {
            "title": "Untitled Video",
            "description": "",
            "tags": [],
            "privacyStatus": "private",
        }
    return json.loads(METADATA_FILE.read_text(encoding="utf-8"))


def main():
    if not VIDEO_FILE.exists():
        print(f"ERROR: {VIDEO_FILE} not found. Render the video first.")
        raise SystemExit(1)

    metadata = load_metadata()
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

    media = MediaFileUpload(str(VIDEO_FILE), chunksize=-1, resumable=True, mimetype="video/mp4")

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
    print("Review it and switch to Public in YouTube Studio when you're ready.")


if __name__ == "__main__":
    main()

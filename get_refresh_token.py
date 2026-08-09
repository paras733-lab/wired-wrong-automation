"""
get_refresh_token.py

RUN THIS ONCE, LOCALLY ON YOUR COMPUTER - not in GitHub Actions.

WHAT THIS DOES:
Walks you through YouTube's login/consent screen one time, then prints out
a "refresh token" - a long-lived credential that lets your automation
upload videos WITHOUT you having to log in again. You'll save this token
(and your client ID/secret) as GitHub Secrets, so GitHub Actions can
upload on your behalf without ever seeing your actual Google password.

BEFORE RUNNING:
1. Put the OAuth credentials JSON file you downloaded from Google Cloud
   Console (Step 6 from our earlier setup) in this same folder, named
   exactly: client_secret.json

HOW TO USE:
    pip install google-auth-oauthlib
    python get_refresh_token.py

A browser window will open. Log into your NEW Google account (the one
for this channel), approve access, then come back here - the token will
be printed in this terminal.
"""

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    # access_type='offline' is what makes Google give us a refresh token,
    # not just a short-lived access token.
    credentials = flow.run_local_server(port=0, access_type="offline", prompt="consent")

    print("\n" + "=" * 60)
    print("SUCCESS. Save these three values as GitHub Secrets:")
    print("=" * 60)
    print(f"YOUTUBE_CLIENT_ID:     {credentials.client_id}")
    print(f"YOUTUBE_CLIENT_SECRET: {credentials.client_secret}")
    print(f"YOUTUBE_REFRESH_TOKEN: {credentials.refresh_token}")
    print("=" * 60)
    print("\nGo to your GitHub repo -> Settings -> Secrets and variables")
    print("-> Actions -> New repository secret, and add all three above.")
    print("\nKeep this terminal output private - anyone with these values")
    print("can upload videos to your channel.")


if __name__ == "__main__":
    main()

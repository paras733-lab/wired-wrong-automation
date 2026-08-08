# Getting Started — Complete Beginner's Guide

This guide assumes you've never used a terminal, installed developer tools,
or touched code before. Every step is spelled out. Don't skip steps even
if they seem obvious — small setup mistakes are the most common reason
things "don't work" later.

Budget a few hours for this FIRST-TIME setup. After it's done once, making
each new video takes minutes, not hours.

---

## Part 0: Words you'll see a lot (read this first)

- **Terminal / Command line**: A text-based window where you type commands
  instead of clicking buttons. On Mac it's called "Terminal." On Windows,
  we'll use "PowerShell" (comes built-in) or "Git Bash" (installed below).
- **Repository (repo)**: A project folder that's tracked by Git/GitHub —
  basically just "your project," with version history.
- **Install / dependencies**: Extra pieces of software your project needs
  to run, downloaded automatically by a command (you won't do this by hand).
- **Run a command**: Type text into the terminal and press Enter.

You won't need to memorize any of this — just recognize the words when
they show up below.

---

## Part 1: Create your accounts (5 minutes)

1. **GitHub account** — go to github.com, sign up for free if you don't
   have one. This is where your project will live and where the free
   automated rendering happens.

---

## Part 2: Install the tools on your computer (30-45 minutes)

Install these one at a time, in order. Each is free.

### 2.1 — Install Node.js
This is the engine that runs the video-rendering code.
- Go to **nodejs.org**
- Download the version labeled **"LTS"** (Long Term Support — this means
  stable, not the newest experimental one)
- Run the installer, click Next/Agree through the defaults
- Confirm it worked: open your terminal and type:
  ```
  node -v
  ```
  You should see something like `v20.x.x`. If you see an error, restart
  your computer and try again (this fixes it 90% of the time).

### 2.2 — Install Python
This runs the auto-timing script (the one that listens to your voiceover).
- Go to **python.org/downloads**
- Download and install the latest version
- **Important on Windows**: during install, check the box that says
  "Add Python to PATH" before clicking Install.
- Confirm it worked:
  ```
  python --version
  ```

### 2.3 — Install a code editor (VS Code)
This is just a nice text editor for looking at/editing your project files.
- Go to **code.visualstudio.com**, download, install with defaults.

### 2.4 — Install Git
This is what lets your project talk to GitHub.
- Go to **git-scm.com/downloads**, download, install with all defaults
  (just keep clicking Next).
- Confirm it worked:
  ```
  git --version
  ```

### 2.5 — Install FFmpeg
This handles audio/video processing behind the scenes.
- **Mac**: open Terminal and run `brew install ffmpeg` (if you don't have
  Homebrew installed, go to brew.sh first and follow the one-line install
  command there).
- **Windows**: go to ffmpeg.org/download.html, follow the Windows build
  instructions, or search "install ffmpeg windows" for an up-to-date
  walkthrough — this one has more moving parts on Windows, take it slow.

---

## Part 3: Get the project onto your computer

1. Unzip the `explainer-template.zip` file I gave you into a folder you'll
   remember, e.g. `Documents/explainer-channel`.
2. Open a terminal.
3. Navigate into that folder by typing `cd ` (with a space after it) and
   then dragging the folder into the terminal window (this auto-fills the
   path). Press Enter.
4. Confirm you're in the right place:
   ```
   ls
   ```
   (On Windows PowerShell, use `dir` instead of `ls`.) You should see
   files like `package.json` and folders like `src`.

---

## Part 4: Install the project's dependencies

Still in that terminal, in that folder, run:
```
npm install
```
This downloads everything Remotion needs. It'll take a minute or two and
print a lot of text — that's normal. When it finishes and gives you your
prompt back with no red "error" text, it worked.

Then install the Python piece:
```
pip install -U openai-whisper
```
This also takes a few minutes the first time (it's downloading a speech
recognition model).

---

## Part 5: Preview the example video locally

Run:
```
npm start
```
This opens a browser window showing Remotion's preview tool. Click on
"Explainer" in the sidebar — you'll see the example stick-figure video
I built, with playback controls. This is just to confirm everything
installed correctly. Close it (Ctrl+C in the terminal) when you're done
looking.

---

## Part 6: Make your first real video — step by step

### 6.1 — Write your script
Just write it normally, like you already do for your Shorts channel.
Aim for 1,200-1,900 words for a 7-10 minute video at a faster narration
pace (see our earlier conversation for the reasoning on word count).

### 6.2 — Split it into sentences for the timing script
Create a new file: `src/scripts/narration.txt`
Paste your script into it, but put **one sentence per line** — wherever
you'd naturally pause. This is the only "extra" formatting step.

### 6.3 — Generate your voiceover
Use your existing free TTS tool, but **increase the speed setting**
(try 1.1x-1.15x for that faster CGP-Grey-style pace). Save the output as:
`public/audio/voiceover.mp3`
(create the `public/audio` folder if it doesn't exist yet)

### 6.4 — Auto-generate the scene timing
Back in your terminal, in the project folder, run:
```
python generate_scene_timing.py
```
This listens to your voiceover, matches it against your sentences, and
writes `src/scripts/example-script.json` with real timestamps. It'll
print how many scenes it made and the estimated video length.

### 6.5 — Add the visuals to each scene
Open `src/scripts/example-script.json` in VS Code. Each scene has a
`"beat"` section that's currently a placeholder. This is where you decide
what's on screen — e.g.:
```json
"beat": {
  "type": "singleFigure",
  "label": "Present You",
  "icon": "couch",
  "animation": "bounceIn"
}
```
Doing this by hand for 30-40 scenes is tedious. The fast way: open a
Claude chat, paste in your full script and the example-script.json file,
and ask it to fill in sensible "beat" values for every scene using the
same schema. Review its suggestions and adjust anything that feels off.

### 6.6 — Preview it
Run `npm start` again, click Explainer, and watch it play with your real
content. Check that the pacing feels right and captions match the audio.

### 6.7 — Render the final video file
```
npx remotion render src/Root.tsx Explainer out/video.mp4
```
This creates your actual video file at `out/video.mp4`. Rendering an 8-10
minute video will take a while on a normal laptop (could be 20 minutes to
a couple hours depending on your computer and how much animation is
happening) — let it run in the background.

---

## Part 7: Automate it on GitHub (so rendering doesn't tie up your laptop)

1. On GitHub.com, click "New repository," give it a name, make it
   **Public** (so rendering is free with no minute limits — see the notes
   in the main README about why).
2. Follow GitHub's instructions on that new repo's page under "…or push
   an existing repository from the command line" — copy those exact
   commands into your terminal while inside your project folder.
3. Once pushed, go to the "Actions" tab on your GitHub repo page. You'll
   see the "Render Explainer Video" workflow. Click "Run workflow" to
   trigger it manually, or just push new script changes and it'll run
   automatically.
4. When it finishes, click into the completed run and download the
   rendered video from the "Artifacts" section at the bottom.

---

## What to do if something breaks

- Copy the exact error text and ask an LLM (like Claude) "I'm following a
  Remotion setup guide and got this error: [paste it]. What does this
  mean and how do I fix it?" This works for almost every setup error
  you'll hit — they're usually very googleable/common issues.
- Most first-time errors are one of: Node.js not installed correctly,
  wrong folder in the terminal, or a typo in a file path. Check those
  three first.

---

## Realistic expectations for your first video

Your first one will take real hands-on time — expect a full afternoon
end to end, mostly spent on setup and troubleshooting, not on the actual
"making" part. Videos 2 and 3 will go much faster since the setup is
already done. By video 4 or 5 this should genuinely feel like your
Shorts pipeline: mostly hands-off.

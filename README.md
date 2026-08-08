# Explainer Channel Template (free, code-driven, CGP-Grey-style)

This mirrors the philosophy of your Shorts channel: **you only ever touch
one input file (the script), everything else is automated.**

## How it works

```
src/scripts/example-script.json   <- YOU edit this per video
        |
        v
src/scenes/ExplainerVideo.tsx     <- reads the script, sequences scenes
        |
        v
src/scenes/Scene.tsx              <- turns each "beat" into visuals
        |
        v
src/components/StickFigure.tsx    <- reusable animated SVG figure
src/components/Caption.tsx        <- reusable caption bar
        |
        v
npx remotion render               <- outputs out/video.mp4
```

## Your actual weekly workflow, once this is set up

1. Write the script (same as you do now).
2. Generate the voiceover with your existing free TTS tool, save it into
   `public/audio/`.
3. Convert the script into scene "beats" — this is the one new skill.
   For a 8-12 min video that's usually 15-40 scenes. You can have an LLM
   (like Claude, via the free web/API tier or a local model) do this
   conversion for you: paste your script in, ask it to output JSON in this
   exact schema, and it'll do the scene-breakdown work.
4. Push to GitHub. The Actions workflow (`.github/workflows/render.yml`)
   renders it automatically and hands you back a video file — no local
   rendering required, no paid render service.
5. Download from the Actions artifact, upload to YouTube.

## Why this fits "no money, 1-2 videos/week"

- **Remotion is free** for individuals and teams of 3 or fewer, including
  commercial/monetized use — you don't pay anything as you scale, unless
  you eventually hire people.
- **Rendering is free** on GitHub Actions for public repos (standard
  runners, no minute cap). If you'd rather keep the repo private, you get
  2,000 free minutes/month, which comfortably covers 2 videos/week at this
  complexity level.
- **All visuals are drawn in code** (SVG shapes, CSS, emoji-as-icons) — no
  paid stock footage, no paid animation software, no asset packs.

## What "beat types" currently exist

- `singleFigure` — one stick figure with a label + optional icon
- `twoFigures` — two figures side by side (comparisons, conflicts)
- `arrow` — one figure "winning" or "leading to" another

## How to grow this later

When you extend this system, you add new beat types the same way — one
new `case` in `Scene.tsx`, one new shape/animation. Things worth adding
next, roughly in order of value for an explainer channel:

1. A `map` beat (useful even outside psychology — history/geography crossover)
2. A `chart` or `barRace` beat for simple data visuals
3. A `timeline` beat for "here's how this played out over time"

None of these require new paid tools — they're all just new SVG/CSS you
(or an AI assistant) write once and reuse forever.

## Honest limitations to know about upfront

- You (or an assistant) need to write the script → JSON conversion logic,
  or do it manually per video. This is the real "cost" of the free
  approach — it's your time instead of your money.
- Visual complexity is capped by what you're willing to code. CGP Grey's
  actual visual variety comes from years of built-up shape/icon library —
  yours will look simpler at first and get richer every few videos as you
  add beat types.
- Test render times locally before relying on GitHub Actions timing —
  complexity (number of simultaneous animated elements) affects render
  time more than video length does.

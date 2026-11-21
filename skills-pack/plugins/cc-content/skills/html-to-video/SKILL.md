---
name: html-to-video
description: Make videos by writing HTML, CSS and JavaScript animations and rendering them frame by frame to MP4 with Playwright and ffmpeg - title cards, animated stats, explainer clips, social shorts, product teasers, report highlights. Use when the user asks to create a video, motion graphic, animated intro, reel, short, or to turn slides, data or a report into a video.
---

# HTML to Video

> Paths: `$SKILL_DIR` means the folder that contains this SKILL.md (Claude Code shows it as the skill base directory). Set it first, e.g. `SKILL_DIR=~/.claude/skills/<skill-name>`.

Write the video as a web page. Render it deterministically, frame by frame. No video editor needed.

## Requirements

- Node 18+, `ffmpeg` on PATH, and Playwright with Chromium:
  ```bash
  npm i -D playwright && npx playwright install chromium
  ```
- Works in Claude Code and any local environment. Not in the Claude.ai chat sandbox unless it has Chromium and ffmpeg.

## Step 1: Storyboard (before code)

Write a beat sheet. Every beat has a time, on-screen text, and motion.

```
Format: 1080x1920 (vertical short) | 30 fps | 12 s
0.0-2.0  Hook: "3 checks before every night shift"   slide up
2.0-5.0  Check 1: Fire panel status                  icon + text, stagger
5.0-8.0  Check 2: Radio and CCTV test                ...
8.0-11.0 Check 3: Patrol route briefing              ...
11.0-12  Logo + CTA                                  fade
```

Common sizes: 1920x1080 (YouTube, slides), 1080x1920 (Reels, Shorts, TikTok), 1080x1350 (LinkedIn/Instagram feed), 1080x1080 (square).

## Step 2: Build the composition

Start from `assets/example-composition.html`. Rules:
- Fixed `html, body` size equal to the video size, `overflow: hidden`.
- Set `window.__duration = <seconds>`.
- Animate with CSS `@keyframes` + `animation-delay`, or the Web Animations API. The renderer pauses every animation and sets its time per frame, so timing is exact.
- For GSAP or custom JS, build a paused timeline and expose a seek function:
  ```js
  const tl = gsap.timeline({ paused: true })
  // ... tl.to(...)
  window.__duration = tl.duration()
  window.__seek = (t) => tl.seek(t)
  ```
- No `Date.now()`, `Math.random()` without a seed, or `setTimeout` for visuals: they break determinism.
- Fonts: load local files or wait for Google Fonts; the renderer waits for `document.fonts.ready`.
- Text safe zone: keep text 80 px inside the edges (more at the bottom of vertical video for platform UI).
- Arabic: set `dir="rtl"` on the element and use a font with Arabic glyphs (Noto Naskh Arabic, IBM Plex Sans Arabic).

## Step 3: Render

```bash
node "$SKILL_DIR/scripts/render.mjs" composition.html out.mp4 --fps 30 --width 1080 --height 1920
```

Output: H.264 MP4, yuv420p, faststart (plays everywhere, uploads to all platforms).

Preview fast first: `--fps 10`. Then render final at 30.

## Step 4: Check

- Extract stills at each beat: `ffmpeg -ss 2.5 -i out.mp4 -frames:v 1 beat1.png` and look at them.
- Confirm duration and size: `ffprobe -v error -show_entries format=duration:stream=width,height out.mp4`.
- Add audio if needed: `ffmpeg -i out.mp4 -i music.mp3 -c:v copy -c:a aac -shortest final.mp4` (only licensed audio).
- Burned-in captions are already in the HTML. For a separate `.srt`, write it from the beat sheet.

## Upstream option

HeyGen's open-source HyperFrames (`heygen-com/hyperframes`, Apache 2.0) is a fuller framework with the same idea, a CLI, and many templates. Install in Claude Code with `/plugin marketplace add heygen-com/hyperframes` or `npx skills add heygen-com/hyperframes`. Use it for longer or production work. This skill is the lightweight, dependency-minimal version.

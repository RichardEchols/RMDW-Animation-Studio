# RMDW Animation Studio — Production Plan (plan.md)

## Title
**"How a Solo Operator Animation Studio Works"**
A 3Blue1Brown-style animated explainer + 3D Blender piece.
Built entirely by JAH 3.0 + Hermes, on Richard's own hardware, with free open tools.

## The narrative arc
The traditional animation studio needs a TEAM (writer, storyboard artist, animator,
editor, sound) and EXPENSIVE software (After Effects, Maya, Cinema 4D) and WEEKS per
video.

The JAH 3.0 + Hermes way: ONE person, ONE local model, FREE open tools, a REPEATABLE
pipeline. Script → Storyboard → Animate → Render → Publish.

The animation takes the viewer from "that's how it used to be" to "here's the new way"
— and lands on the punchline: you don't need a studio. You need a pipeline.

## Visual language
- **Palette:** Classic 3B1B dark (`#1C1C1C` bg) with crimson accent (`#B11E2F` —
  RMDW's brand) + cyan (`#58C4DD`) + green (`#83C167`)
- **Typography:** Monospace (Menlo) for all text — Manim's Pango renderer needs it
- **Motion:** Clean, deliberate. Every reveal gets a `wait()` after it. Opacity
  layering for depth (primary 1.0, contextual 0.4, structural 0.15)

## Scene list

### Scene 1 — The Old Way (the problem)
Show the traditional studio as a wall of expensive tools + a team of roles.
- Title: "The Traditional Studio"
- Visual: stacked role labels (Writer, Storyboard, Animator, Editor, Sound) + price
  tags (After Effects, Maya, Cinema 4D) — heavy, cluttered, expensive
- Message: "A team. Expensive software. Weeks per video."

### Scene 2 — The New Way (the reveal)
- Title: "The Solo Operator"
- Visual: one person icon + one model (JAH 3.0) + a clean pipeline arrow
  Script → Storyboard → Animate → Render → Publish
- Message: "One person. One local model. Free tools. A repeatable pipeline."

### Scene 3 — The Pipeline (the meat)
Animate the 5 stages as a flowing pipeline, each lighting up in sequence:
1. Script — "I write the story"
2. Storyboard — "I plan the scenes"
3. Animate — "I build the visuals" (Manim + Blender + p5.js)
4. Render — "I render the frames"
5. Publish — "I ship the video"
- Message: "The AI is the team. The tools are the hands."

### Scene 4 — The Punchline
- Title: "You don't need a studio. You need a pipeline."
- Visual: "RMDW ANIMATION STUDIO" title card, crimson, bold
- Subtitle: "One person. One local model. Your own hardware. Free tools."
- Final: "Built by JAH 3.0 + Hermes" + repo name

## 3D Blender piece (the "floor him" flex)
A polished 3D render: the RMDW crimson sphere, orbiting, with "RMDW" text — a
cinematic 3D logo animation. Proves true 3D capability beyond 2D explainers.

## Deliverables
- `final.mp4` — stitched Manim explainer (1080p)
- `studio/blender/` — the 3D piece (MP4 + source)
- `stack.md` — recommended tool stack (Anthony's question)
- `README.md` — what this is + how to run it
- `pipeline/` — the repeatable build steps

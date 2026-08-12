# RMDW Animation Studio 🎬

**One person. One local AI model. Free open tools. A repeatable pipeline.**

This repo is a working **solo-operator animation studio** — built entirely by
**JAH 3.0 + Hermes** (Richard's own local AI, running on his own hardware). It answers
the question: *"What are the best platforms and tool stacks to build a solo-operator
animation studio?"*

The answer isn't a single tool. It's a **pipeline**: `SCRIPT → STORYBOARD → ANIMATE →
RENDER → PUBLISH`. The AI is the team. The tools are the hands.

---

## What's in here

| Path | What it is |
|------|-----------|
| `final.mp4` | The finished animated explainer (1080p) |
| `studio/manim/` | Manim source — "How a Solo Operator Animation Studio Works" |
| `studio/blender/` | Blender source — the 3D "RMDW" piece |
| `pipeline/` | The repeatable build steps (script → stitch) |
| `stack.md` | The recommended tool stack (the actual question) |
| `plan.md` | The storyboard / production plan |

---

## The animation

**"How a Solo Operator Animation Studio Works"** — a 3Blue1Brown-style explainer that
takes you from the traditional studio (a team + expensive software + weeks per video)
to the solo operator way (one person + one local model + free tools + a pipeline).

Plus a **3D Blender piece** — a cinematic render of the RMDW crimson sphere with
"RMDW" text, proving true 3D capability beyond 2D explainers.

---

## How it was built (the proof)

Every step was done by JAH 3.0 + Hermes:
1. **Storyboarded** the narrative arc and scene list (`plan.md`)
2. **Wrote** the Manim scenes (Python) and the Blender script
3. **Rendered** the frames locally on the MacBook (Manim + Blender)
4. **Stitched** the scenes into `final.mp4` with ffmpeg
5. **Packaged** this repo and pushed it to GitHub

No cloud AI. No paid software. No team. One person, one local model, free tools.

---

## Run it yourself

```bash
# Manim explainer
pip install manim
manim -qh studio/manim/explainer.py Scene1_OldWay Scene2_NewWay Scene3_Pipeline Scene4_Punchline

# Blender 3D piece
blender --background --python studio/blender/rmdw_3d.py

# Stitch
ffmpeg -f concat -safe 0 -i pipeline/concat.txt -c copy final.mp4
```

---

## License
MIT — free to use, remix, and build on. The tools are free; the pipeline is the moat.

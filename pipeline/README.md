# The Pipeline

This is the repeatable build process that IS the "studio." One person + one local AI
model runs these steps to produce a finished animation.

```
SCRIPT → STORYBOARD → ANIMATE → RENDER → PUBLISH
```

## Step 1 — Script
The AI writes the narrative. What story are we telling? What's the arc?

## Step 2 — Storyboard
The AI plans the scenes: narrative arc, visual language, color palette, motion style.
See `plan.md` for the storyboard of this project.

## Step 3 — Animate
The AI writes the code for each tool:
- **Manim** (`studio/manim/explainer.py`) — 2D explainer scenes
- **Blender** (`studio/blender/rmdw_3d.py`) — 3D piece
- **p5.js** — web-native motion graphics (optional)

## Step 4 — Render
Each tool renders frames locally on your machine:
```bash
manim -qh studio/manim/explainer.py Scene1_OldWay Scene2_NewWay Scene3_Pipeline Scene4_Punchline
blender --background --python studio/blender/rmdw_3d.py
```

## Step 5 — Publish
Stitch the scenes and ship:
```bash
./pipeline/stitch.sh
```
Produces `final.mp4`. Push the source to GitHub so anyone can reproduce it.

---

## Why it works
- **Reproducible** — same code, same output, every time
- **Local** — runs on your own hardware, data never leaves
- **Free** — all tools are open source
- **Scalable** — add more scenes, more tools, more styles

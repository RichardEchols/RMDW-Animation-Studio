# RMDW Animation Studio — Recommended Tool Stack

**The question:** What are the best platforms and tool stacks to build a solo-operator
animation studio?

**The answer (in practice, not theory):** You don't need a studio. You need a pipeline.
One person + one local AI model + a handful of free, open tools. Everything below was
used to produce the animation in this repo — it's the stack that actually works, not a
marketing list.

---

## The core stack

| Layer | Tool | Why | Cost |
|-------|------|-----|------|
| **The "team"** | JAH 3.0 + Hermes | Writes the script, storyboards, writes the code, drives every tool, iterates. The AI is the team. | Runs on your own hardware |
| **Explainer / math / data animation** | [Manim CE](https://www.manim.community/) | Cinematic 3Blue1Brown-style motion graphics. Pure Python, fully reproducible, no GPU needed. | Free (MIT) |
| **True 3D animation** | [Blender](https://www.blender.org/) | Full 3D: modeling, rigging, character animation, VFX, lighting. Industry standard. | Free (GPL) |
| **Web-native motion graphics** | [p5.js](https://p5js.org/) | Generative art, kinetic typography, interactive visuals, shaders. Runs in the browser. | Free (LGPL) |
| **Video assembly / encoding** | [ffmpeg](https://ffmpeg.org/) | Stitch scenes, encode, transcode, publish. The workhorse. | Free (GPL/LGPL) |
| **Narration (optional)** | TTS (edge / openai) | Voiceover without hiring a voice actor. | Free / low cost |

---

## The pipeline (the actual "studio")

```
SCRIPT → STORYBOARD → ANIMATE → RENDER → PUBLISH
```

1. **Script** — the AI writes the narrative (what story are we telling?)
2. **Storyboard** — the AI plans the scenes (narrative arc, visual language, palette)
3. **Animate** — the AI writes the code for each tool (Manim / Blender / p5.js)
4. **Render** — the tools render frames locally on your machine
5. **Publish** — ffmpeg stitches it into a final video; push the source to GitHub

---

## Why this beats the "traditional" studio

| Traditional studio | Solo operator + AI |
|--------------------|--------------------|
| A team (writer, storyboard, animator, editor, sound) | One person + one local model |
| Expensive software (After Effects, Maya, Cinema 4D) | Free open tools |
| Weeks per video | Hours per video |
| Data leaves your machine | Everything runs on your own hardware |

---

## How to run this yourself

```bash
# Manim explainer
pip install manim
manim -qh studio/manim/explainer.py Scene1_OldWay Scene2_NewWay Scene3_Pipeline Scene4_Punchline

# Blender 3D piece
blender --background --python studio/blender/rmdw_3d.py

# Stitch (see pipeline/stitch.sh)
ffmpeg -f concat -safe 0 -i pipeline/concat.txt -c copy final.mp4
```

---

## The philosophy

The moat isn't the model — models are commoditizing. The moat is the **harness**: the
pipeline, the tools, the workflow that turns one person + one local model into a
production studio. That's what this repo demonstrates.

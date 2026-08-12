#!/bin/bash
# RMDW Animation Studio — stitch the rendered scenes into final.mp4
# Usage: ./pipeline/stitch.sh

set -e
cd "$(dirname "$0")/.."

MANIM_DIR="studio/manim/media/videos/explainer/1080p60"
BLENDER_MP4="/tmp/rmdw_3d.mp4"

# Build the concat list from the rendered Manim scenes (in order)
cat > pipeline/concat.txt << EOF
file '${MANIM_DIR}/Scene1_OldWay.mp4'
file '${MANIM_DIR}/Scene2_NewWay.mp4'
file '${MANIM_DIR}/Scene3_Pipeline.mp4'
file '${MANIM_DIR}/Scene4_Punchline.mp4'
EOF

# Stitch the Manim explainer
ffmpeg -y -f concat -safe 0 -i pipeline/concat.txt -c copy pipeline/explainer_stitched.mp4

# If the Blender 3D piece exists, append it as a finale
if [ -f "$BLENDER_MP4" ]; then
  ffmpeg -y -f concat -safe 0 -i <(echo "file 'pipeline/explainer_stitched.mp4'"; echo "file '$BLENDER_MP4'") -c copy final.mp4
else
  cp pipeline/explainer_stitched.mp4 final.mp4
fi

echo "✅ final.mp4 ready"

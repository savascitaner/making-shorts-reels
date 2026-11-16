#!/bin/bash
# kullanım: logs/klip.sh v1 /Users/claude/flow-mcp-out/BE-veo/scene-01.mp4  -> gorseller/klip/v1/*.jpg + n.txt + done
set -e; k=$1; src=$2; d="gorseller/klip/$k"; rm -rf "$d"; mkdir -p "$d"
ffmpeg -v error -i "$src" -vf "fps=24,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -q:v 3 -start_number 0 "$d/%03d.jpg"
ls "$d"/*.jpg | wc -l | tr -d ' ' > "$d/n.txt"; touch "$d/done"; echo "$k $(cat $d/n.txt)"

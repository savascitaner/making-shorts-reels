#!/bin/bash
# 6 evenly spaced frames -> one sheet.  qc_frames.sh video.mp4 out.jpg
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"); args=(); f=""
for k in 0 1 2 3 4 5; do t=$(echo "$d*($k+0.5)/6" | bc -l); args+=(-ss "$t" -i "$1"); f="$f[$k:v]scale=-2:540[v$k];"; done
ffmpeg -v error -y "${args[@]}" -frames:v 1 -filter_complex "${f}[v0][v1][v2][v3][v4][v5]hstack=inputs=6" "$2"

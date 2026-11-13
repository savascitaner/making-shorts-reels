#!/bin/zsh
# Veo klipleri -> gorseller/klip/v<n>/ kareler + n.txt + done (off.txt ayrıca off.py ile)
setopt nullglob
G="/Users/claude/Shorts - Reels/Yunus-Tapduk/gorseller/klip"
for n in 1 2 3 4 5 6 7; do s=~/flow-mcp-out/YT-veo/scene-0$n.mp4; [ -f "$s" ] || continue; d="$G/v$n"; [ -f "$d/done" ] && continue
  mkdir -p "$d"; ffmpeg -v error -y -i "$s" -vf fps=24 -q:v 3 -start_number 0 "$d/%03d.jpg"; ls "$d"/*.jpg | wc -l | tr -d ' ' > "$d/n.txt"; touch "$d/done"; echo "v$n $(cat $d/n.txt) kare"
done

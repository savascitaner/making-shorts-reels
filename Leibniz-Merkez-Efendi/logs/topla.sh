#!/bin/zsh
setopt nullglob
# Flow çıktılarını gorseller/flow ve gorseller/klip/<k>/ karelerine taşır
F=~/flow-mcp-out/Leibniz-Merkez-Efendi; G="/Users/claude/Shorts - Reels/Leibniz-Merkez-Efendi/gorseller"; mkdir -p "$G/flow"
for p in 15:seyh 05:muritler 16:musa 17:leibniz 18:havan 19:mum-istanbul 20:mum-hannover 21:dervis-pencere 22:kubbe 23:yazma 24:istanbul 25:hannover; do
  n=${p%%:*}; k=${p#*:}; m=($F/scene-$n.*); s=${m[1]}; [ -n "$s" ] && [ ! -f "$G/flow/$k.jpg" ] && ffmpeg -v error -y -i "$s" -q:v 2 "$G/flow/$k.jpg" && echo "img $k"
done
for p in 26:seyh 27:murit 28:musa 29:leib 30:havan; do
  n=${p%%:*}; k=${p#*:}; m=($F/scene-$n*.mp4); [ ${#m} -eq 0 ] && continue; s=${m[1]}; [ -f "$G/klip/$k/done" ] && continue
  mkdir -p "$G/klip/$k"; ffmpeg -v error -y -i "$s" -vf fps=24 -q:v 3 -start_number 0 "$G/klip/$k/%03d.jpg"
  ls "$G/klip/$k"/*.jpg | wc -l | tr -d ' ' > "$G/klip/$k/n.txt"; touch "$G/klip/$k/done"; echo "clip $k $(cat $G/klip/$k/n.txt)"
done

#!/bin/zsh
# Veo klipleri -> gorseller/klip/v<n>/ kareler + n.txt + off.txt (konuşma başı ve sonu, sn) + done
setopt nullglob
F=~/flow-mcp-out/MF-veo; G="/Users/claude/Shorts - Reels/Marx-Feuerbach/gorseller/klip"
for p in 1:1 2:2 6:3 7:4 5:5; do sn=${p%%:*}; n=${p#*:}; m=($F/scene-0$sn*.mp4); [ ${#m} -eq 0 ] && continue; s=${m[1]}; d="$G/v$n"; [ -f "$d/done" ] && continue
  mkdir -p "$d"; ffmpeg -v error -y -i "$s" -vf fps=24 -q:v 3 -start_number 0 "$d/%03d.jpg"; ls "$d"/*.jpg | wc -l | tr -d ' ' > "$d/n.txt"
  ffmpeg -v info -i "$s" -af "highpass=f=120,silencedetect=n=-32dB:d=0.25" -vn -f null - 2>&1 | grep -o 'silence_\(start\|end\): [0-9.]*' > "$d/sil.txt"
  python3 -c "
import sys;L=[l.split() for l in open('$d/sil.txt')];ev=[(a[:-1],float(b)) for a,b in L]
ends=[t for k,t in ev if k=='silence_end'];starts=[t for k,t in ev if k=='silence_start']
s0=ends[0] if ends and (not starts or ends[0]>starts[0] and starts[0]<0.05) else 0.0
s0=min([e for e in ends] or [0.6]) if starts and starts[0]<0.05 else 0.0
last=[t for t in starts if t>s0+0.5]; s1=last[-1] if last else 3.0
print(round(s0,2), round(s1,2))" > "$d/off.txt"; touch "$d/done"; echo "v$n $(cat $d/n.txt) kare, konuşma $(cat $d/off.txt)"
done

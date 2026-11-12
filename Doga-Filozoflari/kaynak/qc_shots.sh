#!/bin/bash
# One frame from the middle of every shot -> two sheets.  qc_shots.sh video.mp4 shots.json out_prefix
ts=$(python3 -c "
import json,sys;d=json.load(open(sys.argv[1]));s=d['shots'];e=[x[0] for x in s[1:]]+[d['dur']]
print(' '.join(f'{(a[0]+b)/2:.2f}' for a,b in zip(s,e)))" "$2")
arr=($ts); n=${#arr[@]}; h=$(( (n+1)/2 ))
for part in 0 1; do args=(); f=""; k=0
  for t in "${arr[@]:$((part*h)):$h}"; do args+=(-ss $t -i "$1"); f="$f[$k:v]scale=-2:${4:-480}[v$k];"; k=$((k+1)); done
  st=""; for i in $(seq 0 $((k-1))); do st="$st[v$i]"; done
  ffmpeg -v error -y "${args[@]}" -frames:v 1 -filter_complex "${f}${st}hstack=inputs=$k" "$3-$part.jpg"
done

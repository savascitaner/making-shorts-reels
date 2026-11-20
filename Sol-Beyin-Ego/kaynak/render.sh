#!/bin/zsh
# ./render.sh long|short  -> outputs/Sol-Beyin-Ego/ altina video (+ Shorts icin telefon onizlemesi)
set -e
cd "${0:A:h}"; M="$1"; ROOT="/Users/claude-eng/Shorts - Reels"; O="$ROOT/outputs/Sol-Beyin-Ego"; mkdir -p "$O" renders
export PATH=$(python3 -c "import json;print(json.load(open('$ROOT/.claude/settings.json'))['env']['PATH'])"):$PATH
curl -s -o /dev/null http://127.0.0.1:8765/ || (cd "$ROOT" && nohup python3 -m http.server 8765 --bind 127.0.0.1 >/dev/null 2>&1 & sleep 1)
node "$ROOT/araclar/cinecode/scripts/capture.mjs" --url "http://127.0.0.1:8765/Sol-Beyin-Ego/kaynak/index.html?m=$M" --video "renders/picture-$M.mp4" --workers 4 --crf 17 --maxrate 12M > "renders/capture-$M.log" 2>&1
NAME="Sol-Beyin-Ego-16x9"; [ "$M" = short ] && NAME="Sol-Beyin-Ego-Shorts-9x16"
ffmpeg -v error -y -i "renders/picture-$M.mp4" -i "audio/master-$M.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$O/$NAME.mp4"
if [ "$M" = short ]; then
  ffmpeg -v error -y -i "$O/$NAME.mp4" -vf scale=720:1280 -c:v libx264 -b:v 1100k -maxrate 1300k -bufsize 2600k -preset slow -c:a aac -b:a 96k -movflags +faststart "$O/Onizleme-telefon-Shorts.mp4"
fi
ffprobe -v error -show_entries format=duration,size -of csv=p=0 "$O/$NAME.mp4"

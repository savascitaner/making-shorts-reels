#!/bin/zsh
# 16:9 ve 9:16 render + ses birleştirme. Kullanım: ./render.sh (kaynak/ içinden)
set -e
ROOT="/Users/claude-eng/Shorts - Reels"; CC="$ROOT/araclar/cinecode/scripts"; O="$ROOT/outputs/Kanal-Fragmani"
export PATH="$HOME/.local/node/bin:$ROOT/araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64:$PATH"
curl -s -o /dev/null "http://127.0.0.1:8765/" || (cd "$ROOT" && nohup python3 -m http.server 8765 --bind 127.0.0.1 >/dev/null 2>&1 & sleep 1)
mkdir -p "$O" renders
node "$CC/capture.mjs" --url "http://127.0.0.1:8765/Kanal-Fragmani/kaynak/index.html" --video renders/picture-16x9.mp4 --workers 3 --crf 17 --maxrate 12M > renders/cap-h.log 2>&1
ffmpeg -v error -y -i renders/picture-16x9.mp4 -i audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$O/Kanal-Fragmani-16x9.mp4"
node "$CC/capture.mjs" --url "http://127.0.0.1:8765/Kanal-Fragmani/kaynak/index.html?fmt=v" --video renders/picture-9x16.mp4 --workers 3 --crf 17 --maxrate 12M > renders/cap-v.log 2>&1
ffmpeg -v error -y -i renders/picture-9x16.mp4 -i audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$O/Kanal-Fragmani-Reels-9x16.mp4"
ffmpeg -v error -y -i "$O/Kanal-Fragmani-Reels-9x16.mp4" -vf scale=720:1280 -c:v libx264 -b:v 1100k -maxrate 1300k -bufsize 2600k -preset slow -c:a aac -b:a 96k -movflags +faststart "$O/Onizleme-telefon.mp4"
for f in "$O"/*.mp4; do echo "$(basename "$f") $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f") sn $(du -h "$f" | cut -f1)"; done

set -e
export PATH="$HOME/.local/node/bin:/Users/claude-eng/Shorts - Reels/araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64:$PATH"
CC="/Users/claude-eng/Shorts - Reels/araclar/cinecode/scripts"; O="/Users/claude-eng/Shorts - Reels/outputs/Insanin-Ozu"; mkdir -p "$O"
cd "/Users/claude-eng/Shorts - Reels/Insanin-Ozu/kaynak"
node "$CC/capture.mjs" --url "http://127.0.0.1:8765/Insanin-Ozu/kaynak/index.html?ar=w" --video renders/picture-w.mp4 --workers 3 --crf 17 --maxrate 14M > renders/capture-w.log 2>&1
ffmpeg -v error -y -i renders/picture-w.mp4 -i audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$O/Insanin-Ozu-16x9.mp4"
echo W_OK
node "$CC/capture.mjs" --url "http://127.0.0.1:8765/Insanin-Ozu/kaynak/index.html?ar=t" --video renders/picture-t.mp4 --workers 3 --crf 17 --maxrate 12M > renders/capture-t.log 2>&1
ffmpeg -v error -y -i renders/picture-t.mp4 -i audio/master-r.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$O/Insanin-Ozu-Reels-9x16.mp4"
ffmpeg -v error -y -i "$O/Insanin-Ozu-Reels-9x16.mp4" -vf scale=720:1280 -c:v libx264 -b:v 1100k -maxrate 1300k -bufsize 2600k -preset slow -c:a aac -b:a 96k -movflags +faststart "$O/Onizleme-telefon-Reels.mp4"
for f in "$O"/*.mp4; do echo "$(basename "$f") $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f") $(du -h "$f" | cut -f1)"; done
echo RENDER_BITTI

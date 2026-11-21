#!/bin/zsh
export PATH="$(python3 -c "import json;print(json.load(open('/Users/claude-eng/Shorts - Reels/.claude/settings.json'))['env']['PATH'])"):$PATH"
CC="/Users/claude-eng/Shorts - Reels/araclar/cinecode/scripts"; O="/Users/claude-eng/Shorts - Reels/outputs/Vahdetten-Kesrete"; U="http://127.0.0.1:8765/Vahdetten-Kesrete/kaynak/film.html"
cd "/Users/claude-eng/Shorts - Reels/Vahdetten-Kesrete/kaynak"; mkdir -p renders "$O"
node "$CC/capture.mjs" --url "$U" --params "fmt=shorts" --video renders/picture-shorts.mp4 --workers 3 --crf 17 --maxrate 10M > renders/capture-shorts.log 2>&1
ffmpeg -v error -y -i renders/picture-shorts.mp4 -i audio/master-shorts.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$O/Vahdetten-Kesrete-Shorts-9x16.mp4"
echo "SHORTS_BITTI" >> renders/render.log
node "$CC/capture.mjs" --url "$U" --params "fmt=long" --video renders/picture-long.mp4 --workers 3 --crf 17 --maxrate 14M > renders/capture-long.log 2>&1
ffmpeg -v error -y -i renders/picture-long.mp4 -i audio/master-long.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$O/Vahdetten-Kesrete-YouTube-16x9.mp4"
echo "LONG_BITTI" >> renders/render.log

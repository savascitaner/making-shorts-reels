#!/bin/zsh
# Tek komutla üretim hattı. Kullanım:  ./uret.sh <Konu> <adim>
#   yeni     : _sablon'dan <Konu>/ klasörünü kurar
#   gorsel   : gorseller/prompts.json -> gorseller/ai/*.jpg (yerel SDXL) + gorseller/ai-sheet.jpg (tek bakışlık)
#   hizala   : kaynak/audio/vo.wav -> words.json + outputs/<Konu>/<Konu>-altyazi.srt
#   ses      : müzik + sfx + miks + -14 LUFS master
#   qc       : video.json qc_kareleri -> kaynak/renders/qc-sheet.jpg (tek görsel; QC sadece buna bakılır)
#   render   : tam video + ses -> outputs/<Konu>/<Konu>-Reels-9x16.mp4 + Onizleme-telefon.mp4 (<20 MB)
#   git      : commit + push
set -e
ROOT="/Users/claude/Shorts - Reels"; K="$1"; A="$2"; P="$ROOT/$K"; PY="$ROOT/araclar/venv-vahdet/bin/python"; CC="$ROOT/araclar/cinecode/scripts"
cfg() { python3 -c "import json;print(json.load(open('$P/video.json'))$1)"; }
serve() { curl -s -o /dev/null "http://127.0.0.1:8765/" || (cd "$ROOT" && nohup python3 -m http.server 8765 --bind 127.0.0.1 >/dev/null 2>&1 & sleep 1); }
case "$A" in
  yeni)  [ -e "$P" ] && { echo "zaten var: $P"; exit 1; }
         cp -R "$ROOT/_sablon" "$P"; mkdir -p "$ROOT/outputs/$K" "$P/ses"
         sed -i '' "s/\"KONU\"/\"$K\"/" "$P/video.json"; echo "kuruldu: $P" ;;
  gorsel) cd "$P/gorseller"; HF_HOME="$ROOT/araclar/sd/hf" "$PY" batch_gen.py prompts.json ai > gen.log 2>&1
         ffmpeg -v error -y -pattern_type glob -i 'ai/*.jpg' -vf "scale=180:315,tile=8x3" -frames:v 1 ai-sheet.jpg; ls ai | wc -l ;;
  hizala) cd "$P/kaynak"; [ -f audio/vo.wav ] || ffmpeg -v error -y -i ../ses/vo.mp3 -ar 48000 audio/vo.wav
         "$PY" transcribe.py audio/vo.wav words-raw.json > transcribe.log 2>&1; tail -1 transcribe.log; python3 align.py | head -1 ;;
  ses)   cd "$P/kaynak"; uv run -q --with numpy --with scipy python music.py audio "$(cfg "['sure']")" \
           "$(cfg "['bolum_sinirlari']" | tr -d '[] ')" "" "$(cfg "['gecis']" | tr -d '[] ')" "$(cfg "['boom']" | tr -d '[] ')"
         uv run -q --with numpy --with scipy python mixdown.py
         uv run -q --with numpy --with scipy python "$CC/master_audio.py" audio/mix.wav audio/master.wav | tail -1 ;;
  qc)    serve; cd "$P/kaynak"; rm -rf renders/qc; F=$(cfg "['qc_kareleri']" | tr -d '[] ')
         node "$CC/capture.mjs" --url "http://127.0.0.1:8765/$K/kaynak/index.html" --out renders/qc --frames "$F" --format jpeg | tail -1
         ffmpeg -v error -y -pattern_type glob -i 'renders/qc/*.jpg' -vf "scale=216:384,tile=6x2" -frames:v 1 renders/qc-sheet.jpg; echo "bak: $P/kaynak/renders/qc-sheet.jpg" ;;
  render) serve; cd "$P/kaynak"; O="$ROOT/outputs/$K"; mkdir -p "$O"
         node "$CC/capture.mjs" --url "http://127.0.0.1:8765/$K/kaynak/index.html" --video renders/picture.mp4 --workers 3 --crf 17 --maxrate 12M > renders/capture.log 2>&1
         ffmpeg -v error -y -i renders/picture.mp4 -i audio/master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart "$O/$K-Reels-9x16.mp4"
         ffmpeg -v error -y -i "$O/$K-Reels-9x16.mp4" -vf scale=720:1280 -c:v libx264 -b:v 1100k -maxrate 1300k -bufsize 2600k -preset slow -c:a aac -b:a 96k -movflags +faststart "$O/Onizleme-telefon.mp4"
         ffprobe -v error -show_entries format=duration -of csv=p=0 "$O/$K-Reels-9x16.mp4"; ls -la "$O" | awk '{print $5, $9}' ;;
  git)   cd "$ROOT"; git add -A; git commit -q -m "${3:-$K: güncelleme}" || true; git push -q; echo pushed ;;
  *) sed -n 2,10p "$0" ;;
esac

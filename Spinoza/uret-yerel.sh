#!/bin/zsh
# worktree icin: hizala + gorsel (uret.sh ROOT'a sabit oldugu icin)
set -e
PY="/Users/claude/Shorts - Reels/araclar/venv-vahdet/bin/python"
cd "$(dirname $0)/kaynak"; mkdir -p audio
ffmpeg -v error -y -i ../ses/vo.mp3 -ar 48000 audio/vo.wav
"$PY" transcribe.py audio/vo.wav words-raw.json > transcribe.log 2>&1; tail -1 transcribe.log
python3 align.py | head -1 || true
cd ../gorseller; HF_HOME="/Users/claude/Shorts - Reels/araclar/sd/hf" "$PY" batch_gen.py prompts.json ai > gen.log 2>&1
ffmpeg -v error -y -pattern_type glob -i 'ai/*.jpg' -vf "scale=180:315,tile=8x4" -frames:v 1 ai-sheet.jpg; echo GORSEL_TAMAM

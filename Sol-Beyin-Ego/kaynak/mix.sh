#!/bin/zsh
# Anlatim + muzik (PD Satie: Gnossienne 1 -> Gymnopedie 1) + efektler. Muzik ve efekt anlatim altinda kisilir; -14 LUFS master.
# ./mix.sh long|short
set -e
cd "${0:A:h}"; M="$1"; ROOT="/Users/claude-eng/Shorts - Reels"
export PATH=$(python3 -c "import json;print(json.load(open('$ROOT/.claude/settings.json'))['env']['PATH'])"):$PATH
VO=audio/vo.wav; [ "$M" = short ] && VO=audio/vo-kisa.wav
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "audio/bed-$M.wav")
# gecis: "Ama geriye bir sey kalir" (uzun 216.16 sn; kisada o kesitin basi)
SW=$(python3 -c "
import json;d=json.load(open('timeline.json'));sw=d['sw']
if '$M'=='short':
  sw=[ss+max(0,sw-ls) for ls,le,ss in d['short']['segs'] if ls-1.2<=sw<le][0]
print(round(sw,2))")
X=4   # capraz gecis
ffmpeg -v error -y -i audio/muzik/gnossienne1.ogg -i audio/muzik/gymnopedie1.ogg -filter_complex \
 "[0:a]aresample=48000,atrim=0:$((SW + X / 2.0)),asetpts=N/SR/TB[g];\
  [1:a]aresample=48000,asetpts=N/SR/TB[y];\
  [g][y]acrossfade=d=${X}:c1=tri:c2=tri,apad,atrim=0:$DUR,afade=t=in:d=1.5,afade=t=out:st=$((DUR - 4)):d=4,loudnorm=I=-24:TP=-3:LRA=11,aresample=48000[m]" \
 -map "[m]" -c:a pcm_s24le "audio/muzik-$M.wav"
ffmpeg -v error -y -i "$VO" -i "audio/bed-$M.wav" -i "audio/muzik-$M.wav" -filter_complex \
 "[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,apad[vo];\
  [vo]asplit=3[v1][v2][v3];\
  [1:a]aresample=48000,volume=0.55[fx];\
  [2:a]aresample=48000,volume=0.9[mu];\
  [mu][v2]sidechaincompress=threshold=0.02:ratio=5:attack=60:release=700[mud];\
  [fx][v3]sidechaincompress=threshold=0.03:ratio=3:attack=30:release=400[fxd];\
  [v1][mud][fxd]amix=inputs=3:duration=longest:normalize=0[m]" -map "[m]" -t $DUR -c:a pcm_s24le "audio/mix-$M.wav"
"$ROOT/araclar/venv-vahdet/bin/python" "$ROOT/araclar/cinecode/scripts/master_audio.py" "audio/mix-$M.wav" "audio/master-$M.wav" | tail -1
echo "gecis $SW sn"

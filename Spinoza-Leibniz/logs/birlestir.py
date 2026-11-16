# Sercan (dış ses + Spinoza) ve Orhan (Leibniz) kayıtlarını senaryo sırasına dizer, seviyeleri eşitler.
import subprocess, json, os
FF = "/Users/claude-eng/Shorts - Reels/araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64/ffmpeg"
os.chdir(os.path.join(os.path.dirname(__file__), "..", "ses"))
S, O = "vo-sercan.mp3", "vo-orhan.mp3"
# (dosya, başlangıç, bitiş[None=son], konuşan, sonrasına eklenecek sessizlik)
PARCA = [
  (S, 0.0, 33.1, "anlatici+spinoza", 0.35),
  (O, 0.0, 15.3, "leibniz", 0.35),
  (S, 33.1, 50.3, "spinoza", 0.45),
  (O, 15.3, 29.9, "leibniz", 0.30),
  (S, 50.3, 54.6, "spinoza", 0.15),
  (O, 29.9, None, "leibniz", 0.60),
  (S, 54.6, None, "anlatici", 0.0),
]
os.makedirs("parca", exist_ok=True)
lst, t, harita = [], 0.0, []
for i, (f, a, b, kim, sus) in enumerate(PARCA):
    out = f"parca/{i}.wav"
    cut = ["-ss", str(a)] + (["-to", str(b)] if b else [])
    subprocess.run([FF, "-v", "error", "-y", "-i", f, *cut, "-af",
        f"loudnorm=I=-18:TP=-2:LRA=11,apad=pad_dur={sus}", "-ar", "48000", "-ac", "1", out], check=True)
    d = float(subprocess.run([FF[:-6] + "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    harita.append({"kim": kim, "kaynak": f, "kaynak_bas": a, "bas": round(t, 3), "son": round(t + d, 3)})
    lst.append(f"file '{out}'"); t += d
open("parca/list.txt", "w").write("\n".join(l.replace("parca/", "") for l in lst))
subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "parca/list.txt", "-c:a", "pcm_s16le", "vo.wav"], check=True)
subprocess.run([FF, "-v", "error", "-y", "-i", "vo.wav", "-c:a", "libmp3lame", "-b:a", "192k", "vo.mp3"], check=True)
json.dump(harita, open("parcalar.json", "w"), ensure_ascii=False, indent=1)
print("vo.mp3", round(t, 2), "sn;", [(h["kim"], h["bas"]) for h in harita])

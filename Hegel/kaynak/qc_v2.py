# QC for v2 outputs: hook frames + 8 spread frames as one contact sheet, Whisper on the first 6 s and the last 6 s.
# Usage: python kaynak/qc_v2.py <video.mp4> <out_prefix> <hook frame times comma-sep>
import sys, subprocess, json, numpy as np
from PIL import Image
from faster_whisper import WhisperModel
vid, pre, hk = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vid], capture_output=True, text=True).stdout)
def frame(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", vid, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    p = f"{pre}-{t:06.2f}.png"; open(p, "wb").write(raw); return Image.open(p).convert("RGB")
spread = [dur * (k + 0.5) / 8 for k in range(8)]
for name, ts in (("hook", hk), ("spread", spread)):
    ims = [frame(t) for t in ts]; w, h = ims[0].size; s = 480 / max(w, h)
    th = [i.resize((int(w * s), int(h * s))) for i in ims]
    sheet = Image.new("RGB", (th[0].width * min(4, len(th)), th[0].height * ((len(th) + 3) // 4)))
    for k, t in enumerate(th): sheet.paste(t, ((k % 4) * t.width, (k // 4) * t.height))
    sheet.save(f"{pre}-{name}.jpg", quality=88)
print("dur", round(dur, 2), "spread", [round(t, 1) for t in spread])
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
for lab, ss in (("START", 0.0), ("END", max(0, dur - 7))):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", "7", "-i", vid, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, language="tr", word_timestamps=True, beam_size=5, initial_prompt="Hegel, Aufhebung.")
    ws = [(round(ss + w.start, 2), w.word.strip()) for s_ in segs for w in s_.words]
    print(lab, ws, flush=True)
loud = subprocess.run(["ffmpeg", "-v", "info", "-i", vid, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print("LOUD", " ".join(l.strip() for l in loud.splitlines()[-12:] if ("I:" in l or "Peak:" in l)))

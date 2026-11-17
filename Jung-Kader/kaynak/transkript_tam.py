import sys, subprocess, numpy as np, time
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=10)
pcm = subprocess.run(["ffmpeg","-v","error","-i",src,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
ipucu = "Murat Avcıoğlu, Carl Gustav Jung, bilinçdışı, kader, arketip, gölge, persona, bireyleşme, kolektif bilinçdışı."
segs, info = m.transcribe(audio, language="tr", initial_prompt=ipucu, beam_size=5, vad_filter=True, condition_on_previous_text=False)
t0=time.time()
with open(out, "w") as f:
    for s in segs:
        mm, ss = divmod(int(s.start), 60)
        f.write(f"[{mm:02d}:{ss:02d}] {s.text.strip()}\n"); f.flush()
print("bitti", time.time()-t0)

# Whisper the last 7 s of each deliverable and print the final words.
import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
    pcm = subprocess.run(["ffmpeg","-v","error","-ss",str(max(0,d-7)),"-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
    segs, _ = m.transcribe(a, language="tr", beam_size=5, vad_filter=True, condition_on_previous_text=False)
    print(f.split("/")[-1], f"{d:.1f}s ->", " ".join(s.text.strip() for s in segs), flush=True)

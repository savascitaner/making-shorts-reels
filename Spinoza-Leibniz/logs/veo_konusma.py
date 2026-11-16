# Veo klibindeki konuşmayı (Türkçe) kelime zamanlarıyla çıkarır.
import sys, os, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
for f in sys.argv[1:]:
    pcm = subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
    segs, _ = m.transcribe(a, language="tr", word_timestamps=True, vad_filter=(os.environ.get("VAD","1")=="1"))
    w = [x for s in segs for x in s.words]
    print(f.split('/')[-1], " ".join(f"{x.word.strip()}[{x.start:.2f}-{x.end:.2f}]" for x in w))

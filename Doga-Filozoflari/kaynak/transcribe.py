import json, sys
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
import subprocess, numpy as np
pcm = subprocess.run(["ffmpeg","-v","error","-i",src,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
segs, info = m.transcribe(audio, language="tr", word_timestamps=True, initial_prompt="Tales, Milet, Anaksimandros, Anaksimenes, apeyron, arke, Herakleitos, Efes, Parmenides, Elea, Zenon, Ahilleus, Empedokles, Etna, Lökippos, Demokritos, Abdera, Con Dolton.", beam_size=5, vad_filter=True, condition_on_previous_text=False)
words = []
for s in segs:
    for w in s.words:
        words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)})
json.dump(words, open(out, "w"), ensure_ascii=False, indent=0)
print(len(words), "words; last:", words[-4:])

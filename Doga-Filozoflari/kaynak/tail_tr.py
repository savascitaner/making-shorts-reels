import json, sys, subprocess, numpy as np
from faster_whisper import WhisperModel
src, t0, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
pcm = subprocess.run(["ffmpeg","-v","error","-ss",str(t0),"-i",src,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
segs, _ = m.transcribe(audio, language="tr", word_timestamps=True, beam_size=5, vad_filter=True, condition_on_previous_text=False,
    initial_prompt="Minerva'nın baykuşu, alacakaranlık, Aufhebung, Hegel.")
words = [{"w": w.word.strip(), "s": round(w.start + t0, 3), "e": round(w.end + t0, 3)} for s in segs for w in s.words]
json.dump(words, open(out, "w"), ensure_ascii=False, indent=0); print(" ".join(x["w"] for x in words))

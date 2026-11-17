# Kaydın bir aralığını ayrı transkribe eder: python parca.py vo.wav bas son [cikti.json]
import json, sys, subprocess, numpy as np
from faster_whisper import WhisperModel
src, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); out = sys.argv[4] if len(sys.argv) > 4 else None
CFG = json.load(open('../video.json'))
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
pcm = subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-t",str(b-a),"-i",src,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
segs, _ = m.transcribe(audio, language="tr", word_timestamps=True, initial_prompt=CFG["whisper_ipucu"], beam_size=5, vad_filter=True, condition_on_previous_text=False)
W = [{"w": w.word.strip(), "s": round(w.start+a, 3), "e": round(w.end+a, 3), "p": round(w.probability, 3)} for s in segs for w in s.words]
print(" ".join(f"{x['w']}[{x['s']:.1f}]" for x in W))
if out: json.dump(W, open(out, "w"), ensure_ascii=False)

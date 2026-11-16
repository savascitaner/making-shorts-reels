# Replace the narration from "Sence" to the end with the new closing take; write the tail alone for a local transcription.
import json, subprocess, sys, numpy as np
from scipy.io import wavfile
FF = sys.argv[1]; SR = 48000
def dec(f): return np.frombuffer(subprocess.run([FF, "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
w = json.load(open("kaynak/words.json"))["words"]
i0 = next(i for i, x in enumerate(w) if i > 250 and x["w"].startswith("Sence"))
sr, vo = wavfile.read("kaynak/audio/vo-v2.wav"); vo = vo.astype(np.float32)
new = dec("ses/kapanis.mp3")
env = np.convolve(np.abs(new), np.ones(480) / 480, "same"); on = np.where(env > 0.01)[0]
new = new[max(0, on[0] - 480): on[-1] + 4800]
rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)
a = int(w[i0 - 12]["s"] * SR); b = int(w[i0 - 1]["e"] * SR)          # the last sentences before "Sence"
new *= rms(vo[a:b]) / rms(new)
cut = int((w[i0]["s"] - 0.05) * SR)
out = np.concatenate([vo[:cut], new]); out /= max(1.0, np.abs(out).max() / 0.98)
wavfile.write("kaynak/audio/vo.wav", SR, out.astype(np.float32))
wavfile.write("kaynak/audio/tail.wav", SR, new.astype(np.float32))
json.dump({"cut": cut / SR, "i0": i0}, open("kaynak/tail-info.json", "w"))
print(f"cut at {cut / SR:.2f}s (word {i0} {w[i0]['w']}), new tail {len(new) / SR:.2f}s, total {len(out) / SR:.2f}s")

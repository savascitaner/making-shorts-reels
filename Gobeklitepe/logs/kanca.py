# Replace the first sentence of the narration with the new hook take, keep every later word where it was.
import json, subprocess, sys, numpy as np
from scipy.io import wavfile
FF = sys.argv[1]; SR = 48000
def dec(f): return np.frombuffer(subprocess.run([FF, "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
w = json.load(open("kaynak/words.json"))["words"]
orig, new = dec("ses/vo-v1.mp3"), dec("ses/kanca-aclik.mp3")
env = np.convolve(np.abs(new), np.ones(480) / 480, "same"); on = np.where(env > 0.01)[0]
new = new[max(0, on[0] - 480): on[-1] + 2400]                      # trim silence, keep 10 ms before / 50 ms after
a, b = int(w[0]["s"] * SR), int(w[6]["e"] * SR)
rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)
new *= rms(orig[a:b]) / rms(new)                                     # same level as the old first sentence
gap = w[7]["s"] - w[6]["e"]; cut = int((w[7]["s"] - 0.08) * SR)
out = np.concatenate([np.zeros(a, np.float32), new, np.zeros(int((gap - 0.08) * SR), np.float32), orig[cut:]])
out /= max(1.0, np.abs(out).max() / 0.98)
wavfile.write("kaynak/audio/vo.wav", SR, out.astype(np.float32))
print(f"old sentence {w[6]['e'] - w[0]['s']:.2f}s, new {len(new) / SR:.2f}s, total {len(out) / SR:.2f}s (was {len(orig) / SR:.2f}s)")

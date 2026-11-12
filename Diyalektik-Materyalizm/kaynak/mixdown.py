# VO + ducked music + ambience + sfx -> audio/mix.wav (float). Master afterwards with cinecode master_audio.py
import numpy as np, subprocess, json
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 48000; DUR = 124.0; N = int(SR * DUR)
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "audio/vo.wav", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
vo = np.frombuffer(pcm, np.float32).reshape(-1, 2); V = np.zeros((N, 2), np.float32); V[:len(vo)] = vo[:N]
def ld(f): sr, x = wavfile.read(f); return x[:N].astype(np.float32)
mus, amb, sfx = ld("audio/music.wav"), ld("audio/amb.wav"), ld("audio/sfx.wav")
rms = lambda x: np.sqrt(np.mean(x[np.abs(x).max(1) > 1e-4] ** 2) + 1e-12)
vr = rms(V)
# speech activity from word timings (more robust than RMS for ducking)
W = json.load(open("words.json"))["words"]
act = np.zeros(N, np.float32)
for w in W: act[int(max(0, w["s"] - 0.15) * SR):int((w["e"] + 0.25) * SR)] = 1
sos = butter(1, 2.5, fs=SR, output="sos"); env = np.clip(sosfilt(sos, act) * 1.15, 0, 1)
duck = 10 ** ((-7.0 * env) / 20)
mix = V * 1.0
mix += mus * (vr / rms(mus)) * 10 ** (-13 / 20) * duck[:, None]
mix += amb * (vr / rms(amb)) * 10 ** (-24 / 20) * (10 ** ((-4 * env) / 20))[:, None]
mix += sfx * (vr / (np.abs(sfx).max() + 1e-9)) * 10 ** (-3 / 20) * 0.9
wavfile.write("audio/mix.wav", SR, mix.astype(np.float32))
print("peak", float(np.abs(mix).max()))

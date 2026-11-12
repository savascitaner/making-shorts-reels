# music (Goldberg Aria, CC0) + ambience + sfx for Spinoza -> audio/music.wav, amb.wav, sfx.wav
import numpy as np, subprocess, json
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 48000; DUR = json.load(open('../video.json'))['sure']; N = int(SR * DUR); BOOM = 3.15; ANLA = 115.0; END = 117.6
pcm = subprocess.run(["ffmpeg","-v","error","-i","../muzik-aday/goldberg-aria.ogg","-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
m = np.frombuffer(pcm, np.float32).reshape(-1, 2).copy(); M = np.zeros((N, 2), np.float32)
# hook: aria from the start, cut to silence at the whisper pause, re-enters after the slam
t = np.arange(N) / SR
src = m[:N] if len(m) >= N else np.pad(m, ((0, N - len(m)), (0, 0)))
M[:] = src
g = np.ones(N, np.float32)
g[(t > 1.75) & (t < BOOM + 1.2)] = 0.0
g *= np.clip((t - 0.0) / 0.4, 0, 1)                      # fade in at start
cut = (t >= 1.45) & (t <= 1.75); g[cut] = 1 - (t[cut] - 1.45) / 0.3
re = (t >= BOOM + 1.2) & (t <= BOOM + 3.2); g[re] = (t[re] - BOOM - 1.2) / 2.0
dip = (t >= ANLA - 1.2) & (t <= ANLA + 1.0); g[dip] *= np.clip(1 - (t[dip] - (ANLA - 1.2)) / 0.8, 0.15, 1)   # hush for "Anla."
up = t > ANLA + 1.0; g[up] *= np.clip(0.15 + (t[up] - ANLA - 1.0) / 1.5, 0, 1.2)
fo = t > DUR - 3; g[fo] *= np.clip((DUR - t[fo]) / 3, 0, 1)
wavfile.write("audio/music.wav", SR, (M * g[:, None]).astype(np.float32))
# ambience: warm room tone + faint candle crackle
r = np.random.default_rng(3); n = r.standard_normal((N, 2)).astype(np.float32)
amb = sosfilt(butter(2, 300, fs=SR, output="sos"), n, axis=0)
cr = np.zeros((N, 2), np.float32); idx = r.integers(0, N, 900); cr[idx] = r.uniform(-1, 1, (900, 1)) * 0.6
cr = sosfilt(butter(2, [1500, 6000], btype="band", fs=SR, output="sos"), cr, axis=0)
A = (amb / np.abs(amb).max() + cr * 2).astype(np.float32); A[t < BOOM + 0.6] *= 0.3
wavfile.write("audio/amb.wav", SR, A)
# sfx: whoosh on the throw, sub boom on the slam, soft low hit on "Anla."
S = np.zeros((N, 2), np.float32)
def put(at, x): i = int(at * SR); S[i:i + len(x)] += x[:N - i, None] if x.ndim == 1 else x[:N - i]
L = int(0.9 * SR); tt = np.arange(L) / SR
wh = sosfilt(butter(2, [400, 3000], btype="band", fs=SR, output="sos"), r.standard_normal(L)) * np.sin(np.pi * tt / 0.9) ** 2
put(0.15, (wh / np.abs(wh).max() * 0.5).astype(np.float32))
L = int(2.2 * SR); tt = np.arange(L) / SR
boom = np.sin(2 * np.pi * (48 * tt - 10 * tt ** 2)) * np.exp(-tt * 2.2) + 0.4 * sosfilt(butter(2, 180, fs=SR, output="sos"), r.standard_normal(L)) * np.exp(-tt * 9)
put(BOOM, (boom / np.abs(boom).max()).astype(np.float32))
L = int(1.6 * SR); tt = np.arange(L) / SR
hit = np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 3.0)
put(ANLA - 0.05, (hit * 0.55).astype(np.float32))
wavfile.write("audio/sfx.wav", SR, S)
print("ok")

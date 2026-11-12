# music (Bach Cello Suite 1 Sarabande, PD) + ambience + sfx -> audio/music.wav, amb.wav, sfx.wav
import numpy as np, subprocess, json
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 48000; DUR = json.load(open('../video.json'))['sure']; N = int(SR * DUR); BOOM = 5.1; MERKEZ = 46.6; SENSIN = 49.2; END = 121.6
pcm = subprocess.run(["ffmpeg","-v","error","-i","../muzik/cello-sarabande.ogg","-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
m = np.frombuffer(pcm, np.float32).reshape(-1, 2).copy()
t = np.arange(N) / SR
M = m[:N] if len(m) >= N else np.pad(m, ((0, N - len(m)), (0, 0)))
g = np.clip(t / 0.5, 0, 1).astype(np.float32)
sil = (t > 4.2) & (t < BOOM + 1.0); g[sil] = 0                       # hush after the question, re-enter after the split
cut = (t >= 3.9) & (t <= 4.2); g[cut] = 1 - (t[cut] - 3.9) / 0.3
re = (t >= BOOM + 1.0) & (t <= BOOM + 3.0); g[re] = (t[re] - BOOM - 1.0) / 2.0
dip = (t >= MERKEZ - 2.5) & (t <= SENSIN + 1.5); g[dip] *= 0.45     # quiet under Musa's answer
fo = t > DUR - 3; g[fo] *= np.clip((DUR - t[fo]) / 3, 0, 1)
wavfile.write("audio/music.wav", SR, (M * g[:, None]).astype(np.float32))
r = np.random.default_rng(5); n = r.standard_normal((N, 2)).astype(np.float32)
amb = sosfilt(butter(2, 300, fs=SR, output="sos"), n, axis=0)
cr = np.zeros((N, 2), np.float32); idx = r.integers(0, N, 900); cr[idx] = r.uniform(-1, 1, (900, 1)) * 0.6
cr = sosfilt(butter(2, [1500, 6000], btype="band", fs=SR, output="sos"), cr, axis=0)
A = (amb / np.abs(amb).max() + cr * 2).astype(np.float32); A[t < BOOM] *= 0.3
wavfile.write("audio/amb.wav", SR, A)
S = np.zeros((N, 2), np.float32)
def put(at, x): i = int(at * SR); S[i:i + len(x)] += x[:N - i, None] if x.ndim == 1 else x[:N - i]
L = int(2.2 * SR); tt = np.arange(L) / SR
boom = np.sin(2 * np.pi * (48 * tt - 10 * tt ** 2)) * np.exp(-tt * 2.2) + 0.4 * sosfilt(butter(2, 180, fs=SR, output="sos"), r.standard_normal(L)) * np.exp(-tt * 9)
put(BOOM - 0.05, (boom / np.abs(boom).max()).astype(np.float32))
L = int(1.2 * SR); tt = np.arange(L) / SR                            # three soft ticks on SAVAŞ? HASTALIK? ÖLÜM?
tick = np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 8)
for k in (4.25, 4.55, 4.85): put(k, (tick * 0.35).astype(np.float32))
L = int(3.0 * SR); tt = np.arange(L) / SR                            # bell-like tone on "Merkezinde."
bell = (np.sin(2*np.pi*220*tt) + 0.5*np.sin(2*np.pi*440*tt) + 0.25*np.sin(2*np.pi*661*tt)) * np.exp(-tt * 1.6)
put(MERKEZ, (bell / np.abs(bell).max() * 0.45).astype(np.float32))
put(119.2, (bell / np.abs(bell).max() * 0.35).astype(np.float32))   # "merkezden bakan göz"
L = int(1.6 * SR); tt = np.arange(L) / SR
hit = np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 3.0)
put(END - 0.1, (hit * 0.5).astype(np.float32))
wavfile.write("audio/sfx.wav", SR, S)
print("ok")

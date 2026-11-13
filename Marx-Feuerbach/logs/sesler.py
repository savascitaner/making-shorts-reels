# music (Beethoven Eroica II Marcia funebre, PD Musopen) + ambience + sfx -> audio/music.wav, amb.wav, sfx.wav
import numpy as np, subprocess, json
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 48000; DUR = json.load(open('../video.json'))['sure']; N = int(SR * DUR)
W = json.load(open('words.json'))['words']; wt = lambda i: W[i]['s']
pcm = subprocess.run(["ffmpeg","-v","error","-i","../muzik/eroica-marcia.ogg","-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
m = np.frombuffer(pcm, np.float32).reshape(-1, 2).copy()
t = np.arange(N) / SR
M = m[:N] if len(m) >= N else np.pad(m, ((0, N - len(m)), (0, 0)))
g = np.clip(t / 0.6, 0, 1).astype(np.float32) * 0.85
for i in (277, 342):                                   # a held breath before "Bu mistik olmuş!" and the final line
    a = wt(i) - 0.9; k = (t > a) & (t < wt(i) + 0.2); g[k] *= 0.35
sw = (t > wt(346)) & (t < DUR); g[sw] *= np.clip(1 + (t[sw] - wt(346)) / 2.0, 1, 1.6)   # swell on "değiştirmektir!" into the end card
fo = t > DUR - 2.8; g[fo] *= np.clip((DUR - t[fo]) / 2.8, 0, 1)
wavfile.write("audio/music.wav", SR, (M * g[:, None]).astype(np.float32))
r = np.random.default_rng(5); n = r.standard_normal((N, 2)).astype(np.float32)
amb = sosfilt(butter(2, 260, fs=SR, output="sos"), n, axis=0)           # room tone
cr = np.zeros((N, 2), np.float32); idx = r.integers(0, N, 1100); cr[idx] = r.uniform(-1, 1, (1100, 1)) * 0.6
cr = sosfilt(butter(2, [1500, 6000], btype="band", fs=SR, output="sos"), cr, axis=0)   # candle crackle
A = (amb / np.abs(amb).max() + cr * 2).astype(np.float32)
fab = (t > wt(86) - 0.3) & (t < wt(102) - 0.2)                          # factory rumble under the worker lines
rum = sosfilt(butter(2, [40, 140], btype="band", fs=SR, output="sos"), r.standard_normal(N)).astype(np.float32)
rum *= (0.5 + 0.5 * np.sin(2 * np.pi * 1.6 * t)).astype(np.float32); env = np.zeros(N, np.float32); env[fab] = 1
env = sosfilt(butter(1, 1.0, fs=SR, output="sos"), env).astype(np.float32)
A += (rum / np.abs(rum).max() * 1.4 * env)[:, None]
wavfile.write("audio/amb.wav", SR, A)
S = np.zeros((N, 2), np.float32)
def put(at, x, v=1.0): i = int(at * SR); j = min(N, i + len(x)); S[i:j] += (x[:j - i] * v)[:, None]
L = int(1.8 * SR); tt = np.arange(L) / SR
hit = (np.sin(2 * np.pi * (52 * tt - 8 * tt ** 2)) * np.exp(-tt * 2.6) + 0.35 * sosfilt(butter(2, 200, fs=SR, output="sos"), r.standard_normal(L)) * np.exp(-tt * 10)).astype(np.float32)
hit /= np.abs(hit).max()
for i, v in ((138, 0.7), (196, 0.7), (218, 0.55), (277, 0.9), (346, 1.0)): put(wt(i) - 0.04, hit, v)
L = int(2.5 * SR); tt = np.arange(L) / SR
bell = ((np.sin(2*np.pi*196*tt) + 0.5*np.sin(2*np.pi*392*tt) + 0.25*np.sin(2*np.pi*589*tt)) * np.exp(-tt * 1.8)).astype(np.float32); bell /= np.abs(bell).max()
put(0.0, bell, 0.35); put(176.6, bell, 0.4)
wavfile.write("audio/sfx.wav", SR, S)
print("ok")

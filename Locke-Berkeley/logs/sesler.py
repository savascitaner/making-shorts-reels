# music (Bach, Goldberg Aria, Kimiko Ishizaka, CC0) + room/candle ambience + sfx -> kaynak/audio/music.wav, amb.wav, sfx.wav
import numpy as np, subprocess, json
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 48000; DUR = json.load(open('../video.json'))['sure']; N = int(SR * DUR)
W = json.load(open('words.json'))['words']; wt = lambda i: W[i]['s']; we = lambda i: W[i]['e']
pcm = subprocess.run(["ffmpeg","-v","error","-i","../muzik/aria.ogg","-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
m = np.frombuffer(pcm, np.float32).reshape(-1, 2).copy()
t = np.arange(N) / SR
BOOM = wt(6) - 0.05
M = np.zeros((N, 2), np.float32); st = int(BOOM * SR); seg = m[:N - st]; M[st:st + len(seg)] = seg   # music enters on the hard hit
g = np.ones(N, np.float32) * 0.85
for i in (141, 158):                                   # held breath before "Ses çıktı mı?" and "yok mu oldu?"
    k = (t > wt(i) - 0.9) & (t < we(i + 1) + 0.3); g[k] *= 0.3
ag = (t > wt(135) - 0.3) & (t < wt(141) - 0.9); g[ag] *= 0.45   # the forest: music thins out
sw = t > wt(219); g[sw] *= np.clip(1 + (t[sw] - wt(219)) / 3.0, 1, 1.5)
fo = t > DUR - 2.8; g[fo] *= np.clip((DUR - t[fo]) / 2.8, 0, 1)
g = sosfilt(butter(1, 3, fs=SR, output="sos"), g).astype(np.float32)
wavfile.write("audio/music.wav", SR, (M * g[:, None]).astype(np.float32))
r = np.random.default_rng(5); n = r.standard_normal((N, 2)).astype(np.float32)
amb = sosfilt(butter(2, 260, fs=SR, output="sos"), n, axis=0)
cr = np.zeros((N, 2), np.float32); idx = r.integers(0, N, 1100); cr[idx] = r.uniform(-1, 1, (1100, 1)) * 0.6
cr = sosfilt(butter(2, [1500, 6000], btype="band", fs=SR, output="sos"), cr, axis=0)
A = (amb / np.abs(amb).max() + cr * 2).astype(np.float32)
wind = (t > wt(135) - 0.4) & (t < wt(144) - 0.2)            # forest wind under the riddle
wn = sosfilt(butter(2, [200, 900], btype="band", fs=SR, output="sos"), r.standard_normal(N)).astype(np.float32)
wn *= (0.6 + 0.4 * np.sin(2 * np.pi * 0.2 * t)).astype(np.float32); env = np.zeros(N, np.float32); env[wind] = 1
env = sosfilt(butter(1, 1.0, fs=SR, output="sos"), env).astype(np.float32)
A += (wn / np.abs(wn).max() * 1.6 * env)[:, None]
wavfile.write("audio/amb.wav", SR, A)
S = np.zeros((N, 2), np.float32)
def put(at, x, v=1.0): i = int(at * SR); j = min(N, i + len(x)); S[i:j] += (x[:j - i] * v)[:, None]
L = int(1.8 * SR); tt = np.arange(L) / SR
hit = (np.sin(2 * np.pi * (52 * tt - 8 * tt ** 2)) * np.exp(-tt * 2.6) + 0.35 * sosfilt(butter(2, 200, fs=SR, output="sos"), r.standard_normal(L)) * np.exp(-tt * 10)).astype(np.float32)
hit /= np.abs(hit).max()
for i, v in ((6, 1.0), (67, 0.6), (80, 0.6), (134, 0.85), (141, 0.9), (160, 0.6)): put(wt(i) - 0.04, hit, v)
L = int(3.0 * SR); tt = np.arange(L) / SR                     # tree: creak, then a deep crash
creak = np.sin(2 * np.pi * (180 + 60 * np.sin(2 * np.pi * 3 * tt)) * tt) * np.exp(-((tt - 0.5) / 0.35) ** 2) * 0.4
crash = sosfilt(butter(2, 300, fs=SR, output="sos"), r.standard_normal(L)) * np.exp(-np.clip(tt - 1.1, 0, None) * 2.2) * (tt > 1.1)
tree = (creak + crash * 3 + np.sin(2 * np.pi * 45 * tt) * np.exp(-np.clip(tt - 1.1, 0, None) * 3) * (tt > 1.1)).astype(np.float32); tree /= np.abs(tree).max()
put(wt(138) - 1.0, tree, 0.8)
L = int(2.5 * SR); tt = np.arange(L) / SR
bell = ((np.sin(2*np.pi*196*tt) + 0.5*np.sin(2*np.pi*392*tt) + 0.25*np.sin(2*np.pi*589*tt)) * np.exp(-tt * 1.8)).astype(np.float32); bell /= np.abs(bell).max()
put(119.7, bell, 0.4)
wavfile.write("audio/sfx.wav", SR, S)
print("ok")

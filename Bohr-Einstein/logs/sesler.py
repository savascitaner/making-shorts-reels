# müzik (Bach, Cello Suite 1 Prelude + Sarabande, PD) + oda tonu + efektler -> kaynak/audio/music.wav, amb.wav, sfx.wav
import numpy as np, subprocess, json
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 48000; DUR = json.load(open('../video.json'))['sure']; N = int(SR * DUR)
W = json.load(open('words.json'))['words']; wt = lambda i: W[i]['s']; we = lambda i: W[i]['e']
def ogg(p):
    pcm = subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(pcm, np.float32).reshape(-1, 2).copy()
t = np.arange(N) / SR
BOOM = json.load(open('../video.json'))['boom'][0]
P = ogg('../muzik/cello-prelude.ogg'); S = ogg('../muzik/cello-sarabande.ogg')
M = np.zeros((N, 2), np.float32)
a = int(BOOM * SR); seg = P[:N - a]; M[a:a + len(seg)] += seg
X = wt(324) - 0.8; b = int(X * SR); seg2 = S[:N - b]
xf = np.clip((t - X) / 2.5, 0, 1).astype(np.float32)
M *= (1 - xf)[:, None]; M[b:b + len(seg2)] += seg2 * xf[b:b + len(seg2), None]
g = np.ones(N, np.float32) * 0.9
for i0, i1, k in ((162, 167, 0.35), (335, 338, 0.4)):          # hush: sleepless night, last drawing
    m = (t > wt(i0) - 0.6) & (t < wt(i1) - 0.2); g[m] *= k
m = (t > wt(126) - 0.3) & (t < we(161)); g[m] *= 0.75            # chalk board: let the chalk be heard
fo = t > DUR - 2.8; g[fo] *= np.clip((DUR - t[fo]) / 2.8, 0, 1)
g = sosfilt(butter(1, 3, fs=SR, output="sos"), g).astype(np.float32)
wavfile.write("audio/music.wav", SR, (M * g[:, None]).astype(np.float32))
r = np.random.default_rng(7); n = r.standard_normal((N, 2)).astype(np.float32)
A = sosfilt(butter(2, 300, fs=SR, output="sos"), n, axis=0); A /= np.abs(A).max()
hum = (0.25 * np.sin(2 * np.pi * 55 * t) * (t < BOOM)).astype(np.float32)        # low drone under the whisper
A += hum[:, None]
wavfile.write("audio/amb.wav", SR, A.astype(np.float32))
S2 = np.zeros((N, 2), np.float32)
def put(at, x, v=1.0, pan=0.0):
    i = int(at * SR); j = min(N, i + len(x));
    if i < 0 or i >= N: return
    S2[i:j, 0] += x[:j - i] * v * np.sqrt(0.5 * (1 - pan)); S2[i:j, 1] += x[:j - i] * v * np.sqrt(0.5 * (1 + pan))
def env(L, att, dec): tt = np.arange(L) / SR; return np.minimum(1, tt / att) * np.exp(-tt * dec)
L = int(1.8 * SR); tt = np.arange(L) / SR
hit = (np.sin(2 * np.pi * (52 * tt - 8 * tt ** 2)) * np.exp(-tt * 2.6) + 0.35 * sosfilt(butter(2, 200, fs=SR, output="sos"), r.standard_normal(L)) * np.exp(-tt * 10)).astype(np.float32); hit /= np.abs(hit).max()
tick = (sosfilt(butter(2, [2000, 6000], btype="band", fs=SR, output="sos"), r.standard_normal(int(0.03 * SR))) * env(int(0.03 * SR), 0.001, 200)).astype(np.float32); tick /= np.abs(tick).max()
for k in np.arange(0.3, BOOM - 0.2, 0.5): put(k, tick, 0.35, 0.3)                          # clock ticking in the hook
for k in np.arange(wt(150), wt(158), 0.5): put(k, tick, 0.3, -0.2)                          # the clock in the box
def chalk(d):
    L = int(d * SR); x = sosfilt(butter(2, [1500, 7000], btype="band", fs=SR, output="sos"), r.standard_normal(L)); x *= (0.5 + 0.5 * np.abs(np.sin(np.arange(L) / SR * 2 * np.pi * 9))) * np.minimum(1, np.arange(L) / (0.03 * SR)) * np.exp(-np.arange(L) / SR * 1.2)
    return (x / np.abs(x).max()).astype(np.float32)
for i in (130, 134, 137, 150): put(wt(i), chalk(0.9), 0.28)
clk = (sosfilt(butter(2, [800, 4000], btype="band", fs=SR, output="sos"), r.standard_normal(int(0.06 * SR))) * env(int(0.06 * SR), 0.001, 80)).astype(np.float32); clk /= np.abs(clk).max()
put(wt(138), clk, 0.6); put(wt(211), clk, 0.9); put(wt(211) + 0.12, clk, 0.5)               # shutter, chess king falls
L = int(1.2 * SR); tt = np.arange(L) / SR
sw = (np.sin(2 * np.pi * (500 + 1800 * tt) * tt) * np.exp(-tt * 3) * np.minimum(1, tt / 0.05) * 0.6).astype(np.float32)
put(wt(142), sw, 0.5, 0.4); put(wt(182), sw, 0.4, 0.4)                                     # photon leaves
zap = (np.sin(2 * np.pi * 880 * tt) * np.sin(2 * np.pi * 6 * tt) * np.exp(-tt * 4)).astype(np.float32)
put(wt(243), zap, 0.5)                                                                      # measurement: both particles at once
for i, v in ((4, 1.0), (93, 0.55), (167, 0.6), (211, 0.75), (312, 0.6), (335, 0.7)): put(wt(i) - 0.04 if i != 4 else BOOM, hit, v)
wavfile.write("audio/sfx.wav", SR, S2)
print("ok")

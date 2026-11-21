# Vahdetten Kesrete: kozmik ambient, tamamen kodla (örnek ses yok, lisans sorunu yok).
# uv run --with numpy --with scipy python muzik.py <cikis.wav> <sure> <bolum_sinirlari virgüllü> [patlama_zamani]
import sys, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile
SR = 48000
out, DUR = sys.argv[1], float(sys.argv[2])
B = [0.0] + [float(x) for x in sys.argv[3].split(",") if x] + [DUR]     # bölüm sınırları (s)
BANG = float(sys.argv[4]) if len(sys.argv) > 4 else -1
rng = np.random.default_rng(2026)
N = int(SR * DUR); t = np.arange(N) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
L = np.zeros(N); R = np.zeros(N)
def add(sig, t0, pan=0.0, g=1.0):
    i = int(t0 * SR)
    if i >= N: return
    sig = sig[: N - i] * g
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan)); R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))
def env(n, a, r):
    e = np.ones(n); na = int(a * SR); nr = int(r * SR)
    e[:na] = np.linspace(0, 1, na) ** 2; e[-nr:] = np.minimum(e[-nr:], np.linspace(1, 0, nr) ** 2); return e
# yoğunluk eğrisi (0..1): bölüm başına
def level(tt):
    k = np.searchsorted(B, tt, side="right") - 1; k = min(max(k, 0), len(B) - 2)
    base = [0.35, 0.5, 0.8, 0.65, 0.45, 0.3][min(k, 5)] if len(B) > 6 else [0.35, 0.5, 0.8, 0.65, 0.45][min(k, 4)]
    return base
# akor dizisi (D minör, kozmik): Dm9, Bbmaj7, Gm9, A sus, Dm
CH = [[38, 50, 57, 64, 69], [34, 46, 53, 62, 65], [43, 50, 58, 62, 69], [33, 45, 52, 57, 64], [38, 50, 57, 62, 65]]
step = 14.0; ci = 0; tt = 0.0
while tt < DUR:
    ch = CH[ci % len(CH)]; ln = step + 8
    lv = level(tt)
    n = int(ln * SR); tv = np.arange(n) / SR
    for j, m in enumerate(ch):
        f = hz(m); v = np.zeros(n)
        for d in (-0.07, 0.0, 0.08):                          # detuned katman
            ff = f * 2 ** (d / 12)
            v += np.sin(2 * np.pi * ff * tv + rng.uniform(0, 6)) + 0.35 * np.sin(4 * np.pi * ff * tv) * (0.5 + 0.5 * np.sin(0.2 * tv + j))
        v = lp(v, 900 + 2600 * lv + 800 * np.sin(0.15 * tv + j)) * env(n, 5.5, 7.5)
        add(v, tt, pan=(j - 2) * 0.28, g=(0.05 if m < 45 else 0.032) * (0.6 + 0.8 * lv))
    tt += step; ci += 1
# ışıltılı çanlar (pentatonik), yoğunluğu bölüme göre
PENTA = [74, 77, 79, 81, 84, 86, 89, 93]
tt = 3.0
while tt < DUR - 6:
    lv = level(tt)
    if rng.random() < 0.35 + 0.6 * lv:
        m = PENTA[rng.integers(len(PENTA))]; f = hz(m); ln = 5.5
        tv = np.arange(int(ln * SR)) / SR
        s = np.sin(2 * np.pi * f * tv) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tv) * np.exp(-tv * 3) + 0.25 * np.sin(2 * np.pi * f * 5.4 * tv) * np.exp(-tv * 6)
        s *= np.exp(-tv * 0.9) * np.minimum(1, tv * 200)
        add(s, tt, pan=rng.uniform(-0.8, 0.8), g=0.035 * (0.5 + lv))
    tt += rng.uniform(1.4, 4.2) / (0.5 + lv)
# alt vuruş / yükselen şok (Tekillik anı) ve bölüm geçişlerinde yumuşak yükselişler
def swell(t0, ln, g):
    n = int(ln * SR); tv = np.arange(n) / SR; x = rng.standard_normal(n)
    x = lp(x, 400, 2) * 0 + np.cumsum(x) * 0
    nz = rng.standard_normal(n); sw = np.zeros(n)
    fc = 200 + 5000 * (tv / ln) ** 2
    for k in range(0, n, 2400):
        sw[k:k + 2400] = sosfilt(butter(2, min(fc[k], 20000), btype="low", fs=SR, output="sos"), nz[k:k + 2400])
    sw *= (tv / ln) ** 2
    add(sw, t0, g=g)
for b in B[1:-1]: swell(max(0, b - 6.0), 6.0, 0.07)
if BANG > 0:
    n = int(9 * SR); tv = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (48 - 14 * (1 - np.exp(-tv * 1.2))) * tv) * np.exp(-tv * 0.55)
    add(boom, BANG, g=0.35)
    swell(max(0, BANG - 8), 8.0, 0.1)
# reverb (uzun, geniş)
def reverb(x, sec=4.0, wet=0.45):
    n = int(sec * SR); it = np.arange(n) / SR
    ir = lp(rng.standard_normal(n) * np.exp(-it * 1.3), 5500); ir /= np.sqrt((ir ** 2).sum())
    return x * (1 - wet) + fftconvolve(x, ir)[:N] * wet * 1.5
L, R = reverb(L), reverb(R)
fade = np.minimum(1, np.minimum(t / 3.0, (DUR - t) / 6.0)) ** 2
y = np.stack([L * fade, R * fade], 1); y /= np.abs(y).max() * 1.12
wavfile.write(out, SR, y.astype(np.float32)); print("tamam", out, round(DUR, 1), "sn")

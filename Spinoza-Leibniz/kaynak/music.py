# Spinoza-Leibniz: muzik + ambiyans + efekt, tamamen kodla (lisans sorunu yok).
# Spinoza = tek derin cello notasi, Leibniz = yukselen klavsen arpejleri, imza = mercek cam tinisi.
# Kullanim (uret.sh ses): python music.py audio SURE ...  (diger argumanlar yok sayilir; zamanlar words.json'dan)
import sys, os, json, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile
SR = 48000; outdir, DUR = sys.argv[1], float(sys.argv[2]); N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(1676)
WD = json.load(open('words.json'))['words']; wt = lambda i: WD[i]['s']
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype='low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype='high', fs=SR, output='sos'), x)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, sig, t0, pan=0.0, g=1.0):
        i = int(t0 * SR)
        if i >= N or i + len(sig) <= 0: return
        if i < 0: sig = sig[-i:]; i = 0
        sig = sig[:N - i] * g
        s.L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan)); s.R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))
    def st(s): return np.stack([s.L, s.R], 1)
def reverb(bus, sec=3.5, wet=0.3, decay=1.6, lpf=6000):
    n = int(sec * SR); it = np.arange(n) / SR; out = []
    for ch in (bus.L, bus.R):
        ir = lp(rng.standard_normal(n) * np.exp(-it * decay), lpf); ir /= np.sqrt((ir ** 2).sum())
        out.append(ch * (1 - wet) + fftconvolve(ch, ir)[:N] * wet * 1.6)
    bus.L, bus.R = out
def env(n, att, rel):
    tt = np.arange(n) / SR; d = n / SR
    return np.clip(tt / att, 0, 1) ** 1.5 * np.clip((d - tt) / rel, 0, 1) ** 1.2
def saw(f, tt, vib=0.004, vr=5.0):
    ph = 2 * np.pi * np.cumsum(f * (1 + vib * np.sin(2 * np.pi * vr * tt + rng.uniform(0, 6)))) / SR + rng.uniform(0, 6)
    return 2 * ((ph / (2 * np.pi)) % 1) - 1
# --- cello: bowed, rosin noise, slow vibrato ---
def cello(m, dur, att=0.6, rel=1.8, g=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m)
    y = saw(f, tt, 0.006, 5.2) + 0.5 * saw(f * 1.002, tt, 0.005, 4.7)
    y = lp(y, 900, 3) + 0.15 * bp(rng.standard_normal(n), 1500, 4000) * (0.3 + 0.7 * np.exp(-tt * 2))
    return y * env(n, att, rel) * 0.18 * g
# --- harpsichord: plucked, bright, quick decay, octave coupler ---
def harpsi(m, dur=1.6, vel=0.8):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m); y = np.zeros(n)
    for k in range(1, 14):
        fk = f * k
        if fk > 14000: break
        y += (1 / k ** 0.7) * np.sin(2 * np.pi * fk * tt + rng.uniform(0, 6)) * np.exp(-tt * (2.2 + k * 0.55))
    y += 0.35 * np.sin(2 * np.pi * 2 * f * 1.001 * tt) * np.exp(-tt * 3)
    pluck = hp(rng.standard_normal(n), 2500) * np.exp(-tt * 140) * 0.4
    return (y + pluck) * np.clip(tt / 0.002, 0, 1) * np.clip((dur - tt) / 0.2, 0, 1) * 0.11 * vel
# --- low string pad ---
def pad(ms, dur, att=2.5, rel=3.0, bright=1400, g=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; y = np.zeros(n)
    for m in ms:
        for d in (-0.08, 0.0, 0.09): y += saw(hz(m) * 2 ** (d / 12), tt, 0.003, 4.6)
    return lp(y, bright, 3) * env(n, att, rel) * 0.035 * g / max(1, len(ms)) ** 0.5
# --- glass chime (lens signature) ---
def glass(base=84, dur=3.5, g=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(base); y = np.zeros(n)
    for r, a, d in [(1, 1, 1.4), (2.76, 0.5, 2.2), (5.40, 0.28, 3.5), (8.93, 0.14, 5.0), (1.5, 0.35, 1.8)]:
        y += a * np.sin(2 * np.pi * f * r * tt + rng.uniform(0, 6)) * np.exp(-tt * d)
    return y * np.clip(tt / 0.003, 0, 1) * 0.12 * g

Cm, Ab, Eb, Bb, Fm, G = [48, 55, 60, 63], [44, 56, 60, 63], [51, 55, 58, 63], [46, 53, 58, 62], [41, 56, 60, 65], [43, 55, 59, 62]
mus = Bus()
# 0-3 hook: dark drone under the flame
mus.add(pad([36, 43], 4.2, att=0.3, rel=1.5, bright=500, g=1.4), 0.0)
mus.add(glass(84, 3.0, 1.0), 0.45, pan=0.2)
# "hayir." -> cello stab + sub
mus.add(cello(36, 2.6, att=0.05, rel=1.6, g=1.6), wt(9) - 0.02)
# frame (Lahey) pad
for t0, ch, d in [(6.9, Cm, 5.5), (12.0, Ab, 6.0)]: mus.add(pad(ch, d + 2, g=1.0), t0)
# Spinoza blocks: one deep cello note each, long
def spinoza(t0, t1, notes):
    step = (t1 - t0) / len(notes)
    for i, m in enumerate(notes): mus.add(cello(m, step + 1.6, att=0.9, rel=1.6), t0 + i * step, pan=-0.15)
    k = 0; tt0 = t0
    for ch in [Cm, Fm, Ab, G]:
        if tt0 >= t1: break
        mus.add(pad(ch[:3], min(5.0, t1 - tt0) + 2.5, g=0.7, bright=900), tt0); tt0 += 5.0
# Leibniz blocks: rising harpsichord arpeggios + brighter strings
def leibniz(t0, t1, prog, rate=0.19):
    tt0, k = t0, 0
    while tt0 < t1 - 0.3:
        ch = prog[k % len(prog)]; notes = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[3] + 12, ch[1] + 24, ch[2] + 24, ch[3] + 24, ch[2] + 24]
        for j, m in enumerate(notes):
            tj = tt0 + j * rate
            if tj < t1: mus.add(harpsi(m, 1.4, 0.65 + 0.25 * (j / 8)), tj, pan=0.25 - 0.1 * (j % 2))
        mus.add(pad([ch[0], ch[2] + 12, ch[3] + 12], 8 * rate + 1.8, att=0.6, rel=1.2, bright=2400, g=0.8), tt0)
        tt0 += 8 * rate; k += 1
spinoza(17.9, 32.6, [36, 31, 32])
leibniz(32.6, 48.2, [Cm, Ab, Fm, G, Cm, Eb, Bb, G])
spinoza(48.3, 66.7, [36, 32, 29, 31])
leibniz(66.7, 72.8, [Fm, Bb, Eb, G], rate=0.22)
# "senfoni": karanlik notalar acik akora cozulur
mus.add(pad([39, 51, 55, 58, 63], 4.6, att=1.2, rel=2.0, bright=2600, g=1.6), 72.6)
mus.add(pad([44, 56, 60, 63, 68], 4.0, att=1.0, rel=2.4, bright=2800, g=1.6), 75.4)
for j, m in enumerate([63, 67, 70, 75, 79]): mus.add(harpsi(m, 2.0, 0.6), 75.45 + j * 0.16, pan=0.2)
leibniz(77.0, 80.1, [Ab, Eb], rate=0.24)
# son sozler: once cello (Spinoza fisilti), sonra klavsen ifadesi (Leibniz)
mus.add(cello(43, 4.6, att=1.0, rel=2.0), wt(150) - 0.2, pan=-0.15)
for j, m in enumerate([60, 63, 67, 72, 75]): mus.add(harpsi(m, 1.8, 0.7), wt(156) + j * 0.18, pan=0.25)
mus.add(pad(Cm, 4.5, att=0.8, rel=1.5, g=0.8), 84.4)
# mum soner: muzik susar, sonra yaylilar yavasca yukselir ve "en iyisini" anina oturur
mus.add(pad([36, 43, 48], wt(165) - 88.3 + 0.4, att=0.5, rel=0.3, g=0.8), 88.3)
mus.add(pad([44, 51, 56, 60], 96.6 - 91.0 + 1.0, att=4.5, rel=0.8, bright=1800, g=1.2), 91.0)
mus.add(pad([51, 55, 58, 63, 67], 4.0, att=0.4, rel=2.5, bright=2600, g=1.3), wt(178) - 0.05)
mus.add(glass(91, 3.5, 0.9), wt(178) - 0.02, pan=-0.2)
# soru + kapanis
mus.add(pad([48, 55, 60, 65], 6.6, att=1.0, rel=1.5, bright=1600, g=1.0), 97.6)
mus.add(cello(36, 7.5, att=0.4, rel=4.5, g=1.1), 104.0, pan=-0.1)
mus.add(pad([48, 55, 60, 63, 67], 8.0, att=1.0, rel=4.5, bright=1600, g=1.0), 104.0)
mus.add(glass(84, 4.0, 1.0), 104.05, pan=0.15)
reverb(mus, 3.8, 0.34, 1.4)
fade = np.clip(t / 0.05, 0, 1) * np.clip((DUR - t) / 3.0, 0, 1)
mus.L *= fade; mus.R *= fade

# ---------- ambience ----------
amb = Bus()
def rain_bed(t0, t1, g=1.0, bright=1.0):
    n = int((t1 - t0) * SR); tt = np.arange(n) / SR
    e = np.clip(tt / 0.6, 0, 1) * np.clip((t1 - t0 - tt) / 0.6, 0, 1)
    for ch, pan in ((0, -0.6), (1, 0.6)):
        nz = bp(rng.standard_normal(n), 900 * bright, 7000) * 0.5 + lp(rng.standard_normal(n), 400) * 0.25
        drops = np.zeros(n); idx = rng.integers(0, n, int(n / SR * 90)); drops[idx] = rng.uniform(0.2, 1, len(idx))
        drops = bp(drops, 2000, 6000) * 3
        amb.add((nz + drops) * e * 0.08 * g, t0, pan=pan)
def room(t0, t1, g=1.0):   # candle room tone + flame flutter
    n = int((t1 - t0) * SR); tt = np.arange(n) / SR
    y = lp(rng.standard_normal(n), 180) * 0.25 + bp(rng.standard_normal(n), 300, 900) * 0.05 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * tt))
    amb.add(y * np.clip(tt / 0.4, 0, 1) * np.clip((t1 - t0 - tt) / 0.4, 0, 1) * 0.1 * g, t0)
rain_bed(6.9, 17.95, 1.0); rain_bed(54.0, 58.8, 1.3, 0.8); rain_bed(66.7, 69.9, 0.6, 1.2)
for a, b in [(0, 3.0), (17.9, 54.0), (58.8, 66.7), (69.9, 90.0), (97.7, DUR)]: room(a, b, 1.0)

# ---------- sfx ----------
sfx = Bus()
def noise(dur): return rng.standard_normal(int(dur * SR))
def match():  # kibrit cakma: surtunme + tutusma
    n = int(0.9 * SR); tt = np.arange(n) / SR
    scr = bp(rng.standard_normal(n), 1800, 7000) * np.exp(-((tt - 0.06) / 0.05) ** 2)
    crack = hp(rng.standard_normal(n), 3000) * (rng.random(n) < 0.004) * 4 * np.exp(-tt * 6)
    ign = bp(rng.standard_normal(n), 200, 1500) * np.clip((tt - 0.1) / 0.05, 0, 1) * np.exp(-(tt - 0.1).clip(0) * 3)
    return scr * 0.8 + crack + ign * 0.9
def knock():
    n = int(0.5 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 110 * tt) * np.exp(-tt * 30) + bp(rng.standard_normal(n), 300, 1800) * np.exp(-tt * 60) * 0.6) * 0.9
def whoosh(dur, f0, f1, peak=0.6):
    n = int(dur * SR); tt = np.arange(n) / SR; k = tt / dur; y = rng.standard_normal(n); out = np.zeros(n)
    bands = [(200, 700), (600, 2000), (1600, 5000), (4000, 11000)]
    for i, (lo, hi) in enumerate(bands):
        c = i / 3 if f1 > f0 else 1 - i / 3
        out += bp(y, lo, hi) * np.exp(-((k - (0.25 + 0.6 * c)) / 0.25) ** 2)
    return out * np.exp(-((k - peak) / 0.35) ** 2) * 0.6
def thud():
    n = int(1.2 * SR); tt = np.arange(n) / SR
    sub = np.sin(2 * np.pi * (70 * np.exp(-tt * 6) + 38) * tt) * np.exp(-tt * 5)
    return sub * 1.2 + lp(rng.standard_normal(n), 1200) * np.exp(-tt * 25) * 0.7
def gravel():
    n = int(0.9 * SR); tt = np.arange(n) / SR; y = np.zeros(n); idx = rng.integers(0, int(0.6 * SR), 60); y[idx] = rng.uniform(0.2, 1, 60)
    return bp(y, 2500, 8000) * 2.5 * np.exp(-tt * 3)
def quill(dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    strokes = (np.sin(2 * np.pi * 3.1 * tt) > 0.1) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * tt))
    return bp(rng.standard_normal(n), 3000, 9000) * lp(strokes.astype(float), 30) * 0.35
def blow():
    n = int(1.4 * SR); tt = np.arange(n) / SR
    breath = bp(rng.standard_normal(n), 300, 2500) * np.exp(-((tt - 0.12) / 0.12) ** 2)
    flut = bp(rng.standard_normal(n), 80, 400) * np.exp(-tt * 5) * (1 + np.sin(2 * np.pi * 14 * tt))
    return breath * 0.9 + flut * 0.5
def thunder():
    n = int(4 * SR); tt = np.arange(n) / SR
    return lp(rng.standard_normal(n), 160, 3) * np.clip(tt / 0.3, 0, 1) * np.exp(-tt * 0.9) * 2.5
def shimmer(dur):
    n = int(dur * SR); tt = np.arange(n) / SR; y = np.zeros(n)
    for f in [hz(84), hz(91), hz(96), hz(100)]: y += np.sin(2 * np.pi * f * tt * (1 + 0.002 * np.sin(2 * np.pi * 6 * tt)))
    return y * (tt / dur) ** 2 * 0.05
sfx.add(match(), 0.0, pan=0.1, g=0.9)
for k in (13.35, 13.62, 13.9): sfx.add(knock(), k, pan=0.35, g=0.8)
sfx.add(whoosh(1.6, 300, 2400, 0.5), wt(42) - 0.4, pan=-0.2, g=0.8)
sfx.add(whoosh(1.0, 2200, 300, 0.85), wt(74) - 0.9, g=0.8); sfx.add(thud(), wt(74), g=1.0); sfx.add(gravel(), wt(74) + 0.03, pan=0.15, g=0.7)
sfx.add(quill(1.8), wt(79) - 0.1, pan=0.3, g=0.7); sfx.add(quill(2.2), wt(167), pan=0.3, g=0.7)
sfx.add(thunder(), 54.2, pan=-0.3, g=0.8)
sfx.add(blow(), wt(165) - 0.12, g=1.0)
sfx.add(shimmer(wt(178) - 93.7), 93.7, g=1.0)
# imza: her mercek supurmesinde cam tinisi + hafif hava
for tl in (6.92, 17.9, 32.6, 48.3, 72.5, 88.3, 97.7):
    sfx.add(glass(86 if tl < 60 else 89, 3.0, 0.9), tl - 0.05, pan=0.3)
    sfx.add(whoosh(0.8, 600, 5000, 0.55), tl - 0.45, pan=-0.3, g=0.35)
sfx.add(shimmer(1.2), 48.3, g=1.0)
reverb(sfx, 2.6, 0.35, 2.2, 7000)

def write(name, bus, peak=0.5):
    x = bus.st(); x *= peak / (np.max(np.abs(x)) + 1e-9)
    wavfile.write(os.path.join(outdir, name), SR, x.astype(np.float32))
write('music.wav', mus, 0.5); write('amb.wav', amb, 0.25); write('sfx.wav', sfx, 0.5)
print('wrote music/amb/sfx', DUR)

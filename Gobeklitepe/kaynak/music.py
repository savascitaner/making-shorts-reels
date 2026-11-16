# Gobeklitepe: sub drone + choir pad + bone flute + frame drum, ambience and SFX, all generated in code
# (no samples, no licence issues). Usage:
#   uv run --with numpy --with scipy python music.py audio DURATION b1,b2,... whip1,... trans1,... boom1,...
# b = section boundaries (s); argv[4] (whip) is accepted but unused; argv[5] = transition times (sand whoosh);
# argv[6] = boom times (stone strike). Fixed seed -> identical output on every run.
import sys, os, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt, sosfiltfilt
from scipy.io import wavfile

SR = 48000
outdir, DUR = sys.argv[1], float(sys.argv[2])
os.makedirs(outdir, exist_ok=True)
B = [0.0] + [float(x) for x in sys.argv[3].split(",") if x] + [DUR]
TRANS = [float(x) for x in sys.argv[5].split(",") if x] if len(sys.argv) > 5 else []
BOOMS = [float(x) for x in sys.argv[6].split(",") if x] if len(sys.argv) > 6 else []
rng = np.random.default_rng(11500)
N = int(SR * DUR)
t = np.arange(N) / SR
NB = len(B) - 1
CLOSE = max(0.0, DUR - 5.0)                       # closing: wind + one long note

def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def win(t0, t1, ramp=1.0): return np.clip((t - t0) / ramp, 0, 1) * np.clip((t1 - t) / ramp, 0, 1)
def smooth_noise(f, n=N):                         # slow random curve in 0..1
    x = sosfiltfilt(butter(1, f, fs=SR, output="sos"), rng.standard_normal(n))
    x = x / (np.abs(x).max() + 1e-9)
    return 0.5 + 0.5 * x

def ctl(vals, sm=1.5):
    """per-section values (index clamped to the last entry) -> smooth control curve over time"""
    c = np.zeros(N)
    for i in range(NB):
        c[int(B[i] * SR):int(B[i + 1] * SR)] = vals[min(i, len(vals) - 1)]
    return sosfiltfilt(butter(1, 1.0 / (2 * np.pi * sm) , fs=SR, output="sos"), c)

class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, sig, t0, pan=0.0, g=1.0):
        i = int(t0 * SR)
        if i >= N or i + len(sig) <= 0: return
        if i < 0: sig = sig[-i:]; i = 0
        sig = sig[: N - i] * g
        s.L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan)); s.R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))
    def addst(s, l, r, t0=0.0, g=1.0):
        i = int(t0 * SR); n = min(len(l), N - i)
        if n > 0: s.L[i:i + n] += l[:n] * g; s.R[i:i + n] += r[:n] * g
    def reverb(s, sec=3.0, wet=0.3, decay=1.8, lpf=5000, dry=1.0):
        n = int(sec * SR); it = np.arange(n) / SR; out = []
        for ch in (s.L, s.R):
            ir = lp(rng.standard_normal(n) * np.exp(-it * decay), lpf); ir[:int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
            ir /= np.sqrt((ir ** 2).sum())
            out.append(ch * dry + fftconvolve(ch, ir)[:N] * wet * 1.6)
        s.L, s.R = out
    def mul(s, e): s.L = s.L * e; s.R = s.R * e
    def plus(s, o, g=1.0): s.L = s.L + o.L * g; s.R = s.R + o.R * g

def saw_voice(f, vib=0.0035, drift=0.0):
    v = 1 + vib * np.sin(2 * np.pi * rng.uniform(4.2, 5.4) * t + rng.uniform(0, 6)) * np.clip(t / 3, 0, 1)
    v = v * (1 + drift * smooth_noise(0.2))
    ph = np.cumsum(f * v) / SR + rng.uniform(0, 1)
    return 2 * (ph % 1) - 1

# ====================== MUSIC ======================
# section profiles (index 0..11): drone, choir main, choir tense (b2/minor colour), choir open (major 3rd, stars),
# drum level, flute rate (notes/s), flute gain
DRONE = [1.0, 1.0, 0.75, 0.85, 0.95, 1.0, 0.6, 0.6, 0.75, 0.75, 0.7, 0.35]
CH_A  = [0.15, 0.2, 0.30, 0.45, 0.75, 1.0, 0.25, 0.25, 0.7, 0.9, 0.8, 0.25]
CH_T  = [0.8, 0.9, 0.0, 0.1, 0.2, 0.3, 0.55, 0.5, 0.0, 0.0, 0.0, 0.0]
CH_O  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 1.0, 0.9, 0.35]
DRUM  = [0.0, 0.0, 0.0, 0.30, 0.65, 1.0, 0.0, 0.0, 0.35, 0.45, 0.3, 0.0]
FRATE = [0.05, 0.07, 0.13, 0.05, 0.06, 0.05, 0.09, 0.09, 0.15, 0.18, 0.14, 0.05]
FGAIN = [0.6, 0.6, 0.8, 0.5, 0.5, 0.5, 0.8, 0.8, 1.0, 1.0, 0.9, 0.6]
RF = 55.0                                         # A1 root

mus = Bus()
# sub drone: 55 Hz + slow detuned partner beating at ~0.1 Hz, plus 2nd/3rd harmonics, gentle drift
d_env = ctl(DRONE, 2.0)
dr = np.zeros(N)
for f, a in [(RF, 1.0), (RF * 1.0018, 0.8), (RF * 2, 0.35), (RF * 3.005, 0.12), (RF * 1.5, 0.18)]:
    dr += a * np.sin(2 * np.pi * np.cumsum(f * (1 + 0.004 * smooth_noise(0.15))) / SR)
dr = lp(dr, 400) * d_env * (0.85 + 0.15 * np.sin(2 * np.pi * t / 9.0))
mus.L += dr * 0.9; mus.R += dr * 0.9

# choir pad: formant-filtered detuned saws (vowel "o/a"), three chord layers with own gain curves
def choir(notes, detunes=(-0.12, 0.0, 0.1), chan_seed=0):
    outL = np.zeros(N); outR = np.zeros(N)
    for ch in (0, 1):
        s = np.zeros(N)
        for m in notes:
            for d in detunes:
                s += saw_voice(hz(m) * 2 ** ((d + rng.uniform(-0.04, 0.04)) / 12), vib=0.004, drift=0.003)
        y = bp(s, 300, 600, 2) * 1.0 + bp(s, 650, 950, 2) * 0.8 + bp(s, 2200, 2800, 2) * 0.12 + lp(s, 200, 1) * 0.15
        (outL if ch == 0 else outR)[:] = y
    return outL / (len(notes) * len(detunes)) ** 0.5, outR / (len(notes) * len(detunes)) ** 0.5
# A hicaz-ish colours: main = open fifth stack A2 E3 A3; tense = Bb2 F3 (b2 against the drone) + A3; open = C#3 E3 A3 E4
for notes, curve, gain in [([45, 52, 57], CH_A, 0.06), ([46, 53, 57], CH_T, 0.05), ([49, 52, 57, 64], CH_O, 0.05)]:
    e = ctl(curve, 2.2)
    if e.max() <= 1e-3: continue
    l, r = choir(notes)
    mus.L += l * e * gain; mus.R += r * e * gain

# bone flute / ney: sparse, breathy, vibrato, slow attack; hicaz on A (A Bb C# D E F G A)
HICAZ = [69, 70, 73, 74, 76, 77, 79, 81]
def flute(m, dur, vel=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; f0 = hz(m)
    glide = 2 ** (-0.7 * np.exp(-tt / 0.1) / 12)
    vib = 1 + 0.007 * np.sin(2 * np.pi * (4.9 + 0.3 * rng.standard_normal()) * tt) * np.clip((tt - 0.5) / 1.2, 0, 1)
    ph = 2 * np.pi * np.cumsum(f0 * glide * vib) / SR
    y = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.32 * np.sin(3 * ph) + 0.07 * np.sin(5 * ph)
    breath = bp(rng.standard_normal(n), min(f0 * 2, 3000), min(f0 * 7, 9000)) * (0.25 + 0.4 * np.exp(-tt / 0.3))
    env = np.clip(tt / 0.35, 0, 1) ** 1.5 * np.clip((dur - tt) / 0.9, 0, 1) ** 1.2 * (1 + 0.15 * np.sin(2 * np.pi * tt / 1.7))
    return lp(y * 0.5 + breath * 0.6, 4500) * env * 0.35 * vel
fl = Bus()
fr = ctl(FRATE, 1.0); fg = ctl(FGAIN, 1.0)
tcur = 1.5; idx = 0
while tcur < CLOSE - 3.0:
    rate = max(fr[min(int(tcur * SR), N - 1)], 0.02)
    k = rng.integers(1, 4)                       # short phrase of 1-3 notes
    for _ in range(k):
        idx = int(np.clip(idx + rng.choice([-2, -1, -1, 1, 1, 2]), 0, len(HICAZ) - 1))
        m = HICAZ[idx] + (12 if (idx >= 5 and fg[min(int(tcur * SR), N - 1)] > 0.95 and rng.random() < 0.4) else 0)
        d = rng.uniform(2.0, 4.2)
        fl.add(flute(m, d), tcur, pan=rng.uniform(-0.3, 0.3), g=fg[min(int(tcur * SR), N - 1)])
        tcur += d * 0.75
        if tcur >= CLOSE - 3.0: break
    if idx > 0 and rng.random() < 0.6:           # resolve towards the tonic
        fl.add(flute(HICAZ[0], rng.uniform(3.0, 4.5)), tcur, pan=0.0, g=fg[min(int(tcur * SR), N - 1)]); idx = 0
        tcur += 3.0
    tcur += rng.exponential(1.0 / rate)
fl.reverb(3.8, 0.7, 1.2, 3500, dry=0.55)         # distant
mus.plus(fl, 0.75)

# frame drum (def) heartbeat: lub-dub, tempo rises through the build
def def_hit(f, vel):
    n = int(0.6 * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(f * (0.62 + 0.38 * np.exp(-tt * 18))) / SR) * np.exp(-tt * 9)
    skin = bp(rng.standard_normal(n), 120, 1100) * np.exp(-tt * 28) * 0.7
    rim = hp(rng.standard_normal(n), 3000) * np.exp(-tt * 90) * 0.08
    return lp(body * 1.1 + skin + rim, 2500) * vel
dr_bus = Bus()
for si in range(NB):
    lv = DRUM[min(si, len(DRUM) - 1)]
    if lv <= 0: continue
    t0, t1 = B[si], B[si + 1]
    period = np.interp(lv, [0.3, 1.0], [1.15, 0.82])
    tt_ = t0 + 0.3
    while tt_ < t1 - 0.3:
        v = lv * rng.uniform(0.9, 1.05)
        dr_bus.add(def_hit(95, v), tt_ + rng.uniform(-0.008, 0.008), pan=-0.1)
        dr_bus.add(def_hit(78, v * 0.55), tt_ + 0.32 * period + rng.uniform(-0.01, 0.01), pan=0.1)
        tt_ += period
dr_bus.reverb(2.2, 0.35, 2.4, 3500)
mus.plus(dr_bus, 0.55)

# closing: drone/choir release, then one long note
rel = np.clip((CLOSE + 0.8 - t) / 1.5, 0, 1)      # (all layers above are scaled by this after the long note is added)
mus.mul(np.where(t < CLOSE, 1.0, rel))
if CLOSE > 0:
    ln = Bus(); n = int(5.0 * SR); tn = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(hz(57) * (1 + 0.004 * np.sin(2 * np.pi * 4.6 * tn) * np.clip(tn / 1.5, 0, 1))) / SR
    note = (np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph) + 0.4 * lp(rng.standard_normal(n), 2000) * 0.15)
    note *= np.clip(tn / 0.8, 0, 1) ** 1.5 * np.clip((5.0 - tn) / 3.2, 0, 1) ** 1.3 * 0.4
    sub = np.sin(2 * np.pi * RF * tn) * np.clip(tn / 0.8, 0, 1) * np.clip((5.0 - tn) / 3.0, 0, 1) * 0.5
    ln.add(note + sub, CLOSE, pan=0.0)
    ln.reverb(3.0, 0.45, 1.6, 4000)
    mus.plus(ln, 0.9)
mus.reverb(4.0, 0.28, 1.4, 4500)
fade = np.clip(t / 1.5, 0, 1) * np.clip((DUR - t) / 1.5, 0, 1)
mus.mul(fade)

# ====================== AMBIENCE ======================
amb = Bus()
# wind overhead: two bands, slow gusts, decorrelated channels; stronger at start and in the closing
wind_lvl = 0.55 + 0.45 * win(0, 4, 1.5)[::-1] * 0 + 0.0
wl = np.full(N, 0.55) + 0.35 * np.clip((4.0 - t) / 2.0, 0, 1) + 0.9 * np.clip((t - (CLOSE - 1.0)) / 3.0, 0, 1)
for lo, hi, g in [(150, 600, 1.0), (700, 1800, 0.3)]:
    for ch in (0, 1):
        nz = bp(rng.standard_normal(N), lo, hi)
        gust = (0.35 + 0.65 * smooth_noise(0.12)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / rng.uniform(6, 11) + rng.uniform(0, 6)))
        (amb.L if ch == 0 else amb.R)[:] += nz * gust * g * wl * 0.09
for ch in (0, 1):                                  # faint thin whistle
    w = bp(rng.standard_normal(N), 880, 1000, 2) * smooth_noise(0.1) ** 2 * wl * 0.12
    (amb.L if ch == 0 else amb.R)[:] += w

def crackle(t0, t1, rate, gain, hpf=1500, big=0.08):
    out = np.zeros(N)
    for _ in range(int(rate * (t1 - t0))):
        ln_ = int(rng.uniform(0.003, 0.03) * SR); ti = int(rng.uniform(t0, t1) * SR)
        if ti + ln_ >= N: continue
        a = np.exp(rng.normal(-1.0, 0.9)); a *= 3 if rng.random() < big else 1
        pop = rng.standard_normal(ln_) * np.exp(-np.arange(ln_) / (ln_ / rng.uniform(3, 6)))
        out[ti:ti + ln_] += pop * a
    return hp(out, hpf, 1) * gain

# first 4 s: burning book = crackle + flame roar
e4 = min(4.0, DUR)
fireL = crackle(0, e4, 45, 0.22) ; fireR = crackle(0, e4, 45, 0.22)
env_fire = np.clip(1 - (t - (e4 - 1.2)) / 1.4, 0, 1) * np.clip(t / 0.15, 0, 1)
for ch, fc in ((0, fireL), (1, fireR)):
    roar = lp(rng.standard_normal(N), 350) * (0.5 + 0.5 * smooth_noise(2.0)) + 0.4 * bp(rng.standard_normal(N), 400, 1500) * smooth_noise(5.0) ** 2
    (amb.L if ch == 0 else amb.R)[:] += (fc + roar * 0.35) * env_fire

# section 6 (~58-72 s): torches + distant crowd murmur
s6a, s6b = (B[5], B[6]) if NB > 5 else (0, 0)
if s6b > s6a:
    w6 = win(s6a, s6b, 2.0)
    for ch in (0, 1):
        tc = crackle(s6a, s6b, 9, 0.12, hpf=900, big=0.12) + lp(rng.standard_normal(N), 250) * smooth_noise(1.5) * 0.04 * w6
        cr = bp(rng.standard_normal(N), 220, 2400)
        syl = lp(np.abs(lp(rng.standard_normal(N), 6, 1)), 5, 1); syl = syl / (syl.max() + 1e-9)
        syl2 = lp(np.abs(lp(rng.standard_normal(N), 3, 1)), 3, 1); syl2 = syl2 / (syl2.max() + 1e-9)
        crowd = lp(cr * (0.25 + 0.75 * syl) * (0.3 + 0.7 * syl2), 1600) * 0.5
        (amb.L if ch == 0 else amb.R)[:] += tc * w6 + crowd * w6 * 0.5

# sections 9-11: very quiet night insects
if NB > 10:
    c0, c1 = B[8], B[min(11, NB)]
    for k in range(6):
        f = rng.uniform(3600, 5400); cr_ = rng.uniform(1.4, 2.6); pr = rng.uniform(26, 36); ph0 = rng.uniform(0, 6)
        i0, i1 = int(c0 * SR), int(c1 * SR); ts = t[i0:i1]
        chirp = np.clip(np.sin(2 * np.pi * cr_ * ts + ph0) * 3, 0, 1)
        pulse = np.clip(np.sin(2 * np.pi * pr * ts), 0, 1) ** 2
        slow = 0.4 + 0.6 * smooth_noise(0.3, len(ts))
        sig = np.sin(2 * np.pi * f * ts) * pulse * chirp * slow * np.clip((ts - c0) / 3, 0, 1) * np.clip((c1 - ts) / 3, 0, 1)
        pan = rng.uniform(-0.9, 0.9)
        amb.L[i0:i1] += sig * 0.018 * np.sqrt(0.5 * (1 - pan)); amb.R[i0:i1] += sig * 0.018 * np.sqrt(0.5 * (1 + pan))
amb.reverb(2.0, 0.12, 2.5, 4000)
amb.mul(np.clip(t / 0.05, 0, 1) * np.clip((DUR - t) / 1.0, 0, 1))
# soft-limit crackle spikes (mixdown scales ambience by RMS, so peaks must stay close to the RMS)
_r = np.sqrt(np.mean(np.concatenate([amb.L, amb.R]) ** 2)); amb.L = np.tanh(amb.L / (3 * _r)) * 3 * _r; amb.R = np.tanh(amb.R / (3 * _r)) * 3 * _r

# ====================== SFX ======================
sfx = Bus()
def boom():
    n = int(3.2 * SR); tt = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(26 + 70 * np.exp(-tt * 3.2)) / SR) * np.exp(-tt * 1.6) * np.clip(tt / 0.004, 0, 1)
    thump = lp(rng.standard_normal(n), 450) * np.exp(-tt * 22)
    crack = hp(rng.standard_normal(n), 1500) * np.exp(-tt * 70) * 0.25
    modes = sum(a * np.sin(2 * np.pi * f * tt + rng.uniform(0, 6)) * np.exp(-tt * dk)
                for f, a, dk in [(118, 0.45, 7), (203, 0.3, 9), (341, 0.22, 12), (587, 0.12, 16)])
    return sub * 1.3 + thump * 1.0 + crack + modes * 0.6
for bt in BOOMS: sfx.add(boom(), bt - 0.01, pan=0.0, g=1.0)

def whoosh(dur=0.55):
    n = int(dur * SR); tt = np.arange(n) / SR; k = tt / dur
    nz = rng.standard_normal(n)
    wind = bp(nz, 250, 1100) * np.exp(-((k - 0.5) / 0.25) ** 2)
    sand = hp(lp(rng.standard_normal(n), 6500), 2500) * np.exp(-((k - 0.42) / 0.2) ** 2) * (0.6 + 0.4 * rng.random(n)) * 0.5
    return lp(wind * 0.6 + sand, 7000) * np.sin(np.pi * k) ** 1.3 * 0.7
for tr in TRANS: sfx.add(whoosh(), tr - 0.3, pan=rng.uniform(-0.3, 0.3), g=0.6)

# rope strain / stone scraping between sections 5 and 6 (43-58 s in the trial values)
def rope(dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = 62 + 22 * np.sin(2 * np.pi * tt / dur * 1.3 + rng.uniform(0, 6)) + 18 * tt / dur
    ph = np.cumsum(f * (1 + 0.04 * lp(rng.standard_normal(n), 14, 1))) / SR
    saw = 2 * (ph % 1) - 1
    y = bp(saw, 450, 1400) * 0.9 + bp(saw, 1800, 2600) * 0.25
    return y * np.sin(np.pi * tt / dur) ** 1.5 * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * tt)) * 0.55
def scrape(dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    am = np.clip(0.5 + 0.9 * lp(rng.standard_normal(n), 18, 1) * 12, 0, 1.5)
    y = bp(rng.standard_normal(n), 220, 1400) * am + 0.3 * hp(rng.standard_normal(n), 3000) * am ** 2 * 0.3
    return y * np.sin(np.pi * tt / dur) ** 1.2 * 0.5
if NB > 5:
    a, b_ = B[4], B[5]
    for j in range(6):
        ts = a + (b_ - a) * (0.05 + 0.85 * j / 6) + rng.uniform(-0.6, 0.6)
        if j % 2 == 0: sfx.add(rope(rng.uniform(1.4, 2.4)), ts, pan=rng.uniform(-0.6, 0.6), g=0.4)
        else: sfx.add(scrape(rng.uniform(0.9, 1.6)), ts, pan=rng.uniform(-0.6, 0.6), g=0.5)
sfx.reverb(2.4, 0.3, 2.3, 4500)

# ====================== WRITE ======================
def write(name, bus, peak=0.85):
    x = bus.st() if hasattr(bus, "st") else bus
    m = np.max(np.abs(x)); x = x * (peak / m) if m > 1e-9 else x
    wavfile.write(os.path.join(outdir, name), SR, x.astype(np.float32))
    return x
Bus.st = lambda s: np.stack([s.L, s.R], 1)
for nm, bus in [("music.wav", mus), ("amb.wav", amb), ("sfx.wav", sfx)]:
    x = write(nm, bus)
    print(f"{nm}: {len(x) / SR:.2f}s peak {np.abs(x).max():.3f} rms {np.sqrt(np.mean(x ** 2)):.4f}")

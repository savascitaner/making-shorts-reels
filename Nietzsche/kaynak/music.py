# Dark piano + strings score and SFX, generated entirely in code (no samples -> no licence issues). Usage:
#   uv run --with numpy --with scipy python music.py audio DURATION b1,b2,... whip1,whip2,... trans1,trans2,...
# b = section boundaries (s); whip = distant whip-crack times; trans = 3D transition times (whoosh)
import sys, os, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

SR = 48000
outdir, DUR = sys.argv[1], float(sys.argv[2])
B = [0.0] + [float(x) for x in sys.argv[3].split(",") if x] + [DUR]
WHIPS = [float(x) for x in sys.argv[4].split(",") if x] if len(sys.argv) > 4 else []
TRANS = [float(x) for x in sys.argv[5].split(",") if x] if len(sys.argv) > 5 else []
rng = np.random.default_rng(1844)
N = int(SR * DUR)
t = np.arange(N) / SR

def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)          # midi -> Hz

class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, sig, t0, pan=0.0, g=1.0):
        i = int(t0 * SR)
        if i >= N or i + len(sig) <= 0: return
        if i < 0: sig = sig[-i:]; i = 0
        sig = sig[: N - i] * g
        s.L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan)); s.R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))
    def st(s): return np.stack([s.L, s.R], 1)

def reverb(bus, sec=3.2, wet=0.25, decay=1.8, lpf=6000):
    n = int(sec * SR); it = np.arange(n) / SR
    out = []
    for ch in (bus.L, bus.R):
        ir = lp(rng.standard_normal(n) * np.exp(-it * decay), lpf); ir /= np.sqrt((ir ** 2).sum())
        out.append(ch * (1 - wet) + fftconvolve(ch, ir)[:N] * wet * 1.6)
    bus.L, bus.R = out

# ---------- piano (additive, inharmonic partials, hammer noise) ----------
def piano(m, dur=4.0, vel=0.7):
    f = hz(m); n = int(dur * SR); tt = np.arange(n) / SR
    y = np.zeros(n); B_ = 0.0004
    for k in range(1, 9):
        fk = f * k * np.sqrt(1 + B_ * k * k)
        if fk > 12000: break
        dec = 0.6 + 2.2 * k * (f / 440) ** 0.4
        y += (vel ** (1 + k * 0.15)) / k ** 1.1 * np.sin(2 * np.pi * fk * tt + rng.uniform(0, 6)) * np.exp(-tt * dec)
    y += 0.5 * np.sin(2 * np.pi * f * 1.0015 * tt) * np.exp(-tt * 0.5) * vel     # slow beating string pair
    hammer = bp(rng.standard_normal(n), f, min(f * 8, 9000)) * np.exp(-tt * 60) * 0.25 * vel
    y = (y + hammer) * np.clip(tt / 0.004, 0, 1) * np.clip((dur - tt) / 0.4, 0, 1)
    return lp(y, 5000) * 0.3

# ---------- strings (detuned saw ensemble, slow attack) ----------
def strings(ms, dur, att=2.0, rel=2.5, bright=1800):
    n = int(dur * SR); tt = np.arange(n) / SR; y = np.zeros(n)
    for m in ms:
        for d in (-0.09, -0.03, 0.04, 0.1):
            f = hz(m) * 2 ** (d / 12)
            vib = 1 + 0.003 * np.sin(2 * np.pi * (4.8 + rng.uniform(-0.4, 0.4)) * tt + rng.uniform(0, 6))
            ph = 2 * np.pi * np.cumsum(f * vib) / SR + rng.uniform(0, 6)
            y += 2 * ((ph / (2 * np.pi)) % 1) - 1
    y = lp(y, bright, 3)
    e = np.clip(tt / att, 0, 1) ** 1.6 * np.clip((dur - tt) / rel, 0, 1) ** 1.3
    return y * e * 0.05 / max(1, len(ms)) ** 0.5

# D minor material
Dm, Bb, F, C, Gm, A, Am = [50, 57, 62, 65], [46, 53, 58, 62], [41, 53, 57, 60], [48, 55, 60, 64], [43, 55, 58, 62], [45, 52, 57, 61], [45, 52, 57, 60]
PROG = [Dm, Bb, F, C, Gm, Dm, A, A]
mus = Bus()

def section(t0, t1, density, str_gain, piano_gain, prog=PROG, bar=4.0, high=False):
    t_ = t0; k = 0
    while t_ < t1 - 0.5:
        ch = prog[k % len(prog)]; d = min(bar, t1 - t_)
        if str_gain > 0: mus.add(strings([ch[0] - 12, ch[1], ch[2]] + ([ch[3] + 12] if high else []), d + 2.5, att=1.6, rel=2.4), t_, g=str_gain)
        if piano_gain > 0:
            notes = [ch[0], ch[2] + 12, ch[3] + 12, ch[1] + 12] if density > 1 else [ch[0], ch[3] + 12]
            step = bar / len(notes) if density > 1 else bar / 2
            for j, m in enumerate(notes):
                if rng.random() < 0.92: mus.add(piano(m, 4.5, 0.55 + 0.2 * rng.random()), t_ + j * step + rng.uniform(0, 0.02), pan=rng.uniform(-0.35, 0.35), g=piano_gain)
            if density > 2 and rng.random() < 0.6:   # top melody note
                mus.add(piano(ch[3] + 24 + rng.choice([0, 2, -2, 3]), 4.0, 0.5), t_ + bar * 0.62, pan=0.2, g=piano_gain * 0.7)
        t_ += bar; k += 1

b = B
nb = len(b) - 1
for si in range(nb):
    t0, t1 = b[si], b[si + 1]
    if si == 0:                       # hook: low drone + single piano tolls
        mus.add(strings([38, 45], t1 - t0 + 2, att=2.5, rel=2.5, bright=900), t0, g=1.2)
        for tt0 in np.arange(t0 + 0.4, t1 - 0.5, 2.6): mus.add(piano(62 if int(tt0) % 2 else 57, 4, 0.5), tt0, g=0.7)
    elif si == nb - 1:                # finale: full strings, sparse piano, swell then fade
        section(t0, t1, 1, 1.1, 0.8, prog=[Dm, Bb, Gm, A], high=True)
    elif si in (1, 2):                # biography: piano arpeggio, light strings
        section(t0, t1, 2, 0.45, 0.85)
    elif si == 3:                     # God is dead: low strings, sparse
        section(t0, t1, 1, 0.9, 0.6, prog=[Dm, Gm, Bb, A], bar=5.0)
    else:                             # recurrence / amor fati: fuller
        section(t0, t1, 3, 0.8, 0.85, prog=[Dm, Bb, F, C, Gm, Bb, A, A], high=True)
reverb(mus, 3.6, 0.32, 1.5)
# fade in/out
fade = np.clip(t / 2.0, 0, 1) * np.clip((DUR - t) / 3.5, 0, 1)
mus.L *= fade; mus.R *= fade

# ---------- SFX ----------
amb = Bus()
# winter wind: two layers of filtered noise with slow gusts, strongest in hook and finale
for lo, hi, g in [(180, 700, 1.0), (900, 2600, 0.35)]:
    for ch in (0, 1):
        nz = bp(rng.standard_normal(N), lo, hi)
        gust = 0.55 + 0.45 * np.sin(2 * np.pi * t / (7.3 + ch) + rng.uniform(0, 6)) * np.sin(2 * np.pi * t / 3.1 + rng.uniform(0, 6))
        (amb.L if ch == 0 else amb.R)[:] += nz * gust * g * 0.06
env = np.full(N, 0.18)
for a0, a1 in [(b[0], b[1]), (b[-2], b[-1])]:
    env[int(a0 * SR):int(a1 * SR)] = 1.0
env = lp(env, 0.5, 1)
amb.L *= env * fade; amb.R *= env * fade
# snow hiss (very soft, high)
hiss = hp(rng.standard_normal(N), 6000) * 0.006
amb.L += hiss * env; amb.R += hiss * env
sfx = Bus()
def whip():
    n = int(0.35 * SR); tt = np.arange(n) / SR
    crack = hp(rng.standard_normal(n), 1500) * np.exp(-tt * 120)
    swish = bp(rng.standard_normal(n), 600, 3000) * np.exp(-((tt - 0.06) / 0.04) ** 2) * 0.4
    return lp(crack + swish, 6000) * 0.9
for w in WHIPS: sfx.add(whip(), w - 0.08, pan=-0.45, g=0.7)
def whoosh(dur=1.6, rise=True):
    n = int(dur * SR); tt = np.arange(n) / SR; k = tt / dur
    nz = rng.standard_normal(n); y = np.zeros(n)
    for i, (lo, hi) in enumerate([(200, 800), (600, 2000), (1500, 5000)]):
        y += bp(nz, lo, hi) * np.exp(-((k - (0.55 + 0.1 * i)) / 0.22) ** 2)
    sub = np.sin(2 * np.pi * (40 + 30 * k) * tt) * np.exp(-((k - 0.7) / 0.2) ** 2) * 0.6
    return (y * 0.35 + sub) * 0.8
for tr in TRANS: sfx.add(whoosh(), tr - 0.9, pan=0, g=0.9)
reverb(sfx, 2.5, 0.4, 2.5, 5000)

def write(name, bus, peak=0.5):
    x = bus.st(); x *= peak / (np.max(np.abs(x)) + 1e-9)
    wavfile.write(os.path.join(outdir, name), SR, x.astype(np.float32))
write("music.wav", mus, 0.5); write("amb.wav", amb, 0.25); write("sfx.wav", sfx, 0.5)
print("wrote music/amb/sfx", DUR)

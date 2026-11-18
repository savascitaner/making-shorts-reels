# Jung-Freud: score, ambience and sfx written in code (no samples, no licence issues).
# Signature: a glass-harmonica motif and its MIRROR (melodic inversion), over a warm low cello drone.
# Usage: uv run --with numpy --with scipy python muzik_jf.py   -> audio/music.wav, audio/amb.wav, audio/sfx.wav
import json, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

SR = 48000
V = json.load(open('../video.json')); DUR = V['sure']; N = int(SR * DUR)
WD = json.load(open('words.json'))['words']; wt = lambda i: WD[i]['s']; we = lambda i: WD[i]['e']
SHOT_WORDS = [0, 7, 12, 22, 33, 43, 61, 75, 85, 96, 106, 119]
SHOTS = [0.0] + [wt(i) - 0.15 for i in SHOT_WORDS[1:]]
COVER0 = max(we(132) + 0.9, 79.9)
rng = np.random.default_rng(1913)

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
        sig = sig[: N - i] * g
        s.L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan)); s.R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))
    def st(s): return np.stack([s.L, s.R], 1)

def reverb(bus, sec=3.5, wet=0.3, decay=1.5, lpf=7000):
    n = int(sec * SR); it = np.arange(n) / SR; out = []
    for ch in (bus.L, bus.R):
        ir = lp(rng.standard_normal(n) * np.exp(-it * decay), lpf); ir /= np.sqrt((ir ** 2).sum())
        out.append(ch * (1 - wet) + fftconvolve(ch, ir)[:N] * wet * 1.5)
    bus.L, bus.R = out

# ---------- voices ----------
def glass(m, dur=3.0, vel=0.6):   # glass harmonica: pure partials, slow bloom, shimmer
    f = hz(m); n = int(dur * SR); tt = np.arange(n) / SR
    vib = 1 + 0.0025 * np.sin(2 * np.pi * 5.2 * tt)
    y = np.sin(2 * np.pi * f * tt * vib) + 0.35 * np.sin(2 * np.pi * 2 * f * tt * vib + 1) + 0.12 * np.sin(2 * np.pi * 3.01 * f * tt)
    env = np.clip(tt / 0.12, 0, 1) * np.exp(-tt * 1.1) * np.clip((dur - tt) / 0.5, 0, 1)
    return y * env * vel * 0.22

def cello(ms, dur, att=2.5, rel=3.0, bright=900):   # warm low bowed drone
    n = int(dur * SR); tt = np.arange(n) / SR; y = np.zeros(n)
    for m in ms:
        for d in (-0.06, 0.0, 0.07):
            f = hz(m) * 2 ** (d / 12); ph = rng.uniform(0, 1)
            y += 2 * ((tt * f + ph) % 1) - 1
    y = lp(y, bright, 3) * (1 + 0.15 * np.sin(2 * np.pi * 0.18 * tt))
    env = np.clip(tt / att, 0, 1) * np.clip((dur - tt) / rel, 0, 1)
    return y * env * 0.05

def heartbeat(n_beats, bpm=58):   # soft low double thump
    per = 60 / bpm; n = int(n_beats * per * SR); y = np.zeros(n); tt = np.arange(int(0.35 * SR)) / SR
    th = np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 18)
    for b in range(n_beats):
        for off, g in ((0, 1.0), (0.22, 0.6)):
            i = int((b * per + off) * SR); seg = th[: max(0, n - i)] * g; y[i:i + len(seg)] += seg
    return y * 0.5

# ---------- score ----------
mus = Bus()
# chord per shot: Freud shots sit on D minor colours, Jung shots open to Bb / F / Gm
CH = {0: [38, 45, 50], 1: [34, 41, 46], 2: [38, 45], 3: [38, 45, 50], 4: [36, 43, 48], 5: [34, 41, 46], 6: [38, 45, 50],
      7: [31, 38, 46], 8: [34, 41, 46], 9: [38, 45, 50, 54], 10: [36, 43, 48], 11: [38, 45, 50]}
bounds = SHOTS + [COVER0]
for i in range(len(SHOTS)):
    t0, t1 = bounds[i], bounds[i + 1]
    mus.add(cello(CH[i], t1 - t0 + 3.0), t0 - 0.6, pan=0.0, g=1.0)
mus.add(cello([38, 45, 50, 57], DUR - COVER0 + 1.0, att=1.0, rel=2.0, bright=1300), COVER0 - 0.3, g=1.0)
# the motif and its mirror image (inversion around D5 = 74)
MOT = [74, 77, 81, 76]                      # D F A E
MIR = [74 - (m - 74) for m in MOT]          # D B G C  (mirror)
def phrase(t0, notes, step=0.42, vel=0.55, pan=0.0):
    for k, m in enumerate(notes): mus.add(glass(m, 3.2, vel), t0 + k * step, pan=pan)
phrase(0.25, MOT, pan=-0.3); phrase(1.95, MIR, vel=0.45, pan=0.3)           # hook: motif, then its reflection
for i in (1, 5, 7, 8):                                                         # Jung shots: the motif returns
    phrase(SHOTS[i] + 0.3, MOT if i % 2 else MIR, vel=0.38, pan=-0.2 if i % 2 else 0.2)
phrase(wt(119) + 0.2, MOT, vel=0.42, pan=-0.25); phrase(wt(119) + 2.0, MIR, vel=0.36, pan=0.25)
phrase(COVER0 + 0.2, [74, 78, 81, 86], step=0.3, vel=0.5)                       # resolution: D major on the cover
# heartbeat under the locked chest
hb = heartbeat(int((SHOTS[5] - SHOTS[4]) / (60 / 58)) + 1); mus.add(hb, SHOTS[4], g=0.9)
reverb(mus, 3.8, 0.35, 1.3)
m = mus.st(); fade = np.clip((DUR - np.arange(N) / SR) / 1.2, 0, 1); m *= fade[:, None]
wavfile.write('audio/music.wav', SR, (m / (np.abs(m).max() + 1e-9) * 0.8).astype(np.float32))

# ---------- ambience: a quiet study at night ----------
amb = Bus(); n = N; tt = np.arange(n) / SR
room = lp(np.cumsum(rng.standard_normal(n)) * 0.002, 700); room -= lp(room, 30)
amb.add(room * 0.6, 0, pan=-0.2); amb.add(np.roll(room, 9000) * 0.6, 0, pan=0.2)
for _ in range(140):   # sparse fire crackles
    t0 = rng.uniform(0, DUR - 0.1); L = int(0.012 * SR); c = hp(rng.standard_normal(L), 1500) * np.exp(-np.arange(L) / SR * 300)
    amb.add(c * rng.uniform(0.05, 0.25), t0, pan=rng.uniform(-0.6, 0.6))
a = amb.st(); wavfile.write('audio/amb.wav', SR, (a / (np.abs(a).max() + 1e-9) * 0.5).astype(np.float32))

# ---------- sfx ----------
sfx = Bus()
def glass_whoosh(dur=0.6, up=True):
    n = int(dur * SR); tt = np.arange(n) / SR; k = tt / dur
    y = np.zeros(n); noise = rng.standard_normal(n)
    for j in range(0, n, 480):   # time-varying band (sweep)
        fc = 700 + (4200 if up else -0) * (k[j] if up else 1 - k[j]) + 600; seg = noise[j:j + 480]
        y[j:j + 480] = bp(seg, max(200, fc * 0.7), min(16000, fc * 1.4), 1)
    y *= np.sin(np.pi * k) ** 1.5 * 0.5
    ping = sum(np.sin(2 * np.pi * f * tt) for f in (2349, 3520, 4699)) * np.exp(-np.clip(tt - dur * 0.55, 0, None) * 9) * (tt > dur * 0.55) * 0.12
    return y + ping
def impact(dur=2.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    body = np.sin(2 * np.pi * (60 * np.exp(-tt * 2) + 34) * tt) * np.exp(-tt * 2.2)
    air = lp(rng.standard_normal(n), 900) * np.exp(-tt * 6) * 0.4
    return (body + air) * 0.9
def chime(ms, dur=3.0, vel=0.5):
    return sum(glass(m, dur, vel) for m in ms) * 1.6
def thump():
    n = int(0.4 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 80 * tt) * np.exp(-tt * 14) + lp(rng.standard_normal(n), 400) * np.exp(-tt * 20) * 0.6) * 0.8
for i in range(1, len(SHOTS)):
    sfx.add(glass_whoosh(0.6, up=bool(i % 2)), SHOTS[i] - 0.05, pan=(-0.5 if i % 2 else 0.5), g=0.55)
sfx.add(chime([86, 93], 2.5, 0.5), 0.92, g=0.6)                 # "KENDİ GÖLGEN" lands
sfx.add(thump(), SHOTS[4] + 0.02, g=0.7); sfx.add(thump(), SHOTS[4] + 0.38, g=0.45)   # the chest shakes
sfx.add(impact(), wt(59) - 0.05, g=0.9)                         # GÖLGE
sfx.add(chime([74, 78, 81], 3.0, 0.5), wt(94) - 0.05, g=0.6)     # BİREYLEŞME
sfx.add(chime([81, 86], 2.5, 0.45), wt(119) - 0.05, g=0.5)       # the question
sfx.add(chime([86, 90, 93], 3.0, 0.5), COVER0 - 0.02, g=0.7)    # the cover: mirror ping
reverb(sfx, 2.5, 0.25, 2.0)
s = sfx.st(); wavfile.write('audio/sfx.wav', SR, (s / (np.abs(s).max() + 1e-9) * 0.9).astype(np.float32))
print('music/amb/sfx written', DUR, 's; shots', [round(x, 2) for x in SHOTS], 'cover', round(COVER0, 2))

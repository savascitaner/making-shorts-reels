# Jung Haklı mıydı? — kodla müzik + ses tasarımı + miks.  uv run --with numpy --with scipy python muzik_jung.py reels|16x9
# Motif: GERGİN TEL. Her kesmede bir tel çekilir (Karplus-Strong); yedi iplikte yedi nota yükselir; yaylı zemin re minör,
# yakınsamada ve finalde re majöre açılır. Örnek/kayıt yok, hepsi sentez (lisans derdi yok).
import sys, os, json, subprocess, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
sys.path.insert(0, "/Users/claude-eng/Shorts - Reels")
from sfx import synth as X

F = sys.argv[1]; SR = 48000
O = json.load(open(f"olaylar-{F}.json")); DUR = O["DUR"]; END0 = O["END0"]; N = int(SR * DUR); T = np.arange(N) / SR
CUTS = O["cuts"]; os.makedirs(f"audio/{F}", exist_ok=True)
rng = np.random.default_rng(1875)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
lp = lambda x, f, o=2: sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)
hp = lambda x, f, o=2: sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)
A = lambda l: np.asarray(l, np.float64)
def first(pred, default=None):
    for c in CUTS:
        if pred(c): return c[0]
    return default
# ---- bölüm sınırları (motordan) ----
t_kir = first(lambda c: c[1] == "S2a-enkaz"); t_pen = first(lambda c: c[1] == "S3a-pencereler"); t_ip = first(lambda c: c[1] == "S4a-siluet")
t_con = first(lambda c: c[2] == "converge"); t_olc = first(lambda c: c[1] == "S5a-yanan-sayfa"); t_dog = first(lambda c: c[1] == "A6a-agora")
t_fin = first(lambda c: c[2] == "palm"); t_kan = first(lambda c: c[2] == "kanal")
IP = {}
for c in CUTS:
    if c[2].startswith("iplik:"): IP.setdefault(int(c[2].split(":")[1]), c[0])

class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, sig, t0, pan=0.0, g=1.0):
        sig = A(sig); i = int(t0 * SR)
        if i >= N: return
        if i < 0: sig = sig[-i:]; i = 0
        sig = sig[:N - i] * g; s.L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan)); s.R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))
    def st(s): return np.stack([s.L, s.R], 1)
def reverb(bus, sec=3.5, wet=0.3):
    n = int(sec * SR); it = np.arange(n) / SR
    for ch in ("L", "R"):
        ir = lp(rng.standard_normal(n) * np.exp(-it * 1.6), 5000); ir /= np.sqrt((ir ** 2).sum())
        x = getattr(bus, ch); setattr(bus, ch, x * (1 - wet) + fftconvolve(x, ir)[:N] * wet * 1.5)

# ---------- yaylı zemin ----------
def strings(freqs, t0, t1, att=2.5, rel=2.5, g=1.0):
    t0 = max(0, t0); n = int((t1 - t0 + rel) * SR); tt = np.arange(n) / SR; out = np.zeros(n)
    for f in freqs:
        for det in (-0.004, 0.0, 0.0045):
            ff = f * (1 + det); ph = rng.random() * 6.28; vib = 1 + 0.003 * np.sin(2 * np.pi * 5.2 * tt + ph)
            s = np.zeros(n)
            for h in range(1, 9): s += np.sin(2 * np.pi * ff * h * np.cumsum(vib) / SR + ph * h) / h   # testere yaklaşımı
            out += s
    out = lp(out, 1800) / (len(freqs) * 3)
    env = np.clip(tt / att, 0, 1) * np.clip((t1 - t0 + rel - tt) / rel, 0, 1); env *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * tt)
    return out * env * g
def chord(names): return [hz(m) for m in names]
Dm = [38, 45, 50, 53, 57]; Bb = [34, 46, 50, 53, 58]; Gm = [31, 43, 50, 55, 58]; Am = [33, 45, 52, 57, 60]
Fm = [41, 48, 53, 57, 60]; C = [36, 48, 52, 55, 60]; DM = [38, 45, 50, 54, 57, 62]; Asus = [33, 45, 50, 52, 57]
mus = Bus()
def prog(t0, t1, seq, dur, g=1.0, pan=0.0):
    t = t0; i = 0
    while t < t1:
        e = min(t1, t + dur); mus.add(strings(chord(seq[i % len(seq)]), t, e + 0.6, att=1.8, rel=2.2, g=g), t, pan); t = e; i += 1
prog(0, t_kir, [Dm, Bb, Dm, Asus], 6.0, 0.8)
prog(t_kir, t_pen, [Bb, Gm, Bb, Asus], 5.0, 0.7)
prog(t_pen, t_ip, [Gm, Bb, Fm, C], 3.6, 0.9)
prog(t_ip, t_con, [Dm], 60, 0.75)
prog(t_con, t_olc, [DM, Bb, DM], 4.5, 1.0)
prog(t_olc, t_dog, [Fm, C, Dm, Bb], 4.2, 0.85)
prog(t_dog, t_fin, [Gm, Dm, Bb, Asus], 4.5, 0.85)
prog(t_fin, t_kan, [Bb, Fm, DM], 2.6, 1.1)
prog(t_kan, END0, [DM, Bb, DM], 3.5, 0.8)
prog(END0, DUR, [Dm, Bb, DM], 3.4, 0.75)
# kırılma bölümünde kalp atışı gibi alçak darbe (60 bpm)
t = t_kir
while t < t_pen - 0.5:
    for dt, gg in ((0, 1.0), (0.32, 0.6)):
        n = int(0.5 * SR); tt = np.arange(n) / SR; k = np.sin(2 * np.pi * (55 * np.exp(-tt * 3)) * tt) * np.exp(-tt * 9)
        mus.add(k, t + dt, 0, 0.55 * gg)
    t += 1.0
# pencereler bölümünde yumuşak arpej (tel) — sekizlikler
def ks(freq, dur=1.6, bright=0.5, decay=0.996):   # Karplus-Strong tel
    n = int(dur * SR); p = max(2, int(SR / freq)); buf = rng.uniform(-1, 1, p) * 0.8; out = np.zeros(n)
    buf = lp(buf, 1500 + 6000 * bright)
    for i in range(n):
        out[i] = buf[i % p]; nxt = buf[(i + 1) % p]; buf[i % p] = decay * 0.5 * (buf[i % p] + nxt)
    return out * np.exp(-np.arange(n) / SR * 1.2)
ARP = {tuple(Gm): [55, 58, 62, 67], tuple(Bb): [58, 62, 65, 70], tuple(Fm): [53, 57, 60, 65], tuple(C): [55, 60, 64, 67]}
t = t_pen; seq = [Gm, Bb, Fm, C]; i = 0
cache = {}
def KS(m, dur=1.4, br=0.5):
    key = (m, dur, br)
    if key not in cache: cache[key] = ks(hz(m), dur, br)
    return cache[key]
while t < t_ip - 0.3:
    notes = ARP[tuple(seq[int((t - t_pen) // 3.6) % 4])]
    mus.add(KS(notes[i % 4], 1.2, 0.4), t, 0.3 * ((i % 2) * 2 - 1), 0.22); t += 0.45; i += 1
reverb(mus, 4.0, 0.35)

# ---------- efektler ----------
fx = Bus()
PLUCK = [74, 77, 79, 81, 84, 81, 79, 77]   # D5 F5 G5 A5 C6 ... tel tınısı
pi = 0
for n, c in enumerate(CUTS[1:], 1):
    t0, k, eff = c[0], c[1], c[2]
    if k == CUTS[n - 1][1] and not eff.startswith("iplik"): continue
    if eff.startswith("iplik"):
        j = int(eff.split(":")[1])
        if IP.get(j) == t0:   # yedi iplik: yükselen yedi nota + alçak tel
            m = [62, 65, 69, 72, 74, 77, 81][j]
            fx.add(KS(m, 2.4, 0.7), t0 + 0.05, (j - 3) / 4, 0.55); fx.add(KS(m - 24, 2.4, 0.3), t0 + 0.05, 0, 0.35)
            fx.add(X.whoosh(0.9, 300, 2400, 0.7), t0 - 0.2, (j - 3) / 4, 0.12)
            continue
    fx.add(KS(PLUCK[pi % len(PLUCK)], 1.6, 0.6), t0 + 0.12, 0.4 * (1 if pi % 2 else -1), 0.32); pi += 1
    fx.add(X.whoosh(0.7, 500, 3000, 0.6), t0 - 0.15, 0.5 * (1 if pi % 2 else -1), 0.10)
    if eff == "shatter":   # cam kubbe kırılır
        n0 = int(1.6 * SR); tt = np.arange(n0) / SR; g = hp(rng.standard_normal(n0), 3000) * np.exp(-tt * 6) * 0.6
        for _ in range(28): f0 = rng.uniform(2500, 7000); g += np.sin(2 * np.pi * f0 * tt) * np.exp(-tt * rng.uniform(6, 14)) * 0.05 * (tt > rng.uniform(0, 0.25))
        fx.add(g, t0, 0, 0.9); fx.add(X.impact(1.0), t0, 0, 0.5)
    if eff == "headlights":   # yaklaşan ışık: yükselen gürültü, kesmede susar
        nx = next((c2[0] for c2 in CUTS[n + 1:]), t0 + 5); d = nx - t0
        r = A(X.riser(max(0.5, d - 0.3), 120, 2500)); fx.add(r, t0 + 0.2, 0, 0.18)
    if eff == "converge":
        fx.add(X.riser(2.0, 200, 3000), t0 + 0.1, 0, 0.15); fx.add(X.chime([hz(62), hz(66), hz(69), hz(74)], 3.0, 1.2), t0 + 2.0, 0, 0.35)
    if eff == "palm":
        fx.add(X.chime([hz(62), hz(66), hz(69), hz(74), hz(78)], 3.5, 1.4), t0 + 2.1, 0, 0.35)
    if eff == "kanal":
        fx.add(X.chime([hz(74), hz(78), hz(81)], 2.0, 0.8), t0 + 0.2, 0, 0.25)
# kanca vuruşu
fx.add(X.impact(1.6), 0.0, 0, 0.7); fx.add(KS(50, 3.0, 0.5), 0.02, 0, 0.6); fx.add(KS(62, 2.5, 0.7), 0.05, 0.2, 0.35)
# kapanış dizisi
E = {"takip": 3.6, "kapak": 6.3, "adres": 8.3}
fx.add(KS(74, 1.6, 0.6), END0 + E["takip"], -0.3, 0.3); fx.add(X.chime([hz(62), hz(69), hz(74)], 2.2, 0.9), END0 + E["kapak"], 0, 0.3)
for i in range(3): fx.add(X.pop(500 + i * 150, 900 + i * 150, 0.16), END0 + E["adres"] + i * 0.15, 0, 0.18)
reverb(fx, 2.5, 0.2)

# ---------- miks ----------
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f"../ses/vo-{F}.mp3", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
vo = np.frombuffer(pcm, np.float32).reshape(-1, 2).astype(np.float64); V = np.zeros((N, 2)); V[:min(N, len(vo))] = vo[:N]
rms = lambda x: np.sqrt(np.mean(x[np.abs(x).max(1) > 1e-4] ** 2) + 1e-12)
vr = rms(V)
act = np.zeros(N)
for w, s in O["words"]: act[int(max(0, s - 0.15) * SR):int((s + 0.6) * SR)] = 1
env = np.clip(sosfilt(butter(1, 2.0, fs=SR, output="sos"), act) * 1.15, 0, 1)
M = mus.st(); Fx = fx.st()
mix = V.copy()
mix += M * (vr / rms(M)) * 10 ** (-12 / 20) * (10 ** (-8 * env / 20))[:, None]
mix += Fx * (vr / (np.abs(Fx).max() + 1e-9)) * 10 ** (-4 / 20)
# son 0,6 sn'de yumuşak kapanış
fo = np.clip((DUR - T) / 0.6, 0, 1); mix *= fo[:, None]
wavfile.write(f"audio/{F}/mix.wav", SR, mix.astype(np.float32)); wavfile.write(f"audio/{F}/music.wav", SR, M.astype(np.float32))
print(F, "süre", round(DUR, 2), "tepe", round(float(np.abs(mix).max()), 3))

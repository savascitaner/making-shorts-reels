# Marcus Aurelius score + sound design, synthesized in code (no samples, no licences).
#   uv run --with numpy --with scipy python music.py audio DURATION b1,b2,... "" "" boom
# Instruments are Roman, not piano: plucked lyre, bowed cello ostinato, frame drum, "aah" choir, bronze bell.
# One key for every tonal sound: D Dorian; the finale resolves to D major. Every cue time is read from
# words.json (the same file the picture reads) so picture and sound cannot drift apart.
import sys, os, json, numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

SR = 48000
outdir, DUR = sys.argv[1], float(sys.argv[2])
B = [0.0] + [float(x) for x in sys.argv[3].split(",") if x] + [DUR]
rng = np.random.default_rng(1802)
N = int(SR * DUR); t = np.arange(N) / SR
WD = json.load(open("words.json"))["words"]
wt = lambda i: WD[i]["s"]
def IDX(word, frm=0):
    for j in range(frm, len(WD)):
        if WD[j]["w"].strip(".,?!:;") == word: return j
    raise SystemExit("word not found " + word)

def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def tt_(d): return np.arange(int(d * SR)) / SR

class Bus:
    def __init__(s): s.L = np.zeros(N); s.R = np.zeros(N)
    def add(s, sig, t0, pan=0.0, g=1.0):
        i0 = int(t0 * SR)
        if i0 >= N or len(sig) == 0: return
        if i0 < 0: sig = sig[-i0:]; i0 = 0
        n = min(len(sig), N - i0); l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
        s.L[i0:i0 + n] += sig[:n] * g * l * 1.414; s.R[i0:i0 + n] += sig[:n] * g * r * 1.414
    def st(s): return np.stack([s.L, s.R], 1)

def reverb(bus, sec=3.0, wet=0.3, decay=2.0, lpf=5000):
    n = int(sec * SR); k = np.arange(n) / SR
    for ch in ("L", "R"):
        ir = lp(rng.standard_normal(n), lpf) * np.exp(-k * decay); ir /= np.sqrt(np.sum(ir ** 2))
        x = getattr(bus, ch); setattr(bus, ch, x * (1 - wet) + fftconvolve(x, ir)[:N] * wet)

# ---------------- instruments ----------------
def lyre(m, dur=3.0, vel=0.7):            # plucked gut string: decaying harmonics, brighter partials die first
    tt = tt_(dur); f = hz(m); y = np.zeros_like(tt)
    for h in range(1, 9): y += np.sin(2 * np.pi * h * f * tt * (1 + 0.0007 * h)) / h ** 1.15 * np.exp(-tt * (1.2 + 1.1 * h))
    y += bp(rng.standard_normal(len(tt)), 1500, 5000) * np.exp(-tt * 90) * 0.15     # the pluck
    return y * vel * 0.22

def cello(m, dur, att=0.08, rel=0.25, bright=1400, vib=0.004):   # bowed: band-limited saw, vibrato, rosin noise
    tt = tt_(dur + rel); f = hz(m) * (1 + vib * np.sin(2 * np.pi * 5.2 * tt + rng.uniform(0, 6)) * np.clip(tt / 0.4, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR; y = sum(np.sin(h * ph) / h for h in range(1, 12))
    y = lp(y, bright, 2) + bp(rng.standard_normal(len(tt)), 1800, 5000) * 0.03
    e = np.clip(tt / att, 0, 1) * np.clip((dur + rel - tt) / rel, 0, 1)
    return y * e * 0.09

def choir(ms, dur, att=1.8, rel=2.5):     # "aah": detuned saws through vowel formants
    tt = tt_(dur + rel); y = np.zeros_like(tt)
    for m in ms:
        for d in (-0.08, 0.0, 0.09):
            f = hz(m) * 2 ** (d / 12) * (1 + 0.003 * np.sin(2 * np.pi * (4.6 + rng.uniform(-.5, .5)) * tt + rng.uniform(0, 6)))
            ph = 2 * np.pi * np.cumsum(f) / SR + rng.uniform(0, 6); y += 2 * ((ph / (2 * np.pi)) % 1) - 1
    v = bp(y, 600, 900) * 1.0 + bp(y, 1000, 1300) * 0.6 + bp(y, 2300, 2800) * 0.25 + lp(y, 400) * 0.5
    e = np.clip(tt / att, 0, 1) ** 1.5 * np.clip((dur + rel - tt) / rel, 0, 1) ** 1.3
    return v * e * 0.02 / max(1, len(ms)) ** 0.5

def drum(vel=1.0, low=True):              # frame drum: pitched skin thump + slap
    tt = tt_(0.9); f0 = 95 if low else 180
    body = np.sin(2 * np.pi * (f0 * 0.55 + f0 * 0.45 * np.exp(-tt * 18)) * tt) * np.exp(-tt * (6 if low else 14))
    slap = bp(rng.standard_normal(len(tt)), 700, 3500) * np.exp(-tt * 55) * (0.25 if low else 0.55)
    return (body + slap) * vel * 0.5

def bell(m, dur=6.0):                     # bronze bell: inharmonic partials, long hum
    tt = tt_(dur); f = hz(m); y = np.zeros_like(tt)
    for r, a, d in [(0.5, .5, .5), (1, 1, .8), (1.19, .6, 1.1), (1.56, .45, 1.4), (2.0, .35, 1.8), (2.51, .25, 2.4), (3.01, .2, 3)]:
        y += np.sin(2 * np.pi * f * r * tt) * a * np.exp(-tt * d)
    return y * 0.12 * np.clip(tt / 0.004, 0, 1)

# ---------------- score ----------------
mus = Bus()
D, F, G, A, C, E, Bb = 50, 53, 55, 57, 48, 52, 46    # D Dorian pitches (D3 = 50)
CH = {"Dm": [38, 50, 53, 57], "C": [36, 48, 52, 55], "F": [41, 48, 53, 57], "G": [43, 50, 55, 59], "Am": [45, 52, 57, 60], "Bb": [34, 50, 53, 58], "D": [38, 50, 54, 57]}
b = B
def ostinato(t0, t1, step=0.3, g=1.0, pat=(D, D, F, D, E, D, C, A - 12)):   # cello 8ths: the night, the rebellion
    k = 0; x = t0
    while x < t1 - 0.05:
        m = pat[k % len(pat)] - 12; acc = 1.0 if k % 4 == 0 else 0.7
        mus.add(cello(m, step * 0.85, att=0.02, rel=0.08, bright=900), x, pan=-0.25, g=g * acc); x += step; k += 1
def march(t0, t1, step=0.6, g=1.0):                                          # frame drum: 1 . (3) . with a ghost
    x = t0; k = 0
    while x < t1 - 0.05:
        if k % 4 in (0, 2): mus.add(drum(1.0 if k % 4 == 0 else 0.7), x, pan=0.1, g=g)
        if k % 8 == 7: mus.add(drum(0.5, low=False), x + step * 0.5, pan=0.3, g=g * 0.7)
        x += step; k += 1
def lyre_arp(t0, t1, chords, bar=2.4, g=1.0, high=0):
    x = t0; k = 0
    while x < t1 - 0.3:
        ch = CH[chords[k % len(chords)]]; notes = [ch[1], ch[2], ch[3], ch[2] + 12 if high else ch[2]]
        for j, m in enumerate(notes): mus.add(lyre(m + 12, 3.0, 0.55 + 0.25 * rng.random()), x + j * bar / 4 + rng.uniform(0, .015), pan=-0.4 + 0.25 * j, g=g)
        x += bar; k += 1
def drone(t0, t1, ms, g=1.0):
    mus.add(cello(ms[0], t1 - t0, att=1.5, rel=2.0, bright=500, vib=0.002), t0, g=g)
    for m in ms[1:]: mus.add(cello(m, t1 - t0, att=2.0, rel=2.0, bright=700, vib=0.002), t0, pan=0.3, g=g * 0.6)

# 0 hook: low drone, the drum lands on "okumadı", choir breath
drone(0, b[1] + 1.0, [D - 24, A - 24], 1.1)
mus.add(drum(1.3), wt(IDX("okumadı")) - 0.02, g=1.4); mus.add(choir([D, A], 3.0, att=0.6, rel=2.0), wt(IDX("okumadı")) - 0.3, g=0.8)
# 1 the rebellion night: ostinato + march
ostinato(b[1], b[2], 0.3, 1.0); march(b[1] + 2.4, b[2], 0.6, 0.9); drone(b[1], b[2], [D - 24], 0.7)
# 2 the boy who did not want a throne: lyre
lyre_arp(b[2], b[3], ["Dm", "C", "F", "Dm"], 2.4, 0.9); drone(b[2], b[3], [D - 12], 0.4)
# 3 Stoa: lyre brighter + bowed pad, gentle drum in the second half
lyre_arp(b[3], b[4], ["F", "C", "Dm", "Am", "Bb", "F", "G", "C"], 2.2, 1.0, high=1)
for x, ch in zip(np.arange(b[3], b[4] - 1, 4.4), ["F", "Dm", "Bb", "G", "F", "C", "Dm", "Am", "Bb", "G"]): mus.add(cello(CH[ch][0], 4.4, att=1.2, rel=1.5, bright=700), x, g=0.55)
march((b[3] + b[4]) / 2, b[4], 1.1, 0.35)
# 4 the burden: plague bell tolls, long low cello
for x in np.arange(b[4] + 0.2, b[4] + 14, 3.3): mus.add(bell(D, 6.0), x, pan=-0.2, g=0.9)
drone(b[4], b[5], [D - 24, F - 12], 0.9)
# 5 the notebook: a single cello line over sparse lyre
mel = [(A, 1.6), (G, 0.8), (F, 1.6), (E, 0.8), (D, 2.4), (F, 1.2), (G, 1.2), (A, 2.4), (C + 12, 1.2), (A, 1.2), (G, 2.4)]
x = b[5] + 0.3
for m, d in mel:
    if x > b[6] - 0.5: break
    mus.add(cello(m, d, att=0.25, rel=0.5, bright=1600), x, pan=0.15, g=1.0); x += d
lyre_arp(b[5], b[6], ["Dm", "F", "C", "G"], 4.0, 0.5)
# 6 climax: fire returns; everything drops when he is dying
death = wt(IDX("Beş", 300)) - 0.1
ostinato(b[6], death, 0.27, 1.1); march(b[6], death, 0.54, 1.0)
mus.add(choir([D, F, A], death - b[6], att=4.0, rel=1.5), b[6], g=1.0)
mus.add(choir([D - 12, A - 12, D], b[7] - death + 1, att=1.0, rel=2.0), death, g=0.9)
# 7 today: resolves to D major, last lyre plucks
mus.add(choir([D, 54, A, D + 12], DUR - b[7] + 1, att=1.5, rel=2.5), b[7] - 0.3, g=1.1)
for j, m in enumerate([D, 54, A, D + 12, 54 + 12]): mus.add(lyre(m + 12, 4.0, 0.6), b[7] + 0.4 + j * 0.35, pan=-0.3 + 0.15 * j, g=0.9)
reverb(mus, 3.4, 0.3, 1.6)
fade = np.clip(t / 0.05, 0, 1) * np.clip((DUR - t) / 2.5, 0, 1); mus.L *= fade; mus.R *= fade

# ---------------- ambience beds tied to scenes ----------------
amb = Bus()
def bed(sig_fn, t0, t1, g, fin=0.6, fout=0.8, pan=0.0):
    if t1 <= t0: return
    x = sig_fn(t1 - t0); n = len(x); k = np.arange(n) / SR; e = np.clip(k / fin, 0, 1) * np.clip((t1 - t0 - k) / fout, 0, 1); amb.add(x * e, t0, pan, g)
def crackle_sig(d, rate=40):
    n = int(d * SR); out = np.zeros(n)
    for _ in range(int(rate * d)):
        ln = int(rng.uniform(0.003, 0.03) * SR); ti = int(rng.uniform(0, d) * SR)
        if ti + ln >= n: continue
        a = np.exp(rng.normal(-1.0, 0.9)) * (3 if rng.random() < 0.08 else 1)
        out[ti:ti + ln] += rng.standard_normal(ln) * np.exp(-np.arange(ln) / (ln / rng.uniform(3, 6))) * a
    return np.clip(hp(out, 1500, 1) * 0.2, -0.25, 0.25) + lp(rng.standard_normal(n), 300) * 0.05
def wind_sig(d):
    n = int(d * SR); k = np.arange(n) / SR; nz = bp(rng.standard_normal(n), 200, 900)
    gust = 0.5 + 0.5 * np.sin(2 * np.pi * k / 6.7 + rng.uniform(0, 6)) * np.sin(2 * np.pi * k / 2.9 + rng.uniform(0, 6))
    return nz * gust * 0.5 + hp(rng.standard_normal(n), 6000) * 0.03
def crowd_sig(d):                         # murmur: band-limited voices with syllable-rate envelopes
    n = int(d * SR); k = np.arange(n) / SR; y = np.zeros(n)
    for v in range(14):
        lo = rng.uniform(250, 500); syl = rng.uniform(3, 5.5)
        env = np.clip(np.sin(2 * np.pi * syl * k + rng.uniform(0, 6)), 0, 1) ** 2 * (0.4 + 0.6 * np.clip(np.sin(2 * np.pi * k / rng.uniform(2, 5) + rng.uniform(0, 6)), 0, 1))
        y += bp(rng.standard_normal(n), lo, lo * 4) * env
    return lp(y, 2500) * 0.12
S = lambda w, frm=0: wt(IDX(w, frm)) - 0.1      # a shot's start, as the picture computes it
bed(crackle_sig, 0, S("Yıl") + 0.8, 1.0)                                     # hook brazier
bed(wind_sig, S("Ama"), S("Sonra", 40), 0.9)                                # Danube blizzard + tent
bed(lambda d: crackle_sig(d, 15) * 0.6, S("Üç"), S("Sonra", 40), 0.5)       # tent torches
bed(crowd_sig, S("Kuzeyden"), S("Ve", 239), 0.8)                            # auction in the Forum
bed(wind_sig, S("Ve", 239), S("Her", 250), 0.35)                            # frontier hut at night
bed(crackle_sig, S("Şimdi"), death, 1.1)                                    # the bonfire of letters
bed(crowd_sig, S("Şimdi"), S("Seni"), 0.45)                                 # stunned officers
bed(lambda d: wind_sig(d) * 0.5, death, S("Kimse"), 0.4)                   # dawn tent
amb.L *= fade; amb.R *= fade

# ---------------- sound effects: accent, don't narrate ----------------
sfx = Bus()
def seal_stamp():                          # wax pressed: low thud, wax squash, the signet's click
    tt = tt_(1.0); thud = np.sin(2 * np.pi * (48 + 40 * np.exp(-tt * 25)) * tt) * np.exp(-tt * 9)
    squash = bp(rng.standard_normal(len(tt)), 300, 1400) * np.exp(-((tt - 0.03) / 0.03) ** 2) * 0.5
    click = bp(rng.standard_normal(len(tt)), 2500, 7000) * np.exp(-tt * 160) * 0.35
    return (thud * 1.2 + squash + click) * 0.6
def burn_whoosh(d=1.1):                    # parchment catching: rising roar + a burst of crackle
    tt = tt_(d); k = tt / d; nz = rng.standard_normal(len(tt))
    roar = (bp(nz, 150, 700) * 0.8 + bp(nz, 800, 3000) * 0.35) * np.sin(np.pi * k) ** 1.5
    return roar * 0.5 + crackle_sig(d, 90)[:len(tt)] * np.sin(np.pi * k) * 1.2
def ink_swell(d=1.0):                      # ink spreading: a dark, wet low swell with a drip
    tt = tt_(d); k = tt / d; y = lp(rng.standard_normal(len(tt)), 900) * np.sin(np.pi * k) ** 2 * 0.6
    z = np.clip(tt - 0.15, 0, None); drip = np.sin(2 * np.pi * (900 - 500 * np.clip(z / 0.06, 0, 1)) * z) * np.exp(-z * 40) * (tt > 0.15) * 0.25
    return y + drip
def air_swell(d=0.8):                      # light / snow whiteout
    tt = tt_(d); k = tt / d; return bp(rng.standard_normal(len(tt)), 2000, 9000) * np.sin(np.pi * k) ** 2 * 0.35
def chisel():                              # carved card: two stone-chisel ticks
    tt = tt_(0.4); y = np.zeros(len(tt))
    for o in (0.0, 0.11):
        z = np.clip(tt - o, 0, None); y += (bp(rng.standard_normal(len(tt)), 2500, 8000) * np.exp(-z * 120) + np.sin(2 * np.pi * 2350 * z) * np.exp(-z * 60) * 0.3) * (tt >= o)
    return y * 0.35
def quill(d):                              # reed pen on papyrus: short scratch strokes
    n = int(d * SR); k = np.arange(n) / SR; strokes = np.clip(np.sin(2 * np.pi * 7.3 * k + np.sin(2 * np.pi * 1.7 * k) * 2), 0, 1) ** 3
    return bp(rng.standard_normal(n), 2500, 7500) * strokes * 0.35
def armour():                              # bronze armour shifting
    tt = tt_(0.6); y = np.zeros(len(tt))
    for o in (0, 0.07, 0.19):
        z = np.clip(tt - o, 0, None); y += sum(np.sin(2 * np.pi * f * z) * np.exp(-z * 25) for f in (1650, 2780, 4130)) * (tt >= o) * rng.uniform(0.5, 1)
    return y * 0.06
def heartbeat(bpm, n):                     # slowing lub-dub
    out = np.zeros(int((n * 60 / bpm * 2 + 1) * SR))
    for i in range(n):
        for o, a in ((0, 1.0), (0.28, 0.7)):
            tt = tt_(0.4); x = np.sin(2 * np.pi * (52 + 25 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14) * a
            i0 = int((i * 60 / bpm * (1 + i * 0.12) + o) * SR); m = min(len(x), len(out) - i0); out[i0:i0 + m] += x[:m]
    return out * 0.7
def impact():                              # the one hero hit: the name
    tt = tt_(2.5); sub = np.sin(2 * np.pi * (60 * np.exp(-tt * 3) + 30) * tt) * np.exp(-tt * 2.2)
    return sub * 1.3 + lp(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 16) * 0.7

# transitions (same words and types as the picture's shot list)
for w, frm in (("Yıl", 0), ("Şimdi", 270)): sfx.add(burn_whoosh(1.1), S(w, frm) - 0.25, g=0.9)
sfx.add(burn_whoosh(1.0), S("Daha", 350) - 0.2, g=0.6)
for w, frm in (("Sonra", 190), ("Ve", 239)): sfx.add(ink_swell(1.0), S(w, frm) - 0.1, g=0.8)
for w, frm in (("Ama", 0), ("Çünkü", 100), ("Beş", 300)): sfx.add(air_swell(0.8), S(w, frm) - 0.15, g=0.8)
# chapter seals, the name impact (the single hero hit), the question seal, the closing seal
for w, frm in (("Yıl", 0), ("Çünkü", 100), ("Sonra", 190), ("Ve", 239), ("Şimdi", 270)): sfx.add(seal_stamp(), S(w, frm) + 0.1, g=0.75)
name = S("Adı", 60) + 0.1; sfx.add(impact(), name, g=1.0); sfx.add(seal_stamp(), name + 0.02, g=0.8)
sfx.add(seal_stamp(), S("Sence", 330) + 0.05, g=0.7); sfx.add(seal_stamp(), S("Daha", 350) + 1.15, g=0.8)
# carved cards (only the big ones)
for w, frm in (("Verissimus", 80), ("Stoa'ydı", 120), ("erdemdi", 130), ("Kendine", 240), ("Sezarlaşma", 270)): sfx.add(chisel(), wt(IDX(w, frm)) - 0.05, pan=0.15, g=0.6)
for j, i in enumerate((186, 187, 188, 190, 191, 192)): sfx.add(chisel()[: int(0.15 * SR)], wt(i) - 0.05, pan=-0.5 + 0.2 * j, g=0.45)
# writing: the notebook, the morning line, the quote
sfx.add(quill(max(0.5, S("Her", 250) - S("Ve", 239) - 0.6)), S("Ve", 239) + 0.6, pan=-0.2, g=0.7)
sfx.add(quill(2.2), wt(IDX("Bugün", 250)), pan=0.2, g=0.4)
sfx.add(quill(1.0), wt(IDX("Seni", 285)) - 0.6, pan=0.3, g=0.3)
# tent: armour as he turns away
sfx.add(armour(), wt(IDX("Bakmadı")) - 0.3, pan=0.3, g=0.8); sfx.add(armour(), S("Üç") + 0.4, pan=-0.3, g=0.5)
# the auction: a gavel knock on "çıkardı"
gv = tt_(0.3); sfx.add((np.sin(2 * np.pi * 180 * gv) * np.exp(-gv * 30) + bp(rng.standard_normal(len(gv)), 800, 3000) * np.exp(-gv * 80) * 0.4) * 0.6, wt(IDX("çıkardı")) - 0.05, g=0.8)
# dying: a slowing heartbeat
sfx.add(heartbeat(62, 5), death + 0.3, g=0.9)
reverb(sfx, 2.2, 0.35, 2.6, 5000)

def write(name, bus, peak=0.5):
    x = bus.st(); x *= peak / (np.max(np.abs(x)) + 1e-9)
    wavfile.write(os.path.join(outdir, name), SR, x.astype(np.float32))
write("music.wav", mus, 0.5); write("amb.wav", amb, 0.25); write("sfx.wav", sfx, 0.5)
print("wrote music/amb/sfx", DUR)

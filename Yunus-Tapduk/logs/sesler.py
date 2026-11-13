# Kodla müzik: sentez ney (Hicaz / Uşşak taksim) + dem (drone) + rebap benzeri yaylı + ambiyans + efekt
# -> kaynak/audio/music.wav, amb.wav, sfx.wav   (çalıştır: cd kaynak && python ../logs/sesler.py)
import numpy as np, json
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000; DUR = json.load(open('../video.json'))['sure']; N = int(SR * DUR); t = np.arange(N) / SR
W = json.load(open('words.json'))['words']; wt = lambda i: W[i]['s']; we = lambda i: W[i]['e']
r = np.random.default_rng(11)
bp = lambda x, lo, hi, o=2: sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x)
lp = lambda x, f, o=2: sosfilt(butter(o, f, fs=SR, output='sos'), x)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
def env_ad(L, a, rel):
    e = np.ones(L); na, nr = int(a * SR), int(rel * SR); e[:na] = np.linspace(0, 1, na) ** 1.5; e[-nr:] *= np.linspace(1, 0, nr) ** 1.2; return e
def ney_note(m, dur, prev=None, vel=1.0):
    L = int(dur * SR); tt = np.arange(L) / SR; f = np.full(L, hz(m))
    if prev is not None: g = int(min(0.12, dur * 0.2) * SR); f[:g] = np.linspace(hz(prev), hz(m), g)   # glissando
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.2 * tt) * np.clip((tt - 0.35) / 0.4, 0, 1)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    tone = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.07 * np.sin(3 * ph)
    breath = bp(r.standard_normal(L), hz(m) * 0.8, hz(m) * 3.5) * 0.9
    chiff = bp(r.standard_normal(L), 1500, 6000) * np.exp(-tt * 18) * 0.5
    e = env_ad(L, min(0.18, dur * 0.3), min(0.35, dur * 0.4))
    return ((tone * 0.75 + breath * 0.35 * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * tt))) * e + chiff) * vel
def taksim(t0, t1, scale, root, seed, density=1.0, vel=1.0):
    rr = np.random.default_rng(seed); out = np.zeros(N); x = t0; deg = 0; prev = None
    while x < t1 - 1.0:
        n_notes = rr.integers(3, 7)
        for k in range(n_notes):
            deg = int(np.clip(deg + rr.choice([-2, -1, -1, 1, 1, 2, 0]), -2, 9)); m = root + scale[deg % 7] + 12 * (deg // 7)
            d = rr.choice([0.45, 0.6, 0.9, 1.3]) if k < n_notes - 1 else rr.uniform(1.8, 3.2)
            if x + d > t1: break
            y = ney_note(m, d, prev, vel * rr.uniform(0.8, 1.0)); i = int(x * SR); j = min(N, i + len(y)); out[i:j] += y[:j - i]; prev = m; x += d * 0.92
        x += rr.uniform(0.8, 2.2) / density; deg = int(rr.choice([0, 0, 2, 4]))
    return out
HICAZ = [0, 1, 4, 5, 7, 8, 10]; USSAK = [0, 1.5, 3, 5, 7, 8, 10]
def drone(t0, t1, m, g=1.0, fade=2.0):
    out = np.zeros(N); i, j = int(t0 * SR), int(min(t1, DUR) * SR); L = j - i; tt = np.arange(L) / SR
    x = sum(np.sin(2 * np.pi * hz(m) * k * tt * (1 + 0.0007 * np.sin(2 * np.pi * 0.13 * tt + k))) / k ** 1.3 for k in range(1, 7))
    x = lp(x, 900) * env_ad(L, fade, fade); out[i:j] = x * g; return out
def strings(t0, t1, ms, g=1.0):
    out = np.zeros(N); i, j = int(t0 * SR), int(min(t1, DUR) * SR); L = j - i; tt = np.arange(L) / SR; x = np.zeros(L)
    for m in ms:
        for dt in (-0.004, 0.004):
            ph = 2 * np.pi * hz(m) * (1 + dt) * tt + 0.004 * np.sin(2 * np.pi * 4.8 * tt) * 40
            x += sum(np.sin(k * ph) / k for k in range(1, 9))
    x = lp(x, 2400) * env_ad(L, 3.0, 3.5); out[i:j] = x * g; return out
ir_t = np.arange(int(3.5 * SR)) / SR; IR = r.standard_normal(len(ir_t)) * np.exp(-ir_t * 1.9); IR = lp(IR, 5000); IR /= np.abs(IR).sum() ** 0.5 * 30
def verb(x, wet=0.35): return x * (1 - wet) + fftconvolve(x, IR)[:N] * wet * 6
B_T = wt(13); T3 = wt(56); Y3 = wt(73); T4 = wt(87); C = wt(105); CTA = wt(111); END = DUR
mus = np.zeros(N)
mus += drone(0.0, B_T + 0.2, 38, 0.5, 1.5)                                          # hook A: alçak dem
mus += verb(taksim(9.4, T3 - 0.2, HICAZ, 62, 3, 0.9, 0.55), 0.45)                    # S1: ney taksim (Hicaz)
mus += drone(9.0, T3, 50, 0.22, 2.0)
mus += drone(T3 - 0.3, we(72) + 3.5, 33, 0.9, 0.8)                                  # S2: gerilim bas
mus += verb(taksim(we(72) + 4.0, T4 - 2.0, USSAK, 60, 8, 0.6, 0.45), 0.55)           # S3: gurbet, seyrek ney
mus += drone(we(72) + 3.0, T4 - 1.0, 45, 0.25, 3.0)
mus += strings(T4 - 4.0, C - 0.5, [50, 57, 62, 66], 0.10)                           # S4-5: sıcak yaylı (rebap)
mus += verb(taksim(T4 - 3.5, C - 1.0, HICAZ, 62, 21, 0.9, 0.5), 0.5)
mus += strings(C - 1.0, END, [45, 52, 57, 61], 0.08)                                # C + Rûmî + kapanış
mus += verb(taksim(C + 3.2, END - 2.0, USSAK, 62, 34, 0.7, 0.4), 0.55)
g = np.ones(N); hole = (t > we(5)) & (t < wt(6)); g[hole] = 0.08                    # kanca A: sessizlik
g[(t > B_T - 0.35) & (t < B_T)] = 0.05; g[t > END - 2.5] *= np.clip((END - t[t > END - 2.5]) / 2.5, 0, 1)
g = sosfilt(butter(1, 6, fs=SR, output='sos'), g)
M = mus * g; M /= np.abs(M).max() + 1e-9
st = np.stack([M, np.roll(M, int(0.011 * SR))], 1).astype(np.float32)
wavfile.write('audio/music.wav', SR, st)
# ambiyans: dergâh odası (alçak uğultu) / rüzgâr+yağmur gurbet / sabah kuşları yok, hafif rüzgâr
n = r.standard_normal(N); room = lp(n, 220); wind = bp(r.standard_normal(N), 180, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.17 * t))
rain = bp(r.standard_normal(N), 1500, 9000); w_env = ((t > we(72)) & (t < T4 - 2)).astype(float); rn_env = ((t > we(72) + 6) & (t < Y3 + 9)).astype(float)
sm = lambda e: sosfilt(butter(1, 0.6, fs=SR, output='sos'), e)
A = room / np.abs(room).max() * (1 - sm(w_env)) + wind / np.abs(wind).max() * 1.3 * sm(w_env) + rain / np.abs(rain).max() * 0.7 * sm(rn_env)
wavfile.write('audio/amb.wav', SR, np.stack([A, np.roll(A, 300)], 1).astype(np.float32))
S = np.zeros(N)
def put(at, x, v=1.0): i = int(at * SR); j = min(N, i + len(x)); S[i:j] += x[:j - i] * v
L = int(1.8 * SR); tt = np.arange(L) / SR
hit = np.sin(2 * np.pi * (52 * tt - 8 * tt ** 2)) * np.exp(-tt * 2.6) + 0.35 * lp(r.standard_normal(L), 200) * np.exp(-tt * 10); hit /= np.abs(hit).max()
L = int(1.2 * SR); tt = np.arange(L) / SR
door = lp(r.standard_normal(L), 400) * np.exp(-tt * 9) * 2 + np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 6); door /= np.abs(door).max()
L = int(2.2 * SR); tt = np.arange(L) / SR
creak = np.sin(2 * np.pi * np.cumsum(260 + 90 * np.sin(2 * np.pi * 1.7 * tt) + 40 * r.standard_normal(L).cumsum() / L) / SR) * bp(r.standard_normal(L), 300, 2500) * np.exp(-((tt - 1.0) / 0.6) ** 2); creak /= np.abs(creak).max()
def logs(at):
    for k in range(5): L = int(0.25 * SR); tt = np.arange(L) / SR; x = bp(r.standard_normal(L), 300, 2500) * np.exp(-tt * 30); put(at + k * 0.09 + r.uniform(0, 0.05), x / np.abs(x).max(), 0.5)
put(B_T - 0.04, hit, 1.0); put(B_T + 0.05, door, 0.8)                                 # kanca B: gümleme
put(wt(13) - 6.37 + 0.0, hit, 0.0)
logs(wt(27) - 0.9)                                                                    # odunlar yere
put(wt(65) - 0.04, hit, 0.6)                                                          # "Hâlâ çiğsin!"
put(we(72) + 2.6, door, 0.9)                                                          # kapı kapanır
put(T4 - 2.4, creak, 0.5)                                                             # şafak, kapı açılır
L = int(2.5 * SR); tt = np.arange(L) / SR
bell = (np.sin(2*np.pi*196*tt) + 0.5*np.sin(2*np.pi*392*tt) + 0.25*np.sin(2*np.pi*589*tt)) * np.exp(-tt * 1.8); bell /= np.abs(bell).max()
put(C - 0.3, bell, 0.35); put(END - 4.6, bell, 0.4)
wavfile.write('audio/sfx.wav', SR, np.stack([S, S], 1).astype(np.float32))
print('ok', round(DUR, 1))

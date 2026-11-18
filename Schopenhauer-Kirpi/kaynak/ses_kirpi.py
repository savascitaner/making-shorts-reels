# Schopenhauer: Kirpi İkilemi — music bed (Chopin flute variations, PD), scene ambiences and picture-locked sfx.
# Writes audio/music.wav, audio/amb.wav, audio/sfx.wav (48 kHz stereo float). Then mixdown.py + master_audio.py.
import json, subprocess, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 48000; CFG = json.load(open('../video.json')); DUR = CFG['sure']; N = int(SR * DUR)
WD = json.load(open('words.json'))['words']
rng = np.random.default_rng(7)
def norm(s): return ''.join(c for c in s.lower().replace('İ', 'i').replace('I', 'ı') if c.isalnum() or c in "'çğıöşüâ")
def T(word, frm=0):
    n = norm(word)
    for i in range(frm, len(WD)):
        if norm(WD[i]['w']) == n: return WD[i]['s']
    raise SystemExit('word not found: ' + word)
def E(word, frm=0):
    n = norm(word)
    for i in range(frm, len(WD)):
        if norm(WD[i]['w']) == n: return WD[i]['e']
lp = lambda x, f: sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
hp = lambda x, f: sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
bp = lambda x, a, b: sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def S(t): return int(t * SR)
def env(n, a=0.01, r=0.2):
    e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR)); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def place(buf, t, x, pan=0.0, g=1.0):
    i = S(t); x = x[:max(0, N - i)]
    if i < 0 or len(x) == 0: return
    buf[i:i + len(x), 0] += x * g * np.sqrt(0.5 * (1 - pan)); buf[i:i + len(x), 1] += x * g * np.sqrt(0.5 * (1 + pan))
def noise(d): return rng.standard_normal(int(d * SR))

t15, tArt, tHak, tVe, tDon = T('Annesi'), T("Arthur'un"), T('Haklı'), T('Ve', 60), T('Dondurucu')
tBu, tOku, tBat, tAci, tKan = T('Bu', 20), T('okunacak.'), T('batar.'), T('Acıyla'), T('kanarlar.')
tMes, tIsi, tOna, tAma3, tYani, tSence, tDaha = T('mesafe', 100), T('Isınma'), T('Ona'), T('Ama', 135), T('Yani'), T('Sence'), T('Daha', 190)

# ---------- music: the recording from its start, faded, a gentle swell under the final cards ----------
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', '../ses/muzik-aday/chopin_flut.flac', '-ac', '2', '-ar', str(SR), '-t', str(DUR + 1), '-f', 'f32le', '-'], capture_output=True).stdout
m = np.frombuffer(pcm, np.float32).reshape(-1, 2).astype(np.float64)
mus = np.zeros((N, 2)); mus[:min(N, len(m))] = m[:N]
g = np.ones(N); g[:S(0.4)] = np.linspace(0.3, 1, S(0.4))
g[S(DUR - 2.5):] = np.linspace(1, 0, N - S(DUR - 2.5))
mus *= g[:, None]

# ---------- ambiences per scene (crossfaded) ----------
amb = np.zeros((N, 2))
def bed(t0, t1, x, g=1.0, fade=0.6):
    n = S(t1) - S(t0); x = np.resize(x, n) * env(n, fade, fade); place(amb, t0, x, 0, g)
def room(d): return lp(noise(d), 180) * 0.6
def murmur(d):
    x = bp(noise(d), 250, 1400); mod = 0.6 + 0.4 * np.abs(np.sin(np.linspace(0, d * 3.1, len(x)))) * (0.6 + 0.4 * np.sin(np.linspace(0, d * 1.3, len(x)))); return x * mod
def wind(d, f0=300, f1=900):
    x = bp(noise(d), f0, f1); mod = 0.55 + 0.45 * np.sin(np.linspace(0, d * 0.7, len(x)) + 1.3) * np.sin(np.linspace(0, d * 0.23, len(x))); return x * mod
def water(d): x = bp(noise(d), 120, 600); return x * (0.7 + 0.3 * np.sin(np.linspace(0, d * 2.2, len(x))))
def fire(d):
    x = lp(noise(d), 400) * 0.5; n = len(x)
    for _ in range(int(d * 9)):
        i = rng.integers(0, n - 2000); c = hp(noise(0.03), 1500) * np.exp(-np.linspace(0, 8, S(0.03))) * rng.uniform(0.6, 2.2); x[i:i + len(c)] += c
    return x
bed(0, t15 + 0.3, room(9), 0.9)
bed(t15 - 0.3, tArt + 0.3, murmur(12), 0.8)
bed(tArt - 0.3, tHak + 0.3, room(7), 0.8)
bed(tHak - 0.3, tVe + 0.3, water(12) * 0.8 + wind(12, 200, 600) * 0.5, 0.9)
bed(tVe - 0.3, tDon + 0.2, fire(7), 0.7)
bed(tDon - 0.2, tOna + 0.3, wind(tOna - tDon + 1), 1.0)
bed(tOna - 0.3, tAma3 + 0.3, fire(7) * 0.6, 0.6)
bed(tAma3 - 0.3, tYani + 0.3, fire(12), 0.9)
bed(tYani - 0.3, tDaha + 0.5, wind(tDaha - tYani + 1, 250, 700), 0.6)

# ---------- picture-locked sfx ----------
sfx = np.zeros((N, 2))
def thud(f=55, d=0.9):
    tt = np.linspace(0, d, S(d)); x = np.sin(2 * np.pi * f * tt * (1 - 0.3 * tt)) * np.exp(-tt * 5) + lp(noise(d), 300) * np.exp(-tt * 9) * 0.6; return x
def crackle(d=0.5, dens=120):
    x = np.zeros(S(d))
    for _ in range(int(d * dens)):
        i = rng.integers(0, len(x) - 400); c = hp(noise(0.008), 2500) * rng.uniform(0.3, 1.0); x[i:i + len(c)] += c
    return x * np.linspace(1, 0.2, len(x))
def whoosh(d=0.6):
    x = bp(noise(d), 400, 3000); return x * np.sin(np.linspace(0, np.pi, len(x))) ** 2
def chime(f=1318.5, d=2.2):
    tt = np.linspace(0, d, S(d)); return (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 3)) * np.exp(-tt * 2.2) * env(len(tt), 0.003, 0.3)
def scratch(d):
    x = bp(noise(d), 2000, 6000); strokes = (np.sin(np.linspace(0, d * 2 * np.pi * 3.2, len(x))) > 0.1).astype(float); return lp(strokes, 30) * x * 0.5
def tick():
    tt = np.linspace(0, 0.08, S(0.08)); return (np.sin(2 * np.pi * 2400 * tt) + bp(noise(0.08), 1500, 5000)) * np.exp(-tt * 70)
def swell(d=1.6):
    tt = np.linspace(0, d, S(d)); x = sum(np.sin(2 * np.pi * f * tt) for f in (220, 277.2, 329.6, 440)) * 0.25; return x * np.sin(np.linspace(0, np.pi, len(tt))) ** 1.5
place(sfx, 6.62, thud(48, 1.2), 0, 1.0)                               # the door, the 24 years
place(sfx, tBu, scratch(2.2), 0.2, 0.35)                              # her line in ink
place(sfx, tOku, thud(90, 0.5) * 0.6, 0, 0.7); place(sfx, tOku + 0.02, chime(1760, 1.6), 0, 0.25)   # gold leaf stamp
place(sfx, tDon - 0.45, whoosh(0.7), -0.4, 0.8); place(sfx, tDon - 0.4, crackle(0.5, 160), 0.3, 0.6)  # quill wipe
place(sfx, tBat + 0.05, thud(70, 0.6), 0, 0.9); place(sfx, tBat + 0.05, crackle(0.7, 220), 0, 0.9)  # quills touch
place(sfx, tAci, crackle(0.4, 160), 0.2, 0.6); place(sfx, tAci, whoosh(0.5), 0.5, 0.5)              # recoil apart
place(sfx, tKan + 0.15, thud(65, 0.6), 0, 0.9); place(sfx, tKan + 0.15, crackle(0.6, 220), -0.1, 0.9)
place(sfx, tMes, chime(1318.5), 0, 0.35)                              # the measuring line
place(sfx, tIsi + 0.6, chime(1568, 1.8), 0, 0.3)
for k in range(5):                                                    # pendulum: a tick at each extreme
    tk = tOna + (np.pi / 2 + k * np.pi) / 1.9
    if tk < tAma3: place(sfx, tk, tick(), -0.5 if k % 2 else 0.5, 0.45)
place(sfx, tYani - 0.2, swell(1.8), 0, 0.35)                          # the halo iris into the lone hedgehog

for name, x in (('music', mus), ('amb', amb), ('sfx', sfx)):
    wavfile.write(f'audio/{name}.wav', SR, x.astype(np.float32))
print('ok', DUR)

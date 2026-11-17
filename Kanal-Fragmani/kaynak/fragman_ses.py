"""Kanal fragmanı sesi: anlatım + Mahler Adagietto (son yükseliş, 534,5 sn'den) + alev motifi + sahne ambiyansları.
Çalıştır (proje kökünden):
  uv run -q --with numpy --with scipy python Kanal-Fragmani/kaynak/fragman_ses.py
Çıktı: kaynak/audio/mix.wav (48 kHz stereo); sonra master_audio.py ile -14 LUFS.
"""
import json, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
from sfx.synth import chime, whoosh, bandnoise  # noqa: E402

SR = 48000
CFG = json.load(open(os.path.join(HERE, "..", "video.json")))
DUR = CFG["sure"]
N = int(DUR * SR)
W = json.load(open(os.path.join(HERE, "words.json")))["words"]
FF = os.path.join(ROOT, "araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64/ffmpeg")
MUSIC_START = 530.5   # Mahler 5, IV: son yükseliş; doruk ~575-590 sn = fragmanda 44,5-59,5 sn


def load(path, start=0.0, dur=None):
    cmd = [FF, "-v", "error", "-ss", str(start), "-i", path] + (["-t", str(dur)] if dur else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32).reshape(-1, 2).copy()
    return a


def norm(w):
    return w.lower().replace("İ", "i").strip(".,:;?!“”'")


def ws(word, nth=1, nxt=None):
    n = 0
    for i, x in enumerate(W):
        if norm(x["w"]) == word and (nxt is None or (i + 1 < len(W) and norm(W[i + 1]["w"]) == nxt)):
            n += 1
            if n == nth:
                return x["s"]
    raise SystemExit("kelime yok: " + word)


def put(buf, t, mono, gain=1.0, pan=0.0):
    x = np.asarray(mono, dtype=np.float32) * gain
    i = int(t * SR)
    if i >= len(buf):
        return
    x = x[: len(buf) - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(x), 0] += x * l * 1.414
    buf[i:i + len(x), 1] += x * r * 1.414


def env(points, n=N):
    ts = np.array([p[0] for p in points]) * SR
    vs = np.array([p[1] for p in points])
    return np.interp(np.arange(n), ts, vs).astype(np.float32)


# --- anlatım ---
vo = load(os.path.join(HERE, "..", "ses", "vo.mp3"))[:N]
voice = np.zeros((N, 2), np.float32); voice[: len(vo)] = vo

# --- müzik: tek parça, ek yok ---
mu = load(os.path.join(HERE, "..", "ses", "muzik-aday", "mahler.ogg"), MUSIC_START, DUR + 0.5)[:N]
music = np.zeros((N, 2), np.float32); music[: len(mu)] = mu
# anlatım altında yumuşak ducking (RMS zarfı, 60 ms atak, 450 ms bırakma)
v = np.abs(voice[:, 0]); win = int(0.05 * SR)
rm = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, mode="same"))
on = (rm > 0.01).astype(np.float32)
sm = np.zeros_like(on); a_up, a_dn = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.45 * SR)); s = 0.0
for i in range(N):
    c = on[i]; s = (a_up if c > s else a_dn) * s + (1 - (a_up if c > s else a_dn)) * c; sm[i] = s
duck = 1.0 - 0.55 * sm   # konuşurken müzik ~ -7 dB
ride = env([(0, 0.55), (3.5, 0.75), (20, 0.9), (48, 1.0), (59.6, 1.15), (DUR - 2.5, 1.1), (DUR, 0.0)])  # kapanışta müzik öne
music *= (duck * ride)[:, None]

# --- alev motifi: her alev eşleme kesmesinde nefes (whoosh) + alçak çan (Fa majör) ---
sfx = np.zeros((N, 2), np.float32)
FLAME = [ws("ve"), ws("buda"), ws("spinoza"), ws("freud"), ws("jung"), ws("bu", 1, "kanal"), ws("abone")]
BELL = [[174.61, 349.23, 523.25], [220.0, 349.23, 523.25], [174.61, 261.63, 440.0]]
for n, t in enumerate(FLAME):
    tc = t - 0.15
    put(sfx, tc - 0.42, whoosh(0.62, 300, 2400, peak=0.75), 0.11, -0.15 + 0.05 * n)
    put(sfx, tc, chime(BELL[n % 3], dur=2.4, tau=0.9), 0.07 if n < 6 else 0.1)
# kancada göz açılırken çok alçak bir nefes
put(sfx, 0.0, whoosh(1.8, 120, 600, peak=0.6), 0.05)
# diğer geçişler: sis (Lao Tzu) yumuşak hava, karartmalar (Nietzsche, Avcıoğlu) kısa düşük nefes
put(sfx, ws("lao") - 0.6, whoosh(1.2, 900, 300, peak=0.5), 0.06, 0.3)
for w in ("nietzsche", "murat"):
    put(sfx, ws(w) - 0.5, whoosh(0.5, 1800, 200, peak=0.3), 0.07)

# --- ambiyans (sahne başına, ses tek bir mekânda) ---
amb = np.zeros((N, 2), np.float32)
rng = np.random.default_rng(5)


def bed(t0, t1, fc, q, gain, wob=0.0, pan=0.0):
    n = int((t1 - t0) * SR)
    if n <= 0:
        return
    x = np.array(bandnoise(n, lambda k: fc * (1 + wob * np.sin(k / SR * 0.7)), q), dtype=np.float32)
    x /= (np.abs(x).max() + 1e-9)
    f = np.minimum(1, np.minimum(np.arange(n) / (0.4 * SR), (n - np.arange(n)) / (0.4 * SR))).astype(np.float32)
    put(amb, t0, x * f, gain, pan)


T = {k: ws(k) - 0.15 for k in ("buda", "lao", "stoacılar", "deneyimci", "spinoza", "leibniz", "nietzsche", "freud", "adler", "jung", "murat")}
T["kanal"] = ws("bu", 1, "kanal") - 0.15; T["abone"] = ws("abone") - 0.15
bed(T["buda"], T["lao"], 3600, 1.4, 0.010, 0.05, 0.3)      # gece havası
bed(T["lao"], T["stoacılar"], 900, 0.7, 0.03, 0.2, -0.2)    # akan su
bed(T["stoacılar"], T["deneyimci"], 500, 0.6, 0.03, 0.4)    # rüzgâr
bed(T["deneyimci"], T["spinoza"], 160, 0.7, 0.02, 0.1)     # taş hücre, derin uğultu
bed(T["nietzsche"], T["freud"], 420, 0.5, 0.045, 0.6, 0.2)  # dağ rüzgârı
bed(T["murat"], T["kanal"], 300, 0.8, 0.012)                 # salon havası

mix = voice * 1.0 + music * 0.30 + sfx + amb
out = np.clip(mix, -1, 1)
os.makedirs(os.path.join(HERE, "audio"), exist_ok=True)
with wave.open(os.path.join(HERE, "audio", "mix.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("mix.wav", round(N / SR, 2), "sn; alev kesmeleri:", [round(t - 0.15, 2) for t in FLAME])

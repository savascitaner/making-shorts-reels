# 9:16 narration cut from the master, with every cut point moved to a real silence valley in the waveform.
# Whisper word times are approximate; cutting at them clipped words. Here each edge is searched in the audio.
# Usage: uv run --with numpy python cut916b.py   -> ../ses/vo-916.mp3 (+ report of every edge)
import json, subprocess, numpy as np
SR = 48000; HOP = int(0.005 * SR); WIN = int(0.02 * SR)
FF = "ffmpeg"
pcm = subprocess.run([FF, "-v", "error", "-i", "../ses/master-v4.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(pcm, np.float32).copy()
pcm2 = subprocess.run([FF, "-v", "error", "-i", "../ses/master-v4.mp3", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
X = np.frombuffer(pcm2, np.float32).reshape(-1, 2).copy()
def db_at(t):   # level of the 20 ms window centred at t
    i = int(t * SR); seg = x[max(0, i - WIN // 2): i + WIN // 2]; return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9) if len(seg) else -120
def valley(lo, hi, target, thr=-55.0):
    """quietest point in [lo,hi]; among points below thr prefer the one closest to target"""
    ts = np.arange(max(0, lo), hi, HOP / SR); lv = np.array([db_at(t) for t in ts])
    ok = np.where(lv < thr)[0]
    if len(ok): j = ok[np.argmin(np.abs(ts[ok] - target))]
    else: j = int(np.argmin(lv))
    return float(ts[j]), float(lv[j])
cuts = json.load(open("cuts916.json"))
# real silences in the master (level < -50 dB for >= 90 ms), from the waveform, not from whisper
step = 0.01; T = np.arange(0, len(x) / SR, step); L = np.array([db_at(t) for t in T]); quiet = L < -50
SIL = []; i = 0
while i < len(T):
    if quiet[i]:
        j = i
        while j < len(T) and quiet[j]: j += 1
        if (j - i) * step >= 0.09: SIL.append((T[i], T[j - 1]))
        i = j
    else: i += 1
segs = []; rep = []
for k, (s, e) in enumerate(cuts):
    # start: the silence whose END is nearest the first word (whisper may be early or late)
    a = min(SIL, key=lambda q: abs(q[1] - s)); st = max(a[0], a[1] - 0.05)
    if k == 0: st, a = 0.0, (0.0, s)   # master opens straight on the hook: no silence before it
    # end: the silence whose START is nearest the last word
    b = min(SIL, key=lambda q: abs(q[0] - e)); en = min(b[1], b[0] + 0.15)   # keep 150 ms after the tail falls under -50 dB: soft endings (ş, s, r) decay slowly
    segs.append((st, en)); rep.append((k + 1, s, st, db_at(st), e, en, db_at(en), abs(a[1] - s), abs(b[0] - e)))
# assemble: 0.25 s lead, natural gap capped to [0.35, 0.85] s, 30 ms equal-power crossfade edges
FADE = int(0.04 * SR)
out = [np.zeros((int(0.25 * SR), 2), np.float32)]
prev_en = None
for (st, en), (s, e) in zip(segs, cuts):
    if prev_en is not None:
        gap = min(max(st - prev_en, 0.35), 0.85); out.append(np.zeros((int(gap * SR), 2), np.float32))
    seg = X[int(st * SR): int(en * SR)].copy()
    ramp = np.sin(np.linspace(0, np.pi / 2, FADE)) ** 2
    seg[:FADE] *= ramp[:, None]; seg[-FADE:] *= ramp[::-1][:, None]
    out.append(seg); prev_en = en
y = np.concatenate(out)
subprocess.run([FF, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "libmp3lame", "-b:a", "192k", "../ses/vo-916.mp3"], input=y.tobytes())
print("edge report (dB at the chosen cut point; speech is about -21 dB, silence about -86 dB):")
bad = 0
for k, s, st, lst, e, en, len_, ds, de in rep:
    fl = ("  <-- start not in silence" if lst > -50 else "") + ("  <-- end not in silence" if len_ > -50 else "") + ("  <-- far from word (check)" if max(ds, de) > 0.6 else "")
    bad += (lst > -50) + (len_ > -50)
    print(f"{k:2d} start {s:7.2f}->{st:7.2f} ({lst:6.1f} dB, {ds:.2f}s)   end {e:7.2f}->{en:7.2f} ({len_:6.1f} dB, {de:.2f}s){fl}")
print("edges not in silence:", bad, "| total", round(len(y) / SR, 2), "s")

"""Shorts kesimi: senaryodaki **[S]** paragraflari, tek ana kayittan (audio/vo.wav) kesilir.
Cumleyi bulmak icin kelime sirasi, KESMEK icin dalga bicimindeki gercek sessizlik (-50 dB alti >=90 ms) kullanilir.
Cikti: audio/vo-kisa.wav, short.js (window.SHORTCUT = {segs:[[uzunBas, uzunSon, kisaBas],...], dur, sub})"""
import json, re, subprocess, numpy as np

SR = 48000
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "audio/vo.wav", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
HOP = 480  # 10 ms
db = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(HOP) / HOP, "same")[::HOP]) + 1e-9)
quiet = db < -50

def silence_runs():
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            if (j - i) >= 9: runs.append((i * 0.01, j * 0.01))
            i = j
        else: i += 1
    return runs
RUNS = silence_runs()

def gap(e_prev, s_next):
    """iki kelime arasindaki gercek duraklama: pencere icindeki en uzun sessizlik (-50 dB, >=50 ms)."""
    lo, hi = e_prev - 0.6, s_next + 0.6
    i0, i1 = max(0, int(lo * 100)), min(len(quiet), int(hi * 100)); best, i = None, i0
    while i < i1:
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            if j - i >= 5 and (best is None or j - i > best[1] - best[0]): best = (i, j)
            i = j
        else: i += 1
    if best: return best[0] * 0.01, best[1] * 0.01
    k = (int(e_prev * 100) + int(np.argmin(db[int(e_prev * 100):max(int(s_next * 100), int(e_prev * 100) + 1)]))) * 0.01
    return k, k
def cut_start(t, prev_e):
    if prev_e is None: return 0.0
    s, e = gap(prev_e, t); return max(s, e - 0.06)
def cut_end(t, next_s):
    if next_s is None: return len(x) / SR
    s, e = gap(t, next_s); return min(s + 0.15, e)

W = json.load(open("words.json"))["words"]
md = open("../Sol-Beyin-Ego-senaryo.md").read()
body = md.split("## SAHNE 1")[1].split("(Kapanış kartları")[0]
paras = [l for l in body.split("\n")[1:] if l.strip() and not l.startswith("## ")]
n = 0; marks = []
for p in paras:
    k = len(re.sub(r"\[[^\]]*\]", "", p.replace("**[S]**", "")).replace('"', "").split())
    marks.append((n, n + k - 1, "**[S]**" in p)); n += k
assert n == len(W), (n, len(W))
segs = []
for a, b, s in marks:
    if not s: continue
    if segs and segs[-1][1] == a - 1: segs[-1][1] = b
    else: segs.append([a, b])

GAP = 0.25; FADE = 0.04
out, cuts, ss = [], [], 0.0
for a, b in segs:
    ls = cut_start(W[a]["s"], W[a - 1]["e"] if a > 0 else None); le = cut_end(W[b]["e"], W[b + 1]["s"] if b + 1 < len(W) else None)
    seg = x[int(ls * SR):int(le * SR)].copy(); f = int(FADE * SR)
    seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    if out: out.append(np.zeros(int(GAP * SR), np.float32)); ss += GAP
    cuts.append([round(ls, 3), round(le, 3), round(ss, 3)]); out.append(seg); ss += le - ls
y = np.concatenate(out)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", "audio/vo-kisa.wav"], input=y.tobytes())
dur = len(y) / SR
# abone animasyonu: ~80 sn civarinda, bir cumle bitisine denk
sub = min((c[2] for c in cuts if c[2] > 70), key=lambda v: abs(v - 80), default=80)
open("short.js", "w").write("window.SHORTCUT=" + json.dumps({"segs": cuts, "dur": round(dur, 3), "sub": sub}) + ";")
print(len(cuts), "kesit, kisa sure", round(dur, 1), "sn, abone", sub)
for (a, b), c in zip(segs, cuts): print(c, " ".join(w["w"] for w in W[a:a + 4]), "...", " ".join(w["w"] for w in W[b - 2:b + 1]))

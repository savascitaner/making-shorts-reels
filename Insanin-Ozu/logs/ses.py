# Ses: müzik düzeni (Gnossienne → Sarabande → Gymnopédie) + zar geçiş sesleri + seslendirme miksi. Kullanım: python ses.py w|t
import sys, re, json, subprocess, numpy as np
sys.path.insert(0, '/Users/claude-eng/Shorts - Reels')
from sfx import synth
AR = sys.argv[1]; SR = 48000
FF = "/Users/claude-eng/Shorts - Reels/araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64/ffmpeg"
K = '/Users/claude-eng/Shorts - Reels/Insanin-Ozu/kaynak/'
def load(p, ch=2):
    raw = subprocess.run([FF, '-v', 'error', '-i', p, '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()
norm = lambda s: re.sub(r'[^\w]', '', s.lower().replace('İ', 'i').replace('I', 'ı'))
LW = json.load(open(K + 'words.json'))['words']; LN = [norm(w['w']) for w in LW]
if AR == 't':
    D = json.loads(open(K + 'words-r.js').read()[len('window.DATA='):-1])
else:
    D = dict(words=[dict(w, o=i) for i, w in enumerate(LW)], duration=json.load(open(K + 'words.json'))['duration'], segs=[])
WD = D['words']; LOC = {w['o']: w['s'] for w in WD}
def find(ph, frm=0):
    p = [norm(x) for x in ph.split()]
    for i in range(frm, len(LN) - len(p) + 1):
        if LN[i:i + len(p)] == p: return i
    raise SystemExit('çapa yok: ' + ph)
# motorun çekim listesini oku (index.html SH)
src = open(K + 'index.html').read()
SH = re.findall(r"\['([\w]+)', '([^']+)', \[[^\]]*\], (?:'\w+'|null), (null|'\w+'|\[[^\]]*\])\]", src)
allS, frm = [], 0
for k, ph, card in SH: o = find(ph, frm); frm = o; allS.append(dict(k=k, o=o, sec=card.startswith("['I") or card.startswith("['V") ))
segA = [g['a'] for g in D.get('segs', [])]; shots = []
for n, s in enumerate(allS):
    t0 = LOC.get(s['o'])
    if t0 is None:
        nx = allS[n + 1]['o'] if n + 1 < len(allS) else 10**9; g = [a for a in segA if s['o'] < a < nx]
        if not g: continue
        t0 = LOC[g[0]]
    shots.append(dict(s, t0=0 if n == 0 else t0 - 0.15))
shots.sort(key=lambda x: x['t0'])
def kind(i):
    s = shots[i]
    if i == 0: return None
    if s['sec']: return 'zar'
    if s['k'] == shots[i - 1]['k']: return 'kesme'
    return ['cozul', 'zar', 'cozul', 'kesme'][i % 4]
vo = load(K + ('audio/vo-r.wav' if AR == 't' else 'audio/vo.wav'), 1)[:, 0]
DUR = len(vo) / SR + (1.6 + 5.6 if AR == 'w' else 1.2 + 2.3); N = int(DUR * SR)
out = np.zeros((N, 2), np.float32)
# --- müzik düzeni ---
M = '/Users/claude-eng/Shorts - Reels/Insanin-Ozu/ses/muzik/'
gn, sa, gy = load(M + 'satie-gnossienne-1.ogg'), load(M + 'bach-cello-sarabande.ogg'), load(M + 'satie-gymnopedie-1.ogg')
def rms_norm(x): return x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * 0.05
gn, sa, gy = rms_norm(gn), rms_norm(sa) * 0.9, rms_norm(gy)
act2 = LOC.get(find('Yirminci yüzyılda')) if AR == 'w' else LOC.get(find('Junga göre bu'))
X = 5.0  # çapraz geçiş
bed = np.zeros((N, 2), np.float32)
def place(x, start, end, fin, fout):
    a, b = int(start * SR), min(N, int(end * SR)); x = x[:b - a]; L = len(x)
    env = np.ones(L, np.float32); fi, fo = int(fin * SR), int(fout * SR)
    if fi: env[:fi] = np.linspace(0, 1, fi) ** 0.8
    if fo and L > fo: env[-fo:] = np.linspace(1, 0, fo) ** 0.8
    bed[a:a + L] += x * env[:, None]
place(gn, 0.0, act2 + 1.0, 0.0, X)
s2 = act2 + 1.0 - X; e2 = s2 + len(sa) / SR
if AR == 'w':
    place(sa, s2, e2, X, X); place(gy, e2 - X, DUR, X, 3.0)
else:
    place(sa, s2, DUR, X, 3.0)
# --- konuşma altında yumuşak alçalma (ani değil: 1,2 sn rampalar) ---
speech = np.zeros(N, np.float32)
for w in WD: speech[int(max(0, w['s'] - 0.25) * SR):int((w['e'] + 0.35) * SR)] = 1
k = int(1.2 * SR); ker = np.ones(k, np.float32) / k
sm = np.convolve(speech, ker, mode='same'); sm = np.convolve(sm, ker, mode='same')
gain = 10 ** ((-17.0 * sm + -9.0 * (1 - sm)) / 20)          # konuşurken -17 dB, aralarda -9 dB (müzik değil, oran)
endT = LOC.get(find('Daha fazlası'));
if endT: ramp = np.clip((np.arange(N) / SR - endT) / 2.5, 0, 1); gain = gain * (1 + 0.6 * ramp)
out += bed * gain[:, None]
# --- zar geçiş sesleri (yumuşak, alçak) ---
rng = np.random.default_rng(7)
for i in range(len(shots)):
    kd = kind(i); t = shots[i]['t0']
    if kd != 'zar': continue
    w = np.asarray(synth.whoosh(1.4, 180, 900, peak=0.45, q=0.7), np.float32)
    if w.ndim == 1: w = np.stack([w, w], 1)
    w *= 10 ** ((-25 if not shots[i]['sec'] else -21) / 20) / (np.abs(w).max() + 1e-9)
    a = int(max(0, t - 0.1) * SR); L = min(len(w), N - a); pan = rng.uniform(-0.3, 0.3)
    out[a:a + L, 0] += w[:L, 0] * (1 - pan); out[a:a + L, 1] += w[:L, 1] * (1 + pan)
# --- seslendirme ---
out[:len(vo)] += vo[:, None] * 1.0
fade = int(1.4 * SR); out[-fade:] *= np.linspace(1, 0, fade)[:, None]
import wave
pk = np.abs(out).max(); out = out / max(1.0, pk / 0.95)
fn = K + ('audio/mix-r.wav' if AR == 't' else 'audio/mix.wav')
with wave.open(fn, 'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((out * 32767).astype('<i2').tobytes())
print(AR, 'çekim', len(shots), 'zar', sum(1 for i in range(len(shots)) if kind(i) == 'zar'), 'süre', round(DUR, 2), 'perde2', round(act2, 1))

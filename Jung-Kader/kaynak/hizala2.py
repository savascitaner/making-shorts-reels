# Whisper kelime zamanlarını senaryonun birebir yazımına oturtur (TDK yazımı, "bilinçdışı", "Jung").
# Kullanım: python3 hizala2.py reels|16x9 [kayma_kurallari.json]
import json, re, sys, difflib
F = sys.argv[1]
KONU = "Jung-Kader"
raw = json.load(open(f"words-raw-{F}.json"))
# yama zaman haritası: [[eski_sn, yeni_sn], ...] parça parça doğrusal; son düğümden sonra eğim 1 (yama-<F>.json)
try: KN = json.load(open(f"yama-{F}.json"))
except FileNotFoundError: KN = []
def tmap(t):
    if not KN: return t
    P = [[0.0, 0.0]] + KN
    for (x0, y0), (x1, y1) in zip(P, P[1:]):
        if t <= x1: return y0 + (t - x0) * (y1 - y0) / max(1e-9, x1 - x0)
    return P[-1][1] + t - P[-1][0]
for w in raw: w["s"], w["e"] = tmap(w["s"]), tmap(w["e"])
# apostrof parçalarını birleştir
ww = []
for x in raw:
    if x["w"].startswith("'") and ww: ww[-1]["w"] += x["w"]; ww[-1]["e"] = x["e"]
    else: ww.append(dict(x))
txt = open(f"../ses/metin-{F}.txt").read()
txt = txt.replace("Yunga", "Jung'a").replace("Yungun", "Jung'un").replace("Yung", "Jung")
script = txt.split()
norm = lambda s: re.sub(r"[^a-zçğıöşüâîû0-9]", "", s.lower().replace("'", "").replace("’", "").replace("İ", "i").replace("I", "ı"))
A = [norm(w["w"]) for w in ww]; B = [norm(s) for s in script]
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
out = [None] * len(script)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1): out[j1 + k] = (ww[i1 + k]["s"], ww[i1 + k]["e"])
    elif i2 > i1:  # replace: whisper kelimelerinin zaman aralığını senaryo kelimelerine harf oranıyla dağıt
        s0, e0 = ww[i1]["s"], ww[i2 - 1]["e"]; L = [max(1, len(B[j])) for j in range(j1, j2)]; tot = sum(L); c = s0
        for n, j in enumerate(range(j1, j2)):
            d = (e0 - s0) * L[n] / tot; out[j] = (c, c + d); c += d
# boşlukları komşulardan doldur
for j in range(len(out)):
    if out[j] is None:
        p = next((out[k][1] for k in range(j - 1, -1, -1) if out[k]), 0.0)
        n = next((out[k][0] for k in range(j + 1, len(out)) if out[k]), p + 0.3)
        out[j] = (p, max(p + 0.05, min(n, p + 0.4)))
W = [{"w": s, "s": round(a, 3), "e": round(b, 3)} for s, (a, b) in zip(script, out)]
EMPH = {"kader", "kaderi", "kaderin", "kader,", "bilinçdışı", "hakikatin", "ölçü", "sensin", "değerli", "güvende", "Muhatap"}
for x in W: x["em"] = 1 if norm(x["w"]) in {norm(e) for e in EMPH} else 0
chunks, cur = [], []
for i, x in enumerate(W):
    cur.append(i); t = " ".join(W[j]["w"] for j in cur); nx = W[i + 1] if i + 1 < len(W) else None
    if x["w"][-1] in ".,?!:;\"”" or nx is None or nx["s"] - x["e"] > 0.45 or len(cur) >= 3 or len(t) >= 16: chunks.append(cur); cur = []
D = dict(words=W, chunks=chunks, vo_end=W[-1]["e"])
open(f"words-{F}.js", "w").write("window.DATA=" + json.dumps(D, ensure_ascii=False) + ";")
json.dump(D, open(f"words-{F}.json", "w"), ensure_ascii=False, indent=0)
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h:02}:{m:02}:{int(s):02},{min(999,int(round((s%1)*1000))):03}"
name = f"{KONU}-Reels-altyazi.srt" if F == "reels" else f"{KONU}-altyazi.srt"
import os; os.makedirs(f"../../outputs/{KONU}", exist_ok=True)
with open(f"../../outputs/{KONU}/{name}", "w") as f:
    for n, c in enumerate(chunks, 1):
        s = W[c[0]]["s"]; e = W[c[-1]]["e"]
        if n < len(chunks): e = min(max(e, s + 0.5), W[chunks[n][0]]["s"])
        f.write(f"{n}\n{ts(s)} --> {ts(e)}\n{' '.join(W[j]['w'].strip(chr(34)) for j in c)}\n\n")
bad = [(o[0], o[1], i1, i2, j1, j2) for o in [x for x in sm.get_opcodes() if x[0] != "equal"] for (_, i1, i2, j1, j2) in [o]]
print(len(W), "kelime", len(chunks), "parça, son", W[-1]["e"], "eşleşmeyen", len([b for b in sm.get_opcodes() if b[0] != "equal"]))
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal": print(" ", tag, [w["w"] for w in ww[i1:i2]], "->", script[j1:j2])

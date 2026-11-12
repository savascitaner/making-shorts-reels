# Snap Whisper word boundaries to real pauses: every silence >= 0.2 s is assigned to the nearest word boundary
# (preferring boundaries after punctuation), prev word ends at silence start, next word starts at silence end.
import json, subprocess, numpy as np, os, re
K = os.path.dirname(os.path.abspath(__file__)); VO = os.path.join(os.path.dirname(K), "ses", "Doga-tam.wav")
pcm = subprocess.run(["ffmpeg","-v","error","-i",VO,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
a = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
db = 20*np.log10(np.sqrt(np.convolve(a**2, np.ones(400)/400, "same")[::160] + 1e-12))
sil = db < -60; S = []; k = 0
while k < len(sil):
    if sil[k]:
        j = k
        while j < len(sil) and sil[j]: j += 1
        if j - k >= 20: S.append((k / 100, j / 100))
        k = j
    else: k += 1
D = json.load(open(os.path.join(K, "words.json"))); W = D["words"]; used = set(); n = 0
for s0, s1 in S:
    if s0 < 0.05 or s1 > len(sil) / 100 - 0.05: continue
    best = None
    for i in range(len(W) - 1):
        if i in used: continue
        t = (W[i]["e"] + W[i + 1]["s"]) / 2
        d = 0 if s0 <= t <= s1 else min(abs(t - s0), abs(t - s1))
        if d > 1.5: continue
        score = d - (0.6 if re.search(r"[.,:;?!\"”]$", W[i]["w"]) else 0)
        if best is None or score < best[0]: best = (score, i)
    if best:
        i = best[1]; used.add(i); n += 1
        W[i]["e"] = round(min(max(W[i]["s"] + 0.1, s0 + 0.05), s1), 3); W[i + 1]["s"] = round(max(s1 - 0.05, W[i]["e"]), 3)
        if W[i + 1]["e"] < W[i + 1]["s"] + 0.1: W[i + 1]["e"] = round(W[i + 1]["s"] + 0.15, 3)
for i in range(1, len(W)):   # keep monotonic
    if W[i]["s"] < W[i - 1]["e"]: W[i]["s"] = W[i - 1]["e"]
    if W[i]["e"] < W[i]["s"]: W[i]["e"] = W[i]["s"] + 0.05
json.dump(D, open(os.path.join(K, "words.json"), "w"), ensure_ascii=False, indent=0)
print("silences", len(S), "snapped", n)

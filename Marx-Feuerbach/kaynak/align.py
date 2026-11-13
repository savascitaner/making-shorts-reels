import json, re
CFG = json.load(open("../video.json")); KONU = CFG["konu"]
w = json.load(open("words-raw.json"))
out = []
for x in w:
    if x["w"].startswith("'") and out: out[-1]["w"] += x["w"]; out[-1]["e"] = x["e"]
    else: out.append(dict(x))
fix = CFG["duzelt"]
for x in out:
    x["w"] = fix.get(x["w"], x["w"])
for k, v in CFG.get("idx_duzelt", {}).items(): out[int(k)]["w"] = v
# word times measured from the waveform: {"w": "patlar.", "yeni": "patlar!", "s": 6.4, "e": 7.1}
for z in CFG["zaman_duzelt"]:
    for x in out:
        if x["w"] == z["w"]: x["w"] = z.get("yeni", x["w"]); x["s"], x["e"] = z["s"], z["e"]; break
EMPH = set(CFG["vurgu"])
for x in out: x["em"] = 1 if re.sub(r"[“”.,?!:;']|'.*", "", x["w"]) in EMPH else 0
chunks, cur = [], []
for i, x in enumerate(out):
    cur.append(i); txt = " ".join(out[j]["w"] for j in cur); nxt = out[i + 1] if i + 1 < len(out) else None
    if x["w"][-1] in ".,?!:;”" or nxt is None or nxt["s"] - x["e"] > 0.45 or len(cur) >= 3 or len(txt) >= 15: chunks.append(cur); cur = []
DUR = CFG["sure"]
D = dict(words=out, chunks=chunks, bounds=[], duration=DUR, boom=CFG["boom"])
json.dump(D, open("words.json", "w"), ensure_ascii=False, indent=0)
open("words.js", "w").write("window.DATA=" + json.dumps(D, ensure_ascii=False) + ";")
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h:02}:{m:02}:{int(s):02},{min(999,int(round((s%1)*1000))):03}"
with open(f"../../outputs/{KONU}/{KONU}-altyazi.srt", "w") as f:
    for n, c in enumerate(chunks, 1):
        s = out[c[0]]["s"]; e = out[c[-1]]["e"]
        if n < len(chunks): e = min(max(e, s + 0.5), out[chunks[n][0]]["s"])
        f.write(f"{n}\n{ts(s)} --> {ts(e)}\n{' '.join(out[j]['w'] for j in c)}\n\n")
print(len(out), "words", len(chunks), "chunks")
print(" ".join(f"{i}:{x['w']}" for i, x in enumerate(out)))

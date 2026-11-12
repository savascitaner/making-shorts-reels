# Script text (Doga-Filozoflari-senaryo.md) <-> Whisper words (words-raw.json) -> words.json
# Caption spelling comes from the script; timing from Whisper. Each word gets sec (1-9), par, sent.
import json, re, difflib, os
K = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(K)
md = open(os.path.join(R, "Doga-Filozoflari-senaryo.md")).read().split("\n---")[1]
toks = []
for sec in re.split(r"\n## BÖLÜM ", md)[1:]:
    head, *body = sec.split("\n"); n = int(head.split(":")[0])
    pars = [p.strip().replace("**", "") for p in body if p.strip() and not p.strip().startswith("_")]
    sent = 0
    for pi, p in enumerate(pars):
        for w in p.split():
            toks.append({"w": w, "sec": n, "par": pi, "sent": sent})
            if re.search(r"[.?!][\"”]?$", w) and not w.endswith("..."): sent += 1
        if not re.search(r"[.?!][\"”]?$", p): sent += 1
raw = json.load(open(os.path.join(K, "words-raw.json")))
def norm(s):
    s = s.replace("İ", "i").replace("I", "ı").lower()
    return re.sub(r"[^\wçğıöşüâîû]", "", s)
A = [norm(t["w"]) for t in toks]; B = [norm(x["w"]) for x in raw]
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1): toks[i1 + k]["s"], toks[i1 + k]["e"] = raw[j1 + k]["s"], raw[j1 + k]["e"]
    elif tag == "replace" and j2 > j1:
        s0, e0 = raw[j1]["s"], raw[j2 - 1]["e"]; n = i2 - i1
        for k in range(n):
            toks[i1 + k]["s"] = round(s0 + (e0 - s0) * k / n, 3); toks[i1 + k]["e"] = round(s0 + (e0 - s0) * (k + 1) / n, 3)
        if norm("".join(B[j1:j2])) != norm("".join(A[i1:i2])): print("REPL", A[i1:i2], "<-", B[j1:j2])
    elif tag == "insert": print("EXTRA in audio", B[j1:j2])
    elif tag == "delete": print("MISSING in audio", A[i1:i2])
# interpolate any unmatched
for i, t in enumerate(toks):
    if "s" not in t:
        p = next(toks[j]["e"] for j in range(i - 1, -1, -1) if "e" in toks[j]) if i else 0.0
        q = next((toks[j]["s"] for j in range(i + 1, len(toks)) if "s" in toks[j]), p + 0.4)
        t["s"], t["e"] = p, q
for t in toks: t["s"] = float(t["s"]); t["e"] = float(t["e"])
json.dump({"words": toks}, open(os.path.join(K, "words.json"), "w"), ensure_ascii=False, indent=0)
print(len(toks), "script words,", len(raw), "whisper words; ratio", round(sm.ratio(), 3), "last", toks[-1])

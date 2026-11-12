# Clean whisper words -> words.json (+ sections, caption chunks, emphasis) and the .srt
import json, re
w = json.load(open("words-raw.json"))
out = []
for x in w:                                   # glue Turkish suffixes: Üniversitesi 'nde -> Üniversitesi'nde
    if x["w"].startswith("'") and out: out[-1]["w"] += x["w"]; out[-1]["e"] = x["e"]
    else: out.append(dict(x))
fix = {"dahi.": "dâhi.", "Salome,": "Salomé,", "fatih.": "fati.", "hala": "hâlâ", "mıydım?": "mıydın?", "Sonra,": "Sonra", "Belki": "belki",
       "Sessizlik": "sessizlik", "boyunca,": "boyunca", "nazilerin": "Nazilerin", "ki,": "ki:", "Bu": "Bu", "Torino": "Torino."}
for i, x in enumerate(out):
    if x["w"] in fix and not (x["w"] == "Torino" and i > 5): x["w"] = fix[x["w"]]
    if x["w"] == "1889": x["w"] = "1889."
    if x["w"] == "adam" and i < 8: x["w"] = "adam,"
    if x["w"] == "Tanrı" and i < 25: x["w"] = "“Tanrı"
    if x["w"] == "öldü" and i < 25: x["w"] = "öldü”"
# sections: first word index of each part
def idx(word, after=0): return next(i for i, x in enumerate(out) if x["w"].strip("“”.,?!") == word and i >= after)
starts = [0, idx("Geri"), idx("Ama", 50), idx("Tanrı", 100), idx("Sonra", 140), idx("Ve", 180)]
for si, st in enumerate(starts):
    end = starts[si + 1] if si + 1 < len(starts) else len(out)
    for x in out[st:end]: x["scene"] = si + 1
bounds = [round(out[i]["s"] - 0.2, 2) for i in starts[1:]]
EMPH = {"Torino", "1889", "atın", "ağladı", "Tanrı", "öldü", "Nietzsche", "dâhi", "kör", "40", "7", "Lou", "Salomé", "reddeder",
        "öldürdük", "uyarıydı", "Hiçliğe", "anlamını", "cin", "sonsuz", "Amor", "fati", "Kaderini", "sev", "sessizlik", "çarpıttı",
        "Nazilerin", "yaşıyor", "yaşar", "korkunç", "ihanet", "yalnızlığıyla", "tek", "başına"}
for x in out: x["em"] = 1 if re.sub(r"[“”.,?!:;']|'.*", "", x["w"]) in EMPH else 0
# caption chunks: <= 3 words / <= 16 chars, break after punctuation or pause or section change
chunks, cur = [], []
for i, x in enumerate(out):
    cur.append(i)
    txt = " ".join(out[j]["w"] for j in cur)
    nxt = out[i + 1] if i + 1 < len(out) else None
    brk = (x["w"][-1] in ".,?!:;”" or nxt is None or nxt["s"] - x["e"] > 0.45 or len(cur) >= 3 or len(txt) >= 15
           or (nxt and nxt.get("scene") != x.get("scene")))
    if brk: chunks.append(cur); cur = []
DUR = 141.0
json.dump(dict(words=out, chunks=chunks, bounds=bounds, duration=DUR), open("words.json", "w"), ensure_ascii=False, indent=0)
open("words.js", "w").write("window.DATA=" + json.dumps(dict(words=out, chunks=chunks, bounds=bounds, duration=DUR), ensure_ascii=False) + ";")
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h:02}:{m:02}:{int(s):02},{min(999,int(round((s%1)*1000))):03}"
with open("../teslim/Nietzsche-altyazi.srt", "w") as f:
    for n, c in enumerate(chunks, 1):
        s = out[c[0]]["s"]; e = out[c[-1]]["e"]
        if n < len(chunks): e = min(max(e, s + 0.5), out[chunks[n][0]]["s"])
        f.write(f"{n}\n{ts(s)} --> {ts(e)}\n{' '.join(out[j]['w'] for j in c)}\n\n")
print(len(out), "words,", len(chunks), "chunks; bounds", bounds)
print([ (i, out[i]['w']) for i in starts])

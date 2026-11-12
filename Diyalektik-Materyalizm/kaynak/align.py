import json, re
w = json.load(open("words-raw.json"))
out = []
for x in w:
    if x["w"].startswith("'") and out: out[-1]["w"] += x["w"]; out[-1]["e"] = x["e"]
    else: out.append(dict(x))
fix = {"hala": "hâlâ", "içinde.": "için de.", "Diyamat": "Diamat", "resmi": "resmî", "Burjuva": "burjuva", "Genetik,": "Genetik", "onu,": "onu"}
for x in out:
    x["w"] = fix.get(x["w"], x["w"])
# measured from waveform: "ve patlar!" is 6.1-7.1 s
for x in out:
    if x["w"] == "ve" and x["s"] < 6: x["s"], x["e"] = 6.1, 6.35
    if x["w"] == "patlar.": x["w"] = "patlar!"; x["s"], x["e"] = 6.4, 7.1
EMPH = {"99", "patlar", "seçmiyorsun", "nicelikten", "niteliğe", "Hegel'di", "tersine", "baş", "aşağı", "ayakları", "üstüne", "El", "Buhar", "değirmeni",
        "bilinci", "belirlemez", "Toplumsal", "belirler", "sen", "telefon", "Diamat", "burjuva", "Popper", "sınamaz", "Filozoflar", "değiştirmektir", "Yorumlara"}
for x in out: x["em"] = 1 if re.sub(r"[“”.,?!:;']|'.*", "", x["w"]) in EMPH else 0
chunks, cur = [], []
for i, x in enumerate(out):
    cur.append(i); txt = " ".join(out[j]["w"] for j in cur); nxt = out[i + 1] if i + 1 < len(out) else None
    if x["w"][-1] in ".,?!:;”" or nxt is None or nxt["s"] - x["e"] > 0.45 or len(cur) >= 3 or len(txt) >= 15: chunks.append(cur); cur = []
DUR = 124.0
D = dict(words=out, chunks=chunks, bounds=[], duration=DUR)
json.dump(D, open("words.json", "w"), ensure_ascii=False, indent=0)
open("words.js", "w").write("window.DATA=" + json.dumps(D, ensure_ascii=False) + ";")
def ts(t): h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h:02}:{m:02}:{int(s):02},{min(999,int(round((s%1)*1000))):03}"
with open("../../outputs/Diyalektik-Materyalizm/Diyalektik-Materyalizm-altyazi.srt", "w") as f:
    for n, c in enumerate(chunks, 1):
        s = out[c[0]]["s"]; e = out[c[-1]]["e"]
        if n < len(chunks): e = min(max(e, s + 0.5), out[chunks[n][0]]["s"])
        f.write(f"{n}\n{ts(s)} --> {ts(e)}\n{' '.join(out[j]['w'] for j in c)}\n\n")
print(len(out), "words", len(chunks), "chunks")
print(" ".join(f"{i}:{x['w']}" for i, x in enumerate(out)))

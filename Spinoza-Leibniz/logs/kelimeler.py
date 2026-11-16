# Birleşik vo'nun kelime zamanlarını, iki kaydın ayrı (eksiksiz) transkriptlerinden parça kaydırmasıyla kurar.
import json, os
os.chdir(os.path.join(os.path.dirname(__file__), "..", "kaynak"))
src = {"vo-sercan.mp3": json.load(open("words-sercan.json")), "vo-orhan.mp3": json.load(open("words-orhan.json"))}
P = json.load(open("../ses/parcalar.json")); out = []
for i, p in enumerate(P):
    a = p["kaynak_bas"]
    b = next((q["kaynak_bas"] for q in P[i+1:] if q["kaynak"] == p["kaynak"]), 1e9)
    for w in src[p["kaynak"]]:
        if a <= w["s"] < b:
            out.append({**w, "s": round(p["bas"] + w["s"] - a, 3), "e": round(p["bas"] + w["e"] - a, 3), "kim": p["kim"]})
json.dump(out, open("words-raw.json", "w"), ensure_ascii=False, indent=0)
print(len(out), "kelime")

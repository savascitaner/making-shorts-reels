# Merge: old raw words before the cut + tail words shifted by the cut time
import json
info = json.load(open("kaynak/tail-info.json")); cut = info["cut"]
old = [x for x in json.load(open("kaynak/words-raw-v2.json")) if x["s"] < cut - 0.02]
tail = json.load(open("kaynak/words-tail.json"))
for x in tail: x["s"] = round(x["s"] + cut, 3); x["e"] = round(x["e"] + cut, 3)
json.dump(old + tail, open("kaynak/words-raw.json", "w"), ensure_ascii=False, indent=0)
print(len(old), "+", len(tail), "kelime; kuyruk:", " ".join(x["w"] for x in tail))

# 16:9 long version: words (approved script text + whisper timings), caption chunks, shot list, card marks, .srt
# The TEXT comes from the approved script (ses/uzun-metin-v4.txt, tags removed). Whisper only gives the TIMES:
# its full-file pass misheard three phrases that the audio says correctly (checked with a hinted re-transcription).
import json, re, difflib
SCRIPT = re.sub(r"\[[a-z]+\]\s*", "", open("../../ses/uzun-metin-v4.txt", encoding="utf-8").read()).split()
WH = json.load(open("../../kaynak/words-master.json"))
wm = []
for x in WH:   # merge whisper's apostrophe pieces
    if x["w"].startswith("'") and wm: wm[-1]["w"] += x["w"]; wm[-1]["e"] = x["e"]
    else: wm.append(dict(x))
L = lambda s: re.sub(r"[^a-zçğıöşüâîû0-9]", "", s.lower())
# character streams with owner word index
A, aw = "", []
for i, w in enumerate(wm): t = L(w["w"]); A += t; aw += [i] * len(t)
B, bw = "", []
for i, w in enumerate(SCRIPT): t = L(w); B += t; bw += [i] * len(t)
# spoken numbers: whisper writes "20." for "yirminci"
A_map = {}
sm = difflib.SequenceMatcher(None, B, A, autojunk=False)
for blk in sm.get_matching_blocks():
    for k in range(blk.size): A_map[blk.a + k] = blk.b + k
words = []
for i, w in enumerate(SCRIPT):
    idx = [c for c in range(len(B)) if bw[c] == i]
    hits = [A_map[c] for c in idx if c in A_map]
    if hits and len(hits) >= max(1, len(idx) // 3):
        s = wm[aw[min(hits)]]["s"]; e = wm[aw[max(hits)]]["e"]
    else: s = e = None
    words.append({"w": w, "s": s, "e": e})
# fill gaps by interpolation between known neighbours
for i, w in enumerate(words):
    if w["s"] is None:
        j = i - 1
        while j >= 0 and words[j]["e"] is None: j -= 1
        k = i + 1
        while k < len(words) and words[k]["s"] is None: k += 1
        t0 = words[j]["e"] if j >= 0 else 0.0; t1 = words[k]["s"] if k < len(words) else t0 + 0.4
        n = k - j - 1; p = i - j
        w["s"] = round(t0 + (t1 - t0) * (p - 1) / n, 3); w["e"] = round(t0 + (t1 - t0) * p / n, 3)
for i in range(1, len(words)):   # monotonic
    if words[i]["s"] < words[i - 1]["s"]: words[i]["s"] = words[i - 1]["e"]
    if words[i]["e"] < words[i]["s"]: words[i]["e"] = words[i]["s"] + 0.1
LEAD = 0.3   # vo.wav is padded with 0.3 s so the first sound is not at the very first frame
for w in words: w["s"] = round(w["s"] + LEAD, 3); w["e"] = round(w["e"] + LEAD, 3)
EMPH = {"gölgen", "gölge", "çocukluk", "Bastırılan", "kaybolmaz", "rahatsız", "Öfkenin", "sorumluluğunu", "bireyleşme", "yalan", "desteklenmedi", "zor",
        "projeksiyon", "arketip", "kolektif", "Kırmızı", "potansiyel", "diyalogdu", "serbest"}
for w in words: w["em"] = 1 if re.sub(r"[.,?!:;']|'.*", "", w["w"]) in EMPH else 0
chunks, cur = [], []
for i, x in enumerate(words):
    cur.append(i); txt = " ".join(words[j]["w"] for j in cur); nxt = words[i + 1] if i + 1 < len(words) else None
    if x["w"][-1] in ".,?!:;" or nxt is None or nxt["s"] - x["e"] > 0.45 or len(cur) >= 4 or len(txt) >= 24: chunks.append(cur); cur = []
def at(prefix, start=0):   # index of the first word of the given phrase
    p = prefix.split()
    for i in range(start, len(words) - len(p) + 1):
        if all(L(words[i + k]["w"]) == L(p[k]) for k in range(len(p))): return i
    raise SystemExit("bulunamadı: " + prefix)
# [phrase, image, from[u,v,z], to[u,v,z], fx]
SH = [("Nefret ettiğin", "w01-calisma-odasi", [0.5, 0.5, 1.02], [0.5, 0.48, 1.14], "study"),
      ("Bu video,", "w02-diptik", [0.5, 0.5, 1.1], [0.5, 0.5, 1.0], "diptych"),
      ("Bu fikir Carl", "w03-jung-yakin", [0.62, 0.42, 1.0], [0.66, 0.4, 1.15], "jung"),
      ("Carl Jung ile Sigmund", "w04-birlikte-masa", [0.5, 0.5, 1.15], [0.5, 0.48, 1.02], "together"),
      ("Freud Viyana'da", "w05-iki-sehir", [0.5, 0.5, 1.0], [0.5, 0.5, 1.1], "cities"),
      ("İkisi uzun süre", "w04-birlikte-masa", [0.45, 0.45, 1.3], [0.5, 0.45, 1.45], "together"),
      ("Jung ile Sigmund Freud, 1912", "w06-iki-kapi", [0.5, 0.52, 1.15], [0.5, 0.5, 1.0], "doors"),
      ("Bu ayrılığın arkasında", "w01-calisma-odasi", [0.5, 0.45, 1.35], [0.5, 0.45, 1.6], "study"),
      ("Freud'un temel fikri", "w07-kiler", [0.5, 0.3, 1.25], [0.5, 0.75, 1.25], "cellar"),
      ("Freud'a göre bugün", "w08-freud-koltuk", [0.4, 0.45, 1.05], [0.38, 0.38, 1.2], "freud"),
      ("Bastırılan duygular", "w09-sandik-kilitli", [0.5, 0.55, 1.2], [0.5, 0.55, 1.02], "chest"),
      ("Günlük Yaşamın", "w10-dil-surcmesi", [0.5, 0.45, 1.02], [0.5, 0.42, 1.18], "slip"),
      ("Freud, çocukluk yıllarının", "w11-cocuk-koridor", [0.5, 0.55, 1.2], [0.5, 0.5, 1.0], "child"),
      ("Freud'un analiz yöntemi", "w12-divan", [0.5, 0.5, 1.0], [0.55, 0.45, 1.18], "couch"),
      ("Peki Jung neyi", "w03-jung-yakin", [0.66, 0.4, 1.15], [0.66, 0.36, 1.32], "jung"),
      ("Jung, kişisel bilinçdışının", "w13-kolektif", [0.5, 0.35, 1.2], [0.5, 0.6, 1.2], "collective"),
      ("Bu ortak imgelere", "w14-arketip", [0.5, 0.5, 1.15], [0.5, 0.42, 1.0], "stars"),
      ("Jung'un analizi ise", "w15-jung-diyalog", [0.5, 0.5, 1.02], [0.5, 0.5, 1.16], "dialogue"),
      ("Şimdi videonun asıl", "w16-koridor-ayna", [0.5, 0.5, 1.0], [0.5, 0.5, 1.5], "corridor"),
      ("Jung'a göre gölge,", "w17-jung-ayna", [0.5, 0.5, 1.02], [0.4, 0.45, 1.2], "mirror"),
      ("Buna projeksiyon", "w18-projeksiyon", [0.5, 0.5, 1.15], [0.5, 0.5, 1.0], "projection"),
      ("Bir iş arkadaşına", "w19-ofke-masa", [0.5, 0.55, 1.15], [0.5, 0.5, 1.0], "office"),
      ("Öfkenin bazen", "w20-ayna-yuz", [0.5, 0.48, 1.0], [0.5, 0.45, 1.22], "face"),
      ("Jung'un önerisi", "w21-patika", [0.5, 0.7, 1.2], [0.5, 0.35, 1.2], "path"),
      ("Jung, kendi iç", "w22-kirmizi-kitap", [0.5, 0.5, 1.02], [0.5, 0.55, 1.2], "book"),
      ("Freud ise iyileşmenin", "w23-sandik-acik", [0.5, 0.6, 1.15], [0.5, 0.48, 1.0], "open"),
      ("Bugün birçok terapist", "w24-terapi", [0.5, 0.5, 1.0], [0.5, 0.5, 1.15], "therapy"),
      ("Peki bilimsel olarak", "w25-terazi", [0.5, 0.5, 1.0], [0.5, 0.48, 1.15], "scale"),
      ("Sence o kişide", "w26-ikisi-cerceve", [0.5, 0.45, 1.0], [0.5, 0.42, 1.1], "end")]
shots, pos = [], 0
for ph, k, a, b, fx in SH:
    i = at(ph, pos); pos = i + 1
    shots.append({"t0": 0.0 if not shots else round(words[i]["s"] - 0.15, 3), "k": k, "a": a, "b": b, "fx": fx, "w": i})
def span(ph, start=0):
    i = at(ph, start); n = len(ph.split()); return [i, i + n - 1]
M = {"jung": span("Carl Jung'a ait."), "freud": span("Sigmund Freud,"), "cities": span("Freud Viyana'da çalışıyordu, Jung ise Zürih'te."),
     "split": span("1912 ile 1913 arasında yollarını ayırdılar."), "book1": span("Günlük Yaşamın Psikopatolojisi"),
     "free": span("serbest çağrışımlarına"), "coll": span("kolektif bilinçdışı"), "arch": span("arketip adını verdi."),
     "chapter": span("gölge.", at("Şimdi videonun")), "golge": span("Jung buna gölge diyordu."), "proj": span("Buna projeksiyon diyoruz:"),
     "birey": span("Buna bireyleşme diyordu."), "kitap": span("Kırmızı Kitap"), "soru": span("Sence o kişide gerçekten ne görüyorsun? Cevabını yorumlara yaz."),
     "takip": span("Daha fazlası için takipte kal.")}
DUR = round(words[-1]["e"] + 1.6 + 2.0 + 3.2, 2)   # follow card, clean cover 2 s, addresses
D = dict(words=words, chunks=chunks, duration=DUR, shots=shots, marks=M)
json.dump(D, open("words.json", "w"), ensure_ascii=False, indent=0)
open("words.js", "w").write("window.DATA=" + json.dumps(D, ensure_ascii=False) + ";")
v = {"konu": "Jung-Freud", "sure": DUR}; json.dump(v, open("../video.json", "w"), ensure_ascii=False, indent=2)
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f"{h:02}:{m:02}:{int(s):02},{min(999, int(round((s % 1) * 1000))):03}"
with open("../../../outputs/Jung-Freud/Jung-Freud-Uzun-16x9-altyazi.srt", "w") as f:
    for n, c in enumerate(chunks, 1):
        s = words[c[0]]["s"]; e = words[c[-1]]["e"]
        if n < len(chunks): e = min(max(e, s + 0.5), words[chunks[n][0]]["s"])
        f.write(f"{n}\n{ts(s)} --> {ts(e)}\n{' '.join(words[j]['w'] for j in c)}\n\n")
miss = sum(1 for i, w in enumerate(SCRIPT) if not any(bw[c] == i and c in A_map for c in range(len(B))))
print(len(words), "kelime,", len(chunks), "parça,", len(shots), "plan, süre", DUR, "| zamanı tahminle doldurulan kelime:", miss)

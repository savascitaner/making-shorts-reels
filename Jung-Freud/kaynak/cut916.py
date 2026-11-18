import json, re, difflib
W = json.load(open('words-master.json'))
def letters(s): return re.sub(r"[^a-zçğıöşüâîû0-9]", "", s.lower())
S = ""; cm = []
for i, w in enumerate(W):
    t = letters(w['w'])
    S += t; cm += [i]*len(t)
SENT = [
 "Nefret ettiğin o kişide, kendi gölgen olabilir.",
 "Bu fikir Carl Jung'a ait.",
 "Jung ile Sigmund Freud, 1912 ile 1913 arasında yollarını ayırdılar.",
 "Freud'a göre bugün yaşadığımız çoğu şey, çocukluk yıllarında bastırdığımız duygularla bağlantılıydı.",
 "Bastırılan duygular kaybolmaz; rüyalarda, dil sürçmelerinde ve krizlerde geri döner.",
 "Jung'a göre başkalarında en çok rahatsız olduğun özellik, çoğu zaman kendi kabul etmediğin yanındır.",
 "Jung buna gölge diyordu.",
 "Bir iş arkadaşına, bir akrabaya ya da bir partnerine neden bu kadar kızdığını düşün.",
 "Öfkenin bazen sende olan bir özelliği gösterdiğini Jung'un fikri söyler.",
 "Jung'un önerisi, bu yansımaları fark edip sorumluluğunu almaktı.",
 "Buna bireyleşme diyordu.",
 "Freud ise iyileşmenin, kendine yalan söylemeyi bıraktığın an başladığını düşünürdü.",
 "Bilimsel olarak, Freud'un fikirlerinin büyük bölümü deneylerle desteklenmedi.",
 "Jung'un fikirleri de sınanması zor.",
 "Sence o kişide gerçekten ne görüyorsun?",
 "Cevabını yorumlara yaz.",
 "Daha fazlası için takipte kal.",
]
# whisper writes numbers as digits; compare sentence with digits as spelled-out fallback
pos = 0; out = []
for s in SENT:
    sn = letters(s)
    win = S[pos:pos+len(sn)+2500]
    sm = difflib.SequenceMatcher(None, win, sn, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 3]
    if not blocks: raise SystemExit("EŞLEŞMEDİ: "+s)
    a0 = blocks[0].a; a1 = blocks[-1].a + blocks[-1].size - 1
    matched = sum(b.size for b in blocks)
    cov = matched / len(sn)
    wi0 = cm[pos+a0]; wi1 = cm[pos+a1]
    print(f"{W[wi0]['s']:7.2f}-{W[wi1]['e']:7.2f} cov={cov:.2f}  {s[:55]}")
    if cov < 0.85: raise SystemExit("DÜŞÜK EŞLEŞME: "+s)
    out.append([W[wi0]['s'], W[wi1]['e']])
    pos = pos + a1 + 1
json.dump(out, open('cuts916.json','w'))

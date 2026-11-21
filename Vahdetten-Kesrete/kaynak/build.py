# Senaryo metnini (doğru yazım) ses zamanlarına hizalar, plan (sahne listesi) ile birlikte cfg-long.js / cfg-shorts.js yazar.
import json, re, difflib, sys
def trl(s): return s.replace('İ', 'i').replace('I', 'ı').lower()
def norm(s):
    s = re.sub(r"[^a-zçğıöşüâîû0-9]", "", trl(s)); return s.replace('qu', 'ku').replace('q', 'k')
def display(tokens):
    out = []; prev_end = True
    for t in tokens:
        m = re.match(r"^([^A-Za-zÇĞİÖŞÜçğıöşü]*)([A-ZÇĞİÖŞÜ]+)", t); em = bool(m and len(m.group(2)) >= 3)
        w = t
        if em:
            lead = trl(m.group(2)); 
            if prev_end: lead = ("İ" if lead[0] == "i" else lead[0].upper()) + lead[1:]
            w = m.group(1) + lead + t[m.end():]
        out.append((w, 1 if em else 0)); prev_end = bool(re.search(r"[.?!]['”\"]?$", t))
    return out
def align(script_tokens, wh, off=0.0):
    """script_tokens: list[str]; wh: list of {w,s,e}. returns list of (s,e)."""
    a = [norm(t) for t in script_tokens]; b = [norm(x['w']) for x in wh]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False); res = [None] * len(a)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): res[blk.a + k] = (wh[blk.b + k]['s'] + off, wh[blk.b + k]['e'] + off)
    i = 0
    while i < len(res):
        if res[i] is None:
            j = i
            while j < len(res) and res[j] is None: j += 1
            s0 = res[i - 1][1] if i > 0 else (res[j][0] - 0.3 * (j - i) if j < len(res) else 0)
            e0 = res[j][0] if j < len(res) else s0 + 0.3 * (j - i)
            n = j - i; step = max(0.05, (e0 - s0) / n)
            for k in range(n): res[i + k] = (round(s0 + step * k, 3), round(s0 + step * (k + 1), 3))
            i = j
        else: i += 1
    return res
def mkwords(text_tokens, times):
    d = display(text_tokens); return [{"w": w, "s": round(t[0], 3), "e": round(t[1], 3), "em": em} for (w, em), t in zip(d, times)]
def chunks(W):
    ch, cur = [], []
    for i, x in enumerate(W):
        cur.append(i); txt = " ".join(W[j]['w'] for j in cur); nx = W[i + 1] if i + 1 < len(W) else None
        if x['w'][-1] in ".,?!:;”" or nx is None or nx['s'] - x['e'] > 0.45 or len(cur) >= 3 or len(txt) >= 15: ch.append(cur); cur = []
    return ch
def find(W, phrase, after=0.0):
    p = [norm(x) for x in phrase.split()]
    for i in range(len(W) - len(p)):
        if W[i]['s'] >= after and all(norm(W[i + k]['w']).startswith(p[k]) for k in range(len(p))): return i
    raise SystemExit("bulunamadı: " + phrase)

# ---------------- UZUN ----------------
meta = open("../ses/vo-metin.txt", encoding="utf8").read()
meta = re.sub(r"\[[^\]]*\]", "", meta)
nd1 = open("../ses/nd-1.txt", encoding="utf8").read(); nd1 = re.sub(r"\[[^\]]*\]", "", nd1).strip()
nd2 = open("../ses/nd-2.txt", encoding="utf8").read(); nd2 = re.sub(r"\[[^\]]*\]", "", nd2).strip()
meta = meta.replace("aynı vahdete aittir.", "aynı vahdete aittir. " + nd1, 1)
meta = meta.replace("aynı noktada buluşuyordu.", "aynı noktada buluşuyordu. " + nd2, 1)
tok = meta.split()
wh = json.load(open("words.json"))["words"]
L = mkwords(tok, align(tok, wh))
Q = re.sub(r"\[[^\]]*\]", "", open("../ses/kapanis-uzun.txt", encoding="utf8").read()).split()
K = re.sub(r"\[[^\]]*\]", "", open("../ses/takipte-kal.txt", encoding="utf8").read()).split()
qraw = json.load(open("q-raw.json")); kraw = json.load(open("k-raw.json"))
QS, KS = 429.98 + 0.9, 429.98 + 0.9 + 7.0824 + 0.5
Lq = mkwords(Q, align(Q, qraw, QS)); Lk = mkwords(K, align(K, kraw, KS))
for x in Lq: x['cardq'] = 1
for x in Lk: x['cardk'] = 1
LW = L + Lq + Lk
DUR_L = 447.5
# plan: (t0, src, kind, opts)
I = lambda k: ("img", k)
plan_l = [
 (0.0, "k1", "clip", {}), (8.0, "f01_el-telefon", "img", {}), (16.0, "s02_pencere", "img", {}), (21.4, "s01_yildiz", "img", {}),
 (28.5, "s13_mandala", "img", {}), (37.7, "s14_bosluk", "img", {}), (45.1, "s03_agi", "img", {}), (54.2, "s16_galaksi", "img", {}),
 (61.5, "s09_dogum", "img", {}), (69.8, "f02_demokritos", "img", {}), (83.5, "k2", "clip", {"rate": 0.835}),
 (93.0, "f05_proton", "img", {}), (108.2, "s08_hidrojen", "img", {}), (121.0, "f04_elma", "img", {}), (123.2, "f03_gozyasi", "img", {}),
 (124.8, "s04_noron", "img", {}), (126.3, "s01_yildiz", "img", {"mirror": 1}), (131.2, "s03_agi", "img", {"mirror": 1}), (138.3, "s16_galaksi", "img", {"mirror": 1}),
 (144.9, "k3", "clip", {"rate": 0.9}), (153.5, "s10_supernova", "img", {}), (160.3, "s14_bosluk", "img", {"mirror": 1}),
 (167.8, "s07_plazma", "img", {}), (173.1, "s06_patlama", "img", {}), (187.0, "s13_mandala", "img", {"mirror": 1}),
 (194.9, "s07_plazma", "img", {"mirror": 1}), (204.6, "f09_calisma-odasi", "img", {}), (213.8, "s08_hidrojen", "img", {"mirror": 1}),
 (217.2, "f05_proton", "img", {"mirror": 1}), (224.8, "s08_hidrojen", "img", {}), (229.0, "s09_dogum", "img", {"mirror": 1}),
 (234.6, "f06_dunya", "img", {}), (239.8, "k4", "clip", {"rate": 1.0}), (246.8, "s05_alan", "img", {}), (258.0, "s11_dalga", "img", {}),
 (263.5, "s12_halka", "img", {}), (276.7, "f07_bilge", "img", {}), (298.4, "f08_iki-dalga", "img", {}), (315.4, "s11_dalga", "img", {"mirror": 1}),
 (323.1, "s14_bosluk", "img", {}), (332.5, "s15_yinyang", "img", {}), (342.2, "f09_calisma-odasi", "img", {"mirror": 1}),
 (359.5, "s13_mandala", "img", {}), (367.0, "s02_pencere", "img", {"mirror": 1}), (371.6, "k6", "vclip", {"rate": 0.75}),
 (383.5, "s06_patlama", "img", {"mirror": 1}), (387.4, "s03_agi", "img", {}), (393.4, "s16_galaksi", "img", {}), (399.0, "s01_yildiz", "img", {}),
 (406.5, "f10_siluet", "img", {}), (419.5, "k5", "clip", {"rate": 0.74}),
]
bang = L[find(L, "Fiziğin tekillik", 170)]['s'] + 0.9
pulse_words = ["dalgası", "kesret", "vahdet", "tekillik", "birlik", "donmuş", "kuarklar", "leptonlar", "içine", "advaita", "dalga"]
pulses_l = []
for x in LW:
    if (x.get('em') or norm(x['w']) in ("advaita", "yinyang")) and x['s'] > 1.0: pulses_l.append(round(x['s'], 2))
for ph in ("Dalga, denizden ayrı değildir", "Contraria sunt complementa", "iki olan her şey"):
    try: pulses_l.append(round(L[find(L, ph, 0)]['s'], 2))
    except SystemExit: pass
pulses_l = [p for p in sorted(set(pulses_l)) if any(abs(p - q) < 0.4 for q in (4.78, 179.68, 298.36, 333.28))]
sections_l = [(0, 0.55), (69.8, 0.35), (144.9, 0.8), (239.8, 0.5), (342.2, 0.75)]
cfg_l = dict(fmt="long", W=1920, H=1080, FPS=30, DUR=DUR_L, words=LW, chunks=chunks(LW), plan=plan_l, bang=round(bang, 2), pulses=pulses_l, sections=sections_l,
             beams=[[177,190,0.5]], hook=dict(lines=["SEN BİR", "DALGASIN"], t1=3.0), sub=dict(t0=62.0),
             qcard=dict(t0=QS - 0.1, t1=QS + 7.4, lines=["SENCE SEN OKYANUSTAKİ", "BİR DALGA MISIN,", "YOKSA OKYANUSUN", "TA KENDİSİ Mİ?"], small="CEVABINI YORUMLARA YAZ"),
             kcard=dict(t0=KS - 0.1, t1=DUR_L, addr_t=KS + 2.3), caphide=[[QS - 0.1, QS + 7.4], [KS - 0.1, KS + 2.4]])
open("cfg-long.js", "w", encoding="utf8").write("window.CFG=" + json.dumps(cfg_l, ensure_ascii=False) + ";")
print("uzun", len(LW), "kelime", len(cfg_l['chunks']), "parça", "bang", bang, "pulse", len(pulses_l))

# ---------------- SHORTS ----------------
seg = json.load(open("shorts-seg.json"))["segments"]
S_text = ["Bir Nobel'li fizikçi şövalye olunca, armasına Çin'in yin-yang simgesini koydu.",
          "Üstüne de şu sözü yazdırdı: Contraria sunt complementa.",
          "Karşıtlar birbirini tamamlar.",
          "Şu an bu ekranı tutan elin, evrenin en uzak yıldızıyla aynı okyanusun DALGASI.",
          "Bir elektron, aslında \"elektron alanı\" dediğimiz o tek ve bütün okyanusun üzerinde oluşan küçük bir dalgalanmadan, bir titreşimden ibarettir.",
          "Yani siz ve evrenin öbür ucundaki bir yıldız, aslında aynı okyanusun farklı noktalarındaki iki dalgasınız.",
          "Çünkü bizler sadece evrenin içinde yaşayan canlılar değiliz; bizler, kuarklar ve leptonlar aracılığıyla kendini seyreden evrenin ta kendisiyiz."]
sraw = [x for x in json.load(open("shorts-raw.json")) if x['e'] < 54.3]
stok = " ".join(S_text).split()
sqtok = re.sub(r"\[[^\]]*\]", "", open("../ses/kapanis-shorts.txt", encoding="utf8").read()).split()
sktok = K
alltok = stok + sqtok + sktok
SW = mkwords(alltok, align(alltok, sraw))
nq = len(stok); nk = len(sqtok)
for i in range(nq, nq + nk): SW[i]['cardq'] = 1
for i in range(nq + nk, len(SW)): SW[i]['cardk'] = 1
q0 = seg[7][0]; k0 = seg[8][0]
DUR_S = 59.13
plan_s = [(0.0, "k6", "clip", {"rate": 0.8}), (9.8, "s15_yinyang", "img", {}), (12.23, "f11_v-el", "img", {}), (15.0, "f12_v-dalga", "img", {}),
          (18.15, "s05_alan", "img", {}), (27.4, "f12_v-dalga", "img", {"mirror": 1}), (35.3, "k7", "clip", {"rate": 0.75}),
          (46.15, "f13_v-siluet", "img", {}), (52.0, "s16_galaksi", "img", {})]
pulses_s = [round(seg[1][0] + 2.2, 2)]
cfg_s = dict(fmt="shorts", W=1080, H=1920, FPS=30, DUR=DUR_S, words=SW, chunks=chunks(SW), plan=plan_s, bang=-99, pulses=pulses_s, sections=[(0, 0.7)],
             beams=[], hook=dict(lines=["NOBEL'Lİ", "FİZİKÇİNİN", "ARMASI"], t1=3.0), sub=dict(t0=41.0),
             qcard=dict(t0=q0 - 0.1, t1=q0 + 5.8, lines=["SEN OLSAN", "ARMANA NE", "YAZDIRIRDIN?"], small="YORUMLARA YAZ"),
             kcard=dict(t0=k0 - 0.1, t1=DUR_S, addr_t=k0 + 2.3), caphide=[[q0 - 0.1, q0 + 5.8], [k0 - 0.1, k0 + 2.4]])
open("cfg-shorts.js", "w", encoding="utf8").write("window.CFG=" + json.dumps(cfg_s, ensure_ascii=False) + ";")
print("shorts", len(SW), "kelime", "q0", q0, "k0", k0)

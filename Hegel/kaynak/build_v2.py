# Hegel v2: cold-open hook (sentence 6.2.15 "Sonunda ... köledir.") + rebuilt vertical Reels (full-frame 9:16 crops, no blurred bg)
# and the 16:9 long version with the same hook.  Usage (from Hegel/):  python kaynak/build_v2.py [reels] [16x9]
import json, subprocess, os, math, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
from PIL import Image, ImageFilter, ImageEnhance

W_, find, ts, srt_ts = B.W_, B.find, B.ts, B.srt_ts
K, TMP, OUT, VO, MUSIC, MASTER, FPS, XF = B.K, B.TMP, B.OUT, B.VO, B.MUSIC, B.MASTER, B.FPS, B.XF
R = B.R; GS = os.path.join(R, "gorseller", "secilen"); GA = os.path.join(R, "gorseller", "ai")
TMP2 = os.path.join(TMP, "v2"); os.makedirs(TMP2, exist_ok=True)

# ---------- hook: exact audio span of "Sonunda özgürlüğe giden yolu bulan efendi değil, köledir." ----------
HOOK_A, HOOK_B = find(6, "Sonunda")["i"], find(6, "köledir.")["i"]
HOOK_S0, HOOK_S1 = 237.56, 241.80          # measured on the waveform: onset 237.60, decay done 241.70 (word json says 237.04)
HOOK_REAL = (237.60, 241.62)

# ---------- vertical views: name -> (file, box fractions x0,y0,x1,y1, motion) ----------
#  motion: ("zoom", z0, z1) inside the 9:16 box  |  ("pan", p0, p1): box wider than 9:16, slide from p0 to p1 (0=left, 1=right)
def ai_v(k):
    p = os.path.join(GA, f"AI-{k}-v.png")
    return p
VIEWS = {
    "hook":      ("gorseller/secilen/w-tasci-0.jpg", (0.555, 0.0, 0.898, 1.0), ("zoom", 1.00, 1.07)),
    "tasci-pan": ("gorseller/secilen/w-tasci-0.jpg", (0.10, 0.0, 0.90, 0.93), ("pan", 0.0, 1.0)),
    "jena-ai":   ("gorseller/ai/AI-a-29-v.png", (0, 0, 1, 1), ("zoom", 1.00, 1.08)),
    "portre":    ("gorseller/secilen/a-portre-1.jpg", (0.17, 0.03, 0.83, 0.95), ("zoom", 1.00, 1.08)),
    "portre-yakin": ("gorseller/secilen/a-portre-1.jpg", (0.26, 0.12, 0.74, 0.79), ("zoom", 1.06, 1.00)),
    "jena-savas": ("gorseller/secilen/e-jena-savas-0.jpg", (0.0, 0.0, 1.0, 1.0), ("pan", 0.15, 0.62)),
    "jena-savas2": ("gorseller/secilen/e-jena-savas-0.jpg", (0.0, 0.0, 1.0, 1.0), ("pan", 1.0, 0.55)),
    "sebbers":   ("gorseller/secilen/d-hegel-sebbers-0.jpg", (0.16, 0.0, 0.78, 0.84), ("zoom", 1.00, 1.08)),
    "sabah":     ("gorseller/secilen/r-friedrich-sabah-8.jpg", (0.0, 0.0, 1.0, 1.0), ("pan", 0.0, 0.7)),
    "cicek-ai":  ("gorseller/ai/AI-b-29-v.png", (0, 0, 1, 1), ("zoom", 1.00, 1.08)),
    "cicek-ai2": ("gorseller/ai/AI-b-29-v.png", (0, 0, 1, 1), ("zoom", 1.10, 1.00)),
    "natürmort": ("gorseller/secilen/t-cicek-1.jpg", (0.0, 0.0, 1.0, 1.0), ("pan", 0.45, 1.0)),
    "ay":        ("gorseller/secilen/s-friedrich-ay-6.jpg", (0.0, 0.0, 1.0, 1.0), ("pan", 0.15, 0.55)),
    "ay2":       ("gorseller/secilen/s-friedrich-ay-6.jpg", (0.0, 0.0, 1.0, 1.0), ("pan", 0.75, 0.35)),
    "efendi-ai": ("gorseller/ai/AI-c2-5-v.png", (0, 0, 1, 1), ("zoom", 1.00, 1.08)),
    "ciftci":    ("gorseller/secilen/v-ciftci-0.jpg", (0.0, 0.0, 1.0, 1.0), ("pan", 0.0, 0.85)),
}
VSHOTS = [
    (find(1, "13")["i"], "jena-ai"), (find(1, "Adı")["i"], "portre"), (find(1, "Ertesi")["i"], "jena-savas"),
    (find(3, "Hegel diyalektiği")["i"], "sebbers"), (find(3, "Peki")["i"], "portre-yakin"), (find(3, "Onun")["i"], "sabah"),
    (find(4, "Hegel bunu")["i"], "cicek-ai"), (find(4, "İşte")["i"], "natürmort"),
    (find(6, "Şimdi")["i"], "ay"), (find(6, "Bu istek")["i"], "jena-savas2"), (find(6, "Efendi, tanınmayı")["i"], "efendi-ai"),
    (find(6, "Köle ise")["i"], "tasci-pan"), (find(6, "Ve dünyayı")["i"], "ciftci"), (find(6, "Sonunda")["i"], "hook"),
    (find(6, "Bugün")["i"], "efendi-ai"), (find(6, "Hegel iki")["i"], "portre"),
    (find(9, "Belki")["i"], "ay2"), (find(9, "Tomurcuk")["i"], "cicek-ai2"),
]
VSHOTS.sort()
def vshot_at(i): return [v for k, v in VSHOTS if k <= i][-1]

def load_up(path):
    im = Image.open(os.path.join(R, path)).convert("RGB")
    if min(im.size) < 2000:                      # low-res: 4x lanczos + light sharpen before cropping
        im = im.resize((im.width * 4, im.height * 4), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=3, percent=55, threshold=2))
    return im

def vstill(name, W=1080, H=1920):
    """returns (jpeg path, motion). Pan stills are H*2 tall and wider than 9:16; zoom stills are exactly 2W x 2H."""
    path, (x0, y0, x1, y1), mot = VIEWS[name]
    out = os.path.join(TMP2, f"v-{name}.jpg")
    if os.path.exists(out): return out, mot
    im = load_up(path); bx = (x0 * im.width, y0 * im.height, x1 * im.width, y1 * im.height)
    bw, bh = bx[2] - bx[0], bx[3] - bx[1]; ar = W / H
    if mot[0] == "zoom":                         # fit an exact 9:16 box centred in the given box
        if bw / bh > ar: nw = bh * ar; bx = (bx[0] + (bw - nw) / 2, bx[1], bx[0] + (bw + nw) / 2, bx[3])
        else: nh = bw / ar; bx = (bx[0], bx[1] + (bh - nh) / 2, bx[2], bx[1] + (bh + nh) / 2)
        reg = im.crop(tuple(round(v) for v in bx)).resize((2 * W, 2 * H), Image.LANCZOS)
    else:
        reg = im.crop(tuple(round(v) for v in bx)); s = 2 * H / reg.height
        reg = reg.resize((max(2 * W, round(reg.width * s)), 2 * H), Image.LANCZOS)
    reg.save(out, quality=95); return out, mot

def hook16(W=1920, H=1080):
    out = os.path.join(TMP2, "hook-16x9.jpg")
    if os.path.exists(out): return out
    im = load_up("gorseller/secilen/w-tasci-0.jpg")
    x0, y0, x1 = 0.36 * im.width, 0.0 * im.height, 0.97 * im.width     # old stonebreaker on the right, darker ground on the left for text
    h = (x1 - x0) * H / W
    reg = im.crop((round(x0), round(y0), round(x1), round(y0 + h))).resize((2 * W, 2 * H), Image.LANCZOS)
    reg = ImageEnhance.Brightness(reg).enhance(0.92)
    reg.save(out, quality=95); return out

def ease(n): return f"(0.5-0.5*cos(PI*min(on/{max(1, n - 1)},1)))"

def build(name, W, H, runs, vertical):
    # ---- ranges: hook first, then the flow ----
    rng = [(HOOK_S0, HOOK_S1, HOOK_A, HOOK_B, True)]
    for a, b in runs:
        s0 = W_[a]["s"] - 0.25 if a > 0 else 0.0; s1 = W_[b]["e"] + 0.35
        if b + 1 < len(W_): s1 = min(s1, (W_[b]["e"] + W_[b + 1]["s"]) / 2 + 0.1)
        rng.append((s0, s1, a, b, False))
    TAIL = 1.2 if vertical else 2.5
    words, off, shots = [], 0.0, []
    for s0, s1, a, b, hk in rng:
        if hk:     # spread the word times over the measured speech span (json start of the first word is early)
            js0, js1 = W_[a]["s"], W_[b]["e"]; r0, r1 = HOOK_REAL
            mp = lambda t: r0 + (t - js0) * (r1 - r0) / (js1 - js0) - s0 + off
            for w in W_[a:b + 1]: words.append(dict(w, s=mp(w["s"]), e=mp(w["e"]), hook=True))
            shots.append((0.0, "HOOK"))
        else:
            for w in W_[a:b + 1]: words.append(dict(w, s=w["s"] - s0 + off, e=w["e"] - s0 + off))
            for k in range(a, b + 1):
                img = vshot_at(k) if vertical else B.shot_at(k)
                if shots[-1][1] != img:
                    t = off if k == a else W_[k]["s"] - s0 + off - 0.3
                    if t - shots[-1][0] < 1.5 and shots[-1][1] != "HOOK": shots[-1] = (shots[-1][0], img)
                    else: shots.append((max(0.0, t), img))
        off += s1 - s0
    DUR = round(off + TAIL, 2)
    # ---- audio ----
    af = []
    for j, (s0, s1, a, b, hk) in enumerate(rng):
        d = s1 - s0
        af.append(f"[0:a]atrim={s0:.3f}:{s1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={0.01 if j == 0 else 0.03},afade=t=out:st={d - 0.06:.3f}:d=0.06[r{j}]")
    af.append("".join(f"[r{j}]" for j in range(len(rng))) + f"concat=n={len(rng)}:v=0:a=1,aresample=48000,pan=stereo|c0=c0|c1=c0,apad,atrim=0:{DUR},asplit=2[vo][sc]")
    mstart = 30.0 if vertical else 2.0
    af.append(f"[1:a]aresample=48000,atrim=start={mstart},asetpts=PTS-STARTPTS,atrim=0:{DUR},volume=0.32,afade=t=in:d=1.0,afade=t=out:st={DUR - 3}:d=3[mu]")
    af.append("[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600:makeup=1[md];[vo][md]amix=inputs=2:normalize=0:duration=first[a]")
    mix = os.path.join(TMP2, name + "-mix.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-i", MUSIC, "-filter_complex", ";".join(af), "-map", "[a]", "-c:a", "pcm_s24le", mix], check=True)
    # ---- picture ----
    ends = [s for s, _ in shots[1:]] + [DUR]
    inputs, ch = [], []
    for i, ((t0, img), t1) in enumerate(zip(shots, ends)):
        seg = t1 - t0 + (XF if i < len(shots) - 1 else 0); n = int(math.ceil(seg * FPS)) + 2; e = ease(n)
        if vertical:
            src, mot = vstill("hook" if img == "HOOK" else img, W, H)
        elif img == "HOOK":
            src, mot = hook16(W, H), ("zoom", 1.00, 1.05)
        else:
            src = B.still(img, W, H); z0, z1, ax0, ax1, ay0, ay1 = B.MOVES[i % 4]; mot = None
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{n / FPS:.3f}", "-i", src]
        tail = f"trim=duration={seg:.3f},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},format=yuv420p[s{i}]"
        if mot is None:
            ch.append(f"[{i}:v]zoompan=z='{z0}+({z1}-{z0})*{e}':x='(iw-iw/zoom)*({ax0}+({ax1}-{ax0})*{e})':y='(ih-ih/zoom)*({ay0}+({ay1}-{ay0})*{e})':d=1:s={W}x{H}:fps={FPS},{tail}")
        elif mot[0] == "zoom":
            z0, z1 = mot[1], mot[2]
            ax = 0.62 if (img == "HOOK" and not vertical) else 0.5
            ay = 0.12 if (vertical and img in ("HOOK", "hook")) else 0.4     # keep the hat clear of the top hook text
            ch.append(f"[{i}:v]zoompan=z='{z0}+({z1}-{z0})*{e}':x='(iw-iw/zoom)*{ax}':y='(ih-ih/zoom)*{ay}':d=1:s={W}x{H}:fps={FPS},{tail}")
        else:
            p0, p1 = mot[1], mot[2]; et = f"(0.5-0.5*cos(PI*min(t/{seg:.3f},1)))"
            ch.append(f"[{i}:v]crop=w={2 * W}:h={2 * H}:x='(iw-{2 * W})*({p0}+({p1}-{p0})*{et})':y=0,scale={W}:{H}:flags=lanczos,setsar=1,{tail}")
    fc = ";".join(ch); prev = "s0"
    for i in range(1, len(shots)):
        fc += f";[{prev}][s{i}]xfade=transition=fade:duration={XF}:offset={ends[i - 1]:.3f}[x{i}]"; prev = f"x{i}"
    assf = os.path.join(TMP2, name + ".ass")
    fc += f";[{prev}]trim=duration={DUR},subtitles='{assf}':fontsdir='{os.path.join(K, 'fonts')}',format=yuv420p[v]"
    # ---- captions (hook sentence: SRT yes, burned no - the big hook text carries it) ----
    mxw, mxc = (3, 20) if vertical else (6, 40)
    chunks, cur = [], []
    for k, w in enumerate(words):
        cur.append(w); nx = words[k + 1] if k + 1 < len(words) else None
        txt = " ".join(x["w"] for x in cur)
        if (nx is None or len(cur) >= mxw or len(txt) + 1 + len(nx["w"]) > mxc or re.search(r"[.,?!:;…\"]$", w["w"])
                or nx["par"] != w["par"] or nx["sec"] != w["sec"] or nx["s"] - w["e"] > 0.45 or nx.get("hook") != w.get("hook")):
            chunks.append(cur); cur = []
    fs, ol, sh, mv = (80, 3.2, 2.2, 470) if vertical else (56, 2.4, 1.6, 64)
    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
           "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           f"Style: Cap,Montserrat ExtraBold,{fs},&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,1,0,1,{ol},{sh},2,70,70,{mv},1",
           f"Style: Kin,Playfair Display Black,{110 if vertical else 96},&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,2,0,1,{ol + 0.6},{sh + 1},5,40,40,0,1",
           f"Style: KinS,Montserrat ExtraBold,{68 if vertical else 44},&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,2,0,1,{ol},{sh},5,40,40,0,1",
           f"Style: Hook,Anton,{150 if vertical else 132},&H00FFFFFF,&H00FFFFFF,&H00101010,&H8C000000,0,0,0,0,100,100,1,0,1,3.2,3,{8 if vertical else 4},60,60,0,1",
           f"Style: HookS,Montserrat ExtraBold,52,&H00FFFFFF,&H00FFFFFF,&H00101010,&H8C000000,0,0,0,0,100,100,0,0,1,2.4,2.2,4,60,60,0,1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    srt = []
    for ci, c in enumerate(chunks):
        c_end = min(c[-1]["e"] + 0.3, chunks[ci + 1][0]["s"]) if ci + 1 < len(chunks) else c[-1]["e"] + 0.6
        srt.append(f"{ci + 1}\n{srt_ts(c[0]['s'])} --> {srt_ts(c_end)}\n{' '.join(x['w'] for x in c)}\n")
        if c[0].get("hook"): continue
        for j, w in enumerate(c):
            s = c[0]["s"] if j == 0 else w["s"]; e = c[j + 1]["s"] if j + 1 < len(c) else c_end
            parts = [(f"{{\\1a&H00&\\fscx107\\fscy107}}{x['w']}{{\\1a&H38&\\fscx100\\fscy100}}" if m == j else x["w"]) for m, x in enumerate(c)]
            ass.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\1a&H38&}}{' '.join(parts)}")
    # hook text: on frame 0, no fade-in
    if vertical:
        ass.append(f"Dialogue: 5,{ts(0)},{ts(3.5)},Hook,,0,0,0,,{{\\an8\\pos({W // 2},70)\\fad(0,300)\\fs98}}KAZANAN EFENDİ DEĞİL,\\N{{\\fs165}}KÖLEDİR")
    else:
        ass.append(f"Dialogue: 5,{ts(0)},{ts(4.5)},Hook,,0,0,0,,{{\\an4\\pos(110,440)\\fad(0,350)}}KAZANAN EFENDİ DEĞİL,\\N{{\\fs170}}KÖLEDİR")
        ass.append(f"Dialogue: 5,{ts(0)},{ts(4.5)},HookS,,0,0,0,,{{\\an7\\pos(116,640)\\fad(0,350)}}Hegel diyalektiği: 200 yıllık fikir, 6 dakikada")
    # ---- kinetic typography (same as v1, only where the source words are in this cut) ----
    T = {w["i"]: w for w in words if not w.get("hook")}
    def at(sec, word, nth=0, end=False):
        w = find(sec, word, nth); return (T[w["i"]]["e"] if end else T[w["i"]]["s"]) if w["i"] in T else None
    def sec_end(sec):
        ws = [w for w in words if w["sec"] == sec and not w.get("hook")]; return ws[-1]["e"] + 0.4 if ws else None
    ky = 360 if vertical else 250
    def kin(t0, t1, text, y, style="Kin", fade=(250, 250)):
        if t0 is None or t1 is None or t1 <= t0: return
        ass.append(f"Dialogue: 2,{ts(t0)},{ts(t1)},{style},,0,0,0,,{{\\fad({fade[0]},{fade[1]})\\pos({W // 2},{y})}}{text}")
    def bar(t0, t1, w, h, y):
        if t0 is None or t1 is None or t1 <= t0: return
        w, h = int(w), max(8, int(h))
        ass.append(f"Dialogue: 3,{ts(t0)},{ts(t1)},Kin,,0,0,0,,{{\\an5\\pos({W // 2},{y})\\bord0\\shad0\\1c&H2A2AE6&\\fscx0\\t(0,350,\\fscx100)\\fad(0,250)\\p1}}m 0 0 l {w} 0 {w} {h} 0 {h}{{\\p0}}")
    t1, t2, t3 = at(3, "tez,"), at(3, "antitez,"), at(3, "sentez."); strike = at(3, "kullanmadı.", end=True); hb = at(3, "Aufhebung.")
    if t1 is not None:
        kfs = 120 if vertical else 110
        if vertical:
            for txt, t, y in [("TEZ", t1, ky - 150), ("ANTİTEZ", t2, ky), ("SENTEZ", t3, ky + 150)]:
                kin(t, hb - 0.2, f"{{\\fs{kfs}}}{txt}", y, fade=(200, 250))
                bar(strike, hb - 0.2, len(txt) * kfs * 0.5 + 20, kfs * 0.1, y + 6)
        else:
            kin(t1, t2, "TEZ", ky, fade=(200, 0)); kin(t2, t3, "TEZ – ANTİTEZ", ky, fade=(0, 0)); kin(t3, strike, "TEZ – ANTİTEZ – SENTEZ", ky, fade=(0, 0))
            kin(strike, hb - 0.2, "TEZ – ANTİTEZ – SENTEZ", ky, fade=(0, 250)); bar(strike, hb - 0.2, 22 * 96 * 0.5, 11, ky + 6)
        kin(hb, sec_end(3) + (1.0 if vertical else 0), "AUFHEBUNG", ky, fade=(300, 300))
    a0 = at(4, "Aufhebung")
    if a0 is not None:
        a1, a2, a3 = at(4, "kaldırmak,"), at(4, "saklamak"), at(4, "taşımak.", end=True)
        off4 = at(4, "Hegel bunu") - 0.2; sub = ky + (110 if vertical else 95)
        kin(a0, off4, "AUFHEBUNG", ky, fade=(300, 300))
        if vertical:
            kin(a1, off4, "kaldırmak", sub, "KinS", (200, 300)); kin(a2, off4, "saklamak", sub + 90, "KinS", (200, 300)); kin(a3 - 0.6, off4, "yükseltmek", sub + 180, "KinS", (200, 300))
        else:
            kin(a1, a2, "= kaldırmak", sub, "KinS", (200, 0)); kin(a2, a3 - 0.6, "= kaldırmak · saklamak", sub, "KinS", (0, 0)); kin(a3 - 0.6, off4, "= kaldırmak · saklamak · yükseltmek", sub, "KinS", (0, 300))
    v0 = at(5, "varlığı")
    if v0 is not None:
        h0, o0, end5 = at(5, "hiçliğe"), at(5, "oluş."), sec_end(5)
        kin(v0, h0, "VARLIK", ky, fade=(250, 0)); kin(h0, o0, "VARLIK → HİÇLİK", ky, fade=(0, 0)); kin(o0, end5, "VARLIK → HİÇLİK → OLUŞ", ky, fade=(0, 400))
    open(assf, "w").write("\n".join(ass) + "\n")
    srt_out = os.path.join(TMP2, name + ".srt"); open(srt_out, "w").write("\n".join(srt))
    info = {"dur": DUR, "shots": shots, "last": words[-1]["w"], "ranges": [(round(a, 2), round(b, 2)) for a, b, *_ in rng]}
    print(name, json.dumps(info, ensure_ascii=False), flush=True)
    if os.environ.get("DRY"): return
    pic = os.path.join(TMP2, name + "-pic.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-r", str(FPS), pic], check=True)
    mst = os.path.join(TMP2, name + "-master.wav")
    subprocess.run([sys.executable, MASTER, mix, mst, "--I", "-14", "--TP", "-2", "--limit"], check=True)
    final = os.path.join(TMP2, name + ".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", mst, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
                    "-ar", "48000", "-t", f"{DUR:.3f}", "-movflags", "+faststart", final], check=True)
    json.dump(info, open(os.path.join(TMP2, name + ".json"), "w"), ensure_ascii=False)
    print(name, "DONE", DUR, flush=True)

def sel_runs(pred, drop=()):
    sel = [w["i"] for w in W_ if pred(w) and (w["sec"], w["par"], w["sent"]) not in drop]; out = []
    for i in sel:
        if out and out[-1][1] == i - 1: out[-1][1] = i
        else: out.append([i, i])
    return out

REELS_DROP = {(4, 0, 0), (3, 1, 5), (3, 1, 6), (3, 0, 1), (9, 1, 5)} | set(tuple(x) for x in json.loads(os.environ.get("EXTRA_DROP", "[]")))
CUTS = {
    "reels": ("Hegel-Reels-9x16", 1080, 1920, sel_runs(lambda w: (w["sec"] == 1 and w["par"] < 2) or w["sec"] in (3, 4, 6) or (w["sec"] == 9 and w["par"] >= 1), REELS_DROP), True),
    "16x9": ("Hegel-16x9", 1920, 1080, [[0, len(W_) - 1]], False),
}
if __name__ == "__main__":
    for k in (sys.argv[1:] or CUTS):
        n, w, h, r, v = CUTS[k]; build(n, w, h, r, v)

# Hegel: all deliverables from one voice take.  Usage (from Hegel/):  python3 kaynak/build.py [name ...]
# Picture: PIL pre-composed stills (blurred self as background + full painting) -> ffmpeg zoompan Ken Burns + xfade.
# Captions + kinetic type: ASS (libass). Mix: VO + ducked CC0 music, then cinecode master_audio.py -> -14 LUFS.
import json, subprocess, os, math, sys, re
from PIL import Image, ImageFilter, ImageEnhance

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); K = os.path.join(R, "kaynak")
G = os.path.join(R, "gorseller", "secilen"); OUT = os.path.join(R, "teslim"); TMP = os.path.join(K, "tmp")
VO = os.path.join(R, "ses", "Hegel-tam.wav")
MUSIC = os.path.join(R, "..", "Spinoza", "build", "music", "Kimiko_Ishizaka_-_26_-_Variatio_25_a_2_Clav.mp3")
MASTER = os.path.join(R, "..", "araclar", "cinecode", "scripts", "master_audio.py")
FPS, XF = 30, 0.8
os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
W_ = json.load(open(os.path.join(K, "words.json")))["words"]
for i, w in enumerate(W_): w["i"] = i

def norm(s): return re.sub(r"[^\wçğıöşüâîû]", "", s.replace("İ", "i").replace("I", "ı").lower())
def find(sec, word, nth=0):
    ph = [norm(x) for x in word.split()]; S_ = [w for w in W_ if w["sec"] == sec]
    hits = [S_[k] for k in range(len(S_) - len(ph) + 1) if [norm(x["w"]) for x in S_[k:k + len(ph)]] == ph]
    if len(hits) <= nth: raise SystemExit(f"not found: sec {sec} '{word}' #{nth}")
    return hits[nth]

# ---------- shot list on the full take: (first word index, image) ----------
SHOTS = [
    (find(1, "13")["i"], "AI-a"), (find(1, "Adı")["i"], "a-portre-1"), (find(1, "Ertesi")["i"], "e-jena-savas-0"),
    (find(2, "1770'te")["i"], "c-hegel-genc-0"), (find(2, "Tübingen'de")["i"], "j-holderlin-0"),
    (find(2, "Schelling'le")["i"], "k-schelling-1"), (find(2, "Sonra")["i"], "y-berlin-1831-7"), (find(2, "Öyle")["i"], "b-kugler-0"),
    (find(3, "Hegel diyalektiği")["i"], "d-hegel-sebbers-0"),
    (find(4, "Almancada")["i"], "AI-b"), (find(4, "İşte")["i"], "t-cicek-1"),
    (find(5, "Hegel bu hareketi")["i"], "s-friedrich-ay-6"), (find(5, "Hegel'e göre gerçek")["i"], "r-friedrich-sabah-8"),
    (find(6, "Şimdi")["i"], "s-friedrich-ay-6"), (find(6, "Bu istek")["i"], "e-jena-savas-0"), (find(6, "Efendi, tanınmayı")["i"], "AI-c"),
    (find(6, "Köle ise")["i"], "w-tasci-0"), (find(6, "Ve dünyayı")["i"], "v-ciftci-0"), (find(6, "Hegel iki")["i"], "a-portre-1"),
    (find(7, "Hegel'e")["i"], "e-jena-savas-0"), (find(7, "Jena'da")["i"], "AI-a"),
    (find(8, "Hegel 1831'de")["i"], "a-portre-1"), (find(8, "Genç")["i"], "o-marx-0"), (find(8, "Kierkegaard")["i"], "r-friedrich-sabah-8"),
    (find(8, "Anlatılır")["i"], "a-portre-1"),
    (find(9, "Hegel'in en güzel")["i"], "AI-d"), (find(9, "Belki")["i"], "s-friedrich-ay-6"), (find(9, "Tomurcuk")["i"], "AI-b"),
]
SHOTS.sort()
def shot_at(i): return [img for k, img in SHOTS if k <= i][-1]

# ---------- cuts ----------
def runs(pred):
    sel = [w["i"] for w in W_ if pred(w)]; out = []
    for i in sel:
        if out and out[-1][1] == i - 1: out[-1][1] = i
        else: out.append([i, i])
    return out
def sent_last(sec):  # index of the last sentence in a section
    return max(w["sent"] for w in W_ if w["sec"] == sec)
CUTS = {
    "Hegel-16x9": dict(W=1920, H=1080, runs=[[0, len(W_) - 1]]),
    "Hegel-Reels-9x16": dict(W=1080, H=1920, runs=runs(lambda w: (w["sec"] == 1 and w["par"] < 2) or w["sec"] in (4, 6) or (w["sec"] == 9 and w["par"] >= 1))),
    "Shorts-1-tez-antitez": dict(W=1080, H=1920, runs=runs(lambda w: w["sec"] == 3)),
    "Shorts-2-kazanan-kole": dict(W=1080, H=1920, runs=runs(lambda w: w["sec"] == 6 and w["par"] <= 2)),
    "Shorts-3-dunya-ruhu": dict(W=1080, H=1920, runs=runs(lambda w: (w["sec"] == 1 and w["par"] < 2) or (w["sec"] == 7 and w["sent"] == sent_last(7)))),
}

# ---------- stills ----------
def still(img, W, H):
    out = os.path.join(TMP, f"{img}-{W}x{H}.png")
    if os.path.exists(out): return out
    src = os.path.join(G, img + (".png" if os.path.exists(os.path.join(G, img + ".png")) else ".jpg"))
    im = Image.open(src).convert("RGB"); SW, SH = 2 * W, 2 * H
    bg = im.copy(); r = max(SW / bg.width, SH / bg.height)
    bg = bg.resize((math.ceil(bg.width * r), math.ceil(bg.height * r)), Image.LANCZOS)
    bg = bg.crop(((bg.width - SW) // 2, (bg.height - SH) // 2, (bg.width - SW) // 2 + SW, (bg.height - SH) // 2 + SH))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(SW / 40))).enhance(0.55)
    r = min(SW / im.width, SH / im.height)
    if W < H: r = min(SW / im.width, SH * 0.78 / im.height)       # vertical: keep a little blur above/below
    fg = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    bg.paste(fg, ((SW - fg.width) // 2, (SH - fg.height) // 2)); bg.save(out); return out

MOVES = [(1.00, 1.10, 0.5, 0.5, 0.45, 0.55), (1.10, 1.00, 0.45, 0.55, 0.5, 0.5), (1.02, 1.12, 0.55, 0.45, 0.5, 0.45), (1.12, 1.02, 0.5, 0.5, 0.55, 0.45)]

def ts(t):
    t = max(0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
def srt_ts(t):
    ms = int(round(max(0, t) * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

def build(name, W, H, runs):
    vert = H > W
    # ranges in source time, split also at paragraph gaps -> output timeline
    rng = []
    for a, b in runs:
        s0 = max(0.0, W_[a]["s"] - (0.12 if not rng else 0.25)); s1 = W_[b]["e"] + 0.35
        if b + 1 < len(W_): s1 = min(s1, (W_[b]["e"] + W_[b + 1]["s"]) / 2 + 0.1)
        rng.append((s0, s1, a, b))
    TAIL = 2.5 if not vert else 1.2
    words, off, shots = [], 0.0, []
    for s0, s1, a, b in rng:
        for w in W_[a:b + 1]: words.append(dict(w, s=w["s"] - s0 + off, e=w["e"] - s0 + off))
        for k in range(a, b + 1):
            img = shot_at(k)
            if not shots or shots[-1][1] != img:
                t = off if k == a else W_[k]["s"] - s0 + off - 0.3
                if shots and t - shots[-1][0] < 1.5: shots[-1] = (shots[-1][0], img)   # avoid flashes
                else: shots.append((max(0.0, t), img))
        off += s1 - s0
    DUR = round(off + TAIL, 2)
    shots[0] = (0.0, shots[0][1])
    # ---- audio: cut ranges, tiny fades, concat ----
    af, ins = [], []
    for j, (s0, s1, a, b) in enumerate(rng):
        d = s1 - s0
        af.append(f"[0:a]atrim={s0:.3f}:{s1:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={d - 0.06:.3f}:d=0.06[r{j}]")
    af.append("".join(f"[r{j}]" for j in range(len(rng))) + f"concat=n={len(rng)}:v=0:a=1,aresample=48000,pan=stereo|c0=c0|c1=c0,apad,atrim=0:{DUR},asplit=2[vo][sc]")
    mstart = 2.0 if not vert else 30.0
    af.append(f"[1:a]aresample=48000,atrim=start={mstart},asetpts=PTS-STARTPTS,atrim=0:{DUR},volume=0.32,afade=t=in:d=1.5,afade=t=out:st={DUR - 3}:d=3[mu]")
    af.append("[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600:makeup=1[md];[vo][md]amix=inputs=2:normalize=0:duration=first[a]")
    mix = os.path.join(TMP, name + "-mix.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-i", MUSIC, "-filter_complex", ";".join(af), "-map", "[a]", "-c:a", "pcm_s24le", mix], check=True)
    # ---- picture ----
    ends = [s for s, _ in shots[1:]] + [DUR]
    inputs, ch = [], []
    for i, ((t0, img), t1) in enumerate(zip(shots, ends)):
        seg = t1 - t0 + (XF if i < len(shots) - 1 else 0); n = int(math.ceil(seg * FPS)) + 2
        z0, z1, ax0, ax1, ay0, ay1 = MOVES[i % 4]
        e = f"(0.5-0.5*cos(PI*on/{n - 1}))"
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{n / FPS:.3f}", "-i", still(img, W, H)]
        ch.append(f"[{i}:v]zoompan=z='{z0}+({z1}-{z0})*{e}':x='(iw-iw/zoom)*({ax0}+({ax1}-{ax0})*{e})':y='(ih-ih/zoom)*({ay0}+({ay1}-{ay0})*{e})':d=1:s={W}x{H}:fps={FPS},"
                  f"trim=duration={seg:.3f},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},format=yuv420p[s{i}]")
    fc = ";".join(ch); prev = "s0"
    for i in range(1, len(shots)):
        fc += f";[{prev}][s{i}]xfade=transition=fade:duration={XF}:offset={ends[i - 1]:.3f}[x{i}]"; prev = f"x{i}"
    assf = os.path.join(TMP, name + ".ass")
    fc += f";[{prev}]trim=duration={DUR},subtitles='{assf}':fontsdir='{os.path.join(K, 'fonts')}',format=yuv420p[v]"
    # ---- captions ----
    mxw, mxc = (3, 20) if vert else (6, 40)
    chunks, cur = [], []
    for k, w in enumerate(words):
        cur.append(w); nx = words[k + 1] if k + 1 < len(words) else None
        txt = " ".join(x["w"] for x in cur)
        if (nx is None or len(cur) >= mxw or len(txt) + 1 + len(nx["w"]) > mxc or re.search(r"[.,?!:;…\"]$", w["w"])
                or nx["par"] != w["par"] or nx["sec"] != w["sec"] or nx["s"] - w["e"] > 0.45):
            chunks.append(cur); cur = []
    fs, ol, sh, mv = (80, 3.2, 2.2, 470) if vert else (56, 2.4, 1.6, 64)
    ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
           "[V4+ Styles]", "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
           f"Style: Cap,Montserrat ExtraBold,{fs},&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,1,0,1,{ol},{sh},2,70,70,{mv},1",
           f"Style: Kin,Playfair Display Black,{110 if vert else 96},&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,2,0,1,{ol + 0.6},{sh + 1},5,40,40,0,1",
           f"Style: KinS,Montserrat ExtraBold,{68 if vert else 44},&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,2,0,1,{ol},{sh},5,40,40,0,1",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    srt = []
    for ci, c in enumerate(chunks):
        c_end = min(c[-1]["e"] + 0.3, chunks[ci + 1][0]["s"]) if ci + 1 < len(chunks) else c[-1]["e"] + 0.6
        srt.append(f"{ci + 1}\n{srt_ts(c[0]['s'])} --> {srt_ts(c_end)}\n{' '.join(x['w'] for x in c)}\n")
        for j, w in enumerate(c):
            s = c[0]["s"] if j == 0 else w["s"]; e = c[j + 1]["s"] if j + 1 < len(c) else c_end
            parts = [(f"{{\\1a&H00&\\fscx107\\fscy107}}{x['w']}{{\\1a&H38&\\fscx100\\fscy100}}" if m == j else x["w"]) for m, x in enumerate(c)]
            ass.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\1a&H38&}}{' '.join(parts)}")
    # ---- kinetic typography (only where the source words are inside this cut) ----
    T = {w["i"]: w for w in words}
    def at(sec, word, nth=0, end=False):
        w = find(sec, word, nth); return (T[w["i"]]["e"] if end else T[w["i"]]["s"]) if w["i"] in T else None
    def sec_end(sec):
        ws = [w for w in words if w["sec"] == sec]; return ws[-1]["e"] + 0.4 if ws else None
    ky = 360 if vert else 250
    def kin(t0, t1, text, y, style="Kin", fade=(250, 250)):
        if t0 is None or t1 is None or t1 <= t0: return
        ass.append(f"Dialogue: 2,{ts(t0)},{ts(t1)},{style},,0,0,0,,{{\\fad({fade[0]},{fade[1]})\\pos({W // 2},{y})}}{text}")
    def bar(t0, t1, w, h, y):   # red strike line, drawn left->right
        if t0 is None or t1 is None or t1 <= t0: return
        w, h = int(w), max(8, int(h))
        ass.append(f"Dialogue: 3,{ts(t0)},{ts(t1)},Kin,,0,0,0,,{{\\an5\\pos({W // 2},{y})\\bord0\\shad0\\1c&H2A2AE6&\\fscx0\\t(0,350,\\fscx100)\\fad(0,250)\\p1}}m 0 0 l {w} 0 {w} {h} 0 {h}{{\\p0}}")
    # 3: TEZ - ANTİTEZ - SENTEZ, struck through at "kullanmadı", then AUFHEBUNG
    t1, t2, t3 = at(3, "tez,"), at(3, "antitez,"), at(3, "sentez."); strike = at(3, "kullanmadı.", end=True); hb = at(3, "Aufhebung.")
    if t1 is not None:
        kfs = 120 if vert else 110
        if vert:
            lines = [("TEZ", t1, ky - 150), ("ANTİTEZ", t2, ky), ("SENTEZ", t3, ky + 150)]
            for txt, t, y in lines:
                kin(t, hb - 0.2, f"{{\\fs{kfs}}}{txt}", y, fade=(200, 250))
                bar(strike, hb - 0.2, len(txt) * kfs * 0.5 + 20, kfs * 0.1, y + 6)
        else:
            kin(t1, t2, f"TEZ", ky, fade=(200, 0)); kin(t2, t3, "TEZ – ANTİTEZ", ky, fade=(0, 0)); kin(t3, strike, "TEZ – ANTİTEZ – SENTEZ", ky, fade=(0, 0))
            kin(strike, hb - 0.2, "TEZ – ANTİTEZ – SENTEZ", ky, fade=(0, 250)); bar(strike, hb - 0.2, 22 * 96 * 0.5, 11, ky + 6)
        kin(hb, sec_end(3) + (1.0 if vert else 0), "AUFHEBUNG", ky + (0 if not vert else 0), fade=(300, 300))
    # 4: AUFHEBUNG = kaldırmak · saklamak · yükseltmek
    a0 = at(4, "Aufhebung");
    if a0 is not None:
        a1, a2, a3 = at(4, "kaldırmak,"), at(4, "saklamak"), at(4, "taşımak.", end=True)
        off4 = at(4, "Hegel bunu") - 0.2
        kin(a0, off4, "AUFHEBUNG", ky, fade=(300, 300))
        sub = ky + (110 if vert else 95)
        if vert:
            kin(a1, off4, "kaldırmak", sub, "KinS", (200, 300)); kin(a2, off4, "saklamak", sub + 90, "KinS", (200, 300)); kin(a3 - 0.6, off4, "yükseltmek", sub + 180, "KinS", (200, 300))
        else:
            kin(a1, a2, "= kaldırmak", sub, "KinS", (200, 0)); kin(a2, a3 - 0.6, "= kaldırmak · saklamak", sub, "KinS", (0, 0)); kin(a3 - 0.6, off4, "= kaldırmak · saklamak · yükseltmek", sub, "KinS", (0, 300))
    # 5: VARLIK -> HİÇLİK -> OLUŞ
    v0 = at(5, "varlığı")
    if v0 is not None:
        h0, o0, end5 = at(5, "hiçliğe"), at(5, "oluş."), sec_end(5)
        kin(v0, h0, "VARLIK", ky, fade=(250, 0)); kin(h0, o0, "VARLIK → HİÇLİK", ky, fade=(0, 0)); kin(o0, end5, "VARLIK → HİÇLİK → OLUŞ", ky, fade=(0, 400))
    open(assf, "w").write("\n".join(ass) + "\n")
    open(os.path.join(OUT, name + ".srt"), "w").write("\n".join(srt))
    pic = os.path.join(TMP, name + "-pic.mp4")
    if not os.environ.get("SKIP_PIC"): subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-r", str(FPS), pic], check=True)
    mst = os.path.join(TMP, name + "-master.wav")
    subprocess.run([sys.executable, MASTER, mix, mst, "--I", "-14", "--TP", "-2", "--limit"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pic, "-i", mst, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
                    "-ar", "48000", "-t", f"{DUR:.3f}", "-movflags", "+faststart", os.path.join(OUT, name + ".mp4")], check=True)
    json.dump({"dur": DUR, "shots": shots, "last": words[-1]["w"], "ranges": [(round(a, 2), round(b, 2)) for a, b, _, _ in rng]},
              open(os.path.join(TMP, name + ".json"), "w"), ensure_ascii=False)
    print(name, "DUR", DUR, "shots", len(shots), "last word", words[-1]["w"], flush=True)

if __name__ == "__main__":
    for n in (sys.argv[1:] or CUTS):
        c = CUTS[n]; build(n, c["W"], c["H"], c["runs"])

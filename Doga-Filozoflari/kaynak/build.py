# Doga Filozoflari: all deliverables from one voice take.  Usage (from Doga-Filozoflari/):  python3 kaynak/build.py [name ...]
# Picture: PIL pre-composed stills (blurred self as background + full painting) -> ffmpeg zoompan Ken Burns + xfade.
# Captions + kinetic type: ASS (libass). Mix: VO + ducked CC0 music, then cinecode master_audio.py -> -14 LUFS.
import json, subprocess, os, math, sys, re
from PIL import Image, ImageFilter, ImageEnhance

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); K = os.path.join(R, "kaynak")
G = os.path.join(R, "gorseller", "secilen"); OUT = os.path.join(R, "teslim"); TMP = os.path.join(K, "tmp")
VO = os.path.join(R, "ses", "Doga-tam.wav")
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
from shots import SHOTS_SPEC
SHOTS = [(find(sec, w)["i"], img) for sec, w, img in SHOTS_SPEC]
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
def sents(sec): return sorted({w["sent"] for w in W_ if w["sec"] == sec})
def sent_of(sec, word): return find(sec, word)["sent"]
S8 = sents(8)
CUTS = {
    "Doga-Filozoflari-16x9": dict(W=1920, H=1080, sel=lambda w: True, limit=None, drop=[]),
    "Doga-Filozoflari-Dikey-9x16": dict(W=1080, H=1920, limit=180,
        sel=lambda w: w["sec"] in (0, 4, 5, 7) or (w["sec"] == 1 and w["sent"] == sent_of(1, "Yunanlar buna")) or (w["sec"] == 2 and w["sent"] <= sent_of(2, "Tek bir madde,"))
            or (w["sec"] == 8 and w["sent"] >= S8[-2]),
        drop=[[(5, sent_of(5, "Öğrencisi Zenon"))], [(7, sent_of(7, "Demokritos şöyle")), (7, sent_of(7, "Gerçekte yalnızca")), (7, sent_of(7, "Ona gülen"))],
              [(2, sent_of(2, "Tohumlar"))], [(4, sent_of(4, "Gece ile"))], [(5, sent_of(5, "O hâlde hiçbir"))], [(4, sent_of(4, "Kibirli,"))],
              [(2, sent_of(2, "Su donar,"))], [(5, sent_of(5, "Duyular yalan"))]]),
}
def make_ranges(sel, vert):
    rs = runs(sel); rng = []
    for a, b in rs:
        s0 = max(0.0, W_[a]["s"] - (0.12 if not rng else 0.25)); s1 = W_[b]["e"] + 0.35
        if b + 1 < len(W_): s1 = min(s1, (W_[b]["e"] + W_[b + 1]["s"]) / 2 + 0.1)
        rng.append((s0, s1, a, b))
    return rng, round(sum(b - a for a, b, _, _ in rng) + (1.2 if vert else 2.5), 2)
def plan(c):
    vert = c["H"] > c["W"]; sel = c["sel"]; dropped = []
    rng, d = make_ranges(sel, vert)
    for grp in c["drop"]:
        if c["limit"] is None or d <= c["limit"]: break
        dropped += grp; ds = set(dropped)
        sel = (lambda base, ds: (lambda w: base(w) and (w["sec"], w["sent"]) not in ds))(c["sel"], ds)
        rng, d = make_ranges(sel, vert)
    return rng, d, dropped

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

# vertical: full-screen only. (pan from, pan to) as fraction of the horizontal travel; portraits use fx as crop centre.
VPAN = {"AI-a": (0.05, 0.9), "AI-b": (0.3, 0.7), "AI-c": (0.62, 1.0), "atina-merkez": (0.3, 0.7), "atina-genis": (0.35, 0.65),
        "rubens-ikili": (0.08, 0.92), "tutulma": (0.45, 0.55), "poseidon": (0.45, 0.55), "kaplumbaga": (0.3, 0.6), "thales-nurnberg": (0.2, 0.8), "brugghen-herakleitos": (0.3, 0.3), "brugghen-cift": (0.15, 0.85)}
VSUB = {"brugghen-cift": "demokritos"}   # diptych seam shows when panned vertically
def still_v(img, W, H):
    img = VSUB.get(img, img)
    src = os.path.join(G, img + (".png" if os.path.exists(os.path.join(G, img + ".png")) else ".jpg"))
    im = Image.open(src).convert("RGB"); SW, SH = 2 * W, 2 * H
    r = max(SW / im.width, SH / im.height); im = im.resize((math.ceil(im.width * r), math.ceil(im.height * r)), Image.LANCZOS)
    if im.width > SW * 1.35:     # wide painting: keep full width, pan across
        out = os.path.join(TMP, f"{img}-V{W}x{H}.png")
        im = im.crop((0, (im.height - SH) // 2, im.width, (im.height - SH) // 2 + SH)); im.save(out)
        return out, "pan", VPAN.get(img, (0.3, 0.7))
    out = os.path.join(TMP, f"{img}-F{W}x{H}.png"); fx = VPAN.get(img, (0.5, 0.5)); c = (fx[0] + fx[1]) / 2
    x = int((im.width - SW) * c); y = (im.height - SH) // 2
    im.crop((x, y, x + SW, y + SH)).save(out); return out, "zoom", None

MOVES = [(1.00, 1.10, 0.5, 0.5, 0.45, 0.55), (1.10, 1.00, 0.45, 0.55, 0.5, 0.5), (1.02, 1.12, 0.55, 0.45, 0.5, 0.45), (1.12, 1.02, 0.5, 0.5, 0.55, 0.45)]

def ts(t):
    t = max(0, t); return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"
def srt_ts(t):
    ms = int(round(max(0, t) * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

def build(name, W, H, rng):
    vert = H > W
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
        if vert:
            path, mode, pan = still_v(img, W, H)
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{n / FPS:.3f}", "-i", path]
            if mode == "pan":
                p0, p1 = pan if i % 2 == 0 else pan[::-1]
                ch.append(f"[{i}:v]crop=w={2 * W}:h={2 * H}:x='(iw-ow)*({p0}+({p1}-{p0})*(0.5-0.5*cos(PI*min(t/{seg:.3f},1))))':y=0,scale={W}:{H}:flags=lanczos,"
                          f"trim=duration={seg:.3f},setpts=PTS-STARTPTS,fps={FPS},settb=1/{FPS},format=yuv420p[s{i}]")
                continue
        else:
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
    chunks = [c for c in chunks if not (len(c) == 1 and c[0]["w"] in ("TEZ.", "ANTİTEZ.", "SENTEZ."))]
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
    # section cards: big TEZ / ANTİTEZ / SENTEZ at the start of 2, 4, 6 (spoken word, caption hidden)
    for sec, word in ((2, "TEZ."), (4, "ANTİTEZ."), (6, "SENTEZ.")):
        t0 = at(sec, word)
        if t0 is None: continue
        t1 = at(sec, word, end=True) + 1.6
        big = 230 if vert else 200
        ass.append(f"Dialogue: 4,{ts(max(0, t0 - 0.15))},{ts(t1)},Kin,,0,0,0,,{{\\an5\\pos({W // 2},{H // 2 - (120 if vert else 40)})\\fs{big}\\fsp{14}\\fscx70\\fscy70\\alpha&HFF&\\t(0,260,\\fscx100\\fscy100\\alpha&H00&)\\t(260,1400,\\fscx106\\fscy106)\\fad(0,350)}}{word[:-1]}")
        bar(t0 + 0.25, t1, len(word) * big * 0.55, big * 0.06, H // 2 - (120 if vert else 40) + int(big * 0.62))
    # 1: TEZ · ANTİTEZ · SENTEZ build-up
    t1, t2, t3 = at(1, "tez,"), at(1, "antitez,"), at(1, "sentez.")
    if t1 is not None:
        e1 = at(1, "Hegel'in") - 0.1
        if vert:
            for txt, t, y in (("TEZ", t1, ky - 150), ("ANTİTEZ", t2, ky), ("SENTEZ", t3, ky + 150)): kin(t, e1, f"{{\\fs120}}{txt}", y, fade=(200, 250))
        else:
            kin(t1, t2, "TEZ", ky, fade=(200, 0)); kin(t2, t3, "TEZ · ANTİTEZ", ky, fade=(0, 0)); kin(t3, e1, "TEZ · ANTİTEZ · SENTEZ", ky, fade=(0, 300))
    # 1: ARKHE
    ak = at(1, "arkhe")
    if ak is not None: kin(ak, at(1, "kök.", end=True) + 0.6, "ἀρχή · ARKHE", ky, fade=(250, 300))
    # 3: APEIRON
    ap = at(3, "apeirondur:")
    if ap is not None: kin(ap, at(3, "olmayan.", end=True) + 0.5, "APEIRON", ky, fade=(250, 300))
    # 6: four roots
    r0 = at(6, "toprak,")
    if r0 is not None:
        r1, r2, r3, e6 = at(6, "su,"), at(6, "hava"), at(6, "ateş."), at(6, "ateş.", end=True) + 1.2
        if vert:
            for txt, t, y in (("TOPRAK", r0, ky - 135), ("SU", r1, ky - 45), ("HAVA", r2, ky + 45), ("ATEŞ", r3, ky + 135)): kin(t, e6, f"{{\\fs96}}{txt}", y, fade=(150, 300))
        else:
            kin(r0, r1, "TOPRAK", ky, fade=(150, 0)); kin(r1, r2, "TOPRAK · SU", ky, fade=(0, 0)); kin(r2, r3, "TOPRAK · SU · HAVA", ky, fade=(0, 0)); kin(r3, e6, "TOPRAK · SU · HAVA · ATEŞ", ky, fade=(0, 300))
    # 7: ATOM + BOŞLUK
    ab = at(7, "atomlar", 0)
    if ab is not None:
        kin(ab, at(7, "demektir.", end=True) + 0.3, "ATOM + BOŞLUK", ky, fade=(200, 300))
        bz = at(7, "\"bölünemez\"")
        if bz is not None: kin(bz, at(7, "demektir.", end=True) + 0.3, "ἄτομος = bölünemez", ky + (120 if vert else 100), "KinS", (200, 300))
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
        c = CUTS[n]; rng, d, dropped = plan(c)
        print(n, "planned", d, "s; dropped", dropped, flush=True)
        if os.environ.get("PLAN_ONLY"): continue
        build(n, c["W"], c["H"], rng)

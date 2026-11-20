"""Sol Beyin Ego ses tasarimi (anlatim haric; anlatim mix.sh'de eklenir, yatak altinda kisilir).
Imza motifi: iki yarimkure. Sol kulakta sicak alcak nota (anlatici sol beyin), sag kulakta ona cevap veren
yuksek cam gibi nota (sessiz sag beyin). Bolum gecislerinde (seam) bu ikili calar.
Kullanim:  MODE=long|short python3 -m sfx kaynak/cues.py   (proje kokunden degil, sfx'in oldugu yerden)"""
import json, os
from sfx import synth

HERE = os.path.dirname(os.path.abspath(__file__))
MODE = os.environ.get("MODE", "long")
TL = json.load(open(os.path.join(HERE, "timeline.json")))
AEND, TAIL = TL["aend"], TL["tail"]
SEGS = (TL.get("short") or {}).get("segs", [])
SDUR = (TL.get("short") or {}).get("dur", 0)

def to_out(T):
    """uzun video zamani -> bu ciktinin zamani; kisa videoda kesilen yere duserse None"""
    if MODE == "long": return T
    for ls, le, ss in SEGS:
        if ls - 0.05 <= T < le: return ss + max(0.0, T - ls)
    if T >= AEND: return SDUR + (T - AEND)
    return None

DUR = (AEND if MODE == "long" else SDUR) + TAIL
json.dump({"duration": round(DUR, 3)}, open(os.path.join(HERE, f"tl-{MODE}.json"), "w"))
TIMELINE = os.path.join(HERE, f"tl-{MODE}.json")
OUT = os.path.join(HERE, "audio", f"bed-{MODE}.wav")
TARGET_LUFS = -24.0
SEED = 7

# Re minor -> Re major (kapanista "varim" aydinligi)
N = {"D2": 73.42, "A2": 110.0, "Bb2": 116.54, "C3": 130.81, "D3": 146.83, "E3": 164.81, "F3": 174.61, "F#3": 185.0, "G3": 196.0,
     "A3": 220.0, "Bb3": 233.08, "C4": 261.63, "D4": 293.66, "F4": 349.23, "F#4": 369.99, "A4": 440.0, "D5": 587.33, "A5": 880.0}
Dm, Bb, F, C, Gm, D = ([N[k] for k in ks] for ks in (["D3", "F3", "A3"], ["Bb2", "D3", "F3"], ["A2", "C3", "F3"], ["C3", "E3", "G3"], ["Bb2", "D3", "G3"], ["D3", "F#3", "A3"]))

def score(mix, tl):
    shots, bv = TL["shots"], TL["bv"]
    global SW
    SW = TL["sw"]
    seams = [s["t0"] for s in shots if "seam" in s["fx"]]
    # akor degisimleri: her bolum basinda (seam), ortalarda bir ara akor; "Ben varim" ile Re majore
    marks = sorted([0.0] + seams)
    prog = [Dm, Bb, F, C, Gm, Bb, Dm, F, C]
    chords = []
    for i, m in enumerate(marks):
        nxt = marks[i + 1] if i + 1 < len(marks) else bv
        if m >= bv: break
        chords.append((m, prog[(2 * i) % len(prog)]))
        if nxt - m > 18: chords.append(((m + nxt) / 2, prog[(2 * i + 1) % len(prog)]))
    chords += [(bv, D), (bv + 9, Bb), (bv + 16, D)]
    # cikti zamanina cevir (kisa videoda kesilenler duser)
    out = []
    for t, c in chords:
        o = to_out(t)
        if o is not None and (not out or o - out[-1][0] > 3): out.append((o, c))
    if MODE == "short" and out and out[0][0] > 0: out.insert(0, (0.0, Dm))
    # muzik yatagi artik PD Satie kayitlari (mix.sh); burada yalniz efektler

    # imza: seam gecislerinde sol-sicak / sag-cam ikilisi + yumusak hava
    for t in seams:
        o = to_out(t)
        if o is None: continue
        lo, hi = (349.23, 1046.5) if t < SW else (N["D4"], N["A5"])   # Gnossienne fa minor / Gymnopedie re
        mix.put(o - 0.05, synth.blip(lo, dur=0.9, tau=0.35), 0.3, pan=-0.75)
        mix.put(o + 0.22, synth.blip(hi, dur=1.1, tau=0.45), 0.18, pan=0.75)
        mix.put(o - 0.4, synth.whoosh(0.9, 300, 1800, peak=0.6), 0.18, pan=0.0)
    # sert vurus: "Peki bu karakter..." (fisiltidan sonra etkili giris), videoda tek
    peki = next(s["t0"] for s in shots if s["k"] == "s05-projektor")
    o = to_out(peki)
    if o is not None:
        mix.put(o - 2.2, synth.riser(2.2, 120, 2400), 0.22)
        mix.put(o, synth.impact(1.6), 0.8)
    # kaza / acil: alcak hava
    for s in shots:
        if "flash" in s["fx"]:
            o = to_out(s["t0"])
            if o is not None: mix.put(o - 0.3, synth.whoosh(1.0, 1200, 120, peak=0.35), 0.3)
    # daktilo plani: tuslar
    for s in shots:
        if s["k"] == "s17-daktilo":
            o = to_out(s["t0"])
            if o is not None: mix.typing(o + 0.4, o + 3.6, 22, gain=(0.08, 0.13))
    # etiketler: kucuk kalem cizgisi
    for t in TL["labels"]:
        o = to_out(t)
        if o is not None: mix.put(o + 0.05, synth.scratch(0.5), 0.12, pan=0.0)
    # "Ben varim": Re major can
    o = to_out(bv)
    if o is not None: mix.put(o, synth.chime([N["D4"], N["F#4"], N["A4"], N["D5"]], dur=3.0, tau=1.2), 0.32)
    # abone animasyonu: tik + zil
    subs = [90, 255] if MODE == "long" else [TL["short"]["sub"]]
    for st in subs:
        mix.put(st + 0.1, synth.whoosh(0.45, 400, 2400, peak=0.4), 0.15, pan=-0.5)
        mix.put(st + 1.5, synth.click(1600), 0.35, pan=-0.3)
        mix.put(st + 2.6, synth.click(2200), 0.25, pan=-0.2)
        mix.put(st + 2.62, synth.chime([N["A5"], 1174.66, 1760.0], dur=1.4, tau=0.4), 0.2, pan=-0.2)
    # kapanis: takipte kal, adresler
    e = to_out(AEND)
    mix.put(e + 1.0, synth.whoosh(0.7, 200, 2000, peak=0.5), 0.2)
    mix.put(e + 1.2, synth.chime([N["D4"], N["A4"], N["D5"]], dur=2.0, tau=0.8), 0.25)
    mix.put(e + 5.6, synth.pop(500, 900), 0.2)

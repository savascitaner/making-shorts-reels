# Sercan (anlatıcı + Einstein + kancalar) + Tarkan (Bohr) -> ses/vo.mp3 + kaynak/words-raw.json + ses/segmentler.json
import numpy as np, subprocess, json, sys
SR = 44100; HIZ = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
def load(p):
    b = subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(b, np.float32).copy()
S = load("ses/sercan.mp3"); B = load("ses/bohr.mp3")
def rms(x): return np.sqrt(np.mean(x[np.abs(x) > 0.01] ** 2))
B *= rms(S) / rms(B)
SW = json.load(open("ses/sercan-words.json")); BW = json.load(open("ses/bohr-words.json"))
# whisper Sercan'da 28.6-34.6 aralığını atladı: elle (kısa kesitte yeniden transkribe edilen) kelimeler
yama = [("Tanrı",28.80,29.56),("evrenle",29.56,30.10),("zar",30.10,30.34),("atmaz!",30.34,30.72),("Bohr'un",31.20,32.06),("cevabı",32.06,32.54),("ise",32.54,32.66),("en",32.66,33.12),("az",33.12,33.38),("onun",33.38,33.58),("kadar",33.58,33.90),("efsane:",33.90,34.52)]
SW = [w for w in SW if not (28.6 < w["s"] < 35.0)] + [{"w":a,"s":b,"e":c} for a,b,c in yama]
SW = [dict(w, w="korktuğu") if w["w"] == "kokuyor." else w for w in SW]
SW = [w for w in SW if w["w"] != "Korktuğu"]
SW.sort(key=lambda w: w["s"])
def cut(x, a, b):
    y = x[int(a*SR):int(b*SR) if b else None].copy(); th = 10**(-45/20); i = np.where(np.abs(y) > th)[0]
    s0 = max(0, i[0] - int(0.03*SR)); y = y[s0:i[-1] + int(0.08*SR)]
    n = int(0.015*SR); y[:n] *= np.linspace(0,1,n); y[-n:] *= np.linspace(1,0,n); return y, a + s0/SR
plan = [("S1",S,SW,0,19.95,"S",0.6),("B1",B,BW,0,10.7,"B",0.5),("S2",S,SW,19.95,34.8,"S",0.55),("B2",B,BW,10.7,15.8,"B",0.6),
        ("S3",S,SW,34.8,73.65,"S",0.45),("B3",B,BW,15.8,None,"B",0.55),("S4",S,SW,73.65,None,"S",0.0)]
out, segs, words, t = [], [], [], 0.0
for ad, src, ww, a, b, kim, gap in plan:
    y, a0 = cut(src, a, b); d = len(y)/SR
    for w in ww:
        if w["s"] >= a - 0.05 and (b is None or w["s"] < b):
            words.append({"w": w["w"], "s": round((t + w["s"] - a0)/HIZ, 3), "e": round((t + w["e"] - a0)/HIZ, 3), "p": 1.0, "k": kim})
    segs.append({"ad": ad, "kim": kim, "bas": round(t/HIZ, 2), "son": round((t + d)/HIZ, 2)})
    out += [y, np.zeros(int(gap*SR), np.float32)]; t += d + gap
y = np.concatenate(out); y /= np.abs(y).max() / 0.89
open("/tmp/bevo.f32","wb").write(y.astype(np.float32).tobytes())
af = ["-af", f"atempo={HIZ}"] if HIZ != 1.0 else []
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","/tmp/bevo.f32",*af,"-b:a","192k","ses/vo.mp3"])
json.dump(words, open("kaynak/words-raw.json","w"), ensure_ascii=False, indent=0)
json.dump(segs, open("ses/segmentler.json","w"), ensure_ascii=False, indent=0)
print(round(len(y)/SR/HIZ, 2), len(words)); [print(s) for s in segs]

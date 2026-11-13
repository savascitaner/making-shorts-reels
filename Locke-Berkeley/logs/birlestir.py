# Sercan (kanca + ağaç bilmecesi + Berkeley + anlatıcı) + Serkan Yılmaz (Locke) -> vo.mp3 + segmentler.json
import numpy as np, subprocess, json
SR = 44100
def load(p):
    b = subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(b, np.float32).copy()
S = load("sercan.mp3"); L = load("locke.mp3"); A = load("agac.mp3")
def rms(x): return np.sqrt(np.mean(x[np.abs(x)>0.01]**2))
L *= rms(S[int(6*SR):]) / rms(L)
def seg(x, a, b):
    y = x[int(a*SR):int(b*SR) if b else None].copy()
    th = 10**(-45/20); i = np.where(np.abs(y) > th)[0]
    y = y[max(0,i[0]-int(0.03*SR)):i[-1]+int(0.08*SR)]
    n = int(0.015*SR); y[:n] *= np.linspace(0,1,n); y[-n:] *= np.linspace(1,0,n); return y
plan = [("kanca",S,0,5.5,0.7),("L1",L,0,10.2,0.35),("B1",S,5.5,13.65,0.35),("L2",L,10.6,23.8,0.35),
        ("B2",S,13.65,27.5,0.35),("L3",L,23.9,32.7,0.35),("B3",S,27.5,40.7,0.8),("agac",A,0,None,0.7),("L4",L,32.8,None,0.45),
        ("B4",S,40.7,55.4,0.9),("kapanis",S,55.4,None,0.0)]
out, segs, t = [], [], 0.0
for name, src, a, b, gap in plan:
    y = seg(src, a, b); segs.append({"ad":name,"bas":round(t,2),"son":round(t+len(y)/SR,2),"kaynak_bas":a})
    out += [y, np.zeros(int(gap*SR), np.float32)]; t += len(y)/SR + gap
y = np.concatenate(out); y /= np.abs(y).max() / 0.89
open("/tmp/lbvo.f32","wb").write(y.astype(np.float32).tobytes())
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","/tmp/lbvo.f32","-b:a","192k","vo.mp3"])
json.dump(segs, open("segmentler.json","w"), ensure_ascii=False, indent=0)
print(round(len(y)/SR,2)); [print(s) for s in segs]

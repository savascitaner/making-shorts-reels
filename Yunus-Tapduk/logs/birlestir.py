# Tapduk (Sercan) + Yunus (Serkan Yılmaz) -> ses/vo.mp3 + ses/segmentler.json
import numpy as np, subprocess, json, os
os.chdir(os.path.join(os.path.dirname(__file__), "..", "ses"))
SR = 44100
def load(p):
    b = subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(b, np.float32).copy()
T = load("tapduk.mp3"); Y = load("yunus.mp3")
def rms(x): return np.sqrt(np.mean(x[np.abs(x)>0.01]**2))
Y *= rms(T[int(3*SR):]) / rms(Y[int(7*SR):])
def seg(x, a, b):
    y = x[int(a*SR):int(b*SR) if b else None].copy()
    th = 10**(-45/20); i = np.where(np.abs(y) > th)[0]
    y = y[max(0,i[0]-int(0.03*SR)):i[-1]+int(0.08*SR)]
    n = int(0.015*SR); y[:n] *= np.linspace(0,1,n); y[-n:] *= np.linspace(1,0,n); return y
# (ad, kaynak, bas, son, önceki_bosluk)
plan = [("A1",Y,0,3.3,0.0),("A2",Y,3.5,7.2,0.7),("B",T,0,2.7,0.5),
        ("T1",T,3.0,7.7,4.0),("Y1",Y,7.3,10.3,0.5),("T2",T,7.8,12.5,0.5),("Y2",Y,10.3,17.2,0.5),
        ("T3",T,12.6,21.0,1.2),("Y3",Y,17.2,25.4,12.0),("T4",T,21.0,24.7,14.0),
        ("Y4",Y,25.4,34.0,1.5),("C",Y,34.0,None,5.0),("CTA",T,24.7,None,7.0)]
out, segs, t = [], [], 0.0
for name, src, a, b, gap in plan:
    out.append(np.zeros(int(gap*SR), np.float32)); t += gap
    y = seg(src, a, b); segs.append({"ad":name,"bas":round(t,2),"son":round(t+len(y)/SR,2),"kaynak_bas":a})
    out.append(y); t += len(y)/SR
out.append(np.zeros(int(5.0*SR), np.float32))  # kapanış kartı
y = np.concatenate(out); y /= np.abs(y).max() / 0.89
tmp = "/private/tmp/ytvo.f32"; open(tmp,"wb").write(y.astype(np.float32).tobytes())
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i",tmp,"-b:a","192k","vo.mp3"])
json.dump(segs, open("segmentler.json","w"), ensure_ascii=False, indent=0)
print(round(len(y)/SR,2)); [print(s) for s in segs]

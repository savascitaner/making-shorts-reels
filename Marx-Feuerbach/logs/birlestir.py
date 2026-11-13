# Sercan (Marx + kapanış) + Serkan Yılmaz (Feuerbach) -> vo.mp3
import numpy as np, subprocess, sys
SR = 44100
def load(p):
    b = subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(b, np.float32).copy()
S = load("vo-sercan-hizli.mp3"); F = load("feuerbach-hizli.mp3")
FT = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
def seg(x, a, b):
    y = x[int(a*SR):int(b*SR) if b else None].copy(); n = int(0.015*SR)
    y[:n] *= np.linspace(0,1,n); y[-n:] *= np.linspace(1,0,n); return y
def trim(y, th=10**(-45/20)):
    i = np.where(np.abs(y) > th)[0]; return y[max(0,i[0]-int(0.03*SR)):i[-1]+int(0.08*SR)]
M = [(0,14.72),(32.50,49.17),(68.18,87.43),(94.23,113.86),(129.53,150.40),(158.47,None)]
FS = [(a/1.05, b/1.05 if b else None) for a, b in [(0,18.6),(19.6,40.1),(40.7,47.7),(48.3,64.6),(65.0,None)]]
gap = np.zeros(int(0.4*SR), np.float32)
out = []
for i, m in enumerate(M):
    out.append(trim(seg(S, *m)))
    if i < len(FS):
        f = trim(seg(F, *FS[i])) * 1.45; out += [gap, f, gap]
y = np.concatenate(out); y /= max(1e-6, np.abs(y).max()) / 0.89
open("/tmp/vo.f32","wb").write(y.astype(np.float32).tobytes())
subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i","/tmp/vo.f32","-b:a","192k","vo.mp3"])
print(round(len(y)/SR,2))

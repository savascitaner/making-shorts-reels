# off.txt başlangıcını ses enerjisinden düzelt (whisper ilk kelimeyi 0.00'a koyuyor)
import sys, subprocess, numpy as np
for arg in sys.argv[1:]:
    k, f = arg.split("=")
    a = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout, np.float32)
    fr = 160; e = np.array([np.sqrt((a[i:i+fr]**2).mean()) for i in range(0, len(a)-fr, fr)]); db = 20*np.log10(e+1e-9)
    th = np.percentile(db, 95) - 22
    on = np.where(db > th)[0]; s0 = on[0]*0.01
    p = f"gorseller/klip/{k}/off.txt"; o0, o1 = map(float, open(p).read().split())
    open(p, "w").write(f"{max(o0, s0):.2f} {o1:.2f}"); print(k, f"{max(o0,s0):.2f} {o1:.2f}")

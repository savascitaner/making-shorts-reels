# Shorts sesi: ana kayıttan (vo-nd.wav) cümleleri dalgadaki gerçek sessizliklerden keser (whisper zamanı yalnız cümleyi bulmak için).
import subprocess, json, re
V = "../ses/vo-nd.wav"
sil = subprocess.run(["ffmpeg","-hide_banner","-i",V,"-af","silencedetect=n=-50dB:d=0.09","-f","null","-"],capture_output=True,text=True).stderr
S = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", sil)]; E = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", sil)]
sp = list(zip(S, E[:len(S)]))      # (başlangıç, bitiş)
# (whisper başlangıcı, whisper bitişi) ; ana kayıttaki zamanlar
SEN = [(371.6,376.7),(376.9,381.1),(381.2,383.3),(0.0,5.4),(263.5,272.7),(315.4,322.8),(419.5,429.7)]
segs=[]
for ws, we in SEN:
    a = [e for s,e in sp if ws-0.9 <= e <= ws+0.3]; b = [s for s,e in sp if we-0.3 <= s <= we+0.9]
    st = min(a, key=lambda e: abs(e-ws)) if a else max(0.0, ws-0.05)
    en = (min(b, key=lambda s: abs(s-we)) + 0.15) if b else we+0.3
    segs.append((round(st,3), round(en,3)))
print(segs)
ins = ["-i", V, "-i", "../ses/kapanis-shorts.mp3", "-i", "../ses/takipte-kal.mp3"]
fc = []; lab = []; t = 0.0; tl = []
for i,(a,b) in enumerate(segs):
    fc.append(f"[0:a]atrim={a}:{b},asetpts=N/SR/TB,afade=t=in:d=0.04,afade=t=out:st={b-a-0.04:.3f}:d=0.04[p{i}]"); lab.append(f"[p{i}]"); tl.append((round(t,3), round(t+b-a,3))); t += b-a
    fc.append(f"anullsrc=r=48000:cl=mono,atrim=0:0.28[g{i}]"); lab.append(f"[g{i}]"); t += 0.28
fc.append("[1:a]aresample=48000,aformat=channel_layouts=mono[q]"); lab.append("[q]"); tl.append((round(t,3), round(t+5.564,3))); t += 5.564
fc.append("anullsrc=r=48000:cl=mono,atrim=0:0.3[gq]"); lab.append("[gq]"); t += 0.3
fc.append("[2:a]aresample=48000,aformat=channel_layouts=mono[k]"); lab.append("[k]"); tl.append((round(t,3), round(t+2.116,3))); t += 2.116
fc.append("anullsrc=r=48000:cl=mono,atrim=0:5.0[ge]"); lab.append("[ge]"); t += 5.0
fc = ";".join(fc) + ";" + "".join(lab) + f"concat=n={len(lab)}:v=0:a=1[o]"
subprocess.run(["ffmpeg","-y","-loglevel","error",*ins,"-filter_complex",fc,"-map","[o]","../ses/vo-shorts-final.wav"],check=True)
json.dump({"segments":tl,"total":round(t,3)}, open("shorts-seg.json","w"))
print(tl, round(t,2))

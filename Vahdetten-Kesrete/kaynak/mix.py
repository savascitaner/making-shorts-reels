# ffmpeg ile miks: ses + CC0 müzik (konuşmada kısılır) + sentetik efektler -> -14 LUFS. Kullanım: python3 mix.py long|shorts
import json, subprocess, sys, re
FMT = sys.argv[1]
C = json.loads(open(f"cfg-{FMT}.js", encoding="utf8").read()[len("window.CFG="):-1])
DUR = C["DUR"]; OUT = f"audio/master-{FMT}.wav"
VO = "../ses/vo-uzun-final.wav" if FMT == "long" else "../ses/vo-shorts-final.wav"
S, CN = "../ses/muzik-kaynak/steller_dreams.flac", "../ses/muzik-kaynak/cosmic_navigation.flac"
inputs = []; fc = []; n = 0
def add(args):
    global n; inputs.extend(args); n += 1; return n - 1
vo = add(["-i", VO])
if FMT == "long":
    a, b, c = add(["-i", S]), add(["-i", CN]), add(["-i", S])
    fc.append(f"[{a}:a][{b}:a]acrossfade=d=8:c1=tri:c2=tri[x1];[x1][{c}:a]acrossfade=d=8:c1=tri:c2=tri[x2];[x2]atrim=0:{DUR},afade=t=in:d=3,afade=t=out:st={DUR-8}:d=8,aformat=sample_rates=48000:channel_layouts=stereo[mus]")
else:
    a = add(["-i", CN])
    fc.append(f"[{a}:a]atrim=0:{DUR},afade=t=in:d=2,afade=t=out:st={DUR-4}:d=4,aformat=sample_rates=48000:channel_layouts=stereo[mus]")
# efektler (ffmpeg lavfi ile üretilir)
def sfx(expr, delay, vol, filt=""):
    k = add(["-f", "lavfi", "-t", "6", "-i", expr]); lab = f"fx{k}"
    fc.append(f"[{k}:a]{filt}{',' if filt else ''}volume={vol},adelay={int(delay*1000)}|{int(delay*1000)},aformat=sample_rates=48000:channel_layouts=stereo[{lab}]"); return f"[{lab}]"
fl = []
whoosh = "anoisesrc=d=1.2:c=pink:r=48000"; chime = "aevalsrc='(sin(2*PI*1318*t)+0.5*sin(2*PI*1975*t)+0.25*sin(2*PI*2637*t))*exp(-t*3.2)':d=2:s=48000"
shimmer = "aevalsrc='(sin(2*PI*2093*t)+0.4*sin(2*PI*3136*t))*exp(-t*5)':d=1.5:s=48000"
boom = "aevalsrc='sin(2*PI*(60-28*min(t,3)/3)*t)*exp(-t*1.1)':d=5:s=48000"
riser = "anoisesrc=d=4:c=white:r=48000"
for i, p in enumerate(C["plan"]):
    if False: fl.append(sfx(whoosh, p[0] - 0.15, 0.22, "highpass=f=500,lowpass=f=5500,afade=t=in:d=0.5,afade=t=out:st=0.6:d=0.6"))
for tp in C["pulses"]: fl.append(sfx(shimmer, tp, 0.12))
st = C["sub"]["t0"]; fl += [sfx("aevalsrc='sin(2*PI*900*t)*exp(-t*60)':d=0.3:s=48000", st + 1.6, 0.3), sfx(chime, st + 2.7, 0.18)]
if C["bang"] > 0:
    fl.append(sfx(boom, C["bang"] - 0.05, 0.9, "lowpass=f=220")); fl.append(sfx(riser, C["bang"] - 4.0, 0.3, "highpass=f=800,lowpass=f=7000,afade=t=in:d=3.9:curve=exp"))
fl.append(sfx(chime, C["kcard"]["addr_t"], 0.12))
fc.append("".join(fl) + f"amix=inputs={len(fl)}:normalize=0:duration=longest,atrim=0:{DUR},apad=whole_dur={DUR}[sfx]")
# ducking: müzik konuşmada ~14 dB kısılır
fc.append(f"[{vo}:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[v1][v2]")
fc.append("[mus]volume=0.30[m0];[m0][v2]sidechaincompress=threshold=0.015:ratio=9:attack=30:release=600:makeup=1[md]")
fc.append(f"[v1]apad=whole_dur={DUR}[vp];[vp][md][sfx]amix=inputs=3:normalize=0:duration=first,atrim=0:{DUR}[mix]")
def run(extra, outargs):
    g = ";".join(fc) + ";[mix]" + extra + "[o]"
    return subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "info", *inputs, "-filter_complex", g, "-map", "[o]", *outargs], capture_output=True, text=True)
r = run("loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", ["-f", "null", "-"])
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
ln = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
r2 = run(ln, ["-ar", "48000", OUT]); assert r2.returncode == 0, r2.stderr[-600:]
print("tamam", OUT, "ölçülen giriş", m['input_i'], "LUFS")

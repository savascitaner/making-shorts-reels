# Flow'da yeniden çizilen el kareleri -> gorseller/ai/<ad>_<ar>_s5NN.jpg ; index.html tohumları güncellenir
import os, re, subprocess, sys
FF = "/Users/claude-eng/Shorts - Reels/araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64/ffmpeg"
SRC = "/Users/claude-eng/flow-mcp-out/Insanin-Ozu-eller"
M = {2:('k01_sogan_el','w'),3:('k01_sogan_el','t'),4:('k03_yasli_adam','w'),5:('k03_yasli_adam','t'),6:('b05_lab70','w'),7:('b05_lab70','t'),
     8:('b08_piyano','w'),9:('f06_kivilcim','w'),10:('f07_epiktetos','w'),11:('f12_bicak','w'),12:('f12_bicak','t'),13:('f13_tohum_kil','w'),14:('f13_tohum_kil','t'),
     15:('h02_son_zar','w'),16:('h02_son_zar','t'),17:('h03_avuc_isik','w'),18:('h03_avuc_isik','t'),19:('p06_el','w'),20:('p07_masa','w'),21:('p12_arketip','w'),22:('p12_arketip','t'),23:('f11_kafe','w'),24:('f11_kafe','t'),25:('f07_epiktetos','w')}
skip = set(int(x) for x in sys.argv[1:])
done = {}
for n, (k, ar) in M.items():
    if n in skip: continue
    f = [x for x in os.listdir(SRC) if x.startswith(f'scene-{n:02}') and x.endswith(('.jpeg', '.jpg', '.png'))]
    if not f: continue
    seed = 500 + int(re.search(r'\d+', k[1:3]).group()) if False else 500 + {'k':0,'b':20,'f':30,'p':50,'h':90}[k[0]] + int(k[1:3])
    out = f'gorseller/ai/{k}_{ar}_s{seed}.jpg'
    subprocess.run([FF, '-v', 'error', '-y', '-i', f'{SRC}/{sorted(f)[-1]}', '-q:v', '2', out], check=True)
    done[k.split('_')[0]] = seed; print(n, out)
p = 'kaynak/index.html'; s = open(p).read()
for pre, seed in done.items(): s = re.sub(rf"\b{pre}:\d+\b", f"{pre}:{seed}", s, count=1)
s = re.sub(r"const SEEDT = \{[^}]*\};", "const SEEDT = {};", s)
open(p, 'w').write(s); print(done)

"""Flow (anahtar kareler + ara kareler) ve SDXL ciktilarini gorseller/img/<ad>.jpg altinda toplar."""
import json, os, shutil, glob
SEC = {"s27-korteks": 42, "s31-beyinsapi": 42}  # SDXL tohum secimi
G = "/Users/claude-eng/Shorts - Reels/Sol-Beyin-Ego/gorseller"; os.makedirs(G + "/img", exist_ok=True)
for f in glob.glob(G + "/flow/*.jpg"): shutil.copy(f, G + "/img/" + os.path.basename(f))
for f in glob.glob(G + "/ai/*_s7.jpg"): shutil.copy(f, G + "/img/" + os.path.basename(f).replace("_s7", ""))
fl = json.load(open(G + "/flow-ara.json")); O = os.path.expanduser("~/flow-mcp-out/Sol-Beyin-Ego-ara")
for k, (n, _, _) in enumerate(fl):
    src = f"{O}/scene-{k + 2:02d}.jpeg"
    if os.path.exists(src): shutil.copy(src, f"{G}/img/{n}.jpg")
ek = os.path.expanduser("~/flow-mcp-out/Sol-Beyin-Ego-ara2/scene-01.jpeg")
if os.path.exists(ek): shutil.copy(ek, G + "/img/s30-goz-acilis.jpg")
for n, s in SEC.items():
    f = f"{G}/ai/{n}_s{s}.jpg"
    if os.path.exists(f): shutil.copy(f, f"{G}/img/{n}.jpg")
have = {os.path.basename(f)[:-4] for f in glob.glob(G + "/img/*.jpg")}
need = json.load(open(G + "/../kaynak/need.json"))
print(len(have), "hazir; eksik:", [n for n in need if n not in have])

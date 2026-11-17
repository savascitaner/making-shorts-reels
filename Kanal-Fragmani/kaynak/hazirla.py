"""Flow çıktılarını motora bağlar: kareleri adlandırır, alev noktasını bulur (flames.js), Veo kliplerini 24 fps karelere açar (klip.js).
  uv run -q --with numpy python Kanal-Fragmani/kaynak/hazirla.py
"""
import json, os, shutil, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.expanduser("~/flow-mcp-out/Kanal-Fragmani")
GOR = os.path.join(HERE, "..", "gorseller")
FF = os.path.join(ROOT, "araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64/ffmpeg")
STILL = {1: "eye", 2: "buda", 3: "lao", 4: "stoa", 5: "spinoza", 6: "leibniz", 7: "nietzsche", 8: "freud", 18: "adler", 10: "jung", 16: "avci", 11: "salon", 20: "mistik", 12: "viewer", 13: "lamp"}
CLIP = json.load(open(os.path.join(HERE, "klip-ayar.json"))) if os.path.exists(os.path.join(HERE, "klip-ayar.json")) else {}
# alevi otomatik bulmanın zor olduğu karelerde elle nokta (u, v)
ELLE = json.load(open(os.path.join(HERE, "alev-elle.json"))) if os.path.exists(os.path.join(HERE, "alev-elle.json")) else {}


def small(path, w=240, h=135):
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3).astype(np.float32) / 255


def flame(path):
    a = small(path); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.3 * r + 0.6 * g + 0.1 * b; warm = r - b
    score = lum * 1.0 + warm * 0.6
    thr = np.quantile(score, 0.998); m = score >= thr
    ys, xs = np.nonzero(m); wgt = score[m] - thr + 1e-3
    return [round(float((xs * wgt).sum() / wgt.sum() + 0.5) / a.shape[1], 3), round(float((ys * wgt).sum() / wgt.sum() + 0.5) / a.shape[0], 3)]


os.makedirs(os.path.join(GOR, "flow"), exist_ok=True)
flames = {}
for n, name in STILL.items():
    f = os.path.join(SRC, f"scene-{n:02d}.jpeg")
    if not os.path.exists(f):
        print("eksik kare:", name); continue
    dst = os.path.join(GOR, "flow", name + ".jpg"); shutil.copy(f, dst)
    flames[name] = ELLE.get(name) or flame(dst)
flames["lampEnd"] = flames.get("lamp")
open(os.path.join(HERE, "flames.js"), "w").write("window.FLAMES=" + json.dumps(flames) + ";")
print("alevler:", flames)

klip = {}
for name, c in CLIP.items():   # {"eye": {"scene": 14, "off": 0.0, "rate": 1.0}}
    f = os.path.join(SRC, f"scene-{c['scene']:02d}.mp4")
    if not os.path.exists(f):
        print("eksik klip:", name); continue
    d = os.path.join(GOR, "klip", name); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    subprocess.run([FF, "-v", "error", "-i", f, "-vf", "fps=24,scale=1920:1080:flags=lanczos", "-q:v", "2", os.path.join(d, "%04d.jpg")], check=True)
    n = len(os.listdir(d)); open(os.path.join(d, "n.txt"), "w").write(str(n)); open(os.path.join(d, "done"), "w").write("")
    klip[name] = {"n": n, "off": c.get("off", 0.0), "rate": c.get("rate", 1.0)}
open(os.path.join(HERE, "klip.js"), "w").write("window.KLIP=" + json.dumps(klip) + ";")
print("klipler:", klip)

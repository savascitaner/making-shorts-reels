# Yerel LTX-Video ile görüntüden video. Kullanım: python i2v.py klipler.json [sadece_bu_ad]
# klipler.json: {"W":576,"H":1024,"frames":65,"steps":30,"items":[["ad","ai/kaynak.jpg","hareket promptu"], ...]}
import torch, sys, os, json, time, glob, subprocess
from diffusers import LTXImageToVideoPipeline
from PIL import Image
cfg = json.load(open(sys.argv[1])); only = sys.argv[2] if len(sys.argv) > 2 else None
W, H, NF, ST = cfg.get("W", 576), cfg.get("H", 1024), cfg.get("frames", 65), cfg.get("steps", 30)
STYLE = ", 2D hand-drawn graphic novel illustration, ink outlines, watercolor texture, indigo shadows, golden amber light, smooth natural motion"
NEG = "worst quality, inconsistent motion, blurry, jittery, distorted, morphing faces, text, watermark"
snap = glob.glob(os.environ["HF_HOME"] + "/hub/models--Lightricks--LTX-Video/snapshots/*")[0]
pipe = LTXImageToVideoPipeline.from_pretrained(snap, torch_dtype=torch.bfloat16).to("mps")
pipe.vae.enable_tiling()
os.makedirs("klip", exist_ok=True)
for name, src, prompt in cfg["items"]:
    if only and name != only: continue
    out = f"klip/{name}"
    if os.path.exists(out + "/done"): continue
    os.makedirs(out, exist_ok=True); t = time.time()
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    fr = pipe(image=im, prompt=prompt + STYLE, negative_prompt=NEG, width=W, height=H, num_frames=NF, num_inference_steps=ST,
              guidance_scale=3.0, generator=torch.Generator("cpu").manual_seed(7)).frames[0]
    for i, f in enumerate(fr): f.save(f"{out}/{i:03d}.jpg", quality=92)
    open(out + "/done", "w").write(str(len(fr))); print(name, len(fr), f"{time.time() - t:.0f}s", flush=True)
print("I2V_BITTI", flush=True)

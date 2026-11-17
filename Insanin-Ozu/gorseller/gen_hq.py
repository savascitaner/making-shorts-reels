# Yerel SDXL, iki geçiş: taban (1344x768 ya da 768x1344) + "hires" img2img (x1.5) -> 2016x1152 / 1152x2016
# Kullanım: python gen_hq.py prompts.json ai [sadece_bu_ad_onekleri...]
import torch, sys, os, time, glob, json
HF = "/Users/claude-eng/Shorts - Reels/araclar/sd/hf"
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline, AutoencoderKL, DPMSolverMultistepScheduler
from PIL import Image
cfg = json.load(open(sys.argv[1])); out = sys.argv[2]; only = sys.argv[3:]; os.makedirs(out, exist_ok=True)
vae = AutoencoderKL.from_pretrained(glob.glob(HF+"/hub/models--madebyollin--sdxl-vae-fp16-fix/snapshots/*")[0], torch_dtype=torch.float16)
pipe = StableDiffusionXLPipeline.from_pretrained(glob.glob(HF+"/hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/*")[0], vae=vae, torch_dtype=torch.float16, variant="fp16", use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to("mps"); pipe.enable_attention_slicing(); pipe.vae.enable_tiling()
i2i = StableDiffusionXLImg2ImgPipeline(**pipe.components)
SIZES = {"w": (1344, 768), "t": (768, 1344)}
for it in cfg["items"]:
    name, ar, seeds, p = it[0], it[1], it[2], it[3]
    sty = cfg["styles"][it[4] if len(it) > 4 else "foto"]
    if only and not any(name.startswith(o) for o in only): continue
    for s in seeds:
        fn = os.path.join(out, f"{name}_{ar}_s{s}.jpg")
        if os.path.exists(fn): continue
        t = time.time(); W, H = SIZES[ar]
        g = torch.Generator("cpu").manual_seed(s)
        prompt = p + sty
        im = pipe(prompt=prompt, negative_prompt=cfg["neg"], width=W, height=H, num_inference_steps=32, guidance_scale=6.0, generator=g).images[0]
        im = im.resize((W*3//2, H*3//2), Image.LANCZOS)
        g = torch.Generator("cpu").manual_seed(s)
        im = i2i(prompt=prompt, negative_prompt=cfg["neg"], image=im, strength=0.32, num_inference_steps=30, guidance_scale=5.5, generator=g).images[0]
        im.convert("RGB").save(fn, quality=95); print(name, ar, s, f"{time.time()-t:.0f}s", flush=True)
print("GEN_BITTI", flush=True)

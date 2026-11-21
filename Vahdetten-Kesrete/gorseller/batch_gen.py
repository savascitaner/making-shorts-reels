import torch, sys, os, time, glob, json
HF = "/Users/claude-eng/Shorts - Reels/araclar/sd/hf"
from diffusers import StableDiffusionXLPipeline, AutoencoderKL, DPMSolverMultistepScheduler
cfg = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
vae = AutoencoderKL.from_pretrained(glob.glob(HF+"/hub/models--madebyollin--sdxl-vae-fp16-fix/snapshots/*")[0], torch_dtype=torch.float16)
pipe = StableDiffusionXLPipeline.from_pretrained(glob.glob(HF+"/hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/*")[0], vae=vae, torch_dtype=torch.float16, variant="fp16", use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to("mps"); pipe.enable_attention_slicing()
for name, seeds, p in cfg["items"]:
    for s in seeds:
        fn = os.path.join(out, f"{name}_s{s}.jpg")
        if os.path.exists(fn): continue
        t = time.time(); g = torch.Generator("cpu").manual_seed(s)
        im = pipe(prompt=p+cfg["style"], negative_prompt=cfg["neg"], width=cfg.get("w",768), height=cfg.get("h",1344), num_inference_steps=30, guidance_scale=6.5, generator=g).images[0]
        im.convert("RGB").save(fn, quality=95); print(name, s, f"{time.time()-t:.0f}s", flush=True)
print("GEN_BITTI", flush=True)

# Hegel AI paintings (SDXL base, local, MPS). One model load, 4 prompts x 2 seeds, 1344x768.
import torch, os, time, glob, sys
SD = "/Users/claude/Shorts - Reels/araclar/sd"; HF = os.path.join(SD, "hf")
from diffusers import StableDiffusionXLPipeline, AutoencoderKL, DPMSolverMultistepScheduler
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
vae = AutoencoderKL.from_pretrained(glob.glob(os.path.join(HF,"hub/models--madebyollin--sdxl-vae-fp16-fix/snapshots/*"))[0], torch_dtype=torch.float16)
pipe = StableDiffusionXLPipeline.from_pretrained(glob.glob(os.path.join(HF,"hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/*"))[0], vae=vae, torch_dtype=torch.float16, variant="fp16", use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to("mps"); pipe.enable_attention_slicing()
S = "19th century oil painting on canvas, romantic academic style, visible brushstrokes, dramatic chiaroscuro, muted earthy palette, museum masterpiece"
P = {
 "c2": "European stonemason in ragged linen shirt carving a marble block with hammer and chisel, behind him an old king in red robe sitting alone on a high throne, dim stone hall, " + S,
}
neg = "text, watermark, signature, letters, modern, photo, blurry, deformed hands, extra limbs, cartoon, anime, 3d render, frame, border"
for k, p in P.items():
    for s in (5, 41):
        t = time.time(); g = torch.Generator("cpu").manual_seed(s)
        im = pipe(prompt=p, negative_prompt=neg, width=1344, height=768, num_inference_steps=30, guidance_scale=6.5, generator=g).images[0]
        im.save(os.path.join(out, f"AI-{k}-{s}.png")); print(f"{k} {s} {time.time()-t:.0f}s", flush=True)
print("GEN_BITTI", flush=True)

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
 "a": "1806 Jena, a German philosopher in dark coat at a tall window watching Napoleon on a white horse in the street below, cannon smoke over rooftops, " + S,
 "b": "botanical triptych, a closed flower bud, an open white blossom, a ripe fruit on one branch, dark background, still life, " + S,
 "c": "a ragged slave carving stone with a chisel in the foreground, a lonely master sitting on a throne in a dim hall behind, " + S,
 "d": "a small owl with spread wings taking flight at dusk over ancient Greek temple ruins, twilight sky, " + S,
}
neg = "text, watermark, signature, letters, modern, photo, blurry, deformed hands, extra limbs, cartoon, anime, 3d render, frame, border"
for k, p in P.items():
    for s in (11, 29):
        t = time.time(); g = torch.Generator("cpu").manual_seed(s)
        im = pipe(prompt=p, negative_prompt=neg, width=1344, height=768, num_inference_steps=30, guidance_scale=6.5, generator=g).images[0]
        im.save(os.path.join(out, f"AI-{k}-{s}.png")); print(f"{k} {s} {time.time()-t:.0f}s", flush=True)
print("GEN_BITTI", flush=True)

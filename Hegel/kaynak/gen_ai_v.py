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
SEEDS={"a":(29,),"b":(29,),"c2":(5,)}
P = {
 "a": "1806 Jena, a German philosopher in dark coat at a tall window watching Napoleon on a white horse in the street below, cannon smoke over rooftops, " + S,
 "b": "botanical study, one tall branch with a closed flower bud at the top, an open white blossom in the middle, a ripe fruit at the bottom, dark background, still life, " + S,
 "c2": "European stonemason in ragged linen shirt carving a marble block with hammer and chisel, behind him an old king in red robe sitting alone on a high throne, dim stone hall, " + S,
}
neg = "text, watermark, signature, letters, modern, photo, blurry, deformed hands, extra limbs, cartoon, anime, 3d render, frame, border"
for k, p in P.items():
    for s in SEEDS[k]:
        t = time.time(); g = torch.Generator("cpu").manual_seed(s)
        im = pipe(prompt=p, negative_prompt=neg, width=768, height=1344, num_inference_steps=30, guidance_scale=6.5, generator=g).images[0]
        im.save(os.path.join(out, f"AI-{k}-{s}-v.png")); print(f"{k} {s} {time.time()-t:.0f}s", flush=True)
print("GEN_BITTI", flush=True)

# Doga AI paintings (SDXL base, local, MPS). 3 prompts x 1 seed, 1344x768, 30 min limit.
import torch, os, time, glob, sys
T0 = time.time()
SD = "/Users/claude/Shorts - Reels/araclar/sd"; HF = os.path.join(SD, "hf")
from diffusers import StableDiffusionXLPipeline, AutoencoderKL, DPMSolverMultistepScheduler
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
vae = AutoencoderKL.from_pretrained(glob.glob(os.path.join(HF,"hub/models--madebyollin--sdxl-vae-fp16-fix/snapshots/*"))[0], torch_dtype=torch.float16)
pipe = StableDiffusionXLPipeline.from_pretrained(glob.glob(os.path.join(HF,"hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/*"))[0], vae=vae, torch_dtype=torch.float16, variant="fp16", use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to("mps"); pipe.enable_attention_slicing()
S = "oil painting on canvas, 18th century neoclassical academic style, visible brushstrokes, dramatic chiaroscuro, muted earthy palette, museum masterpiece"
P = {
 "a": "night in ancient Greek Miletus, an old bearded Greek philosopher in a himation gazing up at the starry sky while stumbling and falling into a stone well, a young servant girl with a water jar laughing nearby, marble columns, moonlight, " + S,
 "b": "ancient battlefield in Anatolia 585 BC during a total solar eclipse, black sun with glowing corona in a darkened sky, two ancient armies of soldiers with spears and shields frozen, lowering their swords and looking up in awe, " + S,
 "c": "ancient Greek philosopher Empedocles in a white robe and laurel wreath standing alone on the rim of the erupting Etna volcano crater at night, glowing red lava, smoke, sparks, starry sky, " + S,
}
neg = "text, watermark, signature, letters, modern, photo, blurry, deformed hands, extra limbs, cartoon, anime, 3d render, frame, border"
for k, p in P.items():
    if time.time() - T0 > 1800: print("ZAMAN SINIRI", flush=True); break
    for s in (7,):
        t = time.time(); g = torch.Generator("cpu").manual_seed(s)
        im = pipe(prompt=p, negative_prompt=neg, width=1344, height=768, num_inference_steps=30, guidance_scale=6.5, generator=g).images[0]
        im.save(os.path.join(out, f"AI-{k}-{s}.png")); print(f"{k} {s} {time.time()-t:.0f}s", flush=True)
print("GEN_BITTI", flush=True)

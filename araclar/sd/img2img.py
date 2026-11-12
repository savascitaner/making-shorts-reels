import torch, sys, os, time, glob
from PIL import Image
from diffusers import StableDiffusionXLImg2ImgPipeline, AutoencoderKL, DPMSolverMultistepScheduler
HF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hf")
src, out = sys.argv[1], sys.argv[2]; seeds = [int(s) for s in sys.argv[3].split(",")]; strengths = [float(s) for s in sys.argv[4].split(",")]
prompt, neg = sys.argv[5], sys.argv[6]
os.makedirs(out, exist_ok=True)
vae = AutoencoderKL.from_pretrained(glob.glob(HF + "/hub/models--madebyollin--sdxl-vae-fp16-fix/snapshots/*")[0], torch_dtype=torch.float16)
pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(glob.glob(HF + "/hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/*")[0], vae=vae, torch_dtype=torch.float16, variant="fp16", use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to("mps"); pipe.enable_attention_slicing()
im = Image.open(src).convert("RGB"); W, H = 832, 1472
s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
l, t = (im.width - W) // 2, (im.height - H) // 2; im = im.crop((l, t, l + W, t + H))
for st in strengths:
    for sd in seeds:
        t0 = time.time(); g = torch.Generator("cpu").manual_seed(sd)
        r = pipe(prompt=prompt, negative_prompt=neg, image=im, strength=st, num_inference_steps=40, guidance_scale=6.0, generator=g).images[0]
        r.save(f"{out}/s{int(st*100)}_seed{sd}.png"); print(f"st {st} seed {sd} {time.time()-t0:.0f}s", flush=True)
print("I2I_BITTI", flush=True)

import torch, sys, os, time, glob
HF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hf")
from diffusers import StableDiffusionXLPipeline, AutoencoderKL, DPMSolverMultistepScheduler
os.environ.setdefault("HF_HOME", os.path.join(os.path.dirname(__file__), "hf"))
out = sys.argv[1]; seeds = [int(s) for s in sys.argv[2].split(",")]
prompt = sys.argv[3]; neg = sys.argv[4]
W, H = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (768, 1344)
steps = int(sys.argv[7]) if len(sys.argv) > 7 else 34
os.makedirs(out, exist_ok=True)
vae = AutoencoderKL.from_pretrained(glob.glob(os.path.join(HF,"hub/models--madebyollin--sdxl-vae-fp16-fix/snapshots/*"))[0], torch_dtype=torch.float16)
pipe = StableDiffusionXLPipeline.from_pretrained(glob.glob(os.path.join(HF,"hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/*"))[0], vae=vae, torch_dtype=torch.float16, variant="fp16", use_safetensors=True)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True, algorithm_type="dpmsolver++")
pipe = pipe.to("mps"); pipe.enable_attention_slicing()
for s in seeds:
    t = time.time()
    g = torch.Generator("cpu").manual_seed(s)
    im = pipe(prompt=prompt, negative_prompt=neg, width=W, height=H, num_inference_steps=steps, guidance_scale=6.5, generator=g).images[0]
    im.save(os.path.join(out, f"seed{s}.png")); print(f"seed {s} {time.time()-t:.0f}s", flush=True)
print("GEN_BITTI", flush=True)

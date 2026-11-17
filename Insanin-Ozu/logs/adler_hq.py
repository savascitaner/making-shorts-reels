# Düşük çözünürlüklü kamu malı Adler fotoğrafının birebir aynası: büyüt + SDXL img2img (düşük güç, yüz korunur)
import torch, glob
from PIL import Image
from diffusers import StableDiffusionXLImg2ImgPipeline, AutoencoderKL
HF = "/Users/claude-eng/Shorts - Reels/araclar/sd/hf"
A = "/Users/claude-eng/Shorts - Reels/Insanin-Ozu/gorseller/arsiv/"
vae = AutoencoderKL.from_pretrained(glob.glob(HF + "/hub/models--madebyollin--sdxl-vae-fp16-fix/snapshots/*")[0], torch_dtype=torch.float16)
p = StableDiffusionXLImg2ImgPipeline.from_pretrained(glob.glob(HF + "/hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/*")[0], vae=vae, torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("mps")
p.enable_attention_slicing(); p.vae.enable_tiling()
im = Image.open(A + "adler.jpg").convert("RGB").resize((1144, 1280), Image.LANCZOS)
out = p(prompt="1920s black and white studio portrait photograph of a bald middle aged man with a mustache in a dark suit, sharp focus, fine silver gelatin film grain, ultra detailed, museum archival print",
        negative_prompt="color, cartoon, painting, deformed, blurry, text, watermark", image=im, strength=0.26, num_inference_steps=40, guidance_scale=5.0,
        generator=torch.Generator("cpu").manual_seed(55)).images[0]
out.save(A + "adler-hq.jpg", quality=95); print("adler-hq ok")

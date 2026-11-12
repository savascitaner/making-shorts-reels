# Kurulum (bilgisayar değişirse)

Bu repo yalnızca metinleri ve kodları tutar. Araçlar, modeller ve medya yeniden indirilir ya da yeniden üretilir.

```bash
git clone https://github.com/savascitaner/making-shorts-reels "Shorts - Reels"
cd "Shorts - Reels/araclar"
npm install                      # three, gsap (canvas/3D motoru)
git clone https://github.com/sarpstar/cinecode
git clone https://github.com/SYSTRAN/faster-whisper
git clone https://github.com/remotion-dev/skills remotion-skills
git clone https://github.com/heygen-com/hyperframes        # isteğe bağlı
git clone https://github.com/pbakaus/impeccable            # isteğe bağlı
git clone https://github.com/Nutlope/hallmark              # isteğe bağlı
git clone https://github.com/ahujasid/blender-mcp          # isteğe bağlı
python3 -m venv venv-vahdet && venv-vahdet/bin/pip install torch diffusers transformers accelerate safetensors faster-whisper numpy scipy
```

Modeller (ilk çalıştırmada Hugging Face'ten iner):
- SDXL: `stabilityai/stable-diffusion-xl-base-1.0` ve `madebyollin/sdxl-vae-fp16-fix` → `araclar/sd/hf` (HF_HOME)
- Whisper: `Systran/faster-whisper-large-v3` → `~/.cache/huggingface`

Diğer gereken programlar: ffmpeg, node, uv, gh. Render için yerel sunucu: `python3 -m http.server 8765` (klasör kökünde).

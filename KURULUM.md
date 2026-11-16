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
git clone https://github.com/sanjeed5/audio-video-sync && venv-vahdet/bin/python -m venv audio-video-sync/.venv && audio-video-sync/.venv/bin/pip install -e audio-video-sync   # avsync (Python ≥3.10)
git clone https://github.com/ialakey/music-video-generator  # python3 -m musicvideo (NumPy+Pillow)
git clone https://github.com/whaleyxbt/claude-motion           # motion-design/sound-design skill'lerinin motoru: sfx/ (saf Python ses sentezi), scripts/wave.mjs, sheet.mjs. SKILL.md'ler tek başına yetmez.
git clone https://github.com/Vincentwei1021/mg-styles-15 mg-styles-15   # stil prompt'ları (referans)
# Proje skill'leri (.claude/skills/): cinecode (sarpstar), design-motion-principles (kylezantos, skills/ alt klasörü), motion-design, sound-design, review-loop, web-sims (whaleyxbt/claude-motion, .claude/skills/ alt klasörü)
python3 -m venv venv-vahdet && venv-vahdet/bin/pip install torch diffusers transformers accelerate safetensors faster-whisper numpy scipy
```

Modeller (ilk çalıştırmada Hugging Face'ten iner):
- SDXL: `stabilityai/stable-diffusion-xl-base-1.0` ve `madebyollin/sdxl-vae-fp16-fix` → `araclar/sd/hf` (HF_HOME)
- Whisper: `Systran/faster-whisper-large-v3` → `~/.cache/huggingface`

Diğer gereken programlar: ffmpeg, node, uv, gh. Render için yerel sunucu: `python3 -m http.server 8765` (klasör kökünde).

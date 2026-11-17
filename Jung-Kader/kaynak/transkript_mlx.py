import sys, mlx_whisper
src, out = sys.argv[1], sys.argv[2]
ipucu = "Murat Avcıoğlu, Carl Gustav Jung, bilinçdışı, kader, arketip, gölge, persona, bireyleşme, kolektif bilinçdışı."
r = mlx_whisper.transcribe(src, path_or_hf_repo="mlx-community/whisper-large-v3-mlx", language="tr", initial_prompt=ipucu, condition_on_previous_text=False, verbose=False)
with open(out, "w") as f:
    for s in r["segments"]:
        mm, ss = divmod(int(s["start"]), 60)
        f.write(f"[{mm:02d}:{ss:02d}] {s['text'].strip()}\n")
print("bitti", len(r["segments"]))

# klip/v<n>/off.txt = Veo konuşmasının ilk kelime başı ve son kelime sonu; v5 için offb.txt = "Hâlâ çiğsin ... kapıdan" aralığı
import sys, subprocess, numpy as np, os, json
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
G = "/Users/claude/Shorts - Reels/Yunus-Tapduk/gorseller/klip"
for k in sys.argv[1:]:
    f = os.path.expanduser(f"~/flow-mcp-out/YT-veo/scene-0{k[1:]}.mp4")
    pcm = subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
    s,_ = m.transcribe(a, language="tr", word_timestamps=True, beam_size=5, initial_prompt="Yunus'um, dergâh, Akçadağ, hâlâ çiğsin, Sultanım, Şeyhim")
    w = [x for seg in s for x in seg.words]
    if not w: print(k, "KONUŞMA YOK"); continue
    open(f"{G}/{k}/off.txt","w").write(f"{w[0].start:.2f} {w[-1].end:.2f}")
    json.dump([[x.word.strip(), round(x.start,2), round(x.end,2)] for x in w], open(f"{G}/{k}/words.json","w"), ensure_ascii=False)
    if k == "v5":
        hs = [i for i, x in enumerate(w) if x.word.strip().lower().startswith(("hâlâ","hala","halâ","hâla"))]
        ks = [i for i, x in enumerate(w) if x.word.strip().lower().startswith("kapı")]
        if len(hs) >= 2 and ks: open(f"{G}/{k}/offb.txt","w").write(f"{w[hs[1]].start:.2f} {w[ks[-1]].end:.2f}")
    print(k, f"{w[0].start:.2f} {w[-1].end:.2f}", " ".join(x.word.strip() for x in w))

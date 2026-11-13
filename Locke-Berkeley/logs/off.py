# klip/<k>/off.txt = Veo konuşmasının ilk kelime başı ve son kelime sonu (whisper)
import sys, subprocess, numpy as np, os
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
SRC = {"v1":"LB-veo/scene-01","v2":"LB-veo-b/scene-01","v3":"LB-veo/scene-02","v4":"LB-veo-b/scene-02","v5":"LB-veo/scene-03","v6":"LB-veo-b/scene-03"}
for k in sys.argv[1:]:
    f = os.path.expanduser(f"~/flow-mcp-out/{SRC[k]}.mp4")
    pcm = subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
    s,_ = m.transcribe(a, language="tr", word_timestamps=True, beam_size=5)
    w = [x for seg in s for x in seg.words]
    open(f"gorseller/klip/{k}/off.txt","w").write(f"{w[0].start:.2f} {w[-1].end:.2f}")
    print(k, f"{w[0].start:.2f} {w[-1].end:.2f}", " ".join(x.word.strip() for x in w))

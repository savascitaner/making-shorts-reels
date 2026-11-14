# klip/<k>/off.txt = Veo konuşmasının ilk kelime başı ve son kelime sonu (whisper)
import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
for arg in sys.argv[1:]:
    k, f = arg.split("=")
    a = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout, np.float32)
    s,_ = m.transcribe(a, language="tr", word_timestamps=True, beam_size=5, condition_on_previous_text=False)
    w = [x for seg in s for x in seg.words]
    if not w: print(k, "KONUŞMA YOK"); continue
    open(f"gorseller/klip/{k}/off.txt","w").write(f"{w[0].start:.2f} {w[-1].end:.2f}")
    print(k, f"{w[0].start:.2f} {w[-1].end:.2f}", " ".join(x.word.strip() for x in w))

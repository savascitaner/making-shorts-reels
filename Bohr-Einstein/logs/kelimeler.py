# ses/<ad>.mp3 -> ses/<ad>-words.json (whisper large-v3, kelime zamanları)
import sys, subprocess, json, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
for ad in sys.argv[1:]:
    a = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f"ses/{ad}.mp3","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout, np.float32)
    s,_ = m.transcribe(a, language="tr", word_timestamps=True, beam_size=5, initial_prompt="Einstein, Bohr, Solvay, foton, kuantum dolanıklığı, genel görelilik.")
    w = [{"w":x.word.strip(),"s":round(x.start,2),"e":round(x.end,2)} for seg in s for x in seg.words]
    json.dump(w, open(f"ses/{ad}-words.json","w"), ensure_ascii=False)
    print(ad, round(len(a)/16000,2)); print(" ".join(f"{x['w']}@{x['s']}" for x in w))

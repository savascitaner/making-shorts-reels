import sys
from faster_whisper import WhisperModel
m=WhisperModel("large-v3",device="cpu",compute_type="int8")
for a,b,p in [(226.8,231.6,"dayanan bu benlik, beyin sapı ve talamus gibi derin yapılara bağlıdır.")]:
    import subprocess
    import numpy as np
    pcm=subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-to",str(b),"-i","audio/vo.wav","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    seg,_=m.transcribe(np.frombuffer(pcm,np.int16).astype(np.float32)/32768,language="tr",initial_prompt=p,word_timestamps=True)
    print(a, " ".join(w.word.strip()+f"@{w.start+a:.2f}" for s in seg for w in s.words))

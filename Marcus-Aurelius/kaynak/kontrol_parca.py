import subprocess, numpy as np, sys
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
for a,b,ip in [(144.5,149.0,"Bugün nankör, kıskanç, hilekâr insanlarla karşılaşacağım."),(174.4,180.2,"Okusaydı, ömrünün geri kalanını kimden nefret edeceğini saymakla geçirecekti.")]:
    pcm = subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-to",str(b),"-i","audio/vo.wav","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    au = np.frombuffer(pcm, np.int16).astype(np.float32)/32768
    for ipx in (ip, None):
        segs,_ = m.transcribe(au, language="tr", initial_prompt=ipx, beam_size=5, vad_filter=False)
        print(a, "ipucu" if ipx else "ipucusuz", "|", " ".join(s.text.strip() for s in segs))

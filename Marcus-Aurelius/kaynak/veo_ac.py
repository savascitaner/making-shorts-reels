# Veo kliplerini 30 fps karelere açar, konuşmalı kliplerde ilk kelimenin başını whisper ile ölçer, veo.js yazar.
import json, os, subprocess, glob, sys
FF = "/Users/claude-eng/Shorts - Reels/araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64/ffmpeg"
O = os.path.expanduser("~/flow-mcp-out/")
# candidate files per clip, first existing wins (veo = first batch, veo2 = nameless re-run after the "prominent people" refusal)
SRCS = {"v_s01": ["Marcus-Aurelius-veo/scene-01"], "v_s07": ["Marcus-Aurelius-veo/scene-03"],
        "v_s04": ["Marcus-Aurelius-veo2/scene-01"], "v_s18": ["Marcus-Aurelius-veo/scene-04", "Marcus-Aurelius-veo2/scene-02"],
        "v_s20": ["Marcus-Aurelius-veo2/scene-03"], "v_s21": ["Marcus-Aurelius-veo2/scene-04"], "v_s22": ["Marcus-Aurelius-veo2/scene-05"]}
ORDER = list(SRCS)
TALK = {"v_s04": "Gömün onu.", "v_s18": "Sakın Sezarlaşma.", "v_s21": "Seni yaralayan şey olay değil, olay hakkındaki yargındır.", "v_s22": "Doğan güneşe git. Ben artık batıyorum."}
K = "../gorseller/klip"; clips, speech = {}, {}
model = None
for i, k in enumerate(ORDER, 1):
    vids = [v for c in SRCS[k] for v in sorted(glob.glob(O + c + "*.mp4"))]
    if not vids: print(k, "yok"); continue
    d = f"{K}/{k}"; os.makedirs(d, exist_ok=True)
    if not os.path.exists(f"{d}/done"):
        for f in glob.glob(f"{d}/*.jpg"): os.remove(f)
        subprocess.run([FF, "-v", "error", "-y", "-i", vids[0], "-vf", "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", "-q:v", "3", f"{d}/%04d.jpg"], check=True)
        subprocess.run([FF, "-v", "error", "-y", "-i", vids[0], "-ac", "1", "-ar", "16000", f"{d}/ses.wav"])
        open(f"{d}/done", "w").write(vids[0])
    n = len(glob.glob(f"{d}/*.jpg")); open(f"{d}/n.txt", "w").write(str(n)); clips[k] = n
    if k in TALK:
        if os.path.exists(f"{d}/off.txt"): speech[k] = float(open(f"{d}/off.txt").read()); continue
        if model is None:
            from faster_whisper import WhisperModel; model = WhisperModel("large-v3", device="cpu", compute_type="int8")
        import wave, numpy as np; r = wave.open(f"{d}/ses.wav"); au = np.frombuffer(r.readframes(r.getnframes()), np.int16).astype(np.float32) / 32768
        segs, _ = model.transcribe(au, language="tr", word_timestamps=True, initial_prompt=TALK[k], vad_filter=False)
        ws = [w for s in segs for w in s.words]
        txt = " ".join(w.word.strip() for w in ws)
        if ws: speech[k] = round(ws[0].start, 2); open(f"{d}/off.txt", "w").write(str(speech[k]))
        print(k, "konuşma", speech.get(k), "|", txt)
open("veo.js", "w").write("window.VEO_CLIPS=" + json.dumps(clips) + ";window.VEO_SPEECH=" + json.dumps(speech) + ";")
print("veo.js", clips, speech)

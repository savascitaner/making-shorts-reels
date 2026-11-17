# "Jung" -> /juŋ/ yaması: yama-4.mp3'ün 4 cümlesi vo.wav'daki yerlerine; kelime zamanları kaydırılır.
import json, subprocess, shutil
FF = "/Users/claude-eng/Shorts - Reels/araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64/ffmpeg"
# (orijinal aralık, yama aralığı, kelime indeksleri)
R = [  # NOT: bir kez çalıştırıldı (2026-11-17); ses tekrar yamalanmaz
((235.75, 238.75), (0.00, 3.10), range(502, 508)),
     ((245.75, 250.58), (3.10, 8.65), range(520, 529)),
     ((256.33, 260.40), (8.65, 13.05), range(542, 550)),
     ((377.60, 381.48), (13.05, 17.08), range(802, 812))]
# yama içi kelime zamanları (whisper, birleşik kelimeler)
PW = [[0.0,0.4,0.6,1.6,1.8,2.3,2.75],
      [3.2,3.7,3.9,4.2,4.7,5.3,5.9,6.9,7.6,8.3],
      [8.7,9.1,9.3,9.9,10.6,11.2,11.5,12.3,12.8],
      [12.9,13.4,13.6,13.9,14.6,14.8,15.4,15.7,16.1,16.4,16.85]]
shutil.copy('kaynak/audio/vo.wav', 'ses/vo-jung-oncesi.wav')
fc, parts, prev = [], [], 0.0
for n, ((a, b), (pa, pb), _) in enumerate(R):
    fc.append(f"[0:a]atrim={prev}:{a},asetpts=N/SR/TB[o{n}]"); parts.append(f"[o{n}]")
    fc.append(f"[1:a]aresample=48000,aformat=channel_layouts=mono,atrim={pa}:{pb},asetpts=N/SR/TB,volume=-0.5dB,afade=t=in:d=0.02,afade=t=out:st={pb-pa-0.03:.3f}:d=0.03[p{n}]"); parts.append(f"[p{n}]")
    prev = b
fc.append(f"[0:a]atrim={prev},asetpts=N/SR/TB[o9]"); parts.append("[o9]")
fc.append(''.join(parts) + f"concat=n={len(parts)}:v=0:a=1[o]")
subprocess.run([FF, '-v', 'error', '-y', '-i', 'ses/vo-jung-oncesi.wav', '-i', 'ses/yama-4.mp3', '-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', '-ac', '1', 'kaynak/audio/vo.wav'], check=True)
W = json.load(open('kaynak/words-raw.json')); shutil.copy('kaynak/words-raw.json', 'logs/words-raw-jung-oncesi.json')
def shift(t):  # orijinal zamanı yeni zamana çevir
    d = 0.0
    for (a, b), (pa, pb), _ in R:
        if t >= b: d += (pb - pa) - (b - a)
    return t + d
for i, w in enumerate(W):
    for (a, b), (pa, pb), idx in R:
        if i in idx:
            k = i - idx.start; P = PW[R.index(((a, b), (pa, pb), idx))]
            base = shift(a) - pa
            w['s'] = round(P[k] + base, 3); w['e'] = round(P[k + 1] - 0.02 + base, 3); break
    else:
        w['s'] = round(shift(w['s']), 3); w['e'] = round(shift(w['e']), 3)
json.dump(W, open('kaynak/words-raw.json', 'w'), ensure_ascii=False)
D = sum((pb - pa) - (b - a) for (a, b), (pa, pb), _ in R)
C = json.load(open('video.json')); C['sure'] = round(C['sure'] + D, 2); json.dump(C, open('video.json', 'w'), ensure_ascii=False, indent=2)
print('kayma', round(D, 3), 'yeni sure', C['sure'])
for i in [501,502,507,508,519,520,528,529,541,542,549,550,801,802,811,812,884]: print(i, W[i])

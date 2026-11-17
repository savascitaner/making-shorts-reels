# Senaryo paragraflarını kelime aralıklarına çevirir; Reels kesitinin (R) ses kurgusunu ve zaman haritasını üretir.
import json, re, subprocess, os
FF = "/Users/claude-eng/Shorts - Reels/araclar/audio-video-sync/.venv/lib/python3.12/site-packages/static_ffmpeg/bin/darwin_arm64/ffmpeg"
t = open('Insanin-Ozu-senaryo.md').read().split('## Reels kesiti')[0]
paras = []
for sec in re.split(r'\n## ', t)[1:]:
    rs = '[R]' in sec.split('\n')[0]
    for l in sec.split('\n'):
        if l.startswith('>'):
            x = l.lstrip('> ').strip()
            if not x: continue
            r = rs or '**[R]**' in x; x = x.replace('**[R]**', '').strip()
            paras.append({'n': len(x.split()), 'r': r, 'txt': x[:40]})
W = json.load(open('kaynak/words.json'))['words']
i = 0
for p in paras: p['a'] = i; i += p['n']; p['b'] = i - 1
assert i == len(W), (i, len(W))
# Reels segmentleri: ardışık R paragrafları birleşir
segs = []
for p in paras:
    if not p['r']: continue
    s, e = W[p['a']]['s'] - 0.12, W[p['b']]['e'] + 0.30
    if segs and segs[-1]['b'] == p['a'] - 1: segs[-1]['e'] = e; segs[-1]['b'] = p['b']
    else: segs.append({'a': p['a'], 'b': p['b'], 's': s, 'e': e})
GAP = 0.45  # parçalar arası nefes
rt, out = 0.0, []
for g in segs: g['rt'] = rt; rt += g['e'] - g['s'] + GAP
for g in segs:
    for k in range(g['a'], g['b'] + 1):
        w = dict(W[k]); w['s'] = round(w['s'] - g['s'] + g['rt'], 3); w['e'] = round(w['e'] - g['s'] + g['rt'], 3); w['o'] = k; out.append(w)
RD = round(rt - GAP + 0.2, 2)
# Reels chunks: uzun videonun chunk'larından türet (yalnız korunan kelimeler)
D = json.load(open('kaynak/words.json'))
keep = {w['o']: n for n, w in enumerate(out)}
ch = [[keep[k] for k in c if k in keep] for c in D['chunks']]; ch = [c for c in ch if c]
R = dict(words=out, chunks=ch, duration=RD, segs=segs, reels=True)
open('kaynak/words-r.js', 'w').write('window.DATA=' + json.dumps(R, ensure_ascii=False) + ';')
open('kaynak/paras.json', 'w').write(json.dumps(paras, ensure_ascii=False, indent=0))
# Reels ses kurgusu
fc, ins = [], []
for n, g in enumerate(segs):
    fc.append(f"[0:a]atrim={g['s']:.3f}:{g['e']:.3f},asetpts=N/SR/TB,afade=t=in:d=0.04,afade=t=out:st={g['e']-g['s']-0.06:.3f}:d=0.06,apad=pad_dur={GAP}[s{n}]"); ins.append(f"[s{n}]")
fc.append(''.join(ins) + f"concat=n={len(segs)}:v=0:a=1[o]")
subprocess.run([FF, '-v', 'error', '-y', '-i', 'kaynak/audio/vo.wav', '-filter_complex', ';'.join(fc), '-map', '[o]', '-ar', '48000', '-ac', '1', 'kaynak/audio/vo-r.wav'], check=True)
print(len(paras), 'paragraf;', len(segs), 'Reels parçası; Reels süresi', RD, 'sn')
for g in segs: print(f"  {g['s']:.1f}-{g['e']:.1f}  ->  {g['rt']:.1f}   {W[g['a']]['w']} … {W[g['b']]['w']}")

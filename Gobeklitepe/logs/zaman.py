# After a new alignment: recompute video.json times from words.json
import json
w = json.load(open('kaynak/words.json'))['words']; wt = lambda i: w[i]['s']
c = json.load(open('video.json'))
c['sure'] = round(w[-1]['e'] + 3.6, 2)
c['boom'] = [round(wt(25), 2)]
c['bolum_sinirlari'] = [round(wt(i) - 0.1, 2) for i in [7, 27, 56, 86, 115, 141, 166, 191, 209, 229, 254]]
c['gecis'] = [round(wt(i) - 0.1, 2) for i in [7, 30, 56, 86, 115, 141, 166, 191, 209, 229, 254]]
c['qc_kareleri'] = [0, 45, 100] + [int((wt(i) + d) * 30) for i, d in [(20, 0), (25, 0.4), (36, 0), (52, 0), (64, 0), (72, 0), (97, 0), (99, 0.8), (118, 0), (143, 0), (157, 1.0), (175, 0.3), (187, 0), (204, 0), (214, 0), (227, 0), (250, 0.3), (272, 0)]] + [int((c['sure'] - 2) * 30)]
json.dump(c, open('video.json', 'w'), ensure_ascii=False, indent=2)
print('kelime', len(w), 'sure', c['sure'], 'boom', c['boom'], 'ilk 8:', ' '.join(x['w'] for x in w[:8]))

import json, sys, urllib.request, urllib.parse, csv, os, re
import time
UA = {'User-Agent': 'VideoResearchTool/1.0 (https://commons.wikimedia.org/; personal non-commercial use) python-urllib'}
out, files = sys.argv[1], sys.argv[2:]
rows = []
for spec in files:
    title, name = spec.split('=>')
    u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(dict(action='query', titles=title, prop='imageinfo', iiprop='url|extmetadata|size', format='json'))
    pg = next(iter(json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))['query']['pages'].values()))
    ii = pg['imageinfo'][0]; m = ii['extmetadata']
    fn = os.path.join(out, name)
    if os.path.exists(fn) and os.path.getsize(fn) > 1000: print('var', name); continue
    time.sleep(4); urllib.request.urlretrieve if False else None
    with urllib.request.urlopen(urllib.request.Request(ii['url'], headers=UA), timeout=120) as r, open(fn, 'wb') as f: f.write(r.read())
    art = re.sub('<[^>]+>', '', m.get('Artist', {}).get('value', '?')).strip()
    rows.append([name, title, ii['descriptionurl'], m.get('LicenseShortName', {}).get('value', '?'), art])
    print(name, ii['width'], 'x', ii['height'], m.get('LicenseShortName', {}).get('value'))
new = not os.path.exists('LICENSES.csv')
with open('LICENSES.csv', 'a', newline='') as f:
    w = csv.writer(f)
    if new: w.writerow(['dosya', 'kaynak', 'url', 'lisans', 'yazar'])
    w.writerows(rows)

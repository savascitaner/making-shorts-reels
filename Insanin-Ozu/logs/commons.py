import json, sys, urllib.request, urllib.parse
UA = {'User-Agent': 'reels-research-bot/1.0 (educational video)'}
def api(**p):
    p.update(format='json'); u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(p)
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
for q in sys.argv[1:]:
    r = api(action='query', generator='search', gsrsearch=q, gsrnamespace=6, gsrlimit=6, prop='imageinfo', iiprop='size|extmetadata|mime|url')
    print('##', q)
    for pg in sorted((r.get('query') or {}).get('pages', {}).values(), key=lambda x: x.get('index', 0)):
        ii = pg['imageinfo'][0]; m = ii.get('extmetadata', {})
        dur = ''
        print(f"  {pg['title'][:80]} | {ii.get('width')}x{ii.get('height')} | {ii['mime']} | {m.get('LicenseShortName',{}).get('value','?')} | {round(ii.get('size',0)/1e6,1)}MB")

#!/bin/bash
# Nietzsche fotoğraf ve tablolarını Wikimedia Commons'tan indirir (çift tıkla).
cd "$(dirname "$0")" || exit 1
mkdir -p gorseller/json
UA="SevgiliReels/1.0 (personal video project)"
n=0
while IFS='|' read -r kod sorgu; do
  [ -z "$kod" ] && continue
  echo "Aranıyor: $sorgu"
  curl -sfLG -A "$UA" -o "gorseller/json/$kod.json" "https://commons.wikimedia.org/w/api.php" \
    --data-urlencode "action=query" --data-urlencode "format=json" --data-urlencode "generator=search" \
    --data-urlencode "gsrnamespace=6" --data-urlencode "gsrlimit=10" --data-urlencode "gsrsearch=$sorgu" \
    --data-urlencode "prop=imageinfo" --data-urlencode "iiprop=url|size|mime|extmetadata" --data-urlencode "iiurlwidth=2400" || { echo "  HATA"; continue; }
  osascript -l JavaScript -e "
    const d=JSON.parse($.NSString.stringWithContentsOfFileEncodingError('gorseller/json/$kod.json',4,null).js);
    const p=d.query?Object.values(d.query.pages):[];p.sort((a,b)=>a.index-b.index);
    p.filter(x=>x.imageinfo&&/jpeg|png/.test(x.imageinfo[0].mime)&&x.imageinfo[0].width>=700)
     .map((x,i)=>i+'|'+(x.imageinfo[0].thumburl||x.imageinfo[0].url)+'|'+x.title+'|'+((x.imageinfo[0].extmetadata.LicenseShortName||{}).value||'?')).join('\n')" > gorseller/json/$kod.txt 2>/dev/null
  while IFS='|' read -r i url baslik lis; do
    [ -z "$url" ] && continue
    ext="${url##*.}"; ext=$(echo "$ext" | tr 'A-Z' 'a-z'); [ "$ext" = "jpeg" ] && ext=jpg
    hedef="gorseller/$kod-$i.$ext"
    if curl -sfL --retry 4 --retry-delay 5 -A "$UA" -o "$hedef" "$url"; then echo "$kod-$i.$ext | $baslik | $lis" >> gorseller/LISTE.txt; n=$((n+1)); fi
    sleep 3
  done < gorseller/json/$kod.txt
done <<'LIST'
a-portre-1882|Friedrich Nietzsche 1882 Gustav Schultze
b-genc|Nietzsche 1864 photograph
c-basel|Nietzsche 1869 photograph Basel
d-lou-ree|Lou Salome Paul Ree Nietzsche 1882
e-olde|Hans Olde Nietzsche
f-munch|Munch Friedrich Nietzsche 1906
g-hasta|Nietzsche Weimar 1899
h-torino|Piazza Carlo Alberto Torino
i-torino-eski|Torino via Po 1880 photograph
j-sils|Nietzsche-Haus Sils Maria
k-engadin|Silsersee Engadin painting
l-friedrich|Wanderer above the Sea of Fog
m-friedrich2|Caspar David Friedrich mountains
n-at|Gericault horse painting
o-elisabeth|Elisabeth Forster-Nietzsche
p-zerdust|Also sprach Zarathustra first edition
q-silberblick|Villa Silberblick Weimar
r-1875|Nietzsche 1875 photograph
LIST
echo; echo "Bitti: $n görsel indirildi. Liste: gorseller/LISTE.txt"

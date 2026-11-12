#!/bin/bash
# Hegel görsellerini Wikimedia Commons'tan indirir (çift tıkla).
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
a-portre|Hegel Jakob Schlesinger 1831
b-kugler|Hegel mit Studenten Kugler 1828
c-hegel-genc|Georg Wilhelm Friedrich Hegel portrait lithograph
d-hegel-sebbers|Hegel Sebbers 1828
e-jena-savas|Battle of Jena 1806 painting
f-napoleon-jena|Napoleon Jena Vernet
g-napoleon-at|Napoleon on horseback painting 1806
h-jena-sehir|Jena 1800 Stadtansicht
i-tubingen|Tübinger Stift Kupferstich
j-holderlin|Hölderlin Hiemer 1792
k-schelling|Schelling portrait Stieler
l-berlin-uni|Universität Berlin 1830 Unter den Linden
m-schopenhauer|Schopenhauer 1815 Ruhl
n-fenomenoloji|Phänomenologie des Geistes 1807 title page
o-marx|Karl Marx 1875 photograph Mayall
p-kierkegaard|Søren Kierkegaard sketch Niels Christian Kierkegaard
q-minerva-baykus|Athenian tetradrachm owl
r-friedrich-sabah|Caspar David Friedrich Morning in the Riesengebirge
s-friedrich-ay|Caspar David Friedrich Moonrise over the Sea
t-cicek|Pieter Claesz flower still life
u-tomurcuk|Maria Sibylla Merian flower metamorphosis
v-ciftci|Millet The Gleaners
w-tasci|Courbet The Stone Breakers
x-hegel-mezar|Hegel Grab Dorotheenstädtischer Friedhof
y-berlin-1831|Berlin 1830 painting Gaertner
LIST
echo; echo "Bitti: $n görsel indirildi. Liste: gorseller/LISTE.txt"

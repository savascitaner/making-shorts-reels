#!/bin/bash
# Doğa filozofları görsellerini Wikimedia Commons'tan indirir (çift tıkla).
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
a-atina-okulu|Raphael School of Athens high resolution
b-atina-herakleitos|School of Athens Heraclitus detail
c-atina-parmenides|School of Athens Parmenides detail
d-brugghen-herakleitos|Hendrick ter Brugghen Heraclitus 1628
e-brugghen-demokritos|Hendrick ter Brugghen Democritus 1628
f-rubens|Rubens Heraclitus Democritus
g-thales-nurnberg|Thales Nuremberg Chronicle
h-thales|Thales of Miletus engraving
i-anaksimandros|Anaximander relief Museo Nazionale Romano
j-anaksimenes|Anaximenes Nuremberg Chronicle
k-empedokles|Empedocles Nuremberg Chronicle
l-empedokles-etna|Death of Empedocles Etna engraving
m-etna|Etna eruption painting
n-demokritos|Democritus Coypel painting
o-milet-tiyatro|Miletus theatre ancient
p-efes|Library of Celsus Ephesus
q-tutulma|total solar eclipse corona
r-savas-antik|Ancient battle painting Lydians
s-zeus|Zeus Otricoli bust
t-poseidon|Artemision Bronze Poseidon
u-ahilleus|Achilles red figure vase
v-kaplumbaga|tortoise Testudo hermanni
w-nehir|mountain river long exposure
x-ates|campfire flames close
y-dalton|John Dalton portrait
z-dalton-atom|Dalton atomic symbols 1808
za-elea|Velia Elea Porta Rosa
zb-sicilya|Akragas Valley of the Temples Concordia
LIST
echo; echo "Bitti: $n görsel indirildi. Liste: gorseller/LISTE.txt"

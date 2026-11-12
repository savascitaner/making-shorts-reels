#!/bin/bash
# Slow retry of the critical missing images using standard 1920px thumbnails.
UA="SevgiliReels/1.0 (personal video project)"
for item in "$@"; do kod=${item%-*}; i=${item##*-}
  ls "$kod-$i".* >/dev/null 2>&1 && continue
  line=$(grep "^$i|" json/$kod.txt); url=$(echo "$line" | cut -d'|' -f2); url=${url%%\?*}; baslik=$(echo "$line" | cut -d'|' -f3); lis=$(echo "$line" | cut -d'|' -f4)
  if [[ "$url" == */thumb/* ]]; then base=${url%/*}; name=${base##*/}; u2="$base/1920px-$name"; else u2=$url; fi
  for u in "$u2" "$url"; do
    if curl -sfL -A "$UA" -o tmp.dl "$u"; then t=$(file -b tmp.dl); case "$t" in JPEG*) e=jpg;; PNG*) e=png;; *) e=bin;; esac
      mv tmp.dl "$kod-$i.$e"; echo "$kod-$i.$e | $baslik | $lis" >> LISTE.txt; echo "ok $kod-$i"; break; fi
    sleep 4
  done
  ls "$kod-$i".* >/dev/null 2>&1 || echo "fail $kod-$i"
  sleep 15
done

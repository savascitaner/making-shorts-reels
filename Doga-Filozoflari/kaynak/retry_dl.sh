#!/bin/bash
# Retry Commons downloads that failed (429) + fix file extensions. Run from gorseller/.
UA="SevgiliReels/1.0 (personal video project)"
for f in *.org\&utm*; do [ -e "$f" ] || continue; t=$(file -b "$f"); case "$t" in JPEG*) e=jpg;; PNG*) e=png;; *) e=bin;; esac
  b="${f%%.org&*}"; b="${b%.*}"; mv "$f" "$b.$e"; done
for txt in json/*.txt; do kod=$(basename "$txt" .txt)
  while IFS='|' read -r i url baslik lis; do [ -z "$url" ] && continue
    ls "$kod-$i".* >/dev/null 2>&1 && continue
    u="${url%%\?*}"
    if curl -sfL --retry 3 --retry-delay 8 -A "$UA" -o "tmp.dl" "$u"; then
      t=$(file -b tmp.dl); case "$t" in JPEG*) e=jpg;; PNG*) e=png;; *) e=bin;; esac
      mv tmp.dl "$kod-$i.$e"; echo "$kod-$i.$e | $baslik | $lis" >> LISTE.txt; echo "ok $kod-$i"
    else echo "fail $kod-$i"; fi
    sleep 5
  done < "$txt"
done
sed -i '' -E 's/\.[a-z]+\.org&utm[^ ]* \|/ |/' LISTE.txt

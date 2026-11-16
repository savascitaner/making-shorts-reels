#!/bin/zsh
# kullanım: flow_bekle.sh <proje-adı-parçası>  → o projedeki işler bitene kadar bekler
cd "/Users/claude-eng/Shorts - Reels"
until ./flow.sh status '{"detailed":false}' | python3 -c "
import json,sys;d=json.load(sys.stdin);j=[x for x in d['jobs'] if '$1' in x['project']]
act=[x for x in j if x['status'] in ('queued','running')]
print(len(j),'is,',len(act),'aktif', [(x['scene'],x['status']) for x in j], file=sys.stderr); sys.exit(1 if act else 0)"; do sleep 30; done
./flow.sh status '{"detailed":false}' | python3 -c "
import json,sys;d=json.load(sys.stdin)
for x in d['jobs']:
  if '$1' in x['project']: print(x['scene'],x['status'],x.get('files'),x.get('error',''),x.get('note',''))"

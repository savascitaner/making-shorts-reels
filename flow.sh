#!/bin/zsh
# Flow MCP'nin HTTP köprüsü (MCP araçları oturumda yüklü değilse de çalışır).
# Kullanım: ./flow.sh <metot> '<json>'   ör: ./flow.sh status '{"detailed":true}'
# Metotlar: status generate wait cancel retry assets download agent edit character characters techniques outputs
export PATH="/Users/claude-eng/.local/node/bin:$PATH"
curl -s -m 2 127.0.0.1:8787/api/health >/dev/null || { (cd ~/flow-mcp && nohup node dist/studio.js >/tmp/flow-studio.log 2>&1 &); sleep 4; }
T=$(cat ~/.flow-mcp/token)
curl -s -m ${FLOW_TIMEOUT:-900} -X POST -H "x-flow-token: $T" -H "content-type: application/json" \
  --data "${2:-{\}}" "http://127.0.0.1:8787/api/$1"; echo

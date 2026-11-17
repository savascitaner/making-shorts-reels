// motordan kesme/iplik/kapanış zamanlarını olaylar-<f>.json'a yazar (ses tasarımı için)
const { chromium } = require('/Users/claude-eng/flow-mcp/node_modules/playwright-core');
const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
  for (const f of ['reels', '16x9']) {
    const p = await b.newPage(); await p.goto(`http://127.0.0.1:8765/Jung-Kader/kaynak/jung.html?f=${f}`);
    const o = await p.evaluate(async () => { await window.READY; return { cuts: SHOTS.map(s => [s.t0, s.k, s.fx, s.card]), ...TIMES, words: DATA.words.map(w => [w.w, w.s]) }; });
    fs.writeFileSync(`olaylar-${f}.json`, JSON.stringify(o)); console.log(f, o.cuts.length, o.DUR.toFixed(2));
  }
  await b.close();
})();

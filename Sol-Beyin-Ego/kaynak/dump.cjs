// motorun zaman cizelgesini disa aktarir (ses tasarimi icin): node dump.cjs
const { chromium } = require('/Users/claude-eng/flow-mcp/node_modules/playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
  const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/Sol-Beyin-Ego/kaynak/index.html?m=long&noload=1');
  await p.waitForFunction(() => window.DATA && typeof SHOTS !== 'undefined', null, { timeout: 15000 }).catch(() => {});
  const r = await p.evaluate(() => ({ aend: AEND, tail: TAIL, shots: SHOTS.map(s => ({ t0: s.t0, k: s.k, fx: s.fx })), labels: LABELS.map(l => l.t0), bv: BV.t0, q: QSTART, sw: WD[428].s - 0.3,
    short: window.SHORTCUT }));
  require('fs').writeFileSync('timeline.json', JSON.stringify(r)); console.log('shots', r.shots.length, 'errors', errs.slice(0, 3));
  await b.close();
})();

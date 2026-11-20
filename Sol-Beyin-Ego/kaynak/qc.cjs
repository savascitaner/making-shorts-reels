// QC karesi: node qc.cjs <long|short> <sn,sn,...> <cikti.jpg>   (taslak modunda, eksik gorsel gri)
const { chromium } = require('/Users/claude-eng/flow-mcp/node_modules/playwright-core');
const [m, ts, out] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(`http://127.0.0.1:8765/Sol-Beyin-Ego/kaynak/index.html?m=${m}&taslak=1`);
  const info = await p.evaluate(() => window.READY); const fs = require('fs'); const dir = out.replace(/\.jpg$/, ''); fs.mkdirSync(dir, { recursive: true });
  let n = 0; for (const t of ts.split(',').map(Number)) {
    const url = await p.evaluate(f => window.captureFrame(f, 'image/jpeg', 0.85), Math.round(t * 24));
    fs.writeFileSync(`${dir}/${String(n++).padStart(2, '0')}.jpg`, Buffer.from(url.split(',')[1], 'base64')); }
  console.log(JSON.stringify(info), 'eksik', await p.evaluate(() => window.MISSING.length), errs.slice(0, 2)); await b.close();
})().catch(e => { console.log('HATA', e.message); process.exit(1); });

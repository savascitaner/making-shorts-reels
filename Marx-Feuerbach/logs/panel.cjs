const { chromium } = require(process.env.HOME + '/flow-mcp/node_modules/playwright-core');
(async () => {
  const b = await chromium.connectOverCDP('http://127.0.0.1:9333');
  for (const c of b.contexts()) for (const p of c.pages()) {
    if (!p.url().includes('/project/')) continue;
    const btns = p.getByRole('button', { name: /^close$/i });
    const n = await btns.count(); let clicked = 0;
    for (let i = 0; i < n; i++) { try { if (await btns.nth(i).isVisible()) { await btns.nth(i).click(); clicked++; } } catch (e) {} }
    console.log(p.url(), 'close buttons:', n, 'clicked:', clicked);
  }
  await b.close().catch(()=>{}); process.exit(0);
})();

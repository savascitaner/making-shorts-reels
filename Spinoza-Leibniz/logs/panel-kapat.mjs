// Flow sekmesindeki ajan panelini kapatır (CDP 127.0.0.1:9333).
import { createRequire } from "module";
const require = createRequire(process.env.HOME + "/flow-mcp/package.json");
const { chromium } = require("playwright-core");
const b = await chromium.connectOverCDP("http://127.0.0.1:9333");
const pages = b.contexts().flatMap(c => c.pages()).filter(p => p.url().includes("flow.google.com/project"));
for (const p of pages) {
  const btn = p.getByRole("button", { name: /^close$/i });
  const n = await btn.count();
  if (n) { await btn.first().click().catch(() => {}); }
  console.log(p.url().slice(-36), "close buttons:", n);
}
process.exit(0);

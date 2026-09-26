// Рендерит 7 вертикальных карточек в screenshots/card-N.png (1080×1350, IG 4:5).
// Анимации замораживаются — чистые статичные кадры. Запуск: node tests/screenshot.mjs
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { mkdirSync } from 'node:fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const outDir = resolve(root, 'screenshots');
mkdirSync(outDir, { recursive: true });

const N = 7;
const DSF = Number(process.env.SHOT_SCALE || 1);
const url = 'file://' + resolve(root, 'index.html') + '?export';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1160, height: 1500 }, deviceScaleFactor: DSF });
await page.goto(url, { waitUntil: 'load' });
await page.evaluate(() => document.fonts && document.fonts.ready);
await page.addStyleTag({ content: '*, *::before, *::after { animation: none !important; transition: none !important; }' });
await page.waitForTimeout(1000);

for (let n = 1; n <= N; n++) {
  const el = page.locator('#card-' + n);
  await el.scrollIntoViewIfNeeded();
  const box = await el.boundingBox();
  console.log(`card ${n}: ${Math.round(box.width)}×${Math.round(box.height)} (×${DSF})`);
  await el.screenshot({ path: resolve(outDir, `card-${n}.png`) });
}

await browser.close();
console.log('✓ screenshots →', outDir);

// Рендерит каждую карточку в screenshots/slide-N.png.
// Размер: 1080×1080 (нативный для Instagram). Для @2x (2160): SHOT_SCALE=2 node tests/screenshot.mjs
// Контактный лист (вся колода одним файлом): SHOT_SHEET=1 ...
// Запуск:  node tests/screenshot.mjs   (или `npm run shots`)
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { mkdirSync } from 'node:fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const outDir = resolve(root, 'screenshots');
mkdirSync(outDir, { recursive: true });

const N = 8;
const DSF = Number(process.env.SHOT_SCALE || 1);        // 1 → 1080px (IG native), 2 → 2160px
const url = 'file://' + resolve(root, 'index.html') + '?export';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1160, height: 1200 }, deviceScaleFactor: DSF });
await page.goto(url, { waitUntil: 'load' });
// дать шрифтам/раскладке/диаграммам устаканиться + поймать «живой» кадр анимации
await page.evaluate(() => document.fonts && document.fonts.ready);
await page.waitForTimeout(2200);

for (let n = 1; n <= N; n++) {
  const el = page.locator('#card-' + n);
  await el.scrollIntoViewIfNeeded();
  const box = await el.boundingBox();
  console.log(`slide ${n}: ${Math.round(box.width)}×${Math.round(box.height)} (×${DSF})`);
  await el.screenshot({ path: resolve(outDir, `slide-${n}.png`) });
}

if (process.env.SHOT_SHEET) {
  await page.screenshot({ path: resolve(outDir, 'contact-sheet.png'), fullPage: true });
  console.log('+ contact-sheet.png');
}

await browser.close();
console.log('✓ screenshots →', outDir);

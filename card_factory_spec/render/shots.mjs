// PNG-нарезка карточек (статичные, анимации заморожены на видимом состоянии).
// Использование:  node render/shots.mjs <папка-с-index.html> <кол-во карточек>
// Пример:         node render/shots.mjs examples/square_light 3
// Опции: SHOT_SCALE=2 → двойное разрешение.
import { chromium } from 'playwright';
import { resolve } from 'node:path';
import { mkdirSync } from 'node:fs';

const dir = resolve(process.argv[2] || 'examples/square_light');
const N = Number(process.argv[3] || 3);
const DSF = Number(process.env.SHOT_SCALE || 1);
const outDir = resolve(dir, 'png');
mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 2000 }, deviceScaleFactor: DSF });
await page.goto('file://' + resolve(dir, 'index.html') + '?export', { waitUntil: 'load' });
await page.evaluate(() => document.fonts && document.fonts.ready);
// Заморозка: у staged-элементов базовое состояние ВИДИМОЕ, поэтому animation:none
// даёт полный «спокойный» кадр без объектов на лету.
await page.addStyleTag({ content: '*, *::before, *::after { animation: none !important; transition: none !important; }' });
await page.waitForTimeout(900);

for (let n = 1; n <= N; n++) {
  const el = page.locator('#card-' + n);
  await el.scrollIntoViewIfNeeded();
  const box = await el.boundingBox();
  await el.screenshot({ path: resolve(outDir, `slide-${n}.png`) });
  console.log(`✓ slide-${n}.png  (${Math.round(box.width)}×${Math.round(box.height)} ×${DSF})`);
}
await browser.close();
console.log('✓ PNG →', outDir);

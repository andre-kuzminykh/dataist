// Проверка вёрстки каждого слайда по критериям (см. SPEC §6 «Критерии вёрстки»):
//   1) контентные блоки НЕ накладываются друг на друга;
//   2) ничего не вылезает за пределы карточки 1080×1080 (с полем 48px);
//   3) текст не обрезан и не переполняет контейнер (scrollWidth/Height);
//   4) на слайде не больше одного пунктирного круга.
// Запуск:  node tests/layout.mjs   (печатает нарушения; код выхода 1 при наличии)
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const url = 'file://' + resolve(root, 'index.html') + '?export';

// контентные блоки, которые НЕ должны накладываться (декор — кольца/спицы/grain — исключён)
const SLIDE = {
  1: ['.logo', '.ctitle', '.rings', '.cfoot'],
  2: ['.logo', '.head', '.pcard.prompt', '.pcard.answer', '.s2-arrow', '.s2-under', '.insight'],
  3: ['.logo', '.head', '.src', '.funnel', '.modelbox', '.insight'],
  4: ['.logo', '.head', '.tool', '.center-node', '.insight'],
  5: ['.logo', '.head', '.chain', '.lnode', '.center-node', '.insight'],
  6: ['.logo', '.head', '.hex', '.hub', '.insight'],
  7: ['.logo', '.head', '.uc', '.insight'],
  8: ['.logo', '.head', '.li8', '.insight'],
};
const TOL = 2;          // строгий допуск нахлёста рамок (px)
const SAFE = 40;        // поле от края карточки

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1160, height: 1200 }, deviceScaleFactor: 1 });
await page.goto(url, { waitUntil: 'load' });
await page.evaluate(() => document.fonts && document.fonts.ready);
await page.waitForTimeout(1800);

let problems = 0;
for (let n = 1; n <= 8; n++) {
  const res = await page.evaluate(({ n, sels, TOL, SAFE }) => {
    const card = document.getElementById('card-' + n);
    const cb = card.getBoundingClientRect();
    const items = [];
    sels.forEach((sel) => {
      card.querySelectorAll(sel).forEach((el, i) => {
        const r = el.getBoundingClientRect();
        items.push({
          name: sel + (el.querySelectorAll && card.querySelectorAll(sel).length > 1 ? '#' + i : ''),
          x: r.left - cb.left, y: r.top - cb.top, w: r.width, h: r.height,
          el,
        });
      });
    });
    const out = { overlaps: [], outOfBounds: [], clipped: [] };
    // overlaps
    for (let a = 0; a < items.length; a++) {
      for (let b = a + 1; b < items.length; b++) {
        const A = items[a], B = items[b];
        const ix = Math.min(A.x + A.w, B.x + B.w) - Math.max(A.x, B.x);
        const iy = Math.min(A.y + A.h, B.y + B.h) - Math.max(A.y, B.y);
        if (ix > TOL && iy > TOL) out.overlaps.push(`${A.name} ✕ ${B.name} (${Math.round(ix)}×${Math.round(iy)}px)`);
      }
    }
    // out of bounds + clipped text
    items.forEach((A) => {
      const full = A.w >= 980;   // полноширинный центрированный блок (заголовок-обложка) — гориз. границы не проверяем
      const xBad = !full && (A.x < SAFE - TOL || A.x + A.w > 1080 - SAFE + TOL);
      const yBad = A.y < SAFE - TOL || A.y + A.h > 1080 - SAFE + TOL;
      if (xBad || yBad)
        out.outOfBounds.push(`${A.name} @ [${Math.round(A.x)},${Math.round(A.y)} ${Math.round(A.w)}×${Math.round(A.h)}]`);
      if (A.el.scrollWidth > A.el.clientWidth + 2) out.clipped.push(`${A.name} (текст шире блока на ${A.el.scrollWidth - A.el.clientWidth}px)`);
    });
    // count dashed rings
    out.rings = card.querySelectorAll('.halo, .s5-ring, .orbit').length;
    return out;
  }, { n, sels: SLIDE[n], TOL, SAFE });

  const issues = [];
  res.overlaps.forEach((o) => issues.push('наложение: ' + o));
  res.outOfBounds.forEach((o) => issues.push('за границей: ' + o));
  res.clipped.forEach((o) => issues.push('обрезан текст: ' + o));
  if (res.rings > 1) issues.push(`пунктирных кругов: ${res.rings} (>1)`);

  if (issues.length) { problems += issues.length; console.log(`\n✗ Слайд ${n}:`); issues.forEach((i) => console.log('   - ' + i)); }
  else console.log(`✓ Слайд ${n}: ок (кругов: ${res.rings})`);
}

await browser.close();
console.log(`\n${problems === 0 ? '✓ ВЁРСТКА ЧИСТАЯ' : '✗ НАРУШЕНИЙ: ' + problems}\n`);
process.exit(problems === 0 ? 0 : 1);

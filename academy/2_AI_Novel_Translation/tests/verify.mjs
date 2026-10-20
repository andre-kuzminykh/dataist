// Автопроверки вертикальных карточек (контракт = SPEC.md):
// текст, тёмный фон, логотип, шрифт, размер 1080×1350, границы/обрезка текста.
// Запуск: node tests/verify.mjs
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import assert from 'node:assert/strict';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const url = 'file://' + resolve(root, 'index.html') + '?export';

let pass = 0, fail = 0;
function check(name, fn) {
  try { fn(); console.log('  ✓ ' + name); pass++; }
  catch (e) { console.log('  ✗ ' + name + '\n      ' + e.message); fail++; }
}

const PHRASES = {
  1: ['15', 'активных читателей'],
  2: ['3', 'языка', 'EN', 'FR', 'PL', 'JP'],
  3: ['Не сырой AI', 'фрагменты', 'стиль', 'перевод', 'проверка'],
  4: ['19', '30', 'длинных отрывков', 'за человеком'],
  5: ['522', '250', 'ЧЕЛОВЕК', 'AI', 'фрагменты: человек vs AI'],
  6: ['Проблема — в неровности', 'сильный абзац', 'неловкая фраза'],
  7: ['Главный вывод', 'AI пишет гладко', 'мелочи решают всё'],
};

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1160, height: 1500 } });
await page.goto(url, { waitUntil: 'load' });
await page.evaluate(() => document.fonts && document.fonts.ready);
await page.waitForTimeout(1200);

console.log('\nAI Novel Translation — verify\n');

const cardCount = await page.locator('.card').count();
check('7 карточек', () => assert.equal(cardCount, 7));

for (let n = 1; n <= 7; n++) {
  const box = await page.locator('#card-' + n).boundingBox();
  check(`card-${n}: 1080×1350`, () => { assert.equal(Math.round(box.width), 1080); assert.equal(Math.round(box.height), 1350); });
  const logo = await page.locator(`#card-${n} .logo img`).count();
  check(`card-${n}: логотип AIT`, () => assert.equal(logo, 1));
}

// тёмный фон
const bgs = await page.evaluate(() => {
  const out = {};
  for (let n = 1; n <= 7; n++) out[n] = getComputedStyle(document.getElementById('card-' + n)).backgroundColor;
  return out;
});
function lum(c){ const m = c.match(/\d+/g).map(Number); return 0.299*m[0]+0.587*m[1]+0.114*m[2]; }
for (let n = 1; n <= 7; n++) check(`card-${n}: тёмный фон`, () => assert.ok(lum(bgs[n]) < 40, 'lum=' + lum(bgs[n])));

// шрифт
const jbm = await page.evaluate(() => document.fonts.check("700 40px 'JetBrains Mono'"));
check('JetBrains Mono загружен', () => assert.ok(jbm));

// текст
for (let n = 1; n <= 7; n++) {
  const txt = (await page.locator('#card-' + n).innerText()).replace(/\s+/g, ' ').toLowerCase();
  for (const ph of PHRASES[n]) check(`card-${n}: «${ph}»`, () => assert.ok(txt.includes(ph.toLowerCase()), 'нет в DOM'));
}

// вёрстка: контент внутри кадра, текст не обрезан
const layout = await page.evaluate(() => {
  const out = [];
  const SAFE = 36, TOL = 4;
  for (let n = 1; n <= 7; n++) {
    const card = document.getElementById('card-' + n);
    const cb = card.getBoundingClientRect();
    card.querySelectorAll('.vb > *, .logo, .idx').forEach((el) => {
      const r = el.getBoundingClientRect();
      const x = r.left - cb.left, y = r.top - cb.top;
      if (x < SAFE - TOL || y < SAFE - TOL || x + r.width > 1080 - SAFE + TOL || y + r.height > 1350 - SAFE + TOL)
        out.push(`card-${n}: ${el.className || el.tagName} за границей [${Math.round(x)},${Math.round(y)} ${Math.round(r.width)}×${Math.round(r.height)}]`);
      if (el.scrollWidth > el.clientWidth + 2)
        out.push(`card-${n}: ${el.className} текст шире блока на ${el.scrollWidth - el.clientWidth}px`);
    });
  }
  return out;
});
check('вёрстка: всё в кадре, текст не обрезан', () => assert.ok(layout.length === 0, '\n      ' + layout.join('\n      ')));

// палитра: только flame/plum
const src = await page.content();
for (const b of ['#10B981', '#3B82F6', '#0EA5E9']) {
  check(`палитра: нет «${b}»`, () => assert.ok(!src.includes(b)));
}

await browser.close();
console.log(`\n${fail === 0 ? '✓ ВСЕ ТЕСТЫ ПРОШЛИ' : '✗ ЕСТЬ ПАДЕНИЯ'} — pass: ${pass}, fail: ${fail}\n`);
process.exit(fail === 0 ? 0 : 1);

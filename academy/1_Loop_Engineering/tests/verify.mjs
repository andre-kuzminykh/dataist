// Автотесты карточек урока (контракт = SPEC.md). Без зависимости от @playwright/test:
// используем глобальный playwright + node:assert. Запуск:
//   NODE_PATH=$(npm root -g) node tests/verify.mjs      (или `npm test`)
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const url = 'file://' + resolve(root, 'index.html') + '?export';

let pass = 0, fail = 0;
function check(name, fn) {
  try { fn(); console.log('  ✓ ' + name); pass++; }
  catch (e) { console.log('  ✗ ' + name + '\n      ' + e.message); fail++; }
}

// Ключевые фразы каждого слайда (должны присутствовать в DOM)
const PHRASES = {
  1: ['Хватит самому', 'писать промты', 'Loop Engineering', 'Harness Engineering',
      'Context Engineering', 'Prompt Engineering', 'промптят агентов вместо нас'],
  2: ['1. Prompt Engineering', 'Учимся правильно просить модель', 'ПРОМТ', 'Роль', 'Формат',
      'Ограничения', 'Примеры', 'ОТВЕТ', 'Один промт', 'итоговый результат'],
  3: ['2. Context Engineering', 'правильную информацию', 'Документы', 'Память', 'История', 'Правила',
      'Данные', 'КОНТЕКСТ', 'МОДЕЛЬ', 'не заполнять окно модели'],
  4: ['3. Harness Engineering', 'среду вокруг агента', 'АГЕНТ', 'Инструменты', 'MCP', 'Разрешения',
      'Guardrails', 'Логи', 'без обёртки', 'умеет действовать'],
  5: ['4. Loop Engineering', 'делает это вместо нас', 'Цель', 'Действие',
      'Фидбек', 'Память', 'не один запуск', 'повторяет цикл'],
  6: ['Из чего состоит', 'хороший loop', 'Автоматизация', 'когда запускать', 'Правила', 'Навыки',
      'Коннекторы', 'Агенты', 'Состояния', 'когда остановиться'],
  7: ['Для чего лучше', 'использовать loop', 'Исправление', 'Сортировка', 'Обновление',
      'Обработка', 'Исследовательский', 'Проверка', 'есть фидбек'],
  8: ['Лучшие практики', 'проверяемую цель', 'правильный контекст', 'маленькие шаги',
      'создателя и проверяющего', 'Сохраняйте состояния', 'guardrails', 'умеет проверять его работу'],
};

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1160, height: 1200 }, deviceScaleFactor: 1 });
await page.goto(url, { waitUntil: 'load' });
await page.evaluate(() => document.fonts && document.fonts.ready);
await page.waitForTimeout(1800);

console.log('\nLoop Engineering — verify\n');

// 1. ровно 8 карточек card-1..8
const cardCount = await page.locator('.card').count();
check('8 элементов .card', () => assert.equal(cardCount, 8));
for (let n = 1; n <= 8; n++) {
  const c = await page.locator('#card-' + n).count();
  check(`#card-${n} существует`, () => assert.equal(c, 1));
}

// 2. логотип на каждом слайде + onerror fallback
for (let n = 1; n <= 8; n++) {
  const has = await page.locator(`#card-${n} .logo img`).count();
  const onerr = await page.locator(`#card-${n} .logo img`).first().getAttribute('onerror');
  check(`#card-${n}: логотип AIT + fallback`, () => { assert.equal(has, 1); assert.ok(onerr && /ait-logo\.png/.test(onerr)); });
}

// 3. фон: слайд 1 тёмный, 2..8 светлый
const bg = await page.evaluate(() => {
  const rgb = (el) => getComputedStyle(el.querySelector('.bg')).backgroundColor;
  const out = {};
  for (let n = 1; n <= 8; n++) out[n] = rgb(document.getElementById('card-' + n));
  return out;
});
function lum(c){ const m = c.match(/\d+/g).map(Number); return (0.299*m[0]+0.587*m[1]+0.114*m[2]); }
check('слайд 1 — тёмный фон', () => assert.ok(lum(bg[1]) < 40, 'lum=' + lum(bg[1])));
for (let n = 2; n <= 8; n++) check(`слайд ${n} — светлый фон`, () => assert.ok(lum(bg[n]) > 210, 'lum=' + lum(bg[n])));

// 4. на каждом слайде есть хотя бы один активно анимируемый элемент
const animated = await page.evaluate(() => {
  const out = {};
  for (let n = 1; n <= 8; n++) {
    const card = document.getElementById('card-' + n);
    let count = 0;
    card.querySelectorAll('*').forEach((el) => {
      const s = getComputedStyle(el);
      if (s.animationName && s.animationName !== 'none' && s.animationPlayState === 'running'
          && parseFloat(s.animationDuration) > 0) count++;
    });
    out[n] = count;
  }
  return out;
});
for (let n = 1; n <= 8; n++) check(`слайд ${n}: есть постоянная анимация (${animated[n]} элем.)`, () => assert.ok(animated[n] >= 1));

// 5. блок-инсайт с лампочкой на слайдах 2..8
for (let n = 2; n <= 8; n++) {
  const ins = await page.locator(`#card-${n} .insight`).count();
  const bulb = await page.locator(`#card-${n} .insight .bulb svg`).count();
  check(`слайд ${n}: блок-инсайт + лампочка`, () => { assert.equal(ins, 1); assert.ok(bulb >= 1); });
}

// 6. применён JetBrains Mono
const jbm = await page.evaluate(() => document.fonts.check("700 40px 'JetBrains Mono'"));
check('шрифт JetBrains Mono загружен', () => assert.ok(jbm));
const famUsed = await page.evaluate(() => getComputedStyle(document.body).fontFamily);
check('font-family содержит JetBrains Mono', () => assert.ok(/JetBrains Mono/.test(famUsed)));

// 7. ключевые фразы каждого слайда
for (let n = 1; n <= 8; n++) {
  const txt = await page.locator('#card-' + n).innerText();
  const norm = txt.replace(/\s+/g, ' ');
  for (const ph of PHRASES[n]) {
    check(`слайд ${n}: текст «${ph}»`, () => assert.ok(norm.includes(ph), 'нет в DOM'));
  }
}

// 8. диаграммы построены скриптом (коннекторы/поток/орбита)
const diag = await page.evaluate(() => ({
  spokes4: document.querySelectorAll('#s4radial .spoke').length,
  hex6: document.querySelectorAll('#s6radial .hex').length,
  arrows6: document.querySelectorAll('#s6radial .cyc .ar').length,
  flow3: document.querySelectorAll('#s3lines .flowdot').length,
  tools4: document.querySelectorAll('#s4radial .tool').length,
}));
check('слайд 3: 5 текущих точек-потока', () => assert.equal(diag.flow3, 5));
check('слайд 4: 6 карточек-инструментов', () => assert.equal(diag.tools4, 6));
check('слайд 4: 6 текущих спиц к агенту', () => assert.ok(diag.spokes4 >= 6));
check('слайд 6: 6 карточек цикла', () => assert.equal(diag.hex6, 6));
check('слайд 6: вращающиеся стрелки цикла', () => assert.ok(diag.arrows6 >= 3));

// 9. палитра: только фиолетовый + оранжевый (никаких green/blue/sky)
const src = readFileSync(resolve(root, 'index.html'), 'utf8');
const banned = ['#10B981', '#3B82F6', '#0EA5E9', '16,185,129', '59,130,246', '14,165,233'];
for (const b of banned) {
  check(`палитра: нет постороннего цвета «${b}»`, () => assert.ok(!src.includes(b), 'найден в index.html'));
}

await browser.close();
console.log(`\n${fail === 0 ? '✓ ВСЕ ТЕСТЫ ПРОШЛИ' : '✗ ЕСТЬ ПАДЕНИЯ'} — pass: ${pass}, fail: ${fail}\n`);
process.exit(fail === 0 ? 0 : 1);

// Делает 8 ЦИКЛИЧНЫХ (бесшовных) GIF — по одному на слайд: gifs/slide-1..8.gif
//
// Идеальный цикл: все CSS-анимации приводятся к одному периоду T, затем через Web
// Animations API (document.getAnimations) кадр за кадром перематывается ровно один
// период — первый и «следующий» кадр совпадают, поэтому GIF зациклен без рывка.
// Не-цикличный keyframe `type` временно переопределяется на цикличный.
//
// Кодирование GIF — на чистом JS (gifenc), т.к. в песочнице ffmpeg минимальный.
// Запуск:  npm i gifenc pngjs && node tests/gif.mjs   (или `npm run gif`)
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { mkdirSync, writeFileSync } from 'node:fs';
import gifenc from 'gifenc';
import pngjs from 'pngjs';
const { GIFEncoder, quantize, applyPalette } = gifenc;
const { PNG } = pngjs;

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const outDir = resolve(root, 'gifs');
mkdirSync(outDir, { recursive: true });

const T = Number(process.env.GIF_T || 4000);      // период цикла, мс
const FPS = Number(process.env.GIF_FPS || 15);
const N = Math.round(T * FPS / 1000);             // кадров в цикле
const SIZE = Number(process.env.GIF_SIZE || 600); // сторона GIF, px
const OFFSET = 120000;                            // «устоявшийся» момент таймлайна
const url = 'file://' + resolve(root, 'index.html') + '?export';

// не-цикличный keyframe → цикличный + единый период; шум‑grain выключаем (он рушит сжатие GIF)
const CYCLIC = `
@keyframes type{0%{width:30%;opacity:.5}50%{width:92%;opacity:1}100%{width:30%;opacity:.5}}
*, *::before, *::after { animation-duration: ${T}ms !important; }
.grain { display: none !important; }
`;
const COLORS = Number(process.env.GIF_COLORS || 128);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1160, height: 1200 }, deviceScaleFactor: SIZE / 1080 });
await page.goto(url, { waitUntil: 'load' });
await page.evaluate(() => document.fonts && document.fonts.ready);
await page.waitForTimeout(1600);                  // дать скрипту построить диаграммы
await page.addStyleTag({ content: CYCLIC });
await page.waitForTimeout(300);
await page.evaluate(() => document.getAnimations().forEach(a => { try { a.pause(); } catch (e) {} }));

const delayMs = Math.round(1000 / FPS);
for (let n = 1; n <= 8; n++) {
  const el = page.locator('#card-' + n);
  const enc = GIFEncoder();
  for (let i = 0; i < N; i++) {
    const g = OFFSET + i * (T / N);
    await page.evaluate((gg) => document.getAnimations().forEach(a => { try { a.currentTime = gg; } catch (e) {} }), g);
    const buf = await el.screenshot({ type: 'png' });
    const { data, width, height } = PNG.sync.read(buf);   // RGBA
    const palette = quantize(data, COLORS, { format: 'rgb565' });
    const index = applyPalette(data, palette, 'rgb565');
    enc.writeFrame(index, width, height, { palette, delay: delayMs, transparent: false });
  }
  enc.finish();
  writeFileSync(resolve(outDir, 'slide-' + n + '.gif'), Buffer.from(enc.bytes()));
  console.log(`✓ slide-${n}.gif  (${N} кадров, ${SIZE}px, ${FPS}fps, цикл ${T}мс)`);
}

await browser.close();
console.log('\n✓ 8 циклических GIF (loop=∞) →', outDir);

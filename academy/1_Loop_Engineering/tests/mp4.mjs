// Делает 8 ЦИКЛИЧНЫХ MP4 (H.264) — по одному на слайд: mp4/slide-1..8.mp4
// Полное разрешение 1080×1080, полный цвет (в отличие от GIF).
//
// Бесшовный цикл: все анимации приводятся к одному периоду T, затем через
// document.getAnimations() снимается ровно один период — при зацикливании видео шва нет.
// Кодек H.264 (WASM h264-mp4-encoder). grain оставляем — он статичный и хорошо жмётся.
//
// Запуск:  npm i h264-mp4-encoder pngjs && node tests/mp4.mjs   (или `npm run mp4`)
import { chromium } from 'playwright';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { mkdirSync, writeFileSync } from 'node:fs';
import HME from 'h264-mp4-encoder';
import pngjs from 'pngjs';
const { PNG } = pngjs;

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');
const outDir = resolve(root, 'mp4');
mkdirSync(outDir, { recursive: true });

const T = Number(process.env.MP4_T || 4000);       // период цикла, мс
const FPS = Number(process.env.MP4_FPS || 25);
const N = Math.round(T * FPS / 1000);              // кадров в цикле
const SIZE = Number(process.env.MP4_SIZE || 1080); // сторона видео, px
const QP = Number(process.env.MP4_QP || 20);       // качество H.264 (10..51, меньше = лучше)
const OFFSET = 120000;
const url = 'file://' + resolve(root, 'index.html') + '?export';

const CYCLIC = `
@keyframes type{0%{width:30%;opacity:.5}50%{width:92%;opacity:1}100%{width:30%;opacity:.5}}
*, *::before, *::after { animation-duration: ${T}ms !important; }
`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1160, height: 1200 }, deviceScaleFactor: SIZE / 1080 });
await page.goto(url, { waitUntil: 'load' });
await page.evaluate(() => document.fonts && document.fonts.ready);
await page.waitForTimeout(1600);
await page.addStyleTag({ content: CYCLIC });
await page.waitForTimeout(300);
await page.evaluate(() => document.getAnimations().forEach(a => { try { a.pause(); } catch (e) {} }));

for (let n = 1; n <= 8; n++) {
  const el = page.locator('#card-' + n);
  const enc = await HME.createH264MP4Encoder();
  enc.width = SIZE; enc.height = SIZE; enc.frameRate = FPS; enc.quantizationParameter = QP;
  enc.outputFilename = 'out.mp4';
  enc.initialize();
  for (let i = 0; i < N; i++) {
    const g = OFFSET + i * (T / N);
    await page.evaluate((gg) => document.getAnimations().forEach(a => { try { a.currentTime = gg; } catch (e) {} }), g);
    const buf = await el.screenshot({ type: 'png' });
    const { data } = PNG.sync.read(buf);   // RGBA, SIZE×SIZE
    enc.addFrameRgba(data);
  }
  enc.finalize();
  writeFileSync(resolve(outDir, 'slide-' + n + '.mp4'), Buffer.from(enc.FS.readFile(enc.outputFilename)));
  enc.delete();
  console.log(`✓ slide-${n}.mp4  (${SIZE}px, ${N} кадров, ${FPS}fps, цикл ${T}мс, QP${QP})`);
}

await browser.close();
console.log('\n✓ 8 циклических MP4 →', outDir);

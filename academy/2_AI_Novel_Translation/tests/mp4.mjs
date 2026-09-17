// Делает 7 ЦИКЛИЧНЫХ MP4 (H.264) — по одному на карточку: mp4/card-1..7.mp4
// Вертикаль 1080×1350, полный цвет.
//
// Бесшовный цикл: все анимации приводятся к одному периоду T, затем через
// document.getAnimations() снимается ровно один период — при повторе шва нет.
// Кодек H.264 (WASM h264-mp4-encoder), т.к. ffmpeg в песочнице минимальный.
//
// Запуск:  npm i && node tests/mp4.mjs   (или `npm run mp4`)
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

const T = Number(process.env.MP4_T || 4500);       // период цикла, мс
const FPS = Number(process.env.MP4_FPS || 25);
const N = Math.round(T * FPS / 1000);
const W = 1080, H = 1350;                          // 4:5 (обе стороны чётные для H.264)
const QP = Number(process.env.MP4_QP || 20);
// OFFSET кратен T → видео стартует с «нулевой» фазы цикла (столбики растут с нуля и т.п.)
const OFFSET = Math.ceil(120000 / T) * T;
const url = 'file://' + resolve(root, 'index.html') + '?export';

const CYCLIC = `*, *::before, *::after { animation-duration: ${T}ms !important; }`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1160, height: 1500 }, deviceScaleFactor: 1 });
await page.goto(url, { waitUntil: 'load' });
await page.evaluate(() => document.fonts && document.fonts.ready);
await page.waitForTimeout(1200);
await page.addStyleTag({ content: CYCLIC });
await page.waitForTimeout(300);
await page.evaluate(() => document.getAnimations().forEach(a => { try { a.pause(); } catch (e) {} }));

for (let n = 1; n <= 7; n++) {
  const el = page.locator('#card-' + n);
  await el.scrollIntoViewIfNeeded();
  const enc = await HME.createH264MP4Encoder();
  enc.width = W; enc.height = H; enc.frameRate = FPS; enc.quantizationParameter = QP;
  enc.outputFilename = 'out.mp4';
  enc.initialize();
  for (let i = 0; i < N; i++) {
    const g = OFFSET + i * (T / N);
    await page.evaluate((gg) => document.getAnimations().forEach(a => { try { a.currentTime = gg; } catch (e) {} }), g);
    const buf = await el.screenshot({ type: 'png' });
    const { data } = PNG.sync.read(buf);
    enc.addFrameRgba(data);
  }
  enc.finalize();
  writeFileSync(resolve(outDir, 'card-' + n + '.mp4'), Buffer.from(enc.FS.readFile(enc.outputFilename)));
  enc.delete();
  console.log(`✓ card-${n}.mp4  (${W}×${H}, ${N} кадров, ${FPS}fps, цикл ${T}мс, QP${QP})`);
}

await browser.close();
console.log('\n✓ 7 циклических MP4 →', outDir);

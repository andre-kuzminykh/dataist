// MP4-нарезка карточек: БЕСШОВНО-ЦИКЛИЧНЫЕ видео (H.264).
// Использование:  node render/mp4.mjs <папка-с-index.html> <кол-во карточек>
// Пример:         node render/mp4.mjs examples/vertical_dark 3
// Опции: MP4_T=5000 (период цикла, мс) MP4_FPS=25 MP4_QP=20 (10..51, меньше=лучше).
//
// Техника бесшовного цикла:
// 1) всем анимациям принудительно задаётся ОДИН период T;
// 2) через document.getAnimations() таймлайн перематывается покадрово ровно на один период;
// 3) OFFSET кратен T → видео начинается с фазы 0 (карточка пустая, элементы
//    появляются по очереди с первого кадра), последний кадр = первому.
import { chromium } from 'playwright';
import { resolve } from 'node:path';
import { mkdirSync, writeFileSync } from 'node:fs';
import HME from 'h264-mp4-encoder';
import pngjs from 'pngjs';
const { PNG } = pngjs;

const dir = resolve(process.argv[2] || 'examples/vertical_dark');
const N = Number(process.argv[3] || 3);
const T = Number(process.env.MP4_T || 5000);
const FPS = Number(process.env.MP4_FPS || 25);
const QP = Number(process.env.MP4_QP || 20);
const FRAMES = Math.round(T * FPS / 1000);
const OFFSET = Math.ceil(120000 / T) * T;
const outDir = resolve(dir, 'mp4');
mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 2000 }, deviceScaleFactor: 1 });
await page.goto('file://' + resolve(dir, 'index.html') + '?export', { waitUntil: 'load' });
await page.evaluate(() => document.fonts && document.fonts.ready);
await page.waitForTimeout(900);
await page.addStyleTag({ content: `*, *::before, *::after { animation-duration: ${T}ms !important; }` });
await page.waitForTimeout(200);
await page.evaluate(() => document.getAnimations().forEach(a => { try { a.pause(); } catch (e) {} }));

for (let n = 1; n <= N; n++) {
  const el = page.locator('#card-' + n);
  await el.scrollIntoViewIfNeeded();
  const box = await el.boundingBox();
  const W = Math.round(box.width), H = Math.round(box.height);   // обе стороны должны быть чётными
  const enc = await HME.createH264MP4Encoder();
  enc.width = W; enc.height = H; enc.frameRate = FPS; enc.quantizationParameter = QP;
  enc.outputFilename = 'out.mp4';
  enc.initialize();
  for (let i = 0; i < FRAMES; i++) {
    const g = OFFSET + i * (T / FRAMES);
    await page.evaluate((gg) => document.getAnimations().forEach(a => { try { a.currentTime = gg; } catch (e) {} }), g);
    const buf = await el.screenshot({ type: 'png' });
    enc.addFrameRgba(PNG.sync.read(buf).data);
  }
  enc.finalize();
  writeFileSync(resolve(outDir, `slide-${n}.mp4`), Buffer.from(enc.FS.readFile(enc.outputFilename)));
  enc.delete();
  console.log(`✓ slide-${n}.mp4  (${W}×${H}, ${FRAMES} кадров, ${FPS}fps, цикл ${T}мс)`);
}
await browser.close();
console.log('✓ MP4 →', outDir);

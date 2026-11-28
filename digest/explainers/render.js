// Покадровый рендер ролика: node render.js work/cfg-<ролик>.json work/out-<ролик> [секунды для пробных кадров...]
// compose.html кладёт поверх кадров фона текст сцены и рисует кадр; кадр — скриншот 1120×630.
// В cfg можно указать другую сцену и размер кадра: "compose": "compose-square.html", "size": [720, 720].
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [cfgPath, outDir, ...probe] = process.argv.slice(2);
  const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  if (!probe.length) fs.rmSync(outDir, { recursive: true, force: true }); // без старых кадров от прошлого, более длинного ролика
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const [width, height] = cfg.size || [1120, 630];
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(__dirname, cfg.compose || 'compose.html'), { waitUntil: 'networkidle' });
  await page.evaluate(async () => {
    await document.fonts.load("800 40px 'JetBrains Mono'"); await document.fonts.load("600 16px 'JetBrains Mono'");
    await document.fonts.load("500 46px 'Geist'"); await document.fonts.load("400 21px 'Geist'"); await document.fonts.load("600 18px 'Geist'");
    await document.fonts.ready;
  });
  const total = await page.evaluate(c => window.setup(c), cfg);
  const times = probe.length ? probe.map(Number) : [...Array(Math.round(total * cfg.fps)).keys()].map(f => f / cfg.fps);
  for (let f = 0; f < times.length; f++) {
    await page.evaluate(t => window.render(t), times[f]);
    await page.screenshot({ path: path.join(outDir, probe.length ? `probe-${times[f]}.png` : `f${String(f).padStart(4, '0')}.png`) });
  }
  console.log(cfgPath, 'total', total.toFixed(2), 's, frames', times.length);
  await browser.close();
})();

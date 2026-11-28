// Запись анимаций сайтов без их текста (текст потом кладёт compose.html). Прячется весь текст сайта,
// даже мелкие подписи на схемах (в ролике их всё равно не прочитать) — остаются фигуры и иконки, см. hide-text.js.
// node record.js ait-ru | ait-en | nr | nr-gradient | nr-still   →  work/rec-<что>.webm + .json (время каждого слайда)
//   ait-*       — слайды andre.technology;
//   nr          — слайды neuronium.ai (живой свет фона — для MP4 на сайте);
//   nr-gradient — только свет фона neuronium.ai (финальная сцена);
//   nr-still    — слайды neuronium.ai на неподвижном свете фона (лёгкий GIF для письма) + work/lf-<слайд>.jpg.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { hideText } = require('./hide-text');

const WORK = path.join(__dirname, 'work');
const VIEW = { width: 1280, height: 720 };
const HOLD = 7200; // сколько показывать каждый слайд, мс
const AIT_SLIDES = ['change', 'maturity', 'strategy', 'neuronium', 'training', 'cases'];
const NR_SLIDES = ['slide-hero', 'slide-context', 'slide-management', 'slide-cases'];
const OFF = '{visibility:hidden!important;opacity:0!important}';
const NR_TEXT = ['#slide-hero .hero__line', '#slide-hero .hero__bar', '.ctx__head', '.dept__text', '.cs__title', '.cs-all', '.kq-km'];
const freezeCss = src => `.light-field__canvas{visibility:hidden!important} .light-field{background:#0c090d url(${src}) center/cover no-repeat!important}`;

async function lightSnapshots(browser) {
  // снимок одного света фона на каждом слайде (opacity, а не visibility: дети слайдов включают visibility обратно)
  const page = await browser.newPage({ viewport: VIEW });
  await page.goto('https://neuronium.ai/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2500);
  const snaps = {};
  for (let i = 0; i < NR_SLIDES.length; i++) {
    if (i) { await page.mouse.move(640, 400); await page.mouse.wheel(0, 900); await page.waitForTimeout(3200); }
    const st = await page.addStyleTag({ content: `header.nav,.progress,main.stage,.cw,.skip-link${OFF}` });
    await page.waitForTimeout(150);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    fs.writeFileSync(path.join(WORK, `lf-${NR_SLIDES[i]}.jpg`), buf);
    snaps[NR_SLIDES[i]] = 'data:image/jpeg;base64,' + buf.toString('base64');
    await st.evaluate(e => e.remove());
  }
  await page.close();
  return snaps;
}

(async () => {
  const what = process.argv[2];
  if (!['ait-ru', 'ait-en', 'nr', 'nr-gradient', 'nr-still'].includes(what)) throw new Error('что записать? ' + what);
  fs.mkdirSync(WORK, { recursive: true });
  const browser = await chromium.launch();
  const snaps = what === 'nr-still' ? await lightSnapshots(browser) : null;
  const dir = path.join(WORK, `rec-${what}`);
  fs.rmSync(dir, { recursive: true, force: true });
  const ctx = await browser.newContext({ viewport: VIEW, recordVideo: { dir, size: VIEW } });
  if (snaps) {
    await ctx.addInitScript(css => {
      const add = () => { const s = document.createElement('style'); s.id = 'lf-freeze'; s.textContent = css; document.documentElement.appendChild(s); };
      if (document.documentElement) add(); else document.addEventListener('DOMContentLoaded', add);
    }, freezeCss(snaps['slide-hero']));
  }
  await ctx.addInitScript(hideText, what.startsWith('ait-') ? '' : '.hero__word');  // NEURONIUM на первом слайде — крупный, оставляем
  const page = await ctx.newPage();
  const t0 = Date.now();
  const log = [];
  if (what.startsWith('ait-')) {
    await page.goto(`https://andre.technology/?lang=${what.slice(4)}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(2500);
    await page.addStyleTag({ content: '.hdr,.progress,#ring,.tip,.bcap,.caption,.speaker,#head,#msg-btn,.probe{visibility:hidden!important}' });
    await page.evaluate(() => document.querySelectorAll('.slide h2, .slide h1').forEach(h => { (h.closest('.cases-h') || h.parentElement).style.visibility = 'hidden'; }));
    for (const id of AIT_SLIDES) {
      await page.evaluate(i => document.querySelector(`[data-go="${i}"]`).click(), id);
      log.push({ id, t: (Date.now() - t0) / 1000 });
      await page.waitForTimeout(HOLD);
    }
  } else {
    await page.goto('https://neuronium.ai/', { waitUntil: 'networkidle', timeout: 60000 });
    const text = what === 'nr-gradient' ? [...NR_TEXT, '#slide-hero .hero__word', '#slide-hero .hero__rule'] : NR_TEXT;
    await page.addStyleTag({ content: `header.nav,.progress,.cw,.skip-link${OFF} ${text.join(',')}${OFF}` });
    const slides = what === 'nr-gradient' ? ['slide-hero'] : NR_SLIDES;
    for (let i = 0; i < slides.length; i++) {
      if (i) {
        if (snaps) await page.evaluate(css => { document.getElementById('lf-freeze').textContent = css; }, freezeCss(snaps[slides[i]]));
        await page.mouse.move(640, 400); await page.mouse.wheel(0, 900);
      }
      log.push({ id: slides[i], t: (Date.now() - t0) / 1000 });
      await page.waitForTimeout(HOLD);
    }
  }
  await ctx.close(); await browser.close();
  const f = fs.readdirSync(dir).find(x => x.endsWith('.webm'));
  fs.renameSync(path.join(dir, f), path.join(WORK, `rec-${what}.webm`));
  fs.rmSync(dir, { recursive: true, force: true });
  fs.writeFileSync(path.join(WORK, `rec-${what}.json`), JSON.stringify(log));
  console.log(what, JSON.stringify(log));
})();

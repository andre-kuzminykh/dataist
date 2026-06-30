# Урок 1 — Loop Engineering

Анимированные карточки-слайды для соцсетей по уроку **Loop Engineering**: путь от
*Prompt Engineering* к системам, которые промптят агентов вместо нас.

8 квадратных слайдов **1080×1080** в одном файле `index.html` (карусель + режим экспорта).
Шрифт — **JetBrains Mono**. Обложка тёмная, остальные 7 — светлые. Палитра — строго
**оранжевый + фиолетовый** (минимализм, без других цветов). На каждом слайде — постоянная
анимация. Иконки — inline-SVG (без CDN), шрифт и логотип — локальные, поэтому карточки
самодостаточны и работают офлайн.

## Файлы
```
index.html              ← всё здесь: 8 слайдов, стили, иконки-спрайт, карусель
SPEC.md                 ← спецификация (контент + дизайн + анимации + критерии приёмки)
assets/
  ait-logo.png          ← локальная копия логотипа AIT (fallback, если GitHub недоступен)
  fonts/*.ttf           ← JetBrains Mono (400/500/700/800), self-hosted
tests/
  verify.mjs            ← автотесты контракта (npm test)
  screenshot.mjs        ← рендер screenshots/slide-N.png (npm run shots)
  README.md
screenshots/            ← готовые PNG карточек (1080×1080 @2x) + contact-sheet
package.json
```

## Как смотреть / листать
Открой `index.html` в браузере. Навигация: стрелки ← →, свайп, точки снизу, клавиша «пробел».

## Как получить картинки для Instagram
- Готовые PNG уже лежат в `screenshots/` (`slide-1.png` … `slide-8.png`), размер **1080×1080** — нативный для IG.
- Перегенерировать: `npm install && npm run shots`.
- В удвоенном разрешении (2160×2160): `SHOT_SCALE=2 npm run shots`.
- Контактный лист всей колоды одним файлом: `SHOT_SHEET=1 npm run shots` → `screenshots/contact-sheet.png`.
- Или вручную: открыть `index.html?export` и заскринить каждую карточку.

> Логотип: основной источник — реальный логотип AIT с GitHub
> (`raw.githubusercontent.com/andre-kuzminykh/andre-ait-page/...png`); если он недоступен
> (офлайн), автоматически подставляется локальная копия `assets/ait-logo.png` — это та же
> картинка, поэтому логотип виден всегда, в т.ч. на скриншотах.

## Тесты
```bash
npm install
npm test        # проверка контракта из SPEC.md
npm run shots   # перегенерация скриншотов
```
См. `tests/README.md` и `SPEC.md`.

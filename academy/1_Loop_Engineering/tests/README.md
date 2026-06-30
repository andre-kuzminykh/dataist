# Тесты — Урок 1 Loop Engineering

Два скрипта на Playwright (без `@playwright/test`, чистый Node + `assert`).

## Установка
```bash
cd academy/1_Loop_Engineering
npm install            # ставит playwright (браузер Chromium тянуть не нужно, если он уже есть)
# npx playwright install chromium   # если браузера нет в системе
```

## Запуск
```bash
npm test     # tests/verify.mjs — проверяет контракт из SPEC.md (структура, фон, анимация, текст, шрифт, диаграммы)
npm run shots  # tests/screenshot.mjs — генерит screenshots/slide-1..8.png (1080×1080 @2x) + contact-sheet.png
```

Или напрямую (если playwright стоит глобально):
```bash
node tests/verify.mjs
node tests/screenshot.mjs
```

## Что проверяет `verify.mjs`
1. ровно 8 `.card` с `id=card-1..8`;
2. логотип AIT + `onerror`-fallback на каждом слайде;
3. слайд 1 — тёмный фон, слайды 2–8 — светлый;
4. на каждом слайде есть хотя бы один элемент с **активной** CSS-анимацией;
5. блок-инсайт с лампочкой на слайдах 2–8;
6. загружен и применён шрифт **JetBrains Mono**;
7. ключевые фразы каждого слайда присутствуют в DOM;
8. диаграммы построены скриптом (5 точек-потока, 6 коннекторов + 6 иконок орбиты, 6 пунктир-коннекторов).

## Просмотр
Открой `index.html` напрямую в браузере (двойной клик) — листай стрелками ← →, свайпом
или точками снизу. Для экспорта в картинки: `index.html?export` (все карточки в столбик,
натуральные 1080×1080).

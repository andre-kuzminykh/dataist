#!/usr/bin/env python3
"""Уроки без вшитых библиотек — сами.

Уроки серии 3.x приходят из генератора с Tailwind и Lucide, вшитыми прямо
в страницу: 1 МБ вместо ~130 КБ — в вебвью Telegram и на мобильном это
секунды загрузки. Остальные уроки подключают те же библиотеки ссылками
(и браузер берёт их из кэша), а ещё грузят telegram-web-app.js.

Скрипт приводит урок к тому же виду — и только там, где это ничего не
меняет на странице:
* вшитый Tailwind → <link> на /static/css/tailwind.css, только если он
  байт в байт равен файлу, который отдаёт сайт;
* вшитый Lucide → <script> с unpkg, как у остальных уроков, только если
  все иконки страницы уже есть на уроках, где Lucide подключён ссылкой;
* пустое место «Telegram Web App Script» → скрипт telegram-web-app.js.

Мета-теги (og, twitter, description, canonical) и всё после </head> не
трогаются — превью в Telegram то же, текст тот же; это проверяется.

Запуск: python3 scripts/education_slim.py          — показать, что изменится
        python3 scripts/education_slim.py --apply  — записать
        --tailwind ФАЙЛ — сверять с этим файлом, а не с сайтом
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDU = ROOT / "education"
SITE = "https://dataist.ai"
TW_URL = SITE + "/static/css/tailwind.css"
TW_LINK = '<link rel="stylesheet" href="/static/css/tailwind.css">'
LUCIDE_TAG = '<script src="https://unpkg.com/lucide@latest"></script>'
TG_TAG = '<script src="https://telegram.org/js/telegram-web-app.js"></script>'

TW_RE = re.compile(r'(<!-- Tailwind CSS -->\n[ \t]*)<style>(.*?)</style>', re.S)
LUCIDE_RE = re.compile(r'<script>/\*\*\n \* @license lucide v[\d.]+ - ISC\n.*?</script>', re.S)
TG_RE = re.compile(r'(<!-- Telegram Web App Script -->\n([ \t]*))\n')
ICON_RE = re.compile(r'data-lucide="([a-z0-9-]+)"')
KEEP_RE = re.compile(r'<meta\b[^>]*>|<link\s+rel="(?:canonical|alternate)"[^>]*>')


def fetch_tailwind(path: str | None) -> str | None:
    if path:
        return Path(path).read_text(encoding="utf-8")
    try:
        with urllib.request.urlopen(TW_URL, timeout=30) as r:
            return r.read().decode("utf-8")
    except Exception as e:                                # noqa: BLE001
        print(f"tailwind.css с сайта не получен ({e}) — Tailwind не трогаю")
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="записать изменения")
    ap.add_argument("--tailwind", help="файл tailwind.css для сверки вместо сайта")
    args = ap.parse_args()

    pages = {p.parent.name: p.read_text(encoding="utf-8") for p in sorted(EDU.glob("*/index.html"))}
    heavy = {s: src for s, src in pages.items()
             if TW_RE.search(src.split("</head>", 1)[0]) or LUCIDE_RE.search(src.split("</head>", 1)[0])
             or TG_RE.search(src.split("</head>", 1)[0])}
    if not heavy:
        print("уроков с вшитыми библиотеками нет")
        return 0

    tailwind = fetch_tailwind(args.tailwind) if any(TW_RE.search(s) for s in heavy.values()) else None
    # Иконки, которые уже рисуются Lucide со ссылки — на других уроках.
    proven = {i for src in pages.values() if LUCIDE_TAG in src for i in ICON_RE.findall(src)}

    out: dict[Path, str] = {}
    for slug, src in heavy.items():
        canon = f'<link rel="canonical" href="{SITE}/education/{slug}/">'
        if canon not in src:
            continue                                   # не опубликованный урок
        head, body = src.split("</head>", 1)
        new, done = head, []
        m = TW_RE.search(new)
        if m and tailwind is not None and m.group(2) in (tailwind, tailwind.rstrip("\n")):
            new = new[:m.start()] + m.group(1) + TW_LINK + new[m.end():]
            done.append("Tailwind")
        elif m and tailwind is not None:
            print(f"{slug}: вшитый Tailwind не совпал с сайтом — оставляю")
        m = LUCIDE_RE.search(new)
        if m:
            missing = sorted(set(ICON_RE.findall(src)) - proven)
            if not missing:
                new = new[:m.start()] + LUCIDE_TAG + new[m.end():]
                done.append("Lucide")
            else:
                print(f"{slug}: иконок {missing} нет на других уроках — Lucide оставляю")
        m = TG_RE.search(new)
        if m and "telegram-web-app.js" not in src:
            new = new[:m.start()] + m.group(1) + TG_TAG + "\n" + new[m.end():]
            done.append("telegram-web-app")
        if not done:
            continue
        assert KEEP_RE.findall(new) == KEEP_RE.findall(head), slug
        result = new + "</head>" + body
        assert result.split("</head>", 1)[1] == body
        out[EDU / slug / "index.html"] = result
        print(f"{slug}: {', '.join(done)} — {len(src.encode()) // 1024} → {len(result.encode()) // 1024} КБ")

    if not out:
        print("менять нечего")
        return 0
    if not args.apply:
        print("сухой прогон — ничего не записано (запись: --apply)")
        return 0
    for path, text in out.items():
        path.write_text(text, encoding="utf-8")
    print("записано")
    return 0


if __name__ == "__main__":
    sys.exit(main())

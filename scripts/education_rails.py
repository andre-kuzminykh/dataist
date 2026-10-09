#!/usr/bin/env python3
"""Ленты «Читайте также» раздела «Обучение» — сами.

Ленты уроков берут карточки из education/index.json, а в разметке каждого
урока лежит весь раздел — для читателей без JS и для поисковых роботов.
Раньше и то и другое правили руками на каждом новом уроке: забыли — урок
не виден ни из одной ленты (так было с 3.1–3.4). А уроки, залитые из
черновиков серии, приносили карточки ещё не вышедших уроков — ссылки в
никуда.

Скрипт сверяет всё с тем, что реально опубликовано:
* index.json — запись на каждый урок; новая собирается из <head> урока
  (og:title, og:description, og:image, article:published_time); записи
  уроков, которых нет, убираются; остальные не трогаются;
* вшитая лента каждого урока — все остальные уроки, свежие первыми;
  карточки, совпадающие с собранной, остаются байт в байт, меняется
  только то, что нужно: новые уроки, исчезнувшие, сменившийся заголовок.

<head> и остальная страница уроков не трогаются — превью в Telegram то же.

Запуск: python3 scripts/education_rails.py          — показать, что изменится
        python3 scripts/education_rails.py --apply  — записать
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDU = ROOT / "education"
INDEX = EDU / "index.json"
SITE = "https://dataist.ai"
CARD_RE = re.compile(
    r'(\s*)(<a href="https://dataist\.ai/education/([^"/]+)/" role="listitem">.*?</a>)', re.S)
RAIL_RE = re.compile(r'(<div class="rel-rail[^"]*"[^>]*role="list">)(.*?)(\n[ \t]*</div>)', re.S)
SEP = "\n" + " " * 28


def _meta(head: str, key: str) -> str | None:
    m = re.search(r'<meta\s+(?:property|name)="%s"\s+content="([^"]*)"' % re.escape(key), head)
    return m.group(1) if m else None


def lesson_entry(slug: str) -> dict | None:
    """Запись index.json по самой странице урока; None — не опубликованный урок."""
    page = EDU / slug / "index.html"
    try:
        src = page.read_text(encoding="utf-8")
    except OSError:
        return None
    head = src.split("</head>")[0]
    url = f"{SITE}/education/{slug}/"
    canon = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', head)
    title = _meta(head, "og:title")
    pub = _meta(head, "article:published_time")
    if not canon or canon.group(1) != url or not title or not pub:
        return None
    return {
        "slug": slug,
        "title": html.unescape(title).strip(),
        "teaser": html.unescape(_meta(head, "og:description") or "").strip(),
        "cover": _meta(head, "og:image") or "",
        "url": url,
        "date": pub[:10],
        "published_at": pub,
        "category": "education",
        "source": "",
    }


def card(e: dict) -> str:
    d = e["date"]
    t = html.escape(html.unescape(e["title"]), quote=False)
    return (f'<a href="{e["url"]}" role="listitem">\n'
            f'                                <span class="rel-thumb"><img src="{e["cover"]}" alt="" loading="lazy" decoding="async"></span>\n'
            f'                                <time datetime="{d}">{d[8:10]}.{d[5:7]}.{d[:4]}</time>\n'
            f'                                <span class="rel-title">{t}</span>\n'
            f'                            </a>')


def _natural(s: str) -> list:
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s or "")]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="записать изменения")
    args = ap.parse_args()

    raw = INDEX.read_text(encoding="utf-8")
    feed = json.loads(raw)
    published = {d.name: e for d in EDU.iterdir() if d.is_dir() and (e := lesson_entry(d.name))}

    # 1. index.json: добавить вышедшие, убрать исчезнувшие, остальные — как есть
    added = [s for s in published if s not in {e["slug"] for e in feed}]
    gone = [e["slug"] for e in feed if e["slug"] not in published]
    feed = [e for e in feed if e["slug"] in published] + [published[s] for s in added]
    # Урок поправили (заголовок, обложку, дату) — карточка следует за ним.
    # Анонс (teaser) не трогаем: его могли написать для ленты отдельно.
    changed = []
    for e in feed:
        page = published[e["slug"]]
        for k in ("title", "cover", "url", "date", "published_at"):
            if e.get(k) != page[k]:
                e[k] = page[k]
                changed.append(e["slug"])
    feed.sort(key=lambda e: (str(e.get("published_at") or e.get("date") or ""), _natural(e["slug"])),
              reverse=True)
    new_raw = json.dumps(feed, ensure_ascii=False, indent=2) + "\n"

    # 2. вшитые ленты уроков
    by_slug = {e["slug"]: e for e in feed}
    pages: dict[Path, str] = {}
    for slug in sorted(published, key=_natural):
        path = EDU / slug / "index.html"
        src = path.read_text(encoding="utf-8")
        m = RAIL_RE.search(src)
        if not m:
            continue
        inner = m.group(2)
        items = [(mm.group(1), mm.group(2), mm.group(3)) for mm in CARD_RE.finditer(inner)]
        if not items:
            continue
        matches = list(CARD_RE.finditer(inner))
        lead, tail_ws = inner[:matches[0].start()], inner[matches[-1].end():]
        have = {s: text for _, text, s in items}
        want = [e["slug"] for e in feed if e["slug"] != slug]
        first_ws = items[0][0]
        rest_ws = items[1][0] if len(items) > 1 else SEP
        parts = []
        for i, s in enumerate(want):
            fresh = card(by_slug[s])
            text = have[s] if have.get(s) == fresh else fresh
            parts.append((first_ws if i == 0 else rest_ws) + text)
        new_inner = lead + "".join(parts) + tail_ws
        if new_inner != inner:
            out = src[:m.start(2)] + new_inner + src[m.end(2):]
            assert out.split("</head>", 1)[0] == src.split("</head>", 1)[0]
            pages[path] = out

    print(f"уроков опубликовано: {len(published)} | в index.json добавить: {added} | убрать: {gone}"
          f" | обновить: {sorted(set(changed))} | лент к обновлению: {len(pages)}")
    if not args.apply:
        print("сухой прогон — ничего не записано (запись: --apply)")
        return 0
    if new_raw != raw:
        INDEX.write_text(new_raw, encoding="utf-8")
    for path, text in pages.items():
        path.write_text(text, encoding="utf-8")
    print("записано")
    return 0


if __name__ == "__main__":
    sys.exit(main())

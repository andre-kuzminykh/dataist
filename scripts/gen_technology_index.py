#!/usr/bin/env python3
"""Собирает technology/index.json из метаданных самих статей раздела.

Ленту внизу материала рисует браузер по этому файлу — как в разделе новостей
по news/index.json. Данные берутся из <meta> и JSON-LD каждой страницы, а не
переписываются руками, поэтому файл не расходится со статьями.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / 'technology'
OUT = DIR / 'index.json'


def meta(t, name, attr='property'):
    m = re.search(rf'<meta {attr}="{re.escape(name)}"\s+content="([^"]*)"', t)
    return m.group(1) if m else None


def jsonld(t, key):
    m = re.search(rf'"{re.escape(key)}":\s*"([^"]*)"', t)
    return m.group(1) if m else None


items = []
for d in sorted(p for p in DIR.iterdir() if p.is_dir()):
    page = d / 'index.html'
    if not page.exists():
        continue
    t = page.read_text(encoding='utf-8', errors='replace')
    title = meta(t, 'og:title') or ''
    published = meta(t, 'article:published_time') or jsonld(t, 'datePublished') or ''
    if not title or not published:
        sys.exit(f'{d.name}: нет заголовка или даты — правь страницу, а не индекс')
    items.append({
        'slug': d.name,
        'title': title,
        'teaser': (meta(t, 'og:description') or meta(t, 'description', 'name') or '').strip(),
        'cover': meta(t, 'og:image') or '',
        'url': meta(t, 'og:url') or f'https://dataist.ai/technology/{d.name}/',
        'date': published[:10],
        'published_at': published,
        'category': 'technology',
        'source': '',
    })

items.sort(key=lambda x: x['published_at'], reverse=True)
# Дата в ленте разбирается из первых десяти символов published_at, поэтому
# запись без времени не ломает карточку. Сверка на всякий случай.
for i in items:
    assert i['published_at'][:10] == i['date'], i['slug']
OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'{OUT}: {len(items)} материалов')
for i in items:
    print(f'  {i["date"]}  {i["slug"]:<22} {i["title"][:62]}')

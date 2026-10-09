#!/usr/bin/env python3
"""Короткие ссылки dataist.ai/<номер>.

Человек вбивает dataist.ai/37 и попадает на статью: на русскую, если первый
язык браузера русский (на телефоне это язык телефона), иначе на английскую.

Как устроено
------------
* shortlinks/registry.json — реестр: диапазоны номеров по разделам и выданные
  номера. Номер выдаётся ОДИН РАЗ и навсегда: его уже могли назвать вслух,
  напечатать, вставить в видео. Ничего не перенумеровывается.
* <номер>/index.html — страница-переадресация. В <head> — превью статьи
  (og/twitter берутся у русской версии, иначе у английской), поэтому ссылка
  в Telegram выглядит как сама статья. Страница закрыта от индексации.
  Приложение сайта такие папки статьями не считает: в ленты, sitemap и RSS
  они не попадают.
* shortlinks/README.md — таблица «номер → статья» и остаток номеров.

Новые статьи получают номера по порядку выхода. Кончился диапазон раздела —
номера идут из запасного, ссылки не перестают появляться. О том, что номера
заканчиваются (осталось меньше доли warn_left_share), о переходе на запасной
диапазон и о том, что номеров не осталось совсем, сообщается один раз:
с --notify — issue в репозитории с упоминанием владельца.

Запуск: python3 scripts/shortlinks.py            — показать, что изменится
        python3 scripts/shortlinks.py --apply    — записать
        python3 scripts/shortlinks.py --apply --notify   — то же + issue
                                                    (нужны GH_TOKEN и GITHUB_REPOSITORY)
"""
from __future__ import annotations

import argparse
import glob
import html
import json
import math
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "shortlinks" / "registry.json"
README = ROOT / "shortlinks" / "README.md"
SITE = "https://dataist.ai"
MARKER = "dataist-shortlink"
FALLBACK_IMAGE = SITE + "/cover.png"

# Где лежат статьи раздела. Пары RU/EN связаны через hreflang в <head>.
SECTION_GLOBS = {
    "research": ["20*/index.html", "research/*/index.html", "research/ru/*/index.html"],
    "education": ["education/*/index.html"],
    "news": ["news/*/index.html", "news/en/*/index.html"],
}
DATE_DIR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:_\d+)?/index\.html$")

DEFAULT_REGISTRY = {
    "about": "Короткие ссылки dataist.ai/<номер>. Номер выдаётся один раз и навсегда. "
             "Файл ведёт scripts/shortlinks.py — руками правятся только sections и warn_left_share.",
    "notify": "@andre-kuzminykh",
    "warn_left_share": 0.1,
    "sections": {
        "research": {"title": "Исследования", "enabled": True, "since": "2026-08-01",
                     "ranges": [[1, 999], [2000, 4999]]},
        "education": {"title": "Обучение", "enabled": False, "since": None,
                      "ranges": [[1001, 1999], [5000, 9999]]},
        "news": {"title": "Новости", "enabled": False, "since": "2026-10-01",
                 "ranges": [[10001, 99999], [100000, 999999]]},
    },
    "links": {},
    "alerts_sent": [],
}


# ---------------------------------------------------------------- чтение статей
def _head(src: str) -> str:
    end = src.find("</head>")
    return src[:end] if end >= 0 else src[:20000]


def _meta(head: str, key: str) -> str | None:
    m = re.search(r'<meta\s+(?:property|name)="%s"\s+content="([^"]*)"' % re.escape(key), head)
    return m.group(1) if m else None


def read_page(rel: str) -> dict | None:
    """Всё, что нужно о странице статьи; None — если это не опубликованная статья."""
    path = ROOT / rel
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    head = _head(src)
    lang = re.search(r'<html[^>]*\blang="([a-zA-Z]{2})', src[:1000])
    url = "/" + rel[: -len("index.html")]
    canon = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', head)
    if not lang or not canon or canon.group(1) != SITE + url:
        return None  # дубль (canonical смотрит на другую страницу) или не статья
    date = None
    m = DATE_DIR_RE.match(rel)
    if m:
        date = m.group(1)  # у папки-даты дата выхода — в имени, как и у приложения
    else:
        pub = _meta(head, "article:published_time")
        if not pub:
            ld = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', src)
            pub = ld.group(1) if ld else None
        date = pub[:10] if pub else None
    return {
        "url": url,
        "lang": lang.group(1).lower(),
        "date": date,
        "stamp": _meta(head, "article:published_time") or date or "",
        "hreflang": {l: u[len(SITE):] for l, u in re.findall(
            r'hreflang="(ru|en)"\s+href="(https://dataist\.ai/[^"]+)"', head)},
        "title": _meta(head, "og:title") or "",
        "description": _meta(head, "og:description") or "",
        "image": _meta(head, "og:image") or "",
        "image_w": _meta(head, "og:image:width"),
        "image_h": _meta(head, "og:image:height"),
    }


def discover(section: str) -> tuple[list[dict], dict[str, dict]]:
    """Статьи раздела парами {ru, en, date, stamp}; второй результат — все страницы."""
    pages: dict[str, dict] = {}
    for pattern in SECTION_GLOBS[section]:
        for p in glob.glob(str(ROOT / pattern)):
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            info = read_page(rel)
            if info and info["lang"] in ("ru", "en"):
                pages[info["url"]] = info
    items, used = [], set()
    # Якорь пары — русская страница; английская без русской — отдельная статья.
    for url, info in sorted(pages.items(), key=lambda kv: (kv[1]["lang"] != "ru", kv[0])):
        if url in used:
            continue
        twin_lang = "en" if info["lang"] == "ru" else "ru"
        twin = info["hreflang"].get(twin_lang)
        if twin and (twin not in pages or pages[twin]["hreflang"].get(info["lang"]) != url):
            twin = None  # пара не взаимная или двойника нет на диске
        if twin in used:
            twin = None
        ru, en = (url, twin) if info["lang"] == "ru" else (twin, url)
        anchor = pages[ru] if ru else pages[en]
        used.update(u for u in (ru, en) if u)
        if not anchor["date"]:
            continue
        items.append({"ru": ru, "en": en, "date": anchor["date"], "stamp": anchor["stamp"]})
    return items, pages


# ---------------------------------------------------------------- номера
def ranges_of(cfg: dict) -> list[tuple[int, int]]:
    return [(int(a), int(b)) for a, b in cfg["ranges"]]


def check_config(reg: dict) -> None:
    spans = []
    for name, cfg in reg["sections"].items():
        for a, b in ranges_of(cfg):
            if not (1 <= a <= b):
                raise SystemExit(f"Плохой диапазон {a}–{b} у раздела {name}")
            spans.append((a, b, name))
    spans.sort()
    for (a1, b1, n1), (a2, b2, n2) in zip(spans, spans[1:]):
        if a2 <= b1:
            raise SystemExit(f"Диапазоны пересекаются: {n1} {a1}–{b1} и {n2} {a2}–{b2}")


def next_number(cfg: dict, last: int | None) -> int | None:
    """Следующий свободный номер раздела: после последнего выданного, по диапазонам."""
    for a, b in ranges_of(cfg):
        if last is None or last < a:
            return a
        if a <= last < b:
            return last + 1
    return None


def section_state(reg: dict, section: str) -> dict:
    cfg = reg["sections"][section]
    nums = sorted(int(n) for n, e in reg["links"].items() if e["section"] == section)
    last = nums[-1] if nums else None
    rngs = ranges_of(cfg)
    idx = 0
    for i, (a, b) in enumerate(rngs):
        if last is not None and a <= last <= b:
            idx = i
    a, b = rngs[idx]
    used_in = sum(1 for n in nums if a <= n <= b)
    left_total = sum(b2 - max(a2 - 1, last or 0) for a2, b2 in rngs if b2 > (last or 0))
    return {"count": len(nums), "last": last, "range": (a, b), "range_index": idx,
            "used_in_range": used_in, "left_in_range": b - (last if last and last >= a else a - 1),
            "left_total": left_total}


# ---------------------------------------------------------------- страница-переадресация
def _clean(raw: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(raw or "")).strip()


def _attr(raw: str) -> str:
    return html.escape(_clean(raw), quote=True)


def _text(raw: str) -> str:
    return html.escape(_clean(raw), quote=False)


def render(n: int, entry: dict, pages: dict[str, dict]) -> str:
    ru = entry.get("ru") if entry.get("ru") in pages else None
    en = entry.get("en") if entry.get("en") in pages else None
    src = pages[ru] if ru else pages[en]
    ru_to, en_to = ru or en, en or ru
    title, desc = src["title"], src["description"]
    image = src["image"] or FALLBACK_IMAGE
    size = ""
    if src["image"] and src["image_w"] and src["image_h"]:
        size = (f'\n<meta property="og:image:width" content="{_attr(src["image_w"])}">'
                f'\n<meta property="og:image:height" content="{_attr(src["image_h"])}">')
    if ru and en:
        links = (f'<a href="{_attr(ru_to)}">Читать на русском</a> · '
                 f'<a href="{_attr(en_to)}" lang="en">Read in English</a>')
    else:
        links = f'<a href="{_attr(ru_to)}">Открыть статью</a>'
    js = json.dumps({"ru": ru_to, "en": en_to}, ensure_ascii=True).replace("</", "<\\/")
    return f"""<!DOCTYPE html>
<html lang="{'ru' if ru else 'en'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow">
<meta name="{MARKER}" content="{n}">
<title>{_text(title)}</title>
<script>
// Короткая ссылка dataist.ai/{n}: русская версия, если первый язык браузера
// русский (на телефоне — язык телефона), иначе английская. Файл создаёт
// scripts/shortlinks.py: правку руками затрёт следующий запуск.
(function () {{
  var to = {js}, lang = "";
  try {{ lang = (navigator.languages && navigator.languages[0]) || navigator.language || ""; }} catch (e) {{}}
  // Счётчик сайта (его вставляет приложение) здесь не нужен: просмотр
  // запишет статья. А чтобы в отчёте было видно, что пришли по короткой
  // ссылке, а не «изнутри сайта», — метка источника на сессию, тем же
  // ключом, что у ?utm_source=. Метку из адреса счётчик статьи прочтёт сам.
  window.__dataistTracker = true;
  try {{ if (!sessionStorage.getItem("dataist_src")) sessionStorage.setItem("dataist_src", "short"); }} catch (e) {{}}
  location.replace((/^ru(?:[-_]|$)/i.test(lang) ? to.ru : to.en) + location.search + location.hash);
}})();
</script>
<noscript><meta http-equiv="refresh" content="0; url={_attr(ru_to)}"></noscript>
<meta name="description" content="{_attr(desc)}">
<meta property="og:site_name" content="Датаист">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE}/{n}/">
<meta property="og:title" content="{_attr(title)}">
<meta property="og:description" content="{_attr(desc)}">
<meta property="og:image" content="{_attr(image)}">{size}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{_attr(title)}">
<meta name="twitter:description" content="{_attr(desc)}">
<meta name="twitter:image" content="{_attr(image)}">
<meta name="color-scheme" content="light dark">
<style>
body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
background:#fff;color:#111}}
@media (prefers-color-scheme:dark){{body{{background:#000;color:#eee}}a{{color:#eee}}}}
main{{padding:24px;text-align:center}}a{{color:#111}}
</style>
</head>
<body>
<main>
<p>Открываем статью…</p>
<p>{links}</p>
</main>
</body>
</html>
"""


# ---------------------------------------------------------------- README
def write_readme(reg: dict, pages_by_section: dict[str, dict]) -> str:
    out = ["# Короткие ссылки dataist.ai", "",
           "Человек вбивает `dataist.ai/<номер>` и попадает на статью: на русскую, если первый "
           "язык браузера русский (на телефоне — язык телефона), иначе на английскую. "
           "Номер выдаётся один раз и навсегда.", "",
           "Файл обновляется сам (`scripts/shortlinks.py`), руками его не правят.", "",
           "| Раздел | Номера | Выдано | Последний | Осталось в диапазоне |", "|---|---|---|---|---|"]
    for name, cfg in reg["sections"].items():
        st = section_state(reg, name)
        rng = ", ".join(f"{a}–{b}" + (" (запас)" if i else "") for i, (a, b) in enumerate(ranges_of(cfg)))
        status = "" if cfg.get("enabled") else " — пока выключен"
        out.append(f"| {cfg['title']}{status} | {rng} | {st['count']} | {st['last'] or '—'} | "
                   f"{st['left_in_range']} из {st['range'][1] - st['range'][0] + 1} |")
    for name, cfg in reg["sections"].items():
        rows = sorted(((int(n), e) for n, e in reg["links"].items() if e["section"] == name), key=lambda x: x[0])
        if not rows:
            continue
        pages = pages_by_section.get(name, {})
        out += ["", f"## {cfg['title']}", "", "| № | Дата | Статья | English |", "|---|---|---|---|"]
        for n, e in rows:
            def cell(url):
                if not url:
                    return "—"
                t = html.unescape(pages[url]["title"]) if url in pages else url
                t = t.replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
                return f"[{t}]({SITE}{url})"
            out.append(f"| [{n}]({SITE}/{n}) | {e['date']} | {cell(e.get('ru'))} | {cell(e.get('en'))} |")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- оповещения
def pending_alerts(reg: dict, exhausted: set[str]) -> list[dict]:
    alerts = []
    share = float(reg.get("warn_left_share", 0.1))
    who = reg.get("notify", "")
    for name, cfg in reg["sections"].items():
        if not cfg.get("enabled"):
            continue
        st = section_state(reg, name)
        a, b = st["range"]
        rngs = ranges_of(cfg)
        title = cfg["title"]
        if name in exhausted:
            alerts.append({"id": f"exhausted:{name}:{rngs[-1][0]}-{rngs[-1][1]}",
                           "title": f"Короткие ссылки: в разделе «{title}» номера закончились",
                           "body": f"{who} Все диапазоны раздела «{title}» ({cfg['ranges']}) заняты, "
                                   f"новые статьи остаются без короткой ссылки. Добавьте диапазон в "
                                   f"`shortlinks/registry.json` → `sections.{name}.ranges` — следующий "
                                   f"запуск сам выдаст номера всем, кто ждёт."})
            continue
        if st["range_index"] > 0 and st["count"]:
            alerts.append({"id": f"switch:{name}:{a}-{b}",
                           "title": f"Короткие ссылки: «{title}» перешли на запасной диапазон {a}–{b}",
                           "body": f"{who} Основной диапазон раздела «{title}» закончился, новые статьи "
                                   f"получают номера из запасного {a}–{b}. Ссылки продолжают появляться "
                                   f"сами, делать ничего не нужно. Последний номер: {st['last']}."})
        size = b - a + 1
        if st["count"] and st["left_in_range"] <= max(1, math.ceil(size * share)):
            nxt = next((f"{a2}–{b2}" for a2, b2 in rngs if a2 > b), None)
            then = (f"Когда закончится, номера автоматически пойдут из запасного диапазона {nxt}."
                    if nxt else "Запасного диапазона нет — добавьте его в `shortlinks/registry.json`.")
            alerts.append({"id": f"low:{name}:{a}-{b}",
                           "title": f"Короткие ссылки: в разделе «{title}» заканчиваются номера {a}–{b}",
                           "body": f"{who} В диапазоне {a}–{b} раздела «{title}» осталось "
                                   f"{st['left_in_range']} номеров из {size} (последний выданный — "
                                   f"{st['last']}). {then}"})
    sent = set(reg.get("alerts_sent", []))
    return [x for x in alerts if x["id"] not in sent]


def _github(method: str, path: str, payload: dict | None = None):
    token, repo = os.environ.get("GH_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        raise RuntimeError("нет GH_TOKEN/GITHUB_REPOSITORY")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}{path}",
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"},
        method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read() or b"null")


def open_issue(alert: dict) -> None:
    # Такое оповещение уже могло уйти, а запись об этом — не доехать до main
    # (пуш не прошёл): второй раз то же самое не пишем.
    for issue in _github("GET", "/issues?state=all&per_page=100") or []:
        if issue.get("title") == alert["title"]:
            return
    _github("POST", "/issues", {"title": alert["title"], "body": alert["body"]})


def send_telegram(alert: dict) -> bool:
    """Дубль оповещения в Telegram — если в секретах репозитория есть бот и чат."""
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        return False
    text = f"{alert['title']}\n\n{alert['body']}"
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=json.dumps({"chat_id": chat, "text": text, "disable_web_page_preview": True}).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status == 200


def notify(alert: dict) -> None:
    """Issue в репозитории (обязательно) и Telegram (если настроен)."""
    open_issue(alert)
    try:
        send_telegram(alert)
    except Exception as exc:  # issue уже есть — Telegram не повод повторять
        print(f"! Telegram не принял «{alert['title']}»: {exc}", file=sys.stderr)


# ---------------------------------------------------------------- главное
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="записать изменения")
    ap.add_argument("--notify", action="store_true", help="оповещения — issue в репозитории")
    ap.add_argument("--test-alert", action="store_true",
                    help="отправить пробное оповещение теми же путями и выйти")
    args = ap.parse_args()

    if args.test_alert:
        notify({"title": "Короткие ссылки: проверка оповещений",
                "body": f"{DEFAULT_REGISTRY['notify']} Это пробное сообщение: так придёт весть, когда "
                        "номера раздела начнут заканчиваться, когда раздел перейдёт на запасной "
                        "диапазон и если номера кончатся совсем. Закройте issue — больше не появится."})
        print("пробное оповещение отправлено")
        return 0

    reg = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() \
        else json.loads(json.dumps(DEFAULT_REGISTRY))
    check_config(reg)
    links: dict[str, dict] = reg["links"]

    new, updated, exhausted = [], [], set()
    pages_by_section: dict[str, dict] = {}
    for name, cfg in reg["sections"].items():
        if not cfg.get("enabled"):
            continue
        items, pages = discover(name)
        pages_by_section[name] = pages
        by_ru = {e["ru"]: n for n, e in links.items() if e["section"] == name and e.get("ru")}
        by_en = {e["en"]: n for n, e in links.items() if e["section"] == name and e.get("en")}
        fresh = []
        for it in items:
            n = by_ru.get(it["ru"]) if it["ru"] else None
            n = n or (by_en.get(it["en"]) if it["en"] else None)
            if n:
                e = links[n]
                # Двойник появился позже — дописываем; выданный номер не трогаем.
                for k in ("ru", "en"):
                    if it[k] and not e.get(k):
                        e[k] = it[k]
                        updated.append(n)
                continue
            if cfg.get("since") and it["date"] < cfg["since"]:
                continue
            fresh.append(it)
        fresh.sort(key=lambda it: (it["date"], it["stamp"], it["ru"] or it["en"]))
        last = section_state(reg, name)["last"]
        for it in fresh:
            n = next_number(cfg, last)
            while n is not None and (ROOT / str(n)).exists() and not _is_ours(n):
                print(f"! {n}: папка уже занята чужим содержимым — номер пропущен", file=sys.stderr)
                last = n
                n = next_number(cfg, last)
            if n is None:
                exhausted.add(name)
                break
            links[str(n)] = {"section": name, "date": it["date"], "ru": it["ru"], "en": it["en"]}
            new.append(n)
            last = n

    reg["links"] = {k: links[k] for k in sorted(links, key=int)}

    # Страницы: пересобираются все — двойник, заголовок или обложка статьи могли поменяться.
    writes: dict[Path, str] = {}
    for n, e in reg["links"].items():
        pages = pages_by_section.get(e["section"])
        if pages is None:
            continue  # раздел выключен — его страницы не трогаем
        if not ((e.get("ru") in pages) or (e.get("en") in pages)):
            print(f"! {n}: статьи {e.get('ru') or e.get('en')} больше нет — страницу не трогаем", file=sys.stderr)
            continue
        page = render(int(n), e, pages)
        target = ROOT / n / "index.html"
        if not target.exists() or target.read_text(encoding="utf-8") != page:
            writes[target] = page

    alerts = pending_alerts(reg, exhausted)
    readme = write_readme(reg, pages_by_section)

    print(f"новых номеров: {len(new)}" + (f" ({new[0]}–{new[-1]})" if new else "")
          + f" | дописан двойник: {len(set(updated))} | страниц к записи: {len(writes)}"
          + f" | оповещений: {len(alerts)}")
    for a in alerts:
        print(f"  ⚑ {a['title']}")
    if not args.apply:
        print("сухой прогон — ничего не записано (запись: --apply)")
        return 0

    failed = False
    if args.notify:
        for a in alerts:
            try:
                notify(a)
                reg.setdefault("alerts_sent", []).append(a["id"])
            except Exception as exc:  # оповещение не ушло — повторим в следующий запуск
                failed = True
                print(f"! не удалось открыть issue «{a['title']}»: {exc}", file=sys.stderr)

    for target, page in writes.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not README.exists() or README.read_text(encoding="utf-8") != readme:
        README.write_text(readme, encoding="utf-8")
    print("записано")
    return 1 if failed else 0


def _is_ours(n: int) -> bool:
    page = ROOT / str(n) / "index.html"
    try:
        return f'<meta name="{MARKER}" content="{n}">' in page.read_text(encoding="utf-8")[:3000]
    except OSError:
        return False


if __name__ == "__main__":
    sys.exit(main())

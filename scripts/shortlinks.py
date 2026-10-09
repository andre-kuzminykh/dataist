#!/usr/bin/env python3
"""Короткие ссылки dataist.ai/<номер>.

Человек вбивает dataist.ai/37 и попадает на статью: на русскую, если первый
язык браузера русский (на телефоне это язык телефона), иначе на английскую.

Как устроено
------------
* shortlinks/registry.json — реестр: диапазон номеров каждого раздела и
  выданные номера. Номер выдаётся ОДИН РАЗ и навсегда: его уже могли назвать
  вслух, напечатать, вставить в видео. Ничего не перенумеровывается.
* shortlinks/pages/<номер>.html — страница-переадресация. В <head> — превью
  статьи (og/twitter русской версии, иначе английской), поэтому ссылка в
  Telegram выглядит как сама статья; закрыта от индексации. По короткому
  адресу её отдаёт приложение сайта (маршрут /<число> в dataist-ai).
* <номер>/index.html — та же страница в папке, по-старому: так ссылки
  работают, пока приложение без этого маршрута. Пишется только для разделов
  из legacy_folders; новостям папки не делаются вовсе (их тысячи).
* shortlinks/README.md — сводка по разделам, shortlinks/<раздел>.md — списки
  «номер → статья».

Новые статьи получают номера по порядку выхода. Диапазон раздела кончился —
номера больше не выдаются (+1 дальше не идёт: залезли бы в номера соседнего
раздела). Об этом и заранее — когда остаётся меньше доли warn_left_share —
сообщается один раз: с --notify — issue в репозитории с упоминанием
владельца и, если есть секреты, сообщение в Telegram.

Новости ищутся по news/index.json, а читаются только новые: в автоматике
репозиторий скачан без статей, и нужная страница докачивается по одной.

Запуск: python3 scripts/shortlinks.py            — показать, что изменится
        python3 scripts/shortlinks.py --apply    — записать
        python3 scripts/shortlinks.py --apply --notify   — то же + оповещения
                                                    (нужны GH_TOKEN и GITHUB_REPOSITORY)
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import html
import json
import math
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "shortlinks" / "registry.json"
PAGES = ROOT / "shortlinks" / "pages"
README = ROOT / "shortlinks" / "README.md"
SITE = "https://dataist.ai"
MARKER = "dataist-shortlink"
FALLBACK_IMAGE = SITE + "/cover.png"

# Разделы, которые читаются целиком на каждом запуске (статей немного): у них
# страницы пересобираются всегда — вдруг сменились заголовок или обложка.
FULL_SECTIONS = {
    "research": ["20*/index.html", "research/*/index.html", "research/ru/*/index.html"],
    "education": ["education/*/index.html"],
}
NEWS_INDEX = "news/index.json"
NEWS_TWIN_DAYS = 14   # сколько дней ждать английскую версию новости
DATE_DIR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:_\d+)?/index\.html$")

DEFAULT_REGISTRY = {
    "about": "Короткие ссылки dataist.ai/<номер>. Номер выдаётся один раз и навсегда. "
             "Файл ведёт scripts/shortlinks.py — руками правятся только sections, "
             "warn_left_share и legacy_folders.",
    "notify": "@andre-kuzminykh",
    "warn_left_share": 0.1,
    "legacy_folders": ["research", "education"],
    "test_alert_request": "",
    "sections": {
        "research": {"title": "Исследования", "enabled": True, "since": "2026-08-01",
                     "ranges": [[1, 999]]},
        "education": {"title": "Обучение", "enabled": True, "since": None,
                      "ranges": [[1001, 1999]]},
        "news": {"title": "Новости", "enabled": True, "since": "2026-10-01",
                 "ranges": [[10001, 99999]]},
    },
    "links": {},
    "alerts_sent": [],
}


# ---------------------------------------------------------------- чтение статей
def read_text(rel: str) -> str | None:
    """Файл из рабочей копии, а если его там нет — из git (докачается по одному)."""
    path = ROOT / rel
    if path.is_file():
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{rel}"],
                             capture_output=True, timeout=120, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout.decode("utf-8", errors="replace") if out.returncode == 0 else None


def _head(src: str) -> str:
    end = src.find("</head>")
    return src[:end] if end >= 0 else src[:20000]


def _meta(head: str, key: str) -> str | None:
    m = re.search(r'<meta\s+(?:property|name)="%s"\s+content="([^"]*)"' % re.escape(key), head)
    return m.group(1) if m else None


def _rel(url: str) -> str:
    return url.strip("/") + "/index.html"


def read_page(rel: str) -> dict | None:
    """Всё, что нужно о странице статьи; None — если это не опубликованная статья."""
    src = read_text(rel)
    if src is None:
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


def prefetch(rels: list[str]) -> None:
    """Файлы, которых нет в рабочей копии, — из git одним запросом.

    В автоматике репозиторий скачан без содержимого файлов, и каждый
    `git show` докачивал бы свой файл отдельным запросом — по нескольку
    секунд на новость. Так докачивается вся пачка разом; в обычной копии,
    где файлы на месте, ничего не происходит.
    """
    missing = [r for r in dict.fromkeys(rels) if r and not (ROOT / r).is_file()]
    if not missing:
        return
    try:
        tree = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "HEAD", "--", *missing],
                              capture_output=True, text=True, timeout=120, check=False).stdout
        oids = [ln.split()[2] for ln in tree.splitlines() if len(ln.split()) >= 3 and ln.split()[1] == "blob"]
        if oids:
            subprocess.run(["git", "-C", str(ROOT), "-c", "fetch.negotiationAlgorithm=noop", "fetch",
                            "--no-tags", "--no-write-fetch-head", "--recurse-submodules=no",
                            "--filter=blob:none", "--stdin", "origin"],
                           input="\n".join(oids) + "\n", capture_output=True, text=True,
                           timeout=600, check=False)
    except (OSError, subprocess.TimeoutExpired):
        pass  # не вышло пачкой — read_text докачает по одному


class Pages(dict):
    """Прочитанные страницы по адресу; недостающие дочитываются по запросу."""

    def get_page(self, url: str | None) -> dict | None:
        if not url:
            return None
        if url not in self:
            self[url] = read_page(_rel(url))
        return self[url]

    def warm(self, urls: list[str]) -> None:
        """Страницы и их двойники — двумя пачками вместо запроса на каждую."""
        urls = [u for u in urls if u and u not in self]
        prefetch([_rel(u) for u in urls])
        twins = []
        for u in urls:
            info = self.get_page(u)
            if info:
                twins += [t for t in info["hreflang"].values() if t != u and t not in self]
        prefetch([_rel(t) for t in twins])


def pair_items(urls: list[str], pages: Pages) -> list[dict]:
    """Статьи парами {ru, en, date, stamp}: якорь — русская страница."""
    items, used = [], set()
    infos = [pages.get_page(u) for u in urls]
    infos = [i for i in infos if i and i["lang"] in ("ru", "en")]
    for info in sorted(infos, key=lambda i: (i["lang"] != "ru", i["url"])):
        url = info["url"]
        if url in used:
            continue
        twin_lang = "en" if info["lang"] == "ru" else "ru"
        twin = info["hreflang"].get(twin_lang)
        tw = pages.get_page(twin) if twin else None
        if not tw or tw["hreflang"].get(info["lang"]) != url or twin in used:
            twin = None  # пары нет, она не взаимная или двойник уже занят
        ru, en = (url, twin) if info["lang"] == "ru" else (twin, url)
        used.update(u for u in (ru, en) if u)
        if info["date"]:
            items.append({"ru": ru, "en": en, "date": info["date"], "stamp": info["stamp"]})
    return items


def discover_full(section: str, pages: Pages) -> list[dict]:
    urls = []
    for pattern in FULL_SECTIONS[section]:
        for p in glob.glob(str(ROOT / pattern)):
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            urls.append("/" + rel[: -len("index.html")])
    return pair_items(sorted(urls), pages)


def discover_news(since: str | None, known: set[str], pages: Pages) -> list[dict]:
    """Новые новости: кандидаты из news/index.json, читаются только незнакомые."""
    raw = read_text(NEWS_INDEX)
    if not raw:
        print(f"! нет {NEWS_INDEX} — новости пропущены", file=sys.stderr)
        return []
    floor = ""
    if since:  # дата в индексе по UTC, у страницы — по Москве: берём с запасом в день
        floor = (dt.date.fromisoformat(since) - dt.timedelta(days=1)).isoformat()
    urls = []
    for e in json.loads(raw):
        url = (e.get("url") or "").replace(SITE, "")
        if url and url not in known and str(e.get("date") or "") >= floor:
            urls.append(url)
    pages.warm(urls)
    return pair_items(urls, pages)


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
    """Следующий номер раздела после последнего выданного; None — диапазон кончился."""
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
    total = sum(b - a + 1 for a, b in rngs)
    left = sum(b - max(a - 1, last or 0) for a, b in rngs if b > (last or 0))
    return {"count": len(nums), "last": last, "total": total, "left": left}


# ---------------------------------------------------------------- страница-переадресация
def _clean(raw: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(raw or "")).strip()


def _attr(raw: str) -> str:
    return html.escape(_clean(raw), quote=True)


def _text(raw: str) -> str:
    return html.escape(_clean(raw), quote=False)


def render(n: int, entry: dict, pages: dict[str, dict]) -> str:
    ru = entry.get("ru") if pages.get(entry.get("ru")) else None
    en = entry.get("en") if pages.get(entry.get("en")) else None
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


# ---------------------------------------------------------------- списки
def _md(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")


def write_lists(reg: dict) -> dict[Path, str]:
    """README со сводкой и по списку «номер → статья» на раздел."""
    files: dict[Path, str] = {}
    out = ["# Короткие ссылки dataist.ai", "",
           "Человек вбивает `dataist.ai/<номер>` и попадает на статью: на русскую, если первый "
           "язык браузера русский (на телефоне — язык телефона), иначе на английскую. "
           "Номер выдаётся один раз и навсегда; кончился диапазон раздела — номера больше "
           "не выдаются, владельцу приходит оповещение.", "",
           "Файлы обновляются сами (`scripts/shortlinks.py`), руками их не правят.", "",
           "| Раздел | Номера | Выдано | Последний | Осталось | Список |", "|---|---|---|---|---|---|"]
    for name, cfg in reg["sections"].items():
        st = section_state(reg, name)
        rng = ", ".join(f"{a}–{b}" for a, b in ranges_of(cfg))
        status = "" if cfg.get("enabled") else " — выключен"
        if cfg.get("enabled") and st["count"] and not st["left"]:
            status = " — **номера закончились**"
        out.append(f"| {cfg['title']}{status} | {rng} | {st['count']} | {st['last'] or '—'} | "
                   f"{st['left']} из {st['total']} | [{name}.md]({name}.md) |")
        rows = sorted(((int(n), e) for n, e in reg["links"].items() if e["section"] == name),
                      key=lambda x: x[0])
        sec = [f"# Короткие ссылки — {cfg['title']}", "", "[← сводка](README.md)", "",
               "| № | Дата | Статья | Русская | English |", "|---|---|---|---|---|"]
        for n, e in rows:
            ru = f"[открыть]({SITE}{e['ru']})" if e.get("ru") else "—"
            en = f"[open]({SITE}{e['en']})" if e.get("en") else "—"
            sec.append(f"| [{n}]({SITE}/{n}) | {e['date']} | {_md(e.get('title', ''))} | {ru} | {en} |")
        files[ROOT / "shortlinks" / f"{name}.md"] = "\n".join(sec) + "\n"
    files[README] = "\n".join(out) + "\n"
    return files


# ---------------------------------------------------------------- оповещения
def pending_alerts(reg: dict, exhausted: dict[str, int]) -> list[dict]:
    alerts = []
    share = float(reg.get("warn_left_share", 0.1))
    who = reg.get("notify", "")
    for name, cfg in reg["sections"].items():
        if not cfg.get("enabled"):
            continue
        st = section_state(reg, name)
        title = cfg["title"]
        rng = ", ".join(f"{a}–{b}" for a, b in ranges_of(cfg))
        key = rng.replace(", ", "+")
        if st["count"] and not st["left"]:   # выдан последний номер — дошли до конца
            alerts.append({"id": f"exhausted:{name}:{key}",
                           "title": f"Короткие ссылки: в разделе «{title}» номера закончились",
                           "body": f"{who} Номера раздела «{title}» ({rng}) закончились — последний "
                                   f"выданный {st['last']}. Новые статьи раздела остаются без короткой "
                                   f"ссылки (дальше +1 не идёт, чтобы не залезть в номера соседнего "
                                   f"раздела); сейчас таких {exhausted.get(name, 0)}. Чтобы продолжить, "
                                   f"добавьте в `shortlinks/registry.json` → `sections.{name}.ranges` "
                                   f"свободный диапазон, например [[…], [2000, 4999]], — следующий "
                                   f"запуск сам выдаст номера всем, кто ждёт."})
            continue
        if st["count"] and st["left"] <= max(1, math.ceil(st["total"] * share)):
            alerts.append({"id": f"low:{name}:{key}",
                           "title": f"Короткие ссылки: в разделе «{title}» заканчиваются номера",
                           "body": f"{who} В разделе «{title}» ({rng}) осталось {st['left']} номеров "
                                   f"из {st['total']}, последний выданный — {st['last']}. Когда "
                                   f"закончатся, новые статьи раздела останутся без короткой ссылки: "
                                   f"дальше +1 не пойдёт. Чтобы продолжить, добавьте в "
                                   f"`shortlinks/registry.json` → `sections.{name}.ranges` свободный "
                                   f"диапазон."})
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


TEST_ALERT = {
    "title": "Короткие ссылки: проверка оповещений",
    "body": f"{DEFAULT_REGISTRY['notify']} Это пробное сообщение: так придёт весть, когда номера "
            "раздела начнут заканчиваться и когда закончатся совсем. Закройте issue — больше "
            "не появится.",
}


def open_issue(alert: dict) -> None:
    # Такое оповещение уже могло уйти, а запись об этом — не доехать до main
    # (пуш не прошёл): второй раз то же самое не пишем. Пробное — исключение:
    # его заказывают нарочно, и каждый заказ должен дойти.
    if alert is not TEST_ALERT:
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
        notify(TEST_ALERT)
        print("пробное оповещение отправлено")
        return 0

    reg = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() \
        else json.loads(json.dumps(DEFAULT_REGISTRY))
    check_config(reg)
    links: dict[str, dict] = reg["links"]
    legacy = set(reg.get("legacy_folders", []))
    pages = Pages()
    today = dt.date.today().isoformat()

    new, touched, exhausted = [], set(), {}
    for name, cfg in reg["sections"].items():
        if not cfg.get("enabled"):
            continue
        mine = {n: e for n, e in links.items() if e["section"] == name}
        known = {e[k] for e in mine.values() for k in ("ru", "en") if e.get(k)}
        if name in FULL_SECTIONS:
            items = discover_full(name, pages)
        elif name == "news":
            items = discover_news(cfg.get("since"), known, pages)
            # Английская версия новости может выйти позже русской — ждём её
            # две недели, перечитывая только такие русские страницы.
            horizon = (dt.date.fromisoformat(today) - dt.timedelta(days=NEWS_TWIN_DAYS)).isoformat()
            waiting = [e["ru"] for e in mine.values() if e.get("ru") and not e.get("en")
                       and e["date"] >= horizon]
            pages.warm(waiting)
            items += pair_items(waiting, pages)
        else:
            continue
        by_url = {e[k]: n for n, e in mine.items() for k in ("ru", "en") if e.get(k)}
        fresh = []
        for it in items:
            n = by_url.get(it["ru"]) or by_url.get(it["en"])
            if n:
                e = links[n]
                # Двойник появился позже — дописываем; выданный номер не трогаем.
                for k in ("ru", "en"):
                    if it[k] and not e.get(k):
                        e[k] = it[k]
                        touched.add(n)
                continue
            if cfg.get("since") and it["date"] < cfg["since"]:
                continue
            fresh.append(it)
        fresh.sort(key=lambda it: (it["date"], it["stamp"], _natural(it["ru"] or it["en"])))
        last = section_state(reg, name)["last"]
        for i, it in enumerate(fresh):
            n = next_number(cfg, last)
            while n is not None and (ROOT / str(n)).exists() and not _is_ours(n):
                print(f"! {n}: папка уже занята чужим содержимым — номер пропущен", file=sys.stderr)
                last = n
                n = next_number(cfg, last)
            if n is None:
                exhausted[name] = len(fresh) - i   # стоп: дальше +1 не идёт
                break
            links[str(n)] = {"section": name, "date": it["date"], "ru": it["ru"], "en": it["en"]}
            new.append(n)
            touched.add(str(n))
            last = n

    reg["links"] = {k: links[k] for k in sorted(links, key=int)}

    # Страницы. Полные разделы пересобираются всегда; новости — новые, с
    # дописанным двойником и те, чьей страницы ещё нет.
    writes: dict[Path, str] = {}
    for n, e in reg["links"].items():
        cfg = reg["sections"].get(e["section"], {})
        if not cfg.get("enabled"):
            continue
        target = PAGES / f"{n}.html"
        if e["section"] not in FULL_SECTIONS and n not in touched and target.exists():
            continue
        got = {u: pages.get_page(u) for u in (e.get("ru"), e.get("en")) if u}
        got = {u: p for u, p in got.items() if p}
        if not got:
            print(f"! {n}: статьи {e.get('ru') or e.get('en')} больше нет — страницу не трогаем",
                  file=sys.stderr)
            continue
        page = render(int(n), e, got)
        src = got.get(e.get("ru")) or got.get(e.get("en"))
        e["title"] = _clean(src["title"])
        outs = [target] + ([ROOT / n / "index.html"] if e["section"] in legacy else [])
        for t in outs:
            if not t.exists() or t.read_text(encoding="utf-8") != page:
                writes[t] = page

    alerts = pending_alerts(reg, exhausted)
    lists = write_lists(reg)

    print(f"новых номеров: {len(new)}" + (f" ({new[0]}–{new[-1]})" if new else "")
          + f" | дописан двойник: {len(touched) - len(new)} | файлов страниц к записи: {len(writes)}"
          + f" | оповещений: {len(alerts)}")
    for name, waiting in exhausted.items():
        print(f"  ⛔ {reg['sections'][name]['title']}: номера закончились, без ссылки {waiting}")
    for a in alerts:
        print(f"  ⚑ {a['title']}")
    if not args.apply:
        print("сухой прогон — ничего не записано (запись: --apply)")
        return 0

    failed = False
    if args.notify and reg.get("test_alert_request"):
        # Пробное оповещение по запросу из реестра: так его можно заказать
        # обычным коммитом, без ручного запуска. Запрос снимается, только
        # если оповещение ушло, — иначе повторится в следующий раз.
        try:
            notify(TEST_ALERT)
            reg["test_alert_request"] = ""
            print("пробное оповещение отправлено")
        except Exception as exc:
            failed = True
            print(f"! пробное оповещение не ушло: {exc}", file=sys.stderr)
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
    for path, text in lists.items():
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
    print("записано")
    return 1 if failed else 0


def _natural(s: str) -> list:
    """auto_2_9 раньше auto_2_10: числа в адресе сравниваются как числа."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s or "")]


def _is_ours(n: int) -> bool:
    page = ROOT / str(n) / "index.html"
    try:
        return f'<meta name="{MARKER}" content="{n}">' in page.read_text(encoding="utf-8")[:3000]
    except OSError:
        return False


if __name__ == "__main__":
    sys.exit(main())

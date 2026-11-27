#!/usr/bin/env python3
"""Еженедельный дайджест Датаиста: собирает материалы недели и верстает письмо (RU/EN).

Порядок блоков: Топ новостей → Видеожурнал → Авторский канал → реклама ИИ-трансформации →
Исследования → Обучение → реклама Нейрония. Всё идёт одной колонкой, тексты — целыми
абзацами, без обрывов.

Источники:
  * Видеожурнал — RSS канала YouTube (RU: «🤖 Датаист»; для EN канал пока не задан);
  * Авторский канал — публичная лента t.me/s/andre_dataist (RU), обложка поста —
    картинка превью первой ссылки; для EN — англоязычные авторские статьи сайта и ссылка на X;
  * Исследования — papers.json / papers_en.json и описания страниц сайта;
  * Обучение — посты Академии (@dataist_academy, только RU);
  * Топ новостей — новости, отмеченные в digest/top-news.txt (до 7 за неделю); RU и EN версии
    находятся по реестру коротких ссылок, поэтому одной отметки хватает для обоих писем.

На выходе в папке выпуска:
  email.html — письмо для рассылки (таблицы, встроенные стили, без скриптов);
  index.html — веб-версия «Открыть в браузере»: тот же макет, переключатель
               светлой/тёмной темы и плеер YouTube прямо на странице;
  img/       — обложки видео и постов; meta.json — тема письма и состав.

Примеры:
  python3 digest/build.py --lang ru --date 2026-11-27 --outdir digest/2026-11-27/ru \
      --base-url https://dataist.ai/digest/2026-11-27/ru/
  python3 digest/build.py --lang en --fill --inline --preview --outdir /tmp/preview-en
Ключи:
  --fill    если в разделе нет новинок за неделю — показать последние («Если пропустили»)
  --inline  встроить картинки в HTML как data URI — автономный файл для просмотра
  --preview для просмотра: вместо ссылки отписки из Kit — заглушка
"""
import argparse, base64, datetime as dt, html, io, json, re, sys, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import magazine

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://dataist.ai"
ASSETS_URL = f"{SITE}/digest/assets"
ASSETS_DIR = ROOT / "digest" / "assets"
FIRST_ISSUE = dt.date(2026, 11, 27)            # первый выпуск — пятница
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"

YOUTUBE = {"ru": "UCWWDNv21uZDQEi4UhvhNQIA", "en": None}   # channel_id; EN — когда появится канал
TELEGRAM = {"ru": "andre_dataist"}
UTM = "utm_source=dataist&utm_medium={medium}&utm_campaign=digest-{date}"

# ───────────────────────── тексты ─────────────────────────
T = {
    "ru": {
        "brand": "ДАТАИСТ", "issue": "Выпуск № {n}", "kind": "Еженедельный дайджест",
        "hello": "Привет! Это Датаист — всё главное об ИИ за неделю в одном письме: {parts}. Устраивайтесь поудобнее.",
        "parts": {"video": "новые видео", "author": "новые статьи", "video_author": "новые видео и статьи",
                  "research": "свежие исследования из Лаборатории", "edu": "уроки Академии",
                  "news": "топ новостей недели"}, "and": "и",
        "sign": "Андрей Кузьминых", "sign_role": "Основатель Andre AI Technologies",
        "missed": "Если пропустили", "browser": "Открыть в браузере",
        "s_video": "Видеожурнал", "s_author": "Авторский канал", "s_research": "Лаборатория", "s_edu": "Академия",
        "s_news": "Топ новостей", "l_news": "Live ↗", "u_news": "https://t.me/neuronium_ai",
        "all_news": "Все новости →", "u_all_news": "https://dataist.ai/news/",
        "l_video": "Подписаться ↗", "l_author": "Подписаться ↗", "l_research": "Подписаться ↗", "l_edu": "Подписаться ↗",
        "u_video": "https://www.youtube.com/@andre_dataist", "u_author": "https://t.me/+AXsoJ7OiMG4zMzFi",
        "u_research": "https://t.me/+gjvJGFW0iXUwMjky", "u_edu": "https://t.me/dataist_academy",
        "watch": "▶ Смотреть видео",
        "open_post": "Открыть пост ↗", "read": "Читать разбор →", "read_article": "Читать статью →",
        "lesson": "Открыть урок →",
        "ait_kicker": "Andre AI Technologies", "ait_title": "ИИ-трансформация вашего бизнеса",
        "ait_text": "Бесплатная диагностика ИИ-зрелости, ИИ-стратегия, ИИ-операционная система «Нейроний» "
                    "и 3 месяца обучения команды с ментором.",
        "ait_stats": [("30+", "компаний"), ("$100+ млн", "эффекта"), ("10+ лет", "в ИИ")],
        "ait_cta": "Бесплатная ИИ-диагностика →", "ait_url": "https://andre.technology/?lang=ru",
        "ait_media": "ait-explainer-ru", "nr_media": "neuronium-explainer-ru",
        "nr_kicker": "Нейроний · ИИ-операционная система", "nr_title": "Ведите ИИ-бизнес в ИИ-операционной системе",
        "nr_text": "Единый контекст бизнеса, ИИ-суперагент и 100 готовых ИИ-сотрудников в десяти отделах — "
                   "от целей и задач до продаж, поддержки и кода.",
        "nr_cta": "Попробовать бесплатно →", "nr_url": "https://neuronium.ai/",
        "socials": [("YouTube", "https://www.youtube.com/@andre_dataist"), ("Telegram", "https://t.me/+AXsoJ7OiMG4zMzFi"),
                    ("Instagram", "https://www.instagram.com/andre_dataist"), ("TikTok", "https://www.tiktok.com/@andre_dataist")],
        "why": "Вы получили это письмо, потому что подписались на рассылку Датаиста на dataist.ai.",
        "unsub": "Отписаться", "made": "Создано в", "made_name": "Нейроний",
        "to_dark": "Тёмная тема", "to_light": "Светлая тема",
        "months": ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"],
        "mon": ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"],
        "wd": ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"],
        "subject": "Датаист № {n}: {lead}",
    },
    "en": {
        "brand": "DATAIST", "issue": "Issue No. {n}", "kind": "Weekly digest",
        "hello": "Hi! This is Dataist — the week’s AI essentials in one letter: {parts}. Get comfortable.",
        "parts": {"video": "new videos", "author": "new articles", "video_author": "new videos and articles",
                  "research": "the freshest AI research", "edu": "new lessons",
                  "news": "the week’s top AI news"}, "and": "and",
        "sign": "Andre Kuzminykh", "sign_role": "Founder of Andre AI Technologies",
        "missed": "In case you missed it", "browser": "View in browser",
        "s_video": "Video Journal", "s_author": "Author’s Channel", "s_research": "Lab", "s_edu": "Academy",
        "s_news": "Top news", "l_news": "", "u_news": "",   # в X у Нейрония аккаунта нет
        "all_news": "", "u_all_news": "",                    # английской ленты новостей на сайте пока нет
        "l_video": "Subscribe ↗", "l_author": "Follow ↗", "l_research": "All research ↗", "l_edu": "Academy ↗",
        "u_video": "https://www.youtube.com/@andre.dataist", "u_author": "https://x.com/andre_dataist",
        "u_research": "https://dataist.ai/", "u_edu": "https://dataist.ai/",
        "watch": "▶ Watch the video",
        "open_post": "Open the post ↗", "read": "Read the breakdown →", "read_article": "Read the article →",
        "lesson": "Open the lesson →",
        "ait_kicker": "Andre AI Technologies", "ait_title": "AI transformation of your business",
        "ait_text": "Free AI maturity diagnostic, AI strategy, the Neuronium AI Business OS "
                    "and 3 months of team training with a mentor.",
        "ait_stats": [("30+", "companies"), ("$100M+", "impact"), ("10+ yrs", "in AI")],
        "ait_cta": "Free AI assessment →", "ait_url": "https://andre.technology/?lang=en",
        "ait_media": "ait-explainer-en", "nr_media": "neuronium-explainer-en",
        "nr_kicker": "Neuronium · AI Operating System", "nr_title": "Run AI Business with AI Operating System",
        "nr_text": "One shared business context, one AI Superagent and 100 ready AI employees — "
                   "from goals and tasks to sales, support and code.",
        "nr_cta": "Start free trial →", "nr_url": "https://neuronium.ai/",
        "socials": [("YouTube", "https://www.youtube.com/@andre.dataist"), ("X", "https://x.com/andre_dataist"),
                    ("LinkedIn", "https://www.linkedin.com/in/andre-kuzminykh/"),
                    ("Instagram", "https://www.instagram.com/andre.dataist"), ("TikTok", "https://www.tiktok.com/@andre.dataist")],
        "why": "You are receiving this because you subscribed to the Dataist newsletter on dataist.ai.",
        "unsub": "Unsubscribe", "made": "Made in", "made_name": "Neuronium",
        "to_dark": "Dark theme", "to_light": "Light theme",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "mon": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "wd": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "subject": "Dataist No. {n}: {lead}",
    },
}

# ───────────────────────── утилиты ─────────────────────────
def fetch(url, binary=False, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ru,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def esc(s):
    return html.escape(str(s), quote=True)


def esc_nobr(s):
    """Как esc, но «ИИ-операционной», «AI-ready» и т. п. не рвутся по дефису в конце строки."""
    return re.sub(r"(?<![\w-])((?:ИИ|AI)-[\w-]+)", r'<span style="white-space:nowrap">\1</span>', esc(s))


def plural(n, forms):
    one, few, many = forms
    n = abs(n) % 100
    if 11 <= n <= 19:
        return many
    n %= 10
    return one if n == 1 else few if 2 <= n <= 4 else many


def fmt_date(d, lang, short=False):
    t = T[lang]
    if short:
        return f"{d.day} {t['mon'][d.month - 1]}" if lang == "ru" else f"{t['mon'][d.month - 1]} {d.day}"
    return f"{d.day} {t['months'][d.month - 1]} {d.year}" if lang == "ru" else f"{t['months'][d.month - 1]} {d.day}, {d.year}"


def fmt_range(a, b, lang):
    """Неделя выпуска: «21–27 ноября 2026» / «November 21–27, 2026»."""
    m = T[lang]["months"]
    if lang == "ru":
        if a.month == b.month:
            return f"{a.day}–{b.day} {m[b.month - 1]} {b.year}"
        return f"{a.day} {m[a.month - 1]} – {fmt_date(b, lang)}"
    if a.month == b.month:
        return f"{m[b.month - 1]} {a.day}–{b.day}, {b.year}"
    return f"{m[a.month - 1]} {a.day} – {fmt_date(b, lang)}"


def parse_date(s):
    return dt.date.fromisoformat(str(s)[:10])


def squash(s):
    return re.sub(r"\s+", " ", s or "").strip()


SENT_END = re.compile(r"(?<=[.!?…])\s+(?=[«\"(A-ZА-ЯЁ0-9])")


def by_sentences(text, limit):
    """Целые предложения, пока влезает в limit (минимум одно)."""
    out, total = [], 0
    for s in SENT_END.split(text):
        if out and total + len(s) > limit:
            break
        out.append(s)
        total += len(s) + 1
    return " ".join(out)


LIST_ITEM = re.compile(r"^(\d{1,2}[.)]|[-•–—▪●])\s")


def excerpt(paras, target=420, hard=680):
    """Целые абзацы без обрывов: набираем, пока не наберётся target; длинный абзац — по предложениям.
    Перед списком останавливаемся, а вводную фразу списка («…:») без самого списка не берём."""
    out, total = [], 0
    for p in paras:
        if out and (total >= target or total + len(p) > hard or LIST_ITEM.match(p)):
            break
        if len(p) > hard:
            p = by_sentences(p, hard)
        out.append(p)
        total += len(p)
    while len(out) > 1 and out[-1].rstrip().endswith(":"):
        out.pop()
    return out


def meta_tag(rel_dir, name):
    p = ROOT / rel_dir / "index.html"
    if not p.exists():
        return ""
    attr = "property" if name.startswith("og:") else "name"
    m = re.search(r'<meta %s="%s" content="([^"]*)"' % (attr, re.escape(name)), p.read_text("utf-8", "replace"))
    return html.unescape(m.group(1)) if m else ""


def strip_prefix(teaser, title):
    """«WeVisForensics: …» — убрать название модели, если оно уже есть в заголовке."""
    m = re.match(r"^([^:]{2,40}):\s+(.*)$", teaser)
    if m and title.startswith(m.group(1)):
        return m.group(2)
    return teaser


PER_SECTION = 7          # материалов в каждом разделе выпуска
FULL_CARDS = 3           # в письме: столько — карточками с текстом, остальные — строками (иначе Gmail обрежет письмо)


def pick(items, start, end, want=PER_SECTION, fill=False):
    """Новинки окна [start, end]; при fill (превью) — добираем до want последними материалами.
    Возвращает (материалы, нет_ли_новинок)."""
    new = [x for x in items if start <= x["date"] <= end]
    if not fill:
        return new[:want], False
    return (new + [x for x in items if x not in new])[:want], not new


# ───────────────────────── источники ─────────────────────────
def clean_description(desc):
    lines = []
    for line in (desc or "").split("\n"):
        l = line.strip()
        if not l:
            lines.append("")
            continue
        if re.search(r"https?://|www\.", l) or re.match(r"^\d{1,2}:\d{2}", l) or re.fullmatch(r"(#\S+\s*)+", l):
            continue
        lines.append(re.sub(r"\s#\S+", "", l))
    return [squash(p) for p in re.split(r"\n\s*\n", "\n".join(lines)) if squash(p)]


CTA_LINE = re.compile(r"^(👉|👇|🔗|📌|➡|⬇)|ссылк|подпис|шапке профиля|link in bio|subscribe|t\.me/|instagram|tiktok", re.I)


def video_text(paras, limit=420):
    """Описание видео одним абзацем: без призывов и ссылок, только целые предложения."""
    text = " ".join(p for p in paras if not CTA_LINE.search(p))
    return [by_sentences(squash(text), limit)] if text else []


def youtube(lang):
    cid = YOUTUBE.get(lang)
    if not cid:
        return []
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
          "m": "http://search.yahoo.com/mrss/"}
    root = ET.fromstring(fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"))
    out = []
    for e in root.findall("a:entry", ns):
        vid = e.find("yt:videoId", ns).text
        stats = e.find("m:group/m:community/m:statistics", ns)
        desc = e.find("m:group/m:description", ns)
        out.append({"id": vid, "title": e.find("a:title", ns).text or "",
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "date": parse_date(e.find("a:published", ns).text),
                    "views": int(stats.get("views")) if stats is not None and stats.get("views") else None,
                    "paras": clean_description(desc.text if desc is not None else "")})
    return out


POST_CTA = re.compile(r"^(📜|📄|📖|👉|👇|🔗|📌|➡|⬇)|^(#\S+\s*)+$", re.I)
POST_CTA_SHORT = re.compile(r"стать|читат|подробн|ссылк|полност|full article|read more", re.I)


def clean_post(paras):
    return [p for p in paras if not POST_CTA.search(p) and not (len(p) < 70 and POST_CTA_SHORT.search(p))]


def first_site_link(post, prefix=""):
    for link in post.get("links", []):
        if link.startswith(f"{SITE}/{prefix}"):
            return link
    return None


def telegram(channel):
    page = fetch(f"https://t.me/s/{channel}")
    posts = []
    for b in re.split(r'(?=<div class="tgme_widget_message_wrap)', page)[1:]:
        m = re.search(r'data-post="%s/(\d+)"' % re.escape(channel), b)
        tm = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', b, re.S)
        if not m or not tm:
            continue
        links = [html.unescape(u) for u in re.findall(r'<a href="(https?://[^"]+)"', tm.group(1))]
        text = html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<br\s*/?>", "\n", tm.group(1)))).strip()
        lines = text.split("\n")
        ti = next((i for i, l in enumerate(lines) if l.strip()), None)
        if ti is None:
            continue
        title = squash(lines[ti])
        rest = "\n".join(lines[ti + 1:])
        paras = [squash(p) for p in re.split(r"\n\s*\n", rest) if squash(p)]
        if len(paras) <= 1:
            paras = [squash(p) for p in rest.split("\n") if squash(p)]
        prev = re.search(r"link_preview_(?:right_)?image[^>]*background-image:url\('([^']+)'\)", b)
        photo = re.search(r"tgme_widget_message_photo_wrap[^>]*background-image:url\('([^']+)'\)", b)
        when = re.search(r'<time[^>]+datetime="([^"]+)"', b)
        posts.append({"id": m.group(1), "title": title, "paras": paras, "links": links,
                      "preview_img": prev.group(1) if prev else (photo.group(1) if photo else None),
                      "url": f"https://t.me/{channel}/{m.group(1)}",
                      "date": parse_date(when.group(1)) if when else None})
    posts = [p for p in posts if p["date"]]
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def research(lang):
    data = json.loads((ROOT / ("papers.json" if lang == "ru" else "papers_en.json")).read_text("utf-8"))
    out = []
    for x in data:
        if not x.get("slug", "").startswith("research/"):
            continue
        ru_dir = x["cover"].replace(SITE + "/", "").rsplit("/", 1)[0]
        cover = f"{SITE}/{ru_dir}/cover_card.jpg" if (ROOT / ru_dir / "cover_card.jpg").exists() else x["cover"]
        out.append({"title": x["title"], "url": x["url"], "date": parse_date(x["date"]), "cover": cover,
                    "text": strip_prefix(meta_tag(x["slug"], "description"), x["title"])})
    return sorted(out, key=lambda x: x["date"], reverse=True)


TOP_NEWS_FILE = ROOT / "digest" / "top-news.txt"
TOP_NEWS_LIMIT = 7


def _news_catalog():
    """Все новости по номерам коротких ссылок: дата, пути RU/EN, русский заголовок и обложка."""
    reg = json.loads((ROOT / "shortlinks/registry.json").read_text("utf-8"))["links"]
    index = json.loads((ROOT / "news/index.json").read_text("utf-8"))
    by_ru = {"/" + x["url"].replace(SITE + "/", "").strip("/") + "/": x for x in index}
    cat = {}
    for num, v in reg.items():
        if v.get("section") != "news" or not v.get("date"):
            continue
        ru = by_ru.get(v.get("ru") or "")
        cat[num] = {"num": num, "date": parse_date(v["date"]), "ru": v.get("ru"), "en": v.get("en"),
                    "ru_title": squash(ru["title"] if ru else v.get("title", "")),
                    "ru_cover": ru["cover"] if ru else None}
    return cat


def _news_item(e, lang):
    """Новость на языке письма: заголовок, адрес, обложка."""
    if lang == "ru":
        if not e["ru"]:
            return None
        title, url, cover = e["ru_title"], SITE + e["ru"], e["ru_cover"]
    else:
        if not e["en"]:
            return None
        rel = e["en"].strip("/")
        title = squash(meta_tag(rel, "og:title"))
        if not title:
            return None
        url, cover = f"{SITE}/{rel}/", meta_tag(rel, "og:image") or e["ru_cover"]
    if cover and cover.startswith("/"):
        cover = SITE + cover
    return {"num": e["num"], "date": e["date"], "title": title, "url": url, "cover": cover}


def read_top_marks():
    """Строки digest/top-news.txt без комментариев: номера коротких ссылок или адреса новостей."""
    if not TOP_NEWS_FILE.exists():
        return []
    return [l.split("#", 1)[0].strip() for l in TOP_NEWS_FILE.read_text("utf-8").splitlines()
            if l.split("#", 1)[0].strip()]


def top_news(lang, start, end, limit=TOP_NEWS_LIMIT):
    """Топ новостей недели: отмеченные в digest/top-news.txt, в порядке строк (максимум limit).
    Если за неделю ничего не отмечено — по одной новости с обложкой за каждый день, от последнего.
    Возвращает (новости, отмечены_ли_вручную)."""
    cat = _news_catalog()
    by_path = {p: num for num, e in cat.items() for p in (e["ru"], e["en"]) if p}
    picked, seen = [], set()
    for token in read_top_marks():
        m = re.search(r"(?:^|dataist\.ai/)(\d{3,6})/?$", token)
        num = m.group(1) if m else None
        if not num:
            pm = re.search(r"(/news/[^/?#\s]+)", token)
            num = by_path.get(pm.group(1) + "/") if pm else None
        e = cat.get(num) if num else None
        if not e or num in seen or not (start <= e["date"] <= end):
            continue
        item = _news_item(e, lang)
        if item:
            picked.append(item)
            seen.add(num)
        if len(picked) >= limit:
            break
    if picked:
        return picked, True
    days = {}
    for num, e in sorted(cat.items(), key=lambda kv: int(kv[0]), reverse=True):
        if start <= e["date"] <= end:
            item = _news_item(e, lang)
            if item and item["cover"]:
                days.setdefault(e["date"], []).append(item)
    order, out = sorted(days, reverse=True), []
    while len(out) < limit and any(days[d] for d in order):
        for d in order:
            if days[d] and len(out) < limit:
                out.append(days[d].pop(0))
    return out, False


def author_en():
    data = json.loads((ROOT / "technology/en/index.json").read_text("utf-8"))
    out = [{"title": x["title"], "url": x["url"], "date": parse_date(x["date"]), "cover": x.get("cover", ""),
            "text": squash(x.get("teaser", ""))} for x in data]
    return sorted(out, key=lambda x: x["date"], reverse=True)


# ───────────────────────── картинки ─────────────────────────
def _image_bytes(src):
    """Картинка по URL; адреса dataist.ai берём из локальной копии сайта."""
    if src.startswith(SITE + "/"):
        p = ROOT / src[len(SITE) + 1:]
        if p.exists():
            return p.read_bytes()
    return fetch(src, binary=True)


def save_cover(src, out_path, ratio=16 / 9, width=1120):
    """Обложка поста: обрезка по центру до 16:9, ширина 1120 (2× для ретины)."""
    from PIL import Image
    try:
        im = Image.open(io.BytesIO(_image_bytes(src))).convert("RGB")
    except Exception as e:
        print("cover:", src[:80], e, file=sys.stderr)
        return False
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / ratio)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((width, int(width / ratio)), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=84, optimize=True, progressive=True)
    return True


def post_cover_source(post):
    """Обложка поста — картинка превью его первой ссылки. Если ссылка ведёт на dataist.ai,
    берём ту же картинку из копии сайта (лучше качество, без CDN Telegram)."""
    links = post.get("links", [])
    if links and links[0].startswith(SITE + "/"):
        rel = links[0][len(SITE) + 1:].split("?")[0].split("#")[0].strip("/")
        card_img = ROOT / rel / "cover_card.jpg"
        if card_img.exists():
            return f"{SITE}/{rel}/cover_card.jpg"
        og = meta_tag(rel, "og:image")
        if og:
            return og
    if post.get("preview_img"):
        return post["preview_img"]
    for link in links:
        if link.startswith(SITE + "/"):
            og = meta_tag(link[len(SITE) + 1:].split("?")[0].strip("/"), "og:image")
            if og:
                return og
    return None


def youtube_thumb(vid, out_path, play=True):
    """Обложка видео 16:9, 1120×630; play — кнопка ▶ в левом нижнем углу (не закрывает надписи)."""
    from PIL import Image, ImageDraw
    im = None
    for name in ("maxresdefault", "sddefault", "hqdefault"):
        try:
            im = Image.open(io.BytesIO(fetch(f"https://i.ytimg.com/vi/{vid}/{name}.jpg", binary=True))).convert("RGB")
            if im.width >= 400:
                break
        except Exception:
            im = None
    if im is None:
        return False
    w, h = im.size
    th = int(w * 9 / 16)
    if th < h:                                   # убрать чёрные полосы у 4:3
        top = (h - th) // 2
        im = im.crop((0, top, w, top + th))
    im = im.resize((1120, 630), Image.LANCZOS)
    if not play:
        im.save(out_path, "JPEG", quality=84, optimize=True, progressive=True)
        return True
    k = 4
    layer = Image.new("RGBA", (1120 * k, 630 * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r, s = 58 * k, 21 * k
    cx, cy = 36 * k + r, (630 - 36) * k - r
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 240))
    d.polygon([(cx - s * 0.7, cy - s), (cx - s * 0.7, cy + s), (cx + s * 1.05, cy)], fill=(10, 10, 10, 255))
    base = im.convert("RGBA")
    base.alpha_composite(layer.resize((1120, 630), Image.LANCZOS))
    base.convert("RGB").save(out_path, "JPEG", quality=84, optimize=True, progressive=True)
    return True


# ───────────────────────── вёрстка ─────────────────────────
SANS = "'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "'Space Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono','Courier New',monospace"
INK, TEXT, BODY, MUTED, DIM, LINE = "#0a0a0a", "#1d1d1f", "#3a3a3c", "#6e6e73", "#a1a1a6", "#e5e5ea"


def mono(size=11, color=INK, weight=700, ls=".18em", extra=""):
    return (f"font-family:{MONO};font-size:{size}px;line-height:1.5;font-weight:{weight};"
            f"letter-spacing:{ls};text-transform:uppercase;color:{color};{extra}")


def sans(size=15, color=TEXT, weight=400, lh=1.6, ls="0", extra=""):
    return (f"font-family:{SANS};font-size:{size}px;line-height:{lh};font-weight:{weight};"
            f"letter-spacing:{ls};color:{color};{extra}")


def link_cta(url, label, color=INK):
    return (f'<a href="{esc(url)}" style="{mono(12, color, 700, ".12em")}text-decoration:none;'
            f'border-bottom:1px solid {color};padding-bottom:2px">{esc(label)}</a>')


def pill(url, label, bg="#ffffff", fg="#000000"):
    return (f'<a href="{esc(url)}" style="display:inline-block;background:{bg};color:{fg};{sans(14, fg, 700, 1)}'
            f'text-decoration:none;padding:14px 24px;border-radius:999px">{esc(label)}</a>')


def row(inner, pad="0 40px"):
    return f'<tr><td class="px" style="padding:{pad}">{inner}</td></tr>'


def section_header(num, title, label, url, missed=None):
    note = (f'<tr><td colspan="2" style="padding-top:6px;{mono(10, DIM, 700, ".16em")}">{esc(missed)}</td></tr>'
            if missed else "")
    return row(f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr><td style="border-top:2px solid {INK};padding-top:12px;{mono(11, INK, 700, '.2em')}">{num} — {esc(title)}</td>
<td align="right" style="border-top:2px solid {INK};padding-top:12px;{mono(11, INK, 700, '.14em')}">{f'<a href="{esc(url)}" style="color:{INK};text-decoration:none">{esc(label)}</a>' if label and url else ''}</td></tr>{note}
</table>''', "56px 40px 0")


def card(url, meta, title, paras, cta, img=None, first=False):
    """Карточка во всю ширину: обложка, дата, заголовок, текст целиком, ссылка."""
    divider = "" if first else row(f'<div style="border-top:1px solid {LINE};height:1px;line-height:1px;font-size:0">&nbsp;</div>', "34px 40px 0")
    if img:
        media = (f'<a href="{esc(url)}" style="text-decoration:none"><img src="{esc(img)}" width="560" alt="{esc(title)}" '
                 f'style="display:block;width:100%;max-width:560px;height:auto;border:0;border-radius:16px"></a>')
    else:
        media = ""
    text = "".join(f'<p style="margin:{10 if i == 0 else 12}px 0 0;{sans(15, BODY)}">{esc(p)}</p>' for i, p in enumerate(paras))
    return divider + row(f'''{media}
{f'<div style="padding-top:{18 if media else 0}px;{mono(11, MUTED, 400, ".12em")}">{meta}</div>' if meta else ''}
<h2 class="h1" style="margin:{8 if meta else (18 if media else 0)}px 0 0;{sans(24, INK, 800, 1.2, '-.03em')}"><a href="{esc(url)}" style="color:{INK};text-decoration:none">{esc(title)}</a></h2>
{text}
<p style="margin:16px 0 0">{link_cta(url, cta)}</p>''', f"{20 if first else 34}px 40px 0")


def ad_card(gif, url, kicker, title, text, cta, stats=None, nr_tile=False):
    """Рекламный блок письма: горизонтальный ролик 16:9 (GIF) и подпись под ним."""
    tile = (f'<td valign="middle" style="width:26px;height:26px;border:1px solid #5c5c61;border-radius:6px;text-align:center;'
            f'{sans(13, "#ffffff", 700, 1, "-.05em")}">Nr</td><td class="kick" valign="middle" style="padding-left:10px;{mono(10, "#a1a1a6", 700, ".2em")}">{esc(kicker)}</td>'
            if nr_tile else f'<td class="kick" valign="middle" style="{mono(10, "#a1a1a6", 700, ".2em")}">{esc(kicker)}</td>')
    stats_html = ""
    if stats:
        cells = "".join(
            f'<td class="stat" style="padding-right:24px" valign="top"><div class="stat-n" style="{sans(20, "#ffffff", 800, 1.1, "-.03em")}white-space:nowrap">{esc(a)}</div>'
            f'<div style="padding-top:3px;{mono(10, "#8e8e93", 400, ".1em")}white-space:nowrap">{esc(b)}</div></td>' for a, b in stats)
        stats_html = f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:18px"><tr>{cells}</tr></table>'
    media = f'<img src="{esc(gif)}" width="540" alt="{esc(title)}" style="display:block;width:100%;max-width:540px;height:auto;border:0;border-radius:14px">'
    return row(f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#000000" style="background:#000000;border-radius:22px">
<tr><td style="padding:10px 10px 0">
<a href="{esc(url)}" style="text-decoration:none;display:block">{media}</a></td></tr>
<tr><td class="ad-pad" style="padding:24px 30px 30px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>{tile}</tr></table>
<div class="h1" style="padding-top:14px;{sans(27, '#ffffff', 800, 1.15, '-.03em')}">{esc_nobr(title)}</div>
<p style="margin:12px 0 0;{sans(14, '#c7c7cc', 400, 1.55)}">{esc_nobr(text)}</p>
{stats_html}
<p style="margin:22px 0 0">{pill(url, cta)}</p>
</td></tr></table>''', "56px 40px 0")


def list_rows(entries, pad="26px 40px 0"):
    """Материалы строками (после карточек): обложка 16:9 слева, заголовок справа. entries: (адрес, заголовок, картинка)."""
    rows = []
    for url, title, img in entries:
        thumb = (f'<a href="{esc(url)}" style="text-decoration:none"><img class="tn-thumb" src="{esc(img)}" width="120" height="68" alt="" '
                 f'style="display:block;width:120px;height:68px;border:0;border-radius:10px;object-fit:cover"></a>') if img else ""
        rows.append(f'''<tr>
<td class="tn-img" width="120" valign="middle" style="width:120px;padding:14px 0;border-top:1px solid {LINE}">{thumb}</td>
<td class="tn-txt" valign="middle" style="padding:14px 0 14px 18px;border-top:1px solid {LINE}"><a class="tn-t" href="{esc(url)}" style="{sans(16, INK, 700, 1.35, '-.01em')}text-decoration:none">{esc(title)}</a></td>
</tr>''')
    return row(f'<table role="presentation" class="tn" width="100%" cellpadding="0" cellspacing="0" border="0">{"".join(rows)}</table>', pad)


def top_news_rows(items, imgs, more=None):
    """Топ новостей: строки одна за другой — маленькая картинка слева, заголовок справа;
    more = (подпись, адрес) — ссылка «Все новости» справа под списком."""
    rows = []
    for x in items:
        img = imgs.get(x["num"])
        thumb = (f'<a href="{esc(x["url"])}" style="text-decoration:none"><img class="tn-thumb" src="{esc(img)}" width="120" height="80" alt="" '
                 f'style="display:block;width:120px;height:80px;border:0;border-radius:10px"></a>') if img else ""
        rows.append(f'''<tr>
<td class="tn-img" width="120" valign="middle" style="width:120px;padding:14px 0;border-top:1px solid {LINE}">{thumb}</td>
<td class="tn-txt" valign="middle" style="padding:14px 0 14px 18px;border-top:1px solid {LINE}"><a class="tn-t" href="{esc(x["url"])}" style="{sans(16, INK, 700, 1.35, '-.01em')}text-decoration:none">{esc(x["title"])}</a></td>
</tr>''')
    if more:
        rows.append(f'<tr><td colspan="2" align="right" style="padding:16px 0 0;border-top:1px solid {LINE}">{link_cta(more[1], more[0])}</td></tr>')
    return row(f'<table role="presentation" class="tn" width="100%" cellpadding="0" cellspacing="0" border="0">{"".join(rows)}</table>', "16px 40px 0")


def render(lang, issue, sections, web_url, unsub_url):
    """Письмо. Возвращает (html, тема, прехедер, приветствие)."""
    t = T[lang]
    n = (issue - FIRST_ISSUE).days // 7 + 1
    date_long = f"{t['wd'][issue.weekday()]}, {fmt_date(issue, lang)}"
    keys = [s["key"] for s in sections]
    parts, merged = [], False                  # «новые видео и статьи» — одной фразой на месте первого из двух
    for k in keys:
        if k in ("video", "author"):
            if merged:
                continue
            merged = True
            k = "video_author" if "video" in keys and "author" in keys else k
        parts.append(t["parts"][k])
    parts_txt = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + f" {t['and']} " + parts[-1]
    hello = t["hello"].format(parts=parts_txt)
    preheader = " · ".join(s["count"] for s in sections)
    subject = t["subject"].format(n=n, lead=sections[0]["lead"] if sections else "")

    body = []
    for i, s in enumerate(sections, 1):
        body.append(section_header(f"{i:02d}", s["title"], s["label"], s["url"]))
        body.append(s["html"])
        if s.get("after"):
            body.append(s["after"])

    socials = " &nbsp;·&nbsp; ".join(f'<a href="{esc(u)}" style="color:{INK};text-decoration:none">{esc(name)}</a>'
                                    for name, u in t["socials"])

    left = f'<a href="{esc(web_url)}" style="color:{DIM};text-decoration:none">{esc(t["browser"])}</a>'
    right = ""
    footer_note = (f'<tr><td class="px" align="center" style="padding:26px 40px 0;{sans(12, MUTED, 400, 1.6)}">{esc(t["why"])}<br>'
                   f'<a href="{esc(unsub_url)}" style="color:{MUTED};text-decoration:underline">{esc(t["unsub"])}</a> &nbsp;·&nbsp; '
                   f'<a href="{esc(web_url)}" style="color:{MUTED};text-decoration:underline">{esc(t["browser"])}</a></td></tr>')

    return f'''<!DOCTYPE html>
<html lang="{lang}" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="format-detection" content="telephone=no,date=no,address=no,email=no">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>{esc(subject)}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet">
<style>
  body{{margin:0!important;padding:0!important;background:#ffffff;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}}
  table{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0}}
  img{{-ms-interpolation-mode:bicubic}}
  a{{color:{INK}}}
  @media (max-width:620px){{
    .container{{width:100%!important}}
    .px{{padding-left:20px!important;padding-right:20px!important}}
    .wordmark{{font-size:46px!important}}
    .mark{{width:40px!important;height:40px!important;font-size:17px!important;line-height:40px!important}}
    .h1{{font-size:22px!important}}
    .hide-m{{display:none!important}}
    .hello{{font-size:16px!important}}
    .ad-pad{{padding:22px 20px 26px!important}}
    .stat{{padding-right:14px!important}}
    .stat-n{{font-size:17px!important}}
    .socials{{font-size:10px!important;letter-spacing:.04em!important}}
    .kick{{letter-spacing:.1em!important}}
    .tn-img{{width:96px!important}}
    .tn-thumb{{width:96px!important;height:64px!important}}
    .tn-txt{{padding-left:14px!important}}
    .tn-t{{font-size:14px!important;line-height:1.35!important}}
  }}
</style>
</head>
<body style="margin:0;padding:0;background:#ffffff">
<div id="page">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all">{esc(preheader)}&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="background:#ffffff">
<tr><td align="center" style="padding:0">
<table role="presentation" class="container" width="640" cellpadding="0" cellspacing="0" border="0" style="width:640px;max-width:640px;margin:0 auto">

<tr><td class="px" style="padding:22px 40px 0">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="{mono(10, DIM, 400, '.12em')}">{left}</td>
<td align="right" style="{mono(10, DIM, 400, '.12em')}">{right}</td>
</tr></table></td></tr>

<tr><td class="px" style="padding:18px 40px 0">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="border-top:1px solid {INK};border-bottom:1px solid {INK};padding:8px 0;{mono(10, INK, 700, '.18em')}">{esc(t['issue'].format(n=n))}</td>
<td class="hide-m" align="center" style="border-top:1px solid {INK};border-bottom:1px solid {INK};padding:8px 0;{mono(10, INK, 700, '.18em')}">{esc(t['kind'])}</td>
<td align="right" style="border-top:1px solid {INK};border-bottom:1px solid {INK};padding:8px 0;{mono(10, INK, 700, '.18em')}">{esc(date_long)}</td>
</tr></table></td></tr>

<tr><td class="px" align="center" style="padding:36px 40px 0">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto"><tr>
<td valign="middle"><div class="mark" style="width:54px;height:54px;border-radius:50%;background:{INK};color:#ffffff;text-align:center;font-family:{MONO};font-size:22px;font-weight:700;line-height:54px">i</div></td>
<td valign="middle" class="wordmark" style="padding-left:16px;{sans(72, INK, 800, 1, '-.05em')}">{esc(t['brand'])}</td>
</tr></table></td></tr>
<tr><td class="px" style="padding:30px 40px 0"><div style="border-top:3px solid {INK};height:3px;border-bottom:1px solid {INK};line-height:3px;font-size:0">&nbsp;</div></td></tr>

<tr><td class="px" style="padding:30px 40px 0">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td width="52" valign="top" style="width:52px"><img src="{SITE}/about/andre.jpeg" width="52" height="52" alt="{esc(t['sign'])}" style="display:block;width:52px;height:52px;border-radius:50%;border:0"></td>
<td valign="top" style="padding-left:16px">
<p class="hello" style="margin:0;{sans(17, TEXT, 400, 1.6, '-.005em')}">{esc(hello)}</p>
<p style="margin:12px 0 0;{mono(10, MUTED, 700, '.14em')}">{esc(t['sign'])} · {esc(t['sign_role'])}</p></td>
</tr></table></td></tr>

{''.join(body)}

<tr><td class="px" style="padding:68px 40px 0"><div style="border-top:3px solid {INK};height:3px;border-bottom:1px solid {INK};line-height:3px;font-size:0">&nbsp;</div></td></tr>
<tr><td class="px" align="center" style="padding:28px 40px 0;{sans(26, INK, 800, 1, '-.04em')}">{esc(t['brand'])}</td></tr>
<tr><td class="px socials" align="center" style="padding:16px 40px 0;{mono(11, INK, 700, '.1em')}">{socials}</td></tr>
{footer_note}
<tr><td class="px" align="center" style="padding:24px 40px 48px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto"><tr>
<td valign="middle" style="{sans(12, MUTED, 400, 1)}">{esc(t['made'])}</td>
<td valign="middle" style="padding:0 8px"><div style="width:22px;height:22px;border:1px solid #c7c7cc;border-radius:5px;text-align:center;{sans(11, INK, 700, 1, '-.05em')}line-height:22px">Nr</div></td>
<td valign="middle" style="{sans(12, INK, 700, 1)}">{esc(t['made_name'])}</td></tr></table></td></tr>

</table></td></tr></table>
</div>
</body></html>
''', subject, preheader, hello


# ───────────────────────── сборка ─────────────────────────
def build(lang, issue, outdir, fill=False, inline=False, web_url="#",
          unsub_url="{{ unsubscribe_url }}", base_url=None, embed=True):
    """Собирает выпуск: email.html (письмо), index.html (веб-журнал), meta.json."""
    t = T[lang]
    start, end = issue - dt.timedelta(days=6), issue
    outdir = Path(outdir)
    (outdir / "img").mkdir(parents=True, exist_ok=True)

    def asset(name):
        if inline:
            mime = {".gif": "image/gif", ".mp4": "video/mp4", ".jpg": "image/jpeg"}[Path(name).suffix]
            return f"data:{mime};base64," + base64.b64encode((ASSETS_DIR / name).read_bytes()).decode()
        return f"{ASSETS_URL}/{name}"

    def local_img(path, absolute):
        if inline:
            return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()
        if absolute and base_url:
            return f"{base_url.rstrip('/')}/img/{path.name}"
        return f"img/{path.name}"

    def with_utm(url, medium="email"):
        return url + ("&" if "?" in url else "?") + UTM.format(medium=medium, date=issue.isoformat())

    def ad_web(media, url, kicker, title, text, cta, stats=None):
        """Реклама в журнале: MP4 без звука с обложкой."""
        return {"url": with_utm(url, "web"), "kicker": kicker, "title": title, "text": text, "cta": cta, "stats": stats,
                "mp4": asset(f"{media}.mp4"), "poster": asset(f"{media}.jpg")}

    def attach(sec, html_, front=False):
        sec["after"] = html_ + (sec.get("after") or "") if front else (sec.get("after") or "") + html_

    sections = []   # разделы письма по порядку
    mag = {}        # те же материалы для веб-журнала

    def email_list(parts):
        """Карточки письма (строки HTML) и следующие за ними материалы строками (кортежи)."""
        cards = "".join(p for p in parts if isinstance(p, str))
        extra = [p for p in parts if not isinstance(p, str)]
        return cards + (list_rows(extra) if extra else "")

    def tg_posts(channel):
        try:
            return telegram(channel)
        except Exception as e:
            print(f"telegram {channel}:", e, file=sys.stderr)
            return []

    def tg_cards(posts, cta, link_of, prefix):
        """Посты Telegram: карточки письма + материалы журнала. Обложка — превью первой ссылки, текст — целые абзацы."""
        mail, items = [], []
        for i, p in enumerate(posts):
            path = None
            src = post_cover_source(p)
            if src:
                path = outdir / "img" / f"{prefix}-{p['id']}.jpg"
                if not (path.exists() or save_cover(src, path)):
                    path = None
            url, paras = link_of(p), excerpt(clean_post(p["paras"]))
            img_m = local_img(path, True) if path else None
            mail.append(card(url, "", p["title"], paras, cta, img=img_m, first=i == 0) if i < FULL_CARDS else (url, p["title"], img_m))
            items.append({"title": p["title"], "url": url, "paras": paras, "img": local_img(path, False) if path else None, "cta": cta})
        return email_list(mail), items

    def site_items(xs, cta):
        """Материалы с сайта (EN): обложка по адресу, текст — анонс."""
        mail = email_list([card(x["url"], "", x["title"], [x["text"]], cta, img=x["cover"] or None, first=i == 0) if i < FULL_CARDS
                           else (x["url"], x["title"], x["cover"] or None) for i, x in enumerate(xs)])
        return mail, [{"title": x["title"], "url": x["url"], "paras": [x["text"]] if x["text"] else [], "img": x["cover"] or None,
                       "cta": cta} for x in xs]

    og_img = None

    # 01 — Топ новостей недели (первым разделом): отмеченные в digest/top-news.txt, строки с маленькой картинкой
    tops, marked = top_news(lang, start, end)
    if tops:
        thumbs = {}
        for x in tops:
            path = outdir / "img" / f"news-{x['num']}.jpg"
            if x.get("cover") and (path.exists() or save_cover(x["cover"], path, ratio=3 / 2, width=240)):
                thumbs[x["num"]] = path
        big = outdir / "img" / f"news-{tops[0]['num']}-l.jpg"
        big = big if tops[0].get("cover") and (big.exists() or save_cover(tops[0]["cover"], big, ratio=3 / 2, width=760)) else None
        more = (t["all_news"], with_utm(t["u_all_news"])) if t["u_all_news"] else None
        cnt = len(tops)
        sections.append({"key": "news", "title": t["s_news"], "label": t["l_news"], "url": t["u_news"], "stale": False,
                         "html": top_news_rows(tops, {k: local_img(p, True) for k, p in thumbs.items()}, more),
                         "lead": tops[0]["title"], "marked": marked,
                         "count": (f"{cnt} {plural(cnt, ('новость', 'новости', 'новостей'))}" if lang == "ru"
                                   else f"{cnt} {'story' if cnt == 1 else 'stories'}")})
        mag["news"] = {"items": [{"num": x["num"], "title": x["title"], "url": x["url"],
                                  "img": local_img(thumbs[x["num"]], False) if x["num"] in thumbs else None,
                                  "img_l": local_img(big, False) if (big and i == 0) else None} for i, x in enumerate(tops)],
                       "more": (t["all_news"], with_utm(t["u_all_news"], "web")) if t["u_all_news"] else None}
        og_img = big

    # 02 — Видеожурнал
    try:
        vids = youtube(lang)
    except Exception as e:
        print("youtube:", e, file=sys.stderr)
        vids = []
    items, stale = pick(vids, start, end, fill=fill)
    if items:
        mail, web = [], []
        for i, v in enumerate(items):
            p = outdir / "img" / f"yt-{v['id']}.jpg"
            ok = p.exists() or youtube_thumb(v["id"], p)
            pc = outdir / "img" / f"yt-{v['id']}-c.jpg"
            okc = pc.exists() or youtube_thumb(v["id"], pc, play=False)
            paras = video_text(v["paras"])
            img_m = local_img(p, True) if ok else None
            mail.append(card(v["url"], "", v["title"], paras, t["watch"], img=img_m, first=i == 0) if i < FULL_CARDS
                        else (v["url"], v["title"], img_m))
            web.append({"id": v["id"], "title": v["title"], "url": v["url"], "text": " ".join(paras),
                        "cover": local_img(pc, False) if okc else f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"})
            if i == 0 and okc:
                og_img = pc
        cnt = len(items)
        sections.append({"key": "video", "title": t["s_video"], "label": t["l_video"], "url": t["u_video"], "stale": stale,
                         "html": email_list(mail), "lead": items[0]["title"],
                         "count": f"{cnt} видео" if lang == "ru" else f"{cnt} video{'s' if cnt > 1 else ''}"})
        mag["video"] = web

    # 03 — Авторский канал
    if lang == "ru":
        items, stale = pick(tg_posts(TELEGRAM["ru"]), start, end, fill=fill)
        if items:
            mail, mag["author"] = tg_cards(items, t["open_post"], lambda p: p["url"], "tg")
            cnt = len(items)
            sections.append({"key": "author", "title": t["s_author"], "label": t["l_author"], "url": t["u_author"],
                             "stale": stale, "html": mail, "lead": items[0]["title"],
                             "count": f"{cnt} {plural(cnt, ('пост', 'поста', 'постов'))}"})
    else:
        items, stale = pick(author_en(), start, end, fill=fill)
        if items:
            mail, mag["author"] = site_items(items, t["read_article"])
            cnt = len(items)
            sections.append({"key": "author", "title": t["s_author"], "label": t["l_author"], "url": t["u_author"],
                             "stale": stale, "html": mail, "lead": items[0]["title"],
                             "count": f"{cnt} post{'s' if cnt > 1 else ''}"})

    ait_args = (t["ait_url"], t["ait_kicker"], t["ait_title"], t["ait_text"], t["ait_cta"])
    ait = ad_card(asset(f"{t['ait_media']}.gif"), with_utm(ait_args[0]), *ait_args[1:], stats=t["ait_stats"])
    mag["ait"] = ad_web(t["ait_media"], *ait_args, stats=t["ait_stats"])
    if sections and sections[-1]["key"] == "author":
        attach(sections[-1], ait)
        ait = None

    # 04 — Исследования: RU — посты Лаборатории (@dataist_lab), EN — исследования сайта
    if lang == "ru":
        items, stale = pick(tg_posts("dataist_lab"), start, end, fill=fill)

        def research_link(p):
            return first_site_link(p, "research/") or first_site_link(p) or p["url"]

        if items:
            mail, mag["research"] = tg_cards(items, t["read"], research_link, "lab")
            cnt = len(items)
            sections.append({"key": "research", "title": t["s_research"], "label": t["l_research"], "url": t["u_research"],
                             "stale": stale, "html": mail, "lead": items[0]["title"],
                             "count": f"{cnt} {plural(cnt, ('исследование', 'исследования', 'исследований'))}"})
    else:
        items, stale = pick(research(lang), start, end, fill=fill)
        if items:
            mail, mag["research"] = site_items(items, t["read"])
            cnt = len(items)
            sections.append({"key": "research", "title": t["s_research"], "label": t["l_research"], "url": t["u_research"],
                             "stale": stale, "html": mail, "lead": items[0]["title"],
                             "count": f"{cnt} paper{'s' if cnt > 1 else ''}"})

    # 05 — Обучение: посты Академии (@dataist_academy), только RU
    if lang == "ru":
        items, stale = pick(tg_posts("dataist_academy"), start, end, fill=fill)

        def lesson_link(p):
            return first_site_link(p, "education/") or (p["links"][0] if p["links"] else p["url"])

        if items:
            mail, mag["edu"] = tg_cards(items, t["lesson"], lesson_link, "academy")
            cnt = len(items)
            sections.append({"key": "edu", "title": t["s_edu"], "label": t["l_edu"], "url": t["u_edu"], "stale": stale,
                             "html": mail, "lead": items[0]["title"],
                             "count": f"{cnt} {plural(cnt, ('урок', 'урока', 'уроков'))}"})

    if not sections:
        raise SystemExit("нет материалов для выпуска")
    if ait:                                   # «Авторского канала» нет — реклама после первого раздела за топом новостей
        host = next((x for x in sections if x["key"] != "news"), sections[0])
        attach(host, ait, front=True)
    # Нейроний — сразу после «Обучения» (последнего раздела)
    nr_args = (t["nr_url"], t["nr_kicker"], t["nr_title"], t["nr_text"], t["nr_cta"])
    attach(sections[-1], ad_card(asset(f"{t['nr_media']}.gif"), with_utm(nr_args[0]), *nr_args[1:], nr_tile=True))
    mag["nr"] = ad_web(t["nr_media"], *nr_args)

    email, subject, preheader, hello = render(lang, issue, sections, web_url, unsub_url)
    n = (issue - FIRST_ISSUE).days // 7 + 1
    webpage = magazine.render({
        "lang": lang, "n": n, "brand": t["brand"], "title": subject, "description": hello,
        "hello": hello.replace("в одном письме", "в одном выпуске").replace("in one letter", "in one issue"),
        "sign": t["sign"], "sign_role": t["sign_role"], "avatar": f"{SITE}/about/andre.jpeg", "home": f"{SITE}/",
        "sections": [{k: s.get(k) for k in ("key", "title", "label", "url", "count")} for s in sections],
        "embed": embed, "date_range": fmt_range(start, end, lang), "date_long": fmt_date(issue, lang),
        "date_short": fmt_date(issue, lang, short=True), "socials": t["socials"], "made_name": t["made_name"],
        "to_dark": t["to_dark"], "to_light": t["to_light"],
        "og_image": local_img(og_img, True) if (og_img and base_url and not inline) else None,
        "url": web_url if web_url.startswith("http") else None, **mag})
    (outdir / "email.html").write_text(email, "utf-8")
    (outdir / "index.html").write_text(webpage, "utf-8")
    meta = {"lang": lang, "issue": n, "date": issue.isoformat(), "subject": subject, "preheader": preheader,
            "sections": [{"title": s["title"], "count": s["count"], "stale": s["stale"]} for s in sections],
            "top_news": next(("marked" if s.get("marked") else "auto" for s in sections if s["key"] == "news"), None)}
    (outdir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), "utf-8")
    return outdir, meta


def next_friday(today=None):
    today = today or dt.date.today()
    return today + dt.timedelta(days=(4 - today.weekday()) % 7)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Еженедельный дайджест Датаиста")
    ap.add_argument("--lang", choices=["ru", "en"], required=True)
    ap.add_argument("--date", help="дата выпуска (пятница), по умолчанию ближайшая пятница")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--fill", action="store_true")
    ap.add_argument("--inline", action="store_true")
    ap.add_argument("--preview", action="store_true", help="просмотр: «Отписаться» — заглушка вместо ссылки Kit")
    ap.add_argument("--no-embed", action="store_true", help="в журнале — видео открываются на YouTube (для просмотра файла с диска)")
    ap.add_argument("--web-url", default="#", help="адрес веб-версии для ссылки «Открыть в браузере»")
    ap.add_argument("--base-url", help="абсолютный адрес папки выпуска — для картинок img/ в письме")
    a = ap.parse_args()
    issue = dt.date.fromisoformat(a.date) if a.date else next_friday()
    out, meta = build(a.lang, issue, a.outdir, fill=a.fill, inline=a.inline, web_url=a.web_url,
                      unsub_url="#" if a.preview else "{{ unsubscribe_url }}", base_url=a.base_url, embed=not a.no_embed)
    print(out, json.dumps(meta, ensure_ascii=False))

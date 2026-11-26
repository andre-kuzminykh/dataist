#!/usr/bin/env python3
"""Еженедельный дайджест Датаиста: собирает материалы недели и верстает письмо (RU/EN).

Источники:
  * YouTube — RSS канала (RU: «🤖 Датаист»; для EN канал пока не задан);
  * «Авторский канал» — публичная лента t.me/s/andre_dataist (RU);
    для EN — англоязычные авторские статьи сайта (technology/en) со ссылкой на X;
  * исследования — papers.json / papers_en.json и описания страниц сайта;
  * обучение — education/index.json (только RU).

Письмо — чистый HTML для почтовых клиентов: таблицы, встроенные стили, адаптив.

Примеры:
  python3 digest/build.py --lang ru --date 2026-11-27 --outdir digest/2026-11-27/ru
  python3 digest/build.py --lang en --date 2026-11-27 --fill --inline --outdir /tmp/preview-en
Ключи:
  --fill    если в разделе нет новинок за неделю — показать последние («Если пропустили»)
  --inline  встроить картинки (GIF, обложки видео) в HTML как data URI — автономный файл
  --preview пометка «превью» над письмом
"""
import argparse, base64, datetime as dt, html, io, json, re, sys, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://dataist.ai"
ASSETS = f"{SITE}/digest/assets"
FIRST_ISSUE = dt.date(2026, 11, 27)            # первый выпуск — пятница
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"

YOUTUBE = {"ru": "UCWWDNv21uZDQEi4UhvhNQIA", "en": None}   # channel_id; EN — когда появится канал
TELEGRAM = {"ru": "andre_dataist"}
UTM = "utm_source=dataist&utm_medium=email&utm_campaign=digest-{date}"

# ───────────────────────── тексты ─────────────────────────
T = {
    "ru": {
        "brand": "ДАТАИСТ", "issue": "Выпуск № {n}", "kind": "Еженедельный дайджест",
        "tagline": "ИИ · Исследования · Бизнес — главное за неделю",
        "hello": "Привет! Это пятничный Датаист — всё главное за неделю в одном письме: {parts}. Устраивайтесь поудобнее.",
        "parts": {"video": "новые видео", "author": "мысли из канала", "research": "свежие исследования",
                  "edu": "уроки Академии"}, "and": "и",
        "sign": "Андрей Кузьминых", "sign_role": "Основатель Andre AI Technologies",
        "contents": "В номере", "missed": "Если пропустили",
        "browser": "Открыть в браузере",
        "s_video": "Видеожурнал", "s_author": "Авторский канал", "s_research": "Исследования", "s_edu": "Обучение",
        "l_video": "YouTube ↗", "l_author": "Telegram ↗", "l_research": "Лаборатория ↗", "l_edu": "Академия ↗",
        "u_video": "https://www.youtube.com/@andre_dataist", "u_author": "https://t.me/+AXsoJ7OiMG4zMzFi",
        "u_research": "https://t.me/+gjvJGFW0iXUwMjky", "u_edu": "https://t.me/dataist_academy",
        "watch": "Смотреть видео", "views": "просмотров", "read_tg": "Читать в Telegram", "read": "Читать разбор",
        "read_short": "Читать", "lesson": "Открыть урок", "min": "мин чтения", "module": "Модуль {m} · Урок {l}",
        "ait_kicker": "Andre AI Technologies", "ait_title": "ИИ-трансформация вашего бизнеса",
        "ait_text": "Бесплатная диагностика ИИ-зрелости, ИИ-стратегия, ИИ-операционная система «Нейроний» "
                    "и 3 месяца обучения команды с ментором.",
        "ait_stats": [("30+", "компаний"), ("$100+ млн", "эффекта"), ("10+ лет", "в ИИ")],
        "ait_cta": "Бесплатная ИИ-диагностика →", "ait_video": "▶ Видео · 0:55",
        "nr_kicker": "Нейроний · AI Operating System", "nr_title": "Ведите ИИ-бизнес в ИИ-операционной системе",
        "nr_text": "Единый контекст бизнеса, ИИ-суперагент и 100 готовых ИИ-сотрудников в десяти отделах — "
                   "от целей и задач до продаж, поддержки и кода.",
        "nr_cta": "Открыть AI OS →", "nr_demo": "Смотреть демо",
        "follow": "Датаист в соцсетях",
        "socials": [("YouTube", "https://www.youtube.com/@andre_dataist"), ("Telegram", "https://t.me/+AXsoJ7OiMG4zMzFi"),
                    ("Instagram", "https://www.instagram.com/andre_dataist"), ("TikTok", "https://www.tiktok.com/@andre_dataist")],
        "why": "Вы получили это письмо, потому что подписались на рассылку Датаиста на dataist.ai.",
        "unsub": "Отписаться", "made": "Создано в", "made_name": "Нейроний",
        "preview": "Превью письма · в разделах без новинок за неделю показаны последние материалы",
        "months": ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"],
        "mon": ["янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"],
        "wd": ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"],
        "subject": "Датаист № {n}: {lead}",
    },
    "en": {
        "brand": "DATAIST", "issue": "Issue No. {n}", "kind": "Weekly digest",
        "tagline": "AI · Research · Business — the week in one letter",
        "hello": "Hi! This is the Friday Dataist — the week’s essentials in one letter: {parts}. Get comfortable.",
        "parts": {"video": "new videos", "author": "notes from my channel", "research": "the freshest AI research",
                  "edu": "new lessons"}, "and": "and",
        "sign": "Andre Kuzminykh", "sign_role": "Founder of Andre AI Technologies",
        "contents": "In this issue", "missed": "In case you missed it",
        "browser": "View in browser",
        "s_video": "Video Journal", "s_author": "Author’s Channel", "s_research": "Research", "s_edu": "Learning",
        "l_video": "YouTube ↗", "l_author": "X ↗", "l_research": "Dataist.ai ↗", "l_edu": "Academy ↗",
        "u_video": "https://www.youtube.com/@andre.dataist", "u_author": "https://x.com/andre_dataist",
        "u_research": "https://dataist.ai/", "u_edu": "https://dataist.ai/",
        "watch": "Watch the video", "views": "views", "read_tg": "Read on X", "read": "Read the breakdown",
        "read_short": "Read", "lesson": "Open the lesson", "min": "min read", "module": "Module {m} · Lesson {l}",
        "ait_kicker": "Andre AI Technologies", "ait_title": "AI transformation of your business",
        "ait_text": "Free AI maturity diagnostic, AI strategy, the Neuronium AI Business OS "
                    "and 3 months of team training with a mentor.",
        "ait_stats": [("30+", "companies"), ("$100M+", "impact"), ("10+ yrs", "in AI")],
        "ait_cta": "Free AI assessment →", "ait_video": "▶ Video · 0:55",
        "nr_kicker": "Neuronium · AI Operating System", "nr_title": "Run AI Business with AI Operating System",
        "nr_text": "One shared business context, one AI Superagent and 100 ready AI employees — "
                   "from goals and tasks to sales, support and code.",
        "nr_cta": "Open AI OS →", "nr_demo": "Watch the demo",
        "follow": "Dataist on social",
        "socials": [("YouTube", "https://www.youtube.com/@andre.dataist"), ("X", "https://x.com/andre_dataist"),
                    ("LinkedIn", "https://www.linkedin.com/in/andre-kuzminykh/"),
                    ("Instagram", "https://www.instagram.com/andre.dataist"), ("TikTok", "https://www.tiktok.com/@andre.dataist")],
        "why": "You are receiving this because you subscribed to the Dataist newsletter on dataist.ai.",
        "unsub": "Unsubscribe", "made": "Made in", "made_name": "Neuronium",
        "preview": "Email preview · sections with nothing new this week show the latest items",
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


def clip(text, n):
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0].rstrip(",;:—-–.!? ")
    return cut + "…"


def plural(n, one, few, many):
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


def parse_date(s):
    return dt.date.fromisoformat(str(s)[:10])


def meta_description(rel_dir):
    p = ROOT / rel_dir / "index.html"
    if not p.exists():
        return ""
    m = re.search(r'<meta name="description" content="([^"]*)"', p.read_text("utf-8", "replace"))
    return html.unescape(m.group(1)) if m else ""


def strip_prefix(teaser, title):
    """«WeVisForensics: …» — убрать название модели, если оно уже есть в заголовке."""
    m = re.match(r"^([^:]{2,40}):\s+(.*)$", teaser)
    if m and title.startswith(m.group(1)):
        return m.group(2)
    return teaser


def read_minutes(rel_dir_candidates):
    for rel in rel_dir_candidates:
        p = ROOT / rel / "article_body.txt"
        if p.exists():
            return max(2, round(len(p.read_text("utf-8", "replace").split()) / 200))
    return None


def pick(items, start, end, want, fill):
    """Новинки окна [start, end]; при fill — добрать последними материалами."""
    new = [x for x in items if start <= x["date"] <= end]
    if new or not fill:
        return new[:want], False
    return items[:want], True


# ───────────────────────── источники ─────────────────────────
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
        out.append({
            "id": vid, "title": e.find("a:title", ns).text or "",
            "url": f"https://www.youtube.com/watch?v={vid}",
            "date": parse_date(e.find("a:published", ns).text),
            "views": int(stats.get("views")) if stats is not None and stats.get("views") else None,
            "text": (desc.text or "") if desc is not None else "",
        })
    return out


def telegram(channel):
    page = fetch(f"https://t.me/s/{channel}")
    posts = []
    for b in re.split(r'(?=<div class="tgme_widget_message_wrap)', page)[1:]:
        m = re.search(r'data-post="%s/(\d+)"' % re.escape(channel), b)
        if not m:
            continue
        tm = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', b, re.S)
        if not tm:
            continue
        raw = re.sub(r"<br\s*/?>", "\n", tm.group(1))
        text = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        lines = [l.strip() for l in text.split("\n")]
        title = next((l for l in lines if l), "")
        body = " ".join(l for l in lines[lines.index(title) + 1:] if l) if title else ""
        when = re.search(r'<time[^>]+datetime="([^"]+)"', b)
        posts.append({"id": m.group(1), "title": title, "text": body,
                      "url": f"https://t.me/{channel}/{m.group(1)}",
                      "date": parse_date(when.group(1)) if when else None})
    posts = [p for p in posts if p["date"] and p["title"]]
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
                    "text": strip_prefix(meta_description(x["slug"]), x["title"]),
                    "minutes": read_minutes([x["slug"], ru_dir])})
    return sorted(out, key=lambda x: x["date"], reverse=True)


def education():
    data = json.loads((ROOT / "education/index.json").read_text("utf-8"))
    out = []
    for x in data:
        m = re.match(r"auto_(\d+)_(\d+)$", x["slug"])
        out.append({"title": x["title"], "url": x["url"], "date": parse_date(x["date"]), "cover": x["cover"],
                    "text": x.get("teaser", ""), "module": m.groups() if m else None})
    return sorted(out, key=lambda x: x["date"], reverse=True)


def author_en():
    data = json.loads((ROOT / "technology/en/index.json").read_text("utf-8"))
    out = [{"title": x["title"], "url": x["url"], "date": parse_date(x["date"]), "cover": x.get("cover", ""),
            "text": x.get("teaser", "")} for x in data]
    return sorted(out, key=lambda x: x["date"], reverse=True)


# ───────────────────────── картинки ─────────────────────────
def youtube_thumb(vid, out_path, corner=False):
    """Обложка 16:9 с кнопкой ▶ (2× для ретины): 1120×630; corner — маленькая кнопка в левом нижнем углу."""
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
    k = 4                                        # сглаживание кружка
    layer = Image.new("RGBA", (1120 * k, 630 * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy, r = (560 * k, 315 * k, 62 * k) if not corner else (110 * k, 520 * k, 74 * k)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 240))
    s = (22 if not corner else 26) * k
    d.polygon([(cx - s * 0.7, cy - s), (cx - s * 0.7, cy + s), (cx + s * 1.05, cy)], fill=(10, 10, 10, 255))
    layer = layer.resize((1120, 630), Image.LANCZOS)
    base = im.convert("RGBA")
    base.alpha_composite(layer)
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
            f'text-decoration:none;padding:14px 24px;border-radius:999px;mso-padding-alt:0">{esc(label)}</a>')


def row(inner, pad="0 40px"):
    return f'<tr><td class="px" style="padding:{pad}">{inner}</td></tr>'


def section_header(num, title, label, url, missed=None):
    note = (f'<tr><td colspan="2" style="padding-top:6px;{mono(10, DIM, 700, ".16em")}">{esc(missed)}</td></tr>'
            if missed else "")
    return row(f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
<tr><td style="border-top:2px solid {INK};padding-top:12px;{mono(11, INK, 700, '.2em')}">{num} — {esc(title)}</td>
<td align="right" style="border-top:2px solid {INK};padding-top:12px;{mono(11, INK, 700, '.14em')}"><a href="{esc(url)}" style="color:{INK};text-decoration:none">{esc(label)}</a></td></tr>{note}
</table>''', "52px 40px 0")


def lead_card(img, url, meta, title, text, cta, alt=""):
    img_html = (f'<a href="{esc(url)}" style="text-decoration:none"><img src="{esc(img)}" width="560" alt="{esc(alt or title)}" '
                f'style="display:block;width:100%;max-width:560px;height:auto;border:0;border-radius:16px"></a>') if img else ""
    return row(f'''{img_html}
<div style="padding-top:{18 if img else 0}px;{mono(11, MUTED, 400, '.12em')}">{meta}</div>
<h2 class="h1" style="margin:8px 0 0;{sans(26, INK, 800, 1.18, '-.03em')}"><a href="{esc(url)}" style="color:{INK};text-decoration:none">{esc(title)}</a></h2>
<p style="margin:10px 0 0;{sans(15, BODY)}">{esc(text)}</p>
<p style="margin:16px 0 0">{link_cta(url, cta)}</p>''', "20px 40px 0")


def small_card(img, url, meta, title, width=270, radius=12):
    img_html = (f'<a href="{esc(url)}" style="text-decoration:none"><img src="{esc(img)}" width="{width}" alt="{esc(title)}" '
                f'class="img-full" style="display:block;width:100%;max-width:{width}px;height:auto;border:0;border-radius:{radius}px"></a>') if img else ""
    return f'''{img_html}
<div style="padding-top:12px;{mono(10, MUTED, 400, '.12em')}">{meta}</div>
<div style="padding-top:6px;{sans(17, INK, 700, 1.3, '-.015em')}"><a href="{esc(url)}" style="color:{INK};text-decoration:none">{esc(title)}</a></div>'''


def grid(cards):
    """Пары карточек в две колонки; на телефоне — в столбик."""
    out = []
    for i in range(0, len(cards), 2):
        pair = cards[i:i + 2]
        if len(pair) == 1:
            out.append(row(pair[0], "28px 40px 0"))
            continue
        out.append(row(f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td class="stack stack-pad" width="270" valign="top" style="width:270px;padding-right:10px">{pair[0]}</td>
<td class="stack" width="270" valign="top" style="width:270px;padding-left:10px">{pair[1]}</td>
</tr></table>''', "28px 40px 0"))
    return "".join(out)


def side_card(img, url, meta, title, text, cta):
    """Картинка слева, текст справа (уроки)."""
    return row(f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td class="stack stack-pad" width="210" valign="top" style="width:210px">
<a href="{esc(url)}" style="text-decoration:none"><img class="img-full" src="{esc(img)}" width="210" alt="{esc(title)}" style="display:block;width:100%;max-width:210px;height:auto;border:0;border-radius:12px"></a></td>
<td class="stack" valign="top" style="padding-left:22px">
<div style="{mono(10, MUTED, 400, '.12em')}">{meta}</div>
<div style="padding-top:6px;{sans(18, INK, 700, 1.3, '-.015em')}"><a href="{esc(url)}" style="color:{INK};text-decoration:none">{esc(title)}</a></div>
<p style="margin:8px 0 0;{sans(14, BODY, 400, 1.55)}">{esc(text)}</p>
<p style="margin:12px 0 0">{link_cta(url, cta)}</p></td>
</tr></table>''', "26px 40px 0")


def post_block(meta, title, text, url, cta, first=False):
    border = "" if first else f"border-top:1px solid {LINE};"
    size = 24 if first else 19
    return row(f'''<div style="{border}padding-top:{0 if first else 22}px">
<div style="{mono(11, MUTED, 400, '.12em')}">{meta}</div>
<div style="padding-top:8px;{sans(size, INK, 800, 1.22, '-.025em')}"><a href="{esc(url)}" style="color:{INK};text-decoration:none">{esc(title)}</a></div>
<p style="margin:10px 0 0;{sans(15, BODY)}">{esc(text)}</p>
<p style="margin:14px 0 0">{link_cta(url, cta)}</p></div>''', f"{20 if first else 22}px 40px 0")


def ad_ait(t, asset, utm):
    url = f"https://andre.technology/?{utm}"
    stats = "".join(
        f'<td class="stat" style="padding-right:22px" valign="top"><div class="stat-n" style="{sans(20, "#ffffff", 800, 1.1, "-.03em")}white-space:nowrap">{esc(a)}</div>'
        f'<div style="padding-top:3px;{mono(10, "#8e8e93", 400, ".1em")}white-space:nowrap">{esc(b)}</div></td>' for a, b in t["ait_stats"])
    return row(f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#000000" style="background:#000000;border-radius:22px">
<tr><td class="ad-pad" style="padding:30px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td class="stack center-m stack-pad" width="180" valign="middle" style="width:180px">
<a href="{esc(url)}" style="text-decoration:none"><img class="circle" src="{esc(asset('ait-video.gif'))}" width="180" height="180" alt="{esc(t['ait_title'])}" style="display:block;width:180px;height:180px;border:0;border-radius:50%;margin:0 auto"></a>
<div style="padding-top:12px;text-align:center;{mono(10, '#8e8e93', 700, '.16em')}">{esc(t['ait_video'])}</div></td>
<td class="stack center-m" valign="middle" style="padding-left:28px">
<div style="{mono(10, '#a1a1a6', 700, '.2em')}">{esc(t['ait_kicker'])}</div>
<div class="h1" style="padding-top:10px;{sans(27, '#ffffff', 800, 1.15, '-.03em')}">{esc(t['ait_title'])}</div>
<p style="margin:12px 0 0;{sans(14, '#c7c7cc', 400, 1.55)}">{esc(t['ait_text'])}</p>
<table role="presentation" class="center-t" cellpadding="0" cellspacing="0" border="0" style="margin-top:18px"><tr>{stats}</tr></table>
<p style="margin:22px 0 0">{pill(url, t['ait_cta'])}</p></td>
</tr></table></td></tr></table>''', "52px 40px 0")


def ad_neuronium(t, asset, utm):
    url = f"https://neuronium.ai/?{utm}"
    return row(f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#000000" style="background:#000000;border-radius:22px">
<tr><td style="padding:10px 10px 0">
<a href="{esc(url)}" style="text-decoration:none"><img src="{esc(asset('neuronium-demo.gif'))}" width="540" alt="Neuronium — AI Operating System" style="display:block;width:100%;max-width:540px;height:auto;border:0;border-radius:14px"></a></td></tr>
<tr><td class="ad-pad2" style="padding:24px 30px 30px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td valign="middle" style="width:26px;height:26px;border:1px solid #5c5c61;border-radius:6px;text-align:center;{sans(13, '#ffffff', 700, 1, '-.05em')}">Nr</td>
<td valign="middle" style="padding-left:10px;{mono(10, '#a1a1a6', 700, '.2em')}">{esc(t['nr_kicker'])}</td></tr></table>
<div class="h1" style="padding-top:14px;{sans(27, '#ffffff', 800, 1.15, '-.03em')}">{esc(t['nr_title'])}</div>
<p style="margin:12px 0 0;{sans(14, '#c7c7cc', 400, 1.55)}">{esc(t['nr_text'])}</p>
<p style="margin:22px 0 0">{pill(url, t['nr_cta'])}<span style="display:inline-block;width:18px"></span><a href="{esc(url)}" style="{mono(11, '#ffffff', 700, '.14em')}text-decoration:none;border-bottom:1px solid #5c5c61;padding-bottom:2px">{esc(t['nr_demo'])}</a></p>
</td></tr></table>''', "52px 40px 0")


def render(lang, issue, sections, asset, web_url, unsub_url, preview=False):
    t = T[lang]
    n = (issue - FIRST_ISSUE).days // 7 + 1
    date_long = f"{t['wd'][issue.weekday()]}, {fmt_date(issue, lang)}"
    utm = UTM.format(date=issue.isoformat())

    # «В номере»
    toc_cells = []
    for i, s in enumerate(sections, 1):
        toc_cells.append(f'''<td valign="top" style="padding:14px 10px 0 0;border-top:1px solid {LINE}">
<div style="{mono(10, DIM, 700, '.14em')}">{i:02d}</div>
<div style="padding-top:4px;{sans(15, INK, 700, 1.3, '-.01em')}">{esc(s['title'])}</div>
<div style="padding-top:2px;{sans(12, MUTED, 400, 1.4)}">{esc(s['count'])}</div></td>''')
    toc_rows = "".join(f'''<tr><td width="34" style="width:34px;padding:9px 0;border-top:1px solid {LINE};{mono(10, DIM, 700, '.14em')}">{i:02d}</td>
<td style="padding:9px 0;border-top:1px solid {LINE};{sans(15, INK, 700, 1.3, '-.01em')}">{esc(s['title'])}</td>
<td align="right" style="padding:9px 0;border-top:1px solid {LINE};{sans(12, MUTED, 400, 1.3)}">{esc(s['count'])}</td></tr>'''
                       for i, s in enumerate(sections, 1))
    toc = row(f'''<div style="{mono(10, INK, 700, '.2em')}">{esc(t['contents'])}</div>
<table role="presentation" class="toc-d" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top:10px"><tr>{''.join(toc_cells)}</tr></table>
<!--[if !mso]><!--><table role="presentation" class="toc-m" width="100%" cellpadding="0" cellspacing="0" border="0" style="display:none;mso-hide:all;margin-top:10px">{toc_rows}</table><!--<![endif]-->''', "34px 40px 0")

    body = []
    for i, s in enumerate(sections, 1):
        body.append(section_header(f"{i:02d}", s["title"], s["label"], s["url"], t["missed"] if s["stale"] else None))
        body.append(s["html"])
        if s.get("after"):
            body.append(s["after"])

    socials = " &nbsp;·&nbsp; ".join(f'<a href="{esc(u)}" style="color:{INK};text-decoration:none">{esc(name)}</a>'
                                    for name, u in t["socials"])
    preview_bar = (f'<tr><td style="padding:12px 20px;background:#f5f5f7;text-align:center;{mono(10, MUTED, 400, ".12em")}">'
                   f'{esc(t["preview"])}</td></tr>') if preview else ""
    lead = sections[0]["lead"] if sections else ""
    preheader = " · ".join(s["count"] for s in sections)
    parts = [t["parts"][s["key"]] for s in sections]
    parts_txt = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + f" {t['and']} " + parts[-1]
    hello = t["hello"].format(parts=parts_txt)

    return f'''<!DOCTYPE html>
<html lang="{lang}" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<meta name="format-detection" content="telephone=no,date=no,address=no,email=no">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>{esc(t['subject'].format(n=n, lead=lead))}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet">
<style>
  body{{margin:0!important;padding:0!important;background:#ffffff;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}}
  table{{border-collapse:collapse;mso-table-lspace:0;mso-table-rspace:0}}
  img{{-ms-interpolation-mode:bicubic}}
  a{{color:{INK}}}
  :root{{color-scheme:light only;supported-color-schemes:light}}
  @media (max-width:620px){{
    .container{{width:100%!important}}
    .px{{padding-left:20px!important;padding-right:20px!important}}
    .stack{{display:block!important;width:100%!important;max-width:100%!important;padding-left:0!important;padding-right:0!important}}
    .stack-pad{{padding-bottom:18px!important}}
    .toc{{padding:10px 0 10px 0!important}}
    .wordmark{{font-size:46px!important}}
    .mark{{width:40px!important;height:40px!important;font-size:17px!important}}
    .h1{{font-size:23px!important}}
    .hide-m{{display:none!important}}
    .center-m{{text-align:center!important}}
    .center-t{{margin-left:auto!important;margin-right:auto!important}}
    .circle{{width:160px!important;height:160px!important}}
    .img-full{{width:100%!important;max-width:100%!important}}
    .toc-d{{display:none!important}}
    .toc-m{{display:table!important;width:100%!important}}
    .tagline{{font-size:9px!important;letter-spacing:.12em!important}}
    .hello{{font-size:16px!important}}
    .ad-pad{{padding:26px 18px!important}}
    .ad-pad2{{padding:22px 20px 26px!important}}
    .stat{{padding:0 7px!important}}
    .stat-n{{font-size:17px!important}}
  }}
</style>
</head>
<body style="margin:0;padding:0;background:#ffffff">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all">{esc(preheader)}&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;&#8199;&#65279;&#847;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="background:#ffffff">
{preview_bar}
<tr><td align="center" style="padding:0">
<table role="presentation" class="container" width="640" cellpadding="0" cellspacing="0" border="0" style="width:640px;max-width:640px;margin:0 auto">

<tr><td class="px" style="padding:22px 40px 0">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="{mono(10, DIM, 400, '.12em')}"><a href="{esc(web_url)}" style="color:{DIM};text-decoration:none">{esc(t['browser'])}</a></td>
<td align="right" style="{mono(10, DIM, 400, '.12em')}"><a href="{SITE}/" style="color:{DIM};text-decoration:none">dataist.ai</a></td>
</tr></table></td></tr>

<tr><td class="px" style="padding:18px 40px 0">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="border-top:1px solid {INK};border-bottom:1px solid {INK};padding:8px 0;{mono(10, INK, 700, '.18em')}">{esc(t['issue'].format(n=n))}</td>
<td class="hide-m" align="center" style="border-top:1px solid {INK};border-bottom:1px solid {INK};padding:8px 0;{mono(10, INK, 700, '.18em')}">{esc(t['kind'])}</td>
<td align="right" style="border-top:1px solid {INK};border-bottom:1px solid {INK};padding:8px 0;{mono(10, INK, 700, '.18em')}">{esc(date_long)}</td>
</tr></table></td></tr>

<tr><td class="px" align="center" style="padding:34px 40px 0">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto"><tr>
<td valign="middle"><div class="mark" style="width:54px;height:54px;border-radius:50%;background:{INK};color:#ffffff;text-align:center;font-family:{MONO};font-size:22px;font-weight:700;line-height:54px">i</div></td>
<td valign="middle" class="wordmark" style="padding-left:16px;{sans(72, INK, 800, 1, '-.05em')}">{esc(t['brand'])}</td>
</tr></table></td></tr>

<tr><td class="px tagline" align="center" style="padding:18px 40px 0;{mono(10, MUTED, 700, '.22em')}">{esc(t['tagline'])}</td></tr>
<tr><td class="px" style="padding:20px 40px 0"><div style="border-top:3px solid {INK};height:3px;border-bottom:1px solid {INK};line-height:3px;font-size:0">&nbsp;</div></td></tr>

<tr><td class="px" style="padding:30px 40px 0">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td width="52" valign="top" style="width:52px"><img src="{SITE}/about/andre.jpeg" width="52" height="52" alt="{esc(t['sign'])}" style="display:block;width:52px;height:52px;border-radius:50%;border:0"></td>
<td valign="top" style="padding-left:16px">
<p class="hello" style="margin:0;{sans(17, TEXT, 400, 1.6, '-.005em')}">{esc(hello)}</p>
<p style="margin:12px 0 0;{mono(10, MUTED, 700, '.14em')}">{esc(t['sign'])} · {esc(t['sign_role'])}</p></td>
</tr></table></td></tr>

{toc}
{''.join(body)}

<tr><td class="px" style="padding:64px 40px 0"><div style="border-top:3px solid {INK};height:3px;border-bottom:1px solid {INK};line-height:3px;font-size:0">&nbsp;</div></td></tr>
<tr><td class="px" align="center" style="padding:28px 40px 0;{sans(26, INK, 800, 1, '-.04em')}">{esc(t['brand'])}</td></tr>
<tr><td class="px" align="center" style="padding:10px 40px 0;{mono(10, MUTED, 700, '.2em')}">{esc(t['follow'])}</td></tr>
<tr><td class="px" align="center" style="padding:12px 40px 0;{mono(11, INK, 700, '.1em')}">{socials}</td></tr>
<tr><td class="px" align="center" style="padding:26px 40px 0;{sans(12, MUTED, 400, 1.6)}">{esc(t['why'])}<br>
<a href="{esc(unsub_url)}" style="color:{MUTED};text-decoration:underline">{esc(t['unsub'])}</a> &nbsp;·&nbsp; <a href="{esc(web_url)}" style="color:{MUTED};text-decoration:underline">{esc(t['browser'])}</a></td></tr>
<tr><td class="px" align="center" style="padding:22px 40px 48px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto"><tr>
<td valign="middle" style="{sans(12, MUTED, 400, 1)}">{esc(t['made'])}</td>
<td valign="middle" style="padding:0 8px"><div style="width:22px;height:22px;border:1px solid #c7c7cc;border-radius:5px;text-align:center;{sans(11, INK, 700, 1, '-.05em')}line-height:22px">Nr</div></td>
<td valign="middle" style="{sans(12, INK, 700, 1)}">{esc(t['made_name'])}</td></tr></table></td></tr>

</table></td></tr></table>
</body></html>
'''


# ───────────────────────── сборка ─────────────────────────
def build(lang, issue, outdir, fill=False, inline=False, preview=False, web_url="#", unsub_url="{{ unsubscribe_url }}",
          assets_dir=ROOT / "digest/assets", base_url=None):
    t = T[lang]
    end = issue
    start = issue - dt.timedelta(days=6)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "img").mkdir(exist_ok=True)
    utm = UTM.format(date=issue.isoformat())

    def asset(name):
        p = assets_dir / name
        if inline:
            mime = "image/gif" if name.endswith(".gif") else "image/jpeg"
            return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()
        return f"{ASSETS}/{name}"

    def local_img(path):
        if inline:
            return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()
        return f"{base_url.rstrip('/')}/img/{path.name}" if base_url else f"img/{path.name}"

    sections = []

    # 01 — Видеожурнал
    try:
        vids = youtube(lang)
    except Exception as e:
        print("youtube:", e, file=sys.stderr)
        vids = []
    items, stale = pick(vids, start, end, 3, fill)
    if items:
        html_parts = []
        thumbs = {}
        for i, v in enumerate(items):
            p = outdir / "img" / (f"yt-{v['id']}.jpg" if i == 0 else f"yt-{v['id']}-s.jpg")
            if p.exists() or youtube_thumb(v["id"], p, corner=(i > 0)):
                thumbs[v["id"]] = local_img(p)
        lead, rest = items[0], items[1:]
        views = f" · {lead['views']:,} {t['views']}".replace(",", " ") if lead.get("views") else ""
        html_parts.append(lead_card(thumbs.get(lead["id"]), lead["url"], esc(fmt_date(lead["date"], lang, True)) + " · YouTube" + esc(views),
                                    lead["title"], clip(lead["text"], 220), "▶ " + t["watch"]))
        if rest:
            html_parts.append(grid([small_card(thumbs.get(v["id"]), v["url"], esc(fmt_date(v["date"], lang, True)) + " · YouTube", v["title"])
                                    for v in rest]))
        cnt = len(items)
        count = (f"{cnt} {plural(cnt, 'видео', 'видео', 'видео')}" if lang == "ru" else f"{cnt} video{'s' if cnt > 1 else ''}")
        sections.append({"key": "video", "title": t["s_video"], "label": t["l_video"], "url": t["u_video"], "stale": stale,
                         "html": "".join(html_parts), "count": count, "lead": lead["title"]})

    # 02 — Авторский канал
    if lang == "ru":
        try:
            posts = telegram(TELEGRAM["ru"])
        except Exception as e:
            print("telegram:", e, file=sys.stderr)
            posts = []
        items, stale = pick(posts, start, end, 3, fill)
        if items:
            html_parts = [post_block(esc(fmt_date(p["date"], lang, True)) + " · Telegram", p["title"], clip(p["text"], 260),
                                     p["url"], t["read_tg"] + " ↗", first=(i == 0)) for i, p in enumerate(items)]
            cnt = len(items)
            sections.append({"key": "author", "title": t["s_author"], "label": t["l_author"], "url": t["u_author"], "stale": stale,
                             "html": "".join(html_parts), "count": f"{cnt} {plural(cnt, 'пост', 'поста', 'постов')}",
                             "lead": items[0]["title"]})
    else:
        items, stale = pick(author_en(), start, end, 3, fill)
        if items:
            lead, rest = items[0], items[1:]
            html_parts = [lead_card(lead["cover"], lead["url"], esc(fmt_date(lead["date"], lang, True)) + " · Dataist",
                                    lead["title"], clip(lead["text"], 230), t["read_short"] + " →")]
            if rest:
                html_parts.append(grid([small_card(x["cover"], x["url"], esc(fmt_date(x["date"], lang, True)), x["title"]) for x in rest]))
            cnt = len(items)
            sections.append({"key": "author", "title": t["s_author"], "label": t["l_author"], "url": t["u_author"], "stale": stale,
                             "html": "".join(html_parts), "count": f"{cnt} post{'s' if cnt > 1 else ''}", "lead": lead["title"]})
    if sections and sections[-1]["title"] == t["s_author"]:
        sections[-1]["after"] = ad_ait(t, asset, utm)

    # 03 — Исследования
    papers = research(lang)
    new = [x for x in papers if start <= x["date"] <= end]
    items = new[:4] if len(new) >= 3 or not fill else (new + [x for x in papers if x not in new])[:3]
    stale = fill and not new
    if items:
        lead, rest = items[0], items[1:]
        mins = f" · {lead['minutes']} {t['min']}" if lead.get("minutes") else ""
        html_parts = [lead_card(lead["cover"], lead["url"], esc(fmt_date(lead["date"], lang, True)) + esc(mins),
                                lead["title"], clip(lead["text"], 240), t["read"] + " →")]
        if rest:
            html_parts.append(grid([small_card(x["cover"], x["url"],
                                               esc(fmt_date(x["date"], lang, True)) + (f" · {x['minutes']} {t['min']}" if x.get('minutes') else ""),
                                               x["title"]) for x in rest]))
        cnt = len(items)
        count = (f"{cnt} {plural(cnt, 'исследование', 'исследования', 'исследований')}" if lang == "ru"
                 else f"{cnt} paper{'s' if cnt > 1 else ''}")
        sections.append({"key": "research", "title": t["s_research"], "label": t["l_research"], "url": t["u_research"], "stale": stale,
                         "html": "".join(html_parts), "count": count, "lead": lead["title"]})

    # 04 — Обучение (уроки Академии есть только на русском)
    if lang == "ru":
        items, stale = pick(education(), start, end, 2, fill)
        if items:
            html_parts = []
            for x in items:
                meta = esc(t["module"].format(m=x["module"][0], l=x["module"][1])) if x["module"] else esc(fmt_date(x["date"], lang, True))
                html_parts.append(side_card(x["cover"], x["url"], meta, x["title"], clip(x["text"], 170), t["lesson"] + " →"))
            cnt = len(items)
            sections.append({"key": "edu", "title": t["s_edu"], "label": t["l_edu"], "url": t["u_edu"], "stale": stale,
                             "html": "".join(html_parts), "count": f"{cnt} {plural(cnt, 'урок', 'урока', 'уроков')}",
                             "lead": items[0]["title"]})
    if not sections:
        raise SystemExit("нет материалов для выпуска")
    # Нейроний — сразу после «Обучения» (или после последнего раздела, если обучения нет)
    sections[-1]["after"] = (sections[-1].get("after") or "") + ad_neuronium(t, asset, utm)
    # если «Авторского канала» нет — реклама ИИ-трансформации идёт после первого раздела
    if not any("andre.technology" in (s.get("after") or "") for s in sections):
        sections[0]["after"] = ad_ait(t, asset, utm) + (sections[0].get("after") or "")

    page = render(lang, issue, sections, asset, web_url, unsub_url, preview)
    out = outdir / "index.html"
    out.write_text(page, "utf-8")
    n = (issue - FIRST_ISSUE).days // 7 + 1
    meta = {"lang": lang, "issue": n, "date": issue.isoformat(),
            "subject": t["subject"].format(n=n, lead=sections[0]["lead"] if sections else ""),
            "preheader": " · ".join(s["count"] for s in sections),
            "sections": [{"title": s["title"], "count": s["count"], "stale": s["stale"]} for s in sections]}
    (outdir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), "utf-8")
    return out, meta


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
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--web-url", default="#")
    ap.add_argument("--base-url", help="абсолютный адрес папки выпуска для картинок (img/…)")
    a = ap.parse_args()
    issue = dt.date.fromisoformat(a.date) if a.date else next_friday()
    out, meta = build(a.lang, issue, Path(a.outdir), fill=a.fill, inline=a.inline, preview=a.preview,
                      web_url=a.web_url, unsub_url="#" if a.preview else "{{ unsubscribe_url }}", base_url=a.base_url)
    print(out, json.dumps(meta, ensure_ascii=False))

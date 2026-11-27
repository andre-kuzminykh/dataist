"""Веб-версия выпуска Датаиста — цифровой журнал на весь экран.

render(ctx) → HTML-страница. Материалы те же, что в письме; их собирает build.py.
Первый экран: слева — топ новостей, в центре — видеожурнал (плеер прямо на странице), справа — реклама
ИИ-трансформации и содержание выпуска. Ниже у каждого раздела свой облик: колонка автора на тёплой бумаге,
лаборатория на тёмной миллиметровке, академия с карточками уроков; в конце — Нейроний во всю ширину.
"""
import html
import re

MT = {
    "ru": {
        "tagline": "Еженедельный журнал об ИИ", "contents": "В этом выпуске", "letter": "От автора",
        "nav": {"news": "Новости", "video": "Видео", "author": "Канал", "research": "Исследования", "edu": "Обучение"},
        "ticker": "Главное за неделю", "play": "Смотреть видео", "top": "Наверх ↑", "prev": "Назад", "next": "Дальше",
        "skip": "Перейти к содержанию", "made": "Создано в", "issue": "Выпуск № {n}", "issue_short": "№ {n}",
        "lesson": "Урок", "study": "Исследование",
    },
    "en": {
        "tagline": "The weekly AI magazine", "contents": "In this issue", "letter": "From the author",
        "nav": {"news": "News", "video": "Video", "author": "Channel", "research": "Research", "edu": "Learning"},
        "ticker": "This week", "play": "Watch the video", "top": "Back to top ↑", "prev": "Back", "next": "Next",
        "skip": "Skip to content", "made": "Made in", "issue": "Issue No. {n}", "issue_short": "No. {n}",
        "lesson": "Lesson", "study": "Study",
    },
}

SUN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
       '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2'
       'M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>')
MOON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>')
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>'
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
         'aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
FLASK = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
         'aria-hidden="true"><path d="M19 5h10M21 5v13L9.5 37.5A4 4 0 0 0 13 43h22a4 4 0 0 0 3.5-5.5L27 18V5"/>'
         '<path d="M14.5 30h19" opacity=".55"/><circle cx="20" cy="36" r="1.6" fill="currentColor"/><circle cx="27" cy="33" r="1.1" fill="currentColor"/></svg>')
CAP = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
       'aria-hidden="true"><path d="M4 18 24 9l20 9-20 9z"/><path d="M12 22v10c0 3 5.4 6 12 6s12-3 12-6V22"/><path d="M44 18v11"/></svg>')


def esc(s):
    return html.escape(str(s), quote=True)


def nobr(s):
    """«ИИ-операционная» не рвётся по дефису."""
    return re.sub(r"(?<![\w-])((?:ИИ|AI)-[\w-]+)", r'<span class="nb">\1</span>', esc(s))


def ext(url):
    return f'href="{esc(url)}" target="_blank" rel="noopener"'


# ───────────────────────── блоки ─────────────────────────
def media(url, img, alt="", cls="media", ratio="16/9"):
    if not img:
        return ""
    return (f'<a class="{cls}" {ext(url)} style="aspect-ratio:{ratio}" tabindex="-1">'
            f'<img src="{esc(img)}" alt="{esc(alt)}" loading="lazy" decoding="async"></a>')


def paras(ps, cls="p"):
    return "".join(f'<p class="{cls}">{esc(p)}</p>' for p in ps)


def cta(url, label, cls="cta"):
    return f'<a class="{cls}" {ext(url)}>{esc(label)}</a>'


def strip(items, label_prev, label_next):
    """Лента карточек с прокруткой и стрелками (видео, статьи)."""
    return (f'<div class="strip rv"><button class="st-b" type="button" data-d="-1" aria-label="{esc(label_prev)}">{ARROW}</button>'
            f'<ol class="st">{items}</ol>'
            f'<button class="st-b" type="button" data-d="1" aria-label="{esc(label_next)}">{ARROW}</button></div>')


def news_col(title, news):
    """Топ новостей: маленькая картинка слева, заголовок справа."""
    rows = "".join(
        f'''<li class="rv"><a class="nw" {ext(x["url"])} title="{esc(x["title"])}">
{f'<img src="{esc(x["img"])}" alt="" decoding="async">' if x.get("img") else '<span class="nw-ph"></span>'}
<span>{esc(x["title"])}</span></a></li>''' for x in news["items"])
    more = f'<a class="more rv" {ext(news["more"][1])}>{esc(news["more"][0])}</a>' if news.get("more") else ""
    return f'<h2 class="h-news rv"><i class="live" aria-hidden="true"></i>{esc(title)}</h2><ol class="nws">{rows}</ol>{more}'


def video_panel(title, videos, embed, mt):
    """Видеожурнал — тёмный «кинозал»: плеер, название, лента всех видео выпуска."""
    v0 = videos[0]
    inner = f'<img src="{esc(v0["cover"])}" alt="" decoding="async"><span class="pb">{PLAY}</span>'
    stage = (f'<button class="ph" type="button" data-id="{esc(v0["id"])}" aria-label="{esc(mt["play"])}: {esc(v0["title"])}">{inner}</button>'
             if embed else f'<a class="ph" {ext(v0["url"])} aria-label="{esc(mt["play"])}: {esc(v0["title"])}">{inner}</a>')
    items = "".join(
        f'''<li{' class="on"' if i == 0 else ''}><a {ext(v["url"])} data-id="{esc(v["id"])}" data-title="{esc(v["title"])}"
 data-text="{esc(v["text"])}" data-url="{esc(v["url"])}"><span class="st-m"><img src="{esc(v["cover"])}" alt="" loading="lazy" decoding="async">
<span class="st-pb">{PLAY}</span></span><span class="st-t">{esc(v["title"])}</span></a></li>''' for i, v in enumerate(videos))
    return f'''<div class="cinema">
<h2 class="h-cin rv">{esc(title)}</h2>
<div class="player rv" data-embed="{1 if embed else 0}">{stage}</div>
<div class="now rv"><a class="now-t" {ext(v0["url"])}>{esc(v0["title"])}</a><p class="now-p">{esc(v0["text"])}</p></div>
{strip(items, mt["prev"], mt["next"]) if len(videos) > 1 else ''}</div>'''


def lead_panel(title, items, mt):
    """Центр первого экрана без видео: главный материал крупно и лента остальных."""
    a = items[0]
    rest = "".join(f'''<li><a {ext(x["url"])}><span class="st-m">{f'<img src="{esc(x["img"])}" alt="" loading="lazy" decoding="async">' if x.get("img") else ''}</span>
<span class="st-t">{esc(x["title"])}</span></a></li>''' for x in items[1:])
    return f'''<div class="cinema cinema-read">
<h2 class="h-cin rv">{esc(title)}</h2>
<div class="rv">{media(a["url"], a.get("img"), a["title"], "media lp-m")}</div>
<div class="now rv"><a class="now-t" {ext(a["url"])}>{esc(a["title"])}</a>{paras(a["paras"][:1], "now-p")}</div>
{strip(rest, mt["prev"], mt["next"]) if rest else ''}</div>'''


def ad_video(ad, cls):
    return (f'<a class="{cls}" {ext(ad["url"])} tabindex="-1">'
            f'<video class="ad-video" src="{esc(ad["mp4"])}" poster="{esc(ad["poster"])}" muted loop playsinline preload="metadata" '
            f'autoplay aria-label="{esc(ad["title"])}"></video></a>')


def ait_card(ad):
    """Реклама ИИ-трансформации в правой колонке первого экрана."""
    return f'''<aside class="ad rv" aria-label="{esc(ad["kicker"])}">{ad_video(ad, "ad-m")}
<div class="ad-b"><div class="ad-k">{esc(ad["kicker"])}</div><h3 class="ad-t">{nobr(ad["title"])}</h3>
<p class="ad-p">{nobr(ad["text"])}</p><a class="pill" {ext(ad["url"])}>{esc(ad["cta"])}</a></div></aside>'''


def nr_band(ad):
    return f'''<section class="band" aria-label="{esc(ad["kicker"])}"><div class="glow" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="wrap band-in">{ad_video(ad, "band-m rv")}
<div class="band-b rv"><div class="ad-k"><span class="nr">Nr</span>{esc(ad["kicker"])}</div>
<h2 class="band-t">{nobr(ad["title"])}</h2><p class="band-p">{nobr(ad["text"])}</p>
<a class="pill" {ext(ad["url"])}>{esc(ad["cta"])}</a></div></div></section>'''


def author_band(title, items, ctx):
    """Авторский канал — колонка автора: тёплая бумага, заголовки с засечками, главный пост и лента остальных."""
    a, rest = items[0], items[1:]
    side = "".join(f'''<article class="au-i rv">{media(x["url"], x.get("img"), x["title"], "media au-im") or '<span class="au-ph" aria-hidden="true">“</span>'}
<h3 class="au-it"><a {ext(x["url"])}>{esc(x["title"])}</a></h3></article>''' for x in rest)
    return f'''<section class="paper" id="author" data-spy><div class="wrap">
<div class="au-h rv"><img src="{esc(ctx["avatar"])}" alt="" width="64" height="64"><div><h2 class="au-t">{esc(title)}</h2>
<span class="au-by">{esc(ctx["sign"])}</span></div></div>
<div class="au-g"><article class="au-lead rv">{media(a["url"], a.get("img"), a["title"])}
<h3 class="au-lt"><a {ext(a["url"])}>{esc(a["title"])}</a></h3><div class="au-tx">{paras(a["paras"])}</div>{cta(a["url"], a["cta"])}</article>
{f'<div class="au-side">{side}</div>' if side else ''}</div></div></section>'''


def lab_band(title, items, mt):
    """Исследования — лаборатория: тёмная миллиметровка, свечение, карточки с метками углов."""
    a, rest = items[0], items[1:]
    cards = "".join(f'''<article class="lb-c rv"><i class="cb" aria-hidden="true"></i>{media(x["url"], x.get("img"), x["title"])}
<span class="lb-tag">{esc(mt["study"])}</span><h3 class="lb-t"><a {ext(x["url"])}>{esc(x["title"])}</a></h3>
{paras(x["paras"][:1], "lb-p")}{cta(x["url"], x["cta"], "lb-cta")}</article>''' for x in rest)
    return f'''<section class="lab" id="research" data-spy><div class="lab-glow" aria-hidden="true"></div><div class="wrap">
<div class="lb-h rv"><span class="lb-ic">{FLASK}</span><h2 class="lb-ht">{esc(title)}</h2><span class="lb-line" aria-hidden="true"></span></div>
<article class="lb-f rv"><i class="cb" aria-hidden="true"></i>{media(a["url"], a.get("img"), a["title"])}
<div class="lb-fb"><span class="lb-tag">{esc(mt["study"])}</span><h3 class="lb-ft"><a {ext(a["url"])}>{esc(a["title"])}</a></h3>
{paras(a["paras"][:2], "lb-p")}{cta(a["url"], a["cta"], "lb-cta")}</div></article>
{f'<div class="lb-g">{cards}</div>' if cards else ''}</div></section>'''


def academy_band(title, items, mt):
    """Обучение — академия: светлая тетрадь в точку, эмблема, карточки уроков."""
    a, rest = items[0], items[1:]
    cards = "".join(f'''<article class="ac-c rv">{media(x["url"], x.get("img"), x["title"])}
<div class="ac-cb"><span class="ac-tag">{esc(mt["lesson"])}</span><h3 class="ac-t"><a {ext(x["url"])}>{esc(x["title"])}</a></h3>
{paras(x["paras"][:1], "ac-p")}{cta(x["url"], x["cta"], "ac-cta")}</div></article>''' for x in rest)
    return f'''<section class="acad" id="edu" data-spy><div class="wrap">
<div class="ac-h rv"><span class="ac-em">{CAP}</span><h2 class="ac-ht">{esc(title)}</h2></div>
<article class="ac-f rv">{media(a["url"], a.get("img"), a["title"])}
<div class="ac-fb"><span class="ac-tag">{esc(mt["lesson"])}</span><h3 class="ac-ft"><a {ext(a["url"])}>{esc(a["title"])}</a></h3>
{paras(a["paras"][:2], "ac-p")}{cta(a["url"], a["cta"], "ac-btn")}</div></article>
{f'<div class="ac-g">{cards}</div>' if cards else ''}</div></section>'''


# ───────────────────────── оформление ─────────────────────────
CSS = r"""
:root{--bg:#fff;--ink:#0a0a0a;--text:#1d1d1f;--body:#3a3a3c;--muted:#6e6e73;--dim:#a1a1a6;--line:#e5e5ea;--soft:#f5f5f7;
  --hdr:rgba(255,255,255,.82);--ghost:#ededf0;--cin:#0b0b0c;--cinline:transparent;
  --paper:#f5efe4;--paper-ink:#1b1712;--paper-body:#4a4237;--paper-line:#e3d9c8;
  --acad:#eef1f6;--acad-dot:#cfd6e3;--acad-card:#fff;--acad-ink:#101828;--acad-body:#475467;
  --sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  --serif:'Playfair Display',Georgia,'Times New Roman',serif;
  --mono:'Space Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace;
  --gut:clamp(16px,3.2vw,48px);--max:1480px;--ease:cubic-bezier(.2,.8,.2,1);--top:60px}
html[data-theme="dark"]{--bg:#0a0a0b;--ink:#f5f5f7;--text:#ececf0;--body:#c7c7cc;--muted:#8e8e93;--dim:#636366;--line:#2a2a2d;
  --soft:#161618;--hdr:rgba(10,10,11,.8);--ghost:#18181a;--cin:#000;--cinline:#232326;
  --paper:#15120d;--paper-ink:#f3ead9;--paper-body:#c9bda8;--paper-line:#2e271d;
  --acad:#0d111a;--acad-dot:#232b3b;--acad-card:#141a26;--acad-ink:#eef2f8;--acad-body:#a8b3c5;color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:calc(var(--top) + 12px);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:400 16px/1.6 var(--sans);-webkit-font-smoothing:antialiased;
  transition:background-color .5s var(--ease),color .5s var(--ease)}
a{color:inherit;text-decoration:none}
img,video{display:block;max-width:100%}
button{font:inherit;color:inherit}
h1,h2,h3{margin:0}
:focus-visible{outline:2px solid var(--ink);outline-offset:3px;border-radius:4px}
.nb{white-space:nowrap}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--gut)}
.skip{position:absolute;left:-9999px;top:8px;z-index:100;background:var(--ink);color:var(--bg);padding:10px 16px;border-radius:999px;
  font:700 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase}
.skip:focus{left:16px}
.k{font:700 11px/1.3 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}

/* появление при прокрутке */
html.js .rv{opacity:0;transform:translateY(24px);transition:opacity .9s var(--ease) var(--d,0s),transform .9s var(--ease) var(--d,0s)}
html.js .rv.in{opacity:1;transform:none}
.media{display:block;position:relative;overflow:hidden;border-radius:clamp(12px,1.2vw,18px);background:var(--soft)}
.media img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}
.media:hover img,article:hover .media img{transform:scale(1.045)}
html.js .rv .media,html.js .media.rv{clip-path:inset(0 0 100% 0 round 16px);transition:clip-path 1.2s var(--ease) var(--d,0s)}
html.js .rv.in .media,html.js .media.rv.in{clip-path:inset(0 0 0 0 round 0)}
h3 a{background:linear-gradient(currentColor,currentColor) 0 100%/0 2px no-repeat;transition:background-size .5s var(--ease)}
h3 a:hover{background-size:100% 2px}
.pill{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:#fff;color:#000;font:700 15px/1 var(--sans);padding:16px 24px;
  border-radius:999px;transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
.pill:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(160,113,255,.35)}

/* шапка */
.top{position:sticky;top:0;z-index:50;background:var(--hdr);-webkit-backdrop-filter:saturate(180%) blur(16px);backdrop-filter:saturate(180%) blur(16px);
  border-bottom:1px solid transparent;transition:border-color .4s var(--ease),background-color .5s var(--ease)}
.top.scrolled{border-bottom-color:var(--line)}
.top-in{height:var(--top);display:flex;align-items:center;gap:24px}
.brand{display:flex;align-items:center;gap:10px;font:800 19px/1 var(--sans);letter-spacing:-.04em;color:var(--ink);flex:none;
  opacity:0;transform:translateY(-6px);transition:opacity .5s var(--ease),transform .5s var(--ease)}
.top.scrolled .brand,.top:focus-within .brand{opacity:1;transform:none}
.mk{width:28px;height:28px;border-radius:50%;background:var(--ink);color:var(--bg);display:grid;place-items:center;font:700 13px/1 var(--mono)}
.nav{display:flex;gap:4px;margin:0 auto;overflow-x:auto;scrollbar-width:none}
.nav::-webkit-scrollbar{display:none}
.nav a{font:700 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding:10px 12px;border-radius:999px;
  white-space:nowrap;transition:color .25s,background-color .25s}
.nav a:hover{color:var(--ink)}
.nav a.on{color:var(--bg);background:var(--ink)}
.tools{display:flex;align-items:center;gap:14px;flex:none}
.chip{font:700 10px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
#theme{all:unset;cursor:pointer;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;color:var(--muted);transition:color .2s,background-color .2s}
#theme:hover{color:var(--ink);background:var(--soft)}
#theme:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
#theme svg{width:18px;height:18px}
#theme .t-l{display:none}
html[data-theme="dark"] #theme .t-d{display:none}
html[data-theme="dark"] #theme .t-l{display:block}
.prog{position:absolute;left:0;right:0;bottom:-1px;height:2px;pointer-events:none}
.prog i{display:block;height:100%;background:var(--ink);transform-origin:0 50%;transform:scaleX(0)}

/* первый экран */
.mrow{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;padding-top:6px}
.mast{display:flex;font:800 clamp(54px,7.4vw,132px)/.84 var(--sans);letter-spacing:-.055em;color:var(--ink);overflow:hidden;padding-bottom:.06em}
.mast span{display:block}
html.js .mast span{transform:translateY(104%);transition:transform 1.1s var(--ease);transition-delay:calc(var(--i) * 70ms + 80ms)}
html.js.ready .mast span{transform:none}
.mmeta{display:grid;gap:7px;text-align:right;font:700 11px/1.2 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted);padding-bottom:.5em}
.mmeta b{color:var(--ink)}
.rule{height:7px;border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);margin-top:12px;transform-origin:0 50%}
html.js .rule{transform:scaleX(0);transition:transform 1.3s var(--ease) .4s}
html.js.ready .rule{transform:none}
.ticker{display:flex;align-items:center;gap:6px;background:var(--ink);color:var(--bg);margin-top:12px;border-radius:999px;padding:5px 22px 5px 5px;overflow:hidden}
.tk-l{flex:none;display:inline-flex;align-items:center;gap:10px;background:var(--bg);color:var(--ink);border-radius:999px;padding:8px 16px 8px 14px;
  font:700 10px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;white-space:nowrap}
.tk-l .live{width:7px;height:7px}
.tk-l .live::after{inset:-4px}
.tk-in{flex:1;min-width:0;overflow:hidden;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 40px,#000 calc(100% - 40px),transparent);mask-image:linear-gradient(90deg,transparent,#000 40px,#000 calc(100% - 40px),transparent)}
.tk{display:flex;width:max-content;animation:tk 80s linear infinite}
.ticker:hover .tk{animation-play-state:paused}
.tk span{display:flex;align-items:center;gap:18px;padding:6px 18px 6px 0;font:700 11px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;white-space:nowrap}
.tk a:hover{text-decoration:underline;text-underline-offset:3px}
.tk b{color:var(--dim)}
@keyframes tk{to{transform:translateX(-50%)}}
.spread{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,6fr) minmax(0,3fr);gap:clamp(20px,2vw,32px);padding:18px 0 8px}

/* топ новостей */
.h-news{display:flex;align-items:center;gap:10px;font:800 clamp(20px,1.6vw,24px)/1 var(--sans);letter-spacing:-.03em;color:var(--ink);
  border-top:2px solid var(--ink);padding-top:12px}
.live{width:9px;height:9px;border-radius:50%;background:#ff3b30;position:relative;flex:none}
.live::after{content:"";position:absolute;inset:-5px;border-radius:50%;border:1.5px solid #ff3b30;animation:ping 1.8s var(--ease) infinite}
@keyframes ping{from{transform:scale(.6);opacity:1}to{transform:scale(1.6);opacity:0}}
.nws{list-style:none;margin:12px 0 0;padding:0}
.nw{display:grid;grid-template-columns:64px minmax(0,1fr);gap:12px;align-items:center;padding:10px 0;border-top:1px solid var(--line)}
.nws li:first-child .nw{border-top:0}
.nw img,.nw-ph{width:64px;height:46px;object-fit:cover;border-radius:9px;background:var(--soft);transition:transform .5s var(--ease)}
.nw span{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;font:700 14px/1.32 var(--sans);letter-spacing:-.01em;color:var(--ink)}
.nw:hover img{transform:scale(1.07)}
.nw:hover span{text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.more{display:inline-flex;margin-top:12px;font:700 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink);
  padding-bottom:4px;background:linear-gradient(currentColor,currentColor) 0 100%/100% 1px no-repeat;transition:background-size .4s var(--ease)}
.more:hover{background-size:0 1px;background-position:100% 100%}

/* видеожурнал — кинозал */
.cinema{background:var(--cin);color:#fff;border-radius:clamp(18px,1.8vw,26px);padding:clamp(14px,1.3vw,20px);border:1px solid var(--cinline);
  box-shadow:0 30px 70px -30px rgba(0,0,0,.45)}
.h-cin{display:flex;align-items:center;gap:10px;font:800 clamp(20px,1.6vw,24px)/1 var(--sans);letter-spacing:-.03em;padding:4px 4px 14px}
.h-cin::before{content:"";width:8px;height:8px;border-radius:2px;background:#fff;box-shadow:12px 0 0 rgba(255,255,255,.45),24px 0 0 rgba(255,255,255,.2);margin-right:26px}
.player{position:relative;width:min(100%,calc((100vh - 470px) * 16 / 9));min-width:min(100%,420px);margin:0 auto;aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#000}
.player iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.ph{all:unset;cursor:pointer;position:absolute;inset:0;display:block}
.ph img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease),filter .6s}
.ph:hover img{transform:scale(1.03);filter:brightness(.88)}
.pb{position:absolute;left:50%;top:50%;width:clamp(58px,5.6vw,84px);height:clamp(58px,5.6vw,84px);transform:translate(-50%,-50%);
  border-radius:50%;background:rgba(255,255,255,.95);color:#0a0a0a;display:grid;place-items:center;box-shadow:0 18px 50px rgba(0,0,0,.4);transition:transform .45s var(--ease)}
.pb svg{width:38%;height:38%;margin-left:6%}
.pb::after{content:"";position:absolute;inset:-10px;border-radius:50%;border:1px solid rgba(255,255,255,.7);animation:pulse 2.4s var(--ease) infinite}
@keyframes pulse{from{transform:scale(.9);opacity:1}to{transform:scale(1.35);opacity:0}}
.ph:hover .pb{transform:translate(-50%,-50%) scale(1.08)}
.ph:focus-visible{outline:3px solid #fff;outline-offset:-6px}
.now{padding:14px 4px 0;transition:opacity .35s var(--ease)}
.now.swap{opacity:0}
.now-t{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font:800 clamp(19px,1.6vw,26px)/1.18 var(--sans);letter-spacing:-.03em;color:#fff}
.now-t:hover{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:4px}
.now-p{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin:8px 0 0;font:400 15px/1.55 var(--sans);color:rgba(255,255,255,.68)}
.lp-m{border-radius:14px;aspect-ratio:auto!important;height:min(calc((100vw - 2 * var(--gut)) * .5 * 9 / 16),calc(100vh - 470px))}
.strip{position:relative;display:flex;align-items:center;gap:8px;margin-top:14px}
.st{list-style:none;margin:0;padding:0;flex:1;display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 24px) / 3);gap:12px;
  overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;scroll-behavior:smooth}
.st::-webkit-scrollbar{display:none}
.st li{scroll-snap-align:start;min-width:0}
.st a{display:block}
.st-m{position:relative;display:block;aspect-ratio:16/9;border-radius:10px;overflow:hidden;background:#1c1c1e}
.st-m img{width:100%;height:100%;object-fit:cover;transition:transform .8s var(--ease),opacity .3s;opacity:.82}
.st a:hover .st-m img,.st li.on .st-m img{opacity:1;transform:scale(1.05)}
.st-pb{position:absolute;left:8px;bottom:8px;width:24px;height:24px;border-radius:50%;background:rgba(255,255,255,.92);color:#0a0a0a;display:grid;place-items:center}
.st-pb svg{width:11px;height:11px;margin-left:1px}
.st li.on .st-m{outline:2px solid #fff;outline-offset:-2px}
.st-t{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-top:7px;font:600 12.5px/1.35 var(--sans);color:rgba(255,255,255,.86)}
.st-b{all:unset;cursor:pointer;flex:none;width:32px;height:32px;border-radius:50%;display:grid;place-items:center;color:#fff;
  background:rgba(255,255,255,.1);transition:background-color .2s,opacity .2s;margin-bottom:34px}
.st-b:hover{background:rgba(255,255,255,.22)}
.st-b[disabled]{opacity:.25;cursor:default}
.st-b svg{width:16px;height:16px}
.st-b[data-d="-1"] svg{transform:rotate(180deg)}
.st-b:focus-visible{outline:2px solid #fff;outline-offset:2px}

/* правая колонка: реклама и содержание */
.rail{display:flex;flex-direction:column;gap:18px}
.ad{background:#060606;color:#fff;border-radius:clamp(16px,1.6vw,22px);overflow:hidden;border:1px solid var(--cinline)}
.ad-m{display:block;padding:7px 7px 0}
.ad-m video,.band-m video{width:100%;height:auto;aspect-ratio:16/9;border-radius:12px;background:#000}
.ad-b{padding:14px 18px 18px}
.ad-k{display:flex;align-items:center;gap:10px;font:700 10px/1.3 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:#a1a1a6}
.ad-t{margin-top:8px;font:800 clamp(18px,1.4vw,22px)/1.15 var(--sans);letter-spacing:-.03em;color:#fff}
.ad-p{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;margin:8px 0 0;font:400 13.5px/1.5 var(--sans);color:#b9b9c0}
.ad .pill{display:flex;width:100%;margin-top:14px;font-size:14px;padding:13px 16px}
.ad .pill:hover{box-shadow:0 12px 30px rgba(255,138,51,.35)}
.toc ol{list-style:none;margin:10px 0 0;padding:0}
.toc a{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 0;border-top:1px solid var(--line);
  font:800 17px/1.2 var(--sans);letter-spacing:-.02em;color:var(--ink);transition:padding .35s var(--ease)}
.toc li:last-child a{border-bottom:1px solid var(--line)}
.toc a svg{width:16px;height:16px;flex:none;color:var(--muted);transition:transform .35s var(--ease),color .2s}
.toc a:hover{padding-left:8px}
.toc a:hover svg{transform:translateX(4px);color:var(--ink)}

/* слово автора */
.letter{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,9fr);gap:clamp(24px,4vw,72px);padding-top:clamp(56px,6vw,96px);padding-bottom:clamp(56px,6vw,96px)}
.sig{display:flex;align-items:center;gap:14px;margin-top:18px}
.sig img{width:52px;height:52px;border-radius:50%;object-fit:cover}
.sig b{display:block;font:700 15px/1.3 var(--sans);color:var(--ink)}
.sig span{font:700 10px/1.4 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.lt-p{margin:0;font:500 clamp(22px,2.3vw,34px)/1.36 var(--sans);letter-spacing:-.02em;color:var(--ink);text-wrap:pretty}

/* авторский канал — колонка автора */
.paper{background:var(--paper);color:var(--paper-ink);padding:clamp(64px,7vw,112px) 0;transition:background-color .5s var(--ease)}
.au-h{display:flex;align-items:center;gap:18px;padding-bottom:clamp(28px,3vw,44px);border-bottom:1px solid var(--paper-line);margin-bottom:clamp(28px,3vw,44px)}
.au-h img{width:64px;height:64px;border-radius:50%;object-fit:cover;filter:grayscale(.2)}
.au-t{font:800 clamp(40px,5vw,80px)/.95 var(--serif);letter-spacing:-.02em;font-style:italic}
.au-by{display:block;margin-top:8px;font:700 11px/1 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--paper-body)}
.au-g{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(28px,4vw,72px)}
.au-lead .media{border-radius:6px}
.au-lt{margin-top:24px;font:800 clamp(30px,3vw,50px)/1.06 var(--serif);letter-spacing:-.015em;text-wrap:balance}
.au-tx p{margin:14px 0 0;font:400 18px/1.7 var(--sans);color:var(--paper-body);text-wrap:pretty}
.au-tx p:first-child::first-letter{float:left;font:800 3.4em/.82 var(--serif);margin:.06em .1em 0 0;color:var(--paper-ink)}
.paper .cta{display:inline-block;margin-top:22px;font:700 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--paper-ink);
  padding-bottom:5px;border-bottom:1px solid currentColor}
.au-side{display:flex;flex-direction:column}
.au-i{display:grid;grid-template-columns:136px minmax(0,1fr);gap:18px;align-items:center;padding:18px 0;border-top:1px solid var(--paper-line)}
.au-i:first-child{border-top:0;padding-top:0}
.au-im{border-radius:4px}
.au-ph{display:grid;place-items:center;aspect-ratio:16/9;border-radius:4px;background:var(--paper-line);font:800 64px/1 var(--serif);color:var(--paper-body);padding-top:18px}
.au-it{font:700 clamp(17px,1.35vw,21px)/1.25 var(--serif);letter-spacing:-.005em}

/* исследования — лаборатория */
.lab{position:relative;overflow:hidden;background:#07080f;color:#eef0ff;padding:clamp(64px,7vw,112px) 0;
  background-image:linear-gradient(rgba(160,113,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(160,113,255,.07) 1px,transparent 1px),
  linear-gradient(rgba(160,113,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(160,113,255,.035) 1px,transparent 1px);
  background-size:96px 96px,96px 96px,24px 24px,24px 24px}
.lab-glow{position:absolute;width:60vw;height:60vw;left:50%;top:-30vw;transform:translateX(-50%);
  background:radial-gradient(closest-side,rgba(124,77,255,.35),transparent);filter:blur(20px);pointer-events:none;animation:breathe 9s ease-in-out infinite alternate}
@keyframes breathe{from{opacity:.55;transform:translateX(-50%) scale(.95)}to{opacity:1;transform:translateX(-50%) scale(1.08)}}
.lab .wrap{position:relative}
.lb-h{display:flex;align-items:center;gap:18px;margin-bottom:clamp(32px,3.4vw,52px)}
.lb-ic{width:56px;height:56px;border-radius:16px;display:grid;place-items:center;color:#c4a8ff;background:rgba(160,113,255,.12);
  border:1px solid rgba(160,113,255,.35);box-shadow:0 0 40px rgba(160,113,255,.25);flex:none}
.lb-ic svg{width:30px;height:30px}
.lb-ht{font:800 clamp(38px,4.6vw,72px)/1 var(--sans);letter-spacing:-.045em;color:#fff;text-shadow:0 0 40px rgba(160,113,255,.35)}
.lb-line{flex:1;height:1px;background:linear-gradient(90deg,rgba(160,113,255,.6),transparent)}
.lb-f,.lb-c{position:relative;background:rgba(14,15,28,.72);border:1px solid rgba(160,113,255,.18);border-radius:18px;padding:14px;
  -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);transition:border-color .4s var(--ease),box-shadow .4s var(--ease),transform .5s var(--ease)}
.lb-f:hover,.lb-c:hover{border-color:rgba(160,113,255,.55);box-shadow:0 0 0 1px rgba(160,113,255,.2),0 24px 60px -20px rgba(124,77,255,.45)}
.lb-c:hover{transform:translateY(-4px)}
.cb{position:absolute;inset:0;pointer-events:none;z-index:2}
.cb::before,.cb::after{content:"";position:absolute;width:14px;height:14px;border-color:#a071ff;border-style:solid}
.cb::before{left:-1px;top:-1px;border-width:2px 0 0 2px;border-top-left-radius:18px}
.cb::after{right:-1px;bottom:-1px;border-width:0 2px 2px 0;border-bottom-right-radius:18px}
.lab .media{border-radius:10px;background:#12121f}
.lb-f{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(20px,3vw,48px);align-items:center;margin-bottom:clamp(20px,2vw,28px)}
.lb-fb{padding:10px clamp(4px,1vw,16px) 10px 0}
.lb-tag{display:inline-flex;align-items:center;gap:8px;font:700 10px/1 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:#a071ff}
.lb-tag::before{content:"";width:6px;height:6px;border-radius:50%;background:#a071ff;box-shadow:0 0 10px #a071ff}
.lb-ft{margin-top:14px;font:800 clamp(26px,2.6vw,40px)/1.08 var(--sans);letter-spacing:-.035em;color:#fff;text-wrap:balance}
.lb-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(16px,2vw,28px)}
.lb-c .lb-tag{margin-top:16px}
.lb-t{margin-top:10px;font:800 clamp(18px,1.4vw,22px)/1.2 var(--sans);letter-spacing:-.025em;color:#fff}
.lb-p{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;margin:10px 0 0;font:400 14.5px/1.58 var(--sans);color:#a9acc6}
.lb-f .lb-p{-webkit-line-clamp:5;font-size:16px}
.lb-cta{display:inline-flex;margin-top:14px;font:700 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:#c4a8ff;
  padding-bottom:4px;border-bottom:1px solid rgba(196,168,255,.5);transition:color .2s,border-color .2s}
.lb-cta:hover{color:#fff;border-color:#fff}

/* обучение — академия */
.acad{background-color:var(--acad);color:var(--acad-ink);padding:clamp(64px,7vw,112px) 0;
  background-image:radial-gradient(var(--acad-dot) 1.2px,transparent 1.3px);background-size:22px 22px;transition:background-color .5s var(--ease)}
.ac-h{display:flex;align-items:center;gap:18px;margin-bottom:clamp(32px,3.4vw,52px)}
.ac-em{width:60px;height:60px;border-radius:50%;display:grid;place-items:center;color:#fff;background:linear-gradient(135deg,#1d2b64,#5b3bd1);
  box-shadow:0 0 0 5px var(--acad),0 0 0 6px #b9a3ff;flex:none}
.ac-em svg{width:30px;height:30px}
.ac-ht{font:800 clamp(38px,4.6vw,72px)/1 var(--serif);letter-spacing:-.01em}
.ac-f,.ac-c{background:var(--acad-card);border-radius:22px;overflow:hidden;box-shadow:0 1px 0 rgba(16,24,40,.04),0 24px 50px -28px rgba(16,24,40,.28);
  transition:transform .5s var(--ease),box-shadow .5s var(--ease)}
.ac-f:hover,.ac-c:hover{transform:translateY(-4px);box-shadow:0 1px 0 rgba(16,24,40,.04),0 34px 60px -26px rgba(16,24,40,.38)}
.acad .media{border-radius:0;background:#dfe4ee}
.ac-f{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);align-items:center;margin-bottom:clamp(20px,2vw,28px)}
.ac-fb{padding:clamp(24px,3vw,48px)}
.ac-tag{display:inline-flex;align-items:center;gap:7px;font:700 10px/1 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:#5b3bd1;
  background:rgba(91,59,209,.1);padding:7px 10px 7px 9px;border-radius:999px}
.ac-tag::before{content:"";width:0;height:0;border-left:7px solid currentColor;border-top:4px solid transparent;border-bottom:4px solid transparent}
html[data-theme="dark"] .ac-tag{color:#b9a3ff;background:rgba(185,163,255,.12)}
.ac-ft{margin-top:16px;font:800 clamp(26px,2.6vw,40px)/1.08 var(--serif);letter-spacing:-.01em;text-wrap:balance}
.ac-p{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;margin:12px 0 0;font:400 15px/1.6 var(--sans);color:var(--acad-body)}
.ac-f .ac-p{-webkit-line-clamp:5;font-size:16px}
.ac-btn{display:inline-flex;margin-top:22px;font:700 14px/1 var(--sans);color:#fff;background:linear-gradient(135deg,#1d2b64,#5b3bd1);
  padding:14px 20px;border-radius:999px;transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
.ac-btn:hover{transform:translateY(-2px);box-shadow:0 14px 30px -10px rgba(91,59,209,.6)}
.ac-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(16px,2vw,28px)}
.ac-cb{padding:18px 22px 22px}
.ac-t{margin-top:12px;font:700 clamp(18px,1.4vw,22px)/1.22 var(--serif)}
.ac-cta{display:inline-flex;margin-top:14px;font:700 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:#5b3bd1;
  padding-bottom:4px;border-bottom:1px solid currentColor}
html[data-theme="dark"] .ac-cta{color:#b9a3ff}

/* Нейроний — во всю ширину */
.band{position:relative;overflow:hidden;background:#07060a;color:#fff;padding:clamp(56px,6vw,96px) 0}
.glow{position:absolute;inset:-20%;filter:blur(70px);opacity:.75;pointer-events:none}
.glow i{position:absolute;border-radius:50%;mix-blend-mode:screen;animation:drift 18s ease-in-out infinite alternate}
.glow i:nth-child(1){width:46%;height:60%;left:6%;top:12%;background:#6d28d9;animation-duration:19s}
.glow i:nth-child(2){width:38%;height:52%;left:40%;top:30%;background:#db2777;animation-duration:23s;animation-delay:-6s}
.glow i:nth-child(3){width:36%;height:48%;left:62%;top:4%;background:#f97316;animation-duration:27s;animation-delay:-12s}
@keyframes drift{0%{transform:translate(0,0) scale(1)}50%{transform:translate(6%,8%) scale(1.12)}100%{transform:translate(-6%,-4%) scale(.94)}}
.band::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,6,10,.15),rgba(7,6,10,.55))}
.band-in{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(28px,4vw,72px);align-items:center}
.band-m{display:block;border-radius:clamp(16px,1.6vw,24px);overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45)}
.band-m video{border-radius:0}
.nr{display:inline-grid;place-items:center;width:28px;height:28px;border:1px solid rgba(255,255,255,.45);border-radius:7px;
  font:700 13px/1 var(--sans);letter-spacing:-.05em;color:#fff;text-transform:none}
.band-t{margin-top:18px;font:800 clamp(30px,3.6vw,56px)/1.04 var(--sans);letter-spacing:-.045em;text-wrap:balance}
.band-p{margin:18px 0 0;font:400 17px/1.6 var(--sans);color:rgba(255,255,255,.78);max-width:46ch}
.band .pill{margin-top:28px}

/* подвал */
.ft{padding:clamp(56px,7vw,104px) 0 40px}
.ft-mark{display:flex;justify-content:space-between;font:800 min(15.4vw,232px)/.8 var(--sans);letter-spacing:-.04em;color:var(--ghost);
  padding-bottom:.04em;user-select:none;transition:color .5s var(--ease)}
.ft-row{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px 28px;border-top:1px solid var(--ink);
  margin-top:clamp(18px,2vw,28px);padding-top:18px;font:700 11px/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}
.soc{display:flex;flex-wrap:wrap;gap:8px 22px}
.soc a,.up{background:linear-gradient(currentColor,currentColor) 0 100%/0 1px no-repeat;padding-bottom:3px;transition:background-size .4s var(--ease)}
.soc a:hover,.up:hover{background-size:100% 1px}
.made{display:inline-flex;align-items:center;gap:8px;color:var(--muted)}
.made b{color:var(--ink)}
.made .nr{width:22px;height:22px;font-size:11px;border-color:var(--dim);color:var(--ink);border-radius:5px}

/* адаптивность */
@media (max-height:900px) and (min-width:1181px){.now-p{display:none}.ad-p{-webkit-line-clamp:2}}
@media (max-width:1180px){
  .spread{grid-template-columns:minmax(0,4fr) minmax(0,8fr)}
  .rail{grid-column:1/-1;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(20px,3vw,40px);align-items:start;padding-top:12px}
  .player{width:100%;min-width:0}
  .lp-m{height:auto;aspect-ratio:16/9!important}
  .lb-g,.ac-g{grid-template-columns:repeat(2,minmax(0,1fr))}
  .chip{display:none}
}
@media (max-width:860px){
  :root{--top:56px}
  .top-in{gap:12px}
  .brand{opacity:1;transform:none;font-size:17px}
  .nav{margin:0;flex:1;justify-content:flex-start;-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}
  .nav a{padding:9px 10px;font-size:10px}
  .mrow{flex-direction:column;align-items:stretch;gap:12px}
  .mast{justify-content:space-between;font-size:17.4vw}
  .mmeta{grid-auto-flow:column;justify-content:space-between;text-align:left;padding:0;font-size:10px}
  .mmeta span:last-child{display:none}
  .tk-l{padding:8px 12px;font-size:9px}
  .spread{grid-template-columns:1fr;gap:40px}
  .col-lead{order:-1}
  .rail{display:flex}
  .st{grid-auto-columns:42%}
  .letter,.au-g,.lb-f,.ac-f,.band-in{grid-template-columns:1fr}
  .lb-g,.ac-g{grid-template-columns:1fr}
  .au-i{grid-template-columns:112px minmax(0,1fr);gap:14px}
  .ft-row{flex-direction:column;align-items:flex-start}
}
@media (max-width:480px){
  .chip,.nav{display:none}
  .tools{margin-left:auto}
  .st{grid-auto-columns:64%}
  .st-b{display:none}
  .au-tx p,.lt-p{font-size:17px}
}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation:none!important;transition:none!important}
  html.js .rv,html.js .mast span,html.js .rule{opacity:1;transform:none}
  html.js .rv .media,html.js .media.rv{clip-path:none}
}
"""

JS = r"""
(function(){
var d=document.documentElement,reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var tb=document.getElementById('theme');
function lab(){var l=tb.getAttribute(d.getAttribute('data-theme')==='dark'?'data-light':'data-dark');tb.setAttribute('aria-label',l);tb.title=l;}
if(tb){lab();tb.addEventListener('click',function(){var dark=d.getAttribute('data-theme')!=='dark';
  if(dark)d.setAttribute('data-theme','dark');else d.removeAttribute('data-theme');try{localStorage.setItem('theme',dark?'dark':'light')}catch(e){}lab();});}
function go(){d.classList.add('ready')}
if(document.fonts&&document.fonts.ready){var done=false;document.fonts.ready.then(function(){if(!done){done=true;go()}});setTimeout(function(){if(!done){done=true;go()}},900)}else go();
var top=document.querySelector('.top'),bar=document.querySelector('.prog i'),ticking=false;
function onScroll(){ticking=false;var y=window.scrollY||0,h=d.scrollHeight-innerHeight;top.classList.toggle('scrolled',y>40);
  bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';
  if(y<160)document.querySelectorAll('.nav a.on').forEach(function(a){a.classList.remove('on')});}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll)}},{passive:true});onScroll();
// ленты карточек со стрелками
document.querySelectorAll('.strip').forEach(function(s){var ol=s.querySelector('.st'),bs=s.querySelectorAll('.st-b');
  function upd(){bs[0].disabled=ol.scrollLeft<4;bs[1].disabled=ol.scrollLeft+ol.clientWidth>=ol.scrollWidth-4;}
  bs.forEach(function(b){b.addEventListener('click',function(){ol.scrollBy({left:+b.getAttribute('data-d')*ol.clientWidth,behavior:reduce?'auto':'smooth'})})});
  ol.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();});
if(!('IntersectionObserver' in window)){d.classList.remove('js');return;}
var io=new IntersectionObserver(function(es){var k=0;es.forEach(function(e){if(e.isIntersecting){
  e.target.style.setProperty('--d',Math.min(k++,6)*0.07+'s');e.target.classList.add('in');io.unobserve(e.target);}});},
  {rootMargin:'0px 0px -6% 0px',threshold:0.05});
document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
var links={};document.querySelectorAll('.nav a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
var spy=new IntersectionObserver(function(es){es.forEach(function(e){var a=links[e.target.id];if(a&&e.isIntersecting&&(window.scrollY||0)>=160){
  for(var k in links)links[k].classList.remove('on');a.classList.add('on');
  if(a.parentNode.scrollWidth>a.parentNode.clientWidth)a.parentNode.scrollTo({left:a.offsetLeft-24,behavior:reduce?'auto':'smooth'});}});},
  {rootMargin:'-40% 0px -55% 0px'});
document.querySelectorAll('[data-spy]').forEach(function(s){spy.observe(s)});
var vs=document.querySelectorAll('video.ad-video');
if(reduce)vs.forEach(function(v){v.removeAttribute('autoplay');v.pause()});
else{var seen=[];var vo=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;
  if(e.isIntersecting){if(seen.indexOf(v)<0){seen.push(v);try{v.currentTime=0}catch(x){}}var p=v.play();if(p&&p.catch)p.catch(function(){});}
  else v.pause();});},{threshold:0.35});vs.forEach(function(v){vo.observe(v)});}
var player=document.querySelector('.player');
if(player&&player.getAttribute('data-embed')==='1'){
  var now=document.querySelector('.cinema .now'),nt=now.querySelector('.now-t'),np=now.querySelector('.now-p');
  var play=function(id,title){var f=document.createElement('iframe');
    f.src='https://www.youtube.com/embed/'+id+'?autoplay=1&rel=0&modestbranding=1&playsinline=1';f.title=title||'';
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.referrerPolicy='strict-origin-when-cross-origin';f.allowFullscreen=true;player.innerHTML='';player.appendChild(f);};
  player.addEventListener('click',function(e){var b=e.target.closest('.ph');if(!b)return;e.preventDefault();play(b.getAttribute('data-id'),nt.textContent);});
  document.querySelectorAll('.cinema .st a[data-id]').forEach(function(a){a.addEventListener('click',function(e){
    if(e.metaKey||e.ctrlKey||e.shiftKey)return;e.preventDefault();
    document.querySelectorAll('.cinema .st li').forEach(function(li){li.classList.remove('on')});a.parentNode.classList.add('on');
    now.classList.add('swap');setTimeout(function(){nt.textContent=a.getAttribute('data-title');nt.href=a.getAttribute('data-url');
      if(np)np.textContent=a.getAttribute('data-text');now.classList.remove('swap');},reduce?0:220);
    play(a.getAttribute('data-id'),a.getAttribute('data-title'));
    var r=player.getBoundingClientRect();if(r.top<60||r.bottom>innerHeight)player.scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});});});
}
})();
"""


def render(ctx):
    lang, mt = ctx["lang"], MT[ctx["lang"]]
    secs = ctx["sections"]
    by = {s["key"]: s for s in secs}
    lead = "video" if "video" in by else ("author" if "author" in by else None)

    nav = "".join(f'<a href="#{s["key"]}">{esc(mt["nav"][s["key"]])}</a>' for s in secs)
    toc = "".join(f'<li><a href="#{s["key"]}">{esc(s["title"])}{ARROW}</a></li>' for s in secs)
    letters = "".join(f'<span style="--i:{i}" aria-hidden="true">{esc(c)}</span>' for i, c in enumerate(ctx["brand"]))
    foot_letters = "".join(f"<span>{esc(c)}</span>" for c in ctx["brand"])
    issue = mt["issue"].format(n=ctx["n"])

    news = ctx.get("news") or {}
    tick = "".join(f'<a {ext(x["url"])} tabindex="-1">{esc(x["title"])}</a><b>●</b>' for x in news.get("items", []))
    ticker = (f'<div class="ticker rv" aria-hidden="true"><span class="tk-l"><i class="live"></i>{esc(mt["ticker"])}</span>'
              f'<div class="tk-in"><div class="tk"><span>{tick}</span><span>{tick}</span></div></div></div>') if tick else ""

    # первый экран: новости | видеожурнал (или главный материал) | реклама ИИ-трансформации и содержание
    cols = []
    if "news" in by:
        cols.append(f'<section class="col-news" id="news" data-spy>{news_col(by["news"]["title"], news)}</section>')
    if lead:
        body = (video_panel(by[lead]["title"], ctx["video"], ctx["embed"], mt) if lead == "video"
                else lead_panel(by[lead]["title"], ctx[lead], mt))
        cols.append(f'<section class="col-lead" id="{lead}" data-spy>{body}</section>')
    cols.append(f'<div class="rail">{ait_card(ctx["ait"]) if ctx.get("ait") else ""}'
                f'<nav class="toc rv" aria-label="{esc(mt["contents"])}"><div class="k">{esc(mt["contents"])}</div><ol>{toc}</ol></nav></div>')

    # дальше: у каждого раздела свой облик; Нейроний — в конце во всю ширину
    rest = []
    for s in secs:
        k = s["key"]
        if k in ("news", lead) or not ctx.get(k):
            continue
        if k == "author":
            rest.append(author_band(s["title"], ctx[k], ctx))
        elif k == "research":
            rest.append(lab_band(s["title"], ctx[k], mt))
        elif k == "edu":
            rest.append(academy_band(s["title"], ctx[k], mt))
    if ctx.get("nr"):
        rest.append(nr_band(ctx["nr"]))

    socials = "".join(f'<a {ext(u)}>{esc(n)}</a>' for n, u in ctx["socials"])
    og = ""
    if ctx.get("og_image"):
        og = (f'<meta property="og:type" content="article"><meta property="og:title" content="{esc(ctx["title"])}">'
              f'<meta property="og:description" content="{esc(ctx["description"])}"><meta property="og:image" content="{esc(ctx["og_image"])}">'
              f'<meta name="twitter:card" content="summary_large_image">')
        if ctx.get("url"):
            og += f'<meta property="og:url" content="{esc(ctx["url"])}"><link rel="canonical" href="{esc(ctx["url"])}">'

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(ctx["title"])}</title>
<meta name="description" content="{esc(ctx["description"])}">
<meta name="color-scheme" content="light dark">
{og}
<script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('theme')==='dark')document.documentElement.setAttribute('data-theme','dark')}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Playfair+Display:ital,wght@0,700;0,800;1,800&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">{esc(mt["skip"])}</a>
<header class="top"><div class="wrap top-in">
<a class="brand" href="#top" aria-label="{esc(ctx["brand"])}"><span class="mk">i</span>{esc(ctx["brand"])}</a>
<nav class="nav" aria-label="{esc(mt["contents"])}">{nav}</nav>
<div class="tools"><span class="chip">{esc(mt["issue_short"].format(n=ctx["n"]))} · {esc(ctx["date_short"])}</span>
<button id="theme" type="button" data-dark="{esc(ctx["to_dark"])}" data-light="{esc(ctx["to_light"])}" aria-label="{esc(ctx["to_dark"])}">
<span class="t-d">{MOON}</span><span class="t-l">{SUN}</span></button></div></div>
<div class="prog" aria-hidden="true"><i></i></div></header>

<main id="main">
<div class="wrap front" id="top">
<div class="mrow"><h1 class="mast" aria-label="{esc(ctx["brand"])} — {esc(issue)}">{letters}</h1>
<div class="mmeta"><b>{esc(issue)}</b><span>{esc(ctx["date_range"])}</span><span>{esc(mt["tagline"])}</span></div></div>
<div class="rule" aria-hidden="true"></div>
{ticker}
<div class="spread">{"".join(cols)}</div>
</div>
<section class="wrap letter"><div class="rv"><div class="k">{esc(mt["letter"])}</div>
<div class="sig"><img src="{esc(ctx["avatar"])}" alt="" width="52" height="52"><div><b>{esc(ctx["sign"])}</b><span>{esc(ctx["sign_role"])}</span></div></div></div>
<p class="lt-p rv">{esc(ctx["hello"])}</p></section>
{"".join(rest)}
</main>

<footer class="ft"><div class="wrap">
<div class="ft-mark" aria-hidden="true">{foot_letters}</div>
<div class="ft-row"><div class="soc">{socials}</div>
<span>{esc(issue)} · {esc(ctx["date_long"])}</span>
<span class="made">{esc(mt["made"])} <span class="nr">Nr</span><b>{esc(ctx["made_name"])}</b></span>
<a class="up" href="#top">{esc(mt["top"])}</a></div></div></footer>
<script>{JS}</script>
</body></html>
'''

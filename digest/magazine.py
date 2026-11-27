"""Веб-версия выпуска Датаиста — цифровая газета на весь экран.

render(ctx) → HTML-страница. Материалы те же, что в письме; их собирает build.py.
Газетная вёрстка: белый лист (в тёмной теме — чёрный), колонки разделены тонкими линиями, разделы открываются
жирной двойной линией, прямые углы, заголовки с засечками. Свой фон — только у рекламы.
Первая полоса: топ новостей | видеожурнал с плеером на странице | реклама ИИ-трансформации и содержание.
Дальше разделы различаются вёрсткой: колонка автора, Лаборатория (рамки-«видоискатели»), Академия (программа уроков).
"""
import html
import re

MT = {
    "ru": {
        "tagline": "Еженедельный журнал об ИИ", "contents": "В этом выпуске", "letter": "От автора",
        "nav": {"news": "Новости", "video": "Видео", "author": "Канал", "research": "Лаборатория", "edu": "Академия"},
        "play": "Смотреть видео", "top": "Наверх ↑", "prev": "Назад", "next": "Дальше",
        "skip": "Перейти к содержанию", "made": "Создано в", "issue": "Выпуск № {n}", "issue_short": "№ {n}",
        "lesson": "Урок", "study": "Исследование",
    },
    "en": {
        "tagline": "The weekly AI magazine", "contents": "In this issue", "letter": "From the author",
        "nav": {"news": "News", "video": "Video", "author": "Channel", "research": "Lab", "edu": "Academy"},
        "play": "Watch the video", "top": "Back to top ↑", "prev": "Back", "next": "Next",
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
FLASK = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" '
         'aria-hidden="true"><path d="M19 5h10M21 5v13L9.5 37.5A4 4 0 0 0 13 43h22a4 4 0 0 0 3.5-5.5L27 18V5"/>'
         '<path d="M14.5 30h19"/><circle cx="20" cy="36" r="1.6" fill="currentColor"/><circle cx="27" cy="33" r="1.1" fill="currentColor"/></svg>')
CAP = ('<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" '
       'aria-hidden="true"><path d="M4 18 24 9l20 9-20 9z"/><path d="M12 22v10c0 3 5.4 6 12 6s12-3 12-6V22"/><path d="M44 18v11"/></svg>')


def esc(s):
    return html.escape(str(s), quote=True)


def nobr(s):
    """«ИИ-операционная» не рвётся по дефису."""
    return re.sub(r"(?<![\w-])((?:ИИ|AI)-[\w-]+)", r'<span class="nb">\1</span>', esc(s))


def ext(url):
    return f'href="{esc(url)}" target="_blank" rel="noopener"'


# ───────────────────────── блоки ─────────────────────────
def media(url, img, alt="", cls="media"):
    if not img:
        return ""
    return (f'<a class="{cls}" {ext(url)} tabindex="-1">'
            f'<img src="{esc(img)}" alt="{esc(alt)}" loading="lazy" decoding="async"></a>')


def paras(ps, cls="p"):
    return "".join(f'<p class="{cls}">{esc(p)}</p>' for p in ps)


def cta(url, label, cls="cta"):
    return f'<a class="{cls}" {ext(url)}>{esc(label)}</a>'


def kick(title, live=False):
    """Заголовок колонки на первой полосе: жирная линия и подпись капителью."""
    return f'<div class="kick rv">{"<i class=live aria-hidden=true></i>" if live else ""}{esc(title)}</div>'


def sec_head(title, icon="", extra=""):
    """Шапка раздела: двойная газетная линия и крупное название."""
    return f'<div class="sh rv">{icon}<h2 class="sh-t">{esc(title)}</h2>{extra}</div>'


def strip(items, label_prev, label_next):
    """Лента карточек с прокруткой и стрелками."""
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
    return f'{kick(title, live=True)}<ol class="nws">{rows}</ol>{more}'


def video_col(title, videos, embed, mt):
    """Видеожурнал: плеер на странице, заголовок, лента всех видео выпуска."""
    v0 = videos[0]
    inner = f'<img src="{esc(v0["cover"])}" alt="" decoding="async"><span class="pb">{PLAY}</span>'
    stage = (f'<button class="ph" type="button" data-id="{esc(v0["id"])}" aria-label="{esc(mt["play"])}: {esc(v0["title"])}">{inner}</button>'
             if embed else f'<a class="ph" {ext(v0["url"])} aria-label="{esc(mt["play"])}: {esc(v0["title"])}">{inner}</a>')
    items = "".join(
        f'''<li{' class="on"' if i == 0 else ''}><a {ext(v["url"])} data-id="{esc(v["id"])}" data-title="{esc(v["title"])}"
 data-text="{esc(v["text"])}" data-url="{esc(v["url"])}"><span class="st-m"><img src="{esc(v["cover"])}" alt="" loading="lazy" decoding="async">
<span class="st-pb">{PLAY}</span></span><span class="st-t">{esc(v["title"])}</span></a></li>''' for i, v in enumerate(videos))
    return f'''{kick(title)}<div class="vid">
<div class="player rv" data-embed="{1 if embed else 0}">{stage}</div>
<div class="now rv"><a class="now-t" {ext(v0["url"])}>{esc(v0["title"])}</a><p class="now-p">{esc(v0["text"])}</p></div>
{strip(items, mt["prev"], mt["next"]) if len(videos) > 1 else ''}</div>'''


def lead_col(title, items, mt):
    """Центр первой полосы без видео: главный материал крупно и лента остальных."""
    a = items[0]
    rest = "".join(f'''<li><a {ext(x["url"])}><span class="st-m">{f'<img src="{esc(x["img"])}" alt="" loading="lazy" decoding="async">' if x.get("img") else ''}</span>
<span class="st-t">{esc(x["title"])}</span></a></li>''' for x in items[1:])
    return f'''{kick(title)}<div class="vid">
<div class="rv">{media(a["url"], a.get("img"), a["title"], "media lp-m")}</div>
<div class="now rv"><a class="now-t" {ext(a["url"])}>{esc(a["title"])}</a>{paras(a["paras"][:1], "now-p")}</div>
{strip(rest, mt["prev"], mt["next"]) if rest else ''}</div>'''


def ad_video(ad, cls):
    return (f'<a class="{cls}" {ext(ad["url"])} tabindex="-1">'
            f'<video class="ad-video" src="{esc(ad["mp4"])}" poster="{esc(ad["poster"])}" muted loop playsinline preload="metadata" '
            f'autoplay aria-label="{esc(ad["title"])}"></video></a>')


def ait_card(ad):
    """Реклама ИИ-трансформации в правой колонке первой полосы."""
    return f'''<aside class="ad rv" aria-label="{esc(ad["kicker"])}">{ad_video(ad, "ad-m")}
<div class="ad-b"><div class="ad-k">{esc(ad["kicker"])}</div><h3 class="ad-t">{nobr(ad["title"])}</h3>
<p class="ad-p">{nobr(ad["text"])}</p><a class="pill" {ext(ad["url"])}>{esc(ad["cta"])}</a></div></aside>'''


def nr_band(ad):
    return f'''<section class="band" aria-label="{esc(ad["kicker"])}"><div class="glow" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="wrap band-in">{ad_video(ad, "band-m rv")}
<div class="band-b rv"><div class="ad-k"><span class="nr">Nr</span>{esc(ad["kicker"])}</div>
<h2 class="band-t">{nobr(ad["title"])}</h2><p class="band-p">{nobr(ad["text"])}</p>
<a class="pill" {ext(ad["url"])}>{esc(ad["cta"])}</a></div></div></section>'''


def author_sec(title, items, ctx):
    """Авторский канал — колонка автора: главный пост с буквицей и лента остальных справа."""
    a, rest = items[0], items[1:]
    side = "".join(f'''<article class="au-i rv">{media(x["url"], x.get("img"), x["title"], "media au-im") or '<span class="au-ph" aria-hidden="true">“</span>'}
<h3 class="au-it"><a {ext(x["url"])}>{esc(x["title"])}</a></h3></article>''' for x in rest)
    by = (f'<span class="sh-by"><img src="{esc(ctx["avatar"])}" alt="" width="44" height="44"><span>{esc(ctx["sign"])}</span></span>')
    return f'''<section class="wrap sec" id="author" data-spy>{sec_head(title, extra=by)}
<div class="cols au"><article class="au-lead rv">{media(a["url"], a.get("img"), a["title"])}
<h3 class="au-lt"><a {ext(a["url"])}>{esc(a["title"])}</a></h3><div class="au-tx">{paras(a["paras"])}</div>{cta(a["url"], a["cta"])}</article>
{f'<div class="au-side">{side}</div>' if side else ''}</div></section>'''


def lab_sec(title, items, mt):
    """Лаборатория: картинки в рамках-«видоискателях», техничные заголовки, сетка в три колонки."""
    a, rest = items[0], items[1:]
    cards = "".join(f'''<article class="lb-c rv"><div class="xh">{media(x["url"], x.get("img"), x["title"])}</div>
<span class="tag">{esc(mt["study"])}</span><h3 class="lb-t"><a {ext(x["url"])}>{esc(x["title"])}</a></h3>
{paras(x["paras"][:1], "lb-p")}{cta(x["url"], x["cta"])}</article>''' for x in rest)
    return f'''<section class="wrap sec" id="research" data-spy>{sec_head(title, f'<span class="sh-ic">{FLASK}</span>')}
<article class="lb-f rv"><div class="xh">{media(a["url"], a.get("img"), a["title"])}</div>
<div class="lb-fb"><span class="tag">{esc(mt["study"])}</span><h3 class="lb-ft"><a {ext(a["url"])}>{esc(a["title"])}</a></h3>
{paras(a["paras"][:2], "lb-p")}{cta(a["url"], a["cta"])}</div></article>
{f'<div class="lb-g">{cards}</div>' if cards else ''}</section>'''


def academy_sec(title, items, mt):
    """Академия: главный урок и программа — уроки списком в две колонки."""
    a, rest = items[0], items[1:]
    lessons = "".join(f'''<article class="ac-i rv">{media(x["url"], x.get("img"), x["title"])}
<div><span class="tag tag-l">{esc(mt["lesson"])}</span><h3 class="ac-t"><a {ext(x["url"])}>{esc(x["title"])}</a></h3>
{paras(x["paras"][:1], "ac-p")}{cta(x["url"], x["cta"])}</div></article>''' for x in rest)
    return f'''<section class="wrap sec" id="edu" data-spy>{sec_head(title, f'<span class="sh-ic">{CAP}</span>')}
<article class="ac-f rv">{media(a["url"], a.get("img"), a["title"])}
<div class="ac-fb"><span class="tag tag-l">{esc(mt["lesson"])}</span><h3 class="ac-ft"><a {ext(a["url"])}>{esc(a["title"])}</a></h3>
{paras(a["paras"][:2], "ac-p")}{cta(a["url"], a["cta"], "btn")}</div></article>
{f'<div class="ac-l">{lessons}</div>' if lessons else ''}</section>'''


# ───────────────────────── оформление ─────────────────────────
CSS = r"""
:root{--bg:#fff;--ink:#0a0a0a;--text:#1d1d1f;--body:#3a3a3c;--muted:#6e6e73;--dim:#a1a1a6;--line:#dcdce0;--soft:#f2f2f4;
  --hdr:rgba(255,255,255,.92);--ghost:#ededf0;
  --sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  --serif:'Playfair Display',Georgia,'Times New Roman',serif;
  --mono:'Space Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace;
  --gut:clamp(16px,3.2vw,48px);--max:1480px;--ease:cubic-bezier(.2,.8,.2,1);--top:64px;--colgap:clamp(18px,1.9vw,30px)}
html[data-theme="dark"]{--bg:#0a0a0b;--ink:#f5f5f7;--text:#ececf0;--body:#c7c7cc;--muted:#8e8e93;--dim:#636366;--line:#2c2c2f;
  --soft:#161618;--hdr:rgba(10,10,11,.9);--ghost:#18181a;color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:calc(var(--top) + 12px);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:400 16px/1.6 var(--sans);-webkit-font-smoothing:antialiased;
  transition:background-color .5s var(--ease),color .5s var(--ease)}
a{color:inherit;text-decoration:none}
img,video{display:block;max-width:100%}
button{font:inherit;color:inherit}
h1,h2,h3{margin:0}
:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
.nb{white-space:nowrap}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--gut)}
.skip{position:absolute;left:-9999px;top:8px;z-index:100;background:var(--ink);color:var(--bg);padding:10px 16px;
  font:700 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase}
.skip:focus{left:16px}

/* появление при прокрутке */
html.js .rv{opacity:0;transform:translateY(22px);transition:opacity .9s var(--ease) var(--d,0s),transform .9s var(--ease) var(--d,0s)}
html.js .rv.in{opacity:1;transform:none}
.media{display:block;position:relative;overflow:hidden;background:var(--soft);aspect-ratio:16/9}
.media img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}
.media:hover img,article:hover .media img{transform:scale(1.04)}
html.js .rv .media{clip-path:inset(0 0 100% 0);transition:clip-path 1.2s var(--ease) var(--d,0s)}
html.js .rv.in .media{clip-path:inset(0)}
h3 a,.now-t{background:linear-gradient(currentColor,currentColor) 0 100%/0 1.5px no-repeat;transition:background-size .5s var(--ease)}
h3 a:hover,.now-t:hover{background-size:100% 1.5px}
.cta{display:inline-block;margin-top:14px;font:700 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink);
  padding-bottom:4px;border-bottom:1.5px solid currentColor;transition:opacity .2s}
.cta:hover{opacity:.6}
.btn{display:inline-flex;margin-top:22px;font:700 12px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--bg);background:var(--ink);
  padding:15px 20px;transition:opacity .2s}
.btn:hover{opacity:.82}
.tag{display:inline-flex;align-items:center;gap:8px;font:700 10px/1 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--ink)}
.tag::before{content:"";width:7px;height:7px;background:var(--ink)}
.tag-l::before{width:0;height:0;background:none;border-left:7px solid var(--ink);border-top:4px solid transparent;border-bottom:4px solid transparent}
.pill{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:#fff;color:#000;font:700 15px/1 var(--sans);padding:16px 24px;
  border-radius:999px;transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
.pill:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(160,113,255,.35)}

/* шапка сайта */
.top{position:sticky;top:0;z-index:50;background:var(--hdr);-webkit-backdrop-filter:saturate(180%) blur(14px);backdrop-filter:saturate(180%) blur(14px);
  border-bottom:1px solid var(--line);transition:background-color .5s var(--ease)}
.top-in{height:var(--top);display:flex;align-items:center;gap:24px}
.brand{display:flex;align-items:center;gap:12px;color:var(--ink);flex:none}
.brand-w{font:600 20px/1 -apple-system,BlinkMacSystemFont,'Inter',sans-serif;letter-spacing:-.025em;margin-top:2px}
.mk{width:32px;height:32px;border-radius:50%;background:var(--ink);color:var(--bg);display:grid;place-items:center;font:700 14px/1 var(--mono);
  transition:transform .3s var(--ease),background-color .5s var(--ease),color .5s var(--ease)}
.brand:hover .mk{transform:scale(1.05)}
.nav{display:flex;gap:clamp(14px,1.8vw,26px);margin:0 auto;overflow-x:auto;scrollbar-width:none}
.nav::-webkit-scrollbar{display:none}
.nav a{font:700 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding:9px 0 7px;border-bottom:2px solid transparent;
  white-space:nowrap;transition:color .25s,border-color .25s}
.nav a:hover{color:var(--ink)}
.nav a.on{color:var(--ink);border-bottom-color:var(--ink)}
.tools{display:flex;align-items:center;gap:14px;flex:none}
.chip{font:700 10px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
#theme{all:unset;cursor:pointer;width:34px;height:34px;display:grid;place-items:center;color:var(--muted);transition:color .2s}
#theme:hover{color:var(--ink)}
#theme:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
#theme svg{width:18px;height:18px}
#theme .t-l{display:none}
html[data-theme="dark"] #theme .t-d{display:none}
html[data-theme="dark"] #theme .t-l{display:block}
.prog{position:absolute;left:0;right:0;bottom:-1px;height:2px;pointer-events:none}
.prog i{display:block;height:100%;background:var(--ink);transform-origin:0 50%;transform:scaleX(0)}

/* первая полоса: шапка газеты */
.iss{display:flex;justify-content:space-between;gap:16px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);padding:10px 0;margin-top:14px;
  font:700 11px/1.3 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--ink)}
.mast{display:flex;justify-content:space-between;margin-top:clamp(14px,2.2vw,32px);font:800 min(15.4vw,232px)/.8 var(--sans);letter-spacing:-.04em;
  color:var(--ink);overflow:hidden;padding:.02em 0 .05em}
.mast span{display:block}
html.js .mast span{transform:translateY(104%);transition:transform 1.1s var(--ease);transition-delay:calc(var(--i) * 70ms + 120ms)}
html.js.ready .mast span{transform:none}
.rule{height:7px;border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);margin-top:12px;transform-origin:0 50%}
html.js .rule{transform:scaleX(0);transition:transform 1.3s var(--ease) .4s}
html.js.ready .rule{transform:none}
.ticker{overflow:hidden;background:var(--ink);color:var(--bg);margin-top:10px}
.tk{display:flex;width:max-content;animation:tk 90s linear infinite}
.ticker:hover .tk{animation-play-state:paused}
.tk span{display:flex;align-items:center;gap:20px;padding:12px 20px 12px 0;font:700 11px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;white-space:nowrap}
.tk span:first-child{padding-left:20px}
.tk a:hover{text-decoration:underline;text-underline-offset:3px}
.tk b{opacity:.45}
@keyframes tk{to{transform:translateX(-50%)}}

/* колонки первой полосы */
.spread{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,6fr) minmax(0,3fr);padding-top:22px}
.spread>*{padding:0 var(--colgap)}
.spread>*:first-child{padding-left:0}
.spread>*:last-child{padding-right:0}
.spread>*+*{border-left:1px solid var(--line)}
.kick{display:flex;align-items:center;gap:10px;border-top:3px solid var(--ink);padding-top:10px;margin-bottom:14px;
  font:700 12px/1.2 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink)}
.live{width:8px;height:8px;border-radius:50%;background:#ff3b30;position:relative;flex:none}
.live::after{content:"";position:absolute;inset:-4px;border-radius:50%;border:1.5px solid #ff3b30;animation:ping 1.8s var(--ease) infinite}
@keyframes ping{from{transform:scale(.6);opacity:1}to{transform:scale(1.6);opacity:0}}

/* топ новостей */
.nws{list-style:none;margin:0;padding:0}
.nw{display:grid;grid-template-columns:72px minmax(0,1fr);gap:12px;align-items:start;padding:11px 0}
.nws li+li .nw{border-top:1px solid var(--line)}
.nws li:first-child .nw{padding-top:2px}
.nw img,.nw-ph{width:72px;height:48px;object-fit:cover;background:var(--soft);transition:filter .4s}
.nw span{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;font:700 15px/1.3 var(--serif);color:var(--ink)}
.nw:hover span{text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.nw:hover img{filter:contrast(1.08) saturate(1.1)}
.more{display:inline-block;margin-top:12px;font:700 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink);
  padding-bottom:4px;border-bottom:1.5px solid currentColor}
.more:hover{opacity:.6}

/* видеожурнал */
.player{position:relative;width:min(100%,calc((100vh - 500px) * 16 / 9));min-width:min(100%,440px);margin:0 auto;aspect-ratio:16/9;overflow:hidden;background:#000}
.player iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.ph{all:unset;cursor:pointer;position:absolute;inset:0;display:block}
.ph img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease),filter .6s}
.ph:hover img{transform:scale(1.03);filter:brightness(.9)}
.pb{position:absolute;left:50%;top:50%;width:clamp(58px,5.4vw,82px);height:clamp(58px,5.4vw,82px);transform:translate(-50%,-50%);
  border-radius:50%;background:rgba(255,255,255,.95);color:#0a0a0a;display:grid;place-items:center;box-shadow:0 18px 50px rgba(0,0,0,.35);transition:transform .45s var(--ease)}
.pb svg{width:38%;height:38%;margin-left:6%}
.pb::after{content:"";position:absolute;inset:-10px;border-radius:50%;border:1px solid rgba(255,255,255,.75);animation:pulse 2.4s var(--ease) infinite}
@keyframes pulse{from{transform:scale(.9);opacity:1}to{transform:scale(1.35);opacity:0}}
.ph:hover .pb{transform:translate(-50%,-50%) scale(1.08)}
.ph:focus-visible{outline:3px solid #fff;outline-offset:-6px}
.now{padding-top:14px;transition:opacity .35s var(--ease)}
.now.swap{opacity:0}
.now-t{display:inline;font:800 clamp(22px,2vw,30px)/1.16 var(--serif);color:var(--ink)}
.now-p{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin:10px 0 0;font:400 15px/1.55 var(--sans);color:var(--body)}
.lp-m{max-height:calc(100vh - 500px)}
.strip{display:flex;align-items:flex-start;gap:10px;margin-top:16px;padding-top:14px;border-top:1px solid var(--line)}
.st{list-style:none;margin:0;padding:0;flex:1;min-width:0;display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 28px) / 3);gap:14px;
  overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;scroll-behavior:smooth}
.st::-webkit-scrollbar{display:none}
.st li{scroll-snap-align:start;min-width:0}
.st a{display:block}
.st-m{position:relative;display:block;aspect-ratio:16/9;overflow:hidden;background:var(--soft)}
.st-m img{width:100%;height:100%;object-fit:cover;transition:transform .8s var(--ease)}
.st a:hover .st-m img{transform:scale(1.05)}
.st-pb{position:absolute;left:7px;bottom:7px;width:24px;height:24px;border-radius:50%;background:rgba(255,255,255,.94);color:#0a0a0a;display:grid;place-items:center}
.st-pb svg{width:11px;height:11px;margin-left:1px}
.st li.on .st-m{outline:2px solid var(--ink);outline-offset:2px}
.st-t{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-top:8px;font:700 13.5px/1.3 var(--serif);color:var(--ink)}
.st-b{all:unset;cursor:pointer;flex:none;width:32px;height:32px;margin-top:20px;display:grid;place-items:center;color:var(--ink);border:1px solid var(--ink);
  transition:background-color .2s,color .2s,opacity .2s}
.st-b:hover{background:var(--ink);color:var(--bg)}
.st-b[disabled]{opacity:.2;cursor:default;background:none;color:var(--ink)}
.st-b svg{width:15px;height:15px}
.st-b[data-d="-1"] svg{transform:rotate(180deg)}
.st-b:focus-visible{outline:2px solid var(--ink);outline-offset:2px}

/* правая колонка: реклама и содержание */
.rail{display:flex;flex-direction:column;gap:22px}
.ad{background:#060606;color:#fff}
.ad-m{display:block}
.ad-m video,.band-m video{width:100%;height:auto;aspect-ratio:16/9;background:#000}
.ad-b{padding:16px 18px 20px}
.ad-k{display:flex;align-items:center;gap:10px;font:700 10px/1.3 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:#a1a1a6}
.ad-t{margin-top:8px;font:800 clamp(18px,1.4vw,22px)/1.15 var(--sans);letter-spacing:-.03em;color:#fff}
.ad-p{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;margin:8px 0 0;font:400 13.5px/1.5 var(--sans);color:#b9b9c0}
.ad .pill{display:flex;width:100%;margin-top:14px;font-size:14px;padding:13px 16px}
.ad .pill:hover{box-shadow:0 12px 30px rgba(255,138,51,.35)}
.toc ol{list-style:none;margin:0;padding:0}
.toc a{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);
  font:700 18px/1.2 var(--serif);color:var(--ink);transition:padding .35s var(--ease)}
.toc a svg{width:16px;height:16px;flex:none;transition:transform .35s var(--ease)}
.toc a:hover{padding-left:8px}
.toc a:hover svg{transform:translateX(4px)}
.toc .kick{margin-bottom:4px}

/* слово автора */
.letter{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,9fr);gap:clamp(24px,4vw,72px);margin-top:clamp(48px,5vw,80px);
  padding-top:clamp(28px,3vw,44px);border-top:1px solid var(--line)}
.k{font:700 11px/1.3 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.sig{display:flex;align-items:center;gap:14px;margin-top:18px}
.sig img{width:52px;height:52px;border-radius:50%;object-fit:cover}
.sig b{display:block;font:700 15px/1.3 var(--sans);color:var(--ink)}
.sig span{font:700 10px/1.4 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.lt-p{margin:0;font:italic 500 clamp(24px,2.5vw,38px)/1.32 var(--serif);color:var(--ink);text-wrap:pretty}

/* разделы */
.sec{padding-top:clamp(64px,7vw,112px)}
.sh{display:flex;align-items:center;gap:18px;border-top:4px solid var(--ink);padding-top:18px;margin-bottom:clamp(26px,3vw,44px);position:relative}
.sh::before{content:"";position:absolute;left:0;right:0;top:3px;border-top:1px solid var(--ink)}
.sh-t{font:800 clamp(42px,5vw,80px)/.95 var(--sans);letter-spacing:-.045em;color:var(--ink)}
.sh-ic{width:clamp(46px,4vw,60px);height:clamp(46px,4vw,60px);flex:none;display:grid;place-items:center;border:2px solid var(--ink);color:var(--ink)}
.sh-ic svg{width:60%;height:60%}
.sh-by{margin-left:auto;display:flex;align-items:center;gap:12px;font:700 11px/1.3 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.sh-by img{width:44px;height:44px;border-radius:50%;object-fit:cover}
.cols{display:grid}
.cols>*{padding:0 clamp(20px,2.4vw,40px)}
.cols>*:first-child{padding-left:0}
.cols>*:last-child{padding-right:0}
.cols>*+*{border-left:1px solid var(--line)}

/* авторский канал — колонка автора */
.au{grid-template-columns:minmax(0,7fr) minmax(0,5fr)}
.au-lt{margin-top:24px;font:800 clamp(30px,3.1vw,50px)/1.06 var(--serif);letter-spacing:-.01em;color:var(--ink);text-wrap:balance}
.au-tx p{margin:14px 0 0;font:400 18px/1.7 var(--sans);color:var(--body);text-wrap:pretty}
.au-tx p:first-child::first-letter{float:left;font:800 3.5em/.8 var(--serif);margin:.07em .1em 0 0;color:var(--ink)}
.au-side{display:flex;flex-direction:column}
.au-i{display:grid;grid-template-columns:140px minmax(0,1fr);gap:18px;align-items:center;padding:16px 0;border-bottom:1px solid var(--line)}
.au-i:first-child{padding-top:0}
.au-ph{display:grid;place-items:center;aspect-ratio:16/9;background:var(--soft);font:800 60px/1 var(--serif);color:var(--muted);padding-top:18px}
.au-it{font:700 clamp(17px,1.35vw,21px)/1.25 var(--serif);color:var(--ink)}

/* лаборатория — рамки-«видоискатели» */
.xh{--c:var(--ink);padding:9px;background:
  linear-gradient(var(--c),var(--c)) 0 0/16px 1.5px no-repeat,linear-gradient(var(--c),var(--c)) 0 0/1.5px 16px no-repeat,
  linear-gradient(var(--c),var(--c)) 100% 0/16px 1.5px no-repeat,linear-gradient(var(--c),var(--c)) 100% 0/1.5px 16px no-repeat,
  linear-gradient(var(--c),var(--c)) 0 100%/16px 1.5px no-repeat,linear-gradient(var(--c),var(--c)) 0 100%/1.5px 16px no-repeat,
  linear-gradient(var(--c),var(--c)) 100% 100%/16px 1.5px no-repeat,linear-gradient(var(--c),var(--c)) 100% 100%/1.5px 16px no-repeat}
.lb-f{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(24px,3.4vw,56px);align-items:center;
  padding-bottom:clamp(28px,3vw,44px);border-bottom:1px solid var(--line)}
.lb-ft{margin-top:14px;font:800 clamp(28px,2.8vw,44px)/1.05 var(--sans);letter-spacing:-.04em;color:var(--ink);text-wrap:balance}
.lb-p{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;margin:10px 0 0;font:400 15px/1.58 var(--sans);color:var(--body)}
.lb-f .lb-p{-webkit-line-clamp:5;font-size:16.5px}
.lb-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.lb-c{padding:clamp(24px,2.6vw,36px) clamp(18px,1.9vw,30px);border-bottom:1px solid var(--line)}
.lb-c:nth-child(3n+1){padding-left:0}
.lb-c:nth-child(3n){padding-right:0}
.lb-c:not(:nth-child(3n+1)){border-left:1px solid var(--line)}
.lb-c .tag{margin-top:14px}
.lb-t{margin-top:10px;font:800 clamp(19px,1.5vw,23px)/1.18 var(--sans);letter-spacing:-.025em;color:var(--ink)}

/* академия — программа уроков */
.ac-f{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(24px,3.4vw,56px);align-items:center;
  padding-bottom:clamp(28px,3vw,44px);border-bottom:3px solid var(--ink)}
.ac-ft{margin-top:14px;font:800 clamp(28px,2.8vw,44px)/1.08 var(--serif);color:var(--ink);text-wrap:balance}
.ac-p{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin:10px 0 0;font:400 15px/1.58 var(--sans);color:var(--body)}
.ac-f .ac-p{-webkit-line-clamp:5;font-size:16.5px}
.ac-l{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}
.ac-i{display:grid;grid-template-columns:clamp(140px,13vw,200px) minmax(0,1fr);gap:20px;align-items:start;
  padding:clamp(20px,2.2vw,30px) clamp(20px,2.4vw,40px);border-bottom:1px solid var(--line)}
.ac-i:nth-child(odd){padding-left:0}
.ac-i:nth-child(even){padding-right:0;border-left:1px solid var(--line)}
.ac-t{margin-top:10px;font:700 clamp(18px,1.45vw,22px)/1.22 var(--serif);color:var(--ink)}
.ac-i .cta{margin-top:12px}

/* Нейроний — реклама во всю ширину */
.band{position:relative;overflow:hidden;background:#07060a;color:#fff;padding:clamp(56px,6vw,96px) 0;margin-top:clamp(64px,7vw,112px)}
.glow{position:absolute;inset:-20%;filter:blur(70px);opacity:.75;pointer-events:none}
.glow i{position:absolute;border-radius:50%;mix-blend-mode:screen;animation:drift 18s ease-in-out infinite alternate}
.glow i:nth-child(1){width:46%;height:60%;left:6%;top:12%;background:#6d28d9;animation-duration:19s}
.glow i:nth-child(2){width:38%;height:52%;left:40%;top:30%;background:#db2777;animation-duration:23s;animation-delay:-6s}
.glow i:nth-child(3){width:36%;height:48%;left:62%;top:4%;background:#f97316;animation-duration:27s;animation-delay:-12s}
@keyframes drift{0%{transform:translate(0,0) scale(1)}50%{transform:translate(6%,8%) scale(1.12)}100%{transform:translate(-6%,-4%) scale(.94)}}
.band::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,6,10,.15),rgba(7,6,10,.55))}
.band-in{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(28px,4vw,72px);align-items:center}
.band-m{display:block;box-shadow:0 30px 80px rgba(0,0,0,.45)}
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
.soc a,.up{border-bottom:1px solid transparent;padding-bottom:2px;transition:border-color .3s}
.soc a:hover,.up:hover{border-bottom-color:currentColor}
.made{display:inline-flex;align-items:center;gap:8px;color:var(--muted)}
.made b{color:var(--ink)}
.made .nr{width:22px;height:22px;font-size:11px;border-color:var(--dim);color:var(--ink);border-radius:5px}

/* адаптивность */
@media (max-height:900px) and (min-width:1181px){.now-p{display:none}.ad-p{-webkit-line-clamp:2}}
@media (max-width:1180px){
  .spread{grid-template-columns:minmax(0,4fr) minmax(0,8fr)}
  .spread>.col-lead{padding-right:0}
  .rail{grid-column:1/-1;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:var(--colgap);align-items:start;
    border-left:0!important;border-top:1px solid var(--line);margin-top:28px;padding:28px 0 0!important}
  .player{width:100%;min-width:0}
  .lp-m{max-height:none}
  .lb-g{grid-template-columns:repeat(2,minmax(0,1fr))}
  .lb-c:nth-child(n){padding-left:clamp(18px,1.9vw,30px);padding-right:clamp(18px,1.9vw,30px);border-left:1px solid var(--line)}
  .lb-c:nth-child(2n+1){padding-left:0;border-left:0}
  .lb-c:nth-child(2n){padding-right:0}
  .ac-i{grid-template-columns:140px minmax(0,1fr)}
  .chip{display:none}
}
@media (max-width:860px){
  :root{--top:56px}
  .top-in{gap:14px}
  .mk{width:26px;height:26px;font-size:12px}
  .brand-w{font-size:18px}
  .nav{margin:0;flex:1;justify-content:flex-start;-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}
  .nav a{font-size:10px}
  .iss{font-size:10px;letter-spacing:.14em}
  .iss span:nth-child(2){display:none}
  .spread{grid-template-columns:1fr}
  .spread>*{padding:0!important;border-left:0!important}
  .spread>*+*{margin-top:36px}
  .col-lead{order:-1}
  .rail{display:flex;align-items:stretch;border-top:0;margin-top:36px;padding-top:0!important}
  .st{grid-auto-columns:44%}
  .letter,.au,.lb-f,.ac-f,.band-in{grid-template-columns:1fr}
  .cols>*{padding:0!important;border-left:0!important}
  .au-side{margin-top:28px;border-top:1px solid var(--line);padding-top:20px!important}
  .au-i{grid-template-columns:112px minmax(0,1fr);gap:14px}
  .lb-g,.ac-l{grid-template-columns:1fr}
  .lb-c:nth-child(n),.ac-i:nth-child(n){padding-left:0;padding-right:0;border-left:0}
  .ac-i{grid-template-columns:120px minmax(0,1fr);gap:14px}
  .sh-by span{display:none}
  .ft-row{flex-direction:column;align-items:flex-start}
}
@media (max-width:480px){
  .chip,.nav{display:none}
  .tools{margin-left:auto}
  .st{grid-auto-columns:66%}
  .st-b{display:none}
  .au-tx p{font-size:17px}
  .ac-i .ac-p,.au-i .p{display:none}
}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation:none!important;transition:none!important}
  html.js .rv,html.js .mast span,html.js .rule{opacity:1;transform:none}
  html.js .rv .media{clip-path:none}
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
var bar=document.querySelector('.prog i'),ticking=false;
function onScroll(){ticking=false;var y=window.scrollY||0,h=d.scrollHeight-innerHeight;
  bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';
  if(y<160)document.querySelectorAll('.nav a.on').forEach(function(a){a.classList.remove('on')});}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll)}},{passive:true});onScroll();
// ленты карточек со стрелками
document.querySelectorAll('.strip').forEach(function(s){var ol=s.querySelector('.st'),bs=s.querySelectorAll('.st-b');if(!ol||bs.length<2)return;
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
  var box=player.closest('.vid'),now=box.querySelector('.now'),nt=now.querySelector('.now-t'),np=now.querySelector('.now-p');
  var play=function(id,title){var f=document.createElement('iframe');
    f.src='https://www.youtube.com/embed/'+id+'?autoplay=1&rel=0&modestbranding=1&playsinline=1';f.title=title||'';
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.referrerPolicy='strict-origin-when-cross-origin';f.allowFullscreen=true;player.innerHTML='';player.appendChild(f);};
  player.addEventListener('click',function(e){var b=e.target.closest('.ph');if(!b)return;e.preventDefault();play(b.getAttribute('data-id'),nt.textContent);});
  box.querySelectorAll('.st a[data-id]').forEach(function(a){a.addEventListener('click',function(e){
    if(e.metaKey||e.ctrlKey||e.shiftKey)return;e.preventDefault();
    box.querySelectorAll('.st li').forEach(function(li){li.classList.remove('on')});a.parentNode.classList.add('on');
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
    ticker = (f'<div class="ticker rv" aria-hidden="true"><div class="tk"><span>{tick}</span><span>{tick}</span></div></div>'
              if tick else "")

    # первая полоса: новости | видеожурнал (или главный материал) | реклама ИИ-трансформации и содержание
    cols = []
    if "news" in by:
        cols.append(f'<section class="col-news" id="news" data-spy>{news_col(by["news"]["title"], news)}</section>')
    if lead:
        body = (video_col(by[lead]["title"], ctx["video"], ctx["embed"], mt) if lead == "video"
                else lead_col(by[lead]["title"], ctx[lead], mt))
        cols.append(f'<section class="col-lead" id="{lead}" data-spy>{body}</section>')
    cols.append(f'<div class="rail">{ait_card(ctx["ait"]) if ctx.get("ait") else ""}'
                f'<nav class="toc" aria-label="{esc(mt["contents"])}">{kick(mt["contents"])}<ol>{toc}</ol></nav></div>')

    # дальше разделы, у каждого своя вёрстка; Нейроний — в конце во всю ширину
    rest = []
    for s in secs:
        k = s["key"]
        if k in ("news", lead) or not ctx.get(k):
            continue
        if k == "author":
            rest.append(author_sec(s["title"], ctx[k], ctx))
        elif k == "research":
            rest.append(lab_sec(s["title"], ctx[k], mt))
        elif k == "edu":
            rest.append(academy_sec(s["title"], ctx[k], mt))
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Playfair+Display:ital,wght@0,700;0,800;1,500&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">{esc(mt["skip"])}</a>
<header class="top"><div class="wrap top-in">
<a class="brand" href="{esc(ctx.get("home") or "https://dataist.ai/")}" aria-label="{esc(ctx["brand"])} — dataist.ai"><span class="mk" aria-hidden="true">i</span><span class="brand-w">{esc(ctx["brand"])}</span></a>
<nav class="nav" aria-label="{esc(mt["contents"])}">{nav}</nav>
<div class="tools"><span class="chip">{esc(mt["issue_short"].format(n=ctx["n"]))} · {esc(ctx["date_short"])}</span>
<button id="theme" type="button" data-dark="{esc(ctx["to_dark"])}" data-light="{esc(ctx["to_light"])}" aria-label="{esc(ctx["to_dark"])}">
<span class="t-d">{MOON}</span><span class="t-l">{SUN}</span></button></div></div>
<div class="prog" aria-hidden="true"><i></i></div></header>

<main id="main">
<div class="wrap front" id="top">
<div class="iss"><span>{esc(issue)}</span><span>{esc(mt["tagline"])}</span><span>{esc(ctx["date_range"])}</span></div>
<h1 class="mast" aria-label="{esc(ctx["brand"])} — {esc(issue)}">{letters}</h1>
<div class="rule" aria-hidden="true"></div>
{ticker}
<div class="spread">{"".join(cols)}</div>
</div>
<section class="wrap"><div class="letter"><div class="rv"><div class="k">{esc(mt["letter"])}</div>
<div class="sig"><img src="{esc(ctx["avatar"])}" alt="" width="52" height="52"><div><b>{esc(ctx["sign"])}</b><span>{esc(ctx["sign_role"])}</span></div></div></div>
<p class="lt-p rv">{esc(ctx["hello"])}</p></div></section>
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

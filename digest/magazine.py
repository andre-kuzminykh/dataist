"""Веб-версия выпуска Датаиста — цифровой журнал на весь экран.

render(ctx) → HTML-страница. Материалы те же, что в письме; их собирает build.py:
  слева — топ новостей, в центре — видеожурнал с плеером прямо на странице, справа — реклама ИИ-трансформации,
  ниже — авторский канал, исследования, обучение и большой блок Нейрония; анимации при прокрутке.
"""
import html
import re

MT = {
    "ru": {
        "tagline": "Еженедельный журнал об ИИ", "contents": "В этом выпуске", "letter": "От автора",
        "nav": {"news": "Новости", "video": "Видео", "author": "Канал", "research": "Исследования", "edu": "Обучение"},
        "ticker": "Главное за неделю", "now": "Смотрите в выпуске", "play": "Смотреть видео", "top": "Наверх ↑",
        "skip": "Перейти к содержанию", "made": "Создано в", "issue": "Выпуск № {n}", "issue_short": "№ {n}",
    },
    "en": {
        "tagline": "The weekly AI magazine", "contents": "In this issue", "letter": "From the author",
        "nav": {"news": "News", "video": "Video", "author": "Channel", "research": "Research", "edu": "Learning"},
        "ticker": "This week", "now": "Watch in this issue", "play": "Watch the video", "top": "Back to top ↑",
        "skip": "Skip to content", "made": "Made in", "issue": "Issue No. {n}", "issue_short": "No. {n}",
    },
}

SUN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
       '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2'
       'M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>')
MOON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>')
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>'


def esc(s):
    return html.escape(str(s), quote=True)


def nobr(s):
    """«ИИ-операционная» не рвётся по дефису."""
    return re.sub(r"(?<![\w-])((?:ИИ|AI)-[\w-]+)", r'<span class="nb">\1</span>', esc(s))


# ───────────────────────── блоки ─────────────────────────
def sec_head(num, title, count="", label="", url="", small=False):
    link = f'<a class="sh-l" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>' if label and url else ""
    return (f'<div class="sh{" sh-s" if small else ""} rv"><span class="sh-n">{num}</span>'
            f'<h2 class="sh-t">{esc(title)}</h2>{f"<span class=sh-c>{esc(count)}</span>" if count else ""}{link}</div>')


def media(url, img, alt="", cls="media", ratio="16/9"):
    if not img:
        return ""
    return (f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener" style="aspect-ratio:{ratio}" tabindex="-1">'
            f'<img src="{esc(img)}" alt="{esc(alt)}" loading="lazy" decoding="async"></a>')


def paras(ps, cls="p"):
    return "".join(f'<p class="{cls}">{esc(p)}</p>' for p in ps)


def cta(url, label):
    return f'<a class="cta" href="{esc(url)}" target="_blank" rel="noopener"><span>{esc(label)}</span></a>'


def news_rail(news, mt):
    items = news["items"]
    out = []
    for i, x in enumerate(items):
        if i == 0:
            out.append(f'''<li class="nw nw-lead rv">
{media(x["url"], x.get("img_l") or x.get("img"), x["title"], "media nw-img", "3/2")}
<a class="nw-a" href="{esc(x["url"])}" target="_blank" rel="noopener"><span class="nw-n">01</span><span class="nw-t">{esc(x["title"])}</span></a></li>''')
        else:
            thumb = (f'<img class="nw-th" src="{esc(x["img"])}" alt="" loading="lazy" decoding="async">' if x.get("img") else "")
            out.append(f'''<li class="nw rv"><a class="nw-a" href="{esc(x["url"])}" target="_blank" rel="noopener">
<span class="nw-n">{i + 1:02d}</span><span class="nw-t">{esc(x["title"])}</span>{thumb}</a></li>''')
    more = (f'<a class="more rv" href="{esc(news["more"][1])}" target="_blank" rel="noopener">{esc(news["more"][0])}</a>'
            if news.get("more") else "")
    return f'<ol class="nws">{"".join(out)}</ol>{more}'


def video_block(videos, embed, mt):
    v0 = videos[0]
    if embed:
        stage = (f'<button class="ph" type="button" data-id="{esc(v0["id"])}" aria-label="{esc(mt["play"])}: {esc(v0["title"])}">'
                 f'<img src="{esc(v0["cover"])}" alt="" decoding="async"><span class="pb">{PLAY}</span></button>')
    else:
        stage = (f'<a class="ph" href="{esc(v0["url"])}" target="_blank" rel="noopener" aria-label="{esc(mt["play"])}: {esc(v0["title"])}">'
                 f'<img src="{esc(v0["cover"])}" alt="" decoding="async"><span class="pb">{PLAY}</span></a>')
    pl = "".join(
        f'''<li{' class="on"' if i == 0 else ''}><a href="{esc(v["url"])}" target="_blank" rel="noopener" data-id="{esc(v["id"])}"
 data-title="{esc(v["title"])}" data-text="{esc(v["text"])}" data-url="{esc(v["url"])}">
<span class="pl-m"><img src="{esc(v["cover"])}" alt="" loading="lazy" decoding="async"><span class="pl-pb">{PLAY}</span></span>
<span class="pl-n">{i + 1:02d}</span><span class="pl-t">{esc(v["title"])}</span></a></li>''' for i, v in enumerate(videos))
    return f'''<div class="player rv" data-embed="{1 if embed else 0}">{stage}</div>
<div class="now rv"><a class="now-t" href="{esc(v0["url"])}" target="_blank" rel="noopener">{esc(v0["title"])}</a>
<p class="now-p">{esc(v0["text"])}</p></div>
{f'<ol class="pl rv">{pl}</ol>' if len(videos) > 1 else ''}'''


def lead_list(items):
    """Центральная колонка без видео: первый материал крупно, остальные — строками."""
    a, rest = items[0], items[1:]
    out = [f'''<article class="lead rv">{media(a["url"], a.get("img"), a["title"])}
<h3 class="lead-t"><a href="{esc(a["url"])}" target="_blank" rel="noopener">{esc(a["title"])}</a></h3>{paras(a["paras"])}{cta(a["url"], a["cta"])}</article>''']
    for x in rest:
        out.append(f'''<article class="row rv">{media(x["url"], x.get("img"), x["title"], "media row-m")}
<div><h3 class="row-t"><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["title"])}</a></h3>
{paras(x["paras"][:1], "p p-clamp")}{cta(x["url"], x["cta"])}</div></article>''')
    return "".join(out)


def feature(items):
    """Разворот: главный материал слева, остальные столбиком справа."""
    a, rest = items[0], items[1:]
    side = "".join(f'''<article class="mini rv">{media(x["url"], x.get("img"), x["title"])}
<h3 class="mini-t"><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["title"])}</a></h3>
{paras(x["paras"][:2], "p p-clamp")}{cta(x["url"], x["cta"])}</article>''' for x in rest)
    return f'''<div class="feat"><article class="big rv">{media(a["url"], a.get("img"), a["title"])}
<h3 class="big-t"><a href="{esc(a["url"])}" target="_blank" rel="noopener">{esc(a["title"])}</a></h3>
<div class="big-p">{paras(a["paras"])}</div>{cta(a["url"], a["cta"])}</article>
{f'<div class="side">{side}</div>' if side else ''}</div>'''


def grid(items, cols=3):
    cards = "".join(f'''<article class="card rv">{media(x["url"], x.get("img"), x["title"])}
<div class="card-b"><span class="card-n">{i + 1:02d}</span>
<h3 class="card-t"><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["title"])}</a></h3>
{paras(x["paras"][:2], "p p-clamp")}{cta(x["url"], x["cta"])}</div></article>''' for i, x in enumerate(items))
    return f'<div class="grid g{cols}">{cards}</div>'


def rail_list(items):
    """Правая колонка разворота: материалы столбиком — обложка, номер, заголовок."""
    return "".join(f'''<article class="rl rv">{media(x["url"], x.get("img"), x["title"])}
<div class="rl-b"><span class="card-n">{i + 1:02d}</span>
<h3 class="rl-t"><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["title"])}</a></h3>
{paras(x["paras"][:1], "p p-clamp p-sm")}</div></article>''' for i, x in enumerate(items))


def ad_video(ad, cls):
    return (f'<a class="{cls}" href="{esc(ad["url"])}" target="_blank" rel="noopener" tabindex="-1">'
            f'<video class="ad-video" src="{esc(ad["mp4"])}" poster="{esc(ad["poster"])}" muted loop playsinline preload="metadata" '
            f'autoplay aria-label="{esc(ad["title"])}"></video></a>')


def ait_band(ad):
    stats = "".join(f'<div class="st"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in ad.get("stats") or [])
    return f'''<section class="band band-ait" aria-label="{esc(ad["kicker"])}"><div class="glow" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="wrap band-in band-rev"><div class="band-b rv"><div class="ad-k">{esc(ad["kicker"])}</div>
<h2 class="band-t">{nobr(ad["title"])}</h2><p class="band-p">{nobr(ad["text"])}</p>
{f'<div class="sts">{stats}</div>' if stats else ''}
<a class="pill" href="{esc(ad["url"])}" target="_blank" rel="noopener">{esc(ad["cta"])}</a></div>
{ad_video(ad, "band-m rv")}</div></section>'''


def ad_duo(ait, nr):
    """Обе рекламы рядом — если между ними нет разделов."""
    def one(ad, tile):
        return f'''<article class="duo-c rv">{ad_video(ad, "duo-m")}<div class="duo-b">
<div class="ad-k">{'<span class="nr">Nr</span>' if tile else ''}{esc(ad["kicker"])}</div>
<h3 class="duo-t">{nobr(ad["title"])}</h3><p class="band-p">{nobr(ad["text"])}</p>
<a class="pill" href="{esc(ad["url"])}" target="_blank" rel="noopener">{esc(ad["cta"])}</a></div></article>'''
    return f'<section class="duo"><div class="wrap duo-in">{one(ait, False)}{one(nr, True)}</div></section>'


def nr_band(ad):
    return f'''<section class="band" aria-label="{esc(ad["kicker"])}"><div class="glow" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="wrap band-in">{ad_video(ad, "band-m rv")}
<div class="band-b rv"><div class="ad-k"><span class="nr">Nr</span>{esc(ad["kicker"])}</div>
<h2 class="band-t">{nobr(ad["title"])}</h2><p class="band-p">{nobr(ad["text"])}</p>
<a class="pill" href="{esc(ad["url"])}" target="_blank" rel="noopener">{esc(ad["cta"])}</a></div></div></section>'''


# ───────────────────────── страница ─────────────────────────
CSS = r"""
:root{--bg:#fff;--ink:#0a0a0a;--text:#1d1d1f;--body:#3a3a3c;--muted:#6e6e73;--dim:#a1a1a6;--line:#e5e5ea;--soft:#f5f5f7;
  --adbg:#050505;--adline:transparent;--hdr:rgba(255,255,255,.82);--ghost:#ededf0;
  --sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  --mono:'Space Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace;
  --gut:clamp(16px,3.2vw,48px);--max:1480px;--ease:cubic-bezier(.2,.8,.2,1);--top:64px}
html[data-theme="dark"]{--bg:#0a0a0b;--ink:#f5f5f7;--text:#ececf0;--body:#c7c7cc;--muted:#8e8e93;--dim:#636366;--line:#2a2a2d;
  --soft:#161618;--adbg:#000;--adline:#232326;--hdr:rgba(10,10,11,.8);--ghost:#18181a;color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:calc(var(--top) + 16px);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:400 16px/1.6 var(--sans);-webkit-font-smoothing:antialiased;
  transition:background-color .5s var(--ease),color .5s var(--ease)}
a{color:inherit;text-decoration:none}
img,video{display:block;max-width:100%}
button{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--ink);outline-offset:3px;border-radius:4px}
.nb{white-space:nowrap}
.wrap{max-width:var(--max);margin:0 auto;padding:0 var(--gut)}
.skip{position:absolute;left:-9999px;top:8px;z-index:100;background:var(--ink);color:var(--bg);padding:10px 16px;border-radius:999px;
  font:700 12px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase}
.skip:focus{left:16px}
.mono{font-family:var(--mono);text-transform:uppercase;letter-spacing:.16em}

/* шапка */
.top{position:sticky;top:0;z-index:50;background:var(--hdr);-webkit-backdrop-filter:saturate(180%) blur(16px);backdrop-filter:saturate(180%) blur(16px);
  border-bottom:1px solid transparent;transition:border-color .4s var(--ease),background-color .5s var(--ease)}
.top.scrolled{border-bottom-color:var(--line)}
.top-in{height:var(--top);display:flex;align-items:center;gap:24px}
.brand{display:flex;align-items:center;gap:10px;font:800 19px/1 var(--sans);letter-spacing:-.04em;color:var(--ink);flex:none;
  opacity:0;transform:translateY(-6px);transition:opacity .5s var(--ease),transform .5s var(--ease)}
.top.scrolled .brand,.top:focus-within .brand{opacity:1;transform:none}
.mk{width:28px;height:28px;border-radius:50%;background:var(--ink);color:var(--bg);display:grid;place-items:center;font:700 13px/1 var(--mono);letter-spacing:0}
.nav{display:flex;gap:4px;margin:0 auto;overflow-x:auto;scrollbar-width:none}
.nav::-webkit-scrollbar{display:none}
.nav a{font:700 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding:10px 12px;border-radius:999px;
  white-space:nowrap;transition:color .25s,background-color .25s}
.nav a:hover{color:var(--ink)}
.nav a.on{color:var(--bg);background:var(--ink)}
.tools{display:flex;align-items:center;gap:14px;flex:none}
.chip{font:700 10px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--muted);white-space:nowrap}
#theme{all:unset;cursor:pointer;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;color:var(--muted);
  transition:color .2s,background-color .2s}
#theme:hover{color:var(--ink);background:var(--soft)}
#theme:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
#theme svg{width:18px;height:18px}
#theme .t-l{display:none}
html[data-theme="dark"] #theme .t-d{display:none}
html[data-theme="dark"] #theme .t-l{display:block}
.prog{position:absolute;left:0;right:0;bottom:-1px;height:2px;pointer-events:none}
.prog i{display:block;height:100%;background:var(--ink);transform-origin:0 50%;transform:scaleX(0)}

/* обложка выпуска */
.strip{display:flex;justify-content:space-between;gap:16px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);padding:10px 0;
  font:700 11px/1.3 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--ink);margin-top:20px}
.mast{display:flex;justify-content:space-between;margin:clamp(14px,2.4vw,34px) 0 0;font:800 min(15.4vw,232px)/.8 var(--sans);
  letter-spacing:-.04em;color:var(--ink);overflow:hidden;padding-bottom:.04em}
.mast span{display:block}
html.js .mast span{transform:translateY(104%);transition:transform 1.1s var(--ease);transition-delay:calc(var(--i) * 70ms + 100ms)}
html.js.ready .mast span{transform:none}
.rule{height:7px;border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);margin-top:clamp(14px,2vw,26px);transform-origin:0 50%}
html.js .rule{transform:scaleX(0);transition:transform 1.3s var(--ease) .45s}
html.js.ready .rule{transform:none}
.ticker{overflow:hidden;background:var(--ink);color:var(--bg);margin-top:18px;border-radius:999px;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
.tk{display:flex;width:max-content;animation:tk 70s linear infinite}
.ticker:hover .tk{animation-play-state:paused}
.tk span{display:flex;align-items:center;gap:18px;padding:12px 0 12px 18px;font:700 11px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;white-space:nowrap}
.tk a:hover{text-decoration:underline;text-underline-offset:3px}
.tk b{color:var(--dim);font-weight:700}
@keyframes tk{to{transform:translateX(-50%)}}
.intro{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(28px,5vw,96px);padding:clamp(36px,5vw,72px) 0 clamp(20px,3vw,40px)}
.k{font:700 11px/1.3 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.lt-p{margin:16px 0 0;font:500 clamp(21px,2.2vw,32px)/1.36 var(--sans);letter-spacing:-.02em;color:var(--ink);text-wrap:pretty}
.sig{display:flex;align-items:center;gap:14px;margin-top:26px}
.sig img{width:52px;height:52px;border-radius:50%;object-fit:cover}
.sig b{display:block;font:700 15px/1.3 var(--sans);color:var(--ink)}
.sig span{font:700 10px/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.toc ol{list-style:none;margin:14px 0 0;padding:0}
.toc a{display:grid;grid-template-columns:44px 1fr auto;align-items:baseline;gap:12px;padding:15px 0;border-top:1px solid var(--line);
  transition:padding .35s var(--ease),color .2s}
.toc li:last-child a{border-bottom:1px solid var(--line)}
.toc a:hover{padding-left:10px}
.toc-n{font:700 12px/1 var(--mono);color:var(--muted)}
.toc-t{font:800 clamp(20px,1.8vw,26px)/1.1 var(--sans);letter-spacing:-.03em;color:var(--ink)}
.toc-c{font:700 10px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}

/* заголовки разделов */
.sh{display:flex;align-items:baseline;flex-wrap:wrap;gap:6px 14px;border-top:2px solid var(--ink);padding-top:14px;margin-bottom:24px}
.sh-n{font:700 12px/1 var(--mono);letter-spacing:.12em;color:var(--ink)}
.sh-t{margin:0;font:800 clamp(30px,3.4vw,54px)/1 var(--sans);letter-spacing:-.045em;color:var(--ink)}
.sh-c{font:700 10px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.sh-l{margin-left:auto;font:700 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink);
  background:linear-gradient(currentColor,currentColor) 0 100%/0 1px no-repeat;padding-bottom:4px;transition:background-size .4s var(--ease)}
.sh-l:hover{background-size:100% 1px}
.sh-s .sh-t{font-size:clamp(24px,2vw,30px)}
.sec{padding-top:clamp(56px,7vw,112px)}

/* общие элементы */
.media{display:block;position:relative;overflow:hidden;border-radius:clamp(12px,1.2vw,18px);background:var(--soft)}
.media img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}
.media:hover img,article:hover>.media img{transform:scale(1.04)}
html.js .rv .media,html.js .media.rv{clip-path:inset(0 0 100% 0 round 16px);transition:clip-path 1.2s var(--ease) var(--d,0s)}
html.js .rv.in .media,html.js .media.rv.in{clip-path:inset(0 0 0 0 round 0)}
.p{margin:12px 0 0;font:400 16px/1.62 var(--sans);color:var(--body);text-wrap:pretty}
.p-clamp{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.cta{display:inline-block;margin-top:18px;font:700 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink);
  padding-bottom:5px;background:linear-gradient(currentColor,currentColor) 0 100%/100% 1px no-repeat;transition:background-size .45s var(--ease)}
.cta:hover{background-size:0 1px;background-position:100% 100%}
h3 a{background:linear-gradient(currentColor,currentColor) 0 100%/0 2px no-repeat;transition:background-size .5s var(--ease)}
h3 a:hover{background-size:100% 2px}
.pill{display:inline-flex;align-items:center;gap:8px;background:#fff;color:#000;font:700 15px/1 var(--sans);padding:16px 24px;border-radius:999px;
  transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
.pill:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(160,113,255,.35)}

/* появление при прокрутке */
html.js .rv{opacity:0;transform:translateY(26px);transition:opacity .9s var(--ease) var(--d,0s),transform .9s var(--ease) var(--d,0s)}
html.js .rv.in{opacity:1;transform:none}

/* первый разворот: новости | видео | реклама */
.spread{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,6fr) minmax(0,3fr);gap:0;padding-top:clamp(32px,4vw,64px)}
.col{padding:0 clamp(20px,2.2vw,40px)}
.spread-2{grid-template-columns:minmax(0,4fr) minmax(0,8fr)}
.spread-1{grid-template-columns:1fr}
.col:first-child{padding-left:0}
.col:last-child{padding-right:0}
.col+.col{border-left:1px solid var(--line)}
.stick{position:sticky;top:calc(var(--top) + 24px)}
.nws{list-style:none;margin:0;padding:0;counter-reset:n}
.nw-a{display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:12px;align-items:start;padding:16px 0;border-top:1px solid var(--line)}
.nw-lead .nw-a{grid-template-columns:30px minmax(0,1fr);border-top:0;padding-top:14px}
.nw-n{font:700 12px/1.9 var(--mono);color:var(--muted);transition:color .25s}
.nw-t{font:700 15px/1.38 var(--sans);letter-spacing:-.01em;color:var(--ink)}
.nw-lead .nw-t{font:800 clamp(19px,1.5vw,23px)/1.2 var(--sans);letter-spacing:-.025em}
.nw-th{width:64px;height:48px;object-fit:cover;border-radius:8px;transition:transform .5s var(--ease)}
.nw-a:hover .nw-n{color:var(--ink)}
.nw-a:hover .nw-th{transform:scale(1.06)}
.nw-a:hover .nw-t{text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.more{display:block;text-align:right;padding-top:16px;border-top:1px solid var(--line);font:700 11px/1 var(--mono);letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink)}
.more:hover{text-decoration:underline;text-underline-offset:4px}

.player{position:relative;aspect-ratio:16/9;border-radius:clamp(14px,1.4vw,20px);overflow:hidden;background:#000}
.player iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.ph{all:unset;cursor:pointer;position:absolute;inset:0;display:block}
.ph img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease),filter .6s}
.ph:hover img{transform:scale(1.03);filter:brightness(.9)}
.pb{position:absolute;left:50%;top:50%;width:clamp(64px,7vw,96px);height:clamp(64px,7vw,96px);margin:calc(clamp(64px,7vw,96px) / -2) 0 0 calc(clamp(64px,7vw,96px) / -2);
  border-radius:50%;background:rgba(255,255,255,.94);color:#0a0a0a;display:grid;place-items:center;box-shadow:0 18px 50px rgba(0,0,0,.35);
  transition:transform .45s var(--ease)}
.pb svg{width:38%;height:38%;margin-left:6%}
.pb::after{content:"";position:absolute;inset:-10px;border-radius:50%;border:1px solid rgba(255,255,255,.7);animation:pulse 2.4s var(--ease) infinite}
@keyframes pulse{from{transform:scale(.9);opacity:1}to{transform:scale(1.35);opacity:0}}
.ph:hover .pb{transform:scale(1.08)}
.ph:focus-visible{outline:3px solid #fff;outline-offset:-6px}
.now{padding-top:22px;transition:opacity .35s var(--ease)}
.now.swap{opacity:0}
.now-t{display:block;font:800 clamp(24px,2.3vw,36px)/1.12 var(--sans);letter-spacing:-.035em;color:var(--ink);text-wrap:balance}
.now-t:hover{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:5px}
.now-p{margin:14px 0 0;font:400 17px/1.62 var(--sans);color:var(--body);max-width:70ch;text-wrap:pretty}
.pl{list-style:none;margin:28px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.pl a{display:block}
.pl-m{position:relative;display:block;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:#000}
.pl-m img{width:100%;height:100%;object-fit:cover;transition:transform .8s var(--ease),opacity .3s}
.pl a:hover .pl-m img{transform:scale(1.05)}
.pl-pb{position:absolute;left:10px;bottom:10px;width:30px;height:30px;border-radius:50%;background:rgba(255,255,255,.92);color:#0a0a0a;display:grid;place-items:center}
.pl-pb svg{width:14px;height:14px;margin-left:2px}
.pl-n{display:block;margin-top:10px;font:700 11px/1 var(--mono);letter-spacing:.12em;color:var(--muted)}
.pl-t{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;margin-top:6px;font:700 14px/1.35 var(--sans);color:var(--ink)}
.pl li.on .pl-m{outline:2px solid var(--ink);outline-offset:3px}
.pl li.on .pl-n::after{content:"  ●";color:#ff3b30}

/* правая колонка разворота */
.rl+.rl{margin-top:26px;padding-top:26px;border-top:1px solid var(--line)}
.rl-b{padding-top:14px}
.rl-t{margin:6px 0 0;font:800 18px/1.22 var(--sans);letter-spacing:-.02em;color:var(--ink);text-wrap:balance}
.p-sm{font-size:14px;line-height:1.55;-webkit-line-clamp:3}
/* реклама */
.ad{background:var(--adbg);color:#fff;border-radius:clamp(16px,1.6vw,24px);overflow:hidden;border:1px solid var(--adline)}
.ad-m{display:block;padding:8px 8px 0}
.ad-m video,.band-m video{width:100%;height:auto;aspect-ratio:16/9;border-radius:14px;background:#000}
.ad-b{padding:20px 22px 24px}
.ad-k{display:flex;align-items:center;gap:10px;font:700 10px/1.3 var(--mono);letter-spacing:.2em;text-transform:uppercase;color:#a1a1a6}
.ad-t{margin:12px 0 0;font:800 clamp(21px,1.6vw,26px)/1.14 var(--sans);letter-spacing:-.03em;color:#fff}
.ad-p{margin:10px 0 0;font:400 14px/1.55 var(--sans);color:#c7c7cc}
.sts{display:flex;gap:18px;margin-top:16px;flex-wrap:wrap}
.st b{display:block;font:800 19px/1.1 var(--sans);letter-spacing:-.03em;color:#fff;white-space:nowrap}
.st span{font:400 10px/1.4 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:#8e8e93}
.ad .pill{margin-top:20px;font-size:14px;padding:14px 20px}

/* разворот, сетки */
.feat{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(28px,3.4vw,64px)}
.big-t{margin:22px 0 0;font:800 clamp(28px,2.8vw,44px)/1.08 var(--sans);letter-spacing:-.04em;color:var(--ink);text-wrap:balance}
.big-p .p{font-size:17px}
.side{display:grid;gap:clamp(28px,3vw,44px);align-content:start}
.mini{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:20px;align-items:start}
.mini .cta,.mini .p{grid-column:2}
.mini-t{grid-column:2;margin:0;font:800 clamp(18px,1.4vw,22px)/1.2 var(--sans);letter-spacing:-.025em;color:var(--ink)}
.mini>.media{grid-row:span 3}
.mini .p{margin-top:8px;font-size:15px}
.mini .cta{margin-top:12px}
.grid{display:grid;gap:clamp(24px,2.4vw,40px)}
.g3{grid-template-columns:repeat(3,minmax(0,1fr))}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}
.card-b{padding-top:18px}
.card-n{font:700 11px/1 var(--mono);letter-spacing:.12em;color:var(--muted)}
.card-t{margin:8px 0 0;font:800 clamp(20px,1.6vw,25px)/1.16 var(--sans);letter-spacing:-.03em;color:var(--ink);text-wrap:balance}
.lead-t{margin:20px 0 0;font:800 clamp(26px,2.4vw,38px)/1.1 var(--sans);letter-spacing:-.035em;color:var(--ink)}
.row{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:20px;padding-top:24px;margin-top:24px;border-top:1px solid var(--line)}
.row-t{margin:0;font:800 19px/1.2 var(--sans);letter-spacing:-.02em;color:var(--ink)}
.row .p{font-size:15px;margin-top:8px}

/* Нейроний — во всю ширину */
.band{position:relative;overflow:hidden;background:#07060a;color:#fff;margin-top:clamp(64px,8vw,128px);padding:clamp(48px,6vw,96px) 0}
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
.band-t{margin:18px 0 0;font:800 clamp(30px,3.6vw,56px)/1.04 var(--sans);letter-spacing:-.045em;text-wrap:balance}
.band-p{margin:18px 0 0;font:400 17px/1.6 var(--sans);color:rgba(255,255,255,.78);max-width:46ch}
.band .pill{margin-top:28px}
.band .sts{margin-top:24px;gap:28px}
.band .st b{font-size:24px}
.band-ait{background:#060606}
.band-ait .glow{opacity:.5}
.band-ait .glow i:nth-child(1){background:#7c4dff;left:44%;top:4%}
.band-ait .glow i:nth-child(2){background:#ff8a33;left:70%;top:46%;opacity:.7}
.band-ait .glow i:nth-child(3){background:#3b1d8f;left:-4%;top:40%}
.band-ait::after{background:linear-gradient(90deg,rgba(6,6,6,.75),rgba(6,6,6,.2))}
.band-rev{grid-template-columns:minmax(0,5fr) minmax(0,7fr)}
.band-ait .pill:hover{box-shadow:0 12px 30px rgba(255,138,51,.35)}
.band+.band{margin-top:0}
.duo{margin-top:clamp(64px,8vw,128px)}
.duo-in{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(20px,2.4vw,40px)}
.duo-c{background:#060606;color:#fff;border-radius:clamp(18px,1.8vw,28px);overflow:hidden;border:1px solid var(--adline)}
.duo-m{display:block;padding:10px 10px 0}
.duo-m video{width:100%;height:auto;aspect-ratio:16/9;border-radius:16px;background:#000}
.duo-b{padding:24px 28px 30px}
.duo-t{margin:14px 0 0;font:800 clamp(24px,2.2vw,34px)/1.08 var(--sans);letter-spacing:-.035em}

/* подвал */
.ft{padding:clamp(64px,8vw,120px) 0 40px}
.ft-mark{display:flex;justify-content:space-between;font:800 min(15.4vw,232px)/.8 var(--sans);letter-spacing:-.04em;color:var(--ghost);
  padding-bottom:.04em;user-select:none;transition:color .5s var(--ease)}
.ft-row{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px 28px;border-top:1px solid var(--ink);
  margin-top:clamp(18px,2vw,28px);padding-top:18px;font:700 11px/1.4 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}
.soc{display:flex;flex-wrap:wrap;gap:8px 22px}
.soc a,.up{background:linear-gradient(currentColor,currentColor) 0 100%/0 1px no-repeat;padding-bottom:3px;transition:background-size .4s var(--ease)}
.soc a:hover,.up:hover{background-size:100% 1px}
.made{display:inline-flex;align-items:center;gap:8px;color:var(--muted)}
.made b{color:var(--ink)}
.made .nr{width:22px;height:22px;font-size:11px;border-color:var(--dim);color:var(--ink);border-radius:5px;letter-spacing:-.05em;text-transform:none}

/* адаптивность */
@media (max-width:1180px){
  .spread{grid-template-columns:minmax(0,4fr) minmax(0,8fr)}
  .col:nth-child(2){padding-right:0}
  .col.rail{grid-column:1/-1;border-left:0;padding:clamp(40px,5vw,64px) 0 0}
  .rail .stick{position:static}
  .rail .stick{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0 clamp(20px,2.4vw,36px)}
  .rail .sh{grid-column:1/-1}
  .rl+.rl{margin-top:0;padding-top:0;border-top:0}
  .g3{grid-template-columns:repeat(2,minmax(0,1fr))}
  .chip{display:none}
}
@media (max-width:860px){
  :root{--top:56px}
  .top-in{gap:12px}
  .brand{opacity:1;transform:none;font-size:17px}
  .nav{margin:0;flex:1;justify-content:flex-start;-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}
  .nav a{padding:9px 10px;font-size:10px}
  .strip span:nth-child(2){display:none}
  .intro,.feat,.band-in,.band-rev{grid-template-columns:1fr}
  .band-rev .band-m{order:-1}
  .spread{grid-template-columns:1fr}
  .col{padding:0!important;border-left:0!important}
  .col+.col{padding-top:clamp(48px,10vw,64px)!important}
  .stick{position:static}
  .rail .stick{display:block}
  .rl+.rl{margin-top:26px;padding-top:26px;border-top:1px solid var(--line)}
  .duo-in{grid-template-columns:1fr}
  .pl{grid-template-columns:repeat(3,minmax(140px,1fr));overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:6px}
  .pl li{scroll-snap-align:start}
  .g3,.g2{grid-template-columns:1fr}
  .mini{grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:14px}
  .mini .p{display:none}
  .row{grid-template-columns:minmax(0,2fr) minmax(0,3fr)}
  .row .p{display:none}
  .sh-l{margin-left:0;flex-basis:100%}
  .ft-row{flex-direction:column;align-items:flex-start}
}
@media (max-width:480px){
  .chip,.nav{display:none}
  .tools{margin-left:auto}
  .pl{grid-template-columns:repeat(3,72%)}
  .now-p,.big-p .p{font-size:16px}
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
var top=document.querySelector('.top'),bar=document.querySelector('.prog i'),first=document.querySelector('[data-spy]'),ticking=false;
function onScroll(){ticking=false;var y=window.scrollY||0,h=d.scrollHeight-innerHeight;top.classList.toggle('scrolled',y>40);
  bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';
  if(first&&first.getBoundingClientRect().top>innerHeight*0.45)document.querySelectorAll('.nav a.on').forEach(function(a){a.classList.remove('on')});}
addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll)}},{passive:true});onScroll();
if(!('IntersectionObserver' in window)){d.classList.remove('js');return;}
var io=new IntersectionObserver(function(es){var k=0;es.forEach(function(e){if(e.isIntersecting){
  e.target.style.setProperty('--d',Math.min(k++,6)*0.08+'s');e.target.classList.add('in');io.unobserve(e.target);}});},
  {rootMargin:'0px 0px -7% 0px',threshold:0.06});
document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
var links={};document.querySelectorAll('.nav a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
var spy=new IntersectionObserver(function(es){es.forEach(function(e){var a=links[e.target.id];if(a&&e.isIntersecting){
  for(var k in links)links[k].classList.remove('on');a.classList.add('on');
  if(a.scrollIntoView&&a.parentNode.scrollWidth>a.parentNode.clientWidth)a.parentNode.scrollTo({left:a.offsetLeft-24,behavior:reduce?'auto':'smooth'});}});},
  {rootMargin:'-40% 0px -55% 0px'});
document.querySelectorAll('[data-spy]').forEach(function(s){spy.observe(s)});
var vs=document.querySelectorAll('video.ad-video');
if(reduce)vs.forEach(function(v){v.removeAttribute('autoplay');v.pause()});
else{var seen=[];var vo=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;
  if(e.isIntersecting){if(seen.indexOf(v)<0){seen.push(v);try{v.currentTime=0}catch(x){}}var p=v.play();if(p&&p.catch)p.catch(function(){});}
  else v.pause();});},{threshold:0.35});vs.forEach(function(v){vo.observe(v)});}
var player=document.querySelector('.player');
if(player&&player.getAttribute('data-embed')==='1'){
  var now=document.querySelector('.now'),nt=document.querySelector('.now-t'),np=document.querySelector('.now-p');
  var play=function(id,title){var f=document.createElement('iframe');
    f.src='https://www.youtube.com/embed/'+id+'?autoplay=1&rel=0&modestbranding=1&playsinline=1';f.title=title||'';
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.referrerPolicy='strict-origin-when-cross-origin';f.allowFullscreen=true;player.innerHTML='';player.appendChild(f);};
  player.addEventListener('click',function(e){var b=e.target.closest('.ph');if(!b)return;e.preventDefault();play(b.getAttribute('data-id'),nt.textContent);});
  document.querySelectorAll('.pl a[data-id]').forEach(function(a){a.addEventListener('click',function(e){
    if(e.metaKey||e.ctrlKey||e.shiftKey)return;e.preventDefault();
    document.querySelectorAll('.pl li').forEach(function(li){li.classList.remove('on')});a.parentNode.classList.add('on');
    now.classList.add('swap');setTimeout(function(){nt.textContent=a.getAttribute('data-title');nt.href=a.getAttribute('data-url');
      np.textContent=a.getAttribute('data-text');now.classList.remove('swap');},reduce?0:220);
    play(a.getAttribute('data-id'),a.getAttribute('data-title'));
    var r=player.getBoundingClientRect();if(r.top<60||r.bottom>innerHeight)player.scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});});});
}
})();
"""


def render(ctx):
    lang, mt = ctx["lang"], MT[ctx["lang"]]
    secs = ctx["sections"]
    num = {s["key"]: f"{i:02d}" for i, s in enumerate(secs, 1)}
    by = {s["key"]: s for s in secs}
    lead = "video" if "video" in by else ("author" if "author" in by else None)

    nav = "".join(f'<a href="#{s["key"]}">{esc(mt["nav"][s["key"]])}</a>' for s in secs)
    toc = "".join(f'<li><a href="#{s["key"]}"><span class="toc-n">{num[s["key"]]}</span><span class="toc-t">{esc(s["title"])}</span>'
                  f'<span class="toc-c">{esc(s["count"])}</span></a></li>' for s in secs)
    letters = "".join(f'<span style="--i:{i}" aria-hidden="true">{esc(c)}</span>' for i, c in enumerate(ctx["brand"]))
    foot_letters = "".join(f"<span>{esc(c)}</span>" for c in ctx["brand"])

    news = ctx.get("news") or {}
    tick_items = "".join(f'<a href="{esc(x["url"])}" target="_blank" rel="noopener" tabindex="-1">{esc(x["title"])}</a><b>●</b>'
                         for x in news.get("items", []))
    ticker = (f'<div class="ticker rv" aria-hidden="true"><div class="tk">'
              f'<span><b>{esc(mt["ticker"])}</b><b>●</b>{tick_items}</span><span><b>{esc(mt["ticker"])}</b><b>●</b>{tick_items}</span>'
              f'</div></div>') if tick_items else ""

    # первый разворот: новости | видео (или главный материал) | исследования
    rail = next((k for k in ("research", "edu") if k in by and k != lead), None)
    cols = []
    if "news" in by:
        s = by["news"]
        cols.append(f'<section class="col" id="news" data-spy><div class="stick">{sec_head(num["news"], s["title"], "", s.get("label"), s.get("url"), small=True)}'
                    f'{news_rail(news, mt)}</div></section>')
    if lead:
        s = by[lead]
        body = video_block(ctx["video"], ctx["embed"], mt) if lead == "video" else lead_list(ctx[lead])
        cols.append(f'<section class="col" id="{lead}" data-spy>{sec_head(num[lead], s["title"], s["count"], s.get("label"), s.get("url"))}{body}</section>')
    if rail:
        s = by[rail]
        cols.append(f'<section class="col rail" id="{rail}" data-spy><div class="stick">'
                    f'{sec_head(num[rail], s["title"], "", s.get("label"), s.get("url"), small=True)}{rail_list(ctx[rail])}</div></section>')
    spread = f'<div class="wrap spread spread-{len(cols)}">{"".join(cols)}</div>'

    # остальные разделы; реклама ИИ-трансформации — после «Авторского канала», Нейроний — в конце
    rest_keys = [s["key"] for s in secs if s["key"] not in ("news", lead, rail) and ctx.get(s["key"])]
    ait, nr = ctx.get("ait"), ctx.get("nr")
    rest = []
    if not rest_keys and ait and nr:
        rest.append(ad_duo(ait, nr))
        ait = nr = None
    for k in rest_keys:
        s = by[k]
        items = ctx[k]
        body = feature(items) if k == "author" else grid(items, 2 if k == "edu" else 3)
        rest.append(f'<section class="wrap sec" id="{k}" data-spy>{sec_head(num[k], s["title"], s["count"], s.get("label"), s.get("url"))}{body}</section>')
        if ait and (k == "author" or "author" not in rest_keys):
            rest.append(ait_band(ait))
            ait = None
    if ait:
        rest.append(ait_band(ait))
    if nr:
        rest.append(nr_band(nr))

    socials = "".join(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(n)}</a>' for n, u in ctx["socials"])
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet">
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
<div class="wrap" id="top">
<div class="strip"><span>{esc(mt["issue"].format(n=ctx["n"]))}</span><span>{esc(mt["tagline"])}</span><span>{esc(ctx["date_range"])}</span></div>
<h1 class="mast" aria-label="{esc(ctx["brand"])} — {esc(mt["issue"].format(n=ctx["n"]))}">{letters}</h1>
<div class="rule" aria-hidden="true"></div>
{ticker}
<div class="intro">
<div class="letter rv"><div class="k">{esc(mt["letter"])}</div><p class="lt-p">{esc(ctx["hello"])}</p>
<div class="sig"><img src="{esc(ctx["avatar"])}" alt="" width="52" height="52"><div><b>{esc(ctx["sign"])}</b><span>{esc(ctx["sign_role"])}</span></div></div></div>
<nav class="toc rv" aria-label="{esc(mt["contents"])}"><div class="k">{esc(mt["contents"])}</div><ol>{toc}</ol></nav>
</div></div>

{spread}
{"".join(rest)}
</main>

<footer class="ft"><div class="wrap">
<div class="ft-mark" aria-hidden="true">{foot_letters}</div>
<div class="ft-row"><div class="soc">{socials}</div>
<span>{esc(mt["issue"].format(n=ctx["n"]))} · {esc(ctx["date_long"])}</span>
<span class="made">{esc(mt["made"])} <span class="nr">Nr</span><b>{esc(ctx["made_name"])}</b></span>
<a class="up" href="#top">{esc(mt["top"])}</a></div></div></footer>
<script>{JS}</script>
</body></html>
'''

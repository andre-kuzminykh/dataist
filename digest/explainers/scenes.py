"""Сценарии роликов: по сцене на шаг, тексты — с сайтов andre.technology и neuronium.ai
(у Нейрония сайт на английском — русский текст переведён). Пишет work/cfg-<ролик>.json для render.js.

Чтобы поменять текст: правим здесь и запускаем ./make.sh (или только scenes.py → render.js → кодирование).
hold — сколько секунд сцена стоит после анимации, чтобы успеть дочитать.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
FPS = 24
counts = json.loads((WORK / "frames.json").read_text())["counts"]

GLUE = {"ru": "в во с со к ко и о об у а но по на от до из за не ни для под над без при про".split(),
        "en": "a an the to of in on with for".split()}


def nbsp(html, lang):
    """Неразрывные пробелы: короткие предлоги не висят в конце строки, тире не начинает строку."""
    rx = re.compile(r"(^|[\s>])(" + "|".join(GLUE[lang]) + r") +(?=[^\s<])", re.I)
    out = []
    for p in re.split(r"(<[^>]+>)", html):
        if not p.startswith("<"):
            for _ in range(2):  # «и в работе» — подряд
                p = rx.sub(lambda m: m.group(1) + m.group(2) + " ", p)
            p = re.sub(r" +—", " —", p)
        out.append(p)
    return "".join(out)


def scene(dir_key, hold, lang, **kw):
    n = counts[dir_key]
    for k in ("title", "sub"):
        if kw.get(k):
            kw[k] = nbsp(kw[k], lang)
    return {"dir": f"work/frames/{dir_key}", "frames": n, "dur": round(n / FPS + hold, 3), **kw}


# Только крупные заголовки: подписи-«кикеры», подзаголовки, адреса и кнопки в ролике не читаются —
# кнопка стоит рядом с роликом, на странице.
AIT = {
    "ru": [
        ("change", 0.9, dict(title='От <b class="pv">ИИ-диагностики</b> бизнеса к <b class="go">новой ИИ-компании</b>')),
        ("maturity", 0.9, dict(title='Насколько ваш <b class="go">бизнес</b> <b class="pv">готов к ИИ</b>')),
        ("strategy", 1.0, dict(title='Ваш <b class="go">бизнес</b>, перестроенный под <b class="pv">ИИ</b>')),
        ("neuronium", 0.9, dict(title='<b class="pv">Нейроний</b> — операционная система на базе <b class="go">ИИ</b>')),
        ("training", 0.9, dict(title='Обучаем <b class="go">людей</b>, которых <b class="pv">ИИ</b> не заменит')),
        ("cases", 1.0, dict(title='От <b class="pv">ИИ-стратегии</b> к результатам <b class="go">бизнеса</b>')),
    ],
    "en": [
        ("change", 0.9, dict(title='From an <b class="pv">AI assessment</b> to a <b class="go">new AI company</b>')),
        ("maturity", 0.9, dict(title='How <b class="pv">AI-ready</b> is your <b class="go">business</b>')),
        ("strategy", 1.0, dict(title='Your <b class="go">business</b> redesigned for <b class="pv">AI</b>')),
        ("neuronium", 0.9, dict(title='<b class="pv">Neuronium</b> — AI operating system for your <b class="go">business</b>')),
        ("training", 0.9, dict(title='We train <b class="go">humans</b> <b class="pv">AI</b> can’t replace')),
        ("cases", 1.0, dict(title='From <b class="pv">AI strategy</b> to <b class="go">business</b> results')),
    ],
}

# Вертикальный ролик 720×900 для узкой колонки газеты: сверху — схема сайта крупным планом
# (crop — окно кадра записи 1280×720: x, y, ширина), снизу — только крупный заголовок.
AIT_V_CROP = {"change": [361, 157, 651], "maturity": [541, 262, 499], "strategy": [543, 182, 568],
              "neuronium": [560, 158, 620], "training": [534, 182, 568], "cases": [540, 170, 600]}
AIT_V_CROP_EN = {"maturity": [489, 262, 499], "neuronium": [495, 158, 620]}   # у английской страницы схемы чуть левее
AIT_V = {
    "ru": [
        ("change", 1.2, 'От <b class="pv">ИИ-диагностики</b> к <b class="go">новой ИИ-компании</b>'),
        ("maturity", 1.2, 'Насколько бизнес <b class="pv">готов к ИИ</b>'),
        ("strategy", 1.2, 'Бизнес, перестроенный <b class="pv">под ИИ</b>'),
        ("neuronium", 1.2, '<b class="pv">Нейроний</b> — операционная система на базе ИИ'),
        ("training", 1.2, 'Обучаем людей, которых <b class="pv">ИИ не заменит</b>'),
        ("cases", 1.5, 'От ИИ-стратегии к <b class="go">результатам бизнеса</b>'),
    ],
    "en": [
        ("change", 1.2, 'From <b class="pv">AI assessment</b><br>to <b class="go">a new AI company</b>'),
        ("maturity", 1.2, 'How <b class="pv">AI-ready</b> is your business'),
        ("strategy", 1.2, 'Your business <b class="pv">redesigned for AI</b>'),
        ("neuronium", 1.2, '<b class="pv">Neuronium</b> — AI operating system'),
        ("training", 1.2, 'We train humans<br><b class="pv">AI can’t replace</b>'),
        ("cases", 1.5, 'From AI strategy to <b class="go">business results</b>'),
    ],
}

NR_LAYOUT = {
    "slide-hero": dict(left=60, width=1000, top=362, size=46),
    "slide-context": dict(left=60, width=430),
    "slide-management": dict(left=60, width=440),
    "slide-cases": dict(left=60, width=1000, top=28, size=44, hideLogo=True),
    "gradient": dict(left=60, width=1000, align="center", size=58),
}
NR = {
    "ru": [
        ("slide-hero", 0.5, dict(title='<b>Ведите ИИ-бизнес</b><br><span class="dim">в операционной системе на базе ИИ</span>')),
        ("slide-context", 0.8, dict(title="ИИ-суперагент работает в контексте вашего бизнеса")),
        ("slide-management", 1.0, dict(title="ИИ-управление знаниями")),
        ("slide-cases", 0.6, dict(title="ИИ-суперагент управляет 100 готовыми ИИ-сотрудниками в десяти отделах")),
        ("gradient", 0.8, dict(title="Ведите свой ИИ-бизнес с Нейронием")),
    ],
    "en": [
        ("slide-hero", 0.5, dict(title='<b>Run AI Business</b> <span class="dim">with AI Operating System</span>')),
        ("slide-context", 0.8, dict(title="AI Superagent works in your business context")),
        ("slide-management", 1.0, dict(title="AI Knowledge Management")),
        ("slide-cases", 0.6, dict(title="AI Superagent manages 100 ready AI employees across ten departments")),
        ("gradient", 0.8, dict(title="Run Your AI Business with Neuronium")),
    ],
}


def save(name, cfg):
    (WORK / f"cfg-{name}.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
    print(name, round(sum(s["dur"] for s in cfg["scenes"]), 2), "s")


for lang in ("ru", "en"):
    save(f"ait-{lang}", {"theme": "ait", "fps": FPS, "logo": "ait-logo.png", "scenes": [
        scene(f"at-{lang}/{sid}", hold, lang, layout=dict(left=56, width=500 if sid == "change" else 440), **kw)
        for sid, hold, kw in AIT[lang]]})
    for variant in ("nr", "nrs"):  # nr — живой свет фона (MP4), nrs — неподвижный (GIF)
        save(f"{variant}-{lang}", {"theme": "nr", "fps": FPS, "scenes": [
            scene(f"{variant}/{sid}", hold, lang, layout=NR_LAYOUT[sid], **dict(kw)) for sid, hold, kw in NR[lang]]})
    save(f"ait-vert-{lang}", {"compose": "compose-vertical.html", "size": [720, 900], "fps": FPS, "logo": "ait-logo.png",
                              "scenes": [scene(f"ath-{lang}/{sid}", hold, lang, crop=(lang == "en" and AIT_V_CROP_EN.get(sid)) or AIT_V_CROP[sid], title=title)
                                         for sid, hold, title in AIT_V[lang]]})

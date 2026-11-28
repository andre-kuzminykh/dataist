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


AIT = {
    "ru": [
        ("change", 0.9, dict(kicker="Как проходит ИИ-трансформация",
                             title='От <b class="pv">ИИ-диагностики</b> бизнеса к <b class="go">новой ИИ-компании</b>')),
        ("maturity", 0.9, dict(kicker="01 · Индекс ИИ-зрелости",
                               title='Насколько ваш <b class="go">бизнес</b> <b class="pv">готов к ИИ</b>',
                               sub="Пройдите ИИ-диагностику — бесплатно")),
        ("strategy", 1.0, dict(kicker="02 · Стратегия ИИ-трансформации",
                               title='Ваш <b class="go">бизнес</b>, перестроенный под <b class="pv">ИИ</b>',
                               sub="Составьте план ИИ-трансформации")),
        ("neuronium", 0.9, dict(kicker="03 · Нейроний",
                                title='<b class="pv">ИИ-операционная система</b> для вашего <b class="go">бизнеса</b>',
                                sub="Наймите ИИ-сотрудников")),
        ("training", 0.9, dict(kicker="04 · Консалтинг по внедрению ИИ",
                               title='Обучаем <b class="go">людей</b>, которых <b class="pv">ИИ</b> не заменит',
                               sub="Обучите команду")),
        ("cases", 1.0, dict(kicker="Кейсы ИИ-трансформации",
                            title='От <b class="pv">ИИ-стратегии</b> к результатам <b class="go">бизнеса</b>',
                            cta="Бесплатная ИИ-диагностика →", dom="andre.technology")),
    ],
    "en": [
        ("change", 0.9, dict(kicker="How AI transformation works",
                             title='From an <b class="pv">AI assessment</b> to a <b class="go">new AI company</b>')),
        ("maturity", 0.9, dict(kicker="01 · AI maturity index",
                               title='How <b class="pv">AI-ready</b> is your <b class="go">business</b>',
                               sub="Run an AI assessment — free")),
        ("strategy", 1.0, dict(kicker="02 · AI transformation strategy",
                               title='Your <b class="go">business</b> redesigned for <b class="pv">AI</b>',
                               sub="Build the AI playbook")),
        ("neuronium", 0.9, dict(kicker="03 · Neuronium",
                                title='<b class="pv">AI operating system</b> for your <b class="go">business</b>',
                                sub="Hire AI employees")),
        ("training", 0.9, dict(kicker="04 · Consulting for AI adoption",
                               title='We train <b class="go">humans</b> <b class="pv">AI</b> can’t replace',
                               sub="Train your team")),
        ("cases", 1.0, dict(kicker="AI transformation cases",
                            title='From <b class="pv">AI strategy</b> to <b class="go">business</b> results',
                            cta="Free AI assessment →", dom="andre.technology")),
    ],
}

# Квадратный ролик 720×720 для узкой колонки газеты: сверху — анимация сайта крупным планом
# (crop — окно кадра 1120×630: x, y, ширина), снизу — крупный текст; кнопка — на всех сценах.
AIT_SQ_CROP = {"change": [400, 162, 720], "maturity": [469, 175, 642], "strategy": [434, 160, 642],
               "neuronium": [478, 170, 623], "training": [424, 175, 642], "cases": [500, 198, 540]}
AIT_SQ = {
    "ru": [
        ("change", 1.2, dict(kicker="Как проходит ИИ-трансформация",
                             title='От <b class="pv">ИИ-диагностики</b> к <b class="go">новой ИИ-компании</b>')),
        ("maturity", 1.2, dict(kicker="Шаг 1 · ИИ-диагностика", title='Насколько бизнес <b class="pv">готов к ИИ</b>',
                               sub="Индекс ИИ-зрелости — бесплатно")),
        ("strategy", 1.2, dict(kicker="Шаг 2 · ИИ-стратегия", title='Бизнес, перестроенный <b class="pv">под ИИ</b>',
                               sub="План ИИ-трансформации")),
        ("neuronium", 1.2, dict(kicker="Шаг 3 · Нейроний", title='<b class="pv">Операционная система</b> на базе ИИ',
                                sub="ИИ-суперагент и 100 ИИ-сотрудников")),
        ("training", 1.2, dict(kicker="Шаг 4 · Обучение команды", title='Обучаем людей, которых <b class="pv">ИИ не заменит</b>',
                               sub="3 месяца с ментором")),
        ("cases", 1.5, dict(kicker="Кейсы ИИ-трансформации", title='От ИИ-стратегии к <b class="go">результатам бизнеса</b>')),
    ],
    "en": [
        ("change", 1.2, dict(kicker="How AI transformation works",
                             title='From an <b class="pv">AI assessment</b><br>to <b class="go">a new AI company</b>')),
        ("maturity", 1.2, dict(kicker="Step 1 · AI assessment", title='How <b class="pv">AI-ready</b> is your business',
                               sub="AI maturity index — free")),
        ("strategy", 1.2, dict(kicker="Step 2 · AI strategy", title='Your business <b class="pv">redesigned for AI</b>',
                               sub="AI transformation playbook")),
        ("neuronium", 1.2, dict(kicker="Step 3 · Neuronium", title='<b class="pv">AI operating system</b> for your business',
                                sub="AI Superagent and 100 AI employees")),
        ("training", 1.2, dict(kicker="Step 4 · Team training", title='We train humans<br><b class="pv">AI can’t replace</b>',
                               sub="3 months with a mentor")),
        ("cases", 1.5, dict(kicker="AI transformation cases", title='From AI strategy to <b class="go">business results</b>')),
    ],
}
CTA = {"ait": {"ru": "Бесплатная ИИ-диагностика →", "en": "Free AI assessment →"},
       "nr": {"ru": "Попробовать бесплатно →", "en": "Start free trial →"}}

NR_LAYOUT = {
    "slide-hero": dict(left=60, width=1000, top=362, size=46),
    "slide-context": dict(left=60, width=430),
    "slide-management": dict(left=60, width=440),
    "slide-cases": dict(left=60, width=1000, top=34, size=40, hideLogo=True),
    "gradient": dict(left=60, width=1000, align="center", size=58),
}
NR = {
    "ru": [
        ("slide-hero", 0.5, dict(title='<b>Ведите ИИ-бизнес</b><br><span class="dim">в операционной системе на базе ИИ</span>')),
        ("slide-context", 0.8, dict(kicker="Платформа", title="ИИ-суперагент работает в контексте вашего бизнеса",
                                    sub="Ставите задачу простыми словами — он сам работает в ваших инструментах")),
        ("slide-management", 1.0, dict(kicker="Управление", title="ИИ-управление знаниями",
                                       sub="Ответы с полным контекстом бизнеса — со ссылками на источники")),
        ("slide-cases", 0.6, dict(title="ИИ-суперагент управляет 100 готовыми ИИ-сотрудниками в десяти отделах")),
        ("gradient", 0.8, dict(title="Ведите свой ИИ-бизнес с Нейронием", sub="Каждый тариф начинается с бесплатного периода",
                               cta="Попробовать бесплатно →", dom="neuronium.ai")),
    ],
    "en": [
        ("slide-hero", 0.5, dict(title='<b>Run AI Business</b> <span class="dim">with AI Operating System</span>')),
        ("slide-context", 0.8, dict(kicker="Platform", title="AI Superagent works in your business context",
                                    sub="Give it a task in plain words — it works through your tools")),
        ("slide-management", 1.0, dict(kicker="Management", title="AI Knowledge Management",
                                       sub="Answers with the full business context — and their sources")),
        ("slide-cases", 0.6, dict(title="AI Superagent manages 100 ready AI employees across ten departments")),
        ("gradient", 0.8, dict(title="Run Your AI Business with Neuronium", sub="Every plan starts with a free trial",
                               cta="Start free trial →", dom="neuronium.ai")),
    ],
}


def save(name, cfg):
    (WORK / f"cfg-{name}.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
    print(name, round(sum(s["dur"] for s in cfg["scenes"]), 2), "s")


for lang in ("ru", "en"):
    save(f"ait-{lang}", {"theme": "ait", "fps": FPS, "logo": "ait-logo.png", "cta": CTA["ait"][lang], "scenes": [
        scene(f"at-{lang}/{sid}", hold, lang, layout=dict(left=56, width=500 if sid == "change" else 440), **kw)
        for sid, hold, kw in AIT[lang]]})
    for variant in ("nr", "nrs"):  # nr — живой свет фона (MP4), nrs — неподвижный (GIF)
        save(f"{variant}-{lang}", {"theme": "nr", "fps": FPS, "cta": CTA["nr"][lang], "scenes": [
            scene(f"{variant}/{sid}", hold, lang, layout=NR_LAYOUT[sid], **dict(kw)) for sid, hold, kw in NR[lang]]})
    save(f"ait-sq-{lang}", {"compose": "compose-square.html", "size": [720, 720], "fps": FPS, "logo": "ait-logo.png",
                            "tag": "andre.technology", "cta": CTA["ait"][lang], "scenes": [
        scene(f"at-{lang}/{sid}", hold, lang, crop=AIT_SQ_CROP[sid], **kw) for sid, hold, kw in AIT_SQ[lang]]})

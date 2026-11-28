"""Кадры фона для каждой сцены: кусок записи слайда (record.js), ускоренный до нужной длины, 24 к/с.

work/frames/<вариант>/<сцена>/f0001.jpg …  и work/frames.json (сколько кадров в каждой сцене)
  at-ru, at-en — andre.technology; ath-ru, ath-en — они же в исходном размере 1280×720 (для вертикального ролика,
  где схема идёт крупным планом); nr — neuronium.ai с живым светом фона; nrs — с неподвижным (для GIF).
"""
import json
import os
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE / "work"
FPS = 24
AIT_VF = "scale=1024:576:flags=lanczos,pad=1120:630:96:27:color=0x060606"  # анимации справа, слева — место под текст
NR_VF = "scale=1120:630:flags=lanczos"
# сцена: (с какой секунды слайда, по какую, сколько секунд в ролике)
PLAN = {
    "at": [("change", 0.3, 6.9, 3.4), ("maturity", 0.3, 6.9, 3.4), ("strategy", 0.5, 7.1, 3.4),
           ("neuronium", 0.3, 6.9, 3.4), ("training", 0.3, 6.9, 3.4), ("cases", 0.6, 5.6, 3.6)],
    "nr": [("slide-hero", 0.5, 5.5, 3.4), ("slide-context", 0.4, 7.0, 3.8), ("slide-management", 0.8, 7.2, 3.6),
           ("slide-cases", 0.3, 5.8, 3.6), ("gradient", 0.5, 7.0, 3.8)],
}


def extract(video, t0, a, b, dur, out, vf):
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0 + a:.3f}", "-t", f"{b - a + 0.2:.3f}", "-i", str(video),
                    "-vf", f"setpts=PTS*{dur / (b - a):.5f},fps={FPS},{vf}", "-frames:v", str(round(dur * FPS)),
                    "-q:v", "3", str(out / "f%04d.jpg")], check=True)
    return len(list(out.glob("*.jpg")))


def still(image, dur, out):
    """Неподвижная сцена из одного кадра (свет фона без движения)."""
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(image), "-vf", NR_VF, "-q:v", "3", str(out / "f0001.jpg")], check=True)
    for k in range(2, round(dur * FPS) + 1):
        os.symlink("f0001.jpg", out / f"f{k:04d}.jpg")
    return round(dur * FPS)


def starts(name):
    return {e["id"]: e["t"] for e in json.loads((WORK / f"rec-{name}.json").read_text())}


counts = {}
for lang in ("ru", "en"):
    log = starts(f"ait-{lang}")
    for sid, a, b, d in PLAN["at"]:
        counts[f"at-{lang}/{sid}"] = extract(WORK / f"rec-ait-{lang}.webm", log[sid], a, b, d, WORK / f"frames/at-{lang}/{sid}", AIT_VF)
        counts[f"ath-{lang}/{sid}"] = extract(WORK / f"rec-ait-{lang}.webm", log[sid], a, b, d, WORK / f"frames/ath-{lang}/{sid}", "null")
live, calm, grad = starts("nr"), starts("nr-still"), starts("nr-gradient")["slide-hero"]
for sid, a, b, d in PLAN["nr"]:
    if sid == "gradient":
        counts[f"nr/{sid}"] = extract(WORK / "rec-nr-gradient.webm", grad, a, b, d, WORK / f"frames/nr/{sid}", NR_VF)
        counts[f"nrs/{sid}"] = still(WORK / "lf-slide-hero.jpg", d, WORK / f"frames/nrs/{sid}")
    else:
        counts[f"nr/{sid}"] = extract(WORK / "rec-nr.webm", live[sid], a, b, d, WORK / f"frames/nr/{sid}", NR_VF)
        counts[f"nrs/{sid}"] = extract(WORK / "rec-nr-still.webm", calm[sid], a, b, d, WORK / f"frames/nrs/{sid}", NR_VF)
(WORK / "frames.json").write_text(json.dumps({"plan": PLAN, "counts": counts}, indent=1))
print(json.dumps(counts))

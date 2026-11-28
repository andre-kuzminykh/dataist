#!/bin/bash
# Пересобрать ролики-объяснения для рекламы в дайджесте:
#   ../assets/ait-explainer-{ru,en}.{mp4,jpg,gif}, ../assets/neuronium-explainer-{ru,en}.{mp4,jpg,gif}
#   ../assets/ait-square-{ru,en}.{mp4,jpg} — квадратный ролик с крупным текстом для узкой колонки веб-газеты
#
#   ./make.sh           — всё с нуля: записать анимации сайтов, нарезать сцены, наложить текст, закодировать
#   ./make.sh --no-rec  — без новой записи сайтов: например, поменяли тексты в scenes.py
#
# Нужны: node + playwright (Chromium), ffmpeg, gifsicle, python3 + numpy + pillow;
# сеть: andre.technology, neuronium.ai, fonts.googleapis.com. Рабочие файлы — в work/ (не в git).
# OUT=папка ./make.sh — положить результат в другую папку (например, чтобы сначала посмотреть).
set -euo pipefail
cd "$(dirname "$0")"
OUT=${OUT:-../assets}
mkdir -p work "$OUT"

if [ "${1:-}" != "--no-rec" ]; then
  for what in ait-ru ait-en nr nr-gradient nr-still; do node record.js "$what"; done
  python3 frames.py
fi
python3 scenes.py

pids=()
for c in ait-ru ait-en nr-ru nr-en nrs-ru nrs-en ait-sq-ru ait-sq-en; do node render.js "work/cfg-$c.json" "work/out-$c" & pids+=($!); done
for p in "${pids[@]}"; do wait "$p"; done

# <кадры> <имя>: MP4 и обложка — без GIF (квадратный ролик идёт только в веб-газету)
mp4() {
  ffmpeg -v error -y -framerate 24 -i "work/out-$1/f%04d.png" -c:v libx264 -profile:v high -pix_fmt yuv420p \
    -crf 26 -preset slow -movflags +faststart -an "$OUT/$2.mp4"
  ffmpeg -v error -y -i "work/out-$1/f0067.png" -q:v 3 "$OUT/$2.jpg"
}
# <кадры для MP4> <имя> <кадры для GIF> <с какой секунды начинать GIF: первый кадр с заголовком — его покажет Outlook>
enc() {
  mp4 "$1" "$2"
  python3 gifenc.py "work/out-$3" "$OUT/$2.gif" --fps 10 --thr 8 --block 4 --colors 128 --lossy 100 --rotate "$4"
}
pids=()
enc ait-ru ait-explainer-ru ait-ru 3.4 & pids+=($!)
enc ait-en ait-explainer-en ait-en 3.4 & pids+=($!)
enc nr-ru neuronium-explainer-ru nrs-ru 3.0 & pids+=($!)
enc nr-en neuronium-explainer-en nrs-en 3.0 & pids+=($!)
mp4 ait-sq-ru ait-square-ru & pids+=($!)
mp4 ait-sq-en ait-square-en & pids+=($!)
for p in "${pids[@]}"; do wait "$p"; done
ls -l "$OUT"/*-explainer-* "$OUT"/ait-square-*

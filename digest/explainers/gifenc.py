"""Лёгкий GIF для письма: временная «мёртвая зона» — пиксели фона, которые почти не поменялись,
берём из предыдущего кадра, чтобы GIF хранил только реальные изменения (текст, интерфейс).

python3 gifenc.py <frames_dir> <out.gif> [--fps 10] [--w 560] [--thr 10] [--block 4] [--colors 128]
                  [--lossy 80] [--rotate SEC]
--rotate: начать GIF с этого момента (первый кадр — с полным заголовком: его покажет Outlook).
"""
import argparse, glob, os, shutil, subprocess, tempfile
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--fps', type=float, default=10); ap.add_argument('--w', type=int, default=560)
ap.add_argument('--thr', type=float, default=10); ap.add_argument('--block', type=int, default=4)
ap.add_argument('--colors', type=int, default=128); ap.add_argument('--lossy', type=int, default=80)
ap.add_argument('--dither', default='bayer:bayer_scale=3'); ap.add_argument('--rotate', type=float, default=0)
ap.add_argument('--src-fps', type=float, default=24)
a = ap.parse_args()

src = sorted(glob.glob(os.path.join(a.src, 'f*.png')))
n_out = int(len(src) / a.src_fps * a.fps)
idx = [min(len(src) - 1, round(k * a.src_fps / a.fps)) for k in range(n_out)]
if a.rotate:
    r = int(round(a.rotate * a.fps)) % n_out
    idx = idx[r:] + idx[:r]
h = round(a.w * 9 / 16)
tmp = tempfile.mkdtemp(prefix='gifenc-')
prev = None
B = a.block
for k, i in enumerate(idx):
    im = Image.open(src[i]).convert('RGB').resize((a.w, h), Image.LANCZOS)
    cur = np.asarray(im, dtype=np.int16)
    if prev is not None and B > 0:
        d = np.abs(cur - prev).max(axis=2)
        H, W = d.shape
        db = d[:H - H % B, :W - W % B].reshape(H // B, B, W // B, B).max(axis=(1, 3))
        keep = np.repeat(np.repeat(db < a.thr, B, 0), B, 1)
        mask = np.zeros_like(d, dtype=bool); mask[:keep.shape[0], :keep.shape[1]] = keep
        cur = np.where(mask[..., None], prev, cur)
    prev = cur
    Image.fromarray(cur.astype(np.uint8)).save(os.path.join(tmp, f'g{k:04d}.png'))
raw = os.path.join(tmp, 'raw.gif')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(a.fps), '-i', os.path.join(tmp, 'g%04d.png'), '-vf',
                f'split[x][y];[x]palettegen=max_colors={a.colors}:stats_mode=full[p];[y][p]paletteuse=dither={a.dither}:diff_mode=rectangle',
                raw], check=True)
subprocess.run(['gifsicle', '-O3', f'--lossy={a.lossy}', raw, '-o', a.out], check=True)
shutil.rmtree(tmp)
print(os.path.basename(a.out), f'{os.path.getsize(a.out) // 1024} KB', f'{n_out} frames @ {a.fps} fps', vars(a))

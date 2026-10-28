#!/usr/bin/env python3
"""Mascara os 3 takes (remove fundo) e salva frames RGBA em jobs/job-001/masks/."""
import subprocess, time, sys
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

W = Path('/home/node/.openclaw/workspace/efsm-openclaw-fuzari')
FF = str(W / 'bin/ffmpeg')
MASK_DIR = W / 'jobs/job-001/masks'
MASK_DIR.mkdir(parents=True, exist_ok=True)

# (nome, arquivo, start, end) — V4: cues "Pode"/"Pode ir" + ar morto removidos (análise de energia + whisper)
SEGMENTS = [
    ('seg1', 'IMG_6302.MOV', 2.20, 7.70),
    ('seg2', 'IMG_6303.MOV', 1.50, 7.60),
    ('seg3', 'IMG_6305.MOV', 2.55, 8.40),
]

def log(msg):
    print(msg, flush=True)

log('carregando modelo u2net...')
session = new_session('u2net')
log('modelo ok')

total = 0
for name, fname, start, end in SEGMENTS:
    src = W / 'jobs/job-001/input' / fname
    fdir = MASK_DIR / (name + '_frames')
    fdir.mkdir(parents=True, exist_ok=True)

    log(f'[{name}] extraindo frames (trim {start}-{end})...')
    subprocess.run([FF, '-y', '-i', str(src), '-vf',
                    f'trim={start}:{end},setpts=PTS-STARTPTS,scale=540:960,setsar=1,fps=30',
                    '-f', 'image2', str(fdir / '%04d.png')],
                   check=True, capture_output=True)

    pngs = sorted(fdir.glob('*.png'))
    n = len(pngs)
    total += n
    log(f'[{name}] {n} frames. mascarando...')
    t0 = time.time()
    for i, p in enumerate(pngs):
        img = Image.open(p).convert('RGB')
        out = remove(img, session=session, post_process_mask=True)
        out.save(p)  # sobrescreve com RGBA
        if (i + 1) % 25 == 0 or i + 1 == n:
            el = time.time() - t0
            rate = (i + 1) / el if el > 0 else 0
            eta = (n - i - 1) / rate if rate > 0 else 0
            log(f'[{name}] {i+1}/{n}  ({rate:.2f}f/s)  ETA {eta:.0f}s')
    log(f'[{name}] concluído em {time.time()-t0:.0f}s')

log(f'TODAS AS MÁSCARAS PRONTAS — {total} frames no total')

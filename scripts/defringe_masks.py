#!/usr/bin/env python3
"""Defringe: erode alpha + feather + decontamina borda (remove halo branco)."""
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path

W = Path('/home/node/.openclaw/workspace/efsm-openclaw-fuzari')
M = W / 'jobs/job-001/masks'

def defringe(img):
    arr = np.array(img.convert('RGBA')).astype(np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # 1) erode a máscara (corta o halo branco da borda)
    a_img = Image.fromarray(a.astype(np.uint8), 'L').filter(ImageFilter.MinFilter(5))
    # 2) suaviza (feather) a borda
    a_img = a_img.filter(ImageFilter.GaussianBlur(1.3))
    a = np.array(a_img).astype(np.float32)

    # 3) decontaminação: dessatura e escurece pixels semi-transparentes (spill)
    alpha = a / 255.0
    gray = (r + g + b) / 3.0
    spill = (1.0 - alpha) ** 1.5  # 0 no opaco, 1 no transparente
    r2 = r * (1 - spill * 0.6) + gray * (spill * 0.6)
    g2 = g * (1 - spill * 0.6) + gray * (spill * 0.6)
    b2 = b * (1 - spill * 0.6) + gray * (spill * 0.6)
    darken = 1.0 - spill * 0.35
    r2 *= darken; g2 *= darken; b2 *= darken

    out = np.stack([r2, g2, b2, a], axis=-1).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')

total = 0
for seg in ['seg1_frames', 'seg2_frames', 'seg3_frames']:
    d = M / seg
    pngs = sorted(d.glob('*.png'))
    for p in pngs:
        defringe(Image.open(p)).save(p)
    total += len(pngs)
    print(f'{seg}: {len(pngs)} defringed', flush=True)
print(f'DEFRINGE CONCLUÍDO — {total} frames', flush=True)

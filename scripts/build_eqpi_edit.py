#!/usr/bin/env python3
"""
build_eqpi_edit.py — Edição dinâmica do case EQPI Tecnologia (job-002).

Objetivo: encurtar (remover pausas mortas via jump cuts) + motion (zoom punch in/out)
+ legenda com destaques + música de fundo ritmada.

Entrada: jobs/job-002/input/eqpi_original.mp4 (720x1280, 60fps, ~58.7s)
Saída:  jobs/job-002/renders/eqpi_v1.mp4
"""
import subprocess, json, os
from pathlib import Path

W = Path('/home/node/.openclaw/workspace/efsm-openclaw-fuzari')
FF = str(W / 'bin/ffmpeg')
JOB = W / 'jobs/job-002'
SRC = JOB / 'input/eqpi_original.mp4'
R = JOB / 'renders'
A = JOB / 'audio'
TMP = W / 'tmp_eqpi'
TMP.mkdir(parents=True, exist_ok=True)
R.mkdir(parents=True, exist_ok=True)
A.mkdir(parents=True, exist_ok=True)

FPS = 30
W_OUT, H_OUT = 720, 1280

# (start, end, zoom_kind, caption_text_or_None)
# zoom_kind: 'in' (1.0->1.10) | 'out' (1.10->1.0) | 'soft' (1.0->1.05) | 'still' (1.03)
# Cortes por FRASE INTEIRA (nunca no meio da palavra) — fronteiras nas pausas naturais
SEGMENTS = [
    (0.45, 6.05, 'soft',  'RISCOS TRABALHISTAS E JURÍDICOS'),
    (6.33, 10.95, 'soft', 'CONTRATOS CENTRALIZADOS'),
    (11.35, 15.47, 'soft', 'PROCESSO MANUAL'),
    (16.13, 18.51, 'in',   'A EQPI MUDOU ESSA REALIDADE'),
    (18.77, 22.91, 'soft', 'INTELIGÊNCIA ARTIFICIAL'),
    (23.45, 27.49, 'soft', 'SISTEMA ÚNICO E SEGURO'),
    (27.49, 29.19, 'in',   'RESULTADO TANGÍVEL'),
    (29.59, 37.17, 'in',   '40% DE REDUÇÃO'),
    (38.11, 41.55, 'out',  'TECNOLOGIA + PROPÓSITO'),
    (42.23, 46.79, 'soft', 'BUROCRACIA → ESTRATÉGIA'),
    (46.91, 50.87, 'soft', 'CONFORMIDADE E INOVAÇÃO'),
    (51.27, 52.97, 'in',   'QUER TRANSFORMAR SUA GESTÃO?'),
    (52.97, 57.41, 'in',   'SOLICITE UMA DEMONSTRAÇÃO'),
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1200:])
        raise SystemExit(f'FALHOU: {" ".join(cmd[:6])}...')

def zoom_expr(kind, frames):
    n = max(frames - 1, 1)
    if kind == 'in':
        z0, z1 = 1.0, 1.10
    elif kind == 'out':
        z0, z1 = 1.10, 1.0
    elif kind == 'soft':
        z0, z1 = 1.0, 1.05
    else:  # still
        z0, z1 = 1.03, 1.03
    return f'{z0}+{z1 - z0}*on/{n}'

# ---------- 1. renderizar segmentos (vídeo + áudio) ----------
print('=== [1] renderizando segmentos ===', flush=True)
video_files, audio_files = [], []
cum = 0.0
caption_events = []  # (new_start, new_end, text)

for i, (s, e, kind, cap) in enumerate(SEGMENTS):
    dur = e - s
    frames = max(round(dur * FPS), 2)
    vf = (f"trim={s}:{e},setpts=PTS-STARTPTS,fps={FPS},"
          f"zoompan=z='{zoom_expr(kind, frames)}':x='iw/2-(iw/zoom/2)':"
          f"y='ih/2-(ih/zoom/2)':d=1:s={W_OUT}x{H_OUT}:fps={FPS},setsar=1")
    vfile = TMP / f'seg_{i:02d}.mp4'
    afile = TMP / f'seg_{i:02d}.wav'
    run([FF, '-y', '-i', str(SRC), '-vf', vf, '-r', str(FPS),
         '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
         '-pix_fmt', 'yuv420p', str(vfile)])
    run([FF, '-y', '-i', str(SRC), '-ss', str(s), '-t', f'{dur:.3f}',
         '-vn', '-ac', '1', '-ar', '48000', str(afile)])
    video_files.append(vfile)
    audio_files.append(afile)
    if cap:
        caption_events.append((cum, cum + dur, cap))
    cum += dur
    print(f'  seg {i:02d}: {s:.2f}-{e:.2f} ({dur:.2f}s) zoom={kind} cap={cap!r}', flush=True)

print(f'=== duração nova: {cum:.2f}s (era 58.7s) ===', flush=True)

# ---------- 2. concat vídeo + áudio ----------
print('=== [2] concat ===', flush=True)
vlist = TMP / 'vlist.txt'
alist = TMP / 'alist.txt'
vlist.write_text(''.join(f"file '{f}'\n" for f in video_files))
alist.write_text(''.join(f"file '{f}'\n" for f in audio_files))
cut_v = TMP / 'cut_video.mp4'
cut_a = TMP / 'cut_audio.wav'
run([FF, '-y', '-f', 'concat', '-safe', '0', '-i', str(vlist), '-c', 'copy', str(cut_v)])
run([FF, '-y', '-f', 'concat', '-safe', '0', '-i', str(alist), '-c', 'copy', str(cut_a)])

# ---------- 3. gerar legenda (ASS) ----------
print('=== [3] legenda ===', flush=True)
cap_ass = TMP / 'captions.ass'

def ass_time(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60)
    cs = int(round((t - int(t)) * 100))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

GOLD = r'{\c&H004BB8E8&}'   # #E8B84B (dourado) — ASS usa BGR
WHITE = r'{\c&H00FFFFFF&}'
lines = [
    '[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 720', 'PlayResY: 1280',
    'ScaledBorderAndShadow: yes', 'WrapStyle: 2', '',
    '[V4+ Styles]',
    'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
    'Style: Cap,Archivo Black,46,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,-1,0,0,0,100,100,0,0,3,3,1,5,0,0,0,1',
    '',
    '[Events]',
    'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
]
def split_cap(text):
    if len(text) <= 20:
        return text
    words = text.split()
    mid = len(words) // 2
    return ' '.join(words[:mid]) + '\\N' + ' '.join(words[mid:])

for (cs, ce, text) in caption_events:
    col = GOLD if text == '40% DE REDUÇÃO' else WHITE
    txt = col + split_cap(text)
    y = 880 if '\\N' in txt else 880
    lines.append(f"Dialogue: 0,{ass_time(cs)},{ass_time(ce)},Cap,,0,0,0,,"
                 f"{{\\an5\\pos(360,{y})\\fad(80,80)}}{txt}")

cap_ass.write_text('\n'.join(lines) + '\n', encoding='utf-8')

# ---------- 4. montagem final (legenda + música + loudnorm) ----------
print('=== [4] montagem final ===', flush=True)
music = A / 'bg_music.mp3'
final = R / 'eqpi_v1.mp4'

if music.exists():
    print('  música encontrada, mixando (loop)...', flush=True)
    run([FF, '-y', '-i', str(cut_v), '-i', str(cut_a),
         '-stream_loop', '-1', '-i', str(music),
         '-filter_complex',
         f"[0:v]subtitles={cap_ass}:fontsdir={os.path.expanduser('~/.fonts')},format=yuv420p[vout];"
         f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[avoz];"
         f"[2:a]volume=0.16,afade=t=in:st=0:d=0.6,afade=t=out:st={max(cum-2.5,0):.1f}:d=2.5,aresample=48000[amus];"
         f"[avoz][amus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[aout]",
         '-map', '[vout]', '-map', '[aout]',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '160k', '-ar', '48000',
         '-movflags', '+faststart', str(final)])
else:
    print('  sem música, só legenda + voz...', flush=True)
    run([FF, '-y', '-i', str(cut_v), '-i', str(cut_a),
         '-filter_complex',
         f"[0:v]subtitles={cap_ass}:fontsdir={os.path.expanduser('~/.fonts')},format=yuv420p[vout];"
         f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[aout]",
         '-map', '[vout]', '-map', '[aout]',
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '160k', '-ar', '48000',
         '-movflags', '+faststart', str(final)])

print(f'✅ FINAL: {final}')
print(f'   duração nova: {cum:.2f}s')

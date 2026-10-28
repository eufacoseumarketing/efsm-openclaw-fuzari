#!/usr/bin/env python3
"""Gera captions.ass premium para o criativo "19 contratos em 30 dias" (V4).

- Fonte: Archivo Black (legenda) / Anton (headline).
- Paleta: branco + dourado #E8B84B (palavras-chave) + roxo #7C3AED (caixa do CTA).
- Legenda principal: caixa preta semi-transparente (garante contraste sobre qualquer fundo).
- CTA: caixa roxa sólida + texto branco (alta legibilidade).
- Timeline final (xfade 0.35s): seg1 0.00-5.50 | seg2 5.15-11.20 | seg3 10.85-16.73
"""
from pathlib import Path

W = Path('/home/node/.openclaw/workspace/efsm-openclaw-fuzari')
OUT = W / 'jobs/job-001/captions.ass'

WHITE = r'{\c&H00FFFFFF&}'
GOLD  = r'{\c&H004BB8E8&}'
PURPLE= r'{\c&H00ED3A7C&}'

# (inicio, fim, [(texto, cor)], kind)
# cor: 'w'=branco 'g'=dourado 'p'=roxo | kind: 'head' | 'cap' | 'cta'
EVENTS = [
    # --- Headline seg1 (preenche o intro "esse é...") ---
    (0.25, 2.25, [("CASO REAL", 'g')], 'head'),
    # --- Seg1: hook (trim 2.40s — "pode ir" removido) ---
    (2.25, 2.85, [("FECHOU", 'w')], 'cap'),
    (2.85, 3.95, [("19 CONTRATOS", 'g')], 'cap'),
    (3.95, 4.40, [("EM APENAS", 'w')], 'cap'),
    (4.40, 5.35, [("30 DIAS", 'g')], 'cap'),
    # --- Seg2: método ---
    (5.30, 6.05, [("TUDO ISSO ATRAVÉS", 'w')], 'cap'),
    (6.05, 6.90, [("DE UM ", 'w'), ("MÉTODO", 'g')], 'cap'),
    (6.90, 7.60, [("PENSADO", 'w')], 'cap'),
    (7.90, 8.95, [("EXCLUSIVO", 'g'), (" PARA", 'w')], 'cap'),
    (8.95, 9.80, [("DIVULGADORES QUE", 'w')], 'cap'),
    (9.80, 10.45, [("QUEREM ", 'w'), ("CRESCER", 'g')], 'cap'),
    (10.45, 11.15, [("DE FORMA ", 'w'), ("PREVISÍVEL", 'g')], 'cap'),
    # --- Seg3: CTA (caixa roxa + texto branco) ---
    (11.00, 12.60, [("CLIQUE NO LINK", 'w')], 'cta'),
    (12.60, 13.90, [("E FALE AGORA", 'w')], 'cta'),
    (13.90, 16.65, [("COM O NOSSO TIME", 'w')], 'cta'),
]

def ass_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    cs = int(round((t - int(t)) * 100))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def color_tag(c):
    return {'w': WHITE, 'g': GOLD, 'p': PURPLE}[c]

def build_event(ev):
    start, end, parts, kind = ev
    text = ''.join(color_tag(c) + t for t, c in parts)
    if kind == 'head':
        style = 'Headline'
        pos = r'{\an5\pos(540,340)\fad(180,180)}'
    elif kind == 'cta':
        style = 'CTA'
        pos = r'{\an5\pos(540,1540)\fad(90,90)}'
    else:
        style = 'Cap'
        pos = r'{\an5\pos(540,1500)\fad(90,90)}'
    return (start, end, style, pos + text)

def main():
    L = []
    L.append('[Script Info]')
    L.append('ScriptType: v4.00+')
    L.append('PlayResX: 1080')
    L.append('PlayResY: 1920')
    L.append('ScaledBorderAndShadow: yes')
    L.append('WrapStyle: 2')
    L.append('')
    L.append('[V4+ Styles]')
    L.append('Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding')
    # Headline: Anton dourado (topo, sem caixa)
    L.append('Style: Headline,Anton,140,&H004BB8E8,&H00FFFFFF,&H00101010,&H00000000,-1,0,0,0,100,100,0,0,1,4,1,5,0,0,0,1')
    # Cap: Archivo Black branco + caixa preta semi-transparente
    L.append('Style: Cap,Archivo Black,84,&H00FFFFFF,&H00FFFFFF,&H00101010,&H78000000,-1,0,0,0,100,100,0,0,3,3,1,5,0,0,0,1')
    # CTA: Archivo Black branco + caixa roxa sólida
    L.append('Style: CTA,Archivo Black,84,&H00FFFFFF,&H00FFFFFF,&H00101010,&H00ED3A7C,-1,0,0,0,100,100,0,0,3,3,1,5,0,0,0,1')
    L.append('')
    L.append('[Events]')
    L.append('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text')

    for ev in EVENTS:
        start, end, style, text = build_event(ev)
        L.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},{style},,0,0,0,,{text}")

    OUT.write_text('\n'.join(L) + '\n', encoding='utf-8')
    print(f"✅ captions.ass gerado ({len(EVENTS)} eventos) -> {OUT}")

if __name__ == '__main__':
    main()

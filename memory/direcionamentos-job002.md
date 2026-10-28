# Direcionamentos — Job 002 (Case EQPI Tecnologia)

> Salvo em 2026-09-12. Cliente: **EQPI Tecnologia** (sigla falada vira "KBITEC" no whisper).

## Contexto
- Vídeo original: `jobs/job-002/input/eqpi_original.mp4` (720x1280, 60fps, ~58.7s) — talking head selfie, homem falando em cenário externo (teto de bambu).
- Pedido: "ficou muito longo, tem que ser mais dinâmico" + "música mais ritmada, esse cara já é cansativo".
- Conteúdo (case de mineração): riscos trabalhistas/jurídicos → contratos manuais → EQPI digitalizou (IA, compliance) → 40% redução → previsibilidade → CTA demonstração.

## Decisões
- **Jump cuts** removem pausas mortas entre frases (whisper word_timestamps + RMS): 58.7s → **43.8s** (~25% mais curto).
- **Motion**: zoompan punch in/out por beat (hook/40%/CTA = 'in' 1.0→1.10; contexto = 'soft' 1.0→1.05; transição = 'out').
- **Legenda**: keyword highlights (não transcrição cheia — evita erro do whisper). "40% DE REDUÇÃO" em dourado. Fonte Archivo Black 46, caixa preta, **posição y=880** (zona segura, fora da UI). Textos >20 chars em 2 linhas.
- **Música ritmada** gerada (28s) com `-stream_loop -1` para cobrir o vídeo; volume 0.16, fade in/out.
- Paleta: branco + dourado #E8B84B. Resolução mantida 720x1280 (nativa, sem upscale).

## Pipeline (scripts/build_eqpi_edit.py)
1. 20 segmentos (trim + zoompan) + áudio trimado → `tmp_eqpi/seg_*.mp4/wav`.
2. Concat (demuxer) → cut_video + cut_audio.
3. Gera captions.ass (keyword highlights).
4. Final: subtitles + loudnorm voz + música loop + amix → `eqpi_v1.mp4`.

## Entrega
- `Criativo`... nome: `EQPI_Tecnologia_Case_Dinamico_v1.mp4` — Drive id `1I4KHCYpzC7_SgV1GljVCfcZCtvOryJkz` (raiz, pois pasta "Marcelo 01" sumiu).
- Link: https://drive.google.com/file/d/1I4KHCYpzC7_SgV1GljVCfcZCtvOryJkz/view

## Lições
- **CORTES POR FRASE, NUNCA NO MEIO DA PALAVRA** (feedback do Zanatto). V1 tinha 20 micro-cortes picotando palavras → "esquisito". V2: 13 frases inteiras, corte só nas pausas naturais (whisper word_timestamps). 58.7s → 52.3s.
- Música gerada saiu 28s (não 50s) → loop com `-stream_loop -1` + `amix duration=first`.
- QA com visão flagrou legenda baixa (zona de UI) → subir pra y≈880 e quebrar texto longo.
- Não chamar music_generate + write no mesmo turno (o write é abortado pelo background task).
- Re-transcrever com `--word-timestamps` é essencial pra achar fronteira de frase (o transcript segment-level não basta).

## Entrega v2 (corrigida)
- `EQPI_Tecnologia_Case_Dinamico_v2.mp4` — Drive id `1H4JaLfPZlQf-I418juem8d9Jar6tWS73`.
- Link: https://drive.google.com/file/d/1H4JaLfPZlQf-I418juem8d9Jar6tWS73/view

# Direcionamentos — Job 001 (Criativo "19 contratos em 30 dias")

> Salvo em 2026-09-10 após incidente de disco cheio. Fonte: conversa com Zanatto (Discord).
> Regra: este arquivo é memória durável — preservar/atualizar conforme o trabalho avança.

## Contexto
- Criativo de teste a partir de 3 takes de vídeo do Google Drive (Shared Drive, pasta "Marcelo 01").
- Takes: IMG_6302.MOV, IMG_6303.MOV, IMG_6305.MOV (HEVC, 1920x1080 com rotação -90 → vertical 1080x1920 real, ~60fps).
- Talento fala de um cliente que fechou "19 contratos em 30 dias" via um método exclusivo.
- **Cliente: nome NÃO confirmado.** Transcrição pegou "divulgado(s)"; quadro ao fundo mostra "STALO". NÃO colocar nome do cliente na legenda até o Zanatto confirmar.

## Direcionamentos (feedback em ordem cronológica)
### V2 (feedback 1)
1. Cortar a fala de fundo do Kaique ("pode ir..." ~2x) — é cue de gravação.
2. Mais dinâmico: cortar pausas/silêncios mortos.
3. Trocar fonte por uma mais moderna (DejaVu Sans = amador).
4. Adicionar música de fundo.

### V3 (feedback 2)
5. Adicionar zoom in/out entre as transições (punch-in/out).
6. Mais criatividade e atenção aos detalhes.

### V4 (régua de qualidade)
7. Referência de qualidade: reel da **Fitto Solutions** (@fittosolutions) — "quero vídeos com esse nível".
   - Análise completa: `references/fitto/analysis.md`.
   - 5 pilares: (a) sujeito isolado + cenário desenhado, (b) color grade cinematográfico, (c) tipografia premium com hierarquia, (d) motion graphics de marca, (e) paleta consistente (marinho + branco + dourado).
8. "Faça com o que tem, manda bala" → empurrar o máximo de qualidade com o tooling atual (isolamento de fundo via rembg + arte de fundo gerada por IA + color grade).

## Decisões e lições técnicas (job-001)
- Transcrição: faster-whisper + int8 (CPU). `word_timestamps=True` para localizar o "pode ir" e pausas. Script: `scripts/transcribe.py`.
- **FFmpeg estático (johnvansickle) NÃO tem drawtext** → usar filtro `subtitles`/`ass` (libass) para legendas.
- Fontes modernas (fontsource → `~/.fonts`): **Anton** (headline), **Archivo Black** (legendas/CTA), **Playfair Display** (serif premium). Evitar Montserrat do fontsource (metadata bugada, família "Montserrat Thin").
- Paleta premium: texto branco + **dourado #E8B84B** (palavras-chave) + **roxo #7C3AED** (CTA). Em ASS: dourado `&H004BB8E8&`, roxo `&H00ED3A7C&`.
- Isolamento de fundo: **rembg/u2net** com `post_process_mask=True` (`alpha_matting` é lento demais ~25s/frame; post_process ~1.35s/frame). Mascarar a 540x960 (upscale 2x depois).
- **Defringe** (remover halo branco da borda): erode alpha (PIL `MinFilter(5)`) + `GaussianBlur(1.3)` + decontaminação de borda. Script: `scripts/defringe_masks.py`.
- Composição: **NÃO usar `-loop 1` + `overlay shortest=1` + `zoompan` no mesmo graph** (deadlock "100 buffers queued", mp4 sai 0 bytes). Fazer em 2 etapas: (1) composite overlay simples → seg_comp.mp4; (2) zoom + grade + concat + subtitles (comprovado).
- Grade final: `eq=contrast=1.12:saturation=0.95:brightness=-0.02:gamma=0.97` + cooling. ATENÇÃO: `colorbalance` falhou em um teste — validar ou usar `colorchannelmixer`/`colortemperature`.

## Timeline (trims, 30fps) — V4 (2026-09-12, pós-servidor maior)
- Cues "Pode"/"Pode ir" (voz baixa do Kaique) localizados via análise de energia RMS + whisper:
  - IMG_6302: cue "Pode" 1.5-2.2s, fala alta "esse é..." inicia ~2.3s.
  - IMG_6305: cue "Pode ir" 1.2-1.5s + ~0.9s de ar morto, fala "Se você..." inicia ~2.6s.
- Novos trims: Seg1 (IMG_6302) 2.20→7.70 | Seg2 (IMG_6303) 1.50→7.60 | Seg3 (IMG_6305) 2.55→8.40.
- Total ~16.7s (com xfade 0.35s entre segmentos), 1080x1920, 30fps.
- Motion: zoompan punch-in/out (seg1 in 1→1.08, seg2 out 1.08→1, seg3 in 1→1.10) + xfade smoothleft/smoothup.
- Zoom: seg1 punch-in (z 1→1.10), seg2 punch-out (1.10→1), seg3 punch-in (1→1.12). Fórmula zoompan: `x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30`.

## Áudio
- Música de fundo: gerada (track ~30s), volume ~0.15, afade in/out, `amix normalize=0`.
- Voz: `loudnorm=I=-16:TP=-1.5:LRA=11`.
- Saída: mono (ok p/ social), aac 160k 48kHz.

## Google Drive (via `scripts/drive.py`, supportsAllDrives)
- Pasta alvo "Marcelo 01": `1Pi3Tntw5_1kwRVAAZYorVzXY5vhz8yDw`.
- Entregues: v1 (`1Y0y7JFlpVYoGrJh23-eGKKFYhDiAQ33M`), v2 (`1Z0EMDb8pr1w_IDYuCkT_qhl8hiYYlrS9`).

## Pendências
- [ ] Nome do cliente (divulgado(s) vs STALO) — confirmar com Zanatto. Legenda atual usa "DIVULGADORES".
- [x] Reconstruir ambiente pós-disco: ffmpeg 7.0.2 restaurado, takes rebaixados, máscaras refeitas (524 frames + defringe), render V4 entregue.
- [x] `colorbalance` — evitado; grade usa `eq` apenas (neutro).
- [ ] Spill roxo no pescoço (luz de recorte da filmagem original) — se Zanatto quiser, fazer correção seletiva de matiz.

## V4 entregue (2026-09-12)
- Arquivo: `Criativo_19_Contratos_30_Dias_v4.mp4` — Drive id `1_wwg08EFM0cOOCiTBRi3N3EXAQ4blfdl` (pasta "Marcelo 01").
- Pipeline V4: bg IA (dourado+roxo) + sujeito rembg/u2net + defringe + eq + zoompan + xfade + legenda (caixa preta semitransparente; CTA em caixa roxa sólida + texto branco) + música (volume 0.15) + loudnorm.
- Lição nova: `scale` derruba o alpha antes do `alphaextract` → split ANTES do scale (alphaextract no RGBA cru, depois scale).
- `acrossfade` aceita só 2 entradas → encadear: [a][b]acrossfade → [ab][c]acrossfade.

## V5 (2026-09-12) — feedback 3: cortar "pode ir" + vídeo original
- Feedback Zanatto (áudio): (1) "pode ir" ainda no comecinho — "tá vacilando nisso"; (2) fundo de IA ficou "horroroso"; (3) restante dos cortes/áudio aprovados. Depois: "esquece esse fundo, deixa com o vídeo original".
- **Cue "pode ir" é DOIS eventos de energia**: "pode" 1.58–1.74s + "ir" 1.96–2.14s; fala real "esse é…" inicia 2.44s. O trim antigo (2.20s) pegava o rabo do "ir". **Lições**: (a) usar RMS da forma de onda + word_timestamps do whisper; (b) cortar DEPOIS do cue COMPLETO (não no meio).
- **Decisão: NÃO trocar fundo.** V5 usa o vídeo ORIGINAL (sem rembg, sem bg de IA). Pipeline: trim + `eq` + zoompan + xfade + legenda + música. Máscara/bg ficaram fora.
- Legenda seg1 recuou -0.20s (corte agora em 2.40s). Trims V5: seg1 2.40→7.90 | seg2 1.50→7.55 | seg3 2.55→8.40.
- **Drive mudou de estado pós-migração**: pasta "Marcelo 01" (`1Pi3Tntw5_1kwRVAAZYorVzXY5vhz8yDw`) e V4 (`1_wwg08EFM0cOOCiTBRi3N3EXAQ4blfdl`) retornam 404. V5 subido na RAIZ: `Criativo_19_Contratos_30_Dias_v5.mp4` id `1SdIbQy3n17MnfdXXini24UDSH2GOSSqc` (13.7MB).

## Estado pós-incidente (2026-09-10 ~18:20)
- DISCO CHEIO → ambiente travou. **Perdidos**: `bin/` (ffmpeg/ffprobe), `jobs/` (takes, máscaras 597 frames, renders v001–v004, captions.ass, bg_premium.jpg).
- **Salvos**: MEMORY/IDENTITY/SOUL/USER/TOOLS.md, `system/VIDEOMAKER.md`, `scripts/*`, `references/fitto/*`.
- Python (rembg, onnxruntime, opencv, numpy) em `~/.local` — provavelmente intacto (verificar).

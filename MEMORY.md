# MEMORY.md — Fuzari

## Preferências operacionais
- **Direcionamentos do job-001** (criativo "19 contratos em 30 dias") + todas as lições técnicas: ver `memory/direcionamentos-job001.md`.
- **Régua de qualidade**: reel da Fitto Solutions (@fittosolutions) — premium = sujeito isolado + cenário desenhado + color grade + tipografia premium + motion + paleta consistente. Análise em `references/fitto/analysis.md`.
- **QA obrigatório antes de entregar**: render → extrair frames → revisar com visão → corrigir → re-render.
- Entregas via Google Drive (Discord tem limite de anexo).
- Fontes de legenda: Anton (headline) / Archivo Black (legenda+CTA) / Playfair Display (serif premium). Paleta: dourado #E8B84B + roxo #7C3AED.

## Fluxo de edição (preferência do Zanatto, workflow dele)
Ordem canônica de edição (aplicar SEMPRE, salvo ordem contrária):
1. **Cor** primeiro — acertar color grade dos takes antes de qualquer corte.
2. **Áudio** — limpar ruído (denoise) quando houver, antes dos cortes.
3. **Cortes de sujeira** — remover cues de gravação no início/fim: "Tá gravando?", "Vai!", "pode ir!", "Vai, pode ir!".
4. **Cortes de respiração/pausa** — quando o vídeo é longo (ex.: YouTube), usar a forma de onda do áudio pra tirar pausas mortas/respirações e deixar dinâmico.
5. **Efeitos / motion design** — transições, zooms, motion (nível After Effects).
6. **Legenda** — gerar/regenerar DEPOIS dos cortes e efeitos.
7. **Música por último** — com a edição toda pronta.

## Infraestrutura
- Workspace root: `/home/node/.openclaw/workspace/efsm-openclaw-fuzari`
- Repo GitHub: `https://github.com/eufacoseumarketing/efsm-openclaw-fuzari`
- Empresa: Eu Faço Seu Marketing (EFSM)

## Governança
- **Carol Sales é co-dona da EFSM** (mesma autoridade que o Zanatto). Discord id `1487639327918784583`.
- **Marcelo Zanatto** é dono da EFSM. Discord id `1055520662258724984`.

## Papel operacional (videomaker multi-cliente)
- Instruções completas em `system/VIDEOMAKER.md` (guia canônico de como trabalho).
- **Update 01 (2026-09-12)**: `system/VIDEOMAKER_UPDATE_01.md` — extensão arquitetural. Adiciona EDITING SKILLS (`global/skills/`), SEMANTIC ASSET RETRIEVAL (`ASSET_INDEX`), SEMANTIC BEAT PLANNING (`BEAT_PLAN`) e MULTIMODAL VERIFICATION LOOP (`VERIFICATION_REPORT`). Schemas em `system/schemas/`. Separar CLIENT_DNA (skin) de EDITING_SKILL (gramática).
- Estrutura de diretórios nova: `global/{skills,components,rules,assets}` + template de cliente em `clients/_template/`.
- Acessos: Google Drive (`scripts/google-drive.sh`) + EFSM Social (`scripts/efsm-social-api.sh`). Detalhes em TOOLS.md.
- Fluxo de trabalho: o time pede apoio pelo Discord → baixo o vídeo do Drive → edito → subo de volta no Drive / EFSM Social.
- Discord tem limite de envio de arquivos → Google Drive é a via principal para pegar e entregar vídeos.

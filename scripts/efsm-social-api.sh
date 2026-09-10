#!/usr/bin/env bash
# ============================================================
# efsm-social-api.sh — Wrapper reutilizável para a EFSM Social API
# Workspace: efsm-openclaw-fuzari (Fuzari)
#
# Uso:
#   bash efsm-social-api.sh <METHOD> <ENDPOINT> [JSON_BODY]
#
# Exemplos:
#   bash efsm-social-api.sh GET /clients
#   bash efsm-social-api.sh GET /plannings
#   bash efsm-social-api.sh POST /posts '{"title_internal":"Teste","caption":"..."}'
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDS_FILE="$(dirname "$SCRIPT_DIR")/apis/efsm-social/credentials.env"

if [ -f "$CREDS_FILE" ]; then
  export $(grep -v '^#' "$CREDS_FILE" | xargs)
else
  echo "ERRO: Credenciais não encontradas em $CREDS_FILE" >&2
  exit 1
fi

METHOD="${1:-GET}"
ENDPOINT="${2:-/clients}"
BODY="${3:-}"
URL="${EFSM_BASE_URL}${ENDPOINT}"

if [ -n "$BODY" ] && [ "$METHOD" != "GET" ] && [ "$METHOD" != "DELETE" ]; then
  curl -s -X "$METHOD" "$URL" \
    -H "X-API-Key: $EFSM_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$BODY" | python3 -m json.tool 2>/dev/null || cat
else
  curl -s -X "$METHOD" "$URL" \
    -H "X-API-Key: $EFSM_API_KEY" | python3 -m json.tool 2>/dev/null || cat
fi

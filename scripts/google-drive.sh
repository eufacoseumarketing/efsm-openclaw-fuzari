#!/usr/bin/env bash
# ============================================================
# google-drive.sh — Wrapper Google Drive (leitura) para o Fuzari
# Workspace: efsm-openclaw-fuzari
# Escopo: drive.readonly (SOMENTE LEITURA)
# Usuário: interno@eufacoseu.marketing
#
# Uso:
#   bash google-drive.sh token            → imprime access_token fresco
#   bash google-drive.sh list [query]     → lista arquivos (opcional: busca por nome)
#   bash google-drive.sh get <fileId>     → metadados de um arquivo
#   bash google-drive.sh download <fileId> <dest> → baixa um arquivo
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDS_FILE="$(dirname "$SCRIPT_DIR")/apis/google-drive/credentials.env"

if [ -f "$CREDS_FILE" ]; then
  export $(grep -v '^#' "$CREDS_FILE" | xargs)
else
  echo "ERRO: Credenciais não encontradas em $CREDS_FILE" >&2
  exit 1
fi

get_token() {
  curl -s -X POST https://oauth2.googleapis.com/token \
    -d "client_id=$GOOGLE_DRIVE_CLIENT_ID" \
    -d "client_secret=$GOOGLE_DRIVE_CLIENT_SECRET" \
    -d "refresh_token=$GOOGLE_DRIVE_REFRESH_TOKEN" \
    -d "grant_type=refresh_token" \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))"
}

CMD="${1:-token}"
shift || true

case "$CMD" in
  token)
    get_token
    ;;
  list)
    TOKEN=$(get_token)
    QUERY="${1:-}"
    if [ -n "$QUERY" ]; then
      curl -s "https://www.googleapis.com/drive/v3/files?pageSize=20&q=name%20contains%20%27$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")%27&fields=files(id,name,mimeType,size,modifiedTime)" \
        -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
    else
      curl -s "https://www.googleapis.com/drive/v3/files?pageSize=20&fields=files(id,name,mimeType,size,modifiedTime)" \
        -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
    fi
    ;;
  get)
    TOKEN=$(get_token)
    curl -s "https://www.googleapis.com/drive/v3/files/$1?fields=id,name,mimeType,size,webViewLink,modifiedTime" \
      -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
    ;;
  download)
    TOKEN=$(get_token)
    FILE_ID="$1"
    DEST="${2:-./$FILE_ID}"
    curl -sL "https://www.googleapis.com/drive/v3/files/$FILE_ID?alt=media" \
      -H "Authorization: Bearer $TOKEN" -o "$DEST"
    echo "✅ baixado para $DEST ($(wc -c < "$DEST") bytes)"
    ;;
  *)
    echo "Uso: bash google-drive.sh {token|list [query]|get <id>|download <id> <dest>}" >&2
    exit 1
    ;;
esac

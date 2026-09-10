#!/usr/bin/env bash
# ============================================================
# google-drive.sh — Wrapper Google Drive (leitura + ESCRITA) para o Fuzari
# Workspace: efsm-openclaw-fuzari
# Escopo: drive (completo — ler, criar, editar, excluir)
# Usuário: interno@eufacoseu.marketing
#
# Uso:
#   bash google-drive.sh token            → imprime access_token fresco
#   bash google-drive.sh list [query]     → lista arquivos (opcional: busca por nome)
#   bash google-drive.sh get <fileId>     → metadados de um arquivo
#   bash google-drive.sh download <fileId> <dest> → baixa um arquivo
#   bash google-drive.sh upload <arquivo> [pastaId] → envia um arquivo
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
  upload)
    TOKEN=$(get_token)
    SRC_FILE="$1"
    FOLDER_ID="${2:-}"
    if [ ! -f "$SRC_FILE" ]; then
      echo "❌ Arquivo não encontrado: $SRC_FILE" >&2
      exit 1
    fi
    python3 - "$SRC_FILE" "$FOLDER_ID" "$TOKEN" <<'PYEOF'
import sys, json, urllib.request, mimetypes, os
src, folder, token = sys.argv[1], sys.argv[2], sys.argv[3]
name = os.path.basename(src)
mime = mimetypes.guess_type(src)[0] or "application/octet-stream"
boundary = "openclaw_fuzari_boundary"
meta = {"name": name}
if folder:
    meta["parents"] = [folder]
body = ("--%s\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n%s\r\n" % (boundary, json.dumps(meta)))
body += ("--%s\r\nContent-Type: %s\r\n\r\n" % (boundary, mime))
body = body.encode("utf-8") + open(src, "rb").read()
body += ("\r\n--%s--\r\n" % boundary).encode("utf-8")
req = urllib.request.Request(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    data=body,
    headers={"Authorization": "Bearer " + token, "Content-Type": "multipart/related; boundary=%s" % boundary},
)
try:
    r = urllib.request.urlopen(req)
    d = json.load(r)
    print("✅ enviado: %s (id=%s)" % (d.get("name"), d.get("id")))
except urllib.error.HTTPError as e:
    print("❌ ERRO %s: %s" % (e.code, e.read().decode()[:300]))
    sys.exit(1)
PYEOF
    ;;
  *)
    echo "Uso: bash google-drive.sh {token|list [query]|get <id>|download <id> <dest>|upload <arquivo> [pastaId]}" >&2
    exit 1
    ;;
esac

#!/usr/bin/env bash
# ============================================================
# google-drive-auth.sh — Gera refresh token OAuth2 do Google Drive (ESCRITA)
# Workspace: efsm-openclaw-fuzari (Fuzari)
#
# Este script faz o fluxo "Desktop App" (loopback) manual:
#   1. Monta a URL de autorização
#   2. Você abre no navegador, autoriza e copia o "code" da URL
#   3. O script troca o code por um refresh_token permanente
#
# Uso:
#   bash google-drive-auth.sh <CLIENT_ID> <CLIENT_SECRET> [SCOPE]
#
#   SCOPE padrão: https://www.googleapis.com/auth/drive (leitura + escrita)
#   Alternativa menos privilegiada: https://www.googleapis.com/auth/drive.file
# ============================================================

set -euo pipefail

CLIENT_ID="${1:-}"
CLIENT_SECRET="${2:-}"
SCOPE="${3:-https://www.googleapis.com/auth/drive}"
REDIRECT_URI="http://localhost"

if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
  echo "Uso: bash google-drive-auth.sh <CLIENT_ID> <CLIENT_SECRET> [SCOPE]" >&2
  echo "Exemplo: bash google-drive-auth.sh 3982...apps.googleusercontent.com GOCSPX-... 'https://www.googleapis.com/auth/drive'" >&2
  exit 1
fi

echo "============================================================="
echo " PASSO 1 — Abra esta URL no navegador (logado no Google da EFSM):"
echo "============================================================="
echo ""
python3 - "$CLIENT_ID" "$SCOPE" "$REDIRECT_URI" <<'PYEOF'
import sys, urllib.parse
cid, scope, redirect = sys.argv[1], sys.argv[2], sys.argv[3]
params = {
    "client_id": cid,
    "redirect_uri": redirect,
    "response_type": "code",
    "scope": scope,
    "access_type": "offline",
    "prompt": "consent",
    "include_granted_scopes": "true",
}
print("https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode(params))
PYEOF
echo ""
echo "============================================================="
echo " PASSO 2 — Depois de autorizar, o Google redireciona para:"
echo "   http://localhost/?code=XXXXX&scope=..."
echo "   (a página pode dar 'não é possível acessar' — é NORMAL)"
echo "   Copie o valor de 'code=' (tudo entre code= e &scope)."
echo "============================================================="
echo ""
read -r -p "Cole aqui o código (code): " AUTH_CODE

if [ -z "$AUTH_CODE" ]; then
  echo "❌ Nenhum código informado." >&2
  exit 1
fi

echo ""
echo "============================================================="
echo " PASSO 3 — Trocando o code por tokens..."
echo "============================================================="

RESP=$(curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "redirect_uri=$REDIRECT_URI" \
  -d "code=$AUTH_CODE" \
  -d "grant_type=authorization_code")

echo "$RESP" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if 'refresh_token' not in d:
    print('❌ ERRO:', d.get('error'), '-', d.get('error_description', '')[:200])
    sys.exit(1)
print()
print('✅ SUCESSO! Copie os 3 valores abaixo e me envie (ou salve no credentials.env):')
print()
print('GOOGLE_DRIVE_CLIENT_ID=' + repr('$CLIENT_ID').strip(\"'\") )
print('GOOGLE_DRIVE_CLIENT_SECRET=' + repr('$CLIENT_SECRET').strip(\"'\") )
print('GOOGLE_DRIVE_REFRESH_TOKEN=' + d['refresh_token'])
print()
print('scope concedido:', d.get('scope'))
"

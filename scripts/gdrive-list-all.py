#!/usr/bin/env python3
"""Lista TODOS os arquivos/pastas acessíveis (owned + compartilhados), sem filtros extras."""
import json, os, urllib.request, urllib.parse

CREDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "apis", "google-drive", "credentials.env")

def load_creds():
    env = {}
    with open(CREDS) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k] = v.strip().strip('"').strip("'")
    return env

def get_token(env):
    data = urllib.parse.urlencode({
        "client_id": env["GOOGLE_DRIVE_CLIENT_ID"],
        "client_secret": env["GOOGLE_DRIVE_CLIENT_SECRET"],
        "refresh_token": env["GOOGLE_DRIVE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req) as r:
        return json.load(r)["access_token"]

env = load_creds()
tok = get_token(env)
url = "https://www.googleapis.com/drive/v3/files?pageSize=100&fields=files(id,name,mimeType,size,modifiedTime,ownedByMe)"
req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
print(json.dumps(data, ensure_ascii=False, indent=2))

#!/usr/bin/env python3
"""Cria uma pasta no Drive e abre permissão 'qualquer pessoa com o link pode editar'."""
import sys, json, os, urllib.request, urllib.parse

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

def call(token, method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": "Bearer " + token,
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()[:300]}

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Fuzari - Vídeos Recebidos"
    env = load_creds()
    token = get_token(env)
    created = call(token, "POST", "https://www.googleapis.com/drive/v3/files?fields=id,name,mimeType,webViewLink",
                   {"name": name, "mimeType": "application/vnd.google-apps.folder"})
    if "error" in created:
        print(json.dumps(created, ensure_ascii=False, indent=2))
        sys.exit(1)
    fid = created["id"]
    perm = call(token, "POST", "https://www.googleapis.com/drive/v3/files/%s/permissions?fields=id,type,role" % fid,
                {"type": "anyone", "role": "writer"})
    print(json.dumps({"folder": created, "permission": perm}, ensure_ascii=False, indent=2))
    print("\nLINK: https://drive.google.com/drive/folders/%s" % fid)

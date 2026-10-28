#!/usr/bin/env python3
"""Lista o conteúdo de uma pasta do Google Drive e checa acesso."""
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

def api(token, path):
    req = urllib.request.Request("https://www.googleapis.com/drive/v3/" + path,
                                 headers={"Authorization": "Bearer " + token})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")

if __name__ == "__main__":
    folder = sys.argv[1]
    env = load_creds()
    token = get_token(env)

    status, meta = api(token, "files/%s?fields=id,name,mimeType" % folder)
    print("=== PASTA ===")
    print("status:", status)
    print(json.dumps(meta, ensure_ascii=False, indent=2))

    q = urllib.parse.quote("'%s' in parents" % folder)
    status2, listing = api(token, "files?pageSize=100&q=%s&fields=files(id,name,mimeType,size,modifiedTime)&orderBy=name" % q)
    print("=== CONTEÚDO ===")
    print("status:", status2)
    print(json.dumps(listing, ensure_ascii=False, indent=2))

#!/usr/bin/env python3
"""Busca arquivos por nome no Drive da conta interna."""
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
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()[:300]}

if __name__ == "__main__":
    term = sys.argv[1]
    env = load_creds()
    token = get_token(env)
    q = urllib.parse.quote("name contains '%s'" % term)
    res = api(token, "files?pageSize=50&q=%s&fields=files(id,name,mimeType,size,modifiedTime,parents)" % q)
    print(json.dumps(res, ensure_ascii=False, indent=2))

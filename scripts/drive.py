#!/usr/bin/env python3
"""drive.py — Helper Google Drive (Drive API v3) com suporte a Shared Drives.

Uso:
  python3 scripts/drive.py token
  python3 scripts/drive.py list [query]
  python3 scripts/drive.py folder <folderId>
  python3 scripts/drive.py get <fileId>
  python3 scripts/drive.py download <fileId> <dest>
  python3 scripts/drive.py upload <arquivo> [folderId]
"""
import sys, os, json, urllib.request, urllib.parse, urllib.error, mimetypes

CREDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "apis", "google-drive", "credentials.env")


def load_creds():
    creds = {}
    for line in open(CREDS):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            creds[k] = v
    return creds


def get_token():
    creds = load_creds()
    data = urllib.parse.urlencode({
        "client_id": creds["GOOGLE_DRIVE_CLIENT_ID"],
        "client_secret": creds["GOOGLE_DRIVE_CLIENT_SECRET"],
        "refresh_token": creds["GOOGLE_DRIVE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    r = urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data))
    return json.load(r)["access_token"]


# parâmetros necessários para enxergar Shared Drives
SD = "supportsAllDrives=true&includeItemsFromAllDrives=true&corpora=allDrives"


def api_get(url):
    req = urllib.request.Request(url)
    req.add_header("Authorization", "Bearer " + get_token())
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        return {"HTTPError": e.code, "body": e.read().decode()[:400]}


def cmd_token():
    print(get_token())


def cmd_list(query=None):
    if query:
        q = urllib.parse.quote(f"name contains '{query}'")
        url = f"https://www.googleapis.com/drive/v3/files?pageSize=50&q={q}&{SD}&fields=files(id,name,mimeType,size,driveId,modifiedTime)"
    else:
        url = f"https://www.googleapis.com/drive/v3/files?pageSize=50&{SD}&fields=files(id,name,mimeType,size,driveId,modifiedTime)"
    print(json.dumps(api_get(url), ensure_ascii=False, indent=2))


def cmd_folder(folder_id):
    q = urllib.parse.quote(f"'{folder_id}' in parents")
    url = f"https://www.googleapis.com/drive/v3/files?q={q}&pageSize=100&{SD}&fields=files(id,name,mimeType,size,driveId,modifiedTime)&orderBy=name"
    print(json.dumps(api_get(url), ensure_ascii=False, indent=2))


def cmd_get(file_id):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?supportsAllDrives=true&fields=id,name,mimeType,size,driveId,webViewLink,modifiedTime,parents"
    print(json.dumps(api_get(url), ensure_ascii=False, indent=2))


def cmd_download(file_id, dest):
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&supportsAllDrives=true"
    req = urllib.request.Request(url)
    req.add_header("Authorization", "Bearer " + get_token())
    try:
        with urllib.request.urlopen(req) as r, open(dest, "wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
        print(f"✅ baixado para {dest} ({os.path.getsize(dest)} bytes)")
    except urllib.error.HTTPError as e:
        print(f"❌ ERRO {e.code}: {e.read().decode()[:300]}")
        sys.exit(1)


def cmd_upload(src, folder_id=None):
    if not os.path.isfile(src):
        print(f"❌ Arquivo não encontrado: {src}")
        sys.exit(1)
    name = os.path.basename(src)
    mime = mimetypes.guess_type(src)[0] or "application/octet-stream"
    boundary = "openclaw_fuzari_boundary"
    meta = {"name": name}
    if folder_id:
        meta["parents"] = [folder_id]
    body = (
        f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n"
        f"--{boundary}\r\nContent-Type: {mime}\r\n\r\n"
    ).encode("utf-8") + open(src, "rb").read() + f"\r\n--{boundary}--\r\n".encode("utf-8")
    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true"
    req = urllib.request.Request(url, data=body)
    req.add_header("Authorization", "Bearer " + get_token())
    req.add_header("Content-Type", f"multipart/related; boundary={boundary}")
    try:
        d = json.load(urllib.request.urlopen(req))
        print(f"✅ enviado: {d.get('name')} (id={d.get('id')})")
    except urllib.error.HTTPError as e:
        print(f"❌ ERRO {e.code}: {e.read().decode()[:300]}")
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd = args[0]
    if cmd == "token":
        cmd_token()
    elif cmd == "list":
        cmd_list(args[1] if len(args) > 1 else None)
    elif cmd == "folder":
        cmd_folder(args[1])
    elif cmd == "get":
        cmd_get(args[1])
    elif cmd == "download":
        cmd_download(args[1], args[2])
    elif cmd == "upload":
        cmd_upload(args[1], args[2] if len(args) > 2 else None)
    else:
        print(__doc__)
        sys.exit(1)

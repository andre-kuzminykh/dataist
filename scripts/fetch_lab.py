#!/usr/bin/env python3
"""Fetch all @dataist_lab channel posts (back to SINCE) + their Telegraph content,
then upload the raw dump to the `dataist` repo via the GitHub API.

Run on a host WITH internet access (the VM). No external deps (stdlib only).

    python3 scripts/fetch_lab.py                 # channel=dataist_lab, since=2026-03-01
    python3 scripts/fetch_lab.py dataist_lab 2026-03-01

The GitHub token is read from /opt/dataist_media/.env (any ghp_/github_pat_),
or from the GH_TOKEN env var. The dump is pushed to `_lab_dump.json` on main.
"""
import json, os, re, sys, time, base64, urllib.request, urllib.error
from datetime import datetime

CHANNEL = sys.argv[1] if len(sys.argv) > 1 else "dataist_lab"
SINCE   = sys.argv[2] if len(sys.argv) > 2 else "2026-03-01"
REPO    = "andre-kuzminykh/dataist"
since_d = datetime.strptime(SINCE, "%Y-%m-%d").date()
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"


def get_token():
    t = os.environ.get("GH_TOKEN")
    if t:
        return t.strip()
    try:
        env = open("/opt/dataist_media/.env", encoding="utf-8").read()
        m = re.search(r"(ghp_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)", env)
        if m:
            return m.group(1)
    except OSError:
        pass
    sys.exit("No GitHub token (set GH_TOKEN or put it in /opt/dataist_media/.env)")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


# ---- 1. scrape the public channel feed (paginated via ?before=) ----
posts = {}
before = None
while True:
    url = f"https://t.me/s/{CHANNEL}" + (f"?before={before}" if before else "")
    try:
        html = fetch(url)
    except Exception as e:
        print("fetch channel failed:", e); break
    blocks = re.split(r'(?=<div class="tgme_widget_message[ "])', html)
    ids = []
    for b in blocks:
        m = re.search(r'data-post="%s/(\d+)"' % re.escape(CHANNEL), b)
        if not m:
            continue
        mid = int(m.group(1)); ids.append(mid)
        dt = re.search(r'<time[^>]+datetime="([^"]+)"', b)
        date = None
        if dt:
            try:
                date = datetime.fromisoformat(dt.group(1)).date().isoformat()
            except ValueError:
                pass
        links = sorted(set(re.findall(r'href="(https?://telegra\.ph/[^"&]+)"', b)))
        posts[mid] = {"id": mid, "date": date, "links": links}
    if not ids:
        break
    oldest = min(ids)
    od = posts[oldest]["date"]
    print(f"  page: {len(ids)} msgs, oldest #{oldest} ({od})")
    if od and datetime.fromisoformat(od).date() < since_d:
        break
    if before == oldest:
        break
    before = oldest
    time.sleep(0.5)

selected = [p for p in posts.values()
            if p["date"] and datetime.fromisoformat(p["date"]).date() >= since_d and p["links"]]
selected.sort(key=lambda p: p["date"])
print(f"{len(selected)} posts with a telegra.ph link since {SINCE}")

# ---- 2. fetch each Telegraph page's content ----
out = []
for p in selected:
    link = p["links"][-1]
    path = link.split("telegra.ph/")[-1].split("?")[0].split("#")[0]
    try:
        data = get_json(f"https://api.telegra.ph/getPage/{path}?return_content=true")
        page = data["result"] if data.get("ok") else None
    except Exception as e:
        print("  ERR", link, e); page = None
    if not page:
        continue
    out.append({
        "channel_post_id": p["id"],
        "channel_date": p["date"],
        "telegraph_url": link,
        "title": page.get("title"),
        "author": page.get("author_name"),
        "content": page.get("content", []),
    })
    print("  OK", p["date"], "|", page.get("title"))
    time.sleep(0.3)

# ---- 3. upload dump to the repo via GitHub API ----
TOKEN = get_token()
payload = json.dumps(out, ensure_ascii=False, indent=2)
open("lab_dump.json", "w", encoding="utf-8").write(payload)  # local copy too
b64 = base64.b64encode(payload.encode("utf-8")).decode()

def api(method, path, data=None):
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}{path}", data=data, method=method)
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "fetch-lab")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

st, body = api("GET", "/contents/_lab_dump.json?ref=main")
sha = body.get("sha") if st == 200 else None
data = {"message": "Add dataist_lab raw dump", "content": b64, "branch": "main"}
if sha:
    data["sha"] = sha
st, body = api("PUT", "/contents/_lab_dump.json", json.dumps(data).encode())
print("upload _lab_dump.json:", st, "->", body.get("commit", {}).get("sha", "?")[:8] if st < 300 else json.dumps(body)[:200])
print(f"DONE: {len(out)} articles dumped.")

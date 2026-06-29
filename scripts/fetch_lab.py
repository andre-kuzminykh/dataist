#!/usr/bin/env python3
"""Fetch all @dataist_lab channel posts (back to SINCE) + their Telegraph content,
then upload the raw dump to the `dataist` repo via the GitHub API.

Run on a host WITH internet access (the VM). No external deps (stdlib only).

    python3 scripts/fetch_lab.py                 # channel=dataist_lab, since=2026-03-01
    GH_TOKEN=ghp_xxx python3 scripts/fetch_lab.py dataist_lab 2026-03-01
"""
import json, os, re, sys, time, base64, subprocess, urllib.request, urllib.error
from datetime import datetime
from urllib.parse import unquote

CHANNEL = sys.argv[1] if len(sys.argv) > 1 else "dataist_lab"
SINCE   = sys.argv[2] if len(sys.argv) > 2 else "2020-01-01"   # selection floor; default = all
REPO    = "andre-kuzminykh/dataist"
MAX_PAGES = 40
since_d = datetime.strptime(SINCE, "%Y-%m-%d").date()
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

# Telegraph + its mirror graph.org (+ rare te.legra.ph). Instant-view links
# wrap the URL encoded inside t.me/iv?url=... — we unquote the block first.
TG_RE = re.compile(r'https?://(?:telegra\.ph|graph\.org|te\.legra\.ph)/[^\s"\'<>&]+')
ANY_HREF = re.compile(r'href="(https?://[^"]+)"')


def get_token():
    t = os.environ.get("GH_TOKEN")
    if t:
        return t.strip()
    pat = re.compile(r"(ghp_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)")
    for p in ("/opt/dataist_media/.env", "/home/admin_/dataist-ai/.env",
              "/home/admin_/dataist_media/.env"):
        try:
            m = pat.search(open(p, encoding="utf-8").read())
            if m:
                return m.group(1)
        except OSError:
            pass
    for d in ("/home/admin_/dataist-content", "/home/admin_/dataist-ai"):
        try:
            url = subprocess.check_output(["git", "-C", d, "remote", "get-url", "origin"],
                                          text=True, stderr=subprocess.DEVNULL).strip()
            m = pat.search(url)
            if m:
                return m.group(1)
        except Exception:
            pass
    return None


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
all_hrefs = set()
sample_block = ""
before = None
for _page in range(MAX_PAGES):
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
        if not sample_block:
            sample_block = b[:1200]
        dt = re.search(r'<time[^>]+datetime="([^"]+)"', b)
        date = None
        if dt:
            try:
                date = datetime.fromisoformat(dt.group(1)).date().isoformat()
            except ValueError:
                pass
        dec = unquote(b)                       # unwrap iv?url=encoded links
        links = sorted(set(TG_RE.findall(dec)))
        for h in ANY_HREF.findall(b):
            all_hrefs.add(h)
        posts[mid] = {"id": mid, "date": date, "links": links}
    if not ids:
        break
    oldest = min(ids)
    print(f"  page: {len(ids)} msgs, oldest #{oldest} ({posts[oldest]['date']})")
    if before == oldest:        # no progress → reached the start of the channel
        break
    before = oldest             # paginate to the very beginning (no date cut-off)
    time.sleep(0.5)

# Select posts that CONTAIN a telegraph link (those are the ones to import).
# Posts that only link to dataist.ai are already-published articles → skipped.
selected = [p for p in posts.values()
            if p["links"] and (not p["date"] or datetime.fromisoformat(p["date"]).date() >= since_d)]
selected.sort(key=lambda p: p["date"] or "0000")
print(f"{len(selected)} posts WITH a telegraph link (of {len(posts)} scanned)")

if not selected:
    print("\n--- DEBUG: no telegraph links found ---")
    ext = sorted(h for h in all_hrefs if "t.me" not in h)[:25]
    print("sample external links:")
    for h in ext:
        print("   ", h[:160])
    print("\nsample message HTML (first block, 1200 chars):")
    print(sample_block)
    print("--- end debug ---")

# ---- 2. fetch each Telegraph page's content ----
out = []
for p in selected:
    link = p["links"][-1]
    path = re.sub(r'https?://(?:telegra\.ph|graph\.org|te\.legra\.ph)/', '', link).split("?")[0].split("#")[0]
    page = None
    for api_host in ("https://api.telegra.ph", "https://api.graph.org"):
        try:
            data = get_json(f"{api_host}/getPage/{path}?return_content=true")
            if data.get("ok"):
                page = data["result"]; break
        except Exception as e:
            last = e
    if not page:
        print("  ERR getPage", link); continue
    out.append({
        "channel_post_id": p["id"], "channel_date": p["date"], "telegraph_url": link,
        "title": page.get("title"), "author": page.get("author_name"),
        "content": page.get("content", []),
    })
    print("  OK", p["date"], "|", page.get("title"))
    time.sleep(0.3)

# ---- 3. upload dump to the repo via GitHub API (also keep local copy) ----
payload = json.dumps(out, ensure_ascii=False, indent=2)
open("lab_dump.json", "w", encoding="utf-8").write(payload)
print(f"\nwrote local lab_dump.json ({len(out)} articles)")

TOKEN = get_token()
if not TOKEN:
    print("No GitHub token found. Local lab_dump.json is written; "
          "re-run with GH_TOKEN=ghp_xxx to also upload, or send the file.")
    sys.exit(0)

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
ok = st < 300
print("upload _lab_dump.json:", st, "->",
      (body.get("commit", {}).get("sha", "?")[:8] if ok else json.dumps(body)[:200]))
print(f"DONE: {len(out)} articles dumped.")

#!/usr/bin/env python3
"""Check every posting_url / website_or_linkedin in data.json (Python stdlib only).

Status per URL:
  dead        HTTP 404/410, DNS failure, or an obvious "expired"/"no longer accepting" marker
  suspect     redirected to a generic jobs/search/careers page (job id lost)
  unverified  403/429/999, timeouts or other blocked responses (JobStreet, Indeed, LinkedIn); never "dead"
  ok          everything else

Never modifies data.json. --dry-run prints only; otherwise a Markdown report is written to --report.
Exit code: 1 if any link is dead, else 0 (suspect/unverified never fail the run).
"""
import argparse, json, re, socket, ssl, sys, time, urllib.error, urllib.parse, urllib.request

MARKERS = re.compile(
    r"no longer accepting applications|this job (has )?expired|job (posting )?(is )?no longer available"
    r"|this job is no longer|position has been filled", re.I)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
GENERIC_PATH = re.compile(r"^/(?:[a-z]{2}(?:-[a-z]{2})?/)?(jobs?|search|careers?|job-search|jobsearch|login|authwall)?/?$", re.I)


def job_ids(url):
    return set(re.findall(r"\d{5,}", url))


def is_suspect_redirect(orig, final):
    if not final or final.rstrip("/") == orig.rstrip("/"):
        return False
    lost_id = bool(job_ids(orig)) and not (job_ids(orig) & job_ids(final))
    generic = bool(GENERIC_PATH.match(urllib.parse.urlparse(final).path or "/"))
    return lost_id or (generic and not GENERIC_PATH.match(urllib.parse.urlparse(orig).path or "/"))


def check(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as r:
            final = r.geturl()
            body = r.read(400_000).decode("utf-8", "ignore")
            if MARKERS.search(body):
                return "dead", f"{r.status} but page says expired/closed"
            if is_suspect_redirect(url, final):
                return "suspect", f"{r.status} redirected to generic page {final}"
            return "ok", str(r.status)
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return "dead", f"HTTP {e.code}"
        return "unverified", f"HTTP {e.code}"
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.gaierror):
            return "dead", f"DNS failure ({e.reason})"
        return "unverified", f"network error ({e.reason})"
    except Exception as e:  # timeouts, resets, etc.
        return "unverified", f"{type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data.json")
    ap.add_argument("--dry-run", action="store_true", help="print only, write no report")
    ap.add_argument("--report", default="link-report.md")
    ap.add_argument("--limit", type=int, default=0, help="check at most N URLs (0 = all)")
    ap.add_argument("--delay", type=float, default=1.5, help="seconds between requests (default 1.5)")
    a = ap.parse_args()
    entries = json.load(open(a.data, encoding="utf-8"))
    urls = {}
    for e in entries:
        for k in ("posting_url", "website_or_linkedin"):
            u = (e.get(k) or "").strip()
            if u:
                urls.setdefault(u, f"{e.get('company', '').strip()} - {e.get('roles_or_projects', '').strip()}")
    todo = sorted(urls.items())
    if a.limit > 0:
        todo = todo[: a.limit]
    res = {"ok": [], "dead": [], "suspect": [], "unverified": []}
    for n, (u, who) in enumerate(todo):
        if n:
            time.sleep(max(a.delay, 0))
        status, why = check(u)
        res[status].append((who, u, why))
        print(f"[{status:10}] {why:40} {u}", flush=True)
    summary = (f"{len(todo)} URLs checked, {len(res['ok'])} ok, {len(res['dead'])} dead, "
               f"{len(res['suspect'])} suspect, {len(res['unverified'])} unverified")
    print(f"\nSummary: {summary}")
    lines = [f"Automated link check: {summary}.", "", "## Dead links (404/410, DNS failure, or expired marker)"]
    lines += [f"- {w}: {u} ({y})" for w, u, y in res["dead"]] or ["- none"]
    lines += ["", "## Suspect (redirected to a generic jobs/search/careers page)"]
    lines += [f"- {w}: {u} ({y})" for w, u, y in res["suspect"]] or ["- none"]
    lines += ["", "## Unverified (blocked, 403/429/999, timeouts; NOT necessarily dead)"]
    lines += [f"- {w}: {u} ({y})" for w, u, y in res["unverified"]] or ["- none"]
    lines += ["", "_Updated by `.github/workflows/link-check.yml`. It never edits data.json._"]
    if not a.dry_run:
        with open(a.report, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    return 1 if res["dead"] else 0


if __name__ == "__main__":
    sys.exit(main())

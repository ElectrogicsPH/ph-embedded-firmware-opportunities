#!/usr/bin/env python3
"""Check every posting_url / website_or_linkedin in data.json (stdlib only).

Dead:       HTTP 404/410, DNS failure, or an obvious "expired"/"no longer accepting" marker.
Unverified: 403/429/999 or other blocked/odd responses (JobStreet, Indeed, LinkedIn often block bots).
Never modifies data.json. With --dry-run it only prints; otherwise it writes a Markdown report
to the path given by --report (the workflow turns that into a single issue).
"""
import argparse, json, re, socket, ssl, sys, urllib.error, urllib.request

MARKERS = re.compile(r"no longer accepting applications|this job (has )?expired|job (posting )?(is )?no longer available|this job is no longer|position has been filled", re.I)
UA = "Mozilla/5.0 (compatible; ph-embedded-link-check/1.0; +https://github.com/ElectrogicsPH/ph-embedded-firmware-opportunities)"


def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as r:
            body = r.read(400_000).decode("utf-8", "ignore")
            if MARKERS.search(body):
                return "dead", f"{r.status} but page says expired/closed"
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
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", default="link-report.md")
    a = ap.parse_args()
    entries = json.load(open(a.data, encoding="utf-8"))
    urls = {}
    for e in entries:
        for k in ("posting_url", "website_or_linkedin"):
            u = (e.get(k) or "").strip()
            if u:
                urls.setdefault(u, f"{e.get('company','').strip()} - {e.get('roles_or_projects','').strip()}")
    res = {"ok": [], "dead": [], "unverified": []}
    for u, who in sorted(urls.items()):
        status, why = check(u)
        res[status].append((who, u, why))
        print(f"[{status:10}] {why:40} {u}")
    print(f"\nSummary: {len(urls)} URLs checked, {len(res['ok'])} ok, {len(res['dead'])} dead, {len(res['unverified'])} unverified")
    lines = [f"Automated link check: **{len(res['dead'])} dead**, {len(res['unverified'])} unverified, {len(res['ok'])} ok out of {len(urls)} URLs.", "",
             "## Dead links (404/410, DNS failure, or expired marker)"]
    lines += [f"- {w}: {u} ({y})" for w, u, y in res["dead"]] or ["- none"]
    lines += ["", "## Unverified (blocked, 403/429/999, timeouts; NOT necessarily dead)"]
    lines += [f"- {w}: {u} ({y})" for w, u, y in res["unverified"]] or ["- none"]
    lines += ["", "_This issue is updated by `.github/workflows/link-check.yml`. It never edits data.json._"]
    if not a.dry_run:
        open(a.report, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("DEAD_COUNT=%d" % len(res["dead"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

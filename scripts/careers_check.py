#!/usr/bin/env python3
"""Weekly careers-feed check (Python stdlib only, no AI).

Reads scripts/careers_feeds.json (feeds verified by hand), fetches each public job feed,
keeps postings that look embedded/firmware AND are in the Philippines, drops any whose URL
(or company + title) is already in data.json, and writes a Markdown report for the single
"Careers feed check" issue. Never modifies data.json. --dry-run prints the report only.

A feed error is listed in the report but does not fail the run. Exit code is 0 unless the
script itself crashes.
"""
import argparse, json, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

UA = "ph-embedded-firmware-opportunities careers-check (+https://github.com/ElectrogicsPH/ph-embedded-firmware-opportunities)"
ROLE = re.compile(
    r"firmware|embedded|\bmcu\b|micro-?controller|\brtos\b|bare[- ]?metal|\bbsp\b|board support"
    r"|device driver|\bdrivers?\b.*(linux|kernel)|linux kernel|\bfpga\b|\bverilog\b|\bvhdl\b"
    r"|hardware validation|hardware test|post-?silicon|\bsoc\b|\biot\b|electronics engineer"
    r"|hardware engineer|test (development|equipment) engineer|\bplc\b", re.I)
PH = re.compile(
    r"philippines|\bphl?\b|manila|maynila|makati|taguig|bonifacio|\bbgc\b|cebu|lapu-?lapu|mandaue|laguna"
    r"|calamba|santa rosa|sta\.? rosa|bi[ñn]an|cabuyao|cavite|rosario|gen(eral)? trias|dasmari[ñn]as|imus"
    r"|batangas|lipa|tanauan|pasig|quezon city|eastwood|mandaluyong|ortigas|clark|pampanga|angeles"
    r"|baguio|muntinlupa|alabang|para[ñn]aque|pasay|davao|iloilo|subic|bulacan", re.I)


def fetch(url, data=None, headers=None, timeout=30):
    h = {"User-Agent": UA, "Accept": "application/json, application/xml;q=0.9, */*;q=0.5"}
    h.update(headers or {})
    body = json.dumps(data).encode() if data is not None else None
    if body is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=h, method="POST" if body else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


# Each reader returns a list of dicts: title, location, url, ph_scoped (feed already searched for PH).
def read_workday(f, delay):
    base = f"https://{f['tenant']}.wd{f['wd']}.myworkdayjobs.com"
    out, offset, total = [], 0, None
    while offset < 400:
        d = json.loads(fetch(f"{base}/wday/cxs/{f['tenant']}/{f['site']}/jobs",
                             {"appliedFacets": {}, "limit": 20, "offset": offset, "searchText": f.get("search", "")}))
        posts = d.get("jobPostings") or []
        for p in posts:
            out.append({"title": p.get("title", ""), "location": p.get("locationsText") or "",
                        "url": f"{base}/en-US/{f['site']}{p.get('externalPath', '')}", "ph_scoped": bool(f.get("search"))})
        offset += 20
        if total is None:  # Workday only reports the total on the first page
            total = d.get("total") or 0
        if not posts or offset >= total:
            break
        time.sleep(delay)
    return out


def read_oracle(f, delay):
    searches = f.get("search", "")
    out = []
    for n, term in enumerate(searches if isinstance(searches, list) else [searches]):
        if n:
            time.sleep(delay)
        out += read_oracle_one(f, term, delay)
    return out


def read_oracle_one(f, term, delay):
    out, offset = [], 0
    while offset < 400:
        q = (f"https://{f['host']}/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true"
             f"&expand=requisitionList&finder=findReqs;siteNumber={f['site']},"
             f"keyword={urllib.parse.quote(term)},limit=25,offset={offset}")
        item = (json.loads(fetch(q)).get("items") or [{}])[0]
        reqs = item.get("requisitionList") or []
        for r in reqs:
            out.append({"title": r.get("Title", ""), "location": r.get("PrimaryLocation") or "",
                        "url": f"https://{f['host']}/hcmUI/CandidateExperience/en/sites/{f['site']}/job/{r.get('Id')}",
                        "ph_scoped": False})
        offset += 25
        if not reqs or offset >= (item.get("TotalJobsCount") or 0):
            break
        time.sleep(delay)
    return out


def read_ultipro(f, delay):
    base = f"https://recruiting2.ultipro.com/{f['tenant']}/JobBoard/{f['board']}"
    out, skip = [], 0
    while skip < 400:
        d = json.loads(fetch(f"{base}/JobBoardView/LoadSearchResults", {"opportunitySearch": {
            "Top": 50, "Skip": skip, "QueryString": f.get("search", ""), "Filters": [],
            "OrderBy": [{"Value": "postedDateDesc", "PropertyName": "PostedDate", "Ascending": False}]}}))
        ops = d.get("opportunities") or []
        for o in ops:
            locs = "; ".join(filter(None, ((l.get("LocalizedName") or "") + " " +
                                          ((l.get("Address") or {}).get("Country") or {}).get("Name", "")
                                          for l in o.get("Locations") or [])))
            out.append({"title": o.get("Title", ""), "location": locs.strip(),
                        "url": f"{base}/OpportunityDetail?opportunityId={o.get('Id')}", "ph_scoped": False})
        skip += 50
        if not ops or skip >= (d.get("totalCount") or 0):
            break
        time.sleep(delay)
    return out


def read_smartrecruiters(f, delay):
    out, offset = [], 0
    while offset < 1000:
        d = json.loads(fetch(f"https://api.smartrecruiters.com/v1/companies/{f['id']}/postings?limit=100&offset={offset}"))
        for p in d.get("content") or []:
            loc = p.get("location") or {}
            out.append({"title": p.get("name", ""),
                        "location": ", ".join(filter(None, [loc.get("city"), loc.get("region"), loc.get("country")])),
                        "url": f"https://jobs.smartrecruiters.com/{f['id']}/{p.get('id')}", "ph_scoped": False})
        offset += 100
        if offset >= (d.get("totalFound") or 0):
            break
        time.sleep(delay)
    return out


def read_greenhouse(f, delay):
    d = json.loads(fetch(f"https://boards-api.greenhouse.io/v1/boards/{f['token']}/jobs"))
    return [{"title": j.get("title", ""), "location": (j.get("location") or {}).get("name", ""),
             "url": j.get("absolute_url", ""), "ph_scoped": False} for j in d.get("jobs") or []]


def read_sf_rss(f, delay):
    out = []
    for n, q in enumerate(f.get("queries") or [""]):
        if n:
            time.sleep(delay)
        xml = fetch(f"{f['base']}/services/rss/job/?locale=en_US&keywords=({urllib.parse.quote(q)})")
        for it in ET.fromstring(xml).iter("item"):
            title = it.findtext("title") or ""
            m = re.match(r"(.*?)\s*\(([^()]*)\)\s*$", title)
            link = re.sub(r"\?.*$", "", it.findtext("link") or "")
            out.append({"title": m.group(1) if m else title, "location": m.group(2) if m else "",
                        "url": link, "ph_scoped": False})
    return out


READERS = {"workday": read_workday, "oracle_hcm": read_oracle, "ultipro": read_ultipro,
           "smartrecruiters": read_smartrecruiters, "greenhouse": read_greenhouse,
           "successfactors_rss": read_sf_rss}


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data.json")
    ap.add_argument("--feeds", default="scripts/careers_feeds.json")
    ap.add_argument("--report", default="careers-report.md")
    ap.add_argument("--dry-run", action="store_true", help="print the report, write nothing")
    ap.add_argument("--delay", type=float, default=1.5, help="seconds between requests (default 1.5)")
    a = ap.parse_args()

    entries = json.load(open(a.data, encoding="utf-8"))  # read only
    known_urls = {(e.get(k) or "").strip().rstrip("/") for e in entries
                  for k in ("posting_url", "website_or_linkedin") if e.get(k)}
    known_titles = {(norm(e.get("company")), norm(e.get("roles_or_projects"))) for e in entries}
    feeds = json.load(open(a.feeds, encoding="utf-8"))["feeds"]

    matches, known, errors, scanned = [], [], [], 0
    for n, f in enumerate(feeds):
        if n:
            time.sleep(a.delay)
        try:
            posts = READERS[f["ats"]](f, a.delay)
        except Exception as e:  # feed down, schema change, etc. -> report, don't fail
            errors.append((f["company"], f["ats"], f"{type(e).__name__}: {e}"))
            print(f"[error ] {f['company']} ({f['ats']}): {type(e).__name__}: {e}", flush=True)
            continue
        scanned += len(posts)
        seen, hits = set(), 0
        for p in posts:
            if p["url"] in seen:
                continue
            seen.add(p["url"])
            if not ROLE.search(p["title"]):
                continue
            if not (PH.search(p["location"]) or p["ph_scoped"]):
                continue
            hits += 1
            row = (f["company"], p["title"].strip(), p["location"].strip() or "location not shown", p["url"])
            if p["url"].rstrip("/") in known_urls or (norm(f["company"]), norm(p["title"])) in known_titles:
                known.append(row)
            else:
                matches.append(row)
        print(f"[ok    ] {f['company']} ({f['ats']}): {len(seen)} postings, {hits} embedded/firmware PH", flush=True)

    summary = (f"{len(feeds)} feeds, {scanned} postings scanned, {len(matches)} new embedded/firmware "
               f"roles in the Philippines, {len(known)} already in data.json, {len(errors)} feed errors")
    lines = [f"Automated careers-feed check: {summary}.", "",
             "## New matches (not yet in data.json; verify before adding)"]
    lines += [f"- **{c}**: {t} ({l}) {u}" for c, t, l, u in matches] or ["- none"]
    lines += ["", "## Feed errors (feed skipped this run)"]
    lines += [f"- {c} ({t}): {e}" for c, t, e in errors] or ["- none"]
    lines += ["", f"_Covered feeds: {', '.join(sorted(f['company'] for f in feeds))}._",
              "_Updated by `.github/workflows/careers-check.yml`. It never edits data.json._"]
    report = "\n".join(lines) + "\n"
    print("\nSummary: " + summary + "\n")
    if a.dry_run:
        print(report)
    else:
        with open(a.report, "w", encoding="utf-8") as fh:
            fh.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())

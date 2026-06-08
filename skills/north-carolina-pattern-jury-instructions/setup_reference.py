#!/usr/bin/env python3
"""
setup_reference.py — Download NC Criminal PJI PDFs and convert them to clean markdown.

This is the script the SKILL runs on the customer's machine. It reads catalog.json
(which ships with the skill), downloads each instruction PDF from the official SOG
source into a local cache, extracts the text, and writes one markdown file per
instruction under reference/instructions/. It also enriches the catalog with the
G.S. statute references it finds in each instruction's text, and writes the
cross-reference maps the skill uses for lookup.

No SOG content is redistributed by the vendor — it is fetched locally, on demand.

Requires:  pip install -r requirements.txt   (pdfminer.six)

Usage:
    python3 setup_reference.py                 # download + convert everything current
    python3 setup_reference.py --only 206.10   # just one instruction (on-demand)
    python3 setup_reference.py --include-superseded
    python3 setup_reference.py --refresh        # re-download even if cached
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request

# macOS Python 3 ships without trusted CA certs; use certifi bundle when available.
try:
    import certifi as _certifi
    os.environ.setdefault("SSL_CERT_FILE", _certifi.where())
except ImportError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "catalog.json")
CACHE_DIR = os.path.join(HERE, "cache", "pdfs")
REF_DIR = os.path.join(HERE, "reference")
INSTR_DIR = os.path.join(REF_DIR, "instructions")

# PDFs use both "G.S. 14-17" (abbreviated) and "N.C. Gen. Stat. 14-17, 14-18" (full,
# comma-separated list).  We match each prefix once, then extract every statute number
# that follows it (handling comma/semicolon-delimited lists for the full form).
_GS_ABBREV_RE = re.compile(r"G\.S\.\s*[0-9]+[A-Za-z0-9\-\.]*(?:\([0-9a-zA-Z]+\))*")
_NCGS_LIST_RE = re.compile(
    r"N\.C\.(?:\s+Gen\.\s+Stat\.|\s*G\.S\.)\s+"
    r"((?:[0-9]+[A-Za-z0-9\-\.]*(?:\([0-9a-zA-Z]+\))*(?:[,;]\s*)?)+)"
)
_STAT_NUM_RE = re.compile(r"[0-9]+[A-Za-z0-9\-\.]*(?:\([0-9a-zA-Z]+\))*")


def _extract_statutes(text):
    found = set(_GS_ABBREV_RE.findall(text))
    for group in _NCGS_LIST_RE.findall(text):
        for num in _STAT_NUM_RE.findall(group):
            num = num.rstrip(".")          # strip trailing sentence period
            if num.endswith("-"):          # e.g. "20-" from mid-line break
                continue
            found.add(f"G.S. {num}")
    return sorted(found)


def require_pdfminer():
    try:
        from pdfminer.high_level import extract_text  # noqa: F401
    except ImportError:
        print(
            "Missing dependency. Run:\n  pip install -r requirements.txt\n"
            "(installs pdfminer.six for PDF text extraction).",
            file=sys.stderr,
        )
        sys.exit(1)


def load_catalog():
    if not os.path.exists(CATALOG):
        print(
            f"catalog.json not found at {CATALOG}.\n"
            "Generate it first:  python3 build_catalog.py",
            file=sys.stderr,
        )
        sys.exit(1)
    with open(CATALOG, encoding="utf-8") as f:
        return json.load(f)


def slug(number):
    return number.replace(".", "_")


def download(url, dest, refresh=False):
    if os.path.exists(dest) and not refresh:
        return "cached"
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "nc-pji-reference/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    with open(dest, "wb") as f:
        f.write(data)
    return "downloaded"


def clean_text(raw):
    """Light cleanup: collapse whitespace, drop obvious page-number-only lines."""
    lines = []
    for ln in raw.splitlines():
        s = ln.rstrip()
        if re.fullmatch(r"\s*N\.C\.P\.I\.[^\n]*", s):  # running header
            continue
        if re.fullmatch(r"\s*Page\s+\d+\s*(of\s+\d+)?\s*", s, re.IGNORECASE):
            continue
        if re.fullmatch(r"\s*\d+\s*", s):  # bare page number
            continue
        lines.append(s)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def yaml_escape(value):
    if value is None:
        return '""'
    s = str(value)
    if re.search(r"[:#\[\]{}\"']", s) or s != s.strip():
        return json.dumps(s, ensure_ascii=False)
    return s


def write_markdown(rec, text):
    statutes = sorted(set(rec.get("statutes", [])) | set(_extract_statutes(text)))
    rec["statutes"] = statutes  # enrich in-place for the cross-ref maps

    fm = [
        "---",
        f'number: "{rec["number"]}"',
        f"title: {yaml_escape(rec['title'])}",
        f"chapter: {yaml_escape(rec['chapter'])}",
        f"statutes: [{', '.join(yaml_escape(s) for s in statutes)}]",
        f"revised: {rec['revised'] if rec.get('revised') else 'null'}",
        f"status: {rec['status']}",
        f"source_url: {yaml_escape(rec['source_url'])}",
        "---",
        "",
    ]
    os.makedirs(INSTR_DIR, exist_ok=True)
    path = os.path.join(INSTR_DIR, f"{slug(rec['number'])}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(fm))
        f.write(text + "\n")
    return statutes


def write_indexes(catalog):
    os.makedirs(REF_DIR, exist_ok=True)

    # index.md — the table Claude scans first
    rows = ["# NC Criminal Pattern Jury Instructions — index", ""]
    rows.append("| Number | Title | Chapter | Statutes | Revised | Status |")
    rows.append("|--------|-------|---------|----------|---------|--------|")
    for r in catalog:
        rows.append(
            f"| {r['number']} | {r['title']} | {r['chapter']} | "
            f"{'; '.join(r.get('statutes', []))} | {r.get('revised') or ''} | {r['status']} |"
        )
    with open(os.path.join(REF_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")

    # by_statute.json — G.S. -> [instruction numbers]
    by_statute = {}
    for r in catalog:
        for s in r.get("statutes", []):
            by_statute.setdefault(s, []).append(r["number"])
    with open(os.path.join(REF_DIR, "by_statute.json"), "w", encoding="utf-8") as f:
        json.dump(by_statute, f, indent=2, ensure_ascii=False)

    # by_offense.json — keyword -> [instruction numbers] (title-derived; refine by hand)
    by_offense = {}
    for r in catalog:
        for kw in re.findall(r"[A-Za-z]{4,}", r["title"].lower()):
            by_offense.setdefault(kw, [])
            if r["number"] not in by_offense[kw]:
                by_offense[kw].append(r["number"])
    with open(os.path.join(REF_DIR, "by_offense.json"), "w", encoding="utf-8") as f:
        json.dump(by_offense, f, indent=2, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", help="Process a single instruction number, e.g. 206.10")
    ap.add_argument("--include-superseded", action="store_true",
                    help="Also process entries marked superseded/reference.")
    ap.add_argument("--refresh", action="store_true", help="Re-download cached PDFs.")
    ap.add_argument("--delay", type=float, default=0.5,
                    help="Seconds between downloads (be polite to SOG).")
    args = ap.parse_args()

    require_pdfminer()
    from pdfminer.high_level import extract_text

    catalog = load_catalog()
    if args.only:
        catalog = [r for r in catalog if r["number"] == args.only]
        if not catalog:
            print(f"{args.only} not in catalog.", file=sys.stderr)
            sys.exit(1)
    elif not args.include_superseded:
        catalog = [r for r in catalog if r["status"] == "current"]

    enriched = []
    ok = fail = 0
    for i, rec in enumerate(catalog, 1):
        pdf_path = os.path.join(CACHE_DIR, f"{slug(rec['number'])}.pdf")
        state = None
        try:
            state = download(rec["source_url"], pdf_path, refresh=args.refresh)
            raw = extract_text(pdf_path) or ""
            text = clean_text(raw)
            if not text:
                raise ValueError("no extractable text (scanned PDF?)")
            write_markdown(rec, text)
            enriched.append(rec)
            ok += 1
            print(f"[{i}/{len(catalog)}] {rec['number']}  {state}  ({len(text)} chars)")
        except Exception as e:  # noqa: BLE001
            fail += 1
            print(f"[{i}/{len(catalog)}] {rec['number']}  FAILED: {e}", file=sys.stderr)
        if state == "downloaded":
            time.sleep(args.delay)

    # Merge enriched statutes back over the full catalog for the index maps.
    by_num = {r["number"]: r for r in enriched}
    full = load_catalog()
    for r in full:
        if r["number"] in by_num:
            r["statutes"] = by_num[r["number"]]["statutes"]
    write_indexes(full)

    print(f"\nDone. {ok} converted, {fail} failed.")
    print(f"Markdown:   {INSTR_DIR}")
    print(f"Index/maps: {REF_DIR}")


if __name__ == "__main__":
    main()

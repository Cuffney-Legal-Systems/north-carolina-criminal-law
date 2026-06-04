"""
download_form.py — Download a single NC AOC criminal form PDF by form number.

Looks up the form in index.json, downloads the PDF to nc_aoc_cr_forms/pdfs/,
and adds the form number to nc_aoc_cr_forms/forms.txt.

Usage:
    python3 skill/download_form.py AOC-CR-100
"""

import json
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Missing dependency. Run: pip install requests")

INDEX_PATH = Path(__file__).parent.parent / "nc_aoc_cr_forms" / "index.json"
PDF_DIR = Path(__file__).parent.parent / "nc_aoc_cr_forms" / "pdfs"
FORMS_TXT = Path(__file__).parent.parent / "nc_aoc_cr_forms" / "forms.txt"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


def is_vietnamese(title: str) -> bool:
    return any(ord(c) > 127 for c in title)


def find_in_index(form_number: str) -> dict | None:
    with open(INDEX_PATH) as f:
        index = json.load(f)
    form_number = form_number.upper().strip()
    matches = [d for d in index if d.get("form_number", "").upper() == form_number]
    if not matches:
        return None
    # Prefer English version; fall back to whatever is available
    english = [d for d in matches if not is_vietnamese(d.get("title", ""))]
    return english[0] if english else matches[0]


def download_pdf(pdf_url: str, dest: Path) -> int:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    time.sleep(0.75)
    resp = session.get(pdf_url, timeout=60, stream=True)
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=65536):
            if chunk:
                fh.write(chunk)
    return dest.stat().st_size


def add_to_forms_txt(form_number: str) -> None:
    existing = set()
    if FORMS_TXT.exists():
        existing = {line.strip() for line in FORMS_TXT.read_text().splitlines() if line.strip()}
    if form_number.upper() not in existing:
        with open(FORMS_TXT, "a") as f:
            f.write(form_number.upper() + "\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    form_number = sys.argv[1].upper().strip()

    entry = find_in_index(form_number)
    if not entry:
        print(f"ERROR: {form_number} not found in index.json.")
        sys.exit(1)

    pdf_url = entry.get("pdf_url", "")
    if not pdf_url:
        print(f"ERROR: No PDF URL found for {form_number}.")
        sys.exit(1)

    filename = entry.get("filename", "")
    if not filename:
        filename = f"{form_number}.pdf"

    dest = PDF_DIR / filename

    if dest.exists():
        print(f"Already downloaded: {dest}")
    else:
        print(f"Downloading {form_number}...")
        size = download_pdf(pdf_url, dest)
        print(f"Saved: {dest} ({size // 1024} KB)")

    add_to_forms_txt(form_number)
    print(f"Added {form_number} to forms.txt")


if __name__ == "__main__":
    main()

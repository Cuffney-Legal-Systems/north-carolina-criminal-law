"""
fill_form.py — fill one or more NC AOC criminal form PDFs given a JSON mapping
of field names to values.

Usage:
    python3 fill_form.py <form_number_or_filename> <values_json> [output_path]

    <values_json>  path to a JSON file OR a JSON string  {"FieldName": "value", ...}

    Checkboxes:    set to true / "Yes" / "yes" to check; anything else = unchecked
    Text fields:   string value
    Dropdowns:     string matching one of the /Opt values

Example:
    python3 fill_form.py AOC-CR-314 '{"CountyName":"Wake","RequestorName":"Jane Doe"}' out.pdf
"""

import json
import logging
import os
import ssl
import sys
import urllib.request
import warnings
from pathlib import Path

# Silence third-party deprecation noise and pypdf's per-page field warnings.
warnings.filterwarnings("ignore")
logging.getLogger("pypdf").setLevel(logging.ERROR)

import pypdf
from pypdf import PdfWriter, PdfReader

# PDFs are fetched on demand from S3 and cached here.
S3_BASE_URL = "https://cuffney-legal-systems.s3.amazonaws.com/NC-criminal-law/nc-aoc-cr-forms"
PDF_DIR = Path(__file__).parent / "pdfs"
INDEX_PATH = Path(__file__).parent / "fields_index.json"


def _load_index() -> list:
    """Load fields_index.json (the single source of truth for form metadata)."""
    with open(INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)


def ensure_pdf_cached(filename: str) -> Path:
    """Return the local path to a PDF, downloading from S3 if not yet cached.

    PDFs are cached in PDF_DIR so subsequent calls are instant. Requires the
    S3 bucket objects to allow public (unauthenticated) GET access.
    """
    local = PDF_DIR / filename
    if local.exists():
        return local

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    url = f"{S3_BASE_URL}/{filename}"
    tmp = local.with_suffix(".tmp")
    try:
        print(f"Downloading {filename} ...", file=sys.stderr)
        try:
            import certifi
            ctx = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            ctx = ssl.create_default_context()
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        with opener.open(url) as resp, open(tmp, "wb") as out:
            out.write(resp.read())
        tmp.rename(local)
        return local
    except Exception as exc:
        if tmp.exists():
            tmp.unlink()
        raise FileNotFoundError(
            f"Could not download '{filename}' from S3.\n"
            f"  URL: {url}\n"
            f"  Error: {exc}\n"
            "Check your internet connection. If the problem persists, contact support."
        ) from exc


def resolve_pdf_path(form_ref: str) -> Path:
    """Resolve a form reference to exactly one PDF, fetching from S3 if needed.

    Accepts either an exact bundled filename or a form number (e.g. AOC-CR-601).
    When a form number maps to more than one edition this refuses to guess and
    raises, listing the choices so the caller can pass the exact filename.
    """
    index = _load_index()

    # 1. Exact filename match against the index (case-insensitive).
    for entry in index:
        if entry.get("filename", "").lower() == form_ref.lower():
            return ensure_pdf_cached(entry["filename"])

    # 2. Exact form-number match against the index (not a loose prefix:
    #    "AOC-CR-60" must not match "AOC-CR-601").
    form_ref_norm = form_ref.upper().strip()
    matches = sorted(
        {entry["filename"] for entry in index
         if entry.get("form_number", "").upper().strip() == form_ref_norm}
    )

    if len(matches) == 1:
        return ensure_pdf_cached(matches[0])

    if len(matches) > 1:
        listing = "\n".join(f"    - {m}" for m in matches)
        raise ValueError(
            f"'{form_ref}' has {len(matches)} editions (usually different "
            f"effective-date versions). Re-run with the exact filename of "
            f"the edition you need:\n{listing}"
        )

    # 3. Fallback: treat form_ref as a literal filename and try to fetch it.
    return ensure_pdf_cached(form_ref)


def normalize_checkbox_value(raw) -> str:
    """Return '/Yes' for truthy checkbox values, '/Off' otherwise."""
    if isinstance(raw, bool):
        return "/Yes" if raw else "/Off"
    if isinstance(raw, str) and raw.lower() in ("yes", "true", "1", "x", "on"):
        return "/Yes"
    return "/Off"


def fill_pdf(pdf_path: Path, values: dict, output_path: Path) -> None:
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)

    fields = reader.get_fields() or {}

    # Some AOC-CR forms are flat informational PDFs with no AcroForm fields
    # (e.g. AOC-CR-412, 617, 918M). There is nothing to fill; copy the blank
    # form to the output path and report rather than crashing.
    if not fields:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            writer.write(f)
        print(
            f"'{pdf_path.name}' has no fillable fields — it is a flat "
            f"informational form. Copied the blank PDF unchanged."
        )
        print(f"Output: {output_path}")
        return

    filled = []
    skipped = []

    field_types = {
        name: field.get("/FT", "/Tx")
        for name, field in fields.items()
    }

    # Build the update dict
    update = {}
    for field_name, raw_value in values.items():
        if field_name not in fields:
            skipped.append(field_name)
            continue

        ft = field_types[field_name]
        if ft == "/Btn":
            update[field_name] = normalize_checkbox_value(raw_value)
        else:
            update[field_name] = str(raw_value)
        filled.append(field_name)

    writer.update_page_form_field_values(writer.pages[0], update, auto_regenerate=False)

    # For multi-page forms, apply to all pages
    if len(writer.pages) > 1:
        for page in writer.pages[1:]:
            writer.update_page_form_field_values(page, update, auto_regenerate=False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"Filled {len(filled)} fields, skipped {len(skipped)} unknown fields")
    if skipped:
        print(f"  Unknown fields: {skipped}")
    print(f"Output: {output_path}")


def get_form_fields(form_ref: str) -> list[dict]:
    """Return the field metadata list for a form from fields_index.json.

    ``form_ref`` may be an exact filename or a form number. For form numbers
    with multiple editions this raises rather than guessing, mirroring
    ``resolve_pdf_path``.
    """
    with open(INDEX_PATH) as f:
        index = json.load(f)

    # Exact filename match first.
    for entry in index:
        if entry.get("filename", "").lower() == form_ref.lower():
            return entry["fields"]

    form_ref_norm = form_ref.upper().strip()
    matches = [e for e in index if e["form_number"].upper() == form_ref_norm]
    if len(matches) == 1:
        return matches[0]["fields"]
    if len(matches) > 1:
        listing = "\n".join(f"    - {e['filename']}" for e in matches)
        raise ValueError(
            f"'{form_ref}' has {len(matches)} editions; pass the exact "
            f"filename:\n{listing}"
        )
    raise KeyError(f"Form '{form_ref}' not found in fields_index.json")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    form_ref = sys.argv[1]
    values_arg = sys.argv[2]
    output_arg = sys.argv[3] if len(sys.argv) > 3 else None

    # Parse values
    if os.path.isfile(values_arg):
        with open(values_arg) as f:
            values = json.load(f)
    else:
        values = json.loads(values_arg)

    pdf_path = resolve_pdf_path(form_ref)

    if output_arg:
        output_path = Path(output_arg)
    else:
        output_path = Path(f"{pdf_path.stem}_filled.pdf")

    fill_pdf(pdf_path, values, output_path)


if __name__ == "__main__":
    main()

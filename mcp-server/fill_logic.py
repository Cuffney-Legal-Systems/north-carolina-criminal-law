"""
fill_logic.py — Lambda-adapted PDF fill logic for NC AOC criminal forms.

Fetches PDFs from S3 using boto3 (no urllib), fills AcroForm fields,
and returns the result as a base64-encoded bytes string.
"""

import base64
import io
import json
import logging
import warnings
from pathlib import Path

import boto3
import pypdf  # noqa: F401 — suppress its import-time warnings via the filter below
from pypdf import PdfReader, PdfWriter

warnings.filterwarnings("ignore")
logging.getLogger("pypdf").setLevel(logging.ERROR)

_S3_BUCKET = "cuffney-legal-systems"
_S3_PREFIX = "north-carolina-criminal-law/nc-aoc-cr-forms"
_INDEX_PATH = Path(__file__).parent / "fields_index.json"

# Module-level client reused across warm invocations.
_s3_client = None


def _s3():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3")
    return _s3_client


def _load_index() -> list:
    with open(_INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)


def _fetch_pdf_bytes(filename: str) -> bytes:
    key = f"{_S3_PREFIX}/{filename}"
    resp = _s3().get_object(Bucket=_S3_BUCKET, Key=key)
    return resp["Body"].read()


def _resolve_filename(form_ref: str) -> str:
    """Return the canonical PDF filename for a form number or exact filename."""
    index = _load_index()

    # 1. Exact filename match (case-insensitive).
    for entry in index:
        if entry.get("filename", "").lower() == form_ref.lower():
            return entry["filename"]

    # 2. Exact form-number match — "AOC-CR-60" must not match "AOC-CR-601".
    form_ref_norm = form_ref.upper().strip()
    matches = sorted(
        {entry["filename"] for entry in index
         if entry.get("form_number", "").upper().strip() == form_ref_norm}
    )

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        listing = "\n".join(f"  - {m}" for m in matches)
        raise ValueError(
            f"'{form_ref}' has {len(matches)} editions. Re-run with the exact filename:\n{listing}"
        )

    # 3. Treat as a literal filename and let S3 surface any 404.
    return form_ref


def _normalize_checkbox(raw) -> str:
    if isinstance(raw, bool):
        return "/Yes" if raw else "/Off"
    if isinstance(raw, str) and raw.lower() in ("yes", "true", "1", "x", "on"):
        return "/Yes"
    return "/Off"


def fill_nc_aoc_form_logic(form_ref: str, values: dict) -> tuple:
    """
    Download, fill, and return the PDF.

    Returns (base64_string, filename).  The base64 string encodes the
    filled PDF bytes; filename is the canonical S3 object name.
    """
    filename = _resolve_filename(form_ref)
    pdf_bytes = _fetch_pdf_bytes(filename)

    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    writer.append(reader)

    fields = reader.get_fields() or {}

    if not fields:
        # Flat informational form (e.g. AOC-CR-412, 617, 918M) — no fields to fill.
        buf = io.BytesIO()
        writer.write(buf)
        return base64.b64encode(buf.getvalue()).decode("ascii"), filename

    field_types = {name: field.get("/FT", "/Tx") for name, field in fields.items()}

    update = {}
    for field_name, raw_value in values.items():
        if field_name not in fields:
            continue
        if field_types[field_name] == "/Btn":
            update[field_name] = _normalize_checkbox(raw_value)
        else:
            update[field_name] = str(raw_value)

    writer.update_page_form_field_values(writer.pages[0], update, auto_regenerate=False)
    for page in writer.pages[1:]:
        writer.update_page_form_field_values(page, update, auto_regenerate=False)

    buf = io.BytesIO()
    writer.write(buf)
    return base64.b64encode(buf.getvalue()).decode("ascii"), filename

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
import os
import sys
from pathlib import Path

import pypdf
from pypdf import PdfWriter, PdfReader
from pypdf.generic import NameObject, BooleanObject

PDF_DIR = Path(__file__).parent / "pdfs"
INDEX_PATH = Path(__file__).parent / "fields_index.json"


def resolve_pdf_path(form_ref: str) -> Path:
    """Accept form number (AOC-CR-314) or bare filename."""
    # Direct filename match
    direct = PDF_DIR / form_ref
    if direct.exists():
        return direct

    # Search by form number prefix
    form_ref_norm = form_ref.upper().strip()
    for f in PDF_DIR.glob("*.pdf"):
        if f.name.upper().startswith(form_ref_norm):
            return f

    raise FileNotFoundError(
        f"Could not find PDF for '{form_ref}' in {PDF_DIR}"
    )


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
    """Return the field metadata list for a form from fields_index.json."""
    with open(INDEX_PATH) as f:
        index = json.load(f)
    form_ref_norm = form_ref.upper().strip()
    for entry in index:
        if entry["form_number"].upper() == form_ref_norm:
            return entry["fields"]
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

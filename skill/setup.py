"""
setup.py — Configure SKILL.md with this repo's absolute path, install dependencies,
and download any forms listed in nc_aoc_cr_forms/forms.txt.
Run once after cloning:  python3 skill/setup.py
Re-run any time you add forms to forms.txt.
"""

import subprocess
import sys
from pathlib import Path

SKILL_MD = Path(__file__).parent / "SKILL.md"
REPO_ROOT = Path(__file__).parent.parent.resolve()
FORMS_TXT = REPO_ROOT / "nc_aoc_cr_forms" / "forms.txt"
DOWNLOAD_SCRIPT = Path(__file__).parent / "download_form.py"


def configure_skill_md():
    text = SKILL_MD.read_text()
    if "{{REPO_ROOT}}" in text:
        updated = text.replace("{{REPO_ROOT}}", str(REPO_ROOT))
        SKILL_MD.write_text(updated)
        print(f"SKILL.md configured for: {REPO_ROOT}")
    else:
        print("SKILL.md already configured (no {{REPO_ROOT}} placeholders found).")


def install_dependencies():
    print("Installing Python dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf", "requests"])


def download_forms():
    if not FORMS_TXT.exists():
        print("No forms.txt found — skipping form downloads.")
        return
    form_numbers = [
        line.strip()
        for line in FORMS_TXT.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not form_numbers:
        print("forms.txt is empty — no forms to download.")
        return
    print(f"Downloading {len(form_numbers)} form(s) listed in forms.txt...")
    for form_number in form_numbers:
        subprocess.check_call([sys.executable, str(DOWNLOAD_SCRIPT), form_number])


if __name__ == "__main__":
    configure_skill_md()
    install_dependencies()
    download_forms()
    print("Setup complete.")

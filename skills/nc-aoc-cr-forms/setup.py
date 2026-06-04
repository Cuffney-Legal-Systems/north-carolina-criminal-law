"""
setup.py — Install the nc-aoc-cr-forms skill into Claude's skills directory.

Run once after cloning (or re-run after pulling updates):

    python3 skills/nc-aoc-cr-forms/setup.py

What this does:
  1. Installs Python dependencies (pypdf, requests)
  2. Copies all skill files (scripts + data) to ~/.claude/skills/nc-aoc-cr-forms/
  3. Downloads any forms listed in forms.txt
  4. Prints the final step to register the skill with Claude Code

Note: If you installed this as a Claude plugin (via the plugin manager or Cowork),
setup.py is NOT required — the plugin manager handles installation automatically.
Only use this script for manual / standalone installs.
"""

import shutil
import subprocess
import sys
from pathlib import Path

# Source: the directory this script lives in (skills/nc-aoc-cr-forms/)
SRC_DIR = Path(__file__).parent.resolve()

# Destination: ~/.claude/skills/nc-aoc-cr-forms/
INSTALL_DIR = Path.home() / ".claude" / "skills" / "nc-aoc-cr-forms"

# Files to copy (data + scripts + skill definition)
INSTALL_FILES = [
    "SKILL.md",
    "fill_form.py",
    "download_form.py",
    "fields_index.json",
    "index.json",
    "forms.txt",
]


def install_dependencies() -> None:
    print("Installing Python dependencies (pypdf, requests)...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", "pypdf", "requests"]
    )
    print("  Done.")


def install_skill_files() -> None:
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    (INSTALL_DIR / "pdfs").mkdir(exist_ok=True)

    for filename in INSTALL_FILES:
        src = SRC_DIR / filename
        dst = INSTALL_DIR / filename
        if not src.exists():
            print(f"  WARNING: source file not found, skipping: {src}")
            continue
        shutil.copy2(src, dst)
        print(f"  Copied: {filename}")

    print(f"\nSkill files installed to: {INSTALL_DIR}")


def download_forms() -> None:
    forms_txt = INSTALL_DIR / "forms.txt"
    if not forms_txt.exists():
        print("No forms.txt found — skipping form downloads.")
        return

    form_numbers = [
        line.strip()
        for line in forms_txt.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not form_numbers:
        print("forms.txt has no entries — skipping form downloads.")
        return

    download_script = INSTALL_DIR / "download_form.py"
    print(f"\nDownloading {len(form_numbers)} form(s) listed in forms.txt...")
    for form_number in form_numbers:
        pdf_check = list((INSTALL_DIR / "pdfs").glob(f"{form_number}*.pdf"))
        if pdf_check:
            print(f"  {form_number}: already downloaded, skipping.")
            continue
        print(f"  Downloading {form_number}...")
        subprocess.check_call([sys.executable, str(download_script), form_number])


def print_next_steps() -> None:
    skill_md_src = INSTALL_DIR / "SKILL.md"
    skills_dir = Path.home() / ".claude" / "skills"
    skill_link = skills_dir / "nc-aoc-cr-forms.md"

    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nFinal step — register the skill with Claude Code:")
    print(f"\n  # Symlink (recommended — stays current on git pull + re-run setup.py):")
    print(f"  ln -sf '{skill_md_src}' '{skill_link}'")
    print(f"\n  # Or copy:")
    print(f"  cp '{skill_md_src}' '{skill_link}'")
    print(f"\nThen restart Claude Code and try:")
    print(f"  \"I need to fill out a warrant for arrest\"")


def main() -> None:
    print(f"Installing nc-aoc-cr-forms skill...")
    print(f"  Source:      {SRC_DIR}")
    print(f"  Install dir: {INSTALL_DIR}\n")

    install_dependencies()
    install_skill_files()
    download_forms()
    print_next_steps()


if __name__ == "__main__":
    main()

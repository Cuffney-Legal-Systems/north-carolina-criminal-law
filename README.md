# nc-criminal-law — Claude Plugin

A Claude plugin (**nc-criminal-law**) bundling the **nc-aoc-cr-forms** skill for identifying, understanding, and filling out North Carolina Administrative Office of Courts (AOC) criminal forms — the AOC-CR series, covering the full criminal process from arrest through post-conviction.

**320 forms. Fully indexed. Fill PDFs conversationally.**

---

## Repository structure

```
nc_aoc_cr_forms/                 — repo root = the plugin (nc-criminal-law)
├── .claude-plugin/
│   ├── marketplace.json        — Marketplace catalog (lists the plugin)
│   └── plugin.json             — Plugin manifest (name: nc-criminal-law)
├── skills/
│   └── nc-aoc-cr-forms/         — the skill (name: nc-aoc-cr-forms)
│       ├── SKILL.md            — Claude skill definition (dynamic path detection)
│       ├── fill_form.py        — Fill a form PDF with field values
│       ├── download_form.py    — Download a form PDF on demand from NC Courts
│       ├── setup.py            — Manual install helper (copies files + installs deps)
│       ├── fields_index.json   — AcroForm field definitions for all 320 forms (~9 MB)
│       ├── index.json          — Form catalog: number, title, statute, pdf_url
│       ├── forms.txt           — Forms to pre-download (edit as needed)
│       └── pdfs/               — Downloaded PDFs (gitignored, populated on demand)
└── README.md
```

---

## Installation

### Option A — Claude plugin (Cowork / Claude Code plugin manager)

Install directly from GitHub in Cowork or Claude Code:

```
https://github.com/Cuffney-Legal-Systems/nc_aoc_cr_forms
```

The plugin manager installs the skill automatically. No setup script needed.

### Option B — Manual install (Claude Code CLI)

**Requirements:** Python 3.9+

```bash
# 1. Clone
git clone https://github.com/Cuffney-Legal-Systems/nc_aoc_cr_forms.git
cd nc_aoc_cr_forms

# 2. Run setup — installs deps, copies files to ~/.claude/skills/nc-aoc-cr-forms/
python3 skills/nc-aoc-cr-forms/setup.py

# 3. Register with Claude Code (choose one):
#    Symlink — recommended, stays current after git pull + re-run setup.py
ln -sf ~/.claude/skills/nc-aoc-cr-forms/SKILL.md ~/.claude/skills/nc-aoc-cr-forms.md
#    Or copy:
cp ~/.claude/skills/nc-aoc-cr-forms/SKILL.md ~/.claude/skills/nc-aoc-cr-forms.md
```

### Keeping the skill current

```bash
git pull
python3 skills/nc-aoc-cr-forms/setup.py   # re-copies updated files
```

---

## Using the skill

Once installed, Claude activates automatically when you describe a task involving NC criminal forms:

- "I need to fill out a warrant for arrest"
- "Which AOC-CR form do I use for an expunction?"
- "Help me complete AOC-CR-314 for Wake County"
- "I need a bond forfeiture form"
- "What form covers conditions of probation?"

Claude identifies the right form, asks for the required information, and produces a filled PDF.

---

## Pre-downloading forms

By default, PDFs are downloaded on demand (the skill prompts you the first time you request a form). To pre-download specific forms, add their numbers to `skills/nc-aoc-cr-forms/forms.txt` (one per line) and re-run `setup.py`.

---

## Command-line usage

```bash
# Fill a form — pass values as JSON string or file
python3 skills/nc-aoc-cr-forms/fill_form.py AOC-CR-314 \
  '{"CountyName": "Wake", "DefendantName": "Jane Doe"}' \
  output_filled.pdf

# Download a single form PDF
python3 skills/nc-aoc-cr-forms/download_form.py AOC-CR-100
```

Checkbox fields accept `true`, `"Yes"`, `"yes"`, `"x"`, `"1"`, or `"on"`.

---

## Form series reference

| Series | Purpose |
|--------|---------|
| 100–199 | Arrest: warrants, citations, search warrants, indictments |
| 200–299 | Pretrial: bail/bond, conditions of release, competency |
| 300–399 | Trial & judgment: pleas, verdicts, sentencing |
| 400–499 | Probation & supervision |
| 500–599 | Appeals |
| 600–699 | Post-conviction: expunctions, motions |
| 700+ | Specialized: mental health, mediation |

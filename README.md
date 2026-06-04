# NC AOC Criminal Forms — Claude Code Skill

A [Claude Code](https://claude.ai/code) skill for identifying, understanding, and filling out North Carolina Administrative Office of Courts (AOC) criminal forms (AOC-CR series). Includes a library of 321 forms covering the full criminal process from arrest through post-conviction.

---

## What's included

```
share/
├── skill/
│   ├── SKILL.md        — Claude Code skill definition
│   ├── fill_form.py    — CLI tool to fill a form PDF with field values
│   └── setup.py        — one-time path configuration and dependency install script
└── nc_aoc_cr_forms/
    ├── index.json          — metadata for every form (number, title, statute, etc.)
    ├── index.csv           — same metadata as a spreadsheet
    ├── fields_index.json   — AcroForm field definitions for each PDF
    └── pdfs/               — 321 downloaded PDF forms
```

---

## Installation

**Requirements:** [Claude Code](https://claude.ai/code) and Python 3.9+.

### 1. Clone the repo

```bash
git clone <repo-url>
cd <repo-name>
```

### 2. Configure paths and install dependencies

Run the setup script once. It writes your local clone path into `skill/SKILL.md` and installs the required `pypdf` library:

```bash
python3 skill/setup.py
```

### 4. Install the skill in Claude Code

Copy (or symlink) `skill/SKILL.md` into your Claude Code skills directory:

```bash
# Copy
cp skill/SKILL.md ~/.claude/skills/nc_aoc_cr_forms.md

# Or symlink (stays in sync if you pull updates)
ln -s "$(pwd)/skill/SKILL.md" ~/.claude/skills/nc_aoc_cr_forms.md
```

> If your Claude Code skills directory is elsewhere, check **Settings → Skills** in the Claude Code app.

---

## Using the skill

Once installed, Claude Code will automatically activate the skill when you describe a task involving NC criminal forms. Example prompts:

- "I need to fill out a warrant for arrest"
- "Which AOC-CR form do I use for an expunction?"
- "Help me complete AOC-CR-314 for Wake County"
- "I need to file a motion to suppress, what form is that?"

Claude will walk you through identifying the right form, gathering the required information, and producing a filled PDF.

---

## Filling a form directly from the command line

```bash
# Pass values as a JSON string
python skill/fill_form.py AOC-CR-314 '{"CountyName": "Wake", "RequestorName": "Jane Doe"}' output.pdf

# Or use a JSON file
python skill/fill_form.py AOC-CR-314 values.json output.pdf
```

- Checkbox fields accept `true`, `"Yes"`, `"yes"`, `"x"`, `"1"`, or `"on"` to check.
- If no output path is given, the filled PDF is saved as `<name>_filled.pdf` in the current directory.
- To see what fields a form has, search `nc_aoc_cr_forms/fields_index.json` for the form number.

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
| 700+   | Specialized: mental health, mediation |

---

## Keeping the library current

This repo is periodically updated when NC Courts publishes new or revised forms. To get the latest, pull the repo and re-run setup:

```bash
git pull
python3 skill/setup.py
```

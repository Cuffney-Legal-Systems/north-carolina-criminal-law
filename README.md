# nc-criminal-law — Claude Plugin

A Claude plugin (**nc-criminal-law**) bundling two skills for North Carolina criminal practice:

- **nc-aoc-cr-forms** — identify, understand, and fill North Carolina AOC criminal court forms (AOC-CR series, 320 forms, full process from arrest through post-conviction)
- **north-carolina-pattern-jury-instructions** — look up, explain, and check work against the NC Pattern Jury Instructions for Criminal Cases (N.C.P.I.—Crim., 1,100+ instructions pre-built and ready to use)

---

## Repository structure

```
nc-criminal-law/                 — repo root = the plugin
├── .claude-plugin/
│   ├── marketplace.json        — Marketplace catalog (lists the plugin)
│   └── plugin.json             — Plugin manifest (name: nc-criminal-law, v0.6.0)
├── skills/
│   ├── nc-aoc-cr-forms/        — AOC-CR form filler
│   │   ├── SKILL.md            — Claude skill definition
│   │   ├── fill_form.py        — Fill a form PDF with field values
│   │   ├── fields_index.json   — AcroForm field definitions for all 320 forms (~9 MB)
│   │   ├── reference.md        — Form disambiguation map
│   │   └── pdfs/               — Downloaded PDFs (gitignored, populated on demand)
│   └── north-carolina-pattern-jury-instructions/  — NC Pattern Jury Instructions
│       ├── SKILL.md            — Claude skill definition
│       ├── catalog.json        — All instructions: number, title, statutes, status
│       ├── setup_reference.py  — Download + convert PDFs on demand (rarely needed)
│       ├── requirements.txt    — pdfminer.six (only needed if running setup_reference.py)
│       └── reference/          — Pre-built instruction text (ships ready-to-use)
│           ├── index.md        — Full instruction table
│           ├── by_statute.json — G.S. statute → instruction numbers
│           ├── by_offense.json — keyword → instruction numbers
│           └── instructions/   — 1,100+ markdown files, one per instruction
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

## Using the skills

### nc-aoc-cr-forms

Claude activates automatically when you describe a task involving NC criminal forms:

- "I need to fill out a warrant for arrest"
- "Which AOC-CR form do I use for an expunction?"
- "Help me complete AOC-CR-314 for Wake County"
- "I need a bond forfeiture form"
- "What form covers conditions of probation?"

Claude identifies the right form, asks for the required information, and produces a filled PDF.

### north-carolina-pattern-jury-instructions

Claude activates automatically when you ask about NC criminal jury instructions:

- "What are the elements of second-degree murder under N.C.P.I.?"
- "What's the pattern instruction for felony breaking and entering?"
- "Which instruction covers G.S. 14-87?"
- "Review this jury charge against the pattern for robbery with a dangerous weapon"
- "Is instruction 206.10 still current?"

Claude looks up the instruction, reads the pre-built text, and answers — no download needed for the 1,100+ instructions that ship with the plugin.

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

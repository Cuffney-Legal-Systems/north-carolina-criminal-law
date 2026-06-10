# north-carolina-criminal-law — Claude Plugin

A Claude plugin (**north-carolina-criminal-law**) bundling two skills for North Carolina criminal practice:

- **nc-aoc-cr-forms** — identify, understand, and fill North Carolina AOC criminal court forms (AOC-CR series, 320 forms, full process from arrest through post-conviction)
- **north-carolina-pattern-jury-instructions** — look up, explain, and check work against the NC Pattern Jury Instructions for Criminal Cases (N.C.P.I.—Crim., 1,100+ instructions pre-built and ready to use)

---

## Repository structure

```
north-carolina-criminal-law/                 — repo root = the plugin
├── .claude-plugin/
│   ├── marketplace.json        — Marketplace catalog (lists the plugin)
│   └── plugin.json             — Plugin manifest (name: north-carolina-criminal-law, v26.06.10.01)
├── agents/
│   ├── case-file-harvester.md  — Scans case folder, returns structured JSON of case facts
│   ├── offense-elements-analyzer.md — Element-by-element charge analysis (spawned in parallel)
│   └── nc-form-filler.md       — Fills a single AOC-CR form via MCP (spawned in parallel)
├── skills/
│   ├── nc-aoc-cr-forms/        — AOC-CR form filler
│   │   ├── SKILL.md            — Claude skill definition
│   │   ├── fill_form.py        — Local fill script (dev/testing)
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

### Option A — Claude plugin (Claude Code plugin manager)

Install directly from GitHub in Claude Code:

```
https://github.com/Cuffney-Legal-Systems/north-carolina-criminal-law
```

The plugin manager installs both skills automatically. No setup script needed.

### Option B — Manual install (Claude Code CLI)

**Requirements:** Python 3.9+

```bash
# 1. Clone
git clone https://github.com/Cuffney-Legal-Systems/north-carolina-criminal-law.git
cd north-carolina-criminal-law

# 2. Register both skills with Claude Code
ln -sf "$(pwd)/skills/nc-aoc-cr-forms/SKILL.md" ~/.claude/skills/nc-aoc-cr-forms.md
ln -sf "$(pwd)/skills/north-carolina-pattern-jury-instructions/SKILL.md" \
    ~/.claude/skills/north-carolina-pattern-jury-instructions.md
```

No local PDF or Python dependencies needed for form filling — the fill operation runs in the hosted Lambda backend (see [MCP server](#mcp-server) below).

### Keeping the plugin current

```bash
git pull
# No further steps needed — the symlinks always point to the latest SKILL.md
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

## MCP server

Form filling is handled by an AWS Lambda function exposed as an MCP tool (`fill_nc_aoc_form`). This moves the S3 download and PDF manipulation out of the client sandbox, where outbound network requests are blocked.

The hosted Lambda URL is configured in `.claude-plugin/plugin.json` and is used automatically when the plugin is installed — no setup required.

**Infrastructure:** Python 3.13, 512 MB, 60 s timeout, Function URL with `RESPONSE_STREAM`, CORS locked to `https://claude.ai`, `s3:GetObject` on the forms prefix only.

---

## Command-line usage

```bash
# Fill a form — pass values as JSON string or file
python3 skills/nc-aoc-cr-forms/fill_form.py AOC-CR-314 \
  '{"CountyName": "Wake", "DefendantName": "Jane Doe"}' \
  output_filled.pdf
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

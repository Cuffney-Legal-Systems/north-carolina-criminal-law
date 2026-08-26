# north-carolina-criminal-law — Claude Plugin

A Claude plugin (**north-carolina-criminal-law**) bundling four skills for North Carolina criminal practice:

- **nc-aoc-cr-forms** — identify, understand, and fill North Carolina AOC criminal court forms (AOC-CR series, 320 forms, full process from arrest through post-conviction)
- **north-carolina-pattern-jury-instructions** — look up, explain, and check work against the NC Pattern Jury Instructions for Criminal Cases (N.C.P.I.—Crim., 1,100+ instructions pre-built and ready to use)
- **north-carolina-general-statutes** — read, look up, and explain the full text of every section in G.S. Chapter 14 (Criminal Law), ~978 sections pre-built as markdown files with cross-references to pattern jury instructions
- **prosecutors-analysis** — generate a prosecutorial summary (probable-cause screening) from a North Carolina police report or fact pattern: per-charge element tables with elements quoted from the pattern instructions, weaknesses, defenses, identification analysis, and a bottom-line recommendation, delivered as a `.docx` draft for prosecutor review

---

## Repository structure

```
north-carolina-criminal-law/                 — repo root = the plugin
├── .claude-plugin/
│   └── plugin.json             — Plugin manifest (name: north-carolina-criminal-law, v26.08.26.02)
├── agents/
│   ├── case-file-harvester.md  — Scans case folder, returns structured JSON of case facts
│   ├── offense-elements-analyzer.md — Element-by-element charge analysis (spawned in parallel)
│   └── nc-form-filler.md       — Fills a single AOC-CR form via MCP (spawned in parallel)
├── skills/
│   ├── nc-aoc-cr-forms/        — AOC-CR form filler
│   │   ├── SKILL.md            — Claude skill definition
│   │   ├── fields_index.json   — AcroForm field definitions for all 320 forms (~9 MB)
│   │   └── reference.md        — Form disambiguation map
│   ├── north-carolina-pattern-jury-instructions/  — NC Pattern Jury Instructions
│   │   ├── SKILL.md            — Claude skill definition
│   │   ├── catalog.json        — All instructions: number, title, statutes, status
│   │   ├── setup_reference.py  — Download + convert PDFs on demand (rarely needed)
│   │   ├── requirements.txt    — pdfminer.six (only needed if running setup_reference.py)
│   │   └── reference/          — Pre-built instruction text (ships ready-to-use)
│   │       ├── index.md        — Full instruction table
│   │       ├── by_statute.json — G.S. statute → instruction numbers
│   │       ├── by_offense.json — keyword → instruction numbers
│   │       └── instructions/   — 1,100+ markdown files, one per instruction
│   ├── north-carolina-general-statutes/  — G.S. Chapter 14 full text
│   │   ├── SKILL.md            — Claude skill definition
│   │   ├── catalog.json        — All ~978 sections: cite, title, article, status
│   │   ├── by_article.json     — Article → section numbers
│   │   ├── by_keyword.json     — Keyword → section numbers (1,700+ keywords)
│   │   ├── index.md            — Full section table
│   │   └── statutes/           — ~978 markdown files, one per section (GS-14-{N}.md)
│   └── prosecutors-analysis/   — Prosecutorial summary (probable-cause screening)
│       ├── SKILL.md            — Claude skill definition
│       ├── reference/
│       │   ├── summary-template.md   — Six-section template + word budgets
│       │   ├── example-output.md     — Worked two-charge summary at target length
│       │   └── issue-checklists.md   — Cross-cutting + charge-specific checklists
│       └── scripts/
│           └── summary_to_docx.py    — Markdown draft → formatted .docx renderer
├── CHANGELOG.md
├── .gitignore
└── README.md
```

Blank form PDFs are **not** stored in the repo or downloaded to the client — the
hosted MCP server fetches them from S3 on each fill. Developer tooling (the
Lambda source, the maintenance scripts, and a local fill script used only for
testing) lives in a gitignored `dev/` directory and is not part of the
distributed plugin.

---

## Installation

### Option A — Claude plugin (Claude Code plugin manager)

Install directly from GitHub in Claude Code:

```
https://github.com/Cuffney-Legal-Systems/north-carolina-criminal-law
```

The plugin manager installs all four skills automatically. No setup script needed.

**Option A is the supported install.** It is the only one that registers the MCP
server, which `nc-aoc-cr-forms` requires — see the caveat under Option B.

### Option B — Manual install (development / offline use)

```bash
# 1. Clone
git clone https://github.com/Cuffney-Legal-Systems/north-carolina-criminal-law.git
cd north-carolina-criminal-law

# 2. Link each skill DIRECTORY into ~/.claude/skills/
mkdir -p ~/.claude/skills
for s in nc-aoc-cr-forms north-carolina-pattern-jury-instructions \
         north-carolina-general-statutes prosecutors-analysis; do
  ln -sfn "$(pwd)/skills/$s" ~/.claude/skills/"$s"
done
```

Link the whole skill directory, not just `SKILL.md`. Every skill here reads
sibling files next to its `SKILL.md` — `catalog.json`, `reference/`,
`statutes/`, `scripts/` — so a lone `SKILL.md` symlink installs a skill that
cannot find its own data.

> **A manual install cannot fill forms.** The `fill_nc_aoc_form` MCP server is
> declared in `.claude-plugin/plugin.json` and is registered only by the plugin
> manager. Installed this way, `nc-aoc-cr-forms` will correctly refuse to
> improvise a form and will tell you to reconnect the plugin — there is no
> local fill path by design. Use Option A if you need form filling.

The other three skills work fully offline once linked: jury instructions,
statutes, and the prosecutorial summary all read from files that ship with the
repo.

**Requirements:** Python 3.9+. `prosecutors-analysis` also needs `python-docx`
(`pip install python-docx`) to render its `.docx` output.

### Keeping the plugin current

```bash
git pull
# Nothing else to do — the directory symlinks always point at the latest files.
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

### north-carolina-general-statutes

Claude activates automatically when you ask about specific G.S. Chapter 14 statutes:

- "What does G.S. 14-17 say?"
- "What statute covers breaking and entering in NC?"
- "Show me all the homicide statutes in Chapter 14"
- "Explain G.S. 14-54 in plain language"
- "Look up G.S. 14-87.1 and show me the pattern jury instruction"

Claude reads the pre-built statutory text and can cross-reference the NC Pattern Jury Instructions when relevant. All ~978 sections of Chapter 14 ship ready to use — no internet required at runtime.

### prosecutors-analysis

Claude activates automatically when you ask for a charging screen on a North Carolina report:

- "Write a prosecutorial summary for this police report"
- "Is there probable cause on these charges?"
- "Run a case screening on CMPD report 20171223-2304-00"
- "Should this case be prosecuted, and what are the weak points?"
- "Analyze the charges in the attached incident report"

Claude reads the report, loads element language from the pattern jury instructions and statute text from Chapter 14, analyzes each charge element by element, sweeps for weaknesses, defenses, and identification problems, and delivers a formatted `.docx`.

**Requires `python-docx`** for the bundled `.docx` renderer:

```bash
pip install python-docx
```

**This skill drafts; it does not decide.** Under N.C. Rule of Professional Conduct 3.8 and ABA Criminal Justice Standard 3-4.3 the charging decision belongs to the prosecutor. Output is labeled a draft prepared with AI assistance for prosecutor review, states probable-cause sufficiency only, and traces every factual assertion to the source report.

---

## MCP server

Form filling is handled by an AWS Lambda function exposed as an MCP tool (`fill_nc_aoc_form`). This moves the S3 download and PDF manipulation out of the client sandbox, where outbound network requests are blocked.

The hosted Lambda URL is configured in `.claude-plugin/plugin.json` and is used automatically when the plugin is installed — no setup required.

**Infrastructure:** Python 3.13, 512 MB, 60 s timeout, Function URL with `RESPONSE_STREAM`, CORS locked to `https://claude.ai`, `s3:GetObject` on the forms prefix only.

**Field values.** Text fields take strings. Checkbox fields accept `true`, `"Yes"`, `"yes"`, `"x"`, `"1"`, or `"on"`; anything else reads as unchecked.

**There is no command-line or local fill path.** `fill_nc_aoc_form` is the only supported way to fill a form. If the tool is unavailable the skill stops and says so rather than downloading a blank PDF and filling it by hand — a hand-built court form that looks official but was never validated against the AcroForm field map is worse than no form at all.

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

---
name: north-carolina-general-statutes
description: >-
  Look up, read, and explain North Carolina General Statutes Chapter 14
  (Criminal Law). Use when the user asks what a specific G.S. statute says,
  asks for the text or elements of a North Carolina criminal offense, references
  a statute number (e.g. G.S. 14-17, G.S. 14-54, G.S. 14-87.1), asks what
  offense covers a particular act under NC law, or wants to browse criminal
  statutes by article (e.g. "show me all homicide statutes"). Covers all
  ~1,100 sections of Chapter 14 — arrest, trial, and post-conviction.
  North Carolina criminal only.
version: 26.06.10.01
---

# NC General Statutes — Chapter 14

Full text of all North Carolina General Statutes Chapter 14 sections, pre-built
as markdown files. No internet required for lookups.

## Phase 0 — Locate skill directory

Every bash block begins by dynamically locating the skill directory:

```bash
SKILL_DIR=$(python3 -c "
import os, pathlib as P, sys
root = os.environ.get('CLAUDE_PLUGIN_ROOT')
if root:
    cand = P.Path(root) / 'skills' / 'north-carolina-general-statutes'
    if (cand / 'catalog.json').exists():
        print(cand); sys.exit(0)
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('catalog.json'):
        if f.parent.name == 'north-carolina-general-statutes':
            print(f.parent); sys.exit(0)
print(h/'.claude/skills/north-carolina-general-statutes')
" 2>/dev/null)
echo "Skill directory: $SKILL_DIR"
```

Reuse `$SKILL_DIR` in every subsequent bash block.

## Files

- `$SKILL_DIR/catalog.json` — all sections: number, cite, title, article,
  subchapter, status (`current` / `repealed`), source_url. **Read this first.**
- `$SKILL_DIR/statutes/GS-14-{N}.md` — full text of each section with YAML
  frontmatter. Decimal sub-sections use underscores: `GS-14-2_3.md`.
- `$SKILL_DIR/by_article.json` — article name → [section numbers].
- `$SKILL_DIR/by_keyword.json` — keyword → [section numbers].
- `$SKILL_DIR/index.md` — human-browsable table of all sections.

## Workflow

### 1 — Lookup by statute number

User says "G.S. 14-17", "14-17", "section 17", or similar:

```bash
# Normalize number (strip "G.S. 14-" prefix) then read the file
python3 -c "
import sys
num = '17'   # replace with extracted number (e.g. '2.3', '87.1')
fname = 'GS-14-' + num.replace('.', '_') + '.md'
print('$SKILL_DIR/statutes/' + fname)
"
```

Read `$SKILL_DIR/statutes/GS-14-{N}.md` directly. Quote the full text
to the user, including subsections. Always cite the revision source URL.

### 2 — Lookup by keyword or offense name

User says "what statute covers breaking and entering", "show me robbery statutes", etc.:

```bash
python3 -c "
import json
idx = json.load(open('$SKILL_DIR/by_keyword.json'))
kws = ['breaking', 'entering']   # replace with keywords from user's query
results = set()
for kw in kws:
    results.update(idx.get(kw, []))
print(sorted(results))
"
```

If results > 5, show a numbered list of matching section titles from `catalog.json`
and ask the user which they want. If results ≤ 5, load and display each.

### 3 — Browse by article

User says "show me all homicide statutes", "what's in Article 6", etc.:

```bash
python3 -c "
import json
articles = json.load(open('$SKILL_DIR/by_article.json'))
# e.g. articles['Article 6'] → list of section numbers
for article, nums in articles.items():
    print(article, '->', nums[:3], '...')
" | head -20
```

Present the matching article's sections as a table (cite, title, status).
Offer to read any individual section the user wants.

### 4 — Explain a statute

After reading the statute file, explain it in plain language:

- State what conduct is prohibited or required.
- Identify the key elements (what the State must prove for a criminal charge).
- Note the classification (felony class, misdemeanor class, or civil infraction)
  if stated in the text.
- Flag if the section cross-references another G.S. statute that controls an
  important term — offer to look that up too.
- Note `status: repealed` sections clearly: state the section is no longer in
  effect and suggest checking the article for the current version.

### 5 — Cross-reference jury instructions

When displaying a statute, check the jury instructions skill's index for linked
pattern instructions:

```bash
python3 -c "
import json, pathlib as P, os

# Locate jury instructions skill
root = os.environ.get('CLAUDE_PLUGIN_ROOT')
ji_dir = None
if root:
    cand = P.Path(root) / 'skills' / 'north-carolina-pattern-jury-instructions'
    if (cand / 'reference' / 'by_statute.json').exists():
        ji_dir = cand
if not ji_dir:
    h = P.Path.home()
    for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
        if not base.exists(): continue
        for f in base.rglob('by_statute.json'):
            if f.parent.name == 'reference' and 'pattern-jury-instructions' in str(f):
                ji_dir = f.parent.parent; break

if ji_dir:
    by_statute = json.load(open(ji_dir / 'reference' / 'by_statute.json'))
    cite = 'G.S. 14-17'   # replace with actual cite
    instructions = by_statute.get(cite, [])
    print(instructions)
else:
    print('Jury instructions skill not found')
"
```

If linked instructions exist, list them at the end of your response:

> **Pattern Jury Instructions:** N.C.P.I.—Crim. 206.10, 206.11 — use the
> `north-carolina-pattern-jury-instructions` skill to look up the elements.

## Guardrails

- Always cite the statute as **G.S. 14-{N}** and include the source URL from
  `catalog.json` so the user can verify the current text on ncleg.gov.
- Statutory text is scraped from the official published HTML. Amendments enacted
  after the last library rebuild may not be reflected — always recommend the user
  verify current text at ncleg.gov for anything requiring precision.
- Do not state that a charge "will" succeed or fail based on statutory text alone.
  Elements analysis requires the pattern jury instructions and case law.
- `status: repealed` sections are included for historical reference. Never cite
  a repealed section as current law.
- North Carolina criminal only. If asked about civil matters or another state,
  say it is out of scope.

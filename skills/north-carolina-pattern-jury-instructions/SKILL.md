---
name: north-carolina-pattern-jury-instructions
description: >-
  Look up, explain, and check work against the North Carolina Pattern Jury
  Instructions for Criminal Cases (N.C.P.I. — Crim.). Use when the user asks
  about the elements of an NC offense or defense, asks "what's the pattern
  instruction for [crime]", references an instruction number (e.g. 206.10),
  asks which instruction covers a statute (e.g. G.S. 14-17), or wants a draft
  jury charge compared against the pattern. North Carolina criminal only.
---

# NC Pattern Jury Instructions (Criminal)

This skill answers questions from the North Carolina Pattern Jury Instructions for
Criminal Cases, published by the UNC School of Government. Instruction text ships
pre-built under `reference/instructions/` — no internet required for most lookups.
`setup_reference.py` can refresh or add instructions on demand if needed.

## Phase 0 — Locate skill directory

Every bash block begins by dynamically locating the skill directory:

```bash
SKILL_DIR=$(python3 -c "
import os, pathlib as P, sys
root = os.environ.get('CLAUDE_PLUGIN_ROOT')
if root:
    cand = P.Path(root) / 'skills' / 'north-carolina-pattern-jury-instructions'
    if (cand / 'catalog.json').exists():
        print(cand); sys.exit(0)
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('catalog.json'):
        if f.parent.name == 'north-carolina-pattern-jury-instructions':
            print(f.parent); sys.exit(0)
print(h/'.claude/skills/north-carolina-pattern-jury-instructions')
" 2>/dev/null)
echo "Skill directory: $SKILL_DIR"
```

Reuse `$SKILL_DIR` in every subsequent bash block.

## Files

- `$SKILL_DIR/catalog.json` — every instruction: number, title, chapter, statutes,
  revision year, status (`current` / `superseded` / `reference`), source URL.
  **Read this first.**
- `$SKILL_DIR/setup_reference.py` — downloads + converts instruction PDFs to markdown
  on demand (only needed when an instruction is missing from `reference/instructions/`).
- `$SKILL_DIR/reference/instructions/<number>.md` — instruction text + metadata.
  Ships pre-built; 1,100+ current instructions included.
- `$SKILL_DIR/reference/index.md` — full table of all instructions.
- `$SKILL_DIR/reference/by_statute.json` — G.S. statute → instruction numbers map.
- `$SKILL_DIR/reference/by_offense.json` — keyword → instruction numbers map.

## First-run setup (only needed for missing instructions)

Before answering, check whether the instruction you need exists under
`$SKILL_DIR/reference/instructions/`. Instructions ship pre-built, so this is
rarely needed. If a file is missing:

1. Ensure dependencies: `pip install -r "$SKILL_DIR/requirements.txt"` (one time).
2. Fetch what's needed:
   - For one instruction: `python3 "$SKILL_DIR/setup_reference.py" --only <number>`
   - For everything: `python3 "$SKILL_DIR/setup_reference.py"`
3. Then read the resulting `$SKILL_DIR/reference/instructions/<number>.md`.

If the machine has no network access, fall back to the catalog metadata — you can
still identify the right instruction number, statute, and revision year, but not
quote the operative text.

## Workflow

1. **Identify the instruction.** Search `$SKILL_DIR/catalog.json` by offense/defense
   name (or `$SKILL_DIR/reference/by_offense.json`), by statute
   (`$SKILL_DIR/reference/by_statute.json`), or by number. If several plausibly fit
   (e.g. deadly-weapon vs. no-deadly-weapon murder forms), list them and ask or pick
   the closest, stating your assumption.
2. **Load the text** from `$SKILL_DIR/reference/instructions/<number>.md`
   (running setup if missing) and read the instruction file.
3. **Answer**, always citing the instruction number and revision year, e.g.
   *"N.C.P.I.—Crim. 206.10 (rev. 2022)."*

## Use-case playbooks

- **Elements of an offense/defense.** Find the instruction, then state the numbered
  elements as the pattern lists them. Note bracketed options (e.g. `[Intent]
  [Intentionally]`) are alternatives the judge selects among.
- **Map a statute to its instruction.** Use `by_statute.json`; if empty for that G.S.,
  run setup first. Report every instruction tied to that statute.
- **Compare a draft charge against the pattern.** Load the pattern, then diff the user's
  draft element-by-element: flag missing elements, altered burden/standard language,
  added or dropped bracketed options, and any deviation from the mandatory wording.
  Present as "matches / deviates / missing," with the pattern language quoted.
- **Currency check.** Flag when `status` is `superseded` (never cite as operative —
  point to the replacement) or when `revised` is old relative to known statutory changes.

## Guardrails

- These are **pattern** instructions, not binding law. Note that the judge tailors them
  to the evidence, and that case law or statutory amendments after the revision year may
  control. Recommend the user verify against current G.S. and appellate authority.
- Never cite a `superseded` or `reference` entry as the operative instruction.
- Always include the revision year — pattern instructions change across annual editions.
- Do not paraphrase elements as if they were the exact charge; quote the pattern wording
  when precision matters.
- North Carolina criminal instructions only. If asked about civil or another state, say
  it's out of scope.

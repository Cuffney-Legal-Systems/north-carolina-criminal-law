---
name: north-carolina-pattern-jury-instructions
description: >-
  Look up, explain, analyze facts against, and check work against the North
  Carolina Pattern Jury Instructions for Criminal Cases (N.C.P.I. — Crim.).
  Use when the user asks about the elements of an NC offense or defense, asks
  "what's the pattern instruction for [crime]", presents a set of facts and
  asks what charges apply or whether the facts support each element, references
  an instruction number (e.g. 206.10), asks which instruction covers a statute
  (e.g. G.S. 14-17), or wants a draft jury charge compared against the pattern.
  North Carolina criminal only.
version: 26.06.10.01
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

**PDF source:** `setup_reference.py` downloads directly from the official SOG URL
stored in `source_url` for each catalog entry.

If the machine has no network access, fall back to the catalog metadata — you
can still identify the right instruction number, statute, and revision year, but
not quote the operative text.

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
4. **Offer a PDF download** — see the PDF download playbook below. Always do this
   after completing your answer whenever one or more specific instructions were
   referenced.

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
- **Analyze facts against an instruction (most common use).** See full playbook below.

### Facts-to-elements analysis playbook

Use this when the user presents a narrative or summary of facts and wants to
know whether a charge is supported, what charges could apply, or how each
element maps to the facts.

**Step 0 — Harvest case context (conditional).**
If there's evidence of a case folder (a `CLAUDE.md` is present in the working
directory, or case-related files exist in `pwd`), spawn the `case-file-harvester`
agent to extract existing defendant and charge context before starting the analysis:

```
Agent: case-file-harvester
Prompt:
CASE_DIR: [current working directory]
CONTEXT: [defendant name, case number, or any facts the user already stated]
```

Use harvested charge(s) and defendant information to inform candidate charge
identification in Step 1. Skip this step if the working directory has no case
files.

**Step 1 — Identify candidate charges.**
Extract the offense(s) that plausibly fit the facts. Use `by_offense.json`
(keyword search on the fact pattern's key verbs/nouns) and `catalog.json`.
If multiple instructions plausibly apply (e.g. first-degree vs. second-degree,
with-weapon vs. without), identify all of them. Include any obvious lesser
included offenses (e.g. assault if assault with deadly weapon is the main
charge). State your candidates explicitly before proceeding.

**If N > 1 candidate charges — spawn parallel analyzers:**

Spawn one `offense-elements-analyzer` agent per candidate charge, all in parallel:

```
Agent: offense-elements-analyzer  (spawn N in parallel)
Each prompt:
INSTRUCTION_NUMBER: [e.g. 206.10]
INSTRUCTION_FILE: [absolute path: $SKILL_DIR/reference/instructions/<number>.md]
FACTS: [full fact pattern from the user]
USER_ROLE: [prosecution / defense / neutral — infer from context, default neutral]
```

Note: instruction filenames use underscores for dots — `206.10` →
`$SKILL_DIR/reference/instructions/206_10.md`.

Collect all agent results and present them as a unified multi-charge report:
show each charge's element table in sequence, then close with a cross-charge
comparison (which charge is strongest, which is marginal, any lesser-included
overlaps between charges). Then skip directly to offering PDF download links.
Steps 2–4 below apply only to single-charge inline analysis.

**If N = 1 — continue inline:**

**Step 2 — Load each instruction.**
Read `$SKILL_DIR/reference/instructions/<number>.md` for each candidate.

**Step 3 — Map facts to elements, element by element.**
For each numbered element in the instruction:

1. Quote the element verbatim from the pattern (use the exact pattern language).
2. Identify the specific fact(s) from the user's narrative that speak to that element.
3. Assign a status:
   - **Supported** — the stated facts clearly satisfy this element as a matter
     of sufficiency (a reasonable jury could find it).
   - **Contested** — facts exist that bear on the element but are ambiguous,
     incomplete, or subject to an opposing inference.
   - **Not supported** — no facts in the narrative address this element, or the
     facts affirmatively negate it.
   - **Needs information** — the element cannot be assessed without facts the
     user has not provided; state exactly what is missing.
4. For bracketed alternatives in the pattern (e.g. `[intentionally] [knowingly]`),
   note which bracket the facts point toward and why.

**Step 4 — Summarize.**
After the element-by-element table, provide:
- **Overall charge viability:** Supported / Marginal / Not supported, with a
  one-sentence explanation.
- **Weakest element(s):** identify which element(s) are most likely to fail or
  be contested at trial.
- **Lesser included offenses:** note if the facts support a lesser charge even
  if the main charge is marginal.
- **Fact gaps:** list any facts, if obtained, that would resolve the uncertain
  elements (e.g. "Evidence of intent, such as prior statements, would resolve
  element 3").

**Step 5 — Perspective note.**
If the user's role is not stated, note that the analysis is neutral (facts as
given). If the user identifies as defense counsel, frame which elements are
most vulnerable to challenge and why. If prosecution, frame what additional
evidence would shore up contested elements.

### Official PDF links

**When to offer:** After every response that references one or more specific
instructions by number — including elements lookups, facts analyses, statute
maps, and charge comparisons. Also offer proactively if the user's message
explicitly asks for a jury instruction by name or number without requesting
analysis (they likely want the source document).

**How to provide the link:** At the end of your response, after the substantive
answer, look up the `source_url` field from `$SKILL_DIR/catalog.json` for each
referenced instruction and present it as a direct link to the official SOG PDF.

```bash
python3 -c "
import json
catalog = json.load(open('$SKILL_DIR/catalog.json'))
numbers = ['206.10']   # replace with actual referenced numbers
for num in numbers:
    rec = next((r for r in catalog if r['number'] == num), None)
    if rec:
        print(f\"{num} — {rec['title']}\")
        print(f\"  {rec['source_url']}\")
    else:
        print(f\"{num} — not found in catalog\")
"
```

Present the output to the user as:

> **Official SOG PDFs:**
> - [N.C.P.I.—Crim. 206.10 — First-Degree Murder…](<source_url>)

If multiple instructions were referenced, list all of them. These are direct
links to the authoritative UNC School of Government source.

## Guardrails

- These are **pattern** instructions, not binding law. Note that the judge tailors them
  to the evidence, and that case law or statutory amendments after the revision year may
  control. Recommend the user verify against current G.S. and appellate authority.
- Never cite a `superseded` or `reference` entry as the operative instruction.
- Always include the revision year — pattern instructions change across annual editions.
- Do not paraphrase elements as if they were the exact charge; quote the pattern wording
  when precision matters.
- In a facts analysis, never state that a charge "will" succeed or fail — only assess
  whether the stated facts are sufficient to support each element as a matter of
  sufficiency (reasonable juror standard). Ultimate outcome depends on credibility,
  additional evidence, and jury deliberation.
- North Carolina criminal only. If asked about civil or another state, say it's out of scope.

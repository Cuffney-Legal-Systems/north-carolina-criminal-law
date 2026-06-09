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

**PDF source:** `setup_reference.py` tries the public S3 HTTPS URL
(`https://cuffney-legal-systems.s3.amazonaws.com/north-carolina-criminal-law/north-carolina-pattern-jury-instructions/`)
first, then falls back to the official SOG HTTP URL. No AWS credentials or CLI required — S3 is accessed as a public HTTPS endpoint.

If the machine has no network access and S3 is also unreachable, fall back to
the catalog metadata — you can still identify the right instruction number,
statute, and revision year, but not quote the operative text.

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

**Step 1 — Identify candidate charges.**
Extract the offense(s) that plausibly fit the facts. Use `by_offense.json`
(keyword search on the fact pattern's key verbs/nouns) and `catalog.json`.
If multiple instructions plausibly apply (e.g. first-degree vs. second-degree,
with-weapon vs. without), identify all of them. Include any obvious lesser
included offenses (e.g. assault if assault with deadly weapon is the main
charge). State your candidates explicitly before proceeding.

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

### PDF download playbook

**When to offer:** After every response that references one or more specific
instructions by number — including elements lookups, facts analyses, statute
maps, and charge comparisons. Also offer proactively if the user's message
explicitly asks for a jury instruction by name or number without requesting any
analysis (they likely want the document itself).

**How to offer:** At the end of your response, after the substantive answer,
add a short offer. If one instruction was referenced:

> Would you like me to download the PDF for N.C.P.I.—Crim. 206.10 into your
> project folder?

If multiple instructions were referenced, list them all:

> Would you like me to download any of these PDFs into your project folder?
> - N.C.P.I.—Crim. 206.10 — First-Degree Murder
> - N.C.P.I.—Crim. 206.14 — Second-Degree Murder

**How to download (when the user says yes):**

1. Determine the target directory. Use `$PWD` (the user's current working
   directory) as the default. If the conversation makes the project folder
   obvious (e.g. the user mentioned a case folder or a path earlier), use
   that instead. Confirm the destination with the user if uncertain.

2. Build the filename: `NCPJI_<number_with_underscores>.pdf`
   e.g. instruction 206.10 → `NCPJI_206_10.pdf`.

3. Try S3 (public HTTPS) first, then SOG HTTP fallback:

```bash
NUMBER="206.10"
SLUG="${NUMBER//./_}"
DEST="$PWD/NCPJI_${SLUG}.pdf"
S3_URL="https://cuffney-legal-systems.s3.amazonaws.com/north-carolina-criminal-law/north-carolina-pattern-jury-instructions/${SLUG}.pdf"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

# Try S3 (public, no credentials needed)
if curl -fsSL -A "$UA" -o "$DEST" "$S3_URL" 2>/dev/null; then
    echo "Downloaded from S3: $DEST"
else
    # Fall back to SOG HTTP source_url from catalog.json
    SOURCE_URL=$(python3 -c "
import json, sys
catalog = json.load(open('$SKILL_DIR/catalog.json'))
rec = next((r for r in catalog if r['number'] == '$NUMBER'), None)
print(rec['source_url'] if rec else '', end='')
")
    if [ -z "$SOURCE_URL" ]; then
        echo "No source URL found for $NUMBER." >&2
    else
        curl -fsSL -A "$UA" -o "$DEST" "$SOURCE_URL" \
            && echo "Downloaded from SOG: $DEST" \
            || echo "Download failed." >&2
    fi
fi
```

4. After a successful download, confirm the full path to the user:

> Downloaded: `/path/to/project/NCPJI_206_10.pdf`

If the user asked for multiple instructions, loop over each number and run the
block for each, reporting success or failure per file.

**If download fails:** Report which source(s) were tried and failed, and give
the user the `source_url` from the catalog so they can fetch it manually.

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

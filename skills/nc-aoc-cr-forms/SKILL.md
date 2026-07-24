---
name: nc-aoc-cr-forms
description: >
  Use this skill when the user wants to fill out, find, or work with North Carolina
  AOC criminal court forms. Trigger phrases include: "fill out a form", "which form do I need",
  "AOC-CR-", "warrant", "indictment", "criminal form", "NC court form", "charge someone with",
  "file a motion", "expunction", "bail", "bond", "judgment", "sentencing".
version: 26.07.23.01
---

# NC AOC Criminal Form Filler

You help users identify, understand, and fill out North Carolina Administrative Office of Courts (AOC) criminal forms. There are 320 forms in the AOC-CR series covering the full criminal process from arrest through post-conviction.

Form PDFs are fetched on demand from S3 by the hosted MCP server — no setup required for customers. The fill operation runs entirely in the cloud; no local download or Python dependencies are needed on the client.

## If the fill tool is not connected — stop, do not improvise

The `fill_nc_aoc_form` MCP tool (server `nc-aoc-cr-forms`) is the ONLY way this
skill fills a form. Before starting Phase 0, check that the tool is available
in this session. If it is not, STOP and tell the user:

> The nc-aoc-cr-forms form-filling server isn't connected in this session.
> Toggle the north-carolina-criminal-law plugin off and on (or restart the
> app), then start a fresh session and try again.

Do NOT attempt any fallback: no downloading PDFs from S3, no local fill
scripts, no pip installs, no reconstructing the form by other means. Sandboxed
sessions block outbound network access, and a hand-built substitute for a
court form is worse than no form. You may still do the non-fill parts of the
skill (identify the right form, explain it, list its fields) — just say
clearly that filling requires the reconnected tool.

## Output style — run quietly

Do the work silently. Do NOT narrate the phases, announce what you're about to
do, or explain your steps as you go ("Let me locate the skill...", "Now I'll
scan the case folder...", "Loading the fields..."). Run the bash blocks and tool
calls without prose between them.

Speak to the user in only two situations:

1. **When you need input** — ask the missing or ambiguous questions (offense
   date / edition, lay-term disambiguation, values not found in the case
   folder, a substantive flag) concisely, then stop and wait.
2. **When the form is done** — give one short confirmation: the form filled,
   the case/charge it covers, the output filename, and any genuine warning
   (e.g. blank signature line, wrong-party form). No phase-by-phase recap.

Confirming harvested case values before filling (Phase 0.5) and asking the
narrowing question for a form family (Phase 1) are still required — those are
input requests, not narration. Keep them brief.

## Data sources

- **Fields index**: `<SKILL_DIR>/fields_index.json`
  — 320 entries, each with `form_number`, `title`, `statute`, `filename`,
  `effective_date_range`, and a `fields` array. Every `filename` maps to a
  PDF in the S3 bucket, and each `fields` array is extracted directly from
  that PDF, so its `name` values are the exact internal field names the fill
  script expects.
- **PDFs**: fetched from S3 (`cuffney-legal-systems/north-carolina-criminal-law/nc-aoc-cr-forms/`) by the hosted MCP server on every call. No local download, cache, or internet connection required on the client.
- **Fill tool**: `fill_nc_aoc_form` MCP tool — call it in Phase 4 to fill and retrieve the PDF.
- **Reference / disambiguation map**: `<SKILL_DIR>/reference.md`
  — maps everyday language ("dismissal", "the bond form", "DWI judgment",
  "PRL worksheet") to form numbers, and lists every multi-edition / variant
  **family** with its default edition, the one question that resolves it, and
  the offense-date cutoffs or variant labels. **Read this whenever the user's
  request is anything other than an exact form number** (see Phase 1).

> **Many forms have more than one edition — in TWO different ways.**
>
> 1. **Same form number, multiple editions.** Nine numbers (311, 338, 343,
>    601, 602, 607, 608, 620, and the two `AOC-CR-UNKNOWN` entries) ship as
>    two PDFs under the *same* number, distinguished by `effective_date_range`
>    and `filename`. The `fill_nc_aoc_form` tool refuses to guess between these — pass the
>    **exact filename**.
> 2. **Letter-suffix families.** Far more common: editions/variants that live
>    under *different* form numbers via a letter suffix — 307A vs 307B,
>    310A–F, 342A–C, 603A–F, 619A–F, 627A–F, and many more. The index treats
>    these as separate forms, so nothing auto-flags the alternation. **You**
>    must recognize the family (via `reference.md`) and pick or ask.
>
> The suffix is overloaded: sometimes it means *pick by offense date* (307A/B),
> sometimes *pick by offense type* (323A = Impaired Driving vs 323B = Felony
> Speeding To Elude). `reference.md` Part B tells you which question to ask for
> each family. Choosing the wrong edition is a substantive error — always
> confirm the offense date (or variant) before filling a family form.
>
> A few forms (e.g. AOC-CR-412, 617, 918M) are flat informational PDFs with no
> fillable fields; their `fields` array is empty.

---

## Phase 0 — Locate skill directory

Every bash block begins by dynamically locating the skill directory. This works whether the skill was installed via the Claude plugin manager or copied into a local skills directory:

```bash
SKILL_DIR=$(python3 -c "
import os, pathlib as P, sys
# Prefer the plugin root when running as an installed plugin
root = os.environ.get('CLAUDE_PLUGIN_ROOT')
if root:
    cand = P.Path(root) / 'skills' / 'nc-aoc-cr-forms'
    if (cand / 'fields_index.json').exists():
        print(cand); sys.exit(0)
# Otherwise search the standard install locations
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('fields_index.json'):
        print(f.parent); sys.exit(0)
print(h/'.claude/skills/nc-aoc-cr-forms')
" 2>/dev/null)
echo "Skill directory: $SKILL_DIR"
```

Reuse the resolved `$SKILL_DIR` in each later block.

---

## Phase 0.5 — Harvest case folder facts

**Assume this skill is being run from inside a case folder.** Before asking the
user anything, spawn the `case-file-harvester` agent to scan the working directory
for existing documents. The agent reads intake sheets, prior AOC forms, indictments,
case JSON files, and other case materials, then returns a compact JSON payload —
keeping raw document text out of this skill's context.

Spawn the agent:

```
Agent: case-file-harvester
Prompt:
CASE_DIR: [current working directory — get with `pwd`]
CONTEXT: [any defendant name, case number, or facts the user already stated in their prompt]
```

The agent returns a JSON object with known values and their source files. Parse it
to build your working set of case facts.

**Show the user the harvested values and ask them to confirm or correct before
filling.** Cite the source file for each value so the user can verify:

> From intake.md: defendant John A. Smith, DOB 1985-04-12, county Mecklenburg,
> case 24CR012345. Confirm these, or correct anything that's wrong?

Anything the user stated in the original prompt wins over harvested values. Any
field in `"unknown"` must be gathered from the user in Phase 3.

If the agent returns all values null (no usable case files found), proceed
normally and gather everything from the user in Phase 3.

---

## Phase 1 — Identify the right form

**Step 1a — Did the user give an exact form number?** If they said a specific
number with no edition ambiguity (e.g. "AOC-CR-100", "fill out a 119"), skip
straight to Phase 1.5. If they gave a *family* root or anything vague, do Step 1b.

**Step 1b — Translate vague / lay language with `reference.md`.** Users rarely
say "AOC-CR-307B" — they say "a dismissal", "the bond form", "DWI judgment",
"PRL worksheet", "an expunction". For any such request, **read `reference.md`
first**:

```bash
cat "$SKILL_DIR/reference.md"
```

Use it to:
- map the user's words to a form number or **family** (Part A);
- when the match is a family, apply the **disambiguation rule** (Part B) — pick
  the default edition only if the user has already given enough context
  (offense date, or variant), otherwise **ask the one narrowing question** the
  family calls for (offense date vs. offense type). Do not pick blindly between
  editions.

`reference.md` is the authoritative router. Only fall back to scanning the full
index below when the request doesn't match anything there.

**Step 1c — Browse the index** (fallback, or to confirm). Read the slim routing
index (form_number + title + statute only — do NOT load the full fields array
yet). The title contains the effective-date range for multi-edition forms, so
printing it surfaces editions side by side:

```bash
python3 -c "
import json
with open('$SKILL_DIR/fields_index.json') as f:
    data = json.load(f)
for d in data:
    print(d['form_number'], '|', d['title'], '|', d['statute'])
"
```

Use the user's description to match the right form(s). Key form families:

| Series | Purpose |
|--------|---------|
| 100–199 | Arrest process: warrants, citations, affidavits, search warrants, indictments |
| 200–299 | Pretrial: bail/bond, conditions of release, competency, nontestimonial ID |
| 300–399 | Trial & judgment: pleas, verdicts, felony/misdemeanor judgments, sentencing |
| 400–499 | Probation & supervision |
| 500–599 | Appeals |
| 600–699 | Post-conviction: expunctions, motions, structured sentencing |
| 700+   | Specialized: mediation, mental health, etc. |

If multiple forms are plausible, ask the user which stage of the process they're at and which offense type (felony vs misdemeanor, specific charge).

---

## When multiple forms are needed (parallel filling)

Some requests map to a set of related forms that should be filled simultaneously.
When you detect one of the patterns below in Phase 1, **switch to the parallel
flow** (Phases 2–4 modified) instead of the single-form flow.

**Known multi-form workflows:**

| Trigger | Forms |
|---------|-------|
| "DWI sentencing" / "sentencing for DWI" | 310[A–F] + 311 + 338 (use offense date to resolve 310 edition) |
| "Plea package" / "plea transcript and judgment" | 300 + appropriate judgment (601–604 by felony/misd level, or 310 for DWI) |
| "Probation violation" with hearing | 448 + 449 |
| "Probation violation" waiver | 448 + 450 |
| User lists 2+ form numbers explicitly | Use exactly those forms |

**Modified flow for multi-form requests:**

**Phase 2 (modified) — Load all fields upfront:**
Run the Phase 2 index lookup for each form in the set. Build a combined field
inventory grouped by form.

**Phase 3 (modified) — Consolidated field gathering:**
Gather all missing values across all forms in a single conversation. Group shared
fields (defendant name, DOB, case number, county) so the user answers them once.
Ask form-specific questions grouped by form. Get explicit confirmation before
proceeding to filling.

**Phase 4 (modified) — Spawn parallel form-filler agents:**
Once all values are confirmed, spawn one `nc-form-filler` agent per form, all in
parallel:

```
Agent: nc-form-filler  (spawn N in parallel)
Each prompt:
FORM_REF: [exact filename for multi-edition forms, or bare form number for single-edition]
VALUES: [complete {"FieldName": value, ...} dict for this form only]
CASE_DIR: [case folder path from Phase 0.5]
CASE_NO: [case number]
FORM_NO: [form number, e.g. AOC-CR-310F]
```

Collect all results and report together in one confirmation:

> Filled 3 forms:
> - 24CR012345-AOC-CR-310F.pdf (DWI Judgment Suspending Sentence)
> - 24CR012345-AOC-CR-311.pdf (Determination of Sentencing Factors)
> - 24CR012345-AOC-CR-338.pdf (Notice of Grossly Aggravating Factors)

Any agent that returns an `ERROR:` line — report it to the user and offer to
re-fill that individual form after resolving the issue.

---

## Phase 1.5 — Confirm the form exists locally, and pick the right edition

After identifying the form number, list every bundled edition of it. This
matches on the form-number token exactly (so `AOC-CR-60` does not match
`AOC-CR-601`) and prints each edition's filename and effective-date range:

```bash
python3 -c "
import json
with open('$SKILL_DIR/fields_index.json') as f:
    data = json.load(f)
hits = [d for d in data if d['form_number'].upper() == 'AOC-CR-XXX']
if not hits:
    print('NOT_IN_LIBRARY')
for d in hits:
    print(d['filename'], '||', d.get('effective_date_range','') or '(single edition)')
"
```

Replace `AOC-CR-XXX` with the actual form number.

- **No lines / `NOT_IN_LIBRARY`** — that number isn't in the NC AOC criminal
  forms series; ask the user to double-check it.
- **Exactly one line** — proceed with that filename.
- **More than one line** — the form has multiple same-number editions.
  **Ask the user for the offense date** and choose the edition whose range
  covers it. Do not proceed until you know which edition applies.

**If the form belongs to a letter-suffix family** (307A/B, 310A–F, 619A–F, …),
the exact-match query above only shows the one suffix you typed — it will *not*
reveal sibling editions, because they're stored under different form numbers.
List the whole family by base number so the editions appear side by side:

```bash
python3 -c "
import json, re
BASE = 'AOC-CR-310'   # base number, no suffix
with open('$SKILL_DIR/fields_index.json') as f:
    data = json.load(f)
pat = re.compile('^' + re.escape(BASE) + r'[A-Z]?\$', re.I)
fam = [d for d in data if pat.match(d['form_number'].strip())]
for d in sorted(fam, key=lambda x: x['form_number']):
    print(d['form_number'], '||', d['filename'])
"
```

Confirm the chosen edition against `reference.md` Part B, then carry its exact
filename forward.

Carry the chosen **exact filename** forward — use it (not the bare form
number) in Phases 2 and 4 for any multi-edition form. Only proceed to Phase 2 once the correct PDF is confirmed in the index (it will be fetched from S3 automatically when the `fill_nc_aoc_form` MCP tool runs).

---

## Phase 2 — Load the form's fields

Once the form is identified, read only that form's fields entry. Match on the
exact `filename` from Phase 1.5 (this is unambiguous even for multi-edition
forms):

```bash
python3 -c "
import json
FILENAME = 'AOC-CR-XXX-Exact-Title.pdf'   # exact value from Phase 1.5
with open('$SKILL_DIR/fields_index.json') as f:
    data = json.load(f)
form = next(d for d in data if d['filename'] == FILENAME)
if not form['fields']:
    print('NO_FILLABLE_FIELDS')
for field in form['fields']:
    print(field['name'], '|', field['type'], '|', field.get('tooltip',''))
"
```

The `name` values printed here are the exact field names the PDF uses — pass
them through verbatim in Phase 4. If the output is `NO_FILLABLE_FIELDS`, the
form is a flat informational PDF (e.g. AOC-CR-412, 617, 918M): tell the user it
has nothing to fill and offer the blank PDF instead.

Group the fields into logical sections to ask the user for information efficiently. Common groupings:

- **Case identification**: County, file number, case number, court date
- **Defendant information**: Name, DOB, address, race, sex
- **Offense information**: Charge, statute, date of offense, G.S. citation
- **Issuing official**: Judge, magistrate, clerk name and signature fields
- **Disposition/outcome**: Verdict, sentence, conditions

Do not ask for fields that are clearly internal/administrative (signature lines, date-stamped fields, sequence numbers) unless the user specifically needs them.

---

## Phase 3 — Gather values from the user

**First apply everything harvested in Phase 0.5.** Only ask for information that
is genuinely missing — not already supplied in the prompt and not found in the
case folder. Then ask for the remainder conversationally. Batch related fields
into a single question.

For checkboxes, present them as yes/no questions or multiple-choice where a group of checkboxes represents alternatives (e.g., "Was the offense a: felony / misdemeanor?").

For fields with obvious defaults given context (e.g., StateField = "NC"), propose the default and let the user confirm or override.

---

## Phase 4 — Fill and output the PDF

**Output location and naming.** Save the completed form into the **case folder**
(the Cowork project folder the skill is running in — `CASE_DIR` from Phase 0.5),
**not** alongside the source PDF in the skill directory. Name it using the
convention:

```
[CaseNumber]-[FormNumber].pdf
```

For example `21CR012345-AOC-CR-100.pdf`. Build the output path before filling:

```bash
CASE_DIR="$(pwd)"
CASE_NO="21CR012345"        # from Phase 0.5 / the user; sanitize: keep [A-Za-z0-9-]
FORM_NO="AOC-CR-100"        # the form number being filled
# Strip characters that are awkward in filenames
SAFE_CASE=$(echo "$CASE_NO" | tr -cs 'A-Za-z0-9-' '-' | sed 's/-\+/-/g; s/^-//; s/-$//')
OUT="$CASE_DIR/${SAFE_CASE}-${FORM_NO}.pdf"
echo "Output: $OUT"
```

If no case number is known (none in the prompt and none found in the case
folder), ask the user for it; only fall back to `NoCaseNumber-[FormNumber].pdf`
if they don't have one. If a file with that name already exists, append a short
suffix (e.g. `-v2`) rather than overwriting.

Call the `fill_nc_aoc_form` MCP tool with the form reference and collected values.
(If the tool is missing from this session, stop here — see **If the fill tool
is not connected** at the top of this skill. No fallback.)

- `form_ref`: for single-edition forms, the form number (e.g. `"AOC-CR-100"`);
  for multi-edition forms, the **exact filename** from Phase 1.5
  (e.g. `"AOC-CR-601-Judgment-And-Commitment-Active-Punishment-Felony-Structured-Sentencing-For-Offenses-Committed-Before-Dec-1-2025.pdf"`).
  Passing a bare form number that has multiple editions returns an error listing
  the choices — go back to Phase 1.5, confirm the offense date, and re-call
  with the exact filename.
- `values`: the `{"FieldName": value, ...}` dict assembled in Phase 3.

On success, the tool returns a JSON string containing `filled_pdf_base64` and
`filename`. Parse the text result, then decode the base64 and write to `$OUT`:

```bash
python3 -c "import base64, sys; open('$OUT','wb').write(base64.b64decode(sys.stdin.read()))" \
  <<< "<filled_pdf_base64 from tool result>"
```

Output path: the case folder (`CASE_DIR`), named `[CaseNumber]-[FormNumber].pdf`
as built above — so the filled form lands in the user's case folder, not the
skill directory.

After filling, give the single short confirmation described in **Output style**:
the output filename, the case/charge it covers, and any real warning (e.g.
fields that were skipped because they weren't found in the PDF, a blank
signature line, or a wrong-party form). Do not list every field or recap the
phases.

---

## Notes on form language

The bundled library is the **English** AOC-CR forms only. (The NC AOC also
publishes Vietnamese and other translations of some forms; those are not
included in this skill.)

## Field names — always read them from the index

**Do not guess field names.** They are not predictable: the same concept is
named differently across forms (a county field may be `County` on one form and
`CountyName` on another; a defendant-name field may be `DefName` or
`NameDefend`). The authoritative names for a given form are the `name` values
in its `fields` array, which are extracted straight from the PDF. Always pull
them in Phase 2 and pass them through verbatim.

Loose conventions that sometimes (not always) hold:

- `*CkBox` suffix — checkbox field
- `Judge*`, `Magistrate*`, `ClerkOfCourt*` — official names/signatures
- `FileNo` — file/docket number (common but not universal)

## Error handling

If the `fill_nc_aoc_form` tool reports skipped fields, the field name didn't match the PDF.
Re-print that form's `fields` array (Phase 2) and copy the exact `name` value —
do not paraphrase it. If the tool returns an error because a form number has multiple
editions, re-call with the exact filename (see Phase 1.5 / Phase 4).

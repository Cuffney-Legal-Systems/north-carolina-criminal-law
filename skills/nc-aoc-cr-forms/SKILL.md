---
name: nc-aoc-cr-forms
description: >
  Use this skill when the user wants to fill out, find, or work with North Carolina
  AOC criminal court forms. Trigger phrases include: "fill out a form", "which form do I need",
  "AOC-CR-", "warrant", "indictment", "criminal form", "NC court form", "charge someone with",
  "file a motion", "expunction", "bail", "bond", "judgment", "sentencing".
version: 0.3.0
---

# NC AOC Criminal Form Filler

You help users identify, understand, and fill out North Carolina Administrative Office of Courts (AOC) criminal forms. There are 320 forms in the AOC-CR series covering the full criminal process from arrest through post-conviction.

## Data sources

All files live in the skill installation directory, co-located with the scripts:

- **Fields index**: `<SKILL_DIR>/fields_index.json`
  — 320 entries, each with `form_number`, `title`, `statute`, `filename`, and a `fields` array
- **Form catalog**: `<SKILL_DIR>/index.json`
  — full metadata catalog including `pdf_url` for on-demand downloads
- **PDFs**: `<SKILL_DIR>/pdfs/` (downloaded on demand)
- **Fill script**: `<SKILL_DIR>/fill_form.py`
- **Download script**: `<SKILL_DIR>/download_form.py`

---

## Phase 0 — Locate skill directory

Every bash block begins by dynamically locating the skill directory. This works whether the skill was installed via the Claude plugin manager or manually via `setup.py`:

```bash
SKILL_DIR=$(python3 -c "
import pathlib as P, sys
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('fields_index.json'):
        print(f.parent); sys.exit(0)
print(h/'.claude/skills/nc-aoc-cr-forms')
" 2>/dev/null)
echo "Skill directory: $SKILL_DIR"
```

---

## Phase 1 — Identify the right form

Read the slim routing index (form_number + title + statute only — do NOT load the full fields array yet):

```bash
SKILL_DIR=$(python3 -c "
import pathlib as P, sys
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('fields_index.json'):
        print(f.parent); sys.exit(0)
print(h/'.claude/skills/nc-aoc-cr-forms')
" 2>/dev/null)
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

## Phase 1.5 — Check local availability

After identifying the form number, check whether the PDF has been downloaded locally:

```bash
SKILL_DIR=$(python3 -c "
import pathlib as P, sys
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('fields_index.json'):
        print(f.parent); sys.exit(0)
print(h/'.claude/skills/nc-aoc-cr-forms')
" 2>/dev/null)
python3 -c "
from pathlib import Path
pdf_dir = Path('$SKILL_DIR/pdfs')
matches = list(pdf_dir.glob('AOC-CR-XXX*.pdf'))
print(matches[0].name if matches else 'NOT_FOUND')
"
```

Replace `AOC-CR-XXX` with the actual form number.

If the result is `NOT_FOUND`:

1. Check whether it exists in the full NC AOC catalog:

```bash
SKILL_DIR=$(python3 -c "
import pathlib as P, sys
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('fields_index.json'):
        print(f.parent); sys.exit(0)
print(h/'.claude/skills/nc-aoc-cr-forms')
" 2>/dev/null)
python3 -c "
import json
with open('$SKILL_DIR/index.json') as f:
    data = json.load(f)
form = next((d for d in data if d.get('form_number','').upper() == 'AOC-CR-XXX'), None)
print(form['title'] if form else 'NOT_IN_CATALOG')
"
```

2. If found in the catalog, tell the user:
   > "**AOC-CR-XXX** (*title*) isn't in your local form library yet. Would you like to download it now? It will be saved to your forms folder and added to forms.txt for future use."

3. If the user agrees, download it:

```bash
SKILL_DIR=$(python3 -c "
import pathlib as P, sys
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('fields_index.json'):
        print(f.parent); sys.exit(0)
print(h/'.claude/skills/nc-aoc-cr-forms')
" 2>/dev/null)
python3 "$SKILL_DIR/download_form.py" AOC-CR-XXX
```

4. If the form is not in the catalog at all, tell the user it doesn't exist in the NC AOC criminal forms series and ask them to double-check the form number.

Only proceed to Phase 2 once the PDF is confirmed to exist locally.

---

## Phase 2 — Load the form's fields

Once the form is identified, read only that form's fields entry:

```bash
SKILL_DIR=$(python3 -c "
import pathlib as P, sys
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('fields_index.json'):
        print(f.parent); sys.exit(0)
print(h/'.claude/skills/nc-aoc-cr-forms')
" 2>/dev/null)
python3 -c "
import json
with open('$SKILL_DIR/fields_index.json') as f:
    data = json.load(f)
form = next(d for d in data if d['form_number'] == 'AOC-CR-XXX')
for field in form['fields']:
    print(field['name'], '|', field['type'], '|', field.get('tooltip',''))
"
```

Group the fields into logical sections to ask the user for information efficiently. Common groupings:

- **Case identification**: County, file number, case number, court date
- **Defendant information**: Name, DOB, address, race, sex
- **Offense information**: Charge, statute, date of offense, G.S. citation
- **Issuing official**: Judge, magistrate, clerk name and signature fields
- **Disposition/outcome**: Verdict, sentence, conditions

Do not ask for fields that are clearly internal/administrative (signature lines, date-stamped fields, sequence numbers) unless the user specifically needs them.

---

## Phase 3 — Gather values from the user

Ask for missing information conversationally. Batch related fields into a single question.

For checkboxes, present them as yes/no questions or multiple-choice where a group of checkboxes represents alternatives (e.g., "Was the offense a: felony / misdemeanor?").

For fields with obvious defaults given context (e.g., StateField = "NC"), propose the default and let the user confirm or override.

---

## Phase 4 — Fill and output the PDF

Build a JSON values file and call the fill script:

```bash
SKILL_DIR=$(python3 -c "
import pathlib as P, sys
h = P.Path.home()
for base in [h/'.claude', h/'Library'/'Application Support'/'Claude']:
    if not base.exists(): continue
    for f in base.rglob('fields_index.json'):
        print(f.parent); sys.exit(0)
print(h/'.claude/skills/nc-aoc-cr-forms')
" 2>/dev/null)
python3 "$SKILL_DIR/fill_form.py" \
  "AOC-CR-XXX" \
  '{"FieldName": "value", "CheckboxField": true, ...}' \
  "/path/to/output_filled.pdf"
```

Default output path: same directory as the source PDF, with `_filled` appended to the filename.

After filling, report:
- How many fields were filled
- Any fields that were skipped (not found in the PDF)
- The output file path

---

## Notes on form language

Many forms exist in English and Vietnamese (indicated by Vietnamese titles). English forms are preferred unless the user requests otherwise. The form number is identical — select the file with the English title.

## Common field name patterns

- `CountyName` — NC county
- `DefendantName`, `DefendantDOB`, `DefendantRace`, `DefendantSex`
- `OffenseName`, `OffenseDate`, `StatuteViolated`
- `FileNo`, `CaseNo` — court docket identifiers
- `*CkBox` suffix — checkbox field
- `*Field` suffix — text field paired with a nearby checkbox
- `Judge*`, `Magistrate*`, `ClerkOfCourt*` — official signatures/names

## Error handling

If `fill_form.py` reports skipped fields, check whether the field name has a variant spelling by searching the fields list directly. Field names in these forms are camelCase and occasionally inconsistent between form versions.

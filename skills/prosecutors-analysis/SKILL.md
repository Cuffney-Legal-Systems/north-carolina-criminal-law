---
name: prosecutors-analysis
description: >-
  Generate a North Carolina prosecutorial summary (prosecutor's analysis) from a
  police report or fact pattern — a tight, scannable probable-cause screening of
  each charged offense with elements drawn verbatim from the NC Pattern Jury
  Instructions, proof anchored in direct quotes from the report, followed by
  weaknesses, defenses, identification analysis, and a bottom-line charging
  recommendation. Use when the user asks for a "prosecutorial summary",
  "prosecutor's analysis", "case screening", "charging analysis", asks "is there
  probable cause" or "should this case be prosecuted", or attaches/points to a
  police report (incident report, arrest report, officer narrative) and asks for
  an analysis of the charges. Prosecution-side; North Carolina criminal only.
  Output is a `.docx` draft for prosecutor review — never a charging decision.
version: 26.08.26.01
---

# Prosecutor's Analysis (NC)

This skill produces the prosecutorial summary described in *Ethically Implementing
Generative Artificial Intelligence in Prosecution* (Cuffney, Northwestern
University, 2025): a succinct statement of the facts plus a legal analysis of
each charged offense, answering one question — **do the available facts support
probable cause to proceed on each charge?**

## The two rules that govern everything else

**1. Write for a prosecutor, not a law student.** The reader tries these cases.
They know what intent is, what constructive possession means, what probable
cause requires. Never explain an element — **state the element, state the proof,
state the verdict.** Legal exposition is not thoroughness; it is padding that
buries the three facts that decide the case.

**2. As short as the case allows — and no shorter.** A screening summary a
prosecutor won't finish reading has failed. But a summary that is brief because
it left facts out has failed worse: the prosecutor is making a charging decision
on it, and an incomplete factual picture is the one defect that cannot be
corrected downstream.

So the budget **scales with the case**, and it is a target, not a ceiling:

> **≈ 1,200 words of core + ≈ 250 words per charge.**
> Two charges ≈ 1,700 words. Four ≈ 2,200. Six ≈ 2,700.

The core — Summary, Weaknesses, Defenses, Identification, Bottom Line — grows
with the *report*, not with the charge count; the per-charge element tables are
what scale with charges. Most of the core is Section 1, and that is deliberate:
**the factual chronology is the one section where completeness beats
compression.** A prosecutor who cannot reconstruct the case from Section 1 cannot
use the rest of the document. Count prose against the budget, not the element
tables and verbatim quotes: those are the compression mechanism, not the padding.

Running over is a signal to re-read for padding, **not an instruction to cut
analysis**. Length comes out of *explanation* — never out of a fact, a weakness,
a defense, a discrepancy, or a fact gap. If the case genuinely needs more room
(many charges, multiple defendants, contradictory narratives, a long
investigative history), take it, and say in one line at the end why the summary
ran long.

Corollaries, all load-bearing:

- **Each fact appears once — and the Summary is where facts live.** Section 1
  carries the narrative record; Sections 2–6 carry verdicts, problems, and
  recommendations. Later sections point back by short tag ("the clothing
  mismatch," "the March 20 CODIS hit") and add only what is new — the element it
  proves, the weakness it creates. Re-narrating the incident under Weaknesses,
  and again under Identification, is what turns three pages into fifteen.
- **Quote the report instead of narrating it.** A verbatim quote with its source
  is shorter than a paraphrase, carries the scenario with it, and is verifiable.
  This is the mechanism that gets the page count down without losing context.
- **Format for scanning.** Element tables, bolded status verdicts, bolded bullet
  labels, italic cites, a case-critical flag at the top. See
  `reference/summary-template.md`.

## Design rules from the thesis testing

Six career prosecutors evaluated AI-generated summaries across ten real CMPD
cases. Their criticisms are the rules:

1. **Elements must mirror the pattern jury instructions.** The most consistent
   criticism was paraphrased element language. Never state elements from memory
   — load the N.C.P.I.—Crim. instruction and use its words. The jury hears the
   pattern instruction; so should the screening summary.
2. **Defenses must always be analyzed** — self-defense, accident, alibi — even
   when the answer is "no defense is supported by these facts."
3. **Weaknesses and discrepancies must be surfaced, not smoothed over.** All six
   evaluators caught the same overlooked clothing-description discrepancy the AI
   missed. Discrepancies rarely decide a case, but a summary that hides them
   cannot be trusted.
4. **Every fact must trace to the source report.** No inferred facts ("the
   vehicle was occupied", "the injury was serious") — if the report doesn't say
   it, it is a fact gap, not a narrative sentence.
5. **Facts need their scenario, but not a paragraph of it.** Evaluators rejected
   stripped bullet fragments ("Defendant pushed the victim"). A direct quote
   plus its source carries the scenario in a fraction of the words — prefer it
   to both the fragment and the paragraph.

## Ethical frame

Under N.C. Rule of Professional Conduct 3.8, a prosecutor must refrain from
prosecuting a charge the prosecutor knows is not supported by probable cause;
ABA Criminal Justice Standard 3-4.3 requires charges be supported by probable
cause and sufficient admissible evidence. This skill drafts the screening
analysis that informs that judgment. **It never makes the judgment.** The
output is labeled a draft, and the bottom line frames a recommendation for the
reviewing prosecutor — supporting, not replacing, prosecutorial judgment.

## Companion skills

This skill builds on two sibling skills that ship in this same
`north-carolina-criminal-law` plugin:

- **north-carolina-pattern-jury-instructions** — source of element language,
  defense instructions, and the facts-to-elements method.
- **north-carolina-general-statutes** — full text of G.S. Chapter 14 for
  statute lookups, offense classification, and cross-references.

## Phase 0 — Locate skill directories

Every bash block begins by locating this skill and the two companion skills:

```bash
eval "$(python3 -c "
import os, shlex, pathlib as P

def find(skill_name, marker):
    root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if root:
        cand = P.Path(root) / 'skills' / skill_name
        if (cand / marker).exists():
            return cand
    h = P.Path.home()
    bases = [h/'.claude', h/'Library'/'Application Support'/'Claude', P.Path.cwd()]
    for base in bases:
        if not base.exists(): continue
        try:
            for f in base.rglob(marker):
                if f.parent.name == skill_name and '.git' not in str(f):
                    return f.parent
        except (PermissionError, OSError):
            continue
    return None

ji = find('north-carolina-pattern-jury-instructions', 'catalog.json')
gs = find('north-carolina-general-statutes', 'catalog.json')
pa = find('prosecutors-analysis', 'SKILL.md')
print('JI_DIR=' + shlex.quote(str(ji or '')))
print('GS_DIR=' + shlex.quote(str(gs or '')))
print('PA_DIR=' + shlex.quote(str(pa or '')))
")"
echo "Jury instructions: $JI_DIR"
echo "General statutes:  $GS_DIR"
echo "This skill:        $PA_DIR"
```

If `JI_DIR` or `GS_DIR` is empty, the companion skill's library could not be
located — normally a broken or partial plugin install, since both ship in this
same plugin. Fall back gracefully: state which library is missing, suggest
reinstalling or updating the `north-carolina-criminal-law` plugin, and — only if
the user wants to proceed anyway — flag prominently that element language could
not be verified against the pattern instructions (Rule 1 above is violated; say
so in the output).

Reuse `$JI_DIR`, `$GS_DIR`, and `$PA_DIR` in every subsequent bash block.

## Workflow

### Step 1 — Intake the case materials

Identify the source materials: police report(s), incident/arrest reports,
officer narratives, supplements, witness statements. Accept a file path, an
attached document, or pasted text.

- If a case folder exists (a `CLAUDE.md` in the working directory or
  case-related files in `pwd`) and the `case-file-harvester` agent is
  available, spawn it to extract defendant identity, charges, offense dates,
  and document inventory before reading anything yourself. Otherwise scan the
  folder inline.
- PDFs: extract text (e.g., `pypdf`) rather than rendering pages when the
  report is long.
- **Redacted reports:** if names are redacted, use generic placeholders (John
  Doe 1, Jane Doe 1) consistently — one placeholder per person, tracked across
  the whole report.
- **Degraded text layers.** Scanned and re-converted CMPD exports often OCR
  badly — dropped words, merged lines, redaction bars read as characters. Quote
  only what is actually legible. Where a quotation is partly reconstructed,
  mark it `[OCR]` and say so in the header; never silently repair a quote into
  fluent English. Note in the source line that quotes must be verified against
  the original before use in a charging document. A confidently misquoted
  report is worse than no quote.
- **Build a quote bank as you read.** Pull the verbatim lines that carry
  elements, defenses, identifications, and discrepancies, each tagged with its
  source (narrating officer, witness, supplement, page). These quotes are the
  raw material of the draft — the finished summary should be largely quotes
  plus verdicts.
- Note the report's own quality problems (disorganized narratives, internal
  contradictions, missing supplements). These feed Weaknesses.

### Step 2 — Establish the charges

- If the user named charges or statutes, analyze exactly those. Do not lower
  the analysis's grade for uncharged offenses, but you may note additional
  supported charges in one sentence at the end.
- If no charges were given, identify candidates from the facts using
  `$JI_DIR/reference/by_offense.json` (keyword search) and
  `$JI_DIR/catalog.json`. Include obvious lesser-included offenses (e.g.,
  common law robbery under robbery with a dangerous weapon). State the
  candidate list in a line or two before analyzing — not a discussion.

### Step 3 — Load the law (never work from memory)

For **each** charge:

1. **Statute text:** read `$GS_DIR/statutes/GS-14-{N}.md` (decimal sections use
   underscores: `GS-14-34_1.md`; Chapter 90 drug offenses are outside the
   Chapter 14 library — quote the user's charging language and say the full
   statute text is not in the local library).
2. **Pattern instruction:** map the statute via
   `$JI_DIR/reference/by_statute.json`, then read
   `$JI_DIR/reference/instructions/<number>.md` (dots become underscores:
   `217.30` → `217_30.md`). If several instructions fit (with-weapon vs.
   without, degrees), load all plausible ones.
3. **Defense instructions:** scan the facts for any hint of a legal defense —
   a self-defense claim, an "it was an accident" statement, mutual combat, the
   suspect underneath the victim, alibi. If any appears, load the matching
   defense instruction(s) (e.g., N.C.P.I.—Crim. 308.45 self-defense for
   deadly-force assaults). The thesis's worst-rated case failed precisely
   because self-defense and accident went unanalyzed.

Then read `$PA_DIR/reference/issue-checklists.md` and note which checklists
apply. **The checklists are a sweep you run, not sections you write** — only
the hits reach the page.

### Step 4 — Element-by-element analysis

Follow the facts-to-elements method from the jury instructions skill:

- **Multiple charges and the `offense-elements-analyzer` agent is available:**
  spawn one agent per charge in parallel, passing `INSTRUCTION_NUMBER`,
  `INSTRUCTION_FILE`, `FACTS`, and `USER_ROLE: prosecution`. Aggregate the
  results — and compress them; agent output is working material, not draft
  prose.
- **Otherwise analyze inline:** for each numbered element, take the pattern
  language verbatim, attach **the single strongest quote from the report**
  bearing on it, and mark it **SUPPORTED / CONTESTED / NOT SUPPORTED / GAP**.

This step produces a table, not an essay. Reserve prose for the elements that
are contested, unsupported, or missing facts: what is missing, and what
evidence would fix it. Supported elements need no commentary at all.

### Step 5 — Draft the summary

Compose in markdown — it is the **working draft**, not the deliverable. The
finished product is a `.docx` (Step 7). Write it to a scratch `.md` file so the
verification pass in Step 6 has something to diff against; that scratch file is
not delivered and should not be left in the output folder.

Read **both** reference files before writing:

- `$PA_DIR/reference/summary-template.md` — section structure, word budgets,
  formatting conventions.
- `$PA_DIR/reference/example-output.md` — a complete two-charge summary at the
  target length. **Match its density.** When in doubt about how much to write,
  it is the answer.

Compose the report using the six-section template:

**SUMMARY → CHARGE ANALYSIS → WEAKNESSES → DEFENSES → IDENTIFICATION →
BOTTOM LINE**

**Write Section 1 first, and write it long.** It is a factual chronology in two
parts — *1A. The incident* (narrative prose) and *1B. Investigative chronology*
(dated entries from first response through the latest supplement, including the
steps that produced nothing). Build 1B directly from the report's narrative and
supplement list: one entry per supplement, in date order, each attributed. The
quote bank from Step 1 is the raw material. Sections 2–6 then refer back to the
chronology by date or short tag instead of re-narrating it.

(The thesis's seven-section format listed Elements and Analysis separately.
They are merged here into a single per-charge table with element language in
one column and proof in the next — the duplication between those two sections
was the largest single source of overlong drafts. Element language still
appears verbatim, which is what evaluators demanded.)

Drafting rules:

- **Element tables** with a **Status** column and a **Proof** column carrying
  the direct quote. Prose only for CONTESTED / NOT SUPPORTED / GAP elements.
- **Weaknesses, Defenses, Identification** get short paragraphs or labeled
  bullets — never bare fragments, never a page each. Word budgets are in the
  template.
- **Quote significant suspect and witness statements verbatim.** Words like
  *"run that"* can carry the intent element of conspiracy. Keep quotes under
  about 25 words and always attribute them.
- **Precise statement language:** an admission of presence or knowledge is
  **not** a confession to the crime. Never upgrade one, even where the report
  says "confession."
- **Emphasis carries meaning:** bold status verdicts, bullet labels, and the
  two or three facts the case turns on; italics for cites and recommendations;
  a `>` case-critical flag under the header for the issue that most threatens
  the case (at most two per report).
- **Cite** each instruction with number and revision year (*N.C.P.I.—Crim.
  217.30 (rev. 2023)*) and each statute as G.S. 14-{N}.

### Step 6 — Verification pass (mandatory)

Before delivering, re-read the draft against the source report and
`$PA_DIR/reference/issue-checklists.md`:

1. **Fact trace:** every factual assertion must appear in the source materials.
   Anything inferred (vehicle occupancy, injury seriousness, who possessed
   which item) is removed or moved to fact gaps. This is the anti-hallucination
   gate.
2. **Chronology completeness:** every narrative and supplement in the report's
   own report list appears somewhere in Section 1B, in date order, with what it
   produced — including the ones that produced nothing. A supplement that never
   reaches the chronology is a supplement the prosecutor will not know exists.
3. **Discrepancy sweep:** descriptions vs. actual appearance at arrest,
   contradictions between narratives, non-identifications, show-up vs. lineup
   procedure, visibility and lighting limits. Every discrepancy found goes in
   Weaknesses or Identification — including the ones that don't change the
   outcome.
4. **Element language check:** diff each element against the loaded instruction
   file; fix any paraphrase.
5. **Checklist hits:** confirm every applicable checklist item that *hit* was
   addressed. Items that came up clean stay off the page.
6. **Length and redundancy gate — run this last, and actually cut.** Compare
   the draft against `$PA_DIR/reference/example-output.md`; if it runs
   substantially longer per charge, it is over-written.

   - Over the scaled budget (≈ 1,200 + 250 per charge)? Re-read for padding and
     cut what the next four checks find. If the draft is still over after those
     cuts are made, it is long because the case is — leave it, and add the
     one-line note explaining why.
   - Any fact stated in two sections? Keep it where it does the most work;
     replace the other with a short back-reference.
   - Any sentence explaining a legal concept to a prosecutor? Delete it.
   - Any SUPPORTED element carrying prose? Delete the prose.
   - Any contested or dispositive fact lacking a quote where the report
     supplies one? Add the quote.
   - **Then check the other direction**: is any charge, weakness, defense,
     discrepancy, identification problem, or fact gap missing or thinned to fit?
     Put it back. Under-inclusion is the worse failure.

State in one line at the end that the verification pass was run.

### Step 7 — Deliver

**The deliverable is a `.docx`. Always produce it — do not ask first, and do not
deliver a `.md` file as the output.** Markdown is the working format only.

**How to render it.** This skill ships its own renderer, which already encodes
every formatting convention below:

```bash
python3 "$PA_DIR/scripts/summary_to_docx.py" <working-draft.md> <output.docx>
```

It needs `python-docx` (`pip install python-docx`). It converts the fenced
header block and closing notice into bordered blocks, `>` flags into shaded
call-outs, pipe tables into real Word tables with repeating header rows, and
inline `**bold**` / `*italic*` / `` `code` `` into Word runs — on US Letter,
1" margins, Times New Roman 11 pt, page numbers in the footer.

Use it by default. Fall back to the `docx` skill (`anthropic-skills:docx`) only
if the renderer is unavailable or the user wants a layout it does not produce
(office letterhead, a different type family, a cover page).

**Where it goes.** Default to the **project working directory** — the folder the
session was started in. Two overrides, in order:

1. If the user named an output folder, use it.
2. If the analysis was run against a **case/matter folder** (a `CLAUDE.md` or
   case documents in `pwd`), write the `.docx` there instead and say so — a
   matter-specific location beats the project root for real case work.

Never write the output alongside the source police report if that report lives
outside the project (e.g. a protected-data or discovery directory). Keep the
report where it is and the analysis in the project.

**Filename:** `prosecutorial-summary.{case-number}.{YYYY-MM-DD}.docx` — case
number as it appears on the report, non-alphanumerics collapsed to hyphens.
Example: `prosecutorial-summary.20171223-2304-00.2026-08-26.docx`.

**Formatting the Word document.** These are what the bundled renderer produces.
If you render any other way, reproduce them — a `.docx` that loses the element
tables has lost the format evaluators asked for:

- Header block → a plain paragraph block at the top (not a Word header), single
  spaced, above the title.
- Case-critical flag(s) → an indented, bordered or shaded single-line paragraph,
  bold lead-in. It must remain visually distinct from body text.
- Element tables → real Word tables with a header row, four columns
  (`#` / Element / Status / Proof), header row bold and repeating across pages.
  Never flatten a table into a list.
- Status verdicts, bullet labels, and the two or three facts the case turns on →
  bold. Cites and recommendations → italic.
- Bottom-line table → a real three-column Word table.
- Closing verification and disclaimer block → set apart at the end, smaller or
  boxed, so it reads as a notice rather than analysis.
- Portrait, US Letter, 1" margins, a serif body face at 11–12 pt. Page numbers
  in the footer.

**Confirm it rendered.** Re-open the `.docx` and check the table count and
dimensions before delivering — a silently flattened table is the failure mode
that matters:

```bash
python3 -c "
from docx import Document
d = Document('<output.docx>')
print('tables:', len(d.tables))
for i, tb in enumerate(d.tables):
    print(i, len(tb.rows), 'x', len(tb.columns), [c.text[:20] for c in tb.rows[0].cells])
"
```

There should be one table per charge plus the bottom-line table.

**Then, in chat:**

- Give the file path and a two-or-three-line orientation — the bottom-line
  verdicts and the case-critical flag. Do **not** paste the whole summary back
  into chat; the document is the deliverable.
- Offer the official SOG PDF links for every instruction cited (look up
  `source_url` in `$JI_DIR/catalog.json`).
- Offer the markdown working draft as a separate file only if the user asks for
  it (e.g. to diff revisions).
- Close with the review disclaimer (built into the template): the summary is a
  draft prepared with AI assistance for prosecutor review; the charging
  decision belongs to the prosecutor.
- If the user wants the long-form reasoning behind any verdict, give it in
  chat. It does not go back into the document.

## Guardrails

- **Draft only, never a decision.** The bottom line recommends and explains; it
  never states that the office "will" or "must" charge, and never asserts a
  charge "will" succeed or fail at trial. Probable-cause sufficiency language
  only (could a reasonable jury find each element).
- **No fabricated or assumed facts.** A gunshot wound is not "serious injury"
  until the report describes severity or treatment. A parked car is not
  "occupied" because someone shot at it. When a needed fact is missing, name it
  as a gap.
- **Quotes are verbatim.** Trim with ellipses; never adjust wording, and never
  attribute a quote to the wrong narrative. A misquoted report is worse than no
  quote.
- **Brevity never costs coverage.** Weaknesses, Defenses, and Identification
  are never omitted or reduced to "none noted" without an explicit statement of
  what was checked. Cut words, not analysis.
- **Confidentiality.** Police reports contain victim and witness information
  and may be subject to protective orders. Keep every output — the `.docx` and
  any working draft — on the local filesystem, in the project or matter folder
  per Step 7; never transmit report contents to external services, and never
  publish a summary as a web artifact.
- **Jurisdiction.** North Carolina criminal law only. If asked to run this on
  another state's report, say it is out of scope (federal work belongs to the
  sentencing-memo and motion skills, not this one).
- **Currency.** Pattern instructions and scraped statutes may lag amendments;
  recommend verification against current G.S. and appellate authority for
  anything dispositive.

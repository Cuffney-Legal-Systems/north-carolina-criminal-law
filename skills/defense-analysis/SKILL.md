---
name: defense-analysis
description: >-
  Generate a North Carolina defense case analysis from a police report,
  discovery, or fact pattern — a scannable, attorney-work-product assessment of
  where the State's case is weak and what defenses the client actually has.
  Per-charge element tables with elements quoted from the NC Pattern Jury
  Instructions and the State's proof quoted from the report, then a long
  "Weaknesses in the State's Case" section (witness credibility, sloppy police
  work, investigative gaps, suppression exposure, contradictions), affirmative
  and negating defenses, identification attack, a bottom line per charge, and
  immediate action items. Use when the user asks for a "defense analysis",
  "defense case review", "weaknesses in the State's case", "what are my
  defenses", "case assessment for the defendant", asks "how do I attack this
  case" or "is this triable", or attaches/points to a police report or
  discovery and asks for an analysis on behalf of the defendant. Defense-side;
  North Carolina criminal only. Output is a privileged `.docx` work-product
  draft for defense counsel — never advice to a client and never a filing.
version: 26.08.26.01
---

# Defense Analysis (NC)

The mirror image of the `prosecutors-analysis` skill in this same plugin. That
skill asks whether the State can prove every element. **This one asks where the
State's case breaks.**

The asymmetry is the whole design. A prosecutor must carry every element; defense
counsel needs **one** — one element without substantial evidence, one witness who
cannot survive cross, one search that cannot survive a suppression hearing, one
identification procedure that should never have happened. This skill runs the
record looking for those, names each one, and says what to do with it.

## The three rules that govern everything else

**1. The report is the State's version, not the facts.** Every sentence in a
police report is an allegation written by an interested party, usually from
memory, often from a second-hand account. The analysis never adopts it. Write
*"Doe 1 told Ofc. Reyes the lot was dark"* — never *"the lot was dark."*
Attribution is not a stylistic preference here; an unattributed allegation in a
defense memo is a fact counsel may stop testing. Where the report asserts a
conclusion (*"the victim sustained serious injury," "the defendant confessed"*),
name the conclusion as a conclusion and ask what fact supports it.

**2. Write for a trial lawyer, not a law student.** The reader tries these cases.
They know what constructive possession is and what *Miranda* requires. Never
explain a doctrine — **name the problem, quote the proof, name the use.** Every
weakness ends in a verb: *cross on it, move to suppress it, demand it in
discovery, argue it at the close of the State's evidence, get the expert.* A
weakness with no use attached is an observation, not work product.

**3. Under-inclusion is the failure that matters.** The prosecutor's version
optimizes for brevity because a charging screen that goes unread has failed.
This document is different: it is the issue inventory counsel works from for the
life of the case. A weakness left off the page is a weakness that never gets
litigated. So:

> **≈ 1,400 words of core + ≈ 250 words per charge — and the Weaknesses section
> is exempt from the budget.**

Sections 1, 2, 4, 5, 6 and 7 stay tight. **Section 3 runs as long as the record
supports.** If the report documents fourteen real problems, list fourteen. Cut
explanation, never a problem. If the draft runs long because the case is bad for
the State, that is the document working.

Corollaries, all load-bearing:

- **Each fact appears once — and the Summary is where facts live.** Section 1
  carries the narrative record; Sections 2–7 carry attacks, defenses, and tasks.
  Later sections point back by short tag ("the clothing mismatch," "the 06/04
  array") and add only what is new. Re-narrating the incident under Weaknesses,
  and again under Identification, is what turns four pages into twenty.
- **Quote the report instead of narrating it.** A verbatim quote with its source
  is shorter than a paraphrase, is what counsel will read to the witness on
  cross, and is verifiable against the file. This is the mechanism that keeps
  the page count down without losing anything.
- **Format for scanning.** Element tables, bolded strength verdicts, bolded
  bullet labels, italic cites, a best-issue flag at the top. See
  `reference/analysis-template.md`.

## What this document is for

Four uses, in the order counsel needs them:

1. **The first-look assessment** — after arraignment, before the client meeting:
   what is this case, and how bad is it.
2. **The motions inventory** — what can be suppressed, dismissed, severed, or
   compelled, and on what ground.
3. **The cross-examination outline seed** — every contradiction, omission, and
   credibility problem, with the report's own words attached.
4. **The negotiation posture** — what counsel actually holds when the ADA calls.

It is **not** a filing, not advice to the client, and not a prediction of the
verdict. See Guardrails.

## Design rules

These come from the same evaluator findings that produced the prosecution skill
(*Ethically Implementing Generative Artificial Intelligence in Prosecution*,
Cuffney, Northwestern University, 2025), inverted for the defense reader. The
finding that matters most: across ten real CMPD cases, the discrepancies the AI
smoothed over were the ones every evaluating prosecutor caught. **A prosecutor
who spots the clothing mismatch in their own file expects the defense to build a
case on it.** The defense version's job is to never be the one who missed it.

1. **Elements must mirror the pattern jury instructions.** Never state elements
   from memory — load the N.C.P.I.—Crim. instruction and use its words. This is
   the language the jury will hear and the language a motion to dismiss is
   measured against. A paraphrased element is a missed defense.
2. **Every defense gets analyzed, including the ones nobody named.** A claim
   appearing anywhere in the record (*"she said it was an accident"*), or a
   physical fact that implies one (the suspect found underneath the victim),
   triggers full analysis against its pattern instruction — with what supports
   it, what rebuts it, and what investigation would develop it.
3. **Every discrepancy is an asset.** Where the prosecution skill surfaces
   discrepancies for candor, this one surfaces them because they are the
   product. Contradictions between narratives, description mismatches,
   non-identifications, timeline problems, omitted supplements — all of it goes
   on the page, including the small ones. Small contradictions are how a witness
   loses a jury.
4. **Every assertion traces to the source.** No inferred facts, in either
   direction. The State's evidence is not weaker than the report says, and
   inventing a weakness the record does not support wastes counsel's time and
   damages credibility when it collapses at the hearing.
5. **What the investigation did not do is evidence.** The uncanvassed block, the
   untested swab, the witness never re-contacted, the BWC never pulled, the lab
   request with no result — these are the backbone of a reasonable-doubt
   argument and they are invisible unless the chronology records them.

## Ethical frame

Defense counsel's obligations under the N.C. Rules of Professional Conduct set
the boundary of what this skill produces:

- **RPC 1.1, 1.3** — competence and diligence require identifying the defenses
  and motions the record supports. Finding them is the job; this skill assists
  it and never replaces counsel's judgment.
- **RPC 3.1** — a defense must have a basis in law and fact that is not
  frivolous. *Note:* in a criminal matter counsel may nevertheless require that
  every element be proved. This skill therefore distinguishes **defenses
  supported by the record** from **failures of the State's proof** — both are
  legitimate, but they are not the same thing and are never blended.
- **RPC 3.3, 3.4** — candor to the tribunal and fairness to opposing counsel.
  This skill identifies weaknesses in the State's evidence and defenses the
  record supports. **It never invents a version of events, never proposes a
  narrative unsupported by the file, and never suggests anything touching how a
  witness should testify.**
- **RPC 1.6 and the work-product doctrine** — the output is privileged attorney
  work product. It is labeled as such, it stays on the local filesystem, and it
  is never filed, served, or shown to the client as advice.

The output is a **draft for defense counsel's review**. Counsel decides what to
file, what to try, and what to tell the client.

## Companion skills

Ships alongside three sibling skills in the `north-carolina-criminal-law` plugin:

- **north-carolina-pattern-jury-instructions** — element language, defense
  instructions, evidentiary and cautionary instructions, facts-to-elements
  method.
- **north-carolina-general-statutes** — full text of G.S. Chapter 14.
- **prosecutors-analysis** — the mirror skill. If a prosecutorial summary of the
  same case already exists in the folder, read it: it is a map of what the other
  side already knows is weak.

## Phase 0 — Locate skill directories

Every bash block begins by locating this skill and the two law libraries:

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
da = find('defense-analysis', 'SKILL.md')
print('JI_DIR=' + shlex.quote(str(ji or '')))
print('GS_DIR=' + shlex.quote(str(gs or '')))
print('DA_DIR=' + shlex.quote(str(da or '')))
")"
echo "Jury instructions: $JI_DIR"
echo "General statutes:  $GS_DIR"
echo "This skill:        $DA_DIR"
```

If `JI_DIR` or `GS_DIR` is empty, the companion library could not be located —
normally a broken or partial plugin install, since all of them ship together.
Fall back gracefully: say which library is missing, suggest reinstalling or
updating the `north-carolina-criminal-law` plugin, and — only if the user wants
to proceed anyway — flag prominently that element language could not be verified
against the pattern instructions (Design rule 1 is violated; say so in the
output).

Reuse `$JI_DIR`, `$GS_DIR`, and `$DA_DIR` in every subsequent bash block.

## Workflow

### Step 1 — Intake the case materials

Identify the source materials: police report(s), incident/arrest reports,
officer narratives, supplements, witness statements, discovery productions,
warrants and applications, BWC logs, lab reports. Accept a file path, an
attached document, or pasted text.

- If a case folder exists (a `CLAUDE.md` in the working directory or
  case-related files in `pwd`) and the `case-file-harvester` agent is available,
  spawn it to extract defendant identity, charges, offense dates, and document
  inventory before reading anything yourself. Otherwise scan the folder inline.
- PDFs: extract text (e.g., `pypdf`) rather than rendering pages when the report
  is long.
- **Redacted reports:** if names are redacted, use generic placeholders (John Doe
  1, Jane Doe 1) consistently — one placeholder per person, tracked across the
  whole report. Note that the placeholders will need to be mapped to real names
  before the analysis is usable in the file.
- **Degraded text layers.** Scanned and re-converted exports often OCR badly —
  dropped words, merged lines, redaction bars read as characters. Quote only what
  is actually legible. Where a quotation is partly reconstructed, mark it `[OCR]`
  and say so in the header; never silently repair a quote into fluent English. A
  quote counsel reads to a witness on cross **must** be verifiable against the
  original — say so in the source line. A confidently misquoted report is worse
  than no quote, and worst of all at a suppression hearing.
- **Build a quote bank as you read.** Pull the verbatim lines that carry
  elements, defenses, identifications, contradictions, and admissions of
  investigative failure, each tagged with its source (narrating officer, witness,
  supplement, page). These quotes are the raw material of the draft.
- **Note what is missing from the production.** A report that references a
  supplement, a BWC recording, a 911 call, a lab request, or a photo array that
  is not in the materials provided is a discovery gap. Track these as you read —
  they become Section 7 action items.
- **Note the report's own quality problems** (disorganized narratives, internal
  contradictions, conclusory language, missing supplements). These feed Section 3.

### Step 2 — Identify the client (mandatory — never assume)

**Do not begin the analysis until you know whose lawyer the reader is.** Every
element verdict, every weakness, and every defense in this document is
client-specific. A weakness in the case against the driver is not a weakness in
the case against the shooter — and may be the opposite.

Work it out in this order:

1. **The user already said.** If the request names the client ("analyze this for
   my client Marcus Webb", "I represent Doe 2"), confirm it in one line and move
   on. Do not ask again.
2. **A case folder answers it.** A matter `CLAUDE.md`, a fee agreement, an
   appointment order, a notice of appearance, or a prior filing in the folder
   naming the represented defendant is an answer. State what you found and
   proceed.
3. **Exactly one person is charged or identified as a suspect.** Say so in one
   line — *"Reading this for the sole named defendant, John Doe 1"* — and
   proceed. No question needed.
4. **Otherwise, ask — and ask in terms the report actually supports.** Use
   `AskUserQuestion` with one option per candidate defendant, built from the
   record:

   - **Where names are available**, use them with their role: *"Marcus Webb —
     charged with robbery with a dangerous weapon; alleged to have displayed the
     firearm."*
   - **Where names are redacted or absent**, describe the person by their role in
     the allegation, which is how counsel will recognize their own client:
     *"the alleged shooter (Doe 1)"* / *"the alleged driver of the vehicle (Doe
     2)"* / *"the passenger the purse was recovered from (Doe 3)."*
   - Always include an option for **someone not listed** — an uncharged person, a
     later-added codefendant, or a client the report identifies only by
     description.

   Keep the option labels short and put the identifying detail in the option
   description. Ask this as **one** question; do not interrogate counsel about
   strategy, theory of defense, or what the client says happened. Those come from
   counsel, not from this skill.

**Then, before analyzing, record three things** and carry them through the whole
document:

- **The client's name or designation**, used consistently. Everyone else in the
  case is a codefendant, a witness, or the complaining witness — never "the
  defendant" generically once a client is identified.
- **Which charges are the client's.** Analyze only those. Note a codefendant's
  charge in one line if the client's exposure depends on it (acting in concert,
  conspiracy, accessory), and not otherwise.
- **Whether the record shows a conflict.** If the materials suggest counsel may
  represent more than one codefendant, or that a codefendant has given a
  statement implicating the client, say so plainly in the header flag — RPC 1.7
  and *Bruton* problems are cheaper to spot now than at trial.

**Multi-defendant analysis rules, once the client is fixed:**

- **Attribution is the first attack.** For every element, ask *which defendant
  does the record place there?* Reports routinely say "the suspects" and "they."
  A collective noun is not evidence against the client — mark it, quote it, and
  make it a weakness.
- **Acting in concert (*N.C.P.I.—Crim. 202.10*) is the State's bridge.** If the
  client's exposure runs through it, load the instruction and analyze it as its
  own element block: presence, common purpose, and acts in furtherance. The
  defense attack is usually mere presence.
- **Severance and codefendant statements.** If a codefendant's statement
  implicates the client, flag the *Bruton* problem and the severance motion (G.S.
  15A-927 — verify text; Chapter 15A is not in the local statute library).
  *N.C.P.I.—Crim. 101.42* (multiple defendants, guilt determined separately) is
  the corresponding jury instruction to request.
- **Antagonistic defenses.** If the best defense available to the client is that
  a codefendant did it, say so — and say what it costs (severance posture, joint
  trial dynamics).

### Step 3 — Establish the charges

- If the user named charges or statutes, analyze exactly those.
- If no charges were given, identify them from the record (charging language on
  the report, warrant, or magistrate's order) or from the facts using
  `$JI_DIR/reference/by_offense.json` (keyword search) and `$JI_DIR/catalog.json`.
- **Always identify the lesser-included offenses**, even when the State has not
  charged them. On the defense side these are not an afterthought — they are the
  fallback verdict counsel may want the jury instructed on, and the shape of any
  plea. Name them per charge with their instruction numbers.
- **Note over-charging.** Where the record supports a lesser offense but the
  greater was charged, that is a negotiating fact and a Section 6 line. Where two
  charged offenses arise from a single act, flag the double-jeopardy or
  merger-at-sentencing question for counsel to research.
- State the charge list and the lesser-included map in a line or two before
  analyzing — not a discussion.

### Step 4 — Load the law (never work from memory)

For **each** charge against the client:

1. **Statute text:** read `$GS_DIR/statutes/GS-14-{N}.md` (decimal sections use
   underscores: `GS-14-34_1.md`; Chapter 90 drug offenses and Chapter 15A
   procedure are outside the Chapter 14 library — quote the charging language and
   say the full statute text is not in the local library and must be verified).
2. **Pattern instruction:** map the statute via
   `$JI_DIR/reference/by_statute.json`, then read
   `$JI_DIR/reference/instructions/<number>.md` (dots become underscores:
   `217.30` → `217_30.md`). Load the lesser-included instructions too.
3. **Defense instructions:** read `$DA_DIR/reference/defenses-catalog.md` and
   sweep the record against it. Load every defense instruction the facts could
   plausibly reach — not only the ones someone named. The catalog maps each NC
   defense to its instruction number and to the facts that trigger it.
4. **Evidentiary and cautionary instructions.** These are defense leverage the
   prosecution skill has no reason to look for, and they are in the same library:
   *104.90* (identification of defendant as perpetrator), *104.98* (photo lineup
   requirements), *104.20* (interested witness), *104.25* (accomplice testimony),
   *104.30* (informer or undercover agent), *104.05* (circumstantial evidence),
   *104.41* (actual-constructive possession), *105.20/105.21* (impeachment by
   prior statement; contradictory statements), *101.10* (burden of proof and
   reasonable doubt), *101.30* (defendant's decision not to testify), *101.42*
   (multiple defendants). Load the ones the record puts in play and name them
   where they belong — an instruction counsel can request is a concrete use.

Then read `$DA_DIR/reference/weakness-checklists.md` and note which checklists
apply. **The checklists are a sweep you run, not sections you write** — only the
hits reach the page.

### Step 5 — Element-by-element analysis, from the defense side

- **Multiple charges and the `offense-elements-analyzer` agent is available:**
  spawn one agent per charge in parallel, passing `INSTRUCTION_NUMBER`,
  `INSTRUCTION_FILE`, `FACTS`, and **`USER_ROLE: defense`**. The agent's
  perspective note returns which elements are most vulnerable. Aggregate and
  compress — agent output is working material, not draft prose.
- **Otherwise analyze inline.** For each numbered element, take the pattern
  language verbatim, attach **the single strongest piece of the State's proof**
  (a direct quote from the report wherever one exists), and answer two questions:

  **How strong is the State here?**

  | Verdict | Meaning |
  |---|---|
  | **STRONG** | Direct, attributed evidence a jury would readily accept. Do not spend trial capital here. |
  | **CONTESTED** | Evidence exists but rests on a witness, an inference, or a disputed fact. This is where cross works. |
  | **WEAK** | Thin, purely circumstantial, or internally contradicted. A live sufficiency argument. |
  | **NO PROOF** | Nothing in the record establishes it. Motion to dismiss at the close of the State's evidence. |

  **What is the attack?** One clause, concrete and actionable: the cross-exam
  point, the missing fact, the suppression theory, the competing inference, the
  instruction to request. An element with no attack gets *"—"*, not a
  rationalization.

This step produces a table, not an essay. Reserve prose for elements rated WEAK
or NO PROOF — what is missing, why the State cannot fill it from this record, and
what motion it feeds. STRONG elements get no commentary at all.

**Be honest about STRONG.** A memo that rates every element vulnerable is worth
nothing to counsel; the value of the WEAK verdicts comes entirely from the
credibility of the STRONG ones.

### Step 6 — Run the weakness sweep

This is the section the document exists for, and it deserves its own pass.
Working from `$DA_DIR/reference/weakness-checklists.md`, sweep the record across
every category — witness credibility, investigative gaps and sloppy police work,
physical and forensic evidence, identification, internal contradictions,
constitutional and suppression exposure, charging and procedural defects, and the
charge-specific proof problems.

For each hit, capture four things:

1. **The label** — six words or fewer, bolded. *"Clothing mismatch." "K9 track
   cancelled." "No Miranda warning recorded."*
2. **The problem** — one or two lines, in the report's own words wherever it
   supplies them.
3. **The source** — narrative number, supplement, date, page. Counsel has to find
   it in the file.
4. **The use** — cross, suppress, dismiss, demand in discovery, retain an expert,
   argue in closing, request an instruction. **Every hit ends here.**

Items that come up clean earn no sentence. Do not write "not applicable."

### Step 7 — Draft the analysis

Compose in markdown — it is the **working draft**, not the deliverable. The
finished product is a `.docx` (Step 9). Write it to a scratch `.md` file so the
verification pass in Step 8 has something to diff against; that scratch file is
not delivered and should not be left in the output folder.

Read **both** reference files before writing:

- `$DA_DIR/reference/analysis-template.md` — section structure, budgets, and
  formatting conventions.
- `$DA_DIR/reference/example-output.md` — a complete two-charge analysis at the
  target length and density. **Match its density.**

Compose using the seven-section template:

**SUMMARY → CHARGE ANALYSIS → WEAKNESSES IN THE STATE'S CASE → DEFENSES →
IDENTIFICATION → BOTTOM LINE → ACTION ITEMS**

**Write Section 1 first, and write it long.** It is a factual chronology in two
parts — *1A. The State's account of the incident* (narrative prose, every
assertion attributed to its source) and *1B. Investigative chronology* (dated
entries from first response through the latest supplement, **including every step
that produced nothing**). Build 1B directly from the report's narrative and
supplement list: one entry per supplement, in date order, each attributed. On the
defense side the dead ends carry as much weight as the results — a cancelled K9
track, an uncanvassed block, an unreturned call, a lab request with no report are
each a reasonable-doubt argument, and each is invisible unless the chronology
records it. Sections 2–7 then refer back by date or short tag instead of
re-narrating.

Drafting rules:

- **Element tables** with a **Strength** column and a **Defense attack** column.
  Prose only for WEAK / NO PROOF elements.
- **Weaknesses** is organized under labeled sub-headings by category, bullets
  within each. No cap on length — but no padding either.
- **Defenses and Identification** get short paragraphs or labeled bullets, never
  a page each.
- **Quote significant statements verbatim** and attribute them. Keep quotes under
  about 25 words.
- **Precise statement language, in both directions.** An admission of presence or
  knowledge is not a confession — never let the report's characterization stand.
  Equally, do not downgrade a genuine inculpatory statement into something softer
  than what the report records; counsel needs to know what is actually there.
- **Emphasis carries meaning:** bold strength verdicts, bullet labels, and the
  two or three facts the case turns on; italics for cites and recommendations; a
  `>` flag under the header for the **best issue in the case** (at most two).
- **Cite** each instruction with number and revision year (*N.C.P.I.—Crim. 217.20
  (rev. 2023)*) and each statute as G.S. 14-{N}. Chapter 15A and Chapter 90 cites
  carry *(verify — not in local library)* on first use.

### Step 8 — Verification pass (mandatory)

Before delivering, re-read the draft against the source materials and
`$DA_DIR/reference/weakness-checklists.md`:

1. **Fact trace and attribution.** Every factual assertion appears in the source
   materials **and** is attributed to whose account it comes from. An
   unattributed allegation is a drafting error in this document. Anything
   inferred is removed or moved to fact gaps. This is the anti-hallucination
   gate, and it runs in both directions — no invented weaknesses either.
2. **Client scoping.** Every element verdict, weakness, and defense is about the
   **client**. Scan for any place a codefendant's conduct or a collective noun
   ("the suspects," "they") has been silently attributed to the client. Each one
   found is itself a weakness — move it to Section 3.
3. **Chronology completeness.** Every narrative and supplement in the report's
   own report list appears in Section 1B, in date order, with what it produced —
   including the ones that produced nothing, and including any referenced item
   not actually produced in discovery.
4. **Discrepancy sweep.** Descriptions vs. appearance at arrest, contradictions
   between narratives, non-identifications, show-up vs. lineup procedure,
   visibility and lighting limits, timeline impossibilities. Every discrepancy
   goes in Section 3 or 5 — including the small ones.
5. **Element language check.** Diff each element against the loaded instruction
   file; fix any paraphrase.
6. **Use check.** Every weakness ends in a use. Every WEAK / NO PROOF element
   names its motion. Every defense names what would develop it. Delete or fix any
   bullet that stops at observation.
7. **Checklist hits.** Confirm every applicable checklist item that *hit* was
   addressed. Items that came up clean stay off the page.
8. **Coverage gate — run this last, and check the direction that matters.** Is
   any weakness, contradiction, suppression issue, identification problem,
   defense, lesser-included offense, or discovery gap missing or thinned to fit a
   budget? Put it back. Then, and only then, cut: any sentence explaining a legal
   concept to a trial lawyer, any fact stated in two sections, any prose under a
   STRONG element, any bullet that reads as reassurance rather than a problem.

State in one line at the end that the verification pass was run.

### Step 9 — Deliver

**The deliverable is a `.docx`. Always produce it — do not ask first, and do not
deliver a `.md` file as the output.** Markdown is the working format only.

**How to render it.** This skill ships its own renderer, which already encodes
every formatting convention below:

```bash
python3 "$DA_DIR/scripts/analysis_to_docx.py" <working-draft.md> <output.docx>
```

It needs `python-docx` (`pip install python-docx`). It converts the fenced header
block and closing notice into bordered blocks, `>` flags into shaded call-outs,
pipe tables into real Word tables with repeating header rows (five-column element
tables, three-column bottom-line tables), and inline `**bold**` / `*italic*` /
`` `code` `` into Word runs — on US Letter, 1" margins, Times New Roman 11 pt,
with **ATTORNEY WORK PRODUCT — PRIVILEGED** and page numbers in the footer.

Use it by default. Fall back to the `docx` skill (`anthropic-skills:docx`) only
if the renderer is unavailable or the user wants a layout it does not produce
(firm letterhead, a different type family, a cover page).

**Where it goes.** Default to the **project working directory** — the folder the
session was started in. Two overrides, in order:

1. If the user named an output folder, use it.
2. If the analysis was run against a **case/matter folder** (a `CLAUDE.md` or case
   documents in `pwd`), write the `.docx` there instead and say so.

Never write the output alongside the source discovery if that discovery lives
outside the project (e.g. a protected-data or discovery directory). Keep the
production where it is and the analysis in the matter folder.

**Filename:**
`defense-analysis.{client}.{case-number}.{YYYY-MM-DD}.docx` — client as surname
or Doe designation, case number as it appears on the report, non-alphanumerics
collapsed to hyphens. Example:
`defense-analysis.webb.20171223-2304-00.2026-08-26.docx`.

**Formatting the Word document.** These are what the bundled renderer produces.
If you render any other way, reproduce them:

- Header block → a plain paragraph block at the top (not a Word header), single
  spaced, above the title, and it **must** carry the work-product legend.
- Best-issue flag(s) → an indented, bordered or shaded single-line paragraph,
  bold lead-in, visually distinct from body text.
- Element tables → real Word tables with a header row, five columns
  (`#` / Element / State's proof / Strength / Defense attack), header row bold
  and repeating across pages. Never flatten a table into a list.
- Strength verdicts, bullet labels, and the two or three facts the case turns on
  → bold. Cites and recommendations → italic.
- Bottom-line table → a real three-column Word table.
- Action items → a numbered or bulleted list, grouped by deadline urgency.
- Closing verification and privilege block → set apart at the end, smaller or
  boxed, so it reads as a notice rather than analysis.
- Portrait, US Letter, 1" margins, a serif body face at 11–12 pt. Footer carries
  the work-product legend and page numbers.

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

There should be one table per charge (plus any acting-in-concert block) and the
bottom-line table.

**Then, in chat:**

- Give the file path and a three-or-four-line orientation — the best issue, the
  weakest element in the State's case, and the motions that follow. Do **not**
  paste the whole analysis back into chat; the document is the deliverable.
- Offer the official SOG PDF links for every instruction cited (look up
  `source_url` in `$JI_DIR/catalog.json`).
- Offer the markdown working draft as a separate file only if the user asks for
  it.
- Close with the privilege and review notice: the analysis is attorney work
  product prepared with AI assistance for counsel's review, not a filing and not
  advice to the client.
- If the user wants the long-form reasoning behind any verdict, give it in chat.
  It does not go back into the document.

## Guardrails

- **Work product, not a filing.** The document is privileged and internal. It is
  never served, filed, or handed to the client, and it never contains language
  drafted to be lifted directly into a public filing without counsel's review.
  Every page carries the work-product legend.
- **No advice to the client, ever.** This skill analyzes a case for a lawyer.
  Whether to plead, whether to testify, and what to tell the client are counsel's
  decisions and are never stated as recommendations to a defendant. If the user
  appears to be a defendant rather than counsel, say plainly that this is an
  attorney work-product tool, that it is not legal advice, and that they should
  speak with their lawyer or the public defender's office.
- **No fabricated facts or fabricated defenses.** A defense is analyzed only if
  the record supports it. Never construct a version of events, never suggest what
  a client or witness could say, never propose testimony, and never recommend
  anything that would touch the content of a witness's account. RPC 3.3, 3.4 and
  1.2(d) are hard limits — not drafting preferences.
- **No outcome predictions.** The bottom line assesses the strength of the
  State's proof and names the motions and issues available. It never says the
  client "will be acquitted," that a charge "will be dismissed," or that a motion
  "will be granted." Sufficiency and leverage language only.
- **Never soften the bad facts.** A defense memo that hides the State's strongest
  evidence is worse than useless — counsel walks into the negotiation blind. The
  STRONG verdicts and the client's own inculpatory statements go on the page in
  full.
- **Quotes are verbatim.** Trim with ellipses; never adjust wording, never
  attribute a quote to the wrong narrative. These quotes may end up in a
  suppression motion or a cross-examination; a misquoted report is worse than no
  quote.
- **Verify everything outside the local libraries.** Chapter 15A procedure,
  Chapter 90 drug offenses, constitutional standards, and every case citation are
  outside the shipped statute and instruction libraries. Flag each as *(verify)*
  and never state a case holding from memory. Recommend confirmation against
  current authority before any of it reaches a filing.
- **Confidentiality.** Discovery contains victim and witness information and is
  routinely subject to protective orders — in North Carolina, materials produced
  under G.S. 15A-903 frequently are. Keep every output — the `.docx` and any
  working draft — on the local filesystem, in the project or matter folder per
  Step 9. Never transmit case materials to external services, and never publish
  an analysis as a web artifact.
- **Jurisdiction.** North Carolina criminal law only. Federal work belongs to the
  `federal-criminal-law` plugin's skills, not this one.
- **Currency.** Pattern instructions and scraped statutes may lag amendments;
  recommend verification against current G.S. and appellate authority for
  anything dispositive.

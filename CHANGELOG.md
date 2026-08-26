# Changelog

All notable changes to the **north-carolina-criminal-law** plugin are documented here.
Versions follow `YY.MM.DD.patch` date-based format.

---

## [26.08.26.03] — 2026-08-26

### Added

- **`skills/defense-analysis`** — New skill, the defense-side mirror of `prosecutors-analysis`. Generates a **defense case analysis** from a North Carolina police report, discovery production, or fact pattern: a seven-section report (Summary → Charge Analysis → Weaknesses in the State's Case → Defenses → Identification → Bottom Line → Action Items) with per-charge element tables rating the State's proof **STRONG / CONTESTED / WEAK / NO PROOF** and pairing each element with a concrete defense attack. Element language is loaded from the sibling `north-carolina-pattern-jury-instructions` skill and statute text from `north-carolina-general-statutes` — never stated from memory. Defense-side; NC criminal only. Output is a privileged `.docx` work-product draft for defense counsel — never a filing, never advice to the client, and never a prediction of outcome.

  Design differences from the prosecution skill, all deliberate:

  - **Mandatory client identification.** The skill will not analyze until it knows whose lawyer the reader is. It resolves this from the request, then a matter folder, then a single named defendant — and otherwise **asks**, building one option per candidate from the record. Where names are redacted it describes candidates by their role in the allegation ("the alleged shooter (Doe 1)" / "the alleged driver (Doe 2)") so counsel can recognize their own client. Every element verdict, weakness, and defense is then scoped to that client, and the verification pass scans for places a codefendant's conduct or a collective noun ("the suspects," "they") has been silently attributed to them.
  - **Multi-defendant handling.** Acting in concert (*N.C.P.I.—Crim. 202.10*) gets its own element block rather than being buried in the substantive table — in a joint case it is frequently the whole case. Codefendant statements raise flagged *Bruton* and severance issues, antagonistic defenses are named with what they cost, and an RPC 1.7 conflict is surfaced in the header flag.
  - **Attribution as a drafting rule.** Every assertion is attributed to whose account it comes from — the report is the State's version, not the facts. Conclusory report language ("serious injury," "confessed," "consented," "resisted") is rendered as the report's characterization, with a note on what fact, if any, supports it.
  - **Weaknesses is exempt from the length budget.** The prosecution skill caps its weaknesses at roughly six bullets because a charging screen that goes unread has failed. Here, under-inclusion is the failure that matters — a weakness left off the page is one that never gets litigated. The section is organized under labeled sub-headings and every bullet ends in a **Use:** (cross, suppress, dismiss, demand in discovery, retain an expert, request an instruction).
  - **Section 7, Action Items** — discovery demands, motions with their timing hooks, preservation letters, and investigation tasks, grouped by urgency. New relative to the prosecution template.
  - **Evidentiary and cautionary instructions as leverage** — *104.90*, *104.98*, *104.20*, *104.25*, *104.30*, *104.05*, *104.41*, *105.20*, *105.21*, *101.10*, *101.30*, *101.42* — mapped to the weaknesses that earn them, including the ones the State will request **against** the client (*104.35* flight, *104.40* recent possession, *105.21* conflicting statements).

- **`skills/defense-analysis/reference/`** — `analysis-template.md` (seven-section structure, budgets, formatting), `example-output.md` (a worked two-charge analysis built on the *same fictional case* as the `prosecutors-analysis` example, so the two can be read side by side), `weakness-checklists.md` (cross-cutting sweeps for witness credibility, investigative gaps, forensics, identification, contradictions, suppression exposure, and charging defects, plus charge-specific checklists), and `defenses-catalog.md` (every Part III defense mapped to its instruction number, the facts that trigger it, and who carries the burden).

- **`skills/defense-analysis/scripts/analysis_to_docx.py`** — Bundled renderer for the delivered `.docx`: five-column element tables and three-column bottom-line tables as real Word tables with repeating header rows, shaded best-issue call-outs, bordered header/notice blocks, numbered action-item lists, inline bold/italic/code runs, US Letter with 1" margins, and the **ATTORNEY WORK PRODUCT — PRIVILEGED** legend plus page numbers in the footer. Requires `python-docx`.

### Changed

- **`plugin.json`** — Description now covers the defense analysis alongside forms, jury instructions, statutes, and the prosecutorial summary. The plugin bundles five skills.

- **`README.md`** — Documents `defense-analysis`: intro bullet, repository tree, manual-install symlink loop, `python-docx` requirement, and a usage section covering the client-identification step and the work-product boundary.

### Notes

- **Burden allocation is read from the loaded instruction, never from memory.** North Carolina splits these — self-defense (*308.45*), accident (*307.11*), and alibi (*301.10*) put nothing on the defendant, while duress (*310.10*), necessity (*310.12*), entrapment (*309.10*), and insanity (*304.10*) require proof to the jury's satisfaction. `defenses-catalog.md` records the split as a routing aid and states explicitly that the instruction's own mandate paragraph governs.

- **Authority outside the shipped libraries is flagged, not asserted.** This plugin ships G.S. Chapter 14 and the N.C.P.I.—Crim. instructions. Chapter 15A procedure (discovery, suppression, severance, EIRA), Chapter 90, Chapter 20, the Rules of Evidence, and all case law are not shipped — every such cite in the skill and its references carries a `(verify)` flag, and the guardrails forbid stating a case holding from memory.

---

## [26.08.26.02] — 2026-08-26

### Fixed

- **`README.md` — manual install was broken as documented.** Option B told users to symlink each skill's `SKILL.md` alone into `~/.claude/skills/<name>.md`. Every skill in this plugin reads sibling files next to its `SKILL.md` (`catalog.json`, `reference/`, `statutes/`, `scripts/`), so that install produced skills that could not find their own data. Option B now links the whole skill **directory** (`ln -sfn .../skills/<name> ~/.claude/skills/<name>`), and says why.

- **`README.md` — manual install silently lost form filling.** The MCP server is declared in `plugin.json` and registered only by the plugin manager, so a manual install leaves `nc-aoc-cr-forms` unable to fill anything. Option A is now marked the supported install, and Option B carries an explicit call-out that form filling requires it. Documented the `python-docx` prerequisite for `prosecutors-analysis` in the same section.

- **`README.md` — removed the "Command-line usage" section.** It documented `python3 skills/nc-aoc-cr-forms/fill_form.py …`, a script that stopped shipping in v26.07.23.01 (moved to gitignored `dev/local-fill/`) and a local fill path the skill's own guardrails have forbidden since v26.07.23.04. The still-accurate checkbox value list moved to the MCP server section, alongside a statement that `fill_nc_aoc_form` is the only supported fill path.

- **`README.md` — repository tree corrected.** Dropped `skills/nc-aoc-cr-forms/pdfs/` (blank PDFs have not been downloaded to the client since the fill moved to Lambda) and the stale `.claude-plugin/marketplace.json` entry (removed in ac01e90); added `CHANGELOG.md` and `.gitignore`, and a note on where the gitignored `dev/` tooling lives.

---

## [26.08.26.01] — 2026-08-26

### Added

- **`skills/prosecutors-analysis`** — New skill. Generates a North Carolina **prosecutorial summary** (probable-cause screening) from a police report or fact pattern: a six-section report (Summary → Charge Analysis → Weaknesses → Defenses → Identification → Bottom Line) with per-charge element tables, proof carried as attributed verbatim quotes from the report, and a bottom-line charging recommendation. Element language is loaded from the sibling `north-carolina-pattern-jury-instructions` skill and statute text from `north-carolina-general-statutes` — never stated from memory. Implements the methodology and evaluator findings from *Ethically Implementing Generative Artificial Intelligence in Prosecution* (Cuffney, Northwestern University, 2025), including a mandatory verification pass (fact-tracing, chronology completeness, discrepancy sweep, element-language diff, charge-specific checklists, and a length/redundancy gate). Prosecution-side; NC criminal only. Output is a `.docx` draft for prosecutor review — never a charging decision (N.C. RPC 3.8, ABA Standard 3-4.3).

- **`skills/prosecutors-analysis/scripts/summary_to_docx.py`** — Bundled renderer that converts the markdown working draft into the delivered `.docx`: real Word tables (with repeating header rows) for element and bottom-line tables, shaded case-critical call-outs, bordered header/notice blocks, inline bold/italic/code runs, US Letter with 1" margins and footer page numbers. Requires `python-docx`.

- **`skills/prosecutors-analysis/reference/`** — `summary-template.md` (section structure and word budgets), `example-output.md` (worked two-charge summary at target length), and `issue-checklists.md` (cross-cutting and charge-specific checklists distilled from the thesis's ten CMPD case studies).

### Changed

- **`plugin.json`** — Description now covers the prosecutorial summary alongside forms, jury instructions, and statutes. The plugin bundles four skills.

---

## [26.07.23.04] — 2026-07-23

### Changed

- **`nc-aoc-cr-forms` skill** — The cloud-session check (`CLAUDE_CODE_SKIP_PLUGIN_MCP_SERVERS`) is now **Step 0**, run before any tool lookup, with a hard stop: in a cloud session the skill must deliver the "re-run in a local session" message immediately, without probing S3, websites, or searching for the tool. (A v...03 cloud run correctly diagnosed the environment but first spent commands trying to fetch the blank form — only the sandbox's egress block stopped it.)

- **`nc-aoc-cr-forms` skill** — The no-fallback rule is now source- and method-agnostic: no fetching the blank PDF from ANY source (S3, nccourts.gov, anywhere), no inspecting field layouts for a manual fill, no filling/overlaying/reconstructing by any means. The blank form being publicly available does not make a hand-fill acceptable — the ONLY fill path is the `fill_nc_aoc_form` MCP tool.

---

## [26.07.23.03] — 2026-07-23

### Changed

- **`nc-aoc-cr-forms` skill** — The connection check now distinguishes *why* the `fill_nc_aoc_form` tool is unavailable. If `CLAUDE_CODE_SKIP_PLUGIN_MCP_SERVERS=1` is set, the session is a cloud/remote sandbox where the platform disables plugin MCP servers (and blocks outbound network) — the skill now tells the user to re-run in a local session instead of the (useless there) plugin toggle advice. Genuine disconnections keep the toggle-and-retry message.

### Fixed

- **`agents/nc-form-filler`** — The agent's tool allowlist only named `mcp__nc-aoc-cr-forms__fill_nc_aoc_form`, but when installed as a plugin the tool is prefixed (`mcp__plugin_north-carolina-criminal-law_nc-aoc-cr-forms__fill_nc_aoc_form`), so the subagent could never call the fill tool. Both names are now allowlisted, plus `ToolSearch` for harnesses that defer MCP tool schemas; the agent body explains which name to use.

---

## [26.07.23.02] — 2026-07-23

### Fixed

- **`nc-aoc-cr-forms` skill** — The v26.07.23.01 availability check produced false "server isn't connected" errors in harnesses where MCP tools are **deferred** (connected but absent from the loaded tool list until a `ToolSearch` call fetches the schema). The check is now: look for `fill_nc_aoc_form` among loaded tools (name may be prefixed) → if absent, `ToolSearch` for it (this also waits out a still-connecting server) → only if both come up empty is the server considered down.

---

## [26.07.23.01] — 2026-07-23

### Changed

- **`nc-aoc-cr-forms` skill** — If the `fill_nc_aoc_form` MCP tool is unavailable, the skill now stops and tells the user to reconnect the plugin — no fallbacks (no S3 downloads, no local fill scripts, no hand-built forms). Sandboxed sessions block outbound network, and a hand-rolled court form is worse than none.

### Removed

- Dev leftovers from the shipped `nc-aoc-cr-forms` skill: `fill_form.py` and `requirements.txt` moved to gitignored `dev/local-fill/`; deleted `__pycache__/`, `pdfs/`, and `.DS_Store`.

---

## [26.06.10.02] — 2026-06-10

### Added

- **`skills/north-carolina-general-statutes`** — New skill providing full-text access to all sections of G.S. Chapter 14 (Criminal Law). Ships ~978 statute sections as pre-built markdown files (one per section), with no internet required at runtime. Supports lookup by citation (G.S. 14-N), keyword search, article browsing, plain-language explanation, and cross-referencing to N.C.P.I. instructions via the existing `by_statute.json` index. Reserved and renumbered placeholder sections are excluded. Source: ncleg.gov published HTML, scraped via `dev/maintenance/build_chapter14_statutes.py`.

- **`dev/maintenance/build_chapter14_statutes.py`** — Developer build script that scrapes Chapter 14 from ncleg.gov and produces the statute markdown library and all four index files (`catalog.json`, `by_article.json`, `by_keyword.json`, `index.md`). Supports `--execute`, `--resume` (skip already-written files), `--patch-metadata` (fix frontmatter without re-scraping), `--indexes-only`, and `--section N` (single-section test mode). Requires `requests` and `beautifulsoup4`.

---

## [26.06.10.01] — 2026-06-10

### Added

- **`agents/case-file-harvester`** — Autonomous agent that scans the active case folder (working directory), reads all case documents (intake sheets, prior AOC forms, indictments, case JSON files, etc.), and returns a compact JSON payload of extracted case facts with per-field source citations. Spawned at startup by both skills in place of inline document loading, keeping raw file content out of the parent skill's context. Returns structured fields: case number, county, defendant, charges, attorney, judge.

- **`agents/offense-elements-analyzer`** — Autonomous agent that performs element-by-element analysis of a single NC Pattern Jury Instruction charge against a provided fact pattern. Returns a verbatim-element table with Supported / Contested / Not supported / Needs information status for each element, overall charge viability, weakest elements, lesser included offenses, fact gaps, and an optional prosecution/defense perspective note. Spawned in parallel by the jury instructions skill — one agent per candidate charge — when N > 1 charges are identified in a facts analysis.

- **`agents/nc-form-filler`** — Autonomous agent that fills a single AOC-CR form given a complete, pre-confirmed field values dict. Calls the `fill_nc_aoc_form` MCP tool, decodes the returned base64 PDF, and writes the output to the case folder using the `[CaseNo]-[FormNo].pdf` naming convention (with `-v2`, `-v3` versioning for collisions). Spawned in parallel by the forms skill — one agent per form — for multi-form workflows.

### Changed

- **`nc-aoc-cr-forms` skill (Phase 0.5)** — Inline case folder scan replaced with a `case-file-harvester` agent spawn. The agent returns structured JSON; the parent skill presents harvested values to the user for confirmation before filling. Raw document text no longer loads into the skill's context.

- **`nc-aoc-cr-forms` skill** — New "When multiple forms are needed (parallel filling)" section added. Describes the modified Phase 2–4 flow for common multi-form workflows: load all forms' fields upfront, gather all values in a single consolidated conversation, then spawn parallel `nc-form-filler` agents. Supported workflows: DWI sentencing (310[A–F] + 311 + 338), plea packages, probation violations (448 + 449/450), and explicit multi-form user requests.

- **`north-carolina-pattern-jury-instructions` skill (facts-to-elements playbook)** — Added Step 0 conditional case harvest (spawns `case-file-harvester` when case files are present in the working directory). After Step 1 charge identification, N > 1 candidates now spawn parallel `offense-elements-analyzer` agents and aggregate results into a unified multi-charge report with cross-charge comparison; N = 1 continues inline as before.

---

## [26.06.10.00] — 2026-06-10

### Changed

- Moved dev tooling (MCP server, maintenance scripts) to `dev/` directory.
- Adopted `YY.MM.DD.patch` date-based versioning across plugin manifest and skill files.

---

## [26.06.09.00] — 2026-06-09

### Added

- Date-based versioning (`26.06.09.00`) adopted across plugin.json, marketplace.json, and both SKILL.md files.

---

## [v0.7.0]

### Added

- AWS Lambda MCP server (`fill_nc_aoc_form` tool) — moves S3 fetch and PDF fill server-side; no client network access or Python dependencies required.
- Security hardening: path traversal prevention, CORS locked to `https://claude.ai`, IAM scoped to forms S3 prefix.
- `fields_index.json` bundled with both skill and Lambda for offline field lookup.

---

## [v0.2.0]

### Changed

- Removed S3 dependency from jury instructions skill; instructions now ship pre-built as markdown files under `reference/instructions/` (1,100+ files).

---

## [v0.1.0]

- Initial release: `nc-aoc-cr-forms` and `north-carolina-pattern-jury-instructions` skills.

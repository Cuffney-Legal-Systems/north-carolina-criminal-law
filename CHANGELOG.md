# Changelog

All notable changes to the **north-carolina-criminal-law** plugin are documented here.
Versions follow `YY.MM.DD.patch` date-based format.

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

# Changelog

All notable changes to the **north-carolina-criminal-law** plugin are documented here.
Versions follow `YY.MM.DD.patch` date-based format.

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

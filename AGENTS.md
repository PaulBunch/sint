<!--
SPDX-FileCopyrightText: 2026 sint project contributors

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# AGENTS.md — sint

## Project
sint is a physical interface project that enables an LLM to design, assemble, test and iteratively improve physical systems (including the interface itself).
Core principles: Design for Autonomous Assembly (DFAA), modularity, bootstrapping, 100% consumer-grade components.
Canonical language for code, docs and commits: English.
See `docs/spec.md` and `docs/long-term-memory.md`.

## Critical Documents (read first)
- `docs/current-state.md` — Single Source of Truth for system hardware/software status (always read at start)
- `docs/handoff-latest.md` or latest in `docs/handoffs/` — Actionable bridge from previous session (what was just done, next steps, warnings)
- `docs/spec.md` — Project specification & goals
- `docs/long-term-memory.md` — Memory principles & operational guidelines
- `docs/ROADMAP.md` — High-level phased plan. Read to understand current phase and major priorities. Update when a phase is completed or priorities shift significantly.
- Relevant ADR in `docs/decisions/`

*Bootstrapping Rule (Missing Critical Documents):*
If `current-state.md` or `handoff-latest.md` do not exist (e.g., initial repository setup):
1. Create `docs/` structure if missing.
2. Bootstrap `docs/current-state.md` with base hardware/software state derived from `docs/spec.md`.
3. Create `docs/handoff-latest.md` stating `Initial project setup complete. Ready for Step 1`. Do not fail execution.

*Note on Missing Files:* If `docs/current-state.md` or `docs/handoff-latest.md` do not exist yet (e.g. during project bootstrapping):
1. Do not fail or stop.
2. Initialize `docs/` structure if missing.
3. Create default initial versions of `docs/current-state.md` and `docs/handoff-latest.md` based on `docs/spec.md` and available project files.

## Layout
- `docs/` — all project knowledge, decisions, conversations, handoffs
- `docs/conversations/` — raw multi-LLM discussion archive
- `docs/decisions/` — Architecture Decision Records (ADR)
- `docs/tasks/` — atomic checklists / work packages that break down ROADMAP items
- `hardware/` — CAD, mechanical designs
- `firmware/` — embedded code (future)
- `software/` — higher-level control, simulation, tools (future)

## Naming
- Documentation and conversation files use kebab-case (e.g. `long-term-memory.md`, `current-state.md`).

## Licensing (SPDX / REUSE)
- When creating **new** documentation, code, or configuration files, add SPDX headers:
  ```
  SPDX-FileCopyrightText: 2026 sint project contributors
  SPDX-License-Identifier: <appropriate-license>
  ```
- Typical licenses:
  - Documentation (`.md`): `CC-BY-SA-4.0`
  - Software / scripts: `AGPL-3.0-or-later`
  - Hardware designs: `CERN-OHL-S-2.0`
- If the `reuse` tool is available in the environment, prefer using it:
  - `reuse annotate --copyright="sint project contributors" --license="CC-BY-SA-4.0" <file>`
  - `reuse lint` to check compliance
- Do not spend significant time retroactively annotating old conversation files unless explicitly asked.

## Documentation & Memory Rules
- Canonical documents (`spec.md`, ADR, current-state, etc.) → English
- Conversation files in `docs/conversations/` may be in Russian
- After significant work: update `docs/current-state.md`
- At the end of a session: write/update handoff (`docs/handoff-latest.md` or dated file)
- Never leave important decisions only in chat — promote them to ADR or spec

## Conversation Files
- One topic ≈ one file: `docs/conversations/YYYY-MM-DD--short-topic.md`
- Use YAML frontmatter (`status: open | closed`, etc.)
- Date separator once per day: `---\n*YYYY-MM-DD*\n---`
- Message separator: `---\n**Author**\n`
- Avoid nested triple-backtick code blocks (use indented blocks or 4+ backticks)

## Safety & Constraints
- 100% consumer-available components only
- Never commit secrets, credentials, private keys or `.env`
- Do not run destructive commands without explicit confirmation
- Do not invent hardware interfaces or protocols — check existing docs/CAD first

## Workflow
1. Read `current-state.md` + latest handoff + relevant ADR/spec + current phase of `docs/ROADMAP.md` before making changes
2. Prefer small, reviewable changes
3. After documentation changes — keep structure and frontmatter consistent
4. When a discussion reaches a decision → create/update ADR and close the conversation file
5. When working on a ROADMAP item that has a linked task file — read and update that checklist
6. When working on hardware geometry:
  1. Read docs/build123d-guidelines.md
  2. Follow the pure-script rules (no ocp_vscode inside models)
  3. Lifecycle for every part/assembly: generate → run scripts/cad-export.py → export STEP → inspect/measure → fix

## Agent Notes & Transparency
- Agents may keep working notes in `docs/agent-notes/`.
- All notes must be human-readable (English or Russian).
- Deliberately opaque, encrypted, or steganographic records are not allowed.
- Important conclusions must eventually be promoted to current-state.md, ADR, or handoff documents.

## Tooling preferences
- Search: `rg`
- File discovery: `fd` if available

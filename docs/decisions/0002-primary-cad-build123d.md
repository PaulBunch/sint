<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# ADR-0002: Primary CAD Tool — build123d

- **Status:** Accepted
- **Date:** 2026-09-13
- **Deciders:** Project maintainers / agents working on Phase 1
- **Refines:** [ADR-0001: CAD Tooling Strategy for LLM-Autonomous Design](0001-cad-tooling-and-llm-interaction.md)
- **Related:** `docs/tasks/0001-select-cad-software.md`, `docs/tasks/0002-test-llm-cad-infrastructure.md`, `docs/build123d-guidelines.md`, `docs/conversations/2026-09-13--test-llm-cad-infrastructure.md`

## Context

ADR-0001 locked the overall CAD strategy for sint:

- Code-CAD (script-driven geometry)
- Mandatory headless execution
- STEP (B-rep) as canonical geometry exchange format
- Preference for OpenCASCADE-based open-source tools

It deferred the concrete primary tool among CadQuery, build123d, FreeCAD (Python), and llmcad pending evaluation.

Since then we completed:

1. Documentary comparison of candidates (task 0001, section B)
2. Practical LLM + infrastructure tests S1–S3 (task 0002): parametric plate, joint-like module, mini-assembly
3. Project tooling: `scripts/cad-export.py`, `scripts/cad-show.py`, `docs/build123d-guidelines.md`, local venv workflow

## Decision

1. **Primary CAD library: build123d**  
   All new mechanical design scripts for sint shall be written in build123d unless there is a documented exception.

2. **Fallback: CadQuery**  
   CadQuery remains acceptable for legacy snippets, interoperability experiments, or cases where an existing CadQuery example is the fastest path. Both share the OCP/OpenCASCADE foundation; geometry can be exchanged via `.wrapped` when needed.

3. **Excluded as primary / default**
   - **llmcad** — insufficient open governance / repository availability for a long-lived project dependency
   - **OpenSCAD** — mesh/CSG kernel; does not meet STEP-as-SoT requirement for engineering parts
   - **FreeCAD GUI** — not LLM-autonomous as primary authoring path
   - **Replicad** — interesting for web/WASM, not selected as main engineering stack

4. **FreeCAD role**  
   FreeCAD remains a **secondary** tool (human inspection, FEM workbench, occasional interoperability), not the primary Code-CAD authoring environment.

5. **Operational rules** (already validated)
   - Pure model scripts only (no viewer imports inside `hardware/**/*.py`)
   - Headless path preferred for agents: `scripts/cad-export.py` → STEP
   - Agent authoring rules live in `docs/build123d-guidelines.md`
   - Co-locate script and exported STEP under `hardware/` (or agreed subfolders)

## Options Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| build123d | **Selected as primary** | Modern Python API (context managers), same OCCT/OCP stack, good LLM edit/debug loop in S1–S3, active development, clear evolution from CadQuery fluent style |
| CadQuery | Fallback | Mature, excellent ecosystem, still actively maintained; fluent API less convenient for complex control flow and IDE-oriented agent edits |
| FreeCAD (Python/headless) | Secondary only | Strong FEM and human GUI; weaker as default LLM Code-CAD surface |
| llmcad | Rejected | Attractive minimal API, but open-source longevity/governance not acceptable |
| Replicad | Not primary | Browser/WASM niche; smaller engineering footprint for sint |
| OpenSCAD | Rejected as primary | Not true B-rep / STEP-centric |

## Consequences

### Positive
- Single default authoring language for agents and humans
- Validated generate → export STEP → inspect → fix loop (S1–S3 completed in 2–3 LLM iterations typical)
- Guidelines capture real failure modes (`_` prefix for intermediates, avoid duplicate globals, prefer `Plane` before fillet)

### Negative / Risks
- build123d API still evolving toward 1.0; occasional breaking changes possible → pin versions in `requirements-cad.txt` and re-test after upgrades
- Smaller long-tail example corpus than CadQuery → mitigate via project cheatsheet and guidelines
- Team members familiar only with CadQuery need a short ramp-up (shared OCP knowledge helps)

### Neutral
- CadQuery knowledge remains useful; not discarded
- Downstream FEM/PCB/sim integration still via STEP (unchanged from ADR-0001)

## Implementation Notes

- Treat `docs/build123d-guidelines.md` as the living authoring contract for agents
- Keep `scripts/cad-export.py` as the canonical headless entry point
- Update ROADMAP / current-state: CAD tool selection is complete
- Optional follow-up: pin exact build123d/OCP versions; add minimal CI job running `cad-export` on sample scripts

## References

- ADR-0001 — strategy (Code-CAD, headless, STEP)
- Task 0001 — candidate research and selection process
- Task 0002 — S1–S3 infrastructure validation (closed)
- Conversation 2026-09-13 — test results and guideline refinements

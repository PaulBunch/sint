<!--
SPDX-FileCopyrightText: 2026 sint project contributors

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Project Current State — sint

**Last Updated:** 2026-09-04  
**Status:** Bootstrapping / Specification Phase — Phase 1 (Foundation & Planning)

---

## Recent Progress

- Established comprehensive `README.md` with project overview, core principles, directory structure, autonomous memory architecture summary, etymology, and licensing breakdown.
- Created and populated canonical specification document `docs/spec.md` in English.
- Separated high-level requirements from specific technical solutions:
    - `docs/spec.md` now focuses strictly on requirements and constraints.
    - `docs/implementation-concepts.md` captures candidate technical solutions (BLDC+FOC, gearboxes, docking mechanisms).
- Defined core strategic requirements:
    - **Relocatable Mobility** for expanded reach.
    - **Acoustic Transparency** for diagnostic sensing.
    - **DFAA** (Design for Autonomous Assembly).
    - **100% COTS** and consumer-grade fabrication.
- Established licensing: CERN-OHL-S v2 (Hardware), GNU AGPLv3 (Software), CC-BY-SA-4.0 (Documentation).
- Created `docs/ROADMAP.md` with phased plan (Phase 1–5) including initial steps discussion, CAD/tool selection, research of multiple options per key requirement, and justified selection criteria.
- Integrated `ROADMAP.md` into critical document hierarchy (`AGENTS.md`, `docs/long-term-memory.md`).
- **CAD Strategy (2026-09-06):** Adopted ADR-0001. Decided on Code-CAD (scripting) with mandatory headless execution and STEP as the source of truth for engineering data.
- **CAD Infrastructure Testing (2026-09-13):** Completed S1–S3 (parametric plate, joint module, mini assembly). Key fixes: `_` prefix for intermediate/duplicate variables (prevents `anytree.TreeError`), `Plane` for robust positioning, headless export (`cad-export.py`) preferred over `cad-show.py` due to sandbox limits. Guidelines updated (`docs/build123d-guidelines.md`). Test artifacts (`hardware/s1_*`, `s2_*`, `s3_*`) removed after validation.
- Added conversation record (`docs/conversations/2026-09-04--roadmap.md`) on ROADMAP integration and simulation tool evaluation (MuJoCo vs Isaac Sim).
- Added conversation record (`docs/conversations/2026-09-06--CAD-selection.md`) and ADR-0001 regarding CAD tooling.

---

## Active Specification & Focus

1. **`docs/spec.md`**: Completed initial draft capturing core vision, design principles, high-level requirements table, non-goals, open questions, and early success criteria.
2. **CAD Selection & Testing (Phase 1)**: ADR-0001 accepted; primary CAD = build123d (ADR-0002). Tool-chain (`build123d` + headless `cad-export.py` + `STEP` as SoT) fully validated (S1–S3). Task 0001 (`docs/tasks/0001-select-cad-software.md`) closed (C4, C5, F1–F4 completed). `docs/build123d-guidelines.md` updated.
3. **Next Steps (Phase 1 — Foundation & Planning)**:
   - Define core numerical characteristics (envelope dimensions, payload, power budget, torque/speed targets, acoustic limits, BOM cost).
   - Develop kinematic and mechanical scheme (topology, DoF, relocatable base).
   - Define COTS component composition (motors, drivers, sensors, compute, connectors).
   - Compile preliminary assembly operations and required external tools (constrains DFAA).
   - Determine minimum mandatory end-effectors and workspace/docking grid concept.
   - Evaluate simulation tools (MuJoCo / Isaac Sim) for kinematic validation.
   - Conduct research and make justified selection of primary options for key requirements; formalize ADRs.
   - Refine roadmap based on outcomes.

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
- **CAD Infrastructure Testing (2026-09-13):**
  - Completed Test S1 (Parametric Plate: `hardware/s1_parametric_plate.py`).
  - Completed Test S2 (Joint Module: `hardware/s2_joint_module.py`).
  - Completed Test S3 (Mini Assembly: `hardware/s3_mini_assembly.py`).
  - Successfully exported all tests to STEP and STL using `scripts/cad-export.py` in headless mode.
  - Resolved namespace pollution and `anytree.TreeError` issues by standardizing `_` prefix for intermediate or duplicated CAD variables.
  - Refined CAD guidelines to prefer `Plane` over complex face selectors for robustness, and clarified duplicate CAD variable avoidance.
  - Documented sandbox visualizer limits and venv execution guidelines in `docs/build123d-guidelines.md`.
- Added conversation record (`docs/conversations/2026-09-04--roadmap.md`) on ROADMAP integration and simulation tool evaluation (MuJoCo vs Isaac Sim).
- Added conversation record (`docs/conversations/2026-09-06--CAD-selection.md`) and ADR-0001 regarding CAD tooling.

---

## Active Specification & Focus

1. **`docs/spec.md`**: Completed initial draft capturing core vision, design principles, high-level requirements table, non-goals, open questions, and early success criteria.
2. **CAD Selection & Testing (Phase 1)**: ADR-0001 accepted. S1, S2, and S3 tests completed successfully. Infrastructure is fully validated and ready for regular CAD design.
3. **Next Steps (Phase 1 — Foundation & Planning)**:
   - Complete comparative evaluation of CAD tools and finalize primary selection.
   - Define core numerical characteristics (envelope, payload, power budget, torque/speed targets, acoustic limits, BOM cost).
   - Conduct research to identify multiple solution options for each key requirement (kinematics, docking, EE interface, sensors).
   - Make justified selection of the primary option for each key requirement and formalize ADRs.
   - Evaluate simulation tools (MuJoCo / Isaac Sim) for kinematic validation and controller testing.
   - Compile preliminary assembly operations and required external tools list (directly constrains DFAA design).
   - Refine roadmap based on research outcomes.

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
- Added conversation record (`docs/conversations/2026-09-04--roadmap.md`) on ROADMAP integration and simulation tool evaluation (MuJoCo vs Isaac Sim).

---

## Active Specification & Focus

1. **`docs/spec.md`**: Completed initial draft capturing core vision, design principles, high-level requirements table, non-goals, open questions, and early success criteria.
2. **Next Steps (Phase 1 — Foundation & Planning)**:
   - Select CAD software and other tools enabling autonomous LLM interaction with minimal human assistance.
   - Define core numerical characteristics (envelope, payload, power budget, torque/speed targets, acoustic limits, BOM cost).
   - Conduct research to identify multiple solution options for each key requirement (kinematics, docking, EE interface, sensors).
   - Make justified selection of the primary option for each key requirement and formalize ADRs.
   - Evaluate simulation tools (MuJoCo / Isaac Sim) for kinematic validation and controller testing.
   - Compile preliminary assembly operations and required external tools list (directly constrains DFAA design).
   - Refine roadmap based on research outcomes.

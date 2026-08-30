<!--
SPDX-FileCopyrightText: 2026 sint project contributors

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Project Current State — sint

**Last Updated:** 2026-09-03  
**Status:** Bootstrapping / Specification Phase

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
- Established licensing: CERN-OHL-S v2 (Hardware), GNU AGPLv3 (Software).

---

## Active Specification & Focus

1. **`docs/spec.md`**: Completed initial draft capturing core vision, design principles, high-level requirements table, non-goals, open questions, and early success criteria.
2. **Next Steps**:
   - Resolve open engineering trade-offs regarding relocatable docking mechanisms with attached EEs.
   - Begin preliminary design/CAD research for joint module topology using COTS BLDC motors + FOC drivers.

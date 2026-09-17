<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Project Current State — sint

**Last Updated:** 2026-09-17  
**Status:** Phase 1 (Foundation & Planning) — Kinematic Scheme Selection

---

## Recent Progress

- **Kinematic Scheme (Task 0004):**
    - ADR-0005 accepted (2026-09-17). Primary **S2** (serial 6-DoF, cascaded mass bias, asymmetric ends, power scenario A, coplanar ≥2 docks, base aux-latch walk; wrist not sole cantilever). Fallback **S1** (in-joint). **S3** dual-ended deferred (BOM/mass risk). Details: `docs/decisions/0005-kinematic-scheme.md`. Task 0004 closed.
    - Established **Kinematic Constraints (K1)** including DFAA veto rules and ADR-0003 alignment (`docs/tasks/0004-kinematic-constraints.md`).
    - Completed **Analogue Survey (K2)**: Curated source list (PAROL6, GLUON, AR4 MK5, AMBIDEX, Canadarm2/ERA) and extracted takeaways (`docs/tasks/0004-kinematic-survey-scope.md`, `docs/decisions/0004-kinematic-survey-patterns.md`).
    - Defined **Placement Policy (K3)**: Defaulting to cascaded/proximal mass bias for distal axes to minimize inertia; power scenario A/B roles defined (`docs/tasks/0004-placement-policy.md`).
    - Developed **Candidate Schemes (K4)**:
        - **S1**: Serial 6-DoF Modular In-Joint (classic, pods).
        - **S2**: Serial 6-DoF Cascaded Mass Bias (belt-driven distal axes, default policy).
        - **S3**: Symmetric 7-DoF Dual-Ended Walking Manipulator (inchworm logic).
        - Documentation: `docs/tasks/0004-candidate-schemes.md`.
- **Numerical Targets (ADR-0003):** Consensus reached on N1–N7 targets (0.5 kg payload, 0.5–0.8 m reach, <$1000 BOM). Recorded in `docs/spec.md` and `docs/decisions/0003-core-numerical-characteristics.md`.
- **CAD Infrastructure:** ADR-0001/0002 accepted (build123d). Tool-chain validated via S1–S3 tests (parametric plate, joint module, mini assembly). Guidelines updated (`docs/build123d-guidelines.md`).
- **Core Strategy:** Defined requirements for Relocatable Mobility, Acoustic Transparency, and DFAA (Design for Autonomous Assembly) in `docs/spec.md`.
- **Documentation & Management:** Initialized `ROADMAP.md`, `long-term-memory.md`, and atomic task structure in `docs/tasks/`.

---

## Active Specification & Focus

1. **Kinematic Down-selection (Phase 1 — K5/K6):**
   - Conduct scorecard comparison of S1, S2, S3 against K1 constraints (Task K5.1).
   - Perform order-of-magnitude checks (torque vs payload, print segments) (Task K5.2).
   - Select primary scheme and formalize via ADR-0005 (Task K6).
2. **Next Steps (Phase 1):**
   - Define COTS component composition (motors, drivers, sensors) for the selected scheme.
   - Compile preliminary assembly operations and required external tools.
   - Evaluate simulation tools (MuJoCo / Isaac Sim) for kinematic validation using the selected scheme.
   - Refine roadmap based on the chosen mechanical topology.

<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Handoff — 2026-09-17

## Summary of Changes
- **Kinematic Scheme (Task 0004):**
  - **Constraint Definition:** Created `0004-kinematic-constraints.md` with explicit DFAA veto rules (V1–V8).
  - **Survey & Patterns:** Completed review of analogues (PAROL6, GLUON, AR4, AMBIDEX, Canadarm2/ERA). Retained patterns documented in `ADR-0004`.
  - **Placement Policy:** Formulated `0004-placement-policy.md` focusing on proximal mass bias and Scenario A power default.
  - **Candidate Schemes:** Drafted three schemes (S1, S2, S3) in `0004-candidate-schemes.md` covering modular in-joint, cascaded belt-drive, and symmetric dual-ended walking topologies.
- **Documentation:**
  - Updated `docs/current-state.md` to reflect the completion of K1–K4 subtasks of Task 0004.
  - Linked all new task-specific documents into the `docs/tasks/` hierarchy.

## Current Working Tree
- `docs/tasks/0004-kinematic-scheme.md` — Subtasks K1–K4 marked complete.
- `docs/tasks/0004-kinematic-constraints.md`
- `docs/tasks/0004-kinematic-survey-scope.md`
- `docs/tasks/0004-placement-policy.md`
- `docs/tasks/0004-candidate-schemes.md`
- `docs/decisions/0004-kinematic-survey-patterns.md`
- `docs/conversations/2026-09-14--kinematic-scheme.md` — Record of the development process.

## Next Recommended Actions (Phase 1)
1. **Execute Down-selection (K5):**
   - Create `docs/tasks/0004-scheme-downselect.md`.
   - Score S1, S2, and S3 against K1 criteria.
   - Perform order-of-magnitude calculations (torque vs lever arm, print segmentation count).
2. **Formalize Decision (K6):**
   - Draft and accept `ADR-0005` (Kinematic Scheme).
3. **Move to Components (Phase 1):**
   - Based on the selected scheme, start Task 0005: "Define COTS component composition".

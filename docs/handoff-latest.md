<!--
SPDX-FileCopyrightText: 2026 sint project contributors

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Handoff — 2026-09-13

## Summary of Changes
- **CAD Infrastructure Testing (S1, S2 & S3):**
  - **S1 (Parametric Plate):** Script `hardware/s1_parametric_plate.py`, successful export to STEP/STL.
  - **S2 (Joint Module):** Script `hardware/s2_joint_module.py`. Complex elements handled (boss, bolt circle, fillets).
  - **S3 (Mini Assembly):** Script `hardware/s3_mini_assembly.py`. Multi-body `Compound` export verified. Resolved `anytree.TreeError` caused by duplicate global CAD variables.
  - Identified and fixed fragility of face selectors after `fillet()` — adopted recommendation to use `Plane` for positioning.
- **Guidelines & Infrastructure:**
  - Added rules to `docs/build123d-guidelines.md`: use `#!/usr/bin/env python3`, `_` prefix for intermediate variables, and prefer `Plane` over complex selectors.
  - Confirmed use of `/home/bunch/.venv/cad/bin/python` for stable execution.
- **Documentation Updates:**
  - Updated `docs/current-state.md` and checklist `docs/tasks/0002-test-llm-cad-infrastructure.md`.
  - All discussion details in `docs/conversations/2026-09-13--test-llm-cad-infrastructure.md`.

## Current Working Tree
- `hardware/s1_parametric_plate.py`, `.step`, `.stl`
- `hardware/s2_joint_module.py`, `.step`, `.stl`
- `hardware/s3_mini_assembly.py`, `.step`, `.stl`
- `docs/conversations/2026-09-13--test-llm-cad-infrastructure.md`
- `docs/tasks/0002-test-llm-cad-infrastructure.md` — All scenarios (S1, S2, S3) completed.
- `docs/build123d-guidelines.md` — Updated based on test results (duplicate variable avoidance, Plane preference).

## Next Recommended Actions (Phase 1)
1. **Simulation / Validation:** Try importing `s2_joint_module.step` or `s3_mini_assembly.step` into any external viewer or simulator for final geometry verification.
2. **Infrastructure Ready:** The CAD infrastructure (build123d + headless export + pure scripts) is fully validated. Proceed with regular agent CAD design tasks.

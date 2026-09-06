<!--
SPDX-FileCopyrightText: 2026 sint project contributors

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Handoff — 2026-09-07

## Summary of Changes
- **CAD Tooling Strategy:** Adopted ADR-0001 defining Code-CAD and headless execution as mandatory for LLM autonomy.
- **Documentation:**
  - Added `docs/decisions/0001-cad-tooling-and-llm-interaction.md`.
  - Added `docs/conversations/2026-09-06--CAD-selection.md` capturing the discussion on CAD candidates and versioning.
  - Updated `docs/current-state.md` with the new CAD strategy status.
  - (Planned) Update `docs/ROADMAP.md` to reflect partial completion of CAD selection.

## Current Working Tree
- `docs/decisions/0001-cad-tooling-and-llm-interaction.md`: New ADR for CAD strategy.
- `docs/conversations/2026-09-06--CAD-selection.md`: Record of the CAD discussion.
- `docs/current-state.md`: Updated with recent progress on CAD selection.
- `docs/handoff-latest.md`: This file.

## Next Recommended Actions (Phase 1)
1. **CAD Benchmark:** Conduct a small comparative evaluation of OpenCASCADE-based candidates (CadQuery, build123d, FreeCAD Python, llmcad) using 2–3 realistic joint/link examples.
2. **Finalize CAD Selection:** Based on benchmark results, pick the primary tool and update ADR-0001/ROADMAP.
3. **Define Numerical Characteristics:** Set targets for dimensions, payload, power, torque, and BOM cost (< $1000).
4. **Kinematic Research:** Start research on multiple options for kinematics and docking interfaces.
5. **Simulation Setup:** Begin evaluating MuJoCo for the selected CAD output (STEP -> mesh/URDF/MJCF).

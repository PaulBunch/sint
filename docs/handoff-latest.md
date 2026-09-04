<!--
SPDX-FileCopyrightText: 2026 sint project contributors

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Handoff — 2026-09-04

## Summary of Changes
- Created `docs/ROADMAP.md` with phased plan (Phase 1: Foundation & Planning through Phase 5: Recursive Bootstrapping) and iterative refinement notes.
- Updated `AGENTS.md`: added `docs/ROADMAP.md` to Critical Documents and included current phase in workflow.
- Updated `docs/long-term-memory.md`: added `docs/ROADMAP.md` as living high-level plan.
- Added conversation file `docs/conversations/2026-09-04--roadmap.md` (status: closed) covering ROADMAP integration and simulation tool comparison (MuJoCo vs Isaac Sim).
- Updated `docs/current-state.md`: added ROADMAP creation, Phase 1 focus, and refined next steps.

## Current Working Tree
- `docs/ROADMAP.md`: New high-level phased plan.
- `AGENTS.md`: Updated critical docs list and workflow.
- `docs/long-term-memory.md`: Updated hierarchy.
- `docs/current-state.md`: Updated status and Phase 1 next steps.
- `docs/conversations/2026-09-04--roadmap.md`: Closed discussion on roadmap and simulators.

## Next Recommended Actions (Phase 1)
1. Select CAD software and supporting tools that allow LLM autonomous interaction with minimal human help.
2. Define core numerical characteristics (dimensions, payload, power, torque/speed, acoustic noise limits, BOM cost target < $1000).
3. Conduct research on multiple options for key requirements (kinematics, docking, quick-change EE, sensors, motors/drivers).
4. Make justified selection of primary option per requirement; formalize ADRs.
5. Evaluate simulation environment (prefer MuJoCo for contact-rich assembly; consider Isaac Sim later for synthetic vision data).
6. Compile preliminary assembly operations and required external tools list (directly constrains DFAA design).

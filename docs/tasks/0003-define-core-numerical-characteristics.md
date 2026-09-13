<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Task: Define core numerical characteristics

**Status:** open  
**Related:** `docs/spec.md` (§4 constraints, §7 success), `docs/implementation-concepts.md`, `docs/ROADMAP.md` Phase 1  
**Goal:** Agree working target ranges (not final frozen physics) for envelope, payload, power, joint performance, acoustic noise, and BOM cost — enough to drive kinematics and COTS selection.

## Why this exists
Without numbers, later ADRs on motors, links, docks, and DFAA sequences cannot be compared. Spec already sets qualitative bars (COTS, <~$1000 node, quiet motion, ≥6 DoF, relocatable base). This task turns them into measurable targets.

## Scope (in)
- Envelope / reach class of one mobile node
- Payload at wrist **without** end-effector mass
- Electrical power budget (peak / continuous, dock vs battery if relevant)
- Per-joint torque & speed targets (order-of-magnitude)
- Acoustic noise limits during motion (relative to usable audio diagnostics)
- Target BOM cost for a functional base node

## Scope (out)
- Final motor/SKU selection (later)
- Full kinematic synthesis (next ROADMAP item)
- Detailed thermal design
- Exact microphone SNR curves

## Subtasks
- [x] N1. Collect constraints already in `spec.md` / success criteria (BOM <$1000, FDM 200³ mm, quiet motion, consumer power…)
- [x] N2. Propose **envelope / reach** working range (reach class, stowed size, dock spacing hypothesis)
- [x] N3. Propose **payload without EE** (kg) with rationale (assembly tasks: modules, tools, printed parts)
- [x] N4. Propose **power budget** (W continuous / peak; bus voltage hypothesis)
- [x] N5. Propose **joint torque & speed** bands (proximal vs distal if useful)
- [x] N6. Propose **acoustic limit** (e.g. dB(A) at 1 m or qualitative + measurable proxy)
- [x] N7. Confirm **BOM cost** target and what is included/excluded (one node vs full workspace)
- [ ] N8. Write one-page summary table → promote candidates into conversation; freeze “working targets” in current-state or a small ADR when stable

## Done when
- [ ] A single summary table of working targets exists (with units and short rationale)
- [ ] Open risks / “must revisit after first joint prototype” are listed
- [ ] ROADMAP item can be marked progress / done; numbers referenced from current-state

## Method
1. Human or agent fills N1 from existing docs.
2. For N2–N7: research comparable desktop/research arms + COTS BLDC/gimbal reality; prefer ranges over point values.
3. Record debate in `docs/conversations/2026-09-13--core-numerical-characteristics.md`.
4. Do not invent industrial payloads or silent harmonic drives that violate COTS/FDM constraints.

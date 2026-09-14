<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Kinematic scheme — constraint sheet (task 0004 / K1)

**Status:** active input to survey (K2) and scheme selection (K4–K6)  
**Sources:** `docs/spec.md`, `docs/decisions/0003-core-numerical-characteristics.md`  
**Parent task:** `docs/tasks/0004-kinematic-and-mechanical-scheme.md`

This note is the **filter** for analogue survey and candidate topologies.  
It is not a kinematic design and does not freeze joint SKUs or CAD.

---

## K1.1 — Checklist: any acceptable scheme must satisfy

### A. Spec requirements (architecture)

| ID | Requirement | Scheme implication |
|----|-------------|-------------------|
| R1 | Articulated manipulator, **≥ 6 DoF** | Topology provides at least 6 controlled axes suitable for 3D assembly (not planar-only primary) |
| R2 | **Relocatable base** | Scheme includes a credible story: undock → move → dock on **≥ 2** fixed docks without human carrying the base |
| R3 | **Universal quick-change EE** | At least one end has a standardized mechanical + power + data EE interface path |
| R4 | Tactile / force path (High) | Scheme must not preclude wrist/EE F/T or tactile sensing (space, wiring, stiffness) |
| R5 | Vision + audio (Critical) | Places exist for camera and mics; motion concept compatible with usable audio (see R7 / N6) |
| R6 | Speed subordinate to precision, low vibration, quiet, safety | No scheme that only wins on peak speed at expense of N6 / assembly control |
| R7 | **Acoustic transparency** | Joint/transmission concept compatible with “no masking of speech/clicks at 0.5–1 m” |
| R8 | **Onboard** compute, power management, control | Electronics live on the mobile unit, not only in a fixed cabinet |

### B. Spec principles & constraints

| Theme | Rule |
|-------|------|
| **DFAA** | Subsystems designed for agent assembly / disassembly / service with minimal human help |
| **COTS** | No industrial-only / B2B-only parts as default |
| **FDM** | Major structural parts printable on consumer desktop class (~200 mm bed); large structures **segmented** |
| **BOM** | Functional **node < $1000**; integration kit ambition per ADR-0003 |
| **Protocols** | Open/maker-friendly buses (e.g. CAN, USB, Ethernet, I2C) — scheme must allow routing |
| **Non-goals** | Not industrial heavy payload; not humanoid/biped primary; not ISO cobot certification MVP |

### C. ADR-0003 working numbers (must not be violated without explicit ADR change)

| ID | Parameter | Working target |
|----|-----------|----------------|
| N2 | Printable piece | ≤ ~175–180 mm major print |
| N2 | Reach | **0.5–0.8 m** (stretch ≤ 1.0 m) |
| N2 | Docks | **≥ 2**; spacing centres **~0.6–1.2 m** |
| N3 | Payload w/o EE | **0.5 kg** continuous; **~1 kg** peak |
| N4 | Bus / power | **24 V** class; **100–200 W** continuous; peak higher |
| N4 | Power default | **Scenario A** (dock work + optional transit battery); **B** alternate |
| N5 | Torque | Proximal **~10–25 N·m**; distal **~1–5 N·m** continuous (order) |
| N5 | Speed | Large axes **~30–90 °/s**; wrist **~60–180 °/s** |
| N6 | Acoustic | Primary: no masking speech/click @ **0.5–1 m** |
| N7 | BOM | Node **< $1000**; kit target ≤ $1000 (stretch documented) |

### D. Workspace story (MVP)

Scheme must be plausible for a **single cluster**:
- Bambu Lab **A1 mini**-class printer service (filament, start/monitor, part removal)
- Table buffer + **tool bay** for assembly of the next revision
- Locomotion between **≥ 2 docks** covering that cluster

### E. Success milestones the scheme must enable (not implement yet)

- Base relocation demo (Dock A → Dock B + power/data)
- Autonomous EE swap path
- DFAA demo on at least one major module (joint or dock)
- Quiet enough motion for audio diagnostics during movement

---

## K1.2 — DFAA veto rules (scheme is unacceptable if…)

A candidate topology / mechanical concept is **rejected** if any of the following hold.

### Veto V1 — Agent cannot service the module
- Critical joint, transmission, or dock latch requires human-only fixtures, calibration jigs, or factory tooling as the **normal** service path.
- Fasteners or connectors are unreachable without destroying structure or removing the entire arm as one welded-like assembly.

### Veto V2 — Non-modular “one-shot” structure
- Primary load path is a single non-segmentable custom structure larger than the printable envelope with no DFAA join plan.
- Failure of one actuator requires scrap of multiple unrelated subsystems (no replaceable joint / drive module boundary).

### Veto V3 — Hidden or non-procurable dependency
- Default design assumes industrial-only reducers, proprietary sealed actuators, or B2B-only docks with no consumer-procurable path.
- Scheme only works with a part that cannot be bought on open marketplaces or printed/substituted under COTS rules.

### Veto V4 — Relocatable base is theatre
- “Mobile” only by human repositioning the base, or by a wheeled platform that abandons docked power/data identity of R2.
- No credible **≥ 2 dock** latch + power/data reconnect sequence (even if simplified for MVP).

### Veto V5 — Transmission the agent cannot maintain
- Tendon/belt/cable drive with **no** defined agent-accessible tensioning, inspection, or replacement procedure.
- Wear items buried such that distal failure always implies full proximal teardown.

### Veto V6 — Electronics placement blocks R8 / DFAA
- Compute or motor power electronics exist only off-board in a way that the “mobile unit” cannot operate as an integrated node (contradicts R8).
- Battery / dock power design forces permanent tether that prevents undocked transit **and** provides no dual-dock handoff story when Scenario B is claimed.

### Veto V7 — Acoustic / sensing dead on arrival
- Mechanism class is inherently dominated by continuous gear scream or impact chatter under **0.5 kg** class load with no mitigation path compatible with N6 (e.g. accepting stepper howl as normal).
- No physical place for mic/camera without destroying kinematic envelope assumptions.

### Veto V8 — Numbers ignored
- Required reach, payload, dock count, or node BOM are missed by construction (e.g. primary scheme needs 3 kg at 1.2 m and $3k actuators to “work”).

---

## How to use this sheet

1. **Survey (K2 / NotebookLM):**  
   - **Whole-system gate:** keep as *primary analogues* only systems that could plausibly pass K1.1 and not trigger K1.2.  
   - **Pattern mining (allowed):** systems that fail as a whole (e.g. Canadarm2 / ERA class — wrong scale, cost, non-COTS, not DFAA-agent serviceable) may still contribute **isolated technical ideas** (dual-ended docking logic, latch concepts, walking sequence, load-path thinking), **if and only if** each borrowed idea can be scaled or re-implemented under ADR-0003, COTS/FDM, and DFAA vetoes.  
   - When dropping a full system, tag the veto id; when retaining a pattern from it, note *“pattern only — not full-system analogue”* and the scaling condition.

2. **Candidate schemes (K4):** each S1/S2/S3 must include a short “passes checklist / no veto” note. Borrowed patterns must be named explicitly (source → scaled mechanism).

3. **Scoring (K5):** full-scheme DFAA veto failures are disqualifying, not soft −1 points. A scheme that *only* works by assuming industrial Canadarm-class hardware is vetoed even if the topology sketch looks elegant.

4. **ADR (K6):** selected scheme cites this file + ADR-0003; list rejected full-system analogues vs retained scaled patterns separately if useful

## Non-claims

- Does not choose serial vs tendon vs dual-ended.  
- Does not replace ADR-0003.  
- May be amended if ADR-0003 or spec changes.
- Rejecting a platform as a full-system analogue does **not** forbid scaled reuse of individual mechanisms or operational concepts from that platform.

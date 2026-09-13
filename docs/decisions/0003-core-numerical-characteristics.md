<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# ADR-0003: Phase 1 Working Numerical Characteristics

- **Status:** Accepted (working targets — revisit after first joint / relocatable-base prototype)
- **Date:** 2026-09-13
- **Deciders:** Project maintainers / agents working on Phase 1
- **Related:**
  - `docs/spec.md` (§4 constraints, §7 success criteria)
  - `docs/implementation-concepts.md` (§1 kinematics & actuation references)
  - `docs/tasks/0003-define-core-numerical-characteristics.md`
  - `docs/conversations/2026-09-13--core-numerical-characteristics.md`
  - ROADMAP Phase 1 — “Define core numerical characteristics…”

## Context

sint needs measurable targets before kinematics, motor selection, and dock design diverge.  
`spec.md` already constrains the solution space qualitatively:

- Functional node BOM **< ~$1000**
- Consumer FDM fabrication (desktop build volume class ~200 mm)
- **≥ 6 DoF**
- Motion must not corrupt acoustic diagnostics
- Consumer power / dock-oriented supply
- Explicit **non-goal**: industrial heavy payload

Task 0003 decomposed the work (N1–N8). Discussion fixed reference lessons (INNFOS GLUON quiet modular arm; IRIM Lab / LIMS2-AMBIDEX remote actuation & mass distribution; printable modular BLDC actuators) and MVP workspace intent: service a **Bambu Lab A1 mini**-class printer, table buffer, tool bay, and **≥ 2 docks** for relocatable-base tests.

This ADR freezes **working targets** (not final physics). They may change after the first joint prototype, dual-dock trial, or measured noise/backlash data.

## Decision

Adopt the following **Phase 1 working numerical characteristics** for design and COTS screening.  
Full kinematic synthesis, exact SKUs, and power-scenario ADR remain out of scope here.

### Summary table

| ID | Parameter | Working target | Unit | Short rationale |
|----|-----------|----------------|------|-----------------|
| N2 | Printable part envelope | ≤ **~175–180** per major printed piece | mm | Fits A1 mini-class bed; larger structures are segmented (DFAA) |
| N2 | Reach (one arm / base pose) | **0.5–0.8** (stretch ≤ **1.0**) | m | Covers printer + table + tool bay cluster; GLUON-class order |
| N2 | Dock count (MVP) | **≥ 2** | — | Minimum to demonstrate relocatable base |
| N2 | Dock spacing (centres) | **~0.6–1.2** | m | Matched to reach so one “step” can move between stations |
| N3 | Payload without EE | **0.5** continuous; **~1.0** peak | kg | Printed modules, light tools, COTS hardware; not industrial |
| N4 | DC bus | **24** (research band 12–48) | V | Common maker / BLDC FOC / tool ecosystem |
| N4 | System power | **100–200** continuous; **~300–500** short peak | W | Arm + compute headroom; quiet FOC stack |
| N4 | Power architecture (default) | **Scenario A**: dock-powered work + optional swappable battery for transit | — | Lower MVP risk; allows non-mirrored ends |
| N4 | Power architecture (alternate) | **Scenario B**: dock-only, dual-dock hot handoff, mirrored universal ends | — | Closer to pure Canadarm symmetry; higher interface risk |
| N5 | Proximal joint continuous torque | **~10–25** | N·m | From payload × reach × safety factor; LIMS-style mass distribution helps |
| N5 | Distal / wrist continuous torque | **~1–5** | N·m | Low distal inertia preferred |
| N5 | Joint speed (large axes) | **~30–90** | °/s | Assembly-first; subordinate to quietness & precision |
| N5 | Joint speed (wrist) | **~60–180** | °/s | Higher OK if inertia stays low |
| N6 | Acoustic acceptance (primary) | Motion must **not mask** speech / latch clicks at **0.5–1** | m | Spec acoustic transparency; GLUON-class qualitative bar |
| N6 | Acoustic proxy (secondary) | Orient to **≲ 45–50** dB(A) @ 1 m in quiet mode — **not frozen** | dB(A) | Formal limit only after a fixed measurement method |
| N7 | BOM — functional node | **< 1000** | USD | Spec hard ceiling (arm + onboard electronics + power path) |
| N7 | BOM — integration kit ambition | Target **≤ 1000**; document stretch **≤ ~1500** | USD | Node + 2 docks + basic EE + camera + mic; printer excluded |

### Explicit non-targets (MVP)

- ≥ 2–3 kg continuous payload at full reach  
- Industrial harmonic drives as default on every axis  
- Hard dB(A) legal-style limit without a lab procedure  
- Including the 3D printer itself in robot BOM  

## Options considered

| Topic | Option | Outcome |
|-------|--------|---------|
| Payload | 0.5 kg vs 2 kg class | **0.5 kg** continuous selected; 2 kg remains research ceiling only |
| Power | A (dock + battery) vs B (dual-dock only) | **A default** for numbers; B kept as alternate |
| BOM | Node-only vs full integration kit under $1000 | **Node < $1000** hard; kit is target with recorded stretch risk |
| Acoustics | Qualitative only vs fixed dB(A) | **Qualitative primary**; dB(A) proxy optional until measured |

## Consequences

### Positive
- Kinematics, actuator, and dock work share one number sheet  
- Aligned with COTS / FDM / quiet BLDC direction in `implementation-concepts.md`  
- ROADMAP item can be marked done; agents have citable targets  

### Risks / must revisit after first prototypes
1. **Printable gearbox noise & backlash** — may break N6 or effective precision before torque limits are hit  
2. **Tendon / remote drive serviceability** — DFAA must cover tensioning, wear, calibration  
3. **Integration kit cost** — 2 docks + EE + AV may push past $1000 unless actuators stay cheap  
4. **Scenario A vs B** — battery mass reduces payload margin; B demands mirrored high-current interfaces early  
5. **Reach × dock spacing × A1 mini layout** — needs one top-down workspace sketch before locking link lengths  
6. **Torque table** — refine after real arm mass and transmission choice (in-joint vs remote)  

### Neutral
- Does not choose kinematic topology (next ROADMAP item)  
- Does not pin motor SKUs or gearbox ratios  

## Implementation notes

1. Reference this ADR from `docs/current-state.md` and mark task 0003 closed when checklist matches.  
2. Mark ROADMAP “Define core numerical characteristics…” as done / satisfied by ADR-0003.  
3. Next design work (kinematics, joint module, docks) must cite these targets or explicitly propose an ADR amendment.  
4. After first joint prototype: measure noise, backlash, thermal, and achievable payload; update this ADR or issue a superseding note.  

## References

- `docs/spec.md` — constraints and success criteria  
- `docs/implementation-concepts.md` — GLUON, LIMS2-AMBIDEX, printable BLDC actuator lessons  
- `docs/conversations/2026-09-13--core-numerical-characteristics.md` — derivation discussion  
- `docs/tasks/0003-define-core-numerical-characteristics.md`

<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Task: Define component composition (COTS candidates)

**Status:** open  
**Related:**
- ROADMAP Phase 1 — “Define component composition (motors, drivers, gearboxes, sensors, compute, connectors — COTS candidates)”
- `docs/spec.md` (R7 COTS/FDM, R8 onboard compute, DFAA, quiet motion)
- `docs/decisions/0003-core-numerical-characteristics.md`
- `docs/decisions/0005-kinematic-scheme.md` (S2 primary)
- `docs/tasks/0004-placement-policy.md`
- `docs/implementation-concepts.md` (§1, actuators / FOC)
- Conversation: `docs/conversations/2026-09-17--component-composition.md`

**Goal:** Document a **Phase 1 component composition baseline**: which *classes* of parts the S2 arm needs, and **2–4 COTS (or open-hardware) candidates per class**, with fit to torque/power/acoustic/BOM/DFAA — without freezing a single vendor forever or designing full PCBs/CAD.

---

## Constraints (from existing decisions)

Must respect:

- **ADR-0005:** S2 serial 6-DoF, cascaded mass bias, asymmetric ends, power scenario A, coplanar docks, accessible belt/tendon where used
- **ADR-0003:** payload ~0.5 kg, reach 0.5–0.8 m, proximal ~10–25 N·m / distal ~1–5 N·m continuous bands, 24 V class, acoustic intent, functional-node BOM ceiling
- **DFAA:** agent-replaceable joint/drive module, tensioner, compute brick; no sealed proprietary-only repair path as default
- **N6:** prefer FOC BLDC quiet path over loud steppers as default narrative (steppers only if justified and scored)

Out of scope for this task:

- Full link CAD, belt channel detailed design
- Purchase orders / inventory
- Custom PCB layout (may list *controller families* only)
- MuJoCo asset pack as deliverable
- Non-coplanar climb-rated actuators

---

## Subtasks

### C0. Setup
- [x] C0.1 Create conversation file for this workstream
- [x] C0.2 Link this task from ROADMAP item

### C1. Bill of classes (what must exist on S2)
- [ ] C1.1 List functional classes: motors, gearboxes/reductions, drivers/FOC, encoders/sensors, joint/link MCU, central compute, power (dock + optional battery), connectors/harness, belt/pulley/tensioner (cascade), dock power-data (+ reserved air fitting class)
- [ ] C1.2 Map each class → joint region: proximal (J1–J2/J3 span) vs distal (J4–J6) vs base-end vs EE
- [ ] C1.3 Mark which classes are **required for MVP smoke test** vs **Phase 1 complete arm**

### C2. Requirements per class (from ADR, not from vendor gloss)
- [ ] C2.1 Proximal drive: continuous torque band, speed order-of-magnitude, voltage, bus, noise intent, DFAA boundary
- [ ] C2.2 Distal / cascade-driven axes: lower torque, mass budget, belt-side loads
- [ ] C2.3 Sensors: absolute vs incremental minimum; joint limit / temp as optional
- [ ] C2.4 Compute: local real-time vs central agent; CAN (or chosen bus) assumption
- [ ] C2.5 Connectors: dock vs inter-link vs EE; preference for tool-side serviceability

### C3. COTS / open-hardware shortlist (URLs only in git)
- [ ] C3.1 Motors + gearboxes: 2–4 candidates proximal, 2–4 distal (or integrated pod candidates scored against DFAA)
- [ ] C3.2 Drivers / FOC stacks (e.g. SimpleFOC-class, ODrive-class, vendor FOC boards) — open or documented protocols preferred
- [ ] C3.3 Encoders / feedback
- [ ] C3.4 Central compute module candidates (SBC / MCU-SoM class)
- [ ] C3.5 Connectors & power path (24 V class, dock contact *type* not final metal design)
- [ ] C3.6 Cascade mechanical COTS: belt pitch family, idlers, tensioners (dimensions as *examples*, not ADR-frozen)
- [ ] C3.7 Explicit **reject / avoid** list: sealed non-serviceable pods as only path; industrial-only pricing; patterns that fail V3/V5

### C4. Integration matrix
- [ ] C4.1 Table: class × S2 placement × candidate × notes (mass, torque, bus, DFAA, acoustic, rough unit cost band)
- [ ] C4.2 Identify **one “smoke-test joint” stack** (minimum parts to spin one proximal + one cascaded axis)
- [ ] C4.3 Note power scenario A implications (dock feed, optional proximal battery chemistry class only)

### C5. BOM risk (order-of-magnitude, not quote)
- [ ] C5.1 Roll-up rough cost bands for: 6-axis arm electromechanics + 2 docks electrical + one EE interface (exclude printer)
- [ ] C5.2 Flag items that threaten N7; propose cheaper alternates or deferred features
- [ ] C5.3 Do not claim “exceeds $1000” without stating assumption set

### C6. Decision record
- [ ] C6.1 Draft ADR: component composition baseline (classes + preferred candidate *families* + open issues)
- [ ] C6.2 Accept ADR; link from `docs/current-state.md` and ROADMAP
- [ ] C6.3 Close this task

### C7. Handoff
- [ ] C7.1 Follow-ups: first joint module CAD, harness diagram, dock contact prototype, optional driver firmware bring-up
- [ ] C7.2 Revalidate after hardware: torque/thermal, noise, belt life, real prices, DFAA swap time

---

## Done when

- [ ] Component **class list** exists and maps to S2 regions
- [ ] Per major class: **≥2 COTS/open candidates** with URL citations (no copyrighted PDFs in git)
- [ ] Integration matrix + smoke-test joint stack documented
- [ ] Rough BOM risk narrative vs ADR-0003 N7 (assumptions explicit)
- [ ] ADR accepted; ROADMAP + current-state updated
- [ ] Open issues / revalidate-after-prototype listed

---

## Method notes

- Prefer **families and ranges** over single immortal SKU
- DFAA and N6 are hard filters; price is a hard risk filter
- Candidate links: manufacturer pages, DigiKey/Mouser/LCSC, open GitHub — **URL only**
- Do not merge this task into full arm CAD or firmware architecture ADR
- Align with implementation-concepts (quiet FOC, printable actuator ideas as *optional* track, not default sealed pod)

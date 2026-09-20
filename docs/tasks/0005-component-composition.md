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
- `docs/decisions/0006-lims-class-performance-aspiration.md` (LIMS-class bar; S4 parallel; S2 still baseline)
- `docs/references/lims-family-notes.md`
- `docs/tasks/0004-placement-policy.md`
- `docs/implementation-concepts.md` (§1, actuators / FOC)
- Conversation: `docs/conversations/2026-09-17--component-composition.md`

**Goal:** Document a **Phase 1 component composition baseline** for the arm: classes of parts, and **2–4 COTS/open candidates per class**, fit to torque/power/acoustic/BOM/DFAA. **Default mapping follows S4** (ADR-0005 as amended 2026-09-20: LIMS-inspired serial 6-DoF). **Retain S2 class deltas** so fallback remains executable without redoing the whole shortlist. **Scheme-agnostic smoke-test** stacks (one FOC axis ± short cascade / single joint) may proceed in parallel and do not depend on full S4 wrist/elbow bring-up.

---

## Constraints (from existing decisions)

Must respect:

- **ADR-0005 (amended 2026-09-20):** **MVP primary = S4** — base → J1 → shoulder yoke (J2/J3) → L2 upper arm (compute, optional battery, wrist pack) → dual-hinge elbow (rigid link) → light L3 → bevel 3-DoF wrist; open through-elbow media; asymmetric ends; power scenario A; coplanar docks; base aux-latch walk. **S2** = explicit cascade **fallback**; **S1** = last-resort distal if both transmission paths fail DFAA/N6. See `docs/tasks/0005-s2-s4-gate.md`.
- **ADR-0006:** LIMS-class motion *direction* under DFAA/BOM; opaque multi-cable packs remain gated; no payload÷10 motor scaling from LIMS; relocatable/multi-dock walking remains a first-class direction (planar Phase 1).
- **ADR-0003:** payload ~0.5 kg, reach 0.5–0.8 m, proximal ~10–25 N·m / distal ~1–5 N·m continuous bands, 24 V class, acoustic intent, functional-node BOM ceiling.
- **DFAA:** agent-replaceable joint/drive module, tensioner, compute brick, elbow/wrist packs as applicable; no sealed proprietary-only repair path as default.
- **N6:** prefer FOC BLDC quiet path over loud steppers as default narrative (steppers only if justified and scored).

Out of scope for this task:

- Full link CAD, belt/cable channel detailed design, pretension final mechanism (may list *options*)
- Purchase orders / inventory
- Custom PCB layout (may list *controller families* only)
- MuJoCo asset pack as deliverable
- Non-coplanar climb-rated actuators
- Claiming parity with any external commercial arm

---

## Subtasks

### C0. Setup
- [x] C0.1 Create conversation file for this workstream
- [x] C0.2 Link this task from ROADMAP item

### C1. Bill of classes (what must exist on S2)
- [x] C1.1 List functional classes: motors, gearboxes/reductions, drivers/FOC, encoders/sensors, joint/link MCU, central compute, power (dock + optional battery), connectors/harness, belt/pulley/tensioner (cascade), dock power-data (+ reserved air fitting class)
- [x] C1.2 Map each class → joint region: proximal (J1–J2/J3 span) vs distal (J4–J6) vs base-end vs EE
- [x] C1.3 Mark which classes are **required for MVP smoke test** vs **Phase 1 complete arm**

→ [0005-bill-of-classes.md](0005-bill-of-classes.md)

### C1b. LIMS-class / S4 parallel branch (before full-arm COTS freeze)
- [x] C1b.1 Curate publications + open recreations (URL only) into `docs/references/lims-family-notes.md`
- [x] C1b.2 One-pager: dual-axis / rolling elbow — kinematics intent, dock-perimeter reach, DFAA risks → [0005-lims-elbow-onepager.md](0005-lims-elbow-onepager.md)
- [x] C1b.3 One-pager: N+1-to-2N + pretension — what is known publicly; consumer-reproducible subset? → [0005-lims-n1-to-2n-onepager.md](0005-lims-n1-to-2n-onepager.md)
- [x] C1b.4 Draft **S4** stick-level description (LIMS-inspired, ADR-0003 bands, accessible transmissions only) → [0005-candidate-scheme-s4.md](0005-candidate-scheme-s4.md)
- [x] C1b.5 **S2 vs S4** scorecard: dock-neighbourhood workspace, distal inertia, DFAA, BOM risk, open reproducibility, N6 path → [0005-s2-vs-s4-scorecard.md](0005-s2-vs-s4-scorecard.md)
- [x] C1b.6 Gate decision note: keep S2 / prefer S4 / hybrid — **required before C6 full-arm composition ADR → [0005-s2-s4-gate.md](0005-s2-s4-gate.md)

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
- [ ] C3.6 Cascade mechanical COTS: belt **and** short tendon/cable hardware, idlers, tensioners (examples only); flag long multi-cable packs as S4-research, not default shortlist
- [ ] C3.7 Explicit **reject / avoid** list: sealed non-serviceable pods as only path; industrial-only pricing; patterns that fail V3/V5

### C4. Integration matrix
- [ ] C4.1 Table: class × S2 placement × candidate × notes (mass, torque, bus, DFAA, acoustic, rough unit cost band)
- [ ] C4.2 Identify **one scheme-agnostic smoke-test joint** stack (proximal FOC ± short cascade)
- [ ] C4.2b If S4 advances: list **delta** classes only (extra elbow DoF drive, cable set, pretension unit)
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

- [ ] S2 vs S4 gate note exists (or explicit deferral with date/owner) before full-arm composition ADR
- [ ] LIMS-class aspiration cited (ADR-0006); smoke-test stack does not depend on unresolved S4
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

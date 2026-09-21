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
- `docs/decisions/0005-kinematic-scheme.md` (amended: **S4 MVP primary**, S2 fallback)
- `docs/decisions/0006-lims-class-performance-aspiration.md`
- `docs/tasks/0005-s2-s4-gate.md`
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

### C1. Bill of classes (inventory; written under S2, still valid as class list)
- [x] C1.1 List functional classes: motors, gearboxes/reductions, drivers/FOC, encoders/sensors, joint/link MCU, central compute, power (dock + optional battery), connectors/harness, belt/pulley/tensioner (cascade), dock power-data (+ reserved air fitting class)
- [x] C1.2 Map each class → joint region: proximal (J1–J2/J3 span) vs distal (J4–J6) vs base-end vs EE
- [x] C1.3 Mark which classes are **required for MVP smoke test** vs **Phase 1 complete arm**

→ [0005-bill-of-classes.md](0005-bill-of-classes.md) — apply **S4 region delta** when using for C2–C4

### C1b. LIMS-class / S4 parallel branch (before full-arm COTS freeze)
- [x] C1b.1 Curate publications + open recreations (URL only) into `docs/references/lims-family-notes.md`
- [x] C1b.2 One-pager: dual-axis / rolling elbow — kinematics intent, dock-perimeter reach, DFAA risks → [0005-lims-elbow-onepager.md](0005-lims-elbow-onepager.md)
- [x] C1b.3 One-pager: N+1-to-2N + pretension — what is known publicly; consumer-reproducible subset? → [0005-lims-n1-to-2n-onepager.md](0005-lims-n1-to-2n-onepager.md)
- [x] C1b.4 Draft **S4** stick-level description (LIMS-inspired, ADR-0003 bands, accessible transmissions only) → [0005-candidate-scheme-s4.md](0005-candidate-scheme-s4.md)
- [x] C1b.5 **S2 vs S4** scorecard: dock-neighbourhood workspace, distal inertia, DFAA, BOM risk, open reproducibility, N6 path → [0005-s2-vs-s4-scorecard.md](0005-s2-vs-s4-scorecard.md)
- [x] C1b.6 Gate decision note: keep S2 / prefer S4 / hybrid — **required before C6 full-arm composition ADR → [0005-s2-s4-gate.md](0005-s2-s4-gate.md)

### C2. Requirements per class (from ADR, not from vendor gloss)
- [x] C2.1 Proximal drives (J1 base, J2/J3 on yoke): continuous torque, speed OOM, voltage, bus, N6, DFAA module boundary → [0005-class-requirements-motors.md](0005-class-requirements-motors.md)
- [x] C2.2 Distal wrist axes (motors on **L2**, load at bevel wrist via through-elbow media): lower torque, **L2 pack mass budget**, belt/cable side loads, decoupling assumption → same
- [x] C2.3 Elbow path: dual-hinge + **rigid link** (loads, bearings, DFAA cartridge); not only “cascade belt” → [0005-class-requirements-elbow.md](0005-class-requirements-elbow.md)
- [x] C2.4 Sensors: absolute vs incremental minimum; joint output preferred long-term → [0005-class-requirements-sensors.md](0005-class-requirements-sensors.md)
- [ ] C2.5 Compute / battery: **on L2 upper arm** (not dock interface block); local RT vs central agent; bus
- [ ] C2.6 Connectors: dock vs inter-link vs EE; tool-side serviceability
- [x] C2.7 **S2 fallback delta** (one short subsection): what changes if wrist pack returns to forearm + short belts (requirements that shrink/drop) → fallback in all documents in this section

### C3. COTS / open-hardware shortlist (URLs only in git)
- [ ] C3.1 Motors + gearboxes: proximal (J1–J3) and distal (wrist pack on L2) — 2–4 each
- [ ] C3.2 Drivers / FOC stacks (e.g. SimpleFOC-class, ODrive-class, vendor FOC boards) — open or documented protocols preferred
- [ ] C3.3 Encoders / feedback
- [ ] C3.4 Central compute module candidates (SBC / MCU-SoM class) — sized for **L2** mount
- [ ] C3.5 Connectors & power path (24 V class, dock contact *type* not final metal design)
- [ ] C3.6 Transmission COTS: through-elbow **belt and/or short cable**, idlers, rollers, **pretension options** (examples); dual-hinge bearings/fasteners class; bevel or printable gear options for wrist
- [ ] C3.7 Reject/avoid list (sealed-only pods, industrial-only, V3/V5 fails)
- [ ] C3.8 Optional: one paragraph **S2 fallback** shortlist reuse (same motors/drivers; different X/T layout)

### C4. Integration matrix
- [ ] C4.1 Table: class × **S4 placement** × candidate × notes (mass, torque, bus, DFAA, acoustic, cost band)
- [ ] C4.2 One **scheme-agnostic smoke-test** stack (proximal FOC ± short cascade / single axis)
- [ ] C4.3 **S4-specific** delta classes: dual-hinge elbow set, rigid link, through-elbow media, bevel wrist, pretension option
- [ ] C4.4 Compact **S2 fallback** column or footnote (not a second full matrix)
- [ ] C4.5 Power scenario A: dock feed; optional battery on **L2**

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

- [x] S2 vs S4 gate exists (`0005-s2-s4-gate.md`)
- [ ] Class list exists; **regions interpreted for S4** (bill + delta)
- [ ] Per major class ≥2 candidates with URLs
- [ ] Integration matrix **S4-primary** + smoke-test stack
- [ ] Rough BOM risk narrative vs ADR-0003 N7 (assumptions explicit; S4 default)
- [ ] ADR accepted; ROADMAP + current-state updated

---

## Method notes

- Prefer **families and ranges** over single immortal SKU
- DFAA and N6 are hard filters; price is a hard risk filter
- Candidate links: manufacturer pages, DigiKey/Mouser/LCSC, open GitHub — **URL only**
- Do not merge this task into full arm CAD or firmware architecture ADR
- Align with implementation-concepts (quiet FOC, printable actuator ideas as *optional* track, not default sealed pod)

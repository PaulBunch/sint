<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C2.1 / C2.2 / C2.7 — Motor & drive-train class requirements (S4 primary)

**Status:** done for motor-centric subset of C2  
**Scheme:** S4 MVP primary; S2 fallback deltas in §C2.7  
**Sources:** ADR-0003, ADR-0005 (amended), ADR-0006, S4 stick, lims-family-notes, LIMS papers (principles only), US20220074468A1 (reference, not requirement)

**Not in this doc:** final SKU, full gearbox shortlist (C3), encoder detail beyond motor-loop needs (C2.4).

---

## Shared principles (from LIMS physics, scaled to sint)

1. **Reflected rotor inertia** scales ~ **J_rotor × N²**. Prefer low J_rotor and/or moderate N over “any motor + huge ratio”.
2. **Backdrivability / low friction** support N6 and contact tasks; current sensing as soft force proxy is desirable.
3. **Do not** import LIMS continuous joint torques or custom 28.7 g·cm² motors as musts.
4. **Do not** require multi-wrap tension-amplification or patented compound planetary as default path.

---

## C2.1 Proximal drives (J1 on base → yoke; J2 & J3 on yoke)

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| P-M1 | After reduction, **continuous joint torque** in ADR-0003 proximal band: **~10–25 N·m** (J1, J2); J3 **~5–15 N·m** | ADR-0003 + S4 stick |
| P-M2 | **24 V class** electrical | ADR-0003 |
| P-M3 | **FOC-capable BLDC** (or documented equivalent); steppers not default | N6 |
| P-M4 | Open or well-documented drive protocol path (e.g. SimpleFOC / ODrive-class families in C3) | DFAA, no sealed-only stack |
| P-M5 | **Replaceable drive module** boundary: motor (+ gearbox if integrated) + connector; agent-swappable without destroying yoke/base | DFAA |
| P-M6 | Thermal path compatible with continuous band at sint duty (order-of-magnitude; prove on smoke test) | Reliability |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| P-S1 | **Low rotor inertia** relative to typical same-torque COTS; treat J_rotor as first-class shortlist metric | LIMS lesson; effective mass |
| P-S2 | **Hollow shaft / large central bore** on **J1** (and prefer on J2 if harness crosses axis) for power/data | LIMS2 ~30 mm is aspirational scale; sint may use smaller bore if harness allows |
| P-S3 | Compact **flat / high torque-density** form factor for yoke packing (J2, J3) | S4 yoke density |
| P-S4 | Backdrivable reduction stage (planetary low ratio, belt, capstan, …) — scored in C3 | Compliance, N6 |
| P-S5 | FOC stage co-located or short-harness to motor; **thermal design without default forced-air fans** (heatsink, derating, duty limits). Active fans only if measured thermal failure and N6 budget still met | Packaging + N6 |

### Out / non-goal (proximal)

| ID | Out |
|----|-----|
| P-O1 | Custom wound motor as Phase-1 requirement |
| P-O2 | Industrial harmonic-only as sole path |
| P-O3 | Matching LIMS2 28.7 g·cm² or EX joint N·m tables |
| P-O4 | Capstan or compound planetary as mandatory topology |

**Speed OOM:** joint speeds of order **10² °/s** are *consistent* with LIMS demos and sint assembly tasks; not a hard datasheet floor until measured. Prefer motors that are not thermally limited only at crawl speeds.

---

## C2.2 Distal wrist axes (motors on **L2**, torque at bevel wrist via through-elbow media)

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| D-M1 | Continuous torque at **wrist axes** **~1–5 N·m** after all stages | ADR-0003 distal band |
| D-M2 | Motors **mounted on L2** (upper arm), not on light forearm/wrist shell | S4 |
| D-M3 | Transmission **through dual-hinge elbow** with **open, serviceable** belt or short cable; elbow motion must not systematically reel media (decoupling geometry) | S4 + elbow one-pager. See also `0005-class-requirements-media.md` |
| D-M4 | 24 V FOC BLDC class; same protocol family preference as proximal | N6, harness |
| D-M5 | Pack is a **DFAA unit** (motors + stages + connectors); retension without destroying L2 | DFAA |
| D-M6 | **L2 pack mass** treated as design budget: baseline = relocate S2 forearm pack mass to L2; allow **×1.0–1.3** if pretension/rollers added | S4 §4.9; inertia OOM |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| D-S1 | Low J_rotor still matters (wrist ratios + long reflected path) | Same physics |
| D-S2 | Prefer smaller/lighter motors than proximal; torque density over hollow shaft | Distal band |
| D-S3 | Belt or thin cable side loads within COTS belt/cable ratings at sint tension | Avoid oversize industrial cable |
| D-S4 | Bevel (or equivalent) wrist 3-DoF does not force sealed gear grease packs as only option; printable/MVP gears allowed for bring-up | Gate + scorecard |

### Out / non-goal (distal)

| ID | Out |
|----|-----|
| D-O1 | Multi-wrap tension-amplification (n, n²) as **default** MVP requirement |
| D-O2 | Full LIMS-EX N+1-to-2N / single pretension clone |
| D-O3 | Wrist motors in forearm (that is S2 fallback layout) |
| D-O4 | Payload-scaled copy of LIMS distal continuous torques |

---

## C2.7 S2 fallback delta (motors / drive)

If gate triggers move primary to **S2**:

| Topic | Change |
|-------|--------|
| Torque / V / FOC / J_rotor principles | **Unchanged** (same ADR-0003 bands) |
| J3 motor location | In **L2** with **short belt** (not only yoke + rigid link) |
| J4–J6 motors | **Proximal forearm pack**, short accessible belts — **not** through-elbow from L2 |
| Through-elbow media + dual-hinge cartridge | **Drop** as must |
| Rigid elbow link | **Drop** as must |
| L2 pack mass budget for wrist motors | **Relaxes** (wrist mass leaves L2) |
| Hollow shaft on J1 | Still should |
| Same motor *families* in C3 reusable; **X/T layout** changes |

S1 last-resort: in-joint distal modules; still FOC/N6/DFAA; highest distal mass — only if cascade paths fail.

---

## Mapping to C3 (preview, not done)

Shortlist will score candidates on:

- Continuous torque after realistic N vs bands above  
- J_rotor (or proxy: rotor class / “gimbal motor” vs heavy outrunner)  
- Mass, diameter, hollow bore (J1)  
- FOC support + DFAA module story  
- Rough unit cost vs N7  

LIMS Maxon flat / custom IRIM motors / patent compound planetary = **calibration references**, not mandatory SKUs.

---

## Document control

| Item | Value |
|------|--------|
| Closes | C2.1, C2.2, C2.7 **for motor/drive class** |
| Does not close | C2.3–C2.6, C3 shortlist, gearbox family freeze |
| LIMS use | Principles + warnings; no ÷10 torque scaling |

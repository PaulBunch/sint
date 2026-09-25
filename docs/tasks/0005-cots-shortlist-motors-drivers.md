<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C3.1 / C3.2 — COTS shortlist: motors & FOC drivers

**Status:** draft shortlist (families for MVP procure / bench)  
**Normative filters:** `docs/tasks/0005-class-requirements-motors.md`  
**Number catalog (SoT):** [`0005-motors-catalog.csv`](0005-motors-catalog.csv)  
**Sources:** [`0005-motors-catalog-sources.md`](0005-motors-catalog-sources.md)  
**Scheme:** S4 · Power A · ADR-0003 torque bands · moderate \(N \approx 5\ldots20\) (not CNC-class)

**Out of this shortlist:** Maxon / Kollmorgen frameless as MVP SKUs (cost & supply); pure “toy-only” axes that cannot serve any MVP joint after moderate reduction.

**MVP = first hardware loop** (bring-up, FOC, thermal, noise, backdrive feel). No separate disposable smoke-only motor class.

---

## Design rules (recap)

1. **Joint torque** is the target (ADR continuous bands), not motor nameplate alone.  
2. Prefer **moderate reduction** so reflected inertia \(J_\mathrm{rotor} N^2\) stays acceptable.  
3. Two electrical paths allowed:
   - **24 V raw** BLDC + external FOC + separate G  
   - **48 V integrated joint module** (motor + G + driver in one)  
4. **LIMS-EX torque norms** (shoulder yaw = 1.0) may guide *relative* sizing across J1…wrist; absolute scale remains ADR (~0.5 kg payload), not 5 kg LIMS.

| Joint role | LIMS-EX norm | sint continuous OOM (joint) |
|------------|--------------|-----------------------------|
| J1 base | 1.0 | ~10–25 N·m |
| J2 | ~0.8 | scale from J1 |
| J3 elbow | ~0.7 | ~5–15 N·m class |
| Wrist axes | ~0.1–0.3 | ~1–5 N·m |

---

## C3.1 Motors — primary shortlist

Full rows: CSV. Below: **why selected** only.

### Path A — integrated joint module (Fulling iSVD)

| ID | Model (CSV) | Role | Why in shortlist | Watch-outs |
|----|-------------|------|------------------|------------|
| **A1** | **iSVD88C-48V-480-A14-001** | Proximal (J1–J2) | **11 N·m rated out**, peak 36; FOC + dual enc + **9:1** in one; hits lower–mid proximal band without external gearbox | **48 V**; ~621 g; vendor CAN stack; DFAA weaker than bare motor |
| **A2** | **iSVD78C-…** (36/48 V variants in catalog) | J3 / light proximal | **~6 N·m out**, lighter than 88 | Same module ecosystem; verify exact RU listing |
| **A3** | **iSVD46C-48V-17-A14-001** | Distal / wrist | **1.6 N·m out** already in distal band | 48 V; module mass on L2 |

**Implication:** external planetary **not required** on these axes if module is accepted. External ODrive-class **not required** for commutation (driver inside). Spine still talks **CAN** (or gateway).

### Path B — raw BLDC + separate reduction + external FOC (24 V-class preferred)

| ID | Model (CSV) | Role | Why in shortlist | Watch-outs |
|----|-------------|------|------------------|------------|
| **B1** | **iPower GM110-10** | Proximal | Highest gimbal τ class in catalog (~0.9–1.5 N·m load); hollow ~22 mm; with \(N \sim 12\ldots20\) can approach proximal band | Load ≠ industrial continuous; **J unknown**; ~20 V nominal |
| **B2** | **iPower GM8112** | Proximal / J3 | Strong mid (~0.6–0.9 N·m load); hollow; lighter than GM110 | Same gimbal caveats |
| **B3** | **iPower GM6208** | J3 / light proximal | Hollow 22 mm; common; solid mid τ | Alone weak for full J1 15–25 N·m without higher N |
| **B4** | **Fulling FL48CBL68-24V-3060A** | J3 / light proximal | **24 V**; **J = 80 g·cm²** (rare published); τ ~0.18 N·m → joint ~2–4 N·m at \(N \sim 12\ldots20\) | Long body (68 mm); not full J1 alone |
| **B5** | **Fulling FL60BLW\* 24 V** | Proximal raw | Higher τ_m (~0.29 N·m); 24 V | **J ~1000 g·cm²** — worse reflected inertia than FL48 |
| **B6** | **iPower GM4108H** or **T-Motor GB36-2** | Distal | τ class for wrist after moderate N; obtainable hobby channel | J unknown (gimbal/T-Motor) |
| **B7** | **Fulling FL45BLW\* 24 V** | Distal | Published **J ~100–180**; 24 V; LIMS1-order inertia class | Lower τ_m → needs N |

**Reduction (G) for Path B only:** planetary or belt **\(N \approx 8\ldots20\)** (prefer ≤15 when J is unknown or high). Harmonic ≥50:1 **not** default.

### Recommended MVP mix (default proposal)

| Joint region | Preferred | Fallback if iSVD unavailable / over budget |
|--------------|-----------|-----------------------------------------------|
| J1–J2 | **A1 iSVD88** | **B1 GM110-10** + G + FOC |
| J3 | **A2 iSVD78** or **B3/B4** | GM6208 or FL48 + G |
| Wrist (on L2) | **A3 iSVD46** or **B6/B7** | GM4108 / FL45 + G |

Do **not** freeze SKUs until one axis is powered and measured (τ derate, noise, thermal).

---

## C3.2 Drivers / FOC

| Path | Driver approach | Notes |
|------|-----------------|--------|
| **A (iSVD)** | **Built-in FOC**; host via **CAN** (vendor protocol / manuals) | No ODESC required for phase drive; spine = CAN master/gateway |
| **B (raw)** | **ODESC / ODrive 3.6-class** (RU market clones) or better documented FOC with encoder input | Match continuous current to motor; **encoder required** for joint use |
| **B light / distal** | SimpleFOC-class acceptable if current suffices | Prefer same family across axes when possible |

**N6:** no default forced-air on driver packs.  
**24 V driver must not be fed 48 V.** Path A implies **48 V bus** (or isolated converters). Path B stays **24 V class** where motors allow.

---

## Explicit non-goals for this revision

- Maxon EC flat / Kollmorgen RBE as MVP line items  
- Stepper + high N as default  
- Smoke-only micro motors that cannot map to any ADR joint after moderate N  
- Assuming gimbal “load torque” = continuous industrial rating without bench derate  

---

## Next actions

1. Check RU price/lead for **iSVD88 / iSVD46** vs **GM110-10 + planetary + ODESC**.  
2. Pick **one** Path A *or* Path B stack for the first powered axis.  
3. Update CSV `role_hint` to match this table.  
4. After first axis data: C3 freeze note or ADR amendment (24 vs 48 V bus).

---

## Document control

| Item | Value |
|------|--------|
| Catalog SoT | `0005-motors-catalog.csv` |
| Closes | C3.1/C3.2 **shortlist draft** (not purchase order) |
| Open | Live RU quotes; J measurement on gimbal; bus voltage decision |

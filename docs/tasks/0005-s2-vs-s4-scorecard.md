<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C1b.5 — S2 vs S4 scorecard

**Status:** done (comparative judgment — not lab measurement)  
**Closes:** task 0005 item C1b.5  
**Does not close:** C1b.6 gate decision (keep S2 / prefer S4 / hybrid)  
**Inputs:**
- S2: `docs/tasks/0004-candidate-schemes.md` §2  
- S4: `docs/tasks/0005-candidate-scheme-s4.md`  
- ADR-0003, ADR-0005, ADR-0006, placement policy, K1  
- `docs/tasks/0005-lims-elbow-onepager.md`, `docs/tasks/0005-lims-n1-to-2n-onepager.md`

**Scoring legend (1–5):** 5 = clearly better for sint Phase 1 goals; 3 = comparable / acceptable; 1 = weak.  
Scores are **relative S2↔S4**, not absolute product grades.

**Comparability note:** At this stage the **S4 wrist/elbow path is specified in more mechanical detail** (bevel wrist, dual-hinge, rigid link, through-elbow media) than the **S2 cascade wrist**, which remains a higher-level “short accessible belts/tendons” sketch. Scores that touch wrist internals are therefore **asymmetric in maturity**, not a proof that S2 is inherently simpler in every physical realization. Where S2 is underspecified, assume it may later need comparable discrete parts (idlers, gears, covers) once CAD exists.

---

## 1. Snapshot comparison

| Dimension | S2 (ADR-0005 baseline) | S4 (LIMS-inspired candidate) |
|-----------|------------------------|------------------------------|
| Family | Serial 6-DoF cascade | Serial 6-DoF, deeper proximal bias |
| Elbow | Single pitch; motor in **L2**, short belt | **Dual-hinge** 1 DoF; motor on **yoke**, **rigid link** |
| Wrist motors | Pack in **proximal forearm (L3)** | Pack on **upper arm (L2)** |
| Wrist mechanism | Independent short belts/tendons (stick) | **Bevel differential 3-DoF** + through-elbow media |
| Forearm mass | Motors + structure | Structure only (lightest distal) |
| Compute / optional transit battery | **On upper arm (shoulder link)** in a walking-capable layout — not inside the dense dock interface block | **On L2 upper arm** (same rational placement) |
| Power / ends / walk | Scenario A, asymmetric, base aux-latch | Same |
| Reach / docks | 0.5–0.8 m class; ~0.5–0.6 m step | Same bands; better **fold / dock-neighbourhood** claim |

**Placement alignment:** Both schemes should keep **central compute and optional transit battery on the upper-arm link**, away from the dock latch/connector cluster. Older S2 wording that put compute on “Link 1 / base” is treated as a **documentation debt** for this scorecard; it is not scored as an S2 advantage.

**Inertia OOM (agreed):** S2 wrist-pack mass moves L3→L2 in S4; optional ×1.1–1.3 for pretension/sliders. Distal (beyond elbow) inertia: **S4 advantage**. Moving mass on L2 still loads J2.

---

## 2. Scorecard

| Criterion | Weight | S2 | S4 | Notes |
|-----------|--------|----|----|-------|
| **Dock-neighbourhood workspace** | High | 3 | **5** | Same reach numbers; S4 dual-hinge fold + light forearm improves service around / slightly below dock plane and dual-dock approach poses |
| **Distal inertia** (beyond elbow) | High | 3 | **5** | S4 removes wrist pack from L3; strongest LIMS-class win |
| **Proximal / shoulder loading** | Med | **4** | 3 | S4 puts wrist pack + compute + battery on L2 → higher J2 reflected inertia than S2 (pack was on L3) |
| **DFAA / serviceability** | High | **4** | **3–4** | Both require open covers and replaceable packs. S4 names more mechanisms *today*; S2 may grow similar part counts in CAD. S4 residual risk = pretension TBD + through-elbow routing until proven |
| **BOM risk (N7)** | High | **4** | **3–4** | Motor/driver count similar. S4 lists dual-hinge + bevel + rollers explicitly; S2 underspecified. MVP may use **printed gears/rollers** for mechanism validation; expect shorter life than metal — acceptable for MVP with planned fallback |
| **Open reproducibility** | High | **4** | 3 | S2 matches common DIY cascade practice. S4 depends on video-level LIMS-EX reconstruction; no full open EX BOM |
| **N6 acoustic path** | High | **4** | **4** | Both FOC + non-industrial gears possible. S2: belt mesh. S4: belts/cables + bevel; risk shifts, not clearly better/worse until prototype |
| **Control / calibration complexity** | Med | **4** | **3** | S4 differential wrist + elbow decoupling is structurally more coupled; magnitude depends on final S2 wrist CAD |
| **Fit to ADR-0003 bands** | High | **5** | **5** | Both explicitly in 0.5 kg / torque / planar dock frame |
| **Relocatable walk (planar)** | High | **4** | **4** | Same base aux-latch story; S4 does not need S3 dual-ended ends |
| **Path to LIMS-class dynamics** | Med | 2 | **5** | Core ADR-0006 reason for S4 |
| **Time-to-first-smoke-test** | Med | **5** | **3** | Scheme-agnostic FOC smoke test is unchanged. Full-arm first article: S2 still fewer *named* novel subassemblies; not a claim S2 has zero gears |

**Weighted reading (informal, maturity-aware):**
- **S2** still advantaged on *time-to-integrate* and *known cascade story*, not on proven thinner BOM.
- **S4** advantaged on **distal inertia** and **dock-neighbourhood fold**, with mechanics specified further ahead.
- **N6, planar walk, ADR-0003:** still shared.
- Wrist complexity comparison is **provisional** until S2 is detailed to a similar depth.

Neither scheme fails K1 planar-dock or Scenario A rules as written.

---

## 3. Criterion notes (short)

### 3.1 Dock-neighbourhood workspace
S2 is adequate for A1-mini + table + tool-bay with 0.5–0.6 m docks. S4’s dual-hinge fold is the main geometric upgrade for working near the occupied dock without lengthening links past print limits.

### 3.2 Distal inertia
Clear S4 win if wrist pack truly stays on L2 and forearm stays shell+bearings. Benefit is tip speed, contact safety, and less “tremor” from distal mass — aligned with LIMS demos qualitatively.

### 3.3 DFAA
Both schemes commit to agent-accessible transmissions (V5). S4’s dual-hinge, rigid link, and through-elbow paths are **called out now**; S2’s cascade is **less detailed**, so a lower “parts complexity” score for S2 would be unfair. Fair residual: S4 still carries **open pretension choice** and multi-path elbow routing that must stay serviceable. Printed plastic gears/rollers are allowed for **MVP mechanism checks**; durability limits are accepted with an explicit hardware fallback path (see §4).

### 3.4 BOM risk
Do not treat “S4 has bevels / elbow gears” as unique cost sin until S2 wrist CAD exists. Prefer: similar actuator electronics; mechanical BOM uncertainty **higher on S4 only where geometry is already fixed**. Printed prototypes reduce early cash risk at the expense of wear life.

### 3.5 Open reproducibility
S2: implementation-concepts + printable actuator path. S4: principles from lims-family-notes; full N+1-to-2N not peer-archived for EX. Hobby rolling joints (R1–R2) help elbow/wrist fragments only.

### 3.6 N6 path
Both assume quiet FOC. S4 does not automatically inherit LIMS silence — cable squeal and bevel mesh must be tested like S2 belts.

---

## 4. Risks, MVP validation, and fallback (no separate CAD branch now)

**No parallel “print critical parts to decide the gate” program** at this stage. Critical mechanisms are validated **inside the normal MVP build**, not a side CAD contest before C1b.6.

| Item | Approach |
|------|----------|
| Dual-hinge elbow, bevel wrist, through-elbow media (if S4 or hybrid) | Exercise in MVP; allow **printed** gears/rollers for first units |
| S2 cascade belts/idlers | Same MVP discipline once detailed |
| Wear of printed mesh | Expected; **not** a reason to block scheme choice |
| Fallback | Pre-declare triggers (binding, untunable pretension, N6 failure, DFAA service time) → simplify wrist media, single-hinge elbow, or S1-style in-joint distal — recorded at gate / ADR amendment |

**S2-specific doc fix (follow-up, not scored):** move compute/battery language to upper-arm link for consistency with walking + dock interface reality.

---

## 5. Implications for component composition (0005)

| Activity | Recommendation |
|----------|----------------|
| **Smoke-test FOC stack** | **Scheme-agnostic** — proceed under either baseline |
| **Full-arm COTS freeze (C6)** | **After C1b.6 gate** |
| **Shortlist classes** | Shared: motors, FOC, encoders, CAN, 24 V, dock connectors. S4-only: dual-elbow bearings/sync, bevel set, through-elbow rollers, pretension hardware |
| **Mass accounting** | Use §4.9 mass note when comparing inertia claims |
| **S2 documentation** | Correct compute/battery placement to **upper arm** (parity with S4 stack) in candidate-schemes or ADR follow-up |

---

## 6. Handoff to C1b.6 (gate — not decided here)

C1b.5 **does not** pick the winner. Options for the gate note:

| Option | When it fits |
|--------|----------------|
| **Keep S2 primary** | Prioritize DFAA, BOM, fast path; take S4 fold/inertia as backlog |
| **Prefer S4** | Accept longer mechanics path for distal inertia + dock workspace |
| **Hybrid** | e.g. S2 cascade wrist **or** S4 dual-hinge elbow only as first increment; full bevel through-elbow later |

**Suggested evidence before hard gate:** one dual-hinge elbow mock (print + rigid link) and/or paper refresh on LIMS wrist — not full arm.

---

## Document control

| Item | Value |
|------|--------|
| Revised | 2026-09-20 — maturity asymmetry S2/S4 wrist; compute on upper arm both schemes; printed MVP gears OK; no pre-gate CAD branch; fallback in MVP |
| Closes | C1b.5 (revised) |
| Next | Discussion → C1b.6 gate (keep S2 / prefer S4 / hybrid) |
| Related | ADR-0005 (unchanged until gate), ADR-0006 |

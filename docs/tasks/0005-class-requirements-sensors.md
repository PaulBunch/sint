<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C2.4 — Sensors (position, proprioception, auxiliaries)

**Status:** done (class requirements)  
**Scheme:** S4 primary (cascade / through-elbow media ⇒ joint angle ≠ motor angle under stretch)  
**Related:** ADR-0003, bill-of-classes **E** / **S**, motors & media reqs, lims-family-notes (encoder evolution LIMS2→LIMS3)

**LIMS reference (non-normative):** hybrid incremental-motor + absolute proximal-joint (LIMS2) → **absolute on motors and all joint outputs** (LIMS3/EX). No joint torque sensors; contact via motor current + low friction. Temp/tactile not part of their public arm sensor suite.

---

## 1. Position feedback

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| E-M1 | Every actively controlled axis has **motor-side** position feedback suitable for FOC/servo (incremental **or** absolute) | Smoke test + all Phase-1 axes |
| E-M2 | **MVP smoke test:** motor encoder only is acceptable | Fast bring-up |
| E-M3 | **Phase 1 complete arm (long-term target):** **absolute** position at **joint output** on each arm DoF (J1–J6), *or* an explicit documented exception with observer + risk acceptance | Media stretch/backlash; no homing dependency; LIMS3 lesson |
| E-M4 | Until full joint-absolute coverage exists, any motor-only axes that drive **compliant media** must have a stated calibration/observer strategy (even if simple) | LIMS2 JAN problem class |
| E-M5 | Encoder interfaces and mounting keep **DFAA**: replace sensor/module without destroying the joint shell | DFAA |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| E-S1 | **Absolute on motor and joint** where cost/pack allows (LIMS3 pattern) | Redundancy + stretch observability |
| E-S2 | Joint-output absolute preferred **early** on axes with longest compliant path (wrist via through-elbow; elbow) | Highest motor≠joint error |
| E-S3 | Resolution adequate for assembly positioning at 0.5 kg-class tasks (OOM; quantify in bring-up, not datasheet vanity) | ADR-0003 use case |
| E-S4 | Avoid sole reliance on battery-backed incremental “multi-turn” without joint absolute for cold start of a walking arm | Dock/walk safety |

### Out

| ID | Out |
|----|-----|
| E-O1 | Motion-capture or external lab metrology as **on-robot** requirement |
| E-O2 | Mandatory ultra-high-end industrial encoders that break N7 alone |

---

## 2. Force / torque / contact

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| F-M1 | FOC stack exposes **phase current** (or equivalent torque proxy) to control software | Proprioception baseline |
| F-M2 | **No requirement** for joint torque cells or wrist F/T on MVP | Mass, cost, LIMS pattern |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| F-S1 | Use current-based contact / soft impedance as primary interaction sensing while friction stays low (media + bearings) | N6 + compliance direction |
| F-S2 | Optional **EE F/T** later as a tool module, not embedded in every arm build | Composition EE class |

### Out

| ID | Out |
|----|-----|
| F-O1 | Joint torque sensors as default on J1–J6 |
| F-O2 | Tactile pressure arrays on links as Phase-1 arm requirement |

---

## 3. Auxiliary sensors (class S)

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| S-M1 | None beyond position + driver current for **smoke test** | Minimal path |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| S-S1 | **Temperature** on motor driver and/or motor (often onboard FOC board) for thermal derating | P-M6 thermal; not a LIMS must |
| S-S2 | Soft **limit** switches or hard-stop detection optional for bring-up safety | Does not replace encoders |
| S-S3 | Dock presence / latch-sense at **base** when implementing dual-dock walk | Relocatable direction; electrical class may own detail |

### Out (MVP arm)

| ID | Out |
|----|-----|
| S-O1 | Link IMUs as required for planar dual-dock MVP (revisit if walk state estimation needs them) |
| S-O2 | Tactile skins, acoustic mics-as-joint-sensors, etc. as composition musts |

---

## 4. Minimum configurations (summary)

| Stage | Position | Force proxy | Aux |
|-------|----------|-------------|-----|
| **Smoke test** | Motor encoder per test axis | Driver current | Optional driver temp |
| **MVP arm (acceptable interim)** | Motor encoder all axes + **joint absolute at least on media-heavy axes** (elbow/wrist) preferred | Current | Driver temp should |
| **Phase 1 target** | **Absolute joint output all J1–J6** (+ motor feedback as available) | Current; F/T only if EE option | Temp; dock sense as walk matures |

---

## 5. S2 fallback

Same encoder policy: compliant cascade still benefits from **joint-output absolute**. S2 may delay wrist joint abs slightly if spans are shorter, but Phase 1 target does not change.

---

## 6. Handoff to C3

Shortlist 2–4 **absolute** and 2–4 **incremental** (or dual) encoder families with URLs: magnetic/on-axis, SPI/I²C/ABI, size compatible with yoke/L2/wrist. Prefer parts that do not force sealed vendor lock-in.

---

## Document control

| Item | Value |
|------|--------|
| Closes | **C2.4** |
| Does not close | C3 encoder SKUs, observer design, IMU for walk |

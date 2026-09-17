<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# LIMS family — reference notes (IRIM Lab / related)

**Status:** living reference (extend as new public material appears)  
**Role for sint:** primary **external orientation** for remote/cable-driven low-inertia arms, mass distribution, and joint-level performance scale — **not** a normative ADR and **not** a commitment to copy topology, payload, or motor SKUs.  
**Normative sint numbers remain:** `docs/decisions/0003-core-numerical-characteristics.md`, kinematic scheme ADR, placement policy.

**How to use**

- Prefer **patterns** (proximal mass, light distal, cable routing ideas, sensor placement) over 1:1 scaling of torque or mass.
- Cite **source URLs only** in git; do not commit third-party video files or full transcripts beyond our notes.
- When adding a new LIMS variant, append a section; keep a short changelog at the bottom.

**Related project docs**

- `docs/implementation-concepts.md` §1.4 (synthesis for sint — may lag this file)
- `docs/decisions/0004-kinematic-survey-patterns.md` (cable/remote = pattern-only; opaque packs vs DFAA)
- `docs/tasks/0005-component-composition.md` (COTS classes; LIMS as calibration, not BOM)

---

## 1. Family overview

| Variant | Approx. public framing | Notes for sint |
|--------|-------------------------|----------------|
| **LIMS2-AMBIDEX** | Earlier lab arm; tendon / remote drive; low distal inertia | Survey baseline (see kinematic survey conversation) |
| **LIMS3-AMBIDEX** | Commercialization-oriented; higher shoulder torque & workspace payload; simplified drive for reliability | Rich public performance figures from 2022 demo video |
| **LIMS-EX** | “Tougher environments”; N+1-to-2N actuation; shared pretension; 6-DoF + gripper | Joint continuous-torque table useful as **upper scale** reference |

All figures below are **as extracted from public video material / descriptions** by project contributors. They may be incomplete or rounded; re-check sources before engineering use.

---

## 2. LIMS3-AMBIDEX

**Primary source:** [YouTube — New LIMS with Improved Performance! LIMS3-AMBIDEX](https://www.youtube.com/watch?v=7INPj1hdnyA) (published 2022-08-02)

### 2.1 Intent (from public narrative)

- Higher **payload** across the workspace vs LIMS2  
- Simpler drive aimed at **reliability / production**  
- Impact tolerance and **high backdrivability**  
- Safe interaction via compliance, low distal inertia, gravity compensation  

### 2.2 LIMS3 vs LIMS2 (public comparison)

| Parameter | LIMS3-AMBIDEX | LIMS2-AMBIDEX |
|-----------|---------------|---------------|
| Total arm mass | 9.1 kg | 6.8 kg |
| Mass below shoulder (moving part) | 4.50 kg | 3.61 kg |
| Payload | **5 kg** (entire workspace, as stated) | 3 kg (near body only, as stated) |
| Shoulder speed | 420 °/s | 481 °/s |
| Shoulder continuous torque | **42 N·m** (~4× LIMS2) | 10 N·m |
| Shoulder peak torque | **119 N·m** | 80 N·m |
| Encoders | Absolute on **all motors and joints** | Incremental on motors; ABS on shoulder & elbow |

### 2.3 Geometry, DoF, speeds

| Item | Value |
|------|--------|
| Arm span (shoulder → hand center) | **984 mm** |
| DoF per arm | **7** |
| Shoulder | 3 DoF, up to **420 °/s** |
| Elbow | 1 DoF, up to **730 °/s** |
| Wrist | 3 DoF |

**Wrist motion (as stated):**

| Axis | Range | Speed (up to) |
|------|--------|----------------|
| Roll & pitch | −90° … +90° | 1011 °/s |
| Distal yaw | −165° … +165° | 1310 °/s |

### 2.4 Distal segment masses

| Segment | Mass |
|---------|------|
| Elbow block | 268 g |
| Forearm | 949 g |
| Wrist | 174 g |

### 2.5 Joint friction (reported)

| Joint | Friction torque |
|-------|-----------------|
| Shoulder | 1.39 N·m |
| Elbow | 0.83 N·m |
| Wrist roll/pitch | 0.51 N·m |
| Wrist yaw | 0.49 N·m |

### 2.6 Positioning (experimental series, n = 40)

| Metric | Y | Z |
|--------|---|---|
| Max deviation | 0.097 mm | 0.092 mm |
| Std deviation | 0.043 mm | 0.036 mm |

*Context of measurement setup not fully specified in our notes — treat as order-of-magnitude demo performance, not a transferable accuracy budget for sint.*

### 2.7 Mechanism notes

**Elbow**

- Cable actuation; reported cable diameters **3.2 mm** and **1.6 mm**  
- Six wrist-control cables routed through the elbow **without coupling** elbow motion (as claimed)

**Wrist**

- Compact **quaternion joint** with absolute encoders on all 3 DoF  
- Distal yaw via **cable bevel gears**  
- **Large hollow** passage in the hand for power, signal, or pneumatic lines to the EE  

### 2.8 Ongoing work (as listed in source narrative)

- Impact resilience tests  
- Gravity compensation tests  
- Impedance control under impact  

### 2.9 Qualitative observation (contributor note)

In the demo, motion appears very smooth and largely quiet; drive noise becomes noticeable mainly when a human operator rapidly and irregularly backdrives the arm — consistent with low distal inertia and holding under gravity compensation.

### 2.10 Gaps (important for motor sizing)

Public LIMS3 material cited here gives **shoulder** continuous/peak torque and **distal masses / friction**, but **does not state continuous motor or joint torque for elbow and wrist drives**. Do not invent motor N·m for “below shoulder” without an additional source.

---

## 3. LIMS-EX

**Primary source:** [YouTube — LIMS-EX: Mechanical Design and Preliminary Testing](https://www.youtube.com/watch?v=cjIVU-O5PHo) (description / material dated 2026-02-16 in contributor capture)

### 3.1 Stated key features

- Unique **N+1-to-2N** actuation mechanism  
- **Single pretension** mechanism shared across all cables  
- High payload-to-weight ratio  
- Arm span **> 1 m**  
- High backdrivability with lightweight distal links  

### 3.2 Headline specifications

| Parameter | Value |
|-----------|--------|
| Structure | 6-DoF arm + 1-DoF gripper |
| Mass | 9.7 kg |
| Arm span | 1 m |
| Payload | 5 kg continuous force capability in entire workspace (as stated) |

### 3.3 Continuous joint torque

| Joint | Continuous torque [N·m] |
|-------|-------------------------|
| Shoulder yaw | 93 |
| Shoulder pitch | 72 |
| Elbow | 63 |
| Wrist pitch | 27 |
| Wrist roll | 8 |
| Wrist yaw | 19 |

*These are **joint-level** continuous torques as published in the source description, not necessarily motor-shaft ratings.*

### 3.4 Max speed

| Joint | Max speed [°/s] |
|-------|-----------------|
| Shoulder yaw | 450 |
| Shoulder pitch | 450 |
| Elbow | 450 |
| Wrist pitch | 570 |
| Wrist roll | 570 |
| Wrist yaw | 570 |

### 3.5 Notes for sint

- Joint torque table is the clearest **numeric scale** in the family notes so far (still ~10× sint ADR bands on several axes).  
- Shared single pretension is elegant but must be judged against **DFAA** (agent access, failure modes) before any imitation.  
- N+1-to-2N actuation is a research pattern — document only; no Phase 1 adoption.

---

## 4. Cross-cutting takeaways for sint (non-normative)

1. **Mass distribution:** multi-kg moving arm with **hundreds of grams** at wrist is achievable with remote cable drive — supports cascade / proximal bias, not copy of 5 kg payload.  
2. **Do not scale motors by payload ratio alone** (e.g. 5 kg → 0.5 kg ⇒ ÷10). Self-weight and \(m g L\) terms dominate; use ADR-0003 N5 + estimated arm mass.  
3. **Sensors:** LIMS3 emphasis on **absolute** sensing at motors and joints is a strong reference for class **E** in component composition.  
4. **Utilities:** hollow distal path for power/data/air aligns with reserved pneumatic / harness classes.  
5. **Acoustics / compliance:** quiet smooth motion and backdrivability are design goals to emulate qualitatively under N6 — not by copying their peak speeds.  
6. **DFAA filter:** long multi-cable packs and single shared pretension need explicit service stories; default sint remains **accessible short belt or short tendon**, not opaque full-arm cable trees.

---

## 5. Source index (URL only)

| ID | Topic | URL |
|----|--------|-----|
| S1 | LIMS3-AMBIDEX performance demo | https://www.youtube.com/watch?v=7INPj1hdnyA |
| S2 | LIMS-EX mechanical design & preliminary testing | https://www.youtube.com/watch?v=cjIVU-O5PHo |

*Add rows as new public sources are curated. Prefer official lab channels and peer-visible demos.*

---

## Changelog

| Date | Change |
|------|--------|
| 2026-09-17 | Initial file: LIMS3 extract from S1; LIMS-EX specs from S2 description; sint usage notes |

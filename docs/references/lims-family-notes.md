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

**Primary source:** [YouTube — LIMS-EX: Mechanical Design and Preliminary Testing](https://www.youtube.com/watch?v=cjIVU-O5PHo) (IRIM Lab KOREATECH; public description 2026-02-16).  
**Supplementary:** frame-by-frame reconstruction and discussion notes (project conversation: `docs/conversations/2026-09-17--component-composition.md` 2026-09-19). Figures below mix **stated on-screen / description** values with **engineering interpretation of CAD slides** — treat mechanism details as *best-effort public reconstruction*, not an official IRIM datasheet.

### 3.1 Stated key features

- Unique **N+1-to-2N** actuation mechanism  
- **Single pretension** mechanism shared across all cables  
- High payload-to-weight ratio  
- Arm span **> 1 m**  
- High backdrivability with lightweight distal links  

### 3.2 Headline specifications (as published)

| Parameter | Value |
|-----------|-------|
| Structure | 6-DoF arm + 1-DoF gripper (7 actuators class overall) |
| Mass | 9.7 kg |
| Arm span / reach class | ~1 m (span exceeding 1 m in narrative) |
| Payload | 5 kg continuous capability in entire workspace (as stated) |
| Backdriving force (qualitative) | < 10 N (high backdrivability / compliance narrative) |
| Environment framing | “Tougher environments”; **fully enclosed** cable/mechanism paths |

**Continuous joint torque [N·m]** (from video description):

| Joint | Continuous torque [N·m] |
|-------|-------------------------|
| Shoulder yaw | 93 |
| Shoulder pitch | 72 |
| Elbow | 63 |
| Wrist pitch | 27 |
| Wrist roll | 8 |
| Wrist yaw | 19 |

**Max speed [°/s]:** shoulder & elbow 450; wrist axes 570 (as stated):

| Joint | Max speed [°/s] |
|-------|-----------------|
| Shoulder yaw | 450 |
| Shoulder pitch | 450 |
| Elbow | 450 |
| Wrist pitch | 570 |
| Wrist roll | 570 |
| Wrist yaw | 570 |

### 3.3 Kinematic layout (interpreted)

| Region | DoF (arm proper) | Notes from public CAD / narrative |
|--------|------------------|-----------------------------------|
| Shoulder / base | 2 DoF (base yaw + shoulder pitch class) | Heavy actuators at base fork |
| Elbow | **1 DoF effective**, implemented as **dual-hinge / dual-disk node** with 1:1 synchronization | “Decoupled elbow”; large fold range; smoother cable path than single sharp bend |
| Wrist | **3 DoF** | Differential **bevel-gear** wrist, cable-driven from upper arm |
| Gripper | 1 DoF | Compact actuator in forearm structure (out of scope for detailed notes below) |

**Design intent (public):** proximal mass centering; lightweight distal links; mechanical decoupling so elbow motion does not parasitic-drive the wrist cables.

### 3.4 Actuator placement (proximal mass)

Interpreted from CAD labels and renders (“3 actuators for the elbow and shoulder”, “3 actuators for the wrist”):

| Group | Count | Location (interpretation) |
|-------|-------|---------------------------|
| Base yaw | 1 | Lowest joint / mount flange area |
| Shoulder pitch | 1 | On rotating shoulder fork, at pitch axis |
| Elbow drive | 1 | On opposite side of shoulder fork — **not** at the elbow joint itself; drives elbow via linkage |
| Wrist set | 3 | On **upper-arm link** (between shoulder and elbow), including drive pair + pretension/yaw-related actuator |
| Gripper | 1 | In forearm (not detailed here) |

Forearm remains largely free of wrist motor mass; wrist torque arrives via cables through the elbow.

### 3.5 Elbow: dual-axis node + rigid “bone” linkage

**A. Dual-hinge elbow (1 DoF output)**  
CAD shows two parallel disk/pulley bodies in the elbow region. Interpretation:

- Axis 1: upper arm ↔ intermediate elbow body  
- Axis 2: intermediate body ↔ forearm  
- **1:1 coupling** (gear or equivalent sync) so commanded elbow angle folds both hinges together  

**Why it matters:** larger fold (forearm can lie close along upper arm); wrist cables wrap **two radii** instead of one tight bend → less friction/wear; still commanded as **one** elbow DoF.

**B. Elbow actuation from shoulder base**  
Elbow motor at the **shoulder fork** does not sit in the elbow. Motion is transmitted by a **rigid spatial link / push-pull “bone”** (highlighted pink on CAD; visible on physical half-bent arm and on the passive **leader/master arm**).

- Motor turns a crank/lever at the proximal end  
- Link pushes/pulls the elbow structure → elbow flexion/extension  

**Leader-arm evidence:** the same longitudinal link exists on the passive teaching arm (no wrist motors/cables) → primary role is **elbow angle transmission** to a base-mounted encoder/motor axis, not “cables only.”

**C. Relation to pretension (open but constrained interpretation)**  
Project discussion conclusion:

- Pink link = **primarily elbow drive linkage**  
- Its motion is a natural **kinematic signal** for **passive path-length compensation** of wrist cables when elbow angle changes (slider carriage shifts with elbow geometry)  
- Whether the pink member is *literally* the same part as the “Single Pretension Mechanism” callout, or a **coupled** parallel path, is **not fully settled** from video alone  

### 3.6 Wrist: hybrid N+1-to-2N cable architecture (reconstruction)

Public narrative contrasts:

| Scheme | Motors | Cables (typical story) | Pretension |
|--------|--------|----------------------|------------|
| Classical N+1 | 4 | 4 | Per-cable or complex active control |
| Classical 2N | 3 | 6 | Three independent pretension units |
| **LIMS-EX hybrid N+1-to-2N** | **3** (wrist group) | **5 cables / 3 actuation paths / 1 continuous loop** in reconstruction | **Single pretension** propagates to all wrist cables |

#### 3.6.1 Preferred cable-loop interpretation

For convenience, one complex **continuous** wrist loop can be arbitrarily divided into two or four paths. One **continuous** wrist loops or four independent dead-ended cables at the bevel gears and motor drums:

1. **Upper path (e.g. blue↔red):** one continuous cable from **right** motor drum → right slider → elbow rollers → wrist roller → around **upper** bevel-associated pulley → return left side → **left** motor drum.  
2. **Lower path (e.g. violet↔green):** second continuous cable sharing the same **left/right motor drums** (co-wound or co-anchored) → opposite vertical path through elbow → **lower** bevel pulley → return.

**Decoupled elbow routing:** four elbow roller channels (two sides × upper/lower paths). Cable centerline passes so that **elbow pitch does not change net cable length** (roll about elbow axis) — mechanical decoupling of elbow angle from wrist cable stroke.

**Component count (wrist path, reconstruction):**

| Element | Count (interpreted) |
|---------|---------------------|
| Wrist drive motors (left/right) | 2 |
| Pretension / yaw-related motor | 1 |
| Continuous wrist cable loops | 1 |
| Wrist cable loop attachment points | 4 or 2 |
| Moving sliders | 2 |
| Rollers on sliders | 4 (2 per slider) |
| Elbow rollers (upper-arm side) | 4 |
| Elbow rollers (forearm side) | 4 |
| Wrist pitch axis rollers | 4 |
| Bevel gears | 3 (2 transverse + 1 output) |

#### 3.6.2 Wrist DoF mapping (working model from discussion)

*Subject to revision if official papers differ.*

| Motion | Motor combination (working hypothesis) |
|--------|----------------------------------------|
| **Pitch** (wrist up/down) | Left & right motors **in phase**, same speed — upper vs lower loop differential stroke |
| **Roll** (forearm-axis rotation) | Left & right motors **opposite** phase — upper/lower bevels counter-rotate → output gear spin |
| **Yaw** | Dominated by **third (pretension/slider) actuator** shifting left vs right path lengths so both bevels rotate the same way → frame yaw |
| Combined pitch+roll | Speed/direction mismatch of the two side motors |

Capstan friction wraps and/or local clamps on drums and wrist pulleys are assumed; exact clamp vs pure friction is not proven from frames alone.

#### 3.6.3 Single pretension idea

- One actuation/geometry change at the **slider pair** takes slack out of **both** loops together (“propagates to all cables”).  
- Elbow-angle compensation may be **passive** via linkage geometry (see §3.5C) so wrist motors do not fight elbow-induced length change.  
- This is the core claimed advantage vs three separate pretensioners (2N) or heavy active tension control (classic N+1).

### 3.7 Enclosure and utilities

- Fully enclosed structural shells: cables and gears inside (debris / “tough world” narrative).  
- Hollow distal paths for EE services remain a family theme (see LIMS3 notes); confirm EX specifics when drawings appear.

### 3.8 Test-stand equipment (non-arm, from lab footage)

Interpretive only:

| Item | Likely role |
|------|-------------|
| Large black wheeled/handled unit under table | High-current DC supply and/or battery buffer (regen absorption) |
| Perforated metal DIN supply at table side | AC→DC SMPS (e.g. 24–48 V class rail) |
| Two large red buttons | E-stop (dual-channel / hard kill vs STO-style) |
| Long black block on table | Power distribution / terminal block |

Useful for sint lab practice; not part of arm BOM.

### 3.9 Gaps and caution

- No full official LIMS-EX paper in our index yet — mechanism sections are **video-derived**.  
- Exact motor continuous torque at shaft vs joint table unknown.  
- Pink link = elbow drive **with** pretension coupling is the best current story; pure pretension-only is weaker given the leader arm.  
- Wrist pitch/roll/yaw motor matrix is a **working hypothesis** for S4 study, not certified kinematics.

### 3.10 Relevance to sint (pointer only)

- Strong support for **proximal packs**, **decoupled elbow cable routing**, **light forearm**, **single accessible pretension philosophy** — under **DFAA** (must remain serviceable; no opaque full-arm cable tree as default).  
- Numeric scale remains **reference upper bound**; sint stays on ADR-0003 bands.  
- Feeds ADR-0006 / candidate **S4** study; does **not** by itself amend ADR-0005 S2.

---

## 4. Cable / tendon transmission (family reference)

**Role:** Public LIMS-family practice for remote actuation — **calibration and pattern mining only**.  
**Normative sint media rules:** `docs/tasks/0005-class-requirements-media.md` (belt *or* short cable; no mandatory LIMS diameters or n-wrap).

### Construction patterns

| Topic | LIMS-family practice (as reported in papers / notes) |
|-------|-----------------------------------------------------|
| Construction | Steel cord **7×19** common in LIMS1/2 descriptions |
| Jacket | Nylon-coated wire on elbow/wrist circuits (LIMS1/2) |
| Routing | **No Bowden**; free pulleys/rollers on ball bearings |
| Capstan (shoulder, LIMS1-class) | Example wire **Ø ~1.59 mm**, break ~**1197 N**; drive/driven pulley examples ~30 mm / ~138 mm |
| Elbow & wrist circuits (LIMS1/2) | Example coated wire **Ø ~0.762 mm**, break ~**312 N**; pulley examples ~**16 mm** |
| LIMS3 (notes) | Example elbow-class **~3.2 mm**, distal-class **~1.6 mm** |
| Example circuit lengths (LIMS1) | Capstan ~530 mm; wrist pitch/yaw ~980 mm; wrist roll ~620 mm; elbow ~1030 mm |
| Pulley counts (LIMS1-class examples) | Order-of-magnitude: many idlers per circuit (e.g. ~7–9 on some wrist paths) — package-specific |

### Stiffness, pretension, decoupling

| Topic | Reported practice |
|-------|-------------------|
| Axial stiffness | High; example coated 0.762 mm class cited with large effective k per unit length in papers |
| Pretension rule of thumb | ~**50% of tension at max working load** so peak load takes slack side near zero without derailing |
| Tension amplification | Multi-wrap (block-and-tackle): joint stiffness scales ~**n²**; elbow examples n≈6, wrist bend n≈4 in LIMS1/2 narratives — **not** a sint Phase-1 default |
| Measured joint stiffness (LIMS1-class, papers) | Elbow ~**1410–1440 N·m/rad**; wrist bend hundreds of N·m/rad — scale reference only |
| Decoupling | Wrist cables routed at elbow so flexion does not change net wrist cable length (cross rollers / dual centers) |
| Friction (LIMS3 notes) | Joint friction often **< 1 N·m** class on distal axes — supports current-based contact proxy |

### Joint torque at media (scale only — do not copy into sint BOM)

| Variant | Elbow (indicative) | Wrist (indicative) |
|---------|--------------------|--------------------|
| LIMS1 | Cont. ~11 N·m / peak ~49 N·m class | Cont. ~4 N·m / peak ~12 N·m class |
| LIMS2 peaks (paper) | Peak elbow ~69 N·m class | Roll/pitch peak ~35 N·m; yaw peak ~25 N·m class |
| LIMS-EX continuous (video notes) | Elbow ~63 N·m | Pitch ~27 / yaw ~19 / roll ~8 N·m |

sint distal continuous target remains **~1–5 N·m** (ADR-0003); size media from that margin in C3/CAD, not by ÷10 from the table above.

### LIMS-EX pretension (reconstruction)

Public narrative: hybrid **N+1-to-2N** wrist with **shared pretension** (slider pair). Detail confidence: medium (video). sint may use a **simple accessible take-up** only; full EX clone is out of media musts.

---

## 5. Cross-cutting takeaways for sint (non-normative)

1. **Mass distribution:** multi-kg moving arm with **hundreds of grams** at wrist is achievable with remote cable drive — supports cascade / proximal bias, not copy of 5 kg payload.  
2. **Do not scale motors by payload ratio alone** (e.g. 5 kg → 0.5 kg ⇒ ÷10). Self-weight and \(m g L\) terms dominate; use ADR-0003 N5 + estimated arm mass.  
3. **Sensors:** LIMS3 emphasis on **absolute** sensing at motors and joints is a strong reference for class **E** in component composition.  
4. **Utilities:** hollow distal path for power/data/air aligns with reserved pneumatic / harness classes.  
5. **Acoustics / compliance:** quiet smooth motion and backdrivability are design goals to emulate qualitatively under N6 — not by copying their peak speeds.  
6. **DFAA filter:** long multi-cable packs and single shared pretension need explicit service stories; default sint remains **accessible short belt or short tendon**, not opaque full-arm cable trees.
6b. **Media physics (from family cables, non-normative sizes):** prefer **no Bowden**; free **bearing-mounted** pulleys/rollers; **high axial stiffness / low stretch**; pretension on the order of **~half peak working tension** as a starting rule; **elbow length decoupling** when media cross the elbow. Concrete LIMS diameters, 7×19, and n-wrap stiffness tables stay in §4 — sint musts live in `docs/tasks/0005-class-requirements-media.md`.
7. **LIMS-EX wrist:** hybrid cable loops + single pretension + elbow length decoupling is the concrete mechanism behind the “N+1-to-2N” slogan in public material — primary study object for S4.
8. **Dual-hinge elbow + base-mounted elbow motor via rigid link:** explains fold range and why distal mass stays low; leader arm confirms the link is not “cables only.”
9. **Reconstruction confidence:** high on proximal placement and dual-elbow intent; medium on exact wrist motor→DoF matrix and pretension hardware identity — update when papers or clearer stills appear.

---

## 6. Source index (URL only)

Prefer official lab channels, DOI/IEEE, and stable demo URLs. Do not commit third-party PDFs to git.

| ID | Kind | Topic | URL |
|----|------|--------|-----|
| S1 | Video | LIMS3-AMBIDEX performance | https://www.youtube.com/watch?v=7INPj1hdnyA |
| S2 | Video | LIMS-EX design & preliminary testing | https://www.youtube.com/watch?v=cjIVU-O5PHo |
| S3 | Channel | IRIM LAB KOREATECH | https://www.youtube.com/@IRIMLAB |
| P1 | Paper | LIMS1 tension amplification (IROS 2015) | https://www.cs.cmu.edu/~cga/c/0749.pdf |
| P2 | Paper | LIMS full arm (IEEE T-RO 2017) | https://ieeexplore.ieee.org/document/8016639 |
| P3 | Paper | LIMS2 foldable-objects arm (IROS 2018) | https://ieeexplore.ieee.org/document/8594005 |
| P4 | Paper | Quaternion joint wrist (IROS 2018) | https://ieeexplore.ieee.org/document/8594301 |
| P5 | Paper | AMBIDEX hybrid dynamic / tendon model (Mechatronics 2020) | https://www.sciencedirect.com/science/article/abs/pii/S0957415820300787 |
| PT1 | Patent | Planetary gear actuator (NAVER / KOREATECH) | https://patents.google.com/patent/US20220074468A1/en · granted https://patents.google.com/patent/US11703109B2/en |
| R1 | Recreation | LIMS2-style joint (Thingiverse + demo) | https://www.thingiverse.com/thing:4101834 · https://www.youtube.com/watch?v=RXhtcWz5GBg |
| R2 | Recreation | Printed double rolling joint | https://www.youtube.com/watch?v=6QEgNbaDCjw |

**LIMS-EX:** peer-reviewed write-up of N+1-to-2N / single pretension may lag; structural notes in §3 remain video reconstruction.

*Optional Appendix A:* expanded author/venue metadata for P1–P5, PT1.  
*Optional Appendix B:* recreations only (R1–R2); non-LIMS printable reducers live elsewhere.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-09-17 | Initial file: LIMS3 extract from S1; LIMS-EX specs from S2 description; sint usage notes |
| 2026-09-19 | Expanded §3 LIMS-EX: kinematic/mechanical reconstruction from video frames (wrist loops, decoupled elbow, proximal actuators, pretension/linkage discussion); test-stand notes; explicit uncertainty flags |
| 2026-09-21 | Added § Cable / tendon transmission (family reference); points to sint media requirements doc |

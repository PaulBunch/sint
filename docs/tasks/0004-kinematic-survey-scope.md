<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Task 0004 — Survey scope & selection criteria (K2.1–K2.2)

**Parent:** `docs/tasks/0004-kinematic-scheme.md`  
**Constraints filter:** `docs/tasks/0004-kinematic-constraints.md`  
**Status:** K2.1–K2.3 draft complete

This document defines **what** we survey and **which projects qualify** as sources.
It does not choose sint’s topology (K4–K6).

---

## K2.1 — Survey scope

### Purpose
Build a **curated** set of implemented (or clearly demonstrated) systems to extract:
- kinematic topologies and DoF layouts;
- relocatable / dual-ended operating concepts;
- actuator placement (in-joint vs remote/tendon);
- modularity and service patterns relevant to DFAA;
- quiet BLDC / FOC practice;
- optional: utility pass-through to EE (power, data, **air**).

Bounded review only — not an open-ended web crawl.

### Include (primary interest)

| Class | Why in scope |
|-------|----------------|
| Desktop / light cobot **serial** arms (≈6 DoF, sub-kg–few kg payload) | Closest scale to ADR-0003; joint/module lessons |
| **Modular** arms with repeated joint actuators (integrated drive + encoder) | DFAA-friendly module boundaries; quiet FOC examples |
| **Tendon / cable / belt remote-drive** arms | Mass distribution, proximal motors, distal inertia (LIMS-class lessons) |
| **Dual-ended or relocatable-base** concepts (including space arms as *pattern sources*) | R2 base change, dock walk sequence |
| **Open / maker** arms with public BOM, CAD, or build docs | Service and assembly realism |
| **Printable or hybrid printable** actuator stacks | COTS + FDM path |
| Systems with **EE utility routing** (electrical and, where present, **pneumatic** tool lines) | Possible dock→EE air channel for pneumatic grippers/tools |

### Explicitly secondary (pattern-mining only)

| Class | Role |
|-------|------|
| Large space manipulators (Canadarm2, ERA, …) | Relocatable / dual-role end logic only — **not** full-system analogues |
| Heavy industrial arms, sealed proprietary cobots | Only if a single subsystem idea scales to COTS/DFAA |
| Research platforms with strong papers but weak hardware disclosure | Use cautiously; prefer hardware-visible sources |

### Exclude (out of scope for this survey)

| Class | Reason |
|-------|--------|
| Industrial arms whose main lesson is **>> payload / reach** (tens of kg, multi-metre cells) as the design centre | Violates sint non-goals and BOM class |
| **SCARA / Delta / portal** as *primary* architecture to copy | Poor fit for general 3D assembly + relocatable base story |
| **Legged humanoids** as primary kinematic analogues | Scope creep; locomotion ≠ manipulator scheme |
| Brochure-only products with no usable topology/drive evidence | Cannot support takeaways |
| Pure software / learning stacks with no arm mechanics | Belongs to control/VLA work, not K2 |

### Workspace / scale bias
Prefer lessons compatible with:
- reach order **0.5–0.8 m**, payload **~0.5 kg** continuous;
- consumer FDM segmentation;
- **≥ 2** docks and a desk cluster (printer + table + tool bay).

Larger systems may still contribute **scaled** patterns (see constraints sheet).

### Open design question (track in takeaways, do not require of every source)
**Pneumatic pass-through:** dock → arm → EE air supply for pneumatic end-effectors.  
Survey should note which analogues route air (or other fluid) vs power/data only.  
Not an ADR-0003 hard requirement yet.

---

## K2.2 — Selection criteria for analogues

A project enters the **source list (K2.3)** if it meets **hardware + evidence**, and is useful under **relevance** (full-system or pattern-only).

### A. Hard gates (needed for inclusion)

1. **Reached hardware** — physical system built and shown moving (or major subsystem under test), not concept art alone.  
2. **Public evidence** — enough of: technical page, paper, manual, GitHub/CAD/BOM, and/or video to judge topology and drive approach.  
3. **Stable identity** — clear project/product name and linkable home (repo, lab page, manufacturer page).

### B. Relevance (at least one strong match)

| Axis | Examples of useful signal |
|------|---------------------------|
| Topology | Serial 6-DoF layout, joint arrangement, wrist DoF |
| Relocatable / dual-ended | Dock change, walking arm, symmetric ends |
| Actuation placement | In-joint modules vs proximal motors + transmission |
| Quiet motion | BLDC+FOC, low perceived gear noise under load |
| Modularity / DFAA | Replaceable joints, repeated parts, documented assembly |
| Openness / COTS | Procurable parts, printable structure, published BOM |
| EE utilities | Power/data through wrist; **pneumatic or fluid** tool line if any |

### C. Classification tags (for each source in K2.3)

| Tag | Meaning |
|-----|---------|
| **P — Primary** | Scale/class close enough to study as a system analogue |
| **M — Pattern-only** | Full system fails K1-style gates; mine specific mechanisms/ops only |
| **L — Low priority** | Optional; use if time remains |
| **X — Exclude** | Fails hard gates or scope |

Full-system **P** sources should be plausible under project constraints *in spirit* (desktop/open/modular).  
**M** sources are allowed explicitly for space arms and similar (constraints sheet: pattern mining).

### D. Deprioritize even if popular

- Closed cells with zero transferable mechanical detail  
- Arms relevant only as ROS demos without drive/structure disclosure  
- Humanoid *platforms* where the manipulator is incidental  
- Duplicates of the same pattern already covered by a better-documented source (e.g. second space arm → short note only)

### E. Relation to constraint sheet

- **K1** judges *our* future scheme.  
- **K2.2** judges *whether to read* an external project.  
- A **P** source may still use different numbers (payload, cost); we extract structure, not copy specs.  
- An **M** source may violate COTS/DFAA as a whole; retained ideas must remain scalable under K1 / ADR-0003.

---

## Provisional candidate set (input to K2.3 — not final URLs)

### Primary (deep review)
| Project | Focus |
|---------|--------|
| INNFOS GLUON | Quiet modular serial desktop; integrated actuators |
| PAROL6 (Source Robotics) | Open desktop arm; assembly/docs; **pneumatic aspects** if present |
| Annin Robotics AR4 MK5 | Open(ish) 6-DoF build; modular serial practicality |
| IRIM Lab LIMS2-AMBIDEX | Remote/tendon drive; proximal mass; low distal inertia |
| Elephant myCobot 280 (or equivalent compact serial) | Small serial baseline; joint packaging limits |

### Pattern-only
| Project | Focus |
|---------|--------|
| Canadarm2 | Relocatable base / dual-role ends / walk sequence |
| European Robotic Arm (ERA) | Same family; brief cross-check only |

### Queue / verify before promoting
| Project | Note |
|---------|------|
| Berkeley RLL Blue / Open Arms | Promote to P only if mechanical openness is sufficient |
| Haro380 | Identify exact product + public evidence first |
| 1X EVE | Prefer **exclude** from this kinematic survey (platform ≠ arm scheme) |

---

## K2.3 — Curated source list (kinematics schemes)

**Rule:** URLs only in git. Do not commit PDFs, videos, or full scraped corpora.  
For NotebookLM: upload *selected* public pages / papers the user legally obtains; keep this table as the index.

**Tags:** **P** primary · **M** pattern-only · **L** low priority  
**Pneumatics:** **Y** documented air/vacuum path · **N** electrical only · **?** unknown / not primary lesson

### Primary analogues (deep review)

| # | Project | Tag | Pneum. | Why (kinematics / mechanics) | Priority sources (URL) |
|---|---------|-----|--------|------------------------------|-------------------------|
| 1 | **PAROL6** (Source Robotics) | P | **Y** | Open 6-DoF desktop serial; PETG structure; planetary+belt reductions; **DH + link lengths published**; **2 pneumatic connectors**, tubes routed base→forearm for pneumatic/vacuum gripper | [GitHub README](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm) · [Specs + DH / kinematic diagram](https://source-robotics.github.io/PAROL-docs/page2_2/) · [Peripherals / pneumatics](https://source-robotics.github.io/PAROL-docs/page5/) · [BOM](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm/blob/main/BOM/BOM.md) · [Docs home](https://source-robotics.github.io/PAROL-docs/) |
| 2 | **AR4-MK5** (Annin Robotics) | P | N/? | Mature open DIY 6-DoF; build manual + STL; **standard & modified DH sheets**; spherical-wrist serial layout; practical joint packaging | [MK5 product / downloads hub](https://anninrobotics.com/mk5/) · [Downloads (manual, DH sheets, STL)](https://anninrobotics.com/downloads/) · [Kinematics tutorial page](https://anninrobotics.com/Tutorials/) · [ROS 2 stack (URDF)](https://github.com/Ekumen-OS/ar4) |
| 3 | **INNFOS GLUON** | P | N | Modular serial 6-DoF; repeated **integrated SCA/QDD actuators** in joints; quiet BLDC class; ~0.42 m reach / ~0.5 kg payload order | [Hackster overview](https://www.hackster.io/news/innfos-unveils-a-modular-robotic-arm-driven-by-sca-actuators-e436f9b29823) · [Controller/docs mirror (params)](https://github.com/mintasca/innfos-gluon-controller) · [Skyentific review (arm)](https://www.youtube.com/watch?v=ZlJENPxR7yM) · [Actuator teardown/control](https://www.youtube.com/watch?v=0sgR_RaxYu4) · Optional patent trail: [US20190262989A1](https://patents.google.com/patent/US20190262989A1/en) |
| 4 | **LIMS2-AMBIDEX** (IRIM Lab / KOREATECH) | P/M | N | **7-DoF tendon-driven**; motors concentrated proximal; tension amplification; low distal inertia; wrist rolling-contact mechanism | [IROS 2018 paper (LIMS2)](https://www.researchgate.net/publication/330595465_Development_of_Low-Inertia_High-Stiffness_Manipulator_LIMS2_for_High-Speed_Manipulation_of_Foldable_Objects) · [Mechatronics 2020 hybrid model / AMBIDEX kinematics notes](https://www.sciencedirect.com/science/article/abs/pii/S0957415820300787) · [Basic motion test](https://www.youtube.com/watch?v=Sg1z725Dsd8) · [Mechanical design video](https://www.youtube.com/watch?v=aLaqMreVj9o) · [IRIM Lab channel](https://www.youtube.com/@IRIMLAB) |
| 5 | **myCobot 280 M5** (Elephant Robotics) | P | N | Compact serial 6-DoF baseline; small reach/payload; joint module density limits; consumer product docs | [Specs (M5 2023)](https://www.elephantrobotics.com/en/mycobot-280-m5-2023-specificatons-en/) · [GitBook product parameters](https://docs.elephantrobotics.com/docs/mycobot_280_m5_en/1-ProductInformation/2.ProductParameter/2-ProductParameters.html) |

### Pattern-only (relocatable base / dual-ended interface)

| # | Project | Tag | Pneum. | Why | Priority sources (URL) |
|---|---------|-----|--------|-----|-------------------------|
| 6 | **Canadarm2 (SSRMS)** | M | ? | **Identical LEEs on both ends**; base change via PDGF; latch + power/data grapple — scale down *logic*, not hardware | [CSA — About Canadarm2](https://www.asc-csa.gc.ca/eng/iss/canadarm2/about.asp) · [LEE image / description](https://www.asc-csa.gc.ca/eng/multimedia/search/image/9362) · [StackExchange — LEE operational stages](https://space.stackexchange.com/questions/55753/what-are-the-operational-details-of-the-canadarm-latching-end-effectors) · [NASA LEE context](https://www.nasa.gov/image-article/leading-end-effector-canadarm2-robotic-arm/) |
| 7 | **European Robotic Arm (ERA)** | M | ? | Same family: **symmetric end effectors**, walk between base points; power/data at base points | [ESA ESMATS paper (EES / grapple)](https://www.esmats.eu/amspapers/pastpapers/pdfs/2014/cruijssen.pdf) · [Wikipedia ERA (structure overview)](https://en.wikipedia.org/wiki/European_Robotic_Arm) |

### Explicitly deferred / exclude from this round

| Project | Decision |
|---------|----------|
| Berkeley Blue / Open Arms | Queue — promote only if open mechanical package is as clear as PAROL6/AR4 |
| Haro380 | Queue — identity + public kinematics unclear |
| 1X EVE | **Exclude** from kinematic survey (mobile platform, not arm scheme) |

---

### NotebookLM loading hints (aligned with Gemini)

| Cluster | Feed NotebookLM preferentially | Extract for sint |
|---------|--------------------------------|------------------|
| **PAROL6** | README, BOM, specs/DH page, pneumatics peripherals page | Link lengths, joint reduction types, **air path base→forearm→gripper** |
| **AR4-MK5** | Build manual TOC/chapters on structure, DH calculation sheets, kinematics tutorial | Serial 6-DoF + spherical wrist; modular DIY joint layout |
| **GLUON** | Product/review summaries; actuator-level material; patent abstract if useful | Repeated in-joint actuator module; quiet integrated drive |
| **AMBIDEX / LIMS2** | IROS paper + lab mechanism videos | Proximal motor placement, tendon routing, tension amplification, wrist mechanism |
| **Canadarm2 / ERA** | CSA/ESA pages on LEE/EES and base-change narrative only | Dual-ended latch + power/data; walk sequence — **pattern only** |

**Pneumatic design question (track in K2.5 takeaways):**  
Most desktop serial arms are **electrical-only** through the wrist. **PAROL6** documents onboard pneumatic connectors and tube routing for tool air/vacuum. Space arms show **multi-utility** pass-through at the latch (power/data; sometimes mechanical power). For sint, note whether dock→EE should reserve an **air channel** for pneumatic EE without treating it as mandatory in ADR-0003 yet.

---

### Suggested NotebookLM prompt skeleton (K2.4)

```text
You may use ONLY the uploaded sources. Project constraints are in 0004-kinematic-constraints.md.

For each primary system (PAROL6, AR4-MK5, GLUON, LIMS2-AMBIDEX, myCobot 280):
1) Topology (DoF layout, wrist type, approximate link arrangement)
2) Actuator placement (in-joint vs remote) and transmission type
3) How utilities reach the EE (electrical / pneumatic / none)
4) What is DFAA-friendly vs hostile if an agent had to assemble/service it
5) What scales to: reach 0.5–0.8 m, payload 0.5 kg, ≥2 docks, COTS/FDM

For Canadarm2 and ERA only:
- Extract relocatable-base / dual-ended operating pattern; ignore mass, cost, and flight hardware.

Output a retain/drop table of mechanical patterns for sint (not product recommendations).
```

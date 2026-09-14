<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Task 0004 — Survey scope & selection criteria (K2.1–K2.2)

**Parent:** `docs/tasks/0004-kinematic-and-mechanical-scheme.md`  
**Constraints filter:** `docs/tasks/0004-kinematic-constraints.md`  
**Status:** K2.1–K2.2 draft complete; K2.3 source list next

This document defines **what** we survey and **which projects qualify** as sources.  
It does not list final URLs (K2.3) and does not choose sint’s topology (K4–K6).

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

## Next step (K2.3)

Build a URL-only table: project, tag (P/M/L), links, one-line “why included”, pneumatic Y/N/unknown.  
Do not commit copyrighted full texts or videos into git.

<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C2.3 Elbow path (dual-hinge + rigid link)

**Status:** done  
**Scheme:** S4 primary (dual-hinge 1-DoF elbow, J3 motor on yoke, rigid push-pull link; through-elbow open media to wrist)  
**Note on “cartridge”:** Do **not** require a single-motion pull-out elbow cartridge while wrist cables/belts are live-tensioned. DFAA means **documented, finite service sequence** with removable covers and independent sub-steps — not game-console cartridge semantics.

---

## Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| E-M1 | Elbow output is **one commanded DoF**; mechanism may be **dual-hinge with 1:1 sync** (two revolute stations) | S4 + elbow one-pager |
| E-M2 | J3 motor on **shoulder yoke**; motion to elbow via **rigid push-pull link** (pins/joints accessible) | S4 locked decisions |
| E-M3 | **Through-elbow** wrist media (belt or short cable): path geometry such that elbow flexion does **not** systematically change net media length (decoupling) | S4; avoid parasitic reel |
| E-M4 | **Open service access:** snap/screw **external covers** exposing hinges, sync, rollers/idlers, link ends — without destroying L2 or L3 structure | DFAA / V5 spirit |
| E-M5 | Service is a **finite, ordered procedure** (example pattern below), executable by agent or human with standard tools; procedure documented in repo when CAD exists | Realistic DFAA for tensioned media |
| E-M6 | Bearings at dual-hinge and link pivots are **COTS-replaceable** types; no proprietary sealed elbow-only bearing as sole path | DFAA + BOM |
| E-M7 | Structural loads: elbow + link sized for sint proximal band and 0.5 kg-class tasks (OOM); wrist media side-loads within chosen belt/cable ratings | ADR-0003 |

## Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| E-S1 | Sync (gear or equivalent) inspectable and adjustable without full arm strip | Calibration |
| E-S2 | Rollers/idlers on discrete axles; replace one without reprinting entire elbow shells | Wear |
| E-S3 | Rigid link ends use standard pins/clips; capture features visible | Assembly |
| E-S4 | Covers keyed so wrong orientation is obvious | Agent error reduction |
| E-S5 | After retension, a simple check pose verifies decoupling (elbow sweep ≈ constant wrist media marks) | Bring-up |

## Out / non-goal

| ID | Out |
|----|-----|
| E-O1 | **Single-motion** elbow “cartridge” removal with media still under design tension |
| E-O2 | Opaque multi-wrap tension-amplification inside elbow as default |
| E-O3 | Elbow motor in the hinge (in-joint) as S4 default (that is alternate architecture) |
| E-O4 | Lab-only fixture required for every retension |

---

## Reference service sequence (normative *pattern*, not final work instructions)

Tensioned through-elbow media implies **order**, not one-shot pull-out:

1. Park arm in documented safe pose; power down / brake as required.  
2. **Slack** wrist media at L2 pretension/termination (or designated take-up).  
3. Open **elbow covers**.  
4. Free media from elbow rollers / guides (path still visible).  
5. Disconnect or pin-clear **rigid link** at one end if hinge work requires it.  
6. Service hinges / bearings / sync as needed.  
7. Reverse: route media → set pretension → covers → verification sweep.

Number of steps may grow in CAD; **Must** is that the sequence stays finite, cover-based, and free of hidden one-way assemblies.

---

## Loads & bearings (class level only)

| Element | Class expectation |
|---------|-------------------|
| Dual-hinge pivots | COTS ball or cross-roller as justified by moment; printable shells OK around metal bearings |
| Rigid link | Buckling/tension for J3 torque × geometry; standard rod ends or pinned clevis |
| Elbow rollers | Ball bearings on axles; diameter set in CAD for bend radius of chosen media |

No SKU freeze here.

---

## S2 fallback delta (elbow only)

| S4 | S2 fallback |
|----|-------------|
| Dual-hinge + rigid link from yoke | Single pitch hinge; J3 motor in L2 + **short belt** |
| Through-elbow media mandatory for wrist pack on L2 | No through-elbow wrist path |
| Service sequence centered on covers + slack media | Shorter: belt cover + tensioner on L2/L3 span |

---

## Document control

| Item | Value |
|------|--------|
| Closes | **C2.3** |
| Revises | Earlier “elbow cartridge” language → **cover + sequenced service** |

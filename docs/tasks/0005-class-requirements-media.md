<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C2 — Transmission media (X) & tensioners (T)

**Status:** done (class requirements only)  
**Scheme:** S4 MVP primary; S2 fallback in §6  
**Related:**
- Class IDs **X**, **T** in `docs/tasks/0005-bill-of-classes.md`
- Motors (through-elbow mention): `docs/tasks/0005-class-requirements-motors.md` §C2.2
- Elbow path / service sequence: `docs/tasks/0005-class-requirements-elbow.md`
- LIMS numerical tables (reference only): `docs/references/lims-family-notes.md` § Cable / tendon transmission

**Scope:** What media and tension hardware must *do* for sint — not SKU, not final diameter, not full pulley CAD.  
**Allowed media:** timing **belt** and/or **short cable/tendon** (including coated wire). Equal citizens at requirements level; C3 may prefer one for first article.

---

## 1. Shared principles

1. Media exist to move torque/motion from a motor pack to a joint while keeping **distal structure light** (S4: wrist pack on L2, path through elbow).
2. **Friction and stretch** dominate feel, N6, and control; prefer free-spinning guided paths over sliding conduits.
3. **DFAA:** inspect, slack, retension, replace without destroying link shells.
4. **LIMS wire diameters, n-wrap stiffness, and joint N·m are calibration only** — do not copy as sint musts; do not scale LIMS payload torques by simple ratios into media size.

---

## 2. Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| X-M1 | **No Bowden / flexible conduit** as the default routing method for joint actuation | High friction; LIMS family explicitly avoids; hurts backdrive and efficiency |
| X-M2 | Media run on **free-spinning pulleys/rollers** supported by **COTS bearings** (not plastic-on-plastic journals as default) | Low friction; serviceable |
| X-M3 | Path is **open and inspectable** under removable covers (or equivalent access) along spans that need service | DFAA / V5 |
| X-M4 | Where media **cross the dual-hinge elbow**, geometry keeps **net path length approximately invariant** with elbow angle (decoupling) | S4; avoid parasitic wrist motion |
| X-M5 | **Strength:** working tension capacity adequate for sint distal continuous band **~1–5 N·m** (and any local idler loads) with a clear safety margin; exact Ø and break load chosen in C3/CAD | ADR-0003 distal; E-M7 |
| X-M6 | **Stiffness:** axial stretch under working tension low enough that joint positioning remains usable for assembly tasks (qualitative must; quantify on prototype) | Control / not “rubbery” arm |
| X-M7 | **Tensioners / terminations (T)** provide adjustable pretension without destroying L2/L3 structure; agent- or human-reachable | DFAA; elbow service sequence starts with slack |
| X-M8 | Replacement and retension follow a **finite documented sequence** (open covers → slack → free from guides → service → reverse) | Aligns with elbow doc; realistic for multi-path routing |
| X-M9 | Media choice (belt vs cable) does **not** force a sealed proprietary pack as the only repair path | DFAA |

---

## 3. Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| X-S1 | Prefer **high axial stiffness / low creep** constructions (e.g. steel wire, quality coated wire, or low-stretch timing belt) | LIMS physics without mandating LIMS SKU |
| X-S2 | Use **~half of peak working tension** as a *starting* pretension rule of thumb; tune on hardware so slack side does not derail under peak load | LIMS practice (reference); starting point only |
| X-S3 | Prefer **short runs** and minimal extra sliders/idlers on MVP | BOM, friction, DFAA time |
| X-S4 | **Timing belt** often preferred for first MVP article when DFAA and printability dominate; cable when package or bend radius demands it | Scorecard / open reproducibility |
| X-S5 | Terminations (crimp, clamp, belt lock) are standard or fully documented printable+COTS hybrids | Repeatability |
| X-S6 | Mark left/right or color-code paths when multiple parallel circuits share the elbow | Agent assembly error reduction |
| X-S7 | After setup, **elbow sweep check**: media marks or encoder coupling stay within agreed bound | Bring-up; links to E-S5 |

---

## 4. Out / non-goal

| ID | Out |
|----|-----|
| X-O1 | **Multi-wrap tension amplification** (block-and-tackle, stiffness ∝ n²) as **Phase-1 default** requirement |
| X-O2 | Mandatory LIMS diameters (e.g. 0.762 / 1.59 / 3.2 mm), 7×19-only construction, or nylon jacket as sole allowed jacket |
| X-O3 | Full-arm **opaque** multi-cable tree or LIMS-EX **single pretension clone** as requirement |
| X-O4 | Lab-only tension fixture for every routine retension |
| X-O5 | Copying LIMS continuous/peak joint torques into media sizing via naive payload scaling |

---

## 5. Class split (bill-of-classes)

| ID | Class | In this doc |
|----|--------|-------------|
| **X** | Cascade / through-elbow transmission media | Belt and/or cable/tendon runs, terminations as part of the run |
| **T** | Tensioners, idlers, take-up | Adjustable pretension devices, idler mounts (rollers shared with elbow bearings class) |

Pulleys/rollers: requirements here are functional; **bearing type and exact ⌀** → CAD after media pick in C3.  
Bevel wrist gears: not media; covered under motors/wrist mechanics elsewhere.

---

## 6. S2 fallback delta

| Topic | S4 primary | S2 fallback |
|-------|------------|-------------|
| Through-elbow wrist media | **Must** (with decoupling) | **Not required**; short spans on forearm |
| J3 drive | Rigid link (not media-primary) | Short **belt** L2 → elbow acceptable |
| Pretension / covers | Full sequence | Shorter belt-cover + local tensioner |
| X-M1–X-M3, low stretch, no Bowden | Still apply on remaining spans | Same |

---

## 7. Handoff to C3 / CAD

**C3 (shortlist, URLs only)** should list 2–4 examples each of:

- Timing belt + pulley families (pitch, width bands)  
- Coated or bare cable/tendon families with published break load  
- Simple tensioner hardware (screw take-up, turnbuckle-class, belt tensioner)

Score against X-M5–X-M7 and N7 cost.  
LIMS tables in lims-family-notes = **scale intuition only**.

**CAD** sets: length, bend radius, pulley ⌀, termination detail, cover geometry, exact pretension procedure.

---

## 8. Document control

| Item | Value |
|------|--------|
| Closes | C2 media/tensioner class requirements (supports C2.2 through-elbow + C2.3 service) |
| Does not close | C3 SKU shortlist, pretension mechanism freeze, pulley CAD |
| Does not modify | Motor torque bands; elbow dual-hinge kinematics |

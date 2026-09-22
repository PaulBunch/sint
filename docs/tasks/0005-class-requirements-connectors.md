<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C2.6 — Connectors & mating interfaces (dock, inter-link, EE)

**Status:** done (class requirements; mechanism not frozen)  
**Scheme:** S4, Power Scenario A, asymmetric ends, planar dual-dock walk, reserved air class  
**Related:** ADR-0003, bill-of-classes **K / Q / R / EE / W**, compute (bus/power on arm), media/elbow service (not the same as dock latch)

**Note:** sint-specific. LIMS does not supply a relocatable dual-dock consumer interface; use only general lessons (power enters the arm; distribute on-arm).

---

## 1. Interface roles

| Interface | Mechanical | Power | Data | Air (R) |
|-----------|------------|-------|------|---------|
| **Dock ↔ arm base** | Hard structural latch + alignment | Primary work power (Scenario A) | Field bus + utilities into spine | **Reserve** volume/path only on MVP |
| **Inter-link / module** | Fasteners or small service plugs | 24 V branch | Bus stubs to packs | As routed |
| **Arm EE ↔ tool** | Quick-change structural + align | Tool power (may be subset of bus) | Tool I/O | Reserve same family if possible |
| **Dock station (W)** | Passive or minimal active hardware | Feed to contacts | Feed to contacts | Optional bulkhead later |

**Design bias:** put **cost and complexity on the arm-side base module**, keep **dock stations cheap and easy to replicate**.

---

## 2. Mechanical mating (dock and EE family)

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| K-M1 | Dock mate provides **positive structural connection** able to carry sint walk/cantilever loads at base (aux latch story unchanged: wrist is not the hoist) | Relocatable base |
| K-M2 | Alignment features guide electrical contacts before full load transfer (or staged engage sequence) | Contact life |
| K-M3 | Mate/demate is a **finite, documentable sequence** suitable for agent execution later | DFAA / autonomy |
| K-M4 | **Dock-side hardware stays simple and low-cost** (prefer passive geometry + contacts; minimize actuators on every dock) | Replicable W×N |
| K-M5 | If actuated latch is used, **prefer actuators on the arm base module**, not on each dock | Cost shift to one arm |
| K-M6 | **Power-loss behaviour is explicit:** latched state must not free the arm from dock under loss of 24 V without a defined mechanical backup or normally-secure design | Safety |
| K-M7 | EE interface is a **separate mating face** (may share *design language* with dock later; not required to be identical on MVP) | Asymmetric ends |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| K-S1 | One **alignment/latch family** reusable across ≥2 docks | Walk test |
| K-S2 | Manual override / release accessible for human bring-up | Lab safety |
| K-S3 | Wear parts (pins, pads, catches) replaceable without reprinting whole base | DFAA |
| K-S4 | Electromagnetic latch **allowed as candidate class** only if: (a) arm-side actuation, (b) **secure on power loss** (e.g. mechanical over-center, permanent-magnet bias, or normally engaged lock that needs power to *release*), (c) N6 acceptable | User preference + safety |
| K-S5 | Purely mechanical cam/hook driven by small arm-side actuator is an equal candidate to magnets | Avoid early lock-in |

### Out

| ID | Out |
|----|-----|
| K-O1 | Requiring powered actuators **inside every dock** as the default architecture |
| K-O2 | Relying on friction-only or gravity-only hold for walk loads |
| K-O3 | Free-fall undock on power cut with no documented mechanical retain |
| K-O4 | Freezing a specific latch CAD in C2 |

**Open (CAD / later task, not blocking C2.6):** exact latch kinematics; whether EE reuses dock geometry; sensor for “latched & contacts OK”.

---

## 3. Electrical — power

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| P-M1 | Dock interface carries **24 V class** power adequate for arm continuous duty (budget in C3/C5) | ADR-0003 |
| P-M2 | **On-arm power distribution** after the dock mate (spine/yoke/L2 packs); dock is not a per-driver external wiring farm | Serviceability; user LIMS-EX observation |
| P-M3 | Contacts rated for make/break policy defined in bring-up (hot-plug or power-sequenced — pick in C3/firmware) | Reliability |
| P-M4 | Protection class present (e.g. eFuse/breaker per arm or per branch — family in C3) | Faults |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| P-S1 | **Redundant contact pairs** for high-current rails (two parallel equivalent paths) on the **base–dock** mate to reduce single-pin failure | Robustness |
| P-S2 | Explore **feed from either physical end** only if it does not force full Scenario B dual-ended identity on MVP: e.g. base dock always primary; EE blind-mate power **optional** for tools, not required to energize the whole arm from EE | Scenario A first |
| P-S3 | Arm-side power backplane so adding docks does not multiply unique PSUs per driver | Replication |

### Out

| ID | Out |
|----|-----|
| P-O1 | External thick loom from bench PSU to each motor driver as the **product** architecture |
| P-O2 | Mandatory dual-end full arm energization (true Scenario B) as MVP must |
| P-O3 | Unprotected dead-short path from dock into harness |

**Clarification on “power from either side”:**  
As a **MVP must**, only **dock → arm** is required. Symmetric “either dock or EE can power the whole arm” is a **Should research** item (implies mirrored high-current contacts and policy); do not block C2.6 on it.

---

## 4. Electrical — data

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| D-M1 | Dock mate carries the **joint field bus** (or gateway pair) into the spine per C2.5 | Control |
| D-M2 | Prefer **COTS consumer/industrial connector families** with published pinouts and replaceable cordsets where possible | Repair, N7 |
| D-M3 | Shielding / grounding approach stated at harness design time (not floating logic over long unshielded runs) | EMC |
| D-M4 | Inter-link module plugs support pack swap (yoke / L2 / wrist pack) without rewiring the dock face | DFAA |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| D-S1 | Separate or clearly partitioned pins for EE tool bus vs joint bus if traffic isolation helps | C2.5 B-S2 |
| D-S2 | Blind-mate or guided mate at dock; service pigtails for bench debug | Bring-up |
| D-S3 | Same connector **family** for dock data and EE data if pin count allows — not mandatory identical shells | Inventory |

### Out

| ID | Out |
|----|-----|
| D-O1 | Proprietary connector with no second source and no agent-replaceable lead as sole path |
| D-O2 | Requiring lab-only backplane blades with no cable alternative for MVP |

**C3:** shortlist 2–4 COTS shells (e.g. circular bayonet, industrial rectangular, high-cycle pogo+guide systems) scored on current, pins, cycle life, price — no freeze in C2.

---

## 5. Pneumatic / air (class R)

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| R-M1 | **Reserve** geometric space: channel and/or bulkhead volume through base structure and along the arm envelope for a future air line | Spec utility path |
| R-M2 | MVP **may omit** tubes, fittings, and seals in the first build | Cost / scope |
| R-M3 | Reserved path must not block media covers or latch service access | Conflict avoidance |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| R-S1 | Dock and EE faces leave a **defined blank** for a future air coupler of a chosen size class | Avoid redesign |
| R-S2 | Document bend radius / keep-out so CAD does not close the corridor | Continuity |

### Out

| ID | Out |
|----|-----|
| R-O1 | Full pneumatic implementation as condition of first arm article |
| R-O2 | Air path required for electrical-only smoke test |

---

## 6. Tool-side serviceability (DFAA)

| ID | Requirement |
|----|-------------|
| S-M1 | Primary wear items (contacts, latch hooks, alignment pins) serviceable from **arm base** and **tool** sides with standard tools |
| S-M2 | Dock station: contact cartridges or pads replaceable without replacing the whole dock structure |
| S-M3 | No one-way adhesive-only structural mate for production intent |

---

## 7. S2 fallback

Connector **class** requirements unchanged. Only internal harness lengths change with media layout.

---

## 8. Open points (explicitly not closed by C2.6)

1. Final latch type (magnetic vs cam vs pin-puller).  
2. Whether EE face is mechanically identical to dock face.  
3. Hot-plug vs sequenced power.  
4. Full dual-feed arm power from EE.  
5. Latch presence sensing and interlock logic.

---

## 9. Handoff to C3 / CAD

- C3: COTS connector families (power+data), contact current bands, optional pogo systems.  
- CAD: alignment geometry, latch, keep-outs for air, contact wipe.  
- Firmware: mate state machine (detect → latch → enable power → bus).

---

## Document control

| Item | Value |
|------|--------|
| Closes | **C2.6** |
| Does not close | Latch CAD, connector SKU, pneumatics build |

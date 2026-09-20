<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Task 0005 — C1 Bill of classes

**Status:** done (principles / inventory) — **region map amended for S4 primary 2026-09-20**  
**Schemes:** **S4** = MVP primary (ADR-0005 amended); **S2** = fallback (original C1.2 narrative)  
**Scope:** *what classes exist* and *where* — not SKU freeze. 
**Transmission note:** cascade media include **timing belt (default preference for DFAA)** and **short tendon/cable (allowed alternate)** with agent-accessible tensioners. Full hidden multi-cable LIMS packs remain out of default.

---

## C1.1 Functional classes

| ID | Class | Role on S2 | Notes |
|----|--------|------------|--------|
| **M** | Motors (prime movers) | BLDC preferred (FOC, N6); sized by region torque band | Gimbal/drone / cobot-class; not sealed-only pods as sole path |
| **G** | Gearboxes / reductions | Multiply motor torque to joint continuous band (N5) | **Subtypes to shortlist in C3:** planetary (COTS or printed), cycloidal (often printed), **belt-stage reduction**, strain-wave only if COTS+repair path. Evidence bias: printable **belt reducers** often beat printed cycloidal/planetary on backlash/noise/assembly except **envelope size** |
| **X** | Cascade transmission media | Move torque from motor pack → joint along a span | S4 = through-elbow + optional short J3 rigid-link path (link is **L**-class structure, not only belt); S2 = short belts on J3 and J4–J6 |
| **T** | Tensioners / idlers / terminations | Maintain preload; DFAA service unit | Required wherever X is used |
| **D** | Drivers / FOC power stage | Current control, PWM, brake/fault | SimpleFOC / ODrive-class families in C3 |
| **E** | Encoders / joint feedback | Position (and optionally velocity) for servo loop | Absolute preferred long-term; incremental OK for smoke test |
| **S** | Auxiliary sensors | Limits, temp, optional F/T at EE | Soft requirements |
| **J** | Joint / link MCU | Local FOC loop, bus node, limits | Replaceable “spine” brick |
| **C** | Central compute | Planning, vision/audio, agent stack | Preferred on **upper arm (L2)** for walking layouts (S4 mandatory; S2 should match — doc debt) |
| **P** | Power path | 24 V class distribution, protection | Dock feed + optional proximal transit battery (scenario A) |
| **B** | Battery (optional) | Transit only | Preferred on **upper arm (L2)** for walking layouts (S4 mandatory; S2 should match — doc debt) |
| **H** | Harness / interconnect | Power + data along arm | CAN (or chosen open bus) + 24 V |
| **K** | Connectors | Dock, inter-link, EE, module plugs | Tool-side serviceable |
| **L** | Structural bearings / shafts / fasteners | Revolute support, DFAA hardware | COTS bearings; printed shells separate (CAD task) |
| **Q** | Dock power–data interface | Latch electrical + mechanical contacts | + **reserved air fitting class** (R) |
| **R** | Utility pass-through (air) | Reserved pneumatic/vacuum path | Fitting/tube class only in composition; not full pneumatics design |
| **EE** | End-effector interface | Quick-change mechanical + electrics (+ air reserve) | Tool not frozen here |
| **W** | Workcell docks (×2 MVP) | Coplanar bases for walk test | Electrical class in this task; latch geometry later |

**Explicitly not separate Phase-1 default classes:** spherical multi-DoF mesh joints; industrial harmonic-only stacks; sealed proprietary SCA as only service unit.

---

## C1.2 Map class → region

Regions: **Base-end / dock**, **Proximal (J1–J2, upper-arm span incl. J3 drive)**, **Distal cascade (forearm pack → J4–J6)**, **EE**, **Whole-arm harness**.

| Class | Base-end / dock | Proximal J1–J2 / L2 | Forearm pack → J4–J6 | EE | Notes |
|-------|:---:|:---:|:---:|:---:|--------|
| **M** motors | — | **Yes** (J1, J2; J3 motor in L2) | **Yes** (J4–J6 motors in proximal forearm) | — | No motor mass on light wrist structure if cascade holds |
| **G** reductions | — | **Yes** (high ratio, ~10–25 N·m class) | **Yes** (lower ratio / stage, ~1–5 N·m at joint) | — | G may sit with M in “drive module” |
| **X** belt/tendon | — | **J3 span** (L2 → elbow) | **J4–J6 spans** (short runs) | — | Prefer short runs; accessible covers |
| **T** tensioners | — | **Yes** if X on J3 | **Yes** | — | DFAA-critical |
| **D** drivers | optional shared | **Yes** (with joint MCU or nearby) | **Yes** | — | Often co-packaged with J |
| **E** encoders | — | **Yes** per axis | **Yes** per axis | opt. | On motor and/or joint output (C2) |
| **S** aux sensors | dock sense opt. | temp / limits opt. | limits opt. | F/T opt. | |
| **J** link MCU | — | **Yes** | **Yes** | — | One per joint or per link pack |
| **C** central compute | **Preferred** | allowed on L1 | — | — | Not on wrist |
| **P** power | **Dock feed** | distribution | distribution | low-power EE | 24 V class |
| **B** battery | — | **Optional on L1 / base** | — | **No** | Scenario A transit |
| **H** harness | through dock | through links | through links | to EE | |
| **K** connectors | **Dock** | inter-link / module | module | **EE QC** | |
| **L** bearings etc. | latch structure | every revolute | every revolute | QC | |
| **Q** dock interface | **Yes (×2)** | mates base-end | — | may share pattern w/ EE mechanically later | Aux base latch is **mechanical** follow-up; electrical class here |
| **R** air path | reserved at dock | along arm if used | along arm | at EE | Optional for electrical-only smoke test |
| **EE** interface | — | — | — | **Yes** | |
| **W** dock structures | **Yes** | — | — | — | |

---

## C1.2b S4 region delta (MVP primary)

| Class | S4 placement vs original S2 map |
|-------|----------------------------------|
| **M/G** J3 | Motor on **shoulder yoke**, not “in L2 belt pack only” |
| **M/G** J4–J6 | Pack on **L2 upper arm**, not proximal forearm |
| **X/T** | Through-elbow open media + pretension option; elbow **rigid link** (structural, with **L**) |
| **C, B** | **L2 upper arm** — not dock/base interface block |
| **L** | Dual-hinge elbow cartridge + bevel wrist bearings |
| Forearm column | **Light structure only** (no wrist motor pack) |

Original C1.2 table remains the **S2 fallback** map.

---

## C1.3 MVP smoke test vs Phase 1 complete arm

| Class | MVP smoke test (minimum) | Phase 1 complete arm |
|-------|---------------------------|----------------------|
| **M+G+D+E+J** | **One proximal axis** (e.g. J2-class) **or** one cascaded axis (motor pack + short belt/tendon + joint) | All six axes populated |
| **X+T** | Required **if** smoke axis is cascaded; omit if pure in-joint smoke | On all cascaded spans (J3, J4–J6) |
| **C** | Optional (bench MCU / laptop OK for first spin) | On-arm central compute (R8) |
| **P** | Bench 24 V PSU | Dock-fed 24 V + protection |
| **B** | Omit | Optional proximal transit pack |
| **H+K** | Flying leads OK | Production harness + module connectors |
| **Q+W** | Omit or dummy mount | **≥2** powered docks, planar |
| **R** air | Omit | Reserved fittings/path (even if unused) |
| **EE** | None or fixed dummy mass 0.5 kg | Quick-change interface |
| **S** aux | Omit | Limits; F/T optional |

**Smoke-test definition:** continuously rotate at least one axis under FOC with encoder feedback, log thermal/noise qualitatively, prove **replaceable drive module** boundary; if cascade, prove **retension without destroying the link**.

---

## Implications for later subtasks (not done here)

- **C2:** numeric/service requirements per class (torque, bus, DFAA steps).  
- **C3:** COTS URLs — include belt **and** tendon hardware; compare reduction **families** (belt-stage vs planetary vs cycloidal), citing printable-reducer lessons (belt often wins except size).  
- **C4:** integration matrix + freeze one smoke stack.

---

## Document control

| Item | Value |
|------|--------|
| Closes | C1.1, C1.2, C1.3 |
| Does not close | C2–C7, SKU choice, CAD |

<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C2.5 — Compute, local RT, bus, battery placement

**Status:** done (class requirements)  
**Scheme:** S4 primary — **central compute + optional transit battery on L2 upper arm**, not inside the dock latch/connector block  
**Related:** ADR-0003 (24 V, R8 onboard compute), ADR-0005 amended, S4 stack, motors/sensors reqs, N6 (no default fans)

**LIMS reference (non-normative):** LIMS2 packs motor drivers on shoulder/yaw structure; RT control via Xenomai + ROS managers (~3 ms arm loop); **EtherCAT** to axes + **RS-485** to hand; hollow shaft for power/signal. Fans on dense driver packs are a LIMS packaging choice — **not** adopted as sint default (N6).

---

## 1. Placement

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| C-M1 | **Central / “spine” compute** for the arm lives on **L2 upper arm** (or rigidly co-mounted on the L2 structure), **not** in the dock interface block | S4; walking arm; dock stays latch+connectors |
| C-M2 | **Optional transit battery** (Scenario A), if present, also on **L2** (proximal upper-arm region), not on wrist/EE | S4; mass budget with wrist pack |
| C-M3 | Dock block carries **power/data passthrough** into the arm; it is not the primary SBC mounting volume | Clear mechanical/electrical split |
| C-M4 | Module boundaries support **DFAA**: compute brick and battery pack removable as units with standard fasteners/connectors | DFAA |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| C-S1 | Joint/link **MCUs or FOC boards** co-located with motor packs (yoke for J1–J3 region, L2 for wrist pack) to shorten phase leads | LIMS driver-near-motor pattern without requiring their fan cluster |
| C-S2 | Harness through **J1** (and other axes as needed) minimized to power + bus (+ modest I/O), enabled by proximal electronics | Hollow-bore preference on J1 remains in motors doc |
| C-S3 | Thermal design **passive** (heatsink, copper pour, derating); **no default forced-air fan** on compute or driver packs | N6 |
| C-S4 | Spine compute mass counted inside **L2 mass budget** together with wrist pack and battery | Inertia / J2 load |

### Out

| ID | Out |
|----|-----|
| C-O1 | Main agent computer required only off-arm with **no** on-arm RT capability for joint coordination |
| C-O2 | Battery in wrist or EE as default |
| C-O3 | Forced-air cooling as packaging **requirement** |

---

## 2. Local RT vs central agent (“spine brain”)

sint splits responsibility roughly as:

| Layer | Role | Timing intent (OOM, not hard contract yet) |
|-------|------|-----------------------------------------------|
| **External agent (LLM / planner)** | High-level goals, vision/audio understanding, task plans | Non-RT; episodic commands |
| **On-arm spine compute** | Arm coordination, short-horizon motion, safety stops, optional **small NN** for local coordination / proprioception helpers | Soft-RT to RT; must not depend on cloud round-trip for stable joint motion |
| **Joint / pack MCU + FOC** | Current/velocity/position loops at actuator | Hard RT at driver (kHz-class current loop typical of FOC stacks) |

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| R-M1 | **On-arm spine** can run coordinated multi-axis motion from **buffered high-level setpoints** without continuous LLM token stream | Spec R8; reliability |
| R-M2 | FOC / joint servos remain on **local** hardware (driver MCU); spine does not bit-bang PWM as the only loop | Safety + N6 quality |
| R-M3 | Spine sized at least for: kinematics/trajectory helpers, bus master or gateway role, logging, and **headroom for a small NN** (coordination / filtering — not full VLM on-arm as must) | User “spinal cord” concept |
| R-M4 | Watchdog / fault path: loss of agent link → controlled hold or safe stop using on-arm policies | Walking + contact |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| R-S1 | Control-cycle OOM for arm manager class **~1–5 ms** (LIMS2 ~3 ms is a reference, not a datasheet obligation) | Coordination quality |
| R-S2 | EE/tool loop may be slower OOM (**~10 ms** class) if split | LIMS hand-manager pattern |
| R-S3 | Heavy vision/audio models may run **off-arm**; spine consumes compact results (poses, events) | BOM + thermals on L2 |
| R-S4 | Software stack preference: open, documentable RT path (e.g. Linux PREEMPT_RT / similar + open motor protocols). EtherCAT is **allowed**, not mandatory | Avoid lock-in; see bus |

### Out

| ID | Out |
|----|-----|
| R-O1 | Requiring full Xenomai+EtherCAT+ROS clone of LIMS2 as the only acceptable stack |
| R-O2 | On-arm must run the full multimodal LLM |

---

## 3. Bus & I/O

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| B-M1 | A **single logical field bus or equivalent** for joint modules (command, state, faults) with open or well-documented protocol path | DFAA, multi-axis |
| B-M2 | **24 V class** power distribution with protection (fuse/eFuse/breaker class TBD in C3) from dock into arm | ADR-0003 |
| B-M3 | Path for **EE** tool signals (and reserved air **class** only — not pneumatics design) distinct enough to service | Composition EE / R |
| B-M4 | Physical layer choices must allow **agent-side connector service** (no one-way potting of whole harness) | DFAA |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| B-S1 | Prefer buses with multi-drop + good open-source tooling (examples for C3: **CAN / CAN-FD**, USB not as sole long multi-drop, **EtherCAT** if cost/complexity acceptable) | LIMS used EtherCAT; sint may choose lighter CAN-class for BOM |
| B-S2 | Separate or prioritized channel for EE if EE traffic would jitter joint RT | LIMS RS-485-to-hand pattern as idea |
| B-S3 | Connector/harness plan minimizes conductors across **J1** (power + bus + few lines) | Hollow shaft / reliability |
| B-S4 | Debug port on spine (serial/USB) accessible under cover | Bring-up |

### Out

| ID | Out |
|----|-----|
| B-O1 | Proprietary-only bus with no independent repair/debug story |
| B-O2 | Star of dozens of motor phase cables from dock through every joint as default architecture |

---

## 4. Battery (Scenario A)

### Must

| ID | Requirement | Rationale |
|----|-------------|-----------|
| P-M1 | Work mode **dock-powered** primary | Scenario A |
| P-M2 | If battery fitted: **transit / brownout assist** only; chemistry and Wh sized later in C3; mount on **L2** | S4 |
| P-M3 | Charging policy compatible with dock presence (no requirement for wireless mess on MVP) | Simplicity |

### Should

| ID | Requirement | Rationale |
|----|-------------|-----------|
| P-S1 | Battery pack as DFAA unit (swap/inspect) | Service |
| P-S2 | Voltage class aligns with 24 V bus (buck/boost as needed inside pack module) | Integration |

### Out

| ID | Out |
|----|-----|
| P-O1 | Battery required for all stationary dock work |
| P-O2 | Battery as structural counterweight scheme without electrical role |

---

## 5. Thermal & acoustics

| ID | Requirement |
|----|-------------|
| T-M1 | Continuous compute + driver heat at sint duty must be manageable **without default fans** |
| T-S1 | If a fan is ever introduced, it needs an N6 exception (measured) — same bar as motor drivers |

---

## 6. S2 fallback

Placement of **spine + battery on upper-arm / shoulder link** **stays** (doc debt fix vs old “compute on base”).  
Bus and RT split unchanged. Only motor/media layout changes per motors/media docs.

---

## 7. Handoff to C3

Shortlist examples (URLs only):

- SBC/SoM class for spine (RAM/CPU headroom for small NN; power envelope for passive cooling on L2)  
- Joint MCU / FOC boards already under motors C3  
- CAN-FD or EtherCAT adapter families  
- 24 V pack / dock PSU class (Wh bands later with C5)

---

## Document control

| Item | Value |
|------|--------|
| Closes | **C2.5** |
| Does not close | OS/middleware freeze, exact cycle times, battery Wh, bus chip SKU |
| Explicitly rejects | Fan-cooled driver brick as requirement; compute inside dock latch block |

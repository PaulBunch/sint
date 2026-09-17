<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# sint — Implementation Concepts & Design Options

This document captures specific technical solutions, candidate architectures, and implementation ideas explored during the project. These are not rigid requirements but proposed paths to fulfill the [Project Specification](spec.md).

---

## 1. Kinematics & Actuation

### 1.1. Symmetric Walking Kinematics (Canadarm2/ERA Style)
- **Concept**: A symmetric arm with identical "wrists" and interfaces on both ends.
- **Advantages**: Natural "walking" between docking points; zero-G heritage.
- **Trade-offs**: Requires dual-purpose interfaces (acting as both base and EE mount); increased complexity in power/data routing.

### 1.2. Drive Systems
- **BLDC + FOC (Field Oriented Control)**:
  - **Candidate**: High-pole-count BLDC motors (gimbal / drone class) with controllers such as SimpleFOC or ODrive.
  - **Goal**: Ultra-quiet operation (high PWM carrier, smooth current control) so ambient audio diagnostics remain usable while the arm moves.
- **Gearbox options**:
  - **3D-printed cycloidal**: High reduction in a compact volume; sensitive to print tolerance.
  - **Planetary (incl. helical)**: Easier to print and assemble; typically more backlash than cycloidal/strain-wave.
  - **Strain wave (harmonic)**: High precision; hard to implement as pure COTS / fully printable for MVP.
  - **Belt-stage reduction**: competitive for printed prototypes on backlash/noise/assembly in some comparisons; larger envelope than cycloidal/planetary for the same ratio — relevant to cascade packs.
- **Actuator packaging**:
  - Prefer modular joint modules that an agent can assemble (DFAA).
  - Evaluate both (a) integrated joint actuators and (b) remote/proximal motors with **short** tendon or belt transmission (see §1.4). Prefer inspectable runs over opaque full-arm cable packs.

### 1.3. Reference: quiet modular desktop arm (INNFOS GLUON)
**Why it matters for sint:** demonstrates that a small 6-DoF arm built from a small set of repeated smart actuators can be **smooth and notably quiet**, with a payload class suitable for light assembly rather than industrial handling.

Public / review-oriented figures (order of magnitude, not a procurement commitment):
- Rated payload on the order of **~500 g** (peak claims higher, e.g. ~1 kg in some materials)
- Reach on the order of **~420 mm**
- Built from repeated compact actuators (QDD Lite / SCA-style integrated motor + reducer + driver + encoder)
- Independent reviews often report **good perceived quietness and smoothness**; practical end-effector precision may be closer to **~1–2 mm** under backlash than marketing sub-millimetre claims

**Takeaways for sint numerical targets and design:**
- Payload **without EE** in the **sub-kilogram** class is a credible MVP band for DFAA of printed modules and light tools.
- “Few repeated joint modules + quiet BLDC/FOC stack” is more aligned with agent-maintainable hardware than a zoo of one-off mechanisms.
- Acoustic transparency is achievable in this size class if gear noise and PWM/commutation are controlled — treat **quiet motion under load** as a first-class acceptance test, not an afterthought.

Sources: INNFOS GLUON Kickstarter / product materials; third-party reviews (e.g. Skyentific).

### 1.4. Reference: remote actuation & load distribution (IRIM Lab / LIMS family)
**Why it matters for sint:** the LIMS line (IRIM Lab KOREATECH and related public demos — LIMS2, **LIMS3-AMBIDEX**, **LIMS-EX**) shows how **cable / tendon remote drive** can keep heavy actuators off the distal structure, cut moving inertia, and raise payload-to-distal-mass ratio without putting large gearboxes in every wrist joint.

**Detailed figures and source URLs:** [`docs/references/lims-family-notes.md`](references/lims-family-notes.md) (living extract; extend as new public material appears). This section only keeps **design bias** for agents and ADRs.

**Order-of-magnitude public scale (not sint targets):**

| Item | LIMS-class (public) | sint Phase 1 (normative elsewhere) |
|------|---------------------|-------------------------------------|
| Workspace payload | ~**5 kg** (LIMS3 / LIMS-EX, as stated) | **~0.5 kg** continuous (ADR-0003) |
| Arm span | ~**1 m** | **0.5–0.8 m** reach class |
| Mass below shoulder / moving structure | ~**3.6–4.5 kg** (LIMS2/3) | Much lighter MVP structure expected |
| Distal masses (LIMS3 examples) | Elbow ~268 g, forearm ~949 g, wrist ~174 g | Aim for **light wrist**; exact budget in composition/CAD |
| Shoulder continuous torque | LIMS3 **42 N·m**; LIMS-EX shoulder up to **~72–93 N·m** joint | Proximal band **~10–25 N·m** (ADR-0003) |
| Elbow / wrist continuous (LIMS-EX joints) | Elbow **63 N·m**; wrist **~8–27 N·m** | Distal band **~1–5 N·m** (ADR-0003) |

**Design ideas to evaluate (not adopt blindly):**
- **Motor placement:** concentrate mass at base / proximal links; drive elbow and wrist through **cables or short belts** with inspectable runs.
- **Tension management:** LIMS-EX advertises a **single shared pretension** across cables — elegant, but must pass a **DFAA** service story before imitation; sint default remains **per-span accessible tensioners**.
- **Mass distribution:** sub-kilogram distal segments at ~1 m class arms prove remote drive can unload the tip; useful when justifying cascade (S2) over all in-joint distal motors.
- **Sensing:** LIMS3 stresses **absolute encoders on motors and joints** — strong reference for feedback class selection.
- **Utilities:** large hollow distal path for power / signal / pneumatics aligns with reserved air + harness pass-through.
- **Mechanism detail (LIMS3):** elbow cable diameters cited **3.2 mm / 1.6 mm**; wrist quaternion joint + cable bevel yaw; six wrist cables through elbow “without coupling” (as claimed). Treat as inspiration for routing studies, not a freeze.

**Trade-offs for sint / DFAA / COTS:**
- Long multi-cable trees and lab pretension schemes risk **opaque service** (survey pattern: full LIMS-style pack = not Phase 1 default).
- Prefer **short cascade spans** with **belt (DFAA-friendly) or short tendon** and agent-reachable idlers (placement policy / S2).
- Cable stretch, wear, and calibration become control problems; plan for them if tendons are chosen over belts.
- **Do not size sint motors by linear payload ratio** (e.g. 5 kg → 0.5 kg ⇒ ÷10). Self-weight and \(m g L\) dominate; use ADR-0003 N5 plus estimated arm mass. LIMS joint torques are an **upper reference scale**, not a SKU list.
- Peak speeds of hundreds–1000+ °/s are demonstration-class; sint remains assembly-first and **acoustically quiet** (N6).

**Intent:** keep LIMS as the **primary external orientation** for proximal mass bias and remote transmission *principles*. Normative topology remains the accepted kinematic scheme (S2 cascade serial, asymmetric ends, planar docks). Full tables live only in `lims-family-notes.md`.

**Sources:** see source index in `docs/references/lims-family-notes.md` (LIMS3 demo; LIMS-EX design video); earlier LIMS2 survey notes; related NAVER Labs Ambidex materials where public.

### 1.5. Reference: printable modular BLDC actuators (DIY cobot / open hardware)
**Why it matters for sint:** open, largely 3D-printable BLDC servo actuators align with **100% consumer fabrication** and agent-participatory hardware iteration.

Example class (DIY modular BLDC servo actuator, public build videos / printable kits):
- **5010-class BLDC** motor
- **~4:1 helical planetary** first stage
- Modular stack intended to accept further reduction (e.g. cycloidal stage toward **~100:1** total)
- Fully / mostly 3D-printable structure, open hardware orientation
- Aimed at collaborative / hobby cobot joints rather than sealed industrial actuators

**Takeaways:**
- Printable planetary + optional cycloidal stages are a concrete path under the existing “gearbox options” list.
- Modularity supports DFAA: repeated actuator modules, replaceable printed stages, COTS bearings and fasteners.
- Expect to validate **noise, backlash, thermal behaviour, and service life** empirically; printable gears are a risk item for acoustic transparency and precision.
- Fits the candidate COTS stack (5010-class motors, SimpleFOC-class drivers, magnetic encoders) already sketched in §5.

Source example: public DIY series “3D printable BLDC servo actuator” (5010 + planetary, modular path to higher reduction), e.g. [YouTube build overview](https://www.youtube.com/watch?v=7SZQPEjpaMo).

### 1.6. Synthesis for sint (working design bias)
With kinematic scheme **S2** accepted (cascaded serial 6-DoF) and numerical targets in ADR-0003, prefer concepts that jointly support:
1. **Quiet FOC BLDC motion** (GLUON-class lesson; N6).
2. **Favourable mass distribution** — proximal-heavy, light distal; short **belt or tendon** cascade with agent-accessible tensioning (LIMS-class *principle*, not full cable-tree copy).
3. **Printable or hybrid modular actuators** the agent can assemble and replace (DIY printable actuator lesson; DFAA).
4. **Relocatable base** via **coplanar docks** and scaled walking logic; dual-ended symmetric (Canadarm-class) remains a deferred pattern, not Phase 1 default (§1.1 still relevant as long-term idea).
5. **No naive torque scaling from LIMS payload** — size drives from ADR-0003 bands + arm mass estimates; use LIMS figures only as orientation (`lims-family-notes.md`).

These biases feed component composition (task 0005), joint-module CAD, and later motor/transmission ADRs.

---

## 2. Interface & Docking Mechanisms

### 2.1. Base Anchor Docks (PDGF-style)
- **Mechanical**: Ball-screw latches or wedge-based locking for high rigidity.
- **Electrical**: Spring-loaded pogo pins or co-axial connectors for high-current power and high-speed data (Ethernet/USB3).

### 2.2. Universal Quick-Change EE Interface
- **Magnetic-Mechanical Hybrid**: Using permanent magnets for initial alignment and a motorized latch for rigid locking.
- **Pass-through**: Integrated 8-12 pin connector for I2C/CAN bus and power.

---

## 3. Sensing & Perception

### 3.1. Acoustic Diagnostics
- **Implementation**: MEMS microphone arrays integrated into joints or the wrist.
- **Processing**: Real-time FFT analysis on the LLM/VLA edge compute to detect mechanical anomalies or assembly state (e.g., "click" of a successful latch).

### 3.2. Tactile Sensing
- **Vision-based (GelSight style)**: Using a camera and a soft gel pad for high-resolution tactile maps.
- **Resistive/Capacitive Matrix**: Flexible PCB with pressure-sensitive material for basic force distribution.

---

## 4. Electronics & Compute

### 4.1. Edge Compute
- **Candidates**: NVIDIA Jetson Orin Nano, Raspberry Pi 5, or high-end ESP32/STM32 for real-time motor control.
- **Distribution**: Central "brain" in a link, or distributed micro-controllers per joint communicating via CAN-FD or RS485.

---

## 5. Candidate COTS Stack (Example)
- **Motors**: 2212 - 5208 BLDC Gimbal/Drone motors.
- **Drivers**: SimpleFOC Shield / BGC drivers.
- **Control**: ESP32-S3 or STM32G4.
- **Sensing**: IMU (MPU6050), Magnetic Encoders (AS5600/AS5048A).

---

## References (design inspirations)
- INNFOS GLUON — modular desktop arm / integrated quiet actuators (Kickstarter & reviews)
- IRIM Lab KOREATECH — **LIMS family** (LIMS2 / LIMS3-AMBIDEX / LIMS-EX); detailed notes: [`docs/references/lims-family-notes.md`](references/lims-family-notes.md)
- DIY open-hardware 3D-printed BLDC servo actuators (e.g. 5010 + planetary → higher reduction modular stack)

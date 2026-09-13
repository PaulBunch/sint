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
- **Actuator packaging**:
  - Prefer modular joint modules that an agent can assemble (DFAA).
  - Evaluate both (a) integrated joint actuators and (b) remote/base-mounted motors with tendon or belt transmission (see §1.4).

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

### 1.4. Reference: remote actuation & load distribution (IRIM Lab / LIMS2-AMBIDEX)
**Why it matters for sint:** tendon / cable-driven architectures (IRIM Lab KOREATECH, LIMS / LIMS2-AMBIDEX line) show how to **keep heavy motors off the distal joints**, reduce moving inertia, and improve payload for a given motor size by placing actuators closer to the base/shoulder and transmitting torque via cables, pulleys, and tension-amplification mechanisms.

Design ideas to evaluate (not adopt blindly):
- **Motor placement**: concentrate mass near the base or proximal links; drive elbow/wrist through tendons or equivalent low-mass transmission.
- **Tension amplification**: mechanisms that increase torque/stiffness at the joint without putting a large gearbox in the joint itself.
- **Mass distribution**: lighter distal links improve acceleration, safety in contact, and effective payload at reach.

**Trade-offs for sint / DFAA / COTS:**
- Routing, pretension, wear, and inspection of cables must be agent-serviceable (or replaced by belts/alternative transmissions with clearer DFAA procedures).
- Calibration and stretch/compliance of the transmission become part of the control problem.
- Still compatible with the long-term relocatable / dual-ended interface concept if power/data and mechanical paths are designed deliberately.

**Intent:** use these principles when choosing **where** actuators live along the kinematic chain, especially if numerical targets demand higher payload without simply scaling joint motors at every axis.

Sources: IRIM Lab KOREATECH public demos and design videos (LIMS / LIMS2-AMBIDEX); related NAVER Labs Ambidex materials.

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
Until ADRs freeze choices, prefer concepts that jointly support:
1. **Quiet FOC BLDC motion** (GLUON-class lesson)
2. **Favourable mass distribution** — avoid unnecessary motor mass at every distal joint when tendons/belts/remote drives are workable (LIMS-class lesson)
3. **Printable or hybrid modular actuators** that the agent can assemble and replace (DIY printable actuator lesson)
4. **Symmetric / relocatable kinematics** still as the mobility frame (§1.1)

These biases feed the numerical-characteristics work (payload, torque, noise, BOM) and later motor/transmission ADRs.

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
- IRIM Lab KOREATECH — LIMS / LIMS2-AMBIDEX tendon-driven low-inertia arms
- DIY open-hardware 3D-printed BLDC servo actuators (e.g. 5010 + planetary → higher reduction modular stack)

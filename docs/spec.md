<!--
SPDX-FileCopyrightText: 2026 Paul Bunch

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# sint — Project Specification

**Status:** Stable Draft (Requirements frozen pending implementation concepts)
**Canonical Language:** English  
**License:**  
- **Hardware:** CERN-OHL-S v2 (Strong Copyleft)  
- **Software:** GNU AGPLv3  
- **Documentation:** CC-BY-SA-4.0  

---

## 1. Vision & Goal

### Primary Objective
The primary goal of **sint** (Synthetic Interface System) is to create a physical interface that enables an LLM/VLA agent to autonomously design, assemble, test, and iteratively improve physical systems — **including improved versions of the interface itself**.

**sint** acts as the physical embodiment that closes the feedback loop between digital intelligence and the material world:
```
[ LLM / VLA Agent ] → [ Design & Control ] → [ Physical Interface (sint) ]
             ↑                                        ↓
        [ Multi-Modal Sensing ] ← [ Autonomous Assembly / Test ]
```

The long-term vision is recursive self-improvement of the agent's own physical embodiment using 100% consumer-accessible components and tools.

---

## 2. Core Design Principles

- **Design for Autonomous Assembly (DFAA)**: Every mechanical and electrical subsystem must be engineered so that it can be assembled, disassembled, serviced, and modified by the agent with minimal or zero human intervention.
- **100% Consumer-Grade / COTS Components**: No industrial-only, B2B, or enterprise-restricted parts. Everything must be procurable by a private individual on global consumer marketplaces (e.g., AliExpress, Amazon) and printable on standard consumer FDM printers (build volume 200×200×200 mm).
- **Relocatability (Canadarm / ERA Kinematics)**: The manipulator must not be permanently bound to a single base; it must be able to change its base of operations across docking points in the workspace to dramatically expand its effective reach.
- **Acoustic Transparency & Ultra-Quiet Operation**: Motion must be as silent as possible so that ambient audio sensing remains clean and usable for non-destructive acoustic diagnostics.
- **Multimodal Observability**: Vision, audio, and tactile/force-torque sensing are first-class design primitives required for physical closed-loop feedback.
- **Modularity & Open Standards**: Standardized interfaces for joints, links, docks, end-effectors, compute, and power modules.
- **Self-Reproduction / Bootstrapping**: The system must be capable of participating in the creation of improved versions of itself.
- **Implementation Strategy**: For specific technical solutions and candidate designs, see [Implementation Concepts](implementation-concepts.md).

---

## 3. High-Level Requirements & Strategic Priorities

The following high-level requirements define the core architecture of **sint**. Comments and priorities reflect the engineering evaluation established in project discussions:

| # | Requirement | Priority / Evaluation | Constraints & Functional Target |
|---|---|---|---|
| **R1** | **Manipulator Topology** | **High** | Articulated system (minimum 6 degrees of freedom) suitable for autonomous assembly, reconfiguration, and manipulation tasks within its workspace. |
| **R2** | **Relocatable Base (Mobility)** | **Critical** | The system must be capable of changing its base anchor point autonomously to expand reach without human relocation. |
| **R3** | **Universal Quick-Change EE Interface** | **Critical** | Standardized interface for mechanical locking, power, and data between the manipulator and end-effectors. |
| **R4** | **Tactile Feedback** | **High** | The system shall provide tactile and/or force-torque sensing capability sufficient for closed-loop physical interaction and assembly validation. |
| **R5** | **Multimodal Sensing** | **Critical** | Integration of high-fidelity visual and audio feedback channels. |
| **R6** | **Operation Speed** | **Medium** | Motion performance should be high enough to enable efficient real-world data collection, while remaining subordinate to precision, low vibration, acoustic transparency, and safety. |
| **R7** | **Acoustic Transparency** | **Critical** | Joint and transmission noise must be low enough to allow useful ambient audio sensing and acoustic diagnostics while the manipulator is in motion. |
| **R8** | **Integrated Infrastructure** | **Critical** | All compute, power management, and control electronics must be onboard the mobile unit. |

---

## 4. System Constraints

### 4.1. Technical Constraints
- **Self-Assembly**: All designs must favor parts and connections that the system itself can manipulate or assemble (DFAA).
- **Silent Motion**: Maximum acoustic noise during standard motion must not interfere with the signal-to-noise ratio of onboard audio diagnostic sensors.
- **Power Density**: The system must operate within the power delivery limits of consumer-standard batteries or power supplies reachable via the docking interface.

### 4.2. Economic & Technological Constraints
- **100% COTS (Consumer Off-The-Shelf)**: Use of components restricted to industrial/enterprise channels is prohibited.
- **Standard Fabrication**: Structural parts must be manufacturable using standard desktop FDM/SLA 3D printers or basic manual tools.
- **Budgetary Target**: Initial hardware BOM for a functional node should target a consumer-accessible price point (e.g., < $1000).
- **Communication Standards**: Use of open or widely adopted consumer/maker communication protocols (e.g., USB, WiFi, Ethernet, CAN, I2C).

---

## 5. Non-Goals (Out of Scope for Early MVP)

- Industrial-scale heavy payload capacity or massive reach.
- Certification for industrial human-coexistence safety (e.g., ISO 10218 / ISO/TS 15066 compliance).
- Humanoid or bipedal form factors.
- Fully unguided end-to-end zero-shot autonomy on day one (human oversight remains active during early bootstrapping phases).

---

## 6. Open Questions & Technical Trade-offs

1. **Relocation while holding an EE**: Fine-tuning the protocol for swapping bases (parking EE in a local dock vs dual-interface wrist mechanism).
2. **Optimal Kinematic Topology**: Balancing standard 6-DoF vs 7-DoF or symmetric arm layouts for maximum DFAA capability.
3. **Thermal Management**: Dissipating heat from integrated BLDC FOC drivers and compute onboard compact printed links under continuous load.
4. **Quick-Change Latching Mechanism**: Standardizing a lightweight, 100% COTS-compliant mechanical quick-release interface for power/data/rigid coupling.

---

## 7. Success Criteria (Early Milestones)

- **DFAA Demonstration**: Successful autonomous assembly or significant reconfiguration of at least one major subsystem (e.g. joint module or docking interface) with minimal human intervention.
- **100% COTS Verification**: Entire BOM buildable using off-the-shelf parts and standard 3D printers for < $1000 base node budget.
- **Whisper-Quiet Movement**: Motion noise kept low enough that audio diagnostic sensors detect assembly events cleanly without motor whistle or stepper hum.
- **Base Relocation Demo**: Successfully unlatching from Dock A, walking to Dock B, locking into place, and establishing power/data connectivity.
- **Autonomous Tool Swap**: Changing end-effectors automatically via wrist interface.
- **Closed-Loop LLM Interaction**: An LLM agent reading sensory streams (vision/audio/tactile) and adjusting physical assembly actions in real-time.

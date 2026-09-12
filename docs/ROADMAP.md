<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Roadmap

> Draft — refined iteratively as experience accumulates.

---

## Phase 1: Foundation & Planning

- [x] Discuss optimal first steps for effective project implementation from the start
- [/] Select CAD software (and other required tools) that LLM can interact with independently with minimal human assistance (ADR-0001 adopted, benchmark pending) → [tasks/0001-select-cad-software.md](tasks/0001-select-cad-software.md)
- [ ] Define core numerical characteristics (envelope dimensions, payload without EE, electrical power budget, joint torque/speed targets, acoustic noise limits, target BOM cost)
- [ ] Develop kinematic and mechanical scheme of the interface (topology, DoF layout, relocatable base concept)
- [ ] Define component composition (motors, drivers, gearboxes, sensors, compute, connectors — COTS candidates)
- [ ] Compile preliminary set of assembly operations and list of required external tools (screwdrivers, drivers, soldering equipment, etc.) — directly constrains DFAA design
- [ ] Determine minimum set of mandatory end-effectors required for self-assembly
- [ ] Define workspace layout and docking grid concept
- [ ] Conduct research to identify multiple solution options for each key requirement
- [ ] Make a justified selection of the primary option for each key requirement
- [ ] Formalize ADRs for selected technical directions
- [ ] Evaluate simulation tools (MuJoCo / Isaac Sim / alternatives) for kinematics validation and early controller testing
- [ ] Finalize initial design concept and freeze first milestone scope
- [ ] Refine this roadmap based on research outcomes

---

## Phase 2: Core Design & First Prototypes

- [ ] Complete CAD models for core joint / link modules (DFAA-compliant)
- [ ] Design relocatable docking interface (mechanical + power + data)
- [ ] Design universal quick-change end-effector interface
- [ ] Set up simulation environment (prefer MuJoCo for contact-rich assembly, Isaac Sim if photorealistic vision data is needed)
- [ ] Validate kinematic scheme and basic assembly sequences in simulation before physical prototype
- [ ] Use simulation for controller tuning and synthetic data generation for VLA agent
- [ ] Select COTS BLDC motors + FOC drivers; validate acoustic profile
- [ ] Prototype first joint module and measure noise / torque / backlash / thermal behavior
- [ ] Validate DFAA assembly sequence of the joint module with minimal external tools

---

## Phase 3: Integration & Basic Capabilities

- [ ] Assemble first multi-DoF manipulator node (target ≥6 DoF)
- [ ] Integrate onboard compute, power management, and control electronics
- [ ] Implement multimodal sensing (vision, audio, tactile / force-torque)
- [ ] Demonstrate base relocation (Dock A → Dock B) with power/data reconnect
- [ ] Demonstrate autonomous end-effector swap via wrist interface
- [ ] Close basic sensorimotor loop for simple assembly tasks

---

## Phase 4: Closed-Loop Autonomy & Validation

- [ ] Enable closed-loop LLM / VLA interaction with sensory streams
- [ ] Achieve DFAA demonstration: autonomous assembly / reconfiguration of a major subsystem
- [ ] Verify full BOM remains 100% COTS and under target cost (< $1000)
- [ ] Confirm acoustic transparency: motion noise does not corrupt diagnostic audio
- [ ] Document results, update `docs/current-state.md`, and write next handoff

---

## Phase 5: Recursive Bootstrapping Foundation

- [ ] Enable agent participation in design / fabrication of improved joint or docking modules
- [ ] Establish reliable long-term agent memory and handoff workflows in practice
- [ ] Expand workspace with multiple docks and tool stations
- [ ] Document lessons and prepare the next iteration cycle

---

## Refinement Notes (update as experience grows)

- [ ] Re-evaluate CAD / tool selection after first autonomous design cycle
- [ ] Adjust kinematic topology (6-DoF vs X-DoF / symmetric) based on assembly test results
- [ ] Assess sim-to-real gap after first physical joint module tests
- [ ] Decide whether to invest in Isaac Sim digital twin once multi-DoF node exists
- [ ] Refine thermal management strategy after continuous-load testing
- [ ] Update BOM and budget estimates after first full node build
- [ ] Revisit minimum end-effector set and external tool list after real assembly trials
- [ ] Add new phases for deeper self-reproduction once base autonomy is proven

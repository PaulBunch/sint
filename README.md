<!--
SPDX-FileCopyrightText: 2026 sint project contributors

SPDX-License-Identifier: CC-BY-SA-4.0
-->

# sint — Synthetic Interface System

> An open physical interface enabling LLM and VLA agents to autonomously design, assemble, test, and recursively improve physical hardware.

---

## Overview

**sint** (Synthetic Interface System) is an open hardware and software interface designed to close the feedback loop between digital intelligence and the material world. It provides a physical embodiment capable of autonomous manipulation, tool swapping, and self-reconfiguration using 100% consumer-accessible components and desktop digital fabrication.

```
[ LLM / VLA Agent ] → [ Design & Control ] → [ Physical Interface (sint) ]
          ↑                                        ↓
    [ Multi-Modal Sensing ] ← [ Autonomous Assembly / Test ]
```

### Core Design Principles

- **Design for Autonomous Assembly (DFAA):** Every mechanical and electrical subsystem is engineered for automated assembly, disassembly, and servicing by the agent.
- **100% Consumer-Grade / COTS:** Built exclusively with off-the-shelf components and standard desktop 3D printing. No industrial-only or restricted parts.
- **Relocatable Kinematics:** The manipulator is not bound to a fixed base; it can dock and relocate between anchor points across its workspace to expand reach.
- **Acoustic Transparency:** Ultra-quiet motion designed to keep ambient audio channels clean for acoustic diagnostics during assembly tasks.
- **Multimodal Observability:** First-class integration of vision, audio, and tactile/force feedback for real-world closed-loop physical interaction.
- **Recursive Bootstrapping:** Engineered to participate in the physical manufacturing and evolution of its own hardware and tooling.

---

## Project Status

> **Current Phase:** Bootstrapping & Architectural Specification

The project is currently defining core requirements, candidate technical concepts, and autonomous memory interfaces. Physical CAD models and firmware implementations are in the concept phase.

- **Single Source of Truth (SSOT):** See [`docs/current-state.md`](docs/current-state.md) for live system status.
- **Canonical Specification:** See [`docs/spec.md`](docs/spec.md) for requirements and operational goals.
- **Roadmap & Phases:** See [`docs/ROADMAP.md`](docs/ROADMAP.md) for the high-level phased plan.
- **Implementation Concepts:** Candidate designs (kinematics, motor drives, docking) are tracked in [`docs/implementation-concepts.md`](docs/implementation-concepts.md).

---

## Documentation Guide

| Document | Purpose |
| :--- | :--- |
| **[`docs/spec.md`](docs/spec.md)** | Canonical project requirements, system constraints, and success criteria. |
| **[`docs/implementation-concepts.md`](docs/implementation-concepts.md)** | Technical candidates and trade-off analysis (motors, gearboxes, docking). |
| **[`docs/current-state.md`](docs/current-state.md)** | Single Source of Truth (SSOT) for current hardware/software progress. |
| **[`docs/long-term-memory.md`](docs/long-term-memory.md)** | Architecture for long-term LLM agent memory and session handoffs. |
| **[`docs/naming.md`](docs/naming.md)** | Project etymology, namespace conventions, and CLI standards. |
| **[`docs/ROADMAP.md`](docs/ROADMAP.md)** | High-level phased plan (Phase 1–5) and key milestones. Updated as experience accumulates. |

---

## Autonomous Agent Workflow

`sint` employs a structured external memory and context-bridging architecture optimized for autonomous agent development:

1. **State Persistence:** Real-time state changes are logged in [`docs/current-state.md`](docs/current-state.md).
2. **Context Bridges:** Multi-session continuity is maintained via [`docs/handoff-latest.md`](docs/handoff-latest.md).
3. **Architectural Decisions:** Design trade-offs are formally captured as ADRs in [`docs/decisions/`](docs/decisions/).

For complete operational rules, refer to [`docs/long-term-memory.md`](docs/long-term-memory.md).

---

## License

This project utilizes a multi-license structure:

| Component | License | SPDX Identifier |
| :--- | :--- | :--- |
| **Hardware** (CAD, PCB, mechanical designs) | CERN Open Hardware Licence Version 2 - Strongly Reciprocal | `CERN-OHL-S-2.0` |
| **Software & Firmware** | GNU Affero General Public License v3.0 or later | `AGPL-3.0-or-later` |
| **Documentation** | Creative Commons Attribution-ShareAlike 4.0 International | `CC-BY-SA-4.0` |

Full license texts are available in the [`LICENSES/`](LICENSES/) directory.

<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# ADR-0004: Kinematic Survey — Patterns Retained for Scheme Design

- **Status:** Accepted (hard gate before candidate schemes K3–K5)
- **Date:** 2026-09-15
- **Deciders:** Project maintainers / agents working on Phase 1 kinematics
- **Related:**
  - `docs/spec.md` (R1–R3, R7–R8, DFAA, relocatable base)
  - `docs/decisions/0003-core-numerical-characteristics.md`
  - `docs/tasks/0004-kinematic-and-mechanical-scheme.md`
  - `docs/tasks/0004-kinematic-constraints.md`
  - `docs/tasks/0004-kinematic-survey-scope.md`
  - `docs/conversations/2026-09-14--kinematic-survey-notebooklm.md`
  - `docs/implementation-concepts.md` (§1)

## Context

Task 0004 requires a curated survey of implemented analogues before proposing kinematic schemes. Constraints are fixed in `0004-kinematic-constraints.md` and ADR-0003. Survey scope and source list are in `0004-kinematic-survey-scope.md`. Structured review (K2.4) was run via NotebookLM against that bounded source set; discussion and intermediate tables live in the survey conversation.

This ADR freezes **which mechanical patterns may enter scheme design (K3–K5)** and which are dropped. It does **not** select the final topology, joint count, or dock hardware.

## Decision

1. Adopt the **takeaways table** below as the authoritative retain / pattern-only / drop list for Phase 1 kinematic synthesis.
2. Candidate schemes (K4) must be composed only from **Retain** and **Pattern-only** rows; **Drop** rows must not re-enter without a superseding ADR.
3. Survey conversation is the evidence record for K2.4–K2.6; this ADR is the normative gate.

### Takeaways table (pattern → pros/cons → decision)

| Mechanical pattern | Source analogues | Pros / cons for sint | Decision |
| :--- | :--- | :--- | :--- |
| **6-DoF serial kinematics with spherical (or industrial-style) wrist** | PAROL6, AR4-MK5 | **+** Clear kinematics; published DH-class data; FDM-segmentable links within ~175–180 mm print envelope. **–** In-joint steppers raise distal/proximal inertia at 0.5–0.8 m reach. | **Retain** — default kinematic family for geometric synthesis |
| **Cascaded / proximal mass bias** (heavy drives shifted toward base; light distal) | LIMS2-AMBIDEX (full remote); hybrid cascade discussed in survey conversation | **+** Improves tip inertia and fine assembly; supports N5 distal band. **–** Full multi-cable shoulder pack fails agent serviceability (DFAA V5) unless transmissions are accessible. | **Pattern-only** — prefer **cascaded** placement (elbow drives in upper arm, wrist drives in forearm) with **externally accessible** belts/tendons; reject opaque full-tendon packs as default |
| **Modular quiet BLDC + FOC + bus (e.g. CAN) joint modules** | INNFOS GLUON (SCA/QDD class) | **+** Acoustic path aligned with N6; integrated drive + through-joint power/data. **–** Sealed proprietary modules break COTS/DFAA repair (V3). | **Pattern-only** — copy quiet FOC + modular *boundary*; implement with open/printable or COTS-rebuildable actuators |
| **Internal utility routing including pneumatic channel (base/dock → forearm → EE)** | PAROL6 | **+** Pneumatic/vacuum EE without dangling external hoses. **–** Needs rotary feed-through or managed flex in hollow joints. | **Retain / reserve** — reserve air path in interface and link design; not yet a hard numeric requirement in ADR-0003 |
| **Relocatable base / walking-arm logic** (undock → move → dock; power/data via anchored end) | Canadarm2, ERA | **+** Satisfies R2 with ≥2 docks. **–** Flight-symmetric dual LEE is heavy/costly if copied literally. | **Pattern-only** — keep base-change sequence and dual-role end *logic*; scale interfaces to consumer docks (scaled logic; Phase-1 load cases are planar) |
| **Closed micro-servo integrated arm as whole product** | myCobot 280 | **+** Compact packaging. **–** Reach (~0.28 m) and payload (~0.25 kg) miss N2/N3; non-serviceable internals (V3, V8). | **Drop** |

### Explicit non-decisions (deferred to K3–K6)

- Final choice among pure in-joint serial vs cascaded hybrid vs dual-ended symmetric layout  
- Power scenario A vs B (ADR-0003)  
- Dual-latch dock vs stronger symmetric ends for walk loads  
- Distributed link MCU policy details beyond “low-level control may be local”

## Options considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Skip formal gate; draw schemes from ad-hoc memory | Rejected | Survey effort would not bind later design |
| Full system clone of PAROL6 or GLUON | Rejected | Numbers, quietness, relocatable base, and DFAA need composition of patterns |
| Adopt full LIMS-style all-tendon arm | Rejected as default | DFAA V5 (agent cannot maintain hidden tension network) |
| Keep myCobot as primary analogue | Rejected | Fails N2/N3 and serviceability |

## Consequences

### Positive
- K3–K5 have a fixed pattern vocabulary  
- DFAA vetoes from the constraint sheet remain enforceable  
- Pneumatic pass-through and relocatable logic stay visible without over-constraining MVP  

### Risks
- Cascaded drives still need a credible **dock walk** story (wrist may be too weak as sole cantilever support — dual-latch or stronger base-end remains open)  
- Reserved pneumatics add seal/routing complexity  
- Quiet FOC modules must be reinvented under COTS/FDM, not purchased as sealed SCA  

### Neutral
- Does not change ADR-0003 numeric targets  
- Does not replace implementation-concepts references; it prioritizes them for scheme work  

## Implementation notes

1. Mark task 0004 items **K2.4, K2.5, K2.6** complete; link this ADR and the survey conversation.  
2. Proceed to **K3** (placement policy) using: serial 6-DoF family + cascaded mass bias + quiet FOC modules + reserved air path + scaled walking-arm logic.  
3. Any scheme that reintroduces a **Drop** pattern or full opaque tendon network requires an ADR amendment.  
4. After first joint/dock prototype, revisit cascade vs in-joint and dock walk mechanics.

## Survey record (K2.6)

| Item | Location |
|------|----------|
| Prompts, limits, NotebookLM Q&A | `docs/conversations/2026-09-14--kinematic-survey-notebooklm.md` |
| Scope, criteria, URL index | `docs/tasks/0004-kinematic-survey-scope.md` |
| Constraint filter | `docs/tasks/0004-kinematic-constraints.md` |
| Normative pattern gate | **This ADR** |

## References

- ADR-0003 — working numerical characteristics  
- Spec R1–R3, R7–R8; DFAA principles  
- Survey conversation 2026-09-14/15 (structured review + takeaways draft)

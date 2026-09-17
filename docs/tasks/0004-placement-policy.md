<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Task 0004 — Placement policy (motors & electronics)

**Status:** accepted (principles only — Phase 1)  
**Parent:** `docs/tasks/0004-kinematic-scheme.md`  
**Related:**
- `docs/decisions/0003-core-numerical-characteristics.md`
- `docs/decisions/0004-kinematic-survey-patterns.md`
- `docs/tasks/0004-kinematic-constraints.md`
- `docs/tasks/0004-kinematic-survey-scope.md`
- `docs/conversations/2026-09-14--kinematic-survey-notebooklm.md`
- `docs/implementation-concepts.md` (§1, §4)

**Scope:** principles for where actuators, transmissions, compute, and power live on the manipulator.  
**Out of scope:** final topology stick diagrams (K4), SKU freeze, PCB layout, spherical-gear multi-DoF joints.

---

## 1. Goals

1. Meet ADR-0003 bands (payload, torque, reach, acoustics, BOM) without industrial-only hardware.
2. Keep **DFAA**: the agent can replace drives, tensioners, and compute bricks without destroying the arm.
3. Prefer **light distal mass** for assembly precision and safe contact.
4. Stay compatible with relocatable base (R2) and power scenarios A (default) / B (alternate).

---

## 2. Motor placement (K3.1)

| Option | Role in sint |
|--------|----------------|
| **In-joint module** | Allowed on **proximal** axes (base / shoulder) and as a local fallback. Clear replaceable boundary; adds mass at the axis. |
| **Cascaded proximal (default)** | Elbow drives mounted in the **upper-arm link**; wrist drives mounted in the **forearm**, near the elbow. Motion to the joint via **short belt or tendon in an agent-accessible channel**. |
| **Full proximal pack (LIMS-style all-tendon)** | **Not default.** Opaque multi-cable routing fails maintainability (constraint veto V5) unless every tensioner is agent-serviceable — which this policy does not assume for MVP. |

**Policy**

- Default architecture: **hybrid cascade** — heavy torque near the base of each transmission span; end-effector and distal links stay light.
- Pure in-joint is acceptable where a quiet, replaceable FOC module fits N5/N6 and DFAA.
- Do not adopt sealed proprietary integrated actuators as the only service unit (ADR-0004: pattern-only from GLUON).

---

## 3. Mass distribution bias (K3.2)

Aligned with ADR-0003 **N3 / N5**:

| Region | Intent |
|--------|--------|
| Proximal (base / shoulder) | Carry continuous torque order **~10–25 N·m**; host heavier motors, reduction, optional transit battery |
| Mid (elbow span) | Intermediate; prefer drives in the upper arm rather than on the elbow axis when cascade is used |
| Distal (wrist / EE) | Continuous torque order **~1–5 N·m**; minimise mass for fine assembly and tip dynamics |

**Rules**

- Bias: **proximal-heavy, light distal**.
- A weak wrist must **not** be the sole structural support for a full-arm cantilever during dock-to-dock walk unless a separate scheme (stronger base-end, dual-latch dock, or temporary support) is explicitly chosen in K4–K5. Distal joints are not sized for climb/pull-up re-basing in Phase 1; walk loads use base-end / aux latch / dual-ended proximal ends per scheme.
- Link lengths remain constrained by printable envelope (**≤ ~175–180 mm** major pieces) and reach **0.5–0.8 m**.

---

## 4. Compute and power electronics (K3.3)

| Zone | Responsibility |
|------|----------------|
| **Joint / link MCU** (“local spine”, simplified) | Motor drive (FOC), encoder, joint limits, local servo loop, basic fault handling |
| **Central compute** | On the mobile unit, preferably on a **proximal** link or base-end: planning, vision/audio fusion, agent / VLA interface |
| **Not Phase 1 requirement** | Per-link learned “sleep” weight adaptation or full local world models |

**Rules**

- Satisfy **R8**: compute and power management live on the mobile unit, not only in fixed infrastructure.
- Inter-link bus: open maker-friendly protocol (e.g. **CAN** / CAN-FD class).
- Central brain does not hard-real-time commutate every joint; local MCUs do.
- Each link compute unit should be a **replaceable brick** (see §6).

---

## 5. Power architecture interaction (K3.4)

From ADR-0003:

| Scenario | Placement implications |
|----------|-------------------------|
| **A — default** | Work powered from **dock**. Optional **swappable battery on a proximal segment** for transit between docks. Ends **need not be mirrored**; base-end may carry power/data density that the EE-end does not. |
| **B — alternate** | Dock-only power with dual-dock handoff; pushes toward **mirrored** universal ends. Adopt only if K4–K5 select a strongly symmetric dual-ended scheme. |

**Rules**

- Do not place transit battery mass on the wrist or EE.
- Utility routing may reserve **power + data + optional air** along the arm (ADR-0004: pneumatics retain/reserve from PAROL6 pattern).
- Dock interface design must match the chosen scenario; do not assume Scenario B wiring if the arm is asymmetric under A.

---

## 6. DFAA implications (K3.5)

The agent must be able to replace or service at least:

| Unit | Expectation |
|------|-------------|
| **Joint / drive module** | Remove and refit without scrapping the entire link |
| **Belt/tendon tensioner or idler** (if cascade used) | Accessible from outside; no full-arm teardown for retension |
| **Link compute brick** | Connectorised module on the link |
| **Dock latch / power-data insert** | Serviceable as its own unit |
| **End-effector** | Quick-change per R3 |

**Forbidden as default**

- Hidden cable packs that only a human with factory jigs can tension or re-route (V5).
- Single non-segmentable structure larger than the print envelope with no DFAA join plan (V2).
- Reliance on industrial-only sealed actuators with no consumer repair path (V3).

---

## 7. Explicitly deferred

| Topic | Decision |
|-------|----------|
| **Spherical gear / ABENICS-class multi-DoF mesh joints** | **Out of Phase 1 default.** Printable prototypes show interesting compactness but weak stiffness, backlash, wear, and DFAA cost relative to stacked revolute joints. May be revisited as research for a light wrist only after serial/cascade MVP. |
| Switchable multi-direction single-motor transmissions | Research only; not default vs two simple actuators |
| Final dock walk mechanism (dual-latch vs strong symmetric ends) | Decided in K4–K5 against this policy’s mass and torque bias |

---

## 8. Summary policy (one paragraph)

Phase 1 sint prefers a **serial arm family** with **cascaded actuator placement** (heavy drives proximal on each span, light wrist/EE), **quiet FOC-class modules** that the agent can replace, **distributed joint/link MCUs** plus **proximal central compute**, **power scenario A** by default (dock work, optional proximal battery, ends may be asymmetric), and **agent-accessible** tension and fasteners. Full LIMS-style hidden tendon networks, proprietary sealed joint pods as the only path, spherical-gear primary joints, and distal battery mass are out of default scope.

---

## 9. Handoff to K4

Candidate schemes must state:

1. Which axes are in-joint vs cascaded  
2. Where central compute and optional battery sit  
3. How dock walk loads are carried (without overloading a weak wrist by accident)  
4. How §6 replaceable units map onto the stick diagram  

---

## Document control

| Item | Value |
|------|--------|
| Closes task items | K3.1–K3.5 |
| Normative inputs | ADR-0003, ADR-0004, constraint sheet |
| Next | K4 candidate schemes |

<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# ADR-0005: Phase 1 Kinematic Scheme

- **Status:** Accepted — **Amended 2026-09-20** (S4 MVP primary; S2 fallback)
- **Date:** 2026-09-17
- **Deciders:** Project maintainers / agents working on Phase 1
- **Refines:** ADR-0003 (numerical targets), ADR-0004 (survey patterns), `docs/tasks/0004-placement-policy.md`
- **Related:**
  - `docs/spec.md` (R1–R3, R7–R8, DFAA)
  - `docs/tasks/0004-kinematic-scheme.md`
  - `docs/tasks/0004-kinematic-constraints.md`
  - `docs/tasks/0004-candidate-schemes.md`
  - `docs/tasks/0004-scheme-downselect.md`
  - `docs/conversations/2026-09-14--kinematic-survey-notebooklm.md`

## Context

Phase 1 needs a frozen **kinematic family and mechanical placement concept** before joint modules, docks, and COTS selection diverge.

Prior work:

| Artifact | Role |
|----------|------|
| ADR-0003 | Reach, payload, torque bands, power A/B, BOM, acoustics |
| ADR-0004 | Retained / pattern-only / dropped mechanical patterns |
| Placement policy | Cascade default, distributed MCU, power A, DFAA replaceables |
| K4 candidate schemes | S1 in-joint, S2 cascade, S3 dual-ended symmetric |
| K5 down-select | Comparative scorecard + illustrative order-of-magnitude checks |

MVP workspace is a **coplanar** desk cluster (A1-mini-class printer, table buffer, tool bay) with **≥ 2 docks**. Non-coplanar climb and wrist-as-hoist loads are out of Phase 1 selection.

## Decision

### 1. Primary scheme: **S2 — serial 6-DoF, cascaded mass bias**

| Aspect | Choice |
|--------|--------|
| Topology | Serial articulated arm, **6 DoF** |
| Axis roles (logical) | J1 base yaw · J2 shoulder pitch · J3 elbow pitch · J4 forearm roll · J5 wrist pitch · J6 wrist roll (exact DH to be fixed in kinematics model; roles may be refined without changing family) |
| Actuator placement | **Cascade (default policy):** J1/J2 in-joint or at base of span; **J3 drive in upper-arm link**; **J4–J6 drives in forearm** (proximal end of forearm span); short **agent-accessible** belt/tendon channels to distal axes |
| Mass bias | Proximal-heavy, **light wrist/EE** |
| Ends | **Asymmetric:** structural + power/data **base/dock end**; light **EE quick-change** end (+ reserved air path) |
| Power | **Scenario A** (dock-powered work; optional **proximal** transit battery) |
| Compute | Per-joint or per-link MCU (local servo/FOC) + **proximal central** compute (R8) |
| Utilities | Power + data through arm; **reserve** internal pneumatic route dock→EE (not a numeric hard requirement yet) |

### 2. Relocatable base (R2) — Phase 1 concept

- **≥ 2 docks**, **one work plane** (table/rail).
- Single-step center spacing must fit **dual-dock kinematic span** (order **~0.5–0.6 m** for S2-class reach; refine with joint limits later).
- Walk loads for S2 **must not** use the light wrist as the sole cantilever support. Use **base-segment auxiliary latch / dual-contact overlap** so bending moments go to proximal structure and latches.
- Wall/ceiling/non-coplanar re-basing and pull-up/climb load cases are **deferred** (future ADR / test plan).

### 3. Fallback and deferred schemes

| Scheme | Status |
|--------|--------|
| **S1** (serial 6-DoF, mostly in-joint modular FOC) | **Fallback** if cascade belts fail DFAA, N6, or reliability in prototype |
| **S3** (7-DoF dual-ended symmetric, Scenario B) | **Deferred** — strong R2 purity; higher mass/BOM/complexity risk under ADR-0003 |

### 4. Explicit non-choices (still open)

- Final motor/gearbox SKUs and reduction ratios  
- Exact DH parameters and link CG  
- Detailed dock latch geometry  
- Whether later evolution adopts partial S3-like symmetry  
- Spherical-gear multi-DoF joints (remain out of Phase 1 default)

## Amendment 2026-09-20 — MVP primary scheme role (S4 / S2)

**Context:** Task 0005 C1b (LIMS-class parallel branch), scorecard `docs/tasks/0005-s2-vs-s4-scorecard.md`, gate `docs/tasks/0005-s2-s4-gate.md`, ADR-0006.

**Amendment (does not delete §§1–4 above):**

1. **MVP implementation primary** is scheme **S4** (LIMS-inspired serial 6-DoF) as specified in `docs/tasks/0005-candidate-scheme-s4.md`: shoulder yoke with J2/J3 motors, upper-arm (L2) compute and optional battery and wrist pack, dual-hinge elbow with rigid link drive, light forearm, bevel 3-DoF wrist, open through-elbow transmission, Power Scenario A, asymmetric ends, planar relocatable walk with base aux-latch.

2. Scheme **S2** (this ADR’s original primary) remains the **documented cascade baseline** and the **explicit fallback** if gate triggers in `docs/tasks/0005-s2-s4-gate.md` are met.

3. **S1** remains last-resort fallback for distal actuation if both through-elbow and S2-style cascade fail DFAA or N6.

4. **S3** remains deferred.

5. **Numeric targets** stay ADR-0003. **DFAA and open serviceability** remain mandatory; opaque full-arm cable packs remain rejected as default.

6. **Aspirations** (non-metric): move toward **LIMS-class motion characteristics** and robust **relocatable / multi-dock walking** behaviour under consumer fabrication constraints — without claiming parity with any external product.

7. Component composition and first hardware articles **shall cite S4** unless a recorded fallback to S2/S1 has been declared.

**Rationale:** Prefer addressing classic serial-arm limitations (distal mass, limited fold around docks) on the MVP path, with a pre-declared retreat to S2, rather than optimizing only for short-term mechanical simplicity.

## Options considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| S2 cascade serial | **Selected primary** | Best fit to placement policy, N3/N5 inertia, ADR-0004 cascade pattern, Power A, DFAA-accessible transmissions |
| S1 in-joint serial | Fallback | Simpler mechanics; higher distal mass |
| S3 dual-ended symmetric | Deferred | Native walk; risks mass, dual proximal packs, BOM under N7 |
| Full LIMS-style hidden tendon pack | Rejected | DFAA V5 |
| Planar MVP only vs 3D dock climb | Planar MVP | Matches stated workspace; climb would force distal torque/BOM against policy |

Scorecard totals in the down-select note are **comparative judgments**, not laboratory measurements. Order-of-magnitude masses/torques there are **illustrative** and must be revalidated on hardware.

## Consequences

### Positive

- Single default architecture for agents and humans  
- Aligns kinematics work with ADR-0003/0004 and placement policy  
- Clear relocatable story without over-claiming wrist strength  
- Fallback path (S1) without restarting survey  

### Risks / open issues

1. **Belt/tendon N6 and wear** — open channels help DFAA but need damping and life tests  
2. **Auxiliary base latch** — extra dock/arm interface complexity; must stay agent-serviceable  
3. **Illustrative mass model** — real link/actuator masses may shift N5 margins  
4. **Pneumatic reserve** — seals/rotary feed-through still undesigned  
5. **S3 deferred** — long-term R2 “pure walk” may reopen dual-ended design after MVP  

### Neutral

- Does not freeze COTS list (next ROADMAP item: component composition)  
- Does not replace detailed URDF/DH delivery  

## Implementation notes

1. Mark task **0004** K6 complete; ROADMAP “kinematic scheme…” → done via this ADR.  
2. Update `docs/current-state.md` with S2 primary / S1 fallback / S3 deferred.  
3. Next design work (joint module, dock, URDF/YAML kin model) **shall cite S2** or explicitly propose an ADR amendment.  
4. First prototypes should exercise: cascade belt access (DFAA), quiet motion (N6), planar dual-dock step at ~0.5–0.6 m class spacing.  
5. If cascade is abandoned for S1, record the trigger (noise, slip, service time) in a short ADR amendment or superseding note.

- See amendment 2026-09-20: implement to **S4**; keep S2 designs as fallback reference.
- First prototypes should still exercise planar dual-dock walk and quiet motion (N6); add dual-hinge and through-elbow service checks when building S4.

### Handoff & Next Steps

Based on the S2 selection, the following follow-up tasks and revalidation points are identified:

#### Follow-ups
- **Joint module geometry:** Design proximal FOC pod and cascade belt span under S2 constraints.
- **Dock interface:** Sketch main base latch + auxiliary base latch / dual-contact mechanism for stable planar walk.
- **End Effector (EE):** Design quick-change interface with electrical contacts and reserved air path.
- **Kinematic Model:** (Optional) Create `hardware/kinematics/s2.yaml` (or URDF) for FK reach and dual-dock span verification.
- **Component Selection:** Execute ROADMAP item for motors, drivers, gearboxes, sensors, and compute.
- **LIMS-class (ADR-0006):** performance aspiration and parallel **S4** study; S2 remains baseline until an explicit S2 vs S4 gate amends this ADR.

#### Revalidation (Post-Prototype)
- **Cascade transmission:** Evaluate DFAA accessibility, preload stability, and acoustic contribution (N6).
- **Mass budget:** Re-check real link/actuator masses against the illustrative OOM model to confirm N5 margins.
- **Relocatable base:** Test planar dual-dock step at ~0.5–0.6 m spacing and auxiliary latch load paths.
- **Architecture trigger:** Confirm if S1 fallback is needed due to belt slip, service complexity, or noise.
- **Pneumatics:** Re-evaluate if the reserved pneumatic route is justified vs. electrical-only MVP.

## References

- `docs/tasks/0004-scheme-downselect.md` — K5 scorecard and OOM analysis
- `docs/tasks/0004-candidate-schemes.md` — S1/S2/S3 definitions
- `docs/tasks/0004-placement-policy.md`
- ADR-0003, ADR-0004, ADR-0006
- `docs/spec.md` — R1, R2, R3, R7, R8, DFAA
- `docs/tasks/0005-s2-s4-gate.md` — C1b.6  
- `docs/tasks/0005-candidate-scheme-s4.md`  
- `docs/decisions/0006-lims-class-performance-aspiration.md`

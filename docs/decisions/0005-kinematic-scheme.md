<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# ADR-0005: Phase 1 Kinematic Scheme

- **Status:** Accepted
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

## References

- `docs/tasks/0004-scheme-downselect.md` — K5 scorecard and OOM analysis  
- `docs/tasks/0004-candidate-schemes.md` — S1/S2/S3 definitions  
- `docs/tasks/0004-placement-policy.md`  
- ADR-0003, ADR-0004  
- `docs/spec.md` — R1, R2, R3, R7, R8, DFAA

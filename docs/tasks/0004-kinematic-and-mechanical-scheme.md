<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Task: Develop kinematic and mechanical scheme of the interface

**Status:** open  
**Related:**
- ROADMAP Phase 1 — “Develop kinematic and mechanical scheme…”
- `docs/spec.md` (R1–R3, R7, DFAA, relocatable base)
- `docs/decisions/0003-core-numerical-characteristics.md`
- `docs/implementation-concepts.md` (§1)
- Conversation (to create): `docs/conversations/2026-09-14--kinematic-mechanical-scheme.md`
- Optional survey notes: `docs/conversations/2026-09-14--kinematic-survey-notebooklm.md`

**Goal:** Select and document a Phase 1 kinematic + mechanical scheme (topology, DoF layout, relocatable-base concept, actuator/electronics placement *policy*) that respects ADR-0003 numbers and DFAA — without full detailed CAD or final motor SKUs.

---

## Constraints (from existing decisions)

Must respect:
- ADR-0003: reach, payload, ≥2 docks, power scenario A (default) / B (alternate), torque/speed bands, acoustic intent, BOM ceilings
- Spec: ≥6 DoF, relocatable base, quiet motion, COTS/FDM, DFAA
- Non-goals: industrial heavy payload, humanoid form

Out of scope for this task:
- Full link CAD / manufacturing drawings
- Final gearbox ratios and SKU freeze
- MuJoCo model as deliverable (may be a follow-up)
- PCB design

---

## Subtasks

### K0. Setup
- [x] K0.1 Create conversation file for this workstream
- [x] K0.2 Link this task from ROADMAP item

### K1. Constraint sheet
- [x] K1.1 One-page checklist: ADR-0003 + spec requirements that any scheme must satisfy → [0004-kinematic-constraints.md](0004-kinematic-constraints.md)
- [x] K1.2 Explicit DFAA veto rules (what makes a scheme unacceptable) → same file

### K2. Survey of implemented analogues (curated, not open-web sprawl)
- [x] K2.1 Define survey scope (include / exclude) → [0004-kinematic-survey-scope.md](0004-kinematic-survey-scope.md)
  - Include: desktop/cobot serial arms, dual-ended or relocatable concepts, tendon/remote-drive arms, quiet BLDC modular joints, printable actuator stacks
  - Exclude: industrial 50+ kg arms, pure SCARA/Delta as primary, legged humanoids as primary
- [x] K2.2 Define selection criteria for analogues (reached hardware, public docs/video, relevance to DFAA/relocatable/quiet/COTS) → same (§ K2.2)
- [x] K2.3 Build source list (URLs only; **do not commit copyrighted full texts/media to git**) → same (§ K2.3)
- [x] K2.4 Run structured review (optional: Google NotebookLM bounded to that source list)
- [x] K2.5 Write takeaways table: pattern → pros/cons for sint → retain / drop
- [x] K2.6 Record survey conversation (prompts, limits, summary). Optional: short “patterns retained” note or lightweight ADR if team wants a hard gate before drawing schemes

### K3. Placement policy (motors & electronics) — principles only
- [x] K3.1 Motor placement options: in-joint vs proximal/base + transmission (tendon/belt/gear)
- [x] K3.2 Preferred mass distribution bias (e.g. proximal-heavy, light distal) aligned with N3/N5
- [x] K3.3 Compute / power electronics zones (central proximal vs distributed joint MCUs)
- [x] K3.4 Interaction with power scenario A vs B (battery location; mirrored ends or not)
- [x] K3.5 DFAA implications (what the agent must be able to replace: joint module, tensioner, compute brick)

→ [0004-placement-policy.md](0004-placement-policy.md)

### K4. Candidate schemes (2–3)
- [x] K4.1 Scheme S1 — description + stick diagram + joint list (DoF, approximate axis roles)
- [x] K4.2 Scheme S2 — same
- [x] K4.3 Scheme S3 (optional) — e.g. dual-ended symmetric variant
- [x] K4.4 For each: relocatable-base story (≥2 docks), EE interface role, how printer/table/tool-bay workspace is covered
- [x] K4.5 Diagrams: 2D stick / SVG / simple sketch preferred; build123d only if helpful — not mandatory at this stage

→ [0004-candidate-schemes.md](0004-candidate-schemes.md)

### K5. Compare and down-select
- [ ] K5.1 Scorecard: DFAA, relocatable base, payload/inertia, complexity, BOM risk, acoustic risk, fit to ADR-0003
- [ ] K5.2 Order-of-magnitude checks on leading scheme (link length budget vs print envelope; torque vs N5; dock spacing vs reach)
- [ ] K5.3 Choose preferred scheme + list rejected alternatives with reasons

### K6. Decision record
- [ ] K6.1 Draft ADR (kinematic & mechanical scheme): topology, DoF layout, relocatable concept, placement policy, open issues
- [ ] K6.2 Accept ADR; link from current-state and ROADMAP
- [ ] K6.3 Close this task

### K7. Handoff to next work
- [ ] K7.1 List follow-ups: first joint module geometry, dock interface sketch, optional sim skeleton
- [ ] K7.2 Note what must be revalidated after first hardware prototype

---

## Suggested scheme families to force into K4 (unless survey kills one)

1. **Serial 6-DoF, modular in-joint actuators** (GLUON-like simplicity / DFAA modules)  
2. **Serial 6–7 DoF, proximal motors + distal transmission** (LIMS-inspired inertia/payload)  
3. **Symmetric dual-ended relocatable** (strong R2; harder interfaces / power B)

Hybrids allowed if scoring wins.

---

## Done when

- [ ] Survey takeaways exist (conversation ± table); sources cited by URL only
- [ ] Placement policy for motors/electronics is written at principle level
- [ ] 2–3 candidate schemes documented with stick-level diagrams and joint lists
- [ ] One scheme selected with explicit trade-off rationale
- [ ] ADR accepted; ROADMAP item and `docs/current-state.md` updated
- [ ] Open risks / “revisit after first prototype” listed in ADR

---

## Method notes

- Prefer ranges and policies over false precision
- DFAA is a **veto**, not a soft preference
- Do not merge this task into full kinematics CAD or motor SKU freeze
- NotebookLM (if used): only pre-selected sources; export conclusions into git as **our** text, not scraped corpora

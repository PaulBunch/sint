<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# ADR-0006: LIMS-class performance aspiration (parallel to S2)

- **Status:** Accepted (aspiration + process; does **not** supersede ADR-0005)
- **Date:** 2026-09-18
- **Deciders:** Project maintainers / agents working on Phase 1
- **Related:**
  - `docs/decisions/0005-kinematic-scheme.md` (S2 remains Phase 1 primary scheme)
  - `docs/decisions/0004-kinematic-survey-patterns.md` (remote/cable = pattern-only; opaque packs vs DFAA)
  - `docs/references/lims-family-notes.md`
  - `docs/implementation-concepts.md` §1.4
  - `docs/tasks/0005-component-composition.md`
  - ROADMAP Phase 1

## Context

Public LIMS-family arms (especially **LIMS3-AMBIDEX** and **LIMS-EX**) demonstrate a performance class that many “classic” in-joint desktop arms struggle to match: low distal inertia, smooth quiet motion, strong payload-to-arm-mass ratio (~1:2 at ~5 kg / ~9–10 kg class), and workspace flexibility around the base (including serving the dock perimeter and reaching below the dock plane when edge-mounted).

ADR-0005 correctly selected **S2** (cascaded serial 6-DoF, DFAA-accessible short belt/tendon) under BOM, DFAA, and consumer-COTS constraints. That decision is **not revoked**. However, treating only PAROL6/GLUON-class serial arms as the ceiling risks optimizing into known limits (distal mass, tremor-like compliance, restricted fold-around-dock mobility).

This ADR raises **LIMS-class dynamics** to the **primary external performance reference** and opens a **parallel study branch (candidate scheme S4)** without rewriting prior ADRs.

## Decision

1. **Performance reference:** Prefer LIMS-family behaviour (smoothness, backdrivability, distal lightness, base-neighbourhood workspace) as the **aspiration bar** for sint motion quality — documented in `docs/references/lims-family-notes.md`.
2. **Normative scheme unchanged:** ADR-0005 **S2** remains the **default implementation baseline** until an explicit down-select amends or supersedes it.
3. **Parallel candidate S4 (“LIMS-inspired”):** Study and document a consumer/DFAA-adapted concept that may include:
   - collinear / symmetric link load paths (reduce parasitic joint moments);
   - **proximal motor pack** with very light forearm/wrist;
   - **dual-axis or rolling-contact elbow** class mechanisms for fold and dock-perimeter reach;
   - short accessible cable/belt spans; evaluate **N+1-to-2N** and shared pretension **only** with a DFAA service story;
   - still under ADR-0003 numeric bands (0.5 kg class, not 5 kg clone).
4. **Gate before COTS freeze:** Complete a structured **S2 vs S4** comparison (workspace around dock, inertia, DFAA, BOM risk, open reproducibility) **before** locking component composition ADR for the whole arm. Smoke-test FOC stacks may proceed on **scheme-agnostic** classes (motor/driver/encoder families).
5. **Hard filters retained:** Opaque full-arm cable trees and non-serviceable pretension **fail DFAA V5** unless redesigned for agent access. No naive torque scaling from LIMS payload (÷10 rule rejected).

## Options considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Ignore LIMS beyond survey footnotes | Rejected | Leaves known dynamics gap vs classic desktop arms |
| Immediately replace S2 with full LIMS-EX clone | Rejected | Papers incomplete for EX; custom motors; DFAA/BOM risk |
| Aspiration + parallel S4 study, S2 baseline | **Accepted** | Learns from IRIM path without discarding Phase 1 progress |
| Defer all LIMS work until after full S2 hardware | Rejected as sole plan | Risk of months–years on classic limits |

## Consequences

### Positive
- Clear signal: motion quality target is LIMS-class, not “another slow geared arm”
- S2 work and COTS class lists remain valid
- Forces dual-elbow / proximal-pack study before irreversible SKU freeze

### Risks
- Parallel branch can dilute focus — mitigate with explicit S2 vs S4 checkpoint in task 0005 / ROADMAP
- N+1-to-2N may not be reproducible in open consumer form
- Hobby recreations may only capture fragments of LIMS joints

### Neutral
- ADR-0003 numbers unchanged
- ADR-0005 text unchanged; this ADR **adds** process and aspiration only

## Implementation notes

1. Add ROADMAP item / task branch for LIMS deep-dive + S4 sketch + S2 vs S4 gate.
2. Extend `lims-family-notes.md` with papers and open recreations (URL only).
3. Component composition (0005): keep S2 mapping; annotate which classes are **shared** vs **S4-specific**; do not freeze distal architecture until S2 vs S4 note exists.
4. Optional later: amend ADR-0005 or issue superseding scheme ADR if S4 wins the gate.

## References

- `docs/references/lims-family-notes.md`
- IRIM LAB KOREATECH public LIMS / LIMS2 / LIMS3 / LIMS-EX videos
- ADR-0004, ADR-0005

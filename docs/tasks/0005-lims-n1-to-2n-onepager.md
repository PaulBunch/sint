<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C1b.3 — N+1-to-2N wrist actuation & pretension (one-pager)

**Status:** done (reference synthesis)  
**Closes:** task 0005 item C1b.3  
**Normative for sint?** No — input to **S4** (ADR-0006). Does not change ADR-0005 S2.  
**Sources:** `docs/references/lims-family-notes.md` §3.6; LIMS-EX video (S2); earlier LIMS tension-amplification papers (P1–P2, P4–P5) for family context — **not** a peer-reviewed EX disclosure.

---

## 1. Problem the hybrid scheme addresses

Cable wrists need **always-positive tension** and usually **more cables than DoF**.

| Classical pattern | Motors (wrist) | Cables (typical story) | Pain |
|-------------------|----------------|------------------------|------|
| **N+1** | 4 for 3-DoF | 4 | Extra actuator or heavy active tension control |
| **2N** | 3 for 3-DoF | 6 | Three separate pretension mechanisms; bulk |
| **LIMS-EX claim: N+1-to-2N hybrid** | **3** | ~**4 paths / continuous loops** + **single pretension** | Public slogan; detail = video reconstruction |

Goal: **3 motors → 3 wrist DoF**, continuous tension, **one** pretension device, cables routed through a **decoupled elbow** (see C1b.2).

---

## 2. What is known publicly vs inferred

| Item | Confidence | Note |
|------|------------|------|
| “N+1-to-2N” + single pretension as EX marketing | **High** | On-video key features |
| 3 wrist-group actuators on upper arm | **High** | CAD labels / placement narrative |
| Bevel differential wrist | **High** | CAD “3-DOF wrist with bevel gears” |
| Elbow rollers decouple cable length from elbow angle | **High** (intent) | Stated decoupled elbow; geometry inferred |
| Exact continuous-loop topology (2 loops, co-wound drums, yaw via slider motor) | **Medium** | Contributor reconstruction from colour cable diagram |
| Motor↔DoF matrix (pitch / roll / yaw) | **Medium** | Working hypothesis in lims-family-notes §3.6.2 |
| Peer-reviewed EX paper on this hybrid | **Low / absent** in our index | Treat mechanism as **best-effort** until published |

---

## 3. Working mechanical picture (reconstruction)

```text
[2 side motors on upper arm] --drums--> [2 continuous cable loops]
         |                                    |
         |                                    v
         |                         [elbow rollers: length-invariant bend]
         |                                    |
         |                                    v
         |                         [bevel differential wrist: pitch/roll/yaw]
         |
[1 pretension / bias motor] --> [slider pair] --> takes slack on both loops
```

**Elbow decoupling (ties to C1b.2):** cable centerlines pass so flexing the dual-hinge elbow does **not** net-reel the wrist loops.

**Single pretension:** one geometric/actuator change at the **sliders** propagates tension into all wrist paths — vs three independent tensioners (2N) or four independent active cables (N+1).

**Optional passive compensation:** elbow “bone” motion may also shift slider geometry so elbow angle does not fight pretension (see lims-family-notes §3.5C) — identity of pink link vs pretension callout still **open**.

---

## 4. Consumer-reproducible subset (what sint may attempt)

**Plausible open/DFAA subset (S4 research):**

| Element | Consumer approach |
|---------|-------------------|
| Media | Timing **belt** or thin steel/Dyneema **cable** with visible path |
| Drums | Two side motors, printed/COTS pulleys, clamp or capstan wrap |
| Wrist | Simple bevel or cable differential; start with **2 DoF** wrist if 3 DoF packaging fails |
| Pretension | **One** accessible turnbuckle or screw-slider per span — agent can reach without full disassembly |
| Elbow pass-through | Open covers; rollers on dual-hinge (C1b.2 subset) |
| Sensing | Motor encoder + joint encoder (LIMS3 lesson: ABS both ends) |

**Not in consumer MVP subset:**

- Full EX enclosed multi-roller tree with undocumented loop topology  
- Shared pretension that only a lab fixture can set  
- Requirement for custom frameless BLDC + proprietary compound planetary (patent PT1 is reference only)  
- Copying 5 kg / 9.7 kg scale or EX joint N·m table  

**DFAA rule:** every tensioner and drum must be a **replaceable unit**; no “only works if factory-routed.”

---

## 5. Relation to S2 default

| S2 (ADR-0005) | S4 interest (this note) |
|---------------|-------------------------|
| Short **belt/tendon** cascade, agent-open channels | Same openness requirement |
| Distal drives in forearm pack OK | Prefer **wrist motors on upper arm** + through-elbow paths |
| No mandatory hybrid N+1-to-2N | Hybrid is **optional research** if DFAA holds |
| Simpler debugging | Higher kinematic coupling; needs clear docs + tests |

Smoke-test FOC joint (**C4.2**) stays **scheme-agnostic** and does **not** wait on full N+1-to-2N.

---

## 6. Risks if adopted early

1. **Wrong loop topology** → binding or slack under elbow motion  
2. **Yaw/pretension coupling** misunderstood → unstable tension under load  
3. **BOM/time** exceeds classic cascade before benefits show  
4. **N6:** cable/belt squeal vs quiet FOC motor noise  

Exit: fall back to S2 short cascade or S1 in-joint distal.

---

## 7. Handoff

| Next | Action |
|------|--------|
| C1b.4 | S4 stick: proximal shoulder + upper-arm wrist pack + dual-hinge elbow + **accessible** single pretension story |
| C1b.5 | Score reproducibility and DFAA vs S2 cascade simplicity |
| Papers | Watch for LIMS-EX publication; update lims-family-notes §3.6 confidence |

**One-line summary:** N+1-to-2N on EX means **3 wrist motors + single pretension + decoupled through-elbow cables**; sint may borrow the **idea** only in a **visible, serviceable** subset — not a sealed lab clone.

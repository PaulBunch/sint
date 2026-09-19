<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C1b.2 — Dual-axis / rolling elbow (one-pager)

**Status:** done (reference synthesis)  
**Closes:** task 0005 item C1b.2  
**Normative for sint?** No — input to **S4** study (ADR-0006). S2 baseline unchanged (ADR-0005).  
**Sources:** `docs/references/lims-family-notes.md` §2.7, §3.5; LIMS3/EX videos; open joint recreations (R1–R2 in notes).

---

## 1. What “dual-axis elbow” means here

| Concept | Meaning |
|---------|---------|
| **Effective DoF** | **1** commanded elbow flexion/extension |
| **Physical structure** | **Two hinged stations** in series (upper-arm ↔ intermediate body ↔ forearm), coupled **1:1** (gear or equivalent sync) |
| **Not** | A free 2-DoF elbow under independent control |
| **LIMS-EX framing** | “Decoupled elbow”: dual disk/pulley node; cables roll on radii about the elbow axis so **elbow angle does not change net wrist-cable length** |

Related family idea: **rolling-contact** joints (LIMS2-style / quaternion wrist papers) — pure rolling geometry for low friction and large ROM. Elbow dual-hinge is the **fold + cable-path** cousin of that philosophy.

---

## 2. Kinematic intent

1. **Large fold:** forearm can lie nearly along the upper arm without hard interference of single-pivot shells.  
2. **Gentler cable path:** wrist actuation cables wrap **two radii** instead of one sharp bend → less wear, friction, and tension spike.  
3. **Decoupling:** elbow motion does not parasitic-drive wrist tendons (critical if wrist motors sit on the upper arm).  
4. **Proximal elbow motor:** LIMS-EX drives elbow from a motor on the **shoulder fork** via a rigid push-pull **“bone”** linkage — elbow joint itself stays light.

```text
[shoulder fork] --motor+crank--> [rigid link] --> [dual-hinge elbow 1:1] --> [light forearm]
                                      |
                                      +--> optional kinematic cue to pretension slider (EX reconstruction)
```

---

## 3. Dock-perimeter reach (why it matters for sint)

For a **relocatable / dock-mounted** arm (coplanar docks, printer + tool bay):

| Capability | Single-pivot elbow (typical S2 sketch) | Dual-hinge / high-fold elbow |
|------------|----------------------------------------|------------------------------|
| Reach **around** own base / dock flange | Often limited by elbow “knuckle” bulk | Better: arm can fold tight and still point EE near dock plane |
| EE **below** dock plane (edge-mounted base) | Harder without long links or extra DoF | Easier with deep fold + shoulder pitch |
| Self-service of latch / harness at base | Crowded workspace | Improved “work on own feet” envelope |

This is a **workspace quality** argument for S4, not a claim that S2 cannot dock-walk. S2 remains valid for planar dual-dock with aux latch; dual-hinge is the upgrade path if dock-neighbourhood tasks dominate.

---

## 4. DFAA risks (hard filter)

| Risk | Why it hurts agent assembly/service | Mitigation if adopted |
|------|-------------------------------------|------------------------|
| Extra bearings, sync gear/link, intermediate body | More parts, tighter tolerances, print+fit burden | Modular cartridge: whole dual-elbow unit replaceable |
| 1:1 sync lost or binding | Elbow folds unevenly; cables bind | Visible inspection windows; no sealed lab-only jig |
| Rigid “bone” linkage | Long member; pin wear; must clear covers | Standard pins/clips; agent-reachable ends |
| Cable rollers at both hinges | 4+ rollers per side in EX-class routing | Prefer **short, open channels**; labelled left/right paths |
| Calibration | Zero elbow vs motor crank vs slider | Encoder at elbow output + motor; procedure in docs, not tribal knowledge |

**Veto-aligned rule (ADR-0004 / placement policy):** dual-hinge is acceptable only if the agent can **retension, re-pin, and replace** the elbow cartridge without destroying the upper arm.

---

## 5. Consumer / open-source subset (for S4, not full EX clone)

**In scope to study for sint S4:**

- Dual-hinge 1-DoF elbow with printed shells + COTS bearings  
- Optional rigid link elbow drive from proximal motor (or short belt if DFAA-cleaner)  
- Open roller path for **short** wrist cables/belts through elbow  

**Out of default MVP:**

- Full EX enclosed dual-elbow + lab cable tree  
- Custom frameless motors as requirement  
- Opaque sync gear buried without service cover  

---

## 6. Handoff

| Next | Action |
|------|--------|
| C1b.3 | N+1-to-2N + pretension one-pager (pairs with this elbow decoupling story) |
| C1b.4 | S4 stick: serial arm + **dual-hinge elbow** + proximal packs + accessible spans |
| C1b.5 | Score dual-hinge under dock workspace vs S2 single elbow complexity |

**One-line summary:** Dual-axis elbow is **1 DoF with two hinges** for fold, cable decoupling, and dock-neighbourhood reach; adopt only as a **serviceable module**, not a sealed LIMS copy.

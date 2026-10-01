<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C3.1 / C3.2 — COTS shortlist: motors & FOC drivers

**Status:** draft shortlist (families for MVP procure / bench)  
**Normative filters:** `docs/tasks/0005-class-requirements-motors.md`  
**Number catalog (SoT):** [`0005-motors-catalog.csv`](0005-motors-catalog.csv)  
**Sources:** [`0005-motors-catalog-sources.md`](0005-motors-catalog-sources.md)  
**Scheme:** S4 · Power A · ADR-0003 torque bands · moderate \(N \approx 5\ldots16\) (not CNC-class \(N \ge 36\))

**Out of this shortlist:** Maxon / Kollmorgen as MVP SKUs; \(N > 16\) planetary defaults; pure smoke-only toys.

**MVP = first hardware loop** (FOC, thermal, noise, backdrive). No separate disposable motor class.

---

## Design rules (recap)

1. Target is **joint continuous torque** (ADR), not motor nameplate alone.  
2. Prefer **moderate N** so \(J_\mathrm{rotor} N^2\) stays usable for backdrive / N6.  
3. **Placement (S4 / yoke):**
   - **J1** — strongest actuator (base yaw / first proximal).  
   - **J2 and J3** — **same mass and envelope** (preferably **same SKU**), mounted **symmetrically / mirrored** on the shoulder yoke; avoid different OD/height pairs that unbalance the fork.  
   - **Wrist pack on L2** — lighter distal modules; steel G preferred if continuous load, ALU gear only on light distal.  
4. Electrical paths:
   - **Path QDD:** integrated motor+G(+driver) · often **24/48 V** · CAN to spine  
   - **Path raw:** 24 V-class BLDC + external FOC + separate G  
5. LIMS-EX norms guide *relative* sizing only; absolute scale = ADR (~0.5 kg payload).

| Joint | LIMS-EX norm | sint continuous OOM (joint) | Packaging rule |
|-------|--------------|-----------------------------|----------------|
| J1 | 1.0 | ~10–25 N·m | Strongest single axis |
| J2 | ~0.8 | scale ≤ J1 | **Same module family/size as J3** |
| J3 | ~0.7 | ~5–15 N·m class | **Same as J2** (yoke pair) |
| Wrist | ~0.1–0.3 | ~1–5 N·m | L2 pack mass budget |

---

## C3.1 Motors — primary shortlist

Full numbers: CSV. Below: **selection rationale** only.  
Catalog `J_rotor` for QDD = **motor-side** unless stated; joint reflected \(\sim J N^2\).

### Path Q — integrated QDD / joint modules (preferred for MVP speed)

No custom gearbox design. Driver often optional/on-module; host via **CAN** (vendor).

#### Q1 — SteadyWin GIM (budget primary)

| ID | Model (CSV / table) | Role | Why | Watch-outs |
|----|---------------------|------|-----|------------|
| **Q-SW1** | **GIM8115-9** (24/48) | **J1** preferred | Rated **~13–15 N·m**, N=9, STEEL, hits lower–mid proximal band | ~705 g; driver GDS/GDZ variant; verify RU quote |
| **Q-SW2** | **GIM8108-9** / **GIM8108-8** | J1 alt / strong J2–J3 | 8–9 N·m class, N=8–9, compact vs 8115 | J1 alone may be tight vs upper ADR; OK mid band |
| **Q-SW3** | **GIM6010-8** (24 V GDS preferred for τ) | **J2=J3 pair** default | **5 N·m / peak 11**, N=8, ~388 g, STEEL, low cost | Below full J1; **pair two identical** on yoke |
| **Q-SW4** | **GIM6010-6** / **GIM8108-6** | J2=J3 if more QDD (lower N) | N=6, slightly lower τ | Mass: 6010-6 lighter than 8108-6 |
| **Q-SW5** | **GIM4310-10** | Wrist / distal | **~2 N·m**, N=10, ⌀53, STEEL option | GDS vs GDZ τ differs |
| **Q-SW6** | **GIM3510-8** | Wrist light | ~1.7 N·m GDS; cheap | **ALU gear** — distal only |

#### Q2 — CubeMars AK (performance / same form-factor family)

| ID | Model | Role | Why | Watch-outs |
|----|-------|------|-----|------------|
| **Q-CM1** | **AK10-9** | J1 heavy | **18 N·m** out, N=9 | Mass ~940 g; price OOM high |
| **Q-CM2** | **AK80-8 / AK80-9 / AK70-9** | J1 or matched J2–J3 | 8–10 N·m, dual-enc options | Price > SteadyWin |
| **Q-CM3** | **AK60-6** | J2=J3 light / J3 | 3 N·m, N=6 | |
| **Q-CM4** | **AK45-10 / AK40-10** | Wrist | 1.3–2.5 N·m | |

#### Q3 — Fulling iSVD (integrated FOC+G, 48 V class)

| ID | Model | Role | Why | Watch-outs |
|----|-------|------|-----|------------|
| **Q-FL1** | **iSVD88C** | J1 | **11 N·m**, N=9, dual enc | 48 V; ~621 g |
| **Q-FL2** | **iSVD78C / iSVD57C** | J2=J3 pair | 5–6 N·m class | Same bus as 88 |
| **Q-FL3** | **iSVD46C** | Wrist | 1.6 N·m | Module mass on L2 |

### Path B — raw BLDC + separate G + external FOC (fallback)

Only if QDD lead time/cost fails. **\(N \approx 8\ldots16\)**.

| ID | Model | Role | Why | Watch-outs |
|----|-------|------|-----|------------|
| **B1** | GM110-10 | J1 raw | Highest gimbal τ class + hollow | Load ≠ continuous; J unknown |
| **B2** | GM8112 / GM6208 | J2=J3 raw pair | Matched size possible | Same |
| **B3** | FL48CBL68 / FL60BLW | J3 / light prox | Published J (FL48) | Needs G |
| **B4** | FL45BLW / GM4108H / GB36-2 | Wrist | Distal τ + optional published J | |

---

## Recommended MVP joint map (default proposal)

| Joint | Preferred stack | Matched-pair rule | Fallback |
|-------|-----------------|-------------------|----------|
| **J1** | **GIM8115-9** or **GIM8108-9** or **iSVD88** / AK70–80 | Single strongest | GM110-10 + G + FOC |
| **J2 + J3** | **Two × GIM6010-8** (same SKU, mirrored on yoke) | **Identical OD/height/mass** | Two × GIM8108-8 or two × iSVD57/78 |
| **Wrist (L2)** | **GIM4310-10** or **AK45-10** / iSVD46 | Independent of yoke pair | GIM3510-8 (ALU) or FL45 + G |

**Do not** put a heavier unique module on J2 and a lighter one on J3 (or vice versa) without a written mass-balance exception.

**Bus:** SteadyWin allows mixed 24/48 by SKU — prefer **one bus** per arm (all 24 or all 48) for dock/power A simplicity. Path iSVD implies **48 V**.

---

## C3.2 Drivers / FOC

| Path | Driver | Notes |
|------|--------|--------|
| **Q SteadyWin** | On-module **GDS / GDZ / GDK** | Prefer **CAN**; GDZ if **CAN+485** and secondary encoder needed. Numbers are **driver-variant dependent** — lock SKU+driver together. |
| **Q CubeMars / iSVD** | Built-in FOC | CAN to spine |
| **B raw** | ODESC / ODrive-class or documented FOC + encoder | Encoder required; no 48 V into 24 V driver |
| **N6** | No default fans on driver packs | |

---

## Per-joint envelopes (preliminary — for later mech calc)

*Not a freeze. Order-of-magnitude from shortlist centers; refine after SKU+driver lock.*

| Joint | τ_cont target (ADR) | Candidate τ_rated (module out) | Mass OOM (module w/ driver) | Envelope OOM (OD × H) |
|-------|---------------------|--------------------------------|-----------------------------|------------------------|
| J1 | 10–25 N·m | 8–15 N·m (8115-9 / 8108-9 / iSVD88); up to ~18 (AK10) | ~400–700 g (SW/CM mid); ~900 g heavy | ~⌀90–100 × 40–60 mm |
| J2 | ≤ J1 | **5–8 N·m** (6010-8 / 8108-8) | **~390–570 g each** | **Matched pair** ~⌀80–96 × 40–55 |
| J3 | ~5–15 | **Same as J2** | **Same as J2** | **Same as J2** |
| Wrist ×3 | 1–5 each | 1.3–2.5 N·m | ~190–310 g each | ~⌀46–55 × 40–50 |

Use these as **placeholders** in link/yoke CAD and inertia estimates; replace with chosen CSV rows when purchasing.

---

## Explicit non-goals

- Maxon / Kollmorgen MVP line items  
- Default \(N \ge 36\)  
- Unmatched J2/J3 masses on the yoke  
- Treating gimbal “load torque” as industrial continuous without bench derate  

---

## Next actions

1. Lock **one bus** (24 vs 48) and **one QDD family** for first three axes (J1 + J2/J3 pair).  
2. RU quote: **2× GIM6010-8 + 1× GIM8115-9 (or 8108-9) + 1–3× GIM4310-10**.  
3. After first powered axis: thermal/noise/backdrive → freeze or amend ADR bus.  
4. Later: promote envelope table to dedicated mech handoff doc if needed.

---

## Document control

| Item | Value |
|------|--------|
| Catalog SoT | `0005-motors-catalog.csv` |
| Closes | C3.1/C3.2 **shortlist draft** (not purchase order) |
| Open | Live RU quotes; driver SKU lock; J measurement on raw path |

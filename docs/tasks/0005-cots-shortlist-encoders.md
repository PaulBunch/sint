<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# C3.3 — COTS shortlist: encoders / position feedback

**Status:** draft shortlist  
**Normative:** [`0005-class-requirements-sensors.md`](0005-class-requirements-sensors.md) (C2.4)  
**Motors context:** [`0005-cots-shortlist-motors-drivers.md`](0005-cots-shortlist-motors-drivers.md)  
**Scheme:** S4 (motor angle ≠ joint angle on media paths)

**Goal:** 2–4 families each for (A) motor-side FOC feedback and (B) **joint-output absolute**, with URLs only. Prefer magnetic on-axis, DFAA-replaceable, no sealed-only industrial lock-in.

---

## 1. Policy (recap)

| Stage | Motor-side | Joint-output absolute |
|-------|------------|------------------------|
| Smoke test | Required (1 axis) | Optional |
| MVP interim | All active axes | **Preferred** on elbow + wrist (longest media) |
| Phase 1 target | As available (often inside QDD) | **All J1–J6** (or documented exception + observer) |

- **Force proxy:** FOC phase current — not joint torque cells (C2.4 F-M*).  
- **Type default:** contactless **magnetic** (diametric magnet + IC). Optical / sealed industrial pods → reject list.  
- **DFAA:** magnet + PCB or modular hub replaceable without destroying joint shell.

---

## 2. Layer A — on-module / motor-side (comes with actuator)

Not chosen independently when Path Q is used; document what the SKU already provides.

| Family | Typical story | Counts as joint-output abs? | Notes |
|--------|---------------|----------------------------|--------|
| **SteadyWin GIM + driver** | On-driver magnetic (12–16 bit class); optional **secondary** on output | **Only if** secondary is true output-shaft angle **and** used as control feedback — vendor text often says secondary is for **power-off single-turn memory** only | Prefer GDZ/options with second encoder **and** verify in manual; do not assume E-M3 closed |
| **CubeMars AK*** | Dual magnetic (inner + outer) on many SKUs | Outer closer to joint; still module-local, not arbitrary link mount | Good motor+output pair inside module |
| **Fulling iSVD*** | Dual encoder in module | Same | 48 V path |
| **Path B raw + FOC** | External chip on motor shaft (see §3) | No — motor only until separate joint sensor | ODESC/SimpleFOC need SPI or ABI |

**URLs (examples):**  
- SteadyWin secondary encoder product: https://steadywin-motor.com/products/steadywin-secondary-encoder  
- CubeMars product pages (dual encoder in AK specs): https://www.cubemars.com/categorys/product  
- Fulling iSVD: https://www.fullingmotor.com/en/product  

---

## 3. Layer B — joint-output absolute (COTS, motor-agnostic)

Mounted on **joint / link output** (after G, or on dual-hinge / wrist axis). Same candidates for SteadyWin, CubeMars, or raw Path B.

### B1. Magnetic IC + diametric magnet (primary shortlist)

| ID | Device | Abs bits (typ.) | Interface | Why | Watch-outs |
|----|--------|-----------------|-----------|-----|------------|
| **E-M1** | **ams AS5047P / AS5047U** | 14 | SPI + ABI/UVW/PWM | De-facto FOC/robot joint IC; SimpleFOC & moteus ecosystem; fast | Need magnet air-gap design; PCB or breakout |
| **E-M2** | **MagnTek MT6701** | 14 | SSI / I²C / ABZ / PWM | Low cost; multi-protocol; SimpleFOC driver exists | SSI ≠ full SPI on all MCUs; quality of cheap boards varies |
| **E-M3** | **MPS MA730** | 14-class | SPI | Compact; used in DIY FOC | Board availability |
| **E-M4** | **Broadcom AEAT-8800-Q24** | 10–16 prog. | SSI + ABI/UVW | Higher-end magnetic; programmable | Cost; QFN assembly |

**Magnet:** diametrically magnetized NdFeB, on-axis over IC (size per datasheet, often Ø6 mm class).

**Example breakouts / refs (URL only):**  
- AS5047P: manufacturer portfolio / Mouser ams position sensors  
- MT6701: community + datasheet via MagnTek; SimpleFOC forum support  
- MA730: open breakout designs in DIY FOC repos  

### B2. Modular shaft absolute (optional, heavier)

| ID | Device | Type | Interface | Why | Watch-outs |
|----|--------|------|-----------|-----|------------|
| **E-H1** | **CUI Devices AMT22** (SPI) | Capacitive modular | SPI | Hub on shaft, 12/14-bit abs, settable zero | ~16 g; shaft tolerance; cost ≫ magnetic IC |
| **E-H2** | **CUI AMT21** | Capacitive modular | RS-485 | If multi-drop joint bus wanted | Same mechanical constraints |

**URL:** CUI/Same Sky AMT21/AMT22 series (Digi-Key / Mouser datasheets).

### B3. Incremental-only (supporting, not Phase-1 primary)

| ID | Use | Notes |
|----|-----|--------|
| **E-I1** | ABI from AS5047*/MT6701 | Fine for velocity / FOC assist; **not** cold-start absolute alone |
| **E-I2** | Classic optical A/B | Avoid as default (dust, alignment) |

---

## 4. Wiring / compute implications

| Sensor | Typical host | Independent channel? |
|--------|--------------|----------------------|
| QDD internal motor (and module dual) | Module MCU → **CAN** to spine | No extra SPI on L2 for that axis |
| External joint abs (E-M*) | Joint MCU or L2 SoM | **Yes** — SPI/SSI per sensor or daisy carefully; CS per axis |
| AMT21 RS-485 | Shared bus possible | Yes, bus design |
| Path B motor IC | FOC board | Yes, on driver |

**Spine ("spinal cord"):** may only see joint angles if joint MCU publishes them; raw SPI from six AS5047 to one SBC is possible but messy — prefer **local RT + CAN**.

---

## 5. MVP mapping proposal

| Joint | Motor-side | Joint-output abs (MVP interim → Phase 1) |
|-------|------------|------------------------------------------|
| J1 | QDD onboard | Add E-M1/E-M2 when base walk / no-home required |
| J2, J3 (yoke) | QDD onboard | Same pair of external abs if cascade/media; matched mount |
| Elbow output | — | **Priority** external abs (media path) |
| Wrist (3) | QDD or remote drive | **Priority** external abs at bevel outputs |

Smoke axis: motor encoder only is enough to close FOC bring-up.

---

## 6. Reject / avoid (encoders)

- Sealed proprietary joint pods without replaceable sensor  
- Optical disks as default in open FDM structure  
- Relying on SteadyWin “secondary encoder” **alone** to satisfy E-M3 without reading the actual function (power-off memory vs control feedback)  
- MoCap / external lab metrology as on-robot requirement  
- Joint torque cells as default (C2.4 out)

---

## 7. S2 fallback

Same policy: any remaining compliant span still wants **joint-output absolute**; shorter belts may delay wrist abs slightly, Phase-1 target unchanged.

---

## 8. Next

1. For chosen QDD SKU: one-row table **motor enc | secondary? | true output angle?** from manual.  
2. Pick **one** magnetic family (AS5047P or MT6701) for first joint-abs prototype + magnet.  
3. Feed C3.4 compute: SPI/SSI budget and CAN angle topics.  
4. After first joint abs bench: resolution vs assembly task (E-S3), not datasheet vanity.

---

## Document control

| Item | Value |
|------|--------|
| Closes | C3.3 **shortlist draft** |
| Does not close | Observer design, full harness, IMU for walk |

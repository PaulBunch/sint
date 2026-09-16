<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# Kinematic Scheme Selection — Down-select (Task 0004 / K5)

**Status:** Completed (Authoritative input for ADR-0005)  
**Parent task:** `docs/tasks/0004-kinematic-and-mechanical-scheme.md`  
**Normative inputs:** `docs/decisions/0003-core-numerical-characteristics.md`, `docs/decisions/0004-kinematic-survey-patterns.md`, `docs/tasks/0004-kinematic-constraints.md`, `docs/tasks/0004-placement-policy.md`, `docs/tasks/0004-candidate-schemes.md`

---

## 1. Shared Assumptions for All Scoring

To ensure an objective and fair evaluation, all candidate schemes (S1, S2, S3) are assessed under a unified, practical, and highly scoped set of assumptions aligned with the Phase 1 MVP boundaries:

* **Workspace & Reach:** The target cluster consists of a Bambu Lab A1-mini printer (bed area $180 \times 180 \text{ mm}$, maximum Z height $180 \text{ mm}$), an assembly table buffer, and a tool bay. 
* **Relocatable MVP (Coplanar Only):** Locomotion is strictly coplanar. The arm transitions between **$\ge 2$ docks arranged on a single flat surface** (the table/rail assembly). The spacing between dock centers must fit within the achievable **dual-dock kinematic span** during a valid transition pose (typically $0.5\text{--}0.7\text{ m}$ for an arm with a nominal reach of $0.5\text{--}0.8\text{ m}$). 
* **Out of Scope for Scoring:** Vertical climbing, wall/ceiling mounting, biped-style stair/gap climbing, or using the wrist roll/pitch actuators as primary hoisting winches for body-weight-class loads are explicitly ignored. No scheme is rewarded or penalized for non-coplanar or heavy climbing capabilities.
* **Adherence to Placement Policy:** All schemes must respect the physical constraints of their joint torque classes. In asymmetric schemes (S1, S2), the lightweight distal wrist (torque class $1\text{--}5\text{ N}\cdot\text{m}$) cannot bear cantilever walking loads. Locomotion for S1 and S2 is executed via a robust base-segment auxiliary docking latch (base dual-contact overlap), transferring all bending moments directly to the powerful proximal base joints (J1/J2) and dedicated structural latches.

---

## 2. K5.1 Scorecard

Each scheme is scored on a scale of **1 to 5** (where 5 is optimal/lowest risk, and 1 is unacceptable/highest risk). Any failure of a DFAA veto (V1–V8) results in immediate disqualifying score (1) in the respective category.

| Evaluation Criterion | S1 (Modular In-Joint) | S2 (Cascaded Mass Bias) | S3 (Symmetric Dual-Ended) |
| :--- | :---: | :---: | :---: |
| **DFAA (Design for Autonomous Assembly)** | **4** / 5<br>Clean boundaries; simple joint swaps; internal wiring routing is complex. | **3** / 5<br>Belt routing and tensioners are agent-accessible, but belt wear adds maintenance steps. | **4** / 5<br>Symmetric design reduces unique parts; identical end clusters are easy to assemble. |
| **Relocatable-base clarity (planar)** | **4** / 5<br>Relies on base aux-latch overlap; asymmetric ends make transition control simpler. | **4** / 5<br>Similar to S1; low forearm mass simplifies positioning during docking. | **5** / 5<br>Natively dual-ended; either end serves as base or EE; perfect symmetry for walk. |
| **Payload/inertia (N3/N5)** | **3** / 5<br>In-joint distal motors add mass to forearm, reducing effective continuous payload. | **5** / 5<br>Distal motors shifted proximally; minimal arm inertia; highest effective payload. | **2** / 5<br>Must carry heavy proximal-class motors on BOTH ends; high distal mass when acting as EE. |
| **Complexity** | **4** / 5<br>Low; standard 6-DoF serial arm; direct-drive or integrated gearbox joints. | **3** / 5<br>Medium; requires timing belt runs, tensioners, and open-channel routing. | **3** / 5<br>Medium; 7-DoF kinematically redundant; dual high-current power/data interfaces. |
| **BOM Risk** | **4** / 5<br>6 actuator pods; lower torque distal motors are highly affordable. | **4** / 5<br>6 motors; timing belts and pulleys are extremely low-cost COTS parts. | **2** / 5<br>Requires 7 proximal-class actuator pods and 2 expensive universal docking ends; high risk of exceeding $1000. |
| **Acoustic Risk** | **4** / 5<br>Low; quiet FOC BLDC pods; minimal long-distance mechanical noise paths. | **3** / 5<br>Medium; timing belt resonance and open-channel acoustics require physical dampening. | **4** / 5<br>Low; quiet FOC BLDC pods used throughout; no belt paths. |
| **Fit ADR-0003** | **4** / 5<br>Fits reach, payload, and cost targets; transit battery fits on Link 1. | **5** / 5<br>Excellent fit; maximizes N3 payload and N5 torque/speed margins; default policy. | **2** / 5<br>Exceeds $1000 BOM target (N7); excessive mass limits continuous payload to <0.5 kg. |
| **TOTAL SCORE** | **27** | **28** | **22** |

---

## 3. K5.2 Order-of-Magnitude Analysis

### 3.1 Static Load and Torque Calculations (Physical Baseline)
To ground the torque checks, we define a realistic mass model for a $0.5 \text{ kg}$ payload and $0.8 \text{ m}$ maximum reach:
* **Payload ($m_{pl}$):** $0.5 \text{ kg}$
* **End-Effector / Tool ($m_{ee}$):** $0.2 \text{ kg}$
* **Arm Structure (Links + Actuators/Belts):** 
  * For **S1** / **S2**: Arm mass is roughly distributed as $1.5\text{--}2.0 \text{ kg}$ total (Link 2: $0.8 \text{ kg}$, Link 3: $0.6 \text{ kg}$, Wrist: $0.2 \text{ kg}$).
  * For **S3**: Fully symmetric, carrying heavy actuator clusters on both ends. Total arm mass is roughly $2.5\text{--}3.0 \text{ kg}$.

#### Peak Static Bending Moment at Base (J2 Shoulder Pitch) at full $0.8 \text{ m}$ extension:
$$T_{static} = \left( (m_{pl} + m_{ee}) \cdot g \cdot L_{total} \right) + \sum \left( m_{link, i} \cdot g \cdot L_{cg, i} \right)$$

Assuming simplified center of gravity ($L_{cg}$) at the midpoint of each link:
1. **S1 (Modular In-Joint):**
  * $L_2 = 0.35 \text{ m}$, $L_3 = 0.35 \text{ m}$, $L_{wrist} = 0.1 \text{ m}$.
  * $T_{static} \approx \left( 0.7 \text{ kg} \cdot 9.81 \cdot 0.8 \text{ m} \right) + \left( 0.8 \text{ kg} \cdot 9.81 \cdot 0.175 \text{ m} \right) + \left( 0.6 \text{ kg} \cdot 9.81 \cdot 0.525 \text{ m} \right) \approx 5.49 + 1.37 + 3.09 \approx \mathbf{9.95 \text{ N}\cdot\text{m}}$
  * With a dynamic/safety multiplier of $1.5\times\text{--}2.0\times$, the required continuous torque is **$15\text{--}20 \text{ N}\cdot\text{m}$**. This fits the $10\text{--}25 \text{ N}\cdot\text{m}$ proximal target.

2. **S2 (Cascaded Mass Bias):**
  * Distal wrist mass is halved ($0.1 \text{ kg}$ instead of $0.2 \text{ kg}$ due to cascaded motors in Link 3).
  * $T_{static} \approx \left( 0.7 \text{ kg} \cdot 9.81 \cdot 0.8 \text{ m} \right) + \left( 0.8 \text{ kg} \cdot 9.81 \cdot 0.175 \text{ m} \right) + \left( 0.5 \text{ kg} \cdot 9.81 \cdot 0.5 \text{ m} \right) \approx 5.49 + 1.37 + 2.45 \approx \mathbf{9.31 \text{ N}\cdot\text{m}}$
  * Slightly lower static torque at the shoulder, but drastically lower joint inertia at J3 and J4, meaning significantly lower dynamic torque spikes and motor power consumption during rapid movement.

3. **S3 (Symmetric Dual-Ended):**
  * S3 must carry a $0.8 \text{ kg}$ actuator cluster at its active distal end.
  * $T_{static} \approx \left( (0.5 + 0.2 + 0.8) \text{ kg} \cdot 9.81 \cdot 0.8 \text{ m} \right) + \text{link weights} \approx 11.77 + 4.5 \approx \mathbf{16.27 \text{ N}\cdot\text{m}}$
  * With a safety factor, the base shoulder joint J2 requires **$\ge 25\text{--}30 \text{ N}\cdot\text{m}$** continuous. This pushes the proximal actuators to their absolute thermal and mechanical limit under ADR-0003 constraints, demanding heavier, more expensive motors and violating the $1000 BOM cap (N7).

---

### 3.2 Scheme S1 — Serial 6-DoF Modular In-Joint
* **Printable Segments vs. Size Limit ($\le 175\text{--}180 \text{ mm}$):**
  * Nominal link lengths: Link 2 (Upper Arm) = $300 \text{ mm}$, Link 3 (Forearm) = $300 \text{ mm}$.
  * Each link is split into exactly 2 printable segments ($150 \text{ mm}$ each), which comfortably fits the $175 \text{ mm}$ limit. Assembly via robust interlocking mating joints with transverse steel hardware pins.
* **Rough Torque Check (Proximal vs. Distal):**
  * Distal Wrist (J4, J5, J6): Carry local NEMA 11-size equivalent BLDC motors with planetary gearboxes. Combined wrist assembly weight $\approx 0.35 \text{ kg}$.
  * Max static torque on J4 forearm roll is negligible ($\le 0.5 \text{ N}\cdot\text{m}$); J5 wrist pitch must handle payload + tool moment arm: $0.7 \text{ kg} \times 9.81 \times 0.1 \text{ m} = 0.68 \text{ N}\cdot\text{m}$.
  * Distal continuous torque target of $1\text{--}3 \text{ N}\cdot\text{m}$ provides a solid $1.5\times\text{--}3\times$ safety margin.
* **Dock Spacing vs. Dual-Dock Reach:**
  * S1 nominal stick reach is $0.65\text{ m}$. To perform a relocatable walk, the arm must bend into a closed "arch" pose to engage the base auxiliary latch on Dock B while rooted at Dock A.
  * The maximum geometric span between Dock A and Dock B that allows dual-dock overlap with a comfortable kinematic margin is **$0.45\text{--}0.55\text{ m}$**. 
  * If Dock A is located at the center-left of the A1-mini printer bed, Dock B can be placed at $0.5 \text{ m}$ spacing on the table. S1 can step between them natively without intermediate steps.

---

### 3.3 Scheme S2 — Serial 6-DoF Cascaded Mass Bias (Default Policy)
* **Printable Segments vs. Size Limit ($\le 175\text{--}180 \text{ mm}$):**
  * Nominal link lengths: Link 2 = $320 \text{ mm}$, Link 3 = $300 \text{ mm}$.
  * Each link shell is segmented into 2 halves ($160 \text{ mm}$ and $150 \text{ mm}$ respectively).
  * Because S2 carries internal timing belt runs, the printed shells act as "structural channels." Split-lines are designed with integrated reinforcement bulkheads to prevent structural flexing under belt pre-tensioning.
* **Rough Torque Check (Proximal vs. Distal):**
  * Forearm roll (J4), wrist pitch (J5), and wrist roll (J6) actuators are grouped into a "motor pack" located at the very base of Link 3 (elbow joint). Wrist weight drops to a mere $0.12 \text{ kg}$.
  * The distal wrist torque of $1\text{--}3 \text{ N}\cdot\text{m}$ is fully maintained via short, high-efficiency GT2 timing belts ($2\text{ mm}$ pitch, $6\text{ mm}$ width, fiberglass reinforced).
  * The J3 elbow pitch actuator is located at the base of Link 2 (shoulder joint), reducing Upper Arm dynamic inertia.
  * J3 continuous torque is $10\text{--}15 \text{ N}\cdot\text{m}$. Driven by a proximal BLDC pod via a $3:1$ secondary timing belt reduction, the physical actuator needs to output only $3\text{--}5 \text{ N}\cdot\text{m}$ locally, reducing actuator size and thermal load.
* **Dock Spacing vs. Dual-Dock Reach:**
  * With a slightly longer Link 2 ($320 \text{ mm}$), S2 nominal reach is $0.70 \text{ m}$.
  * The achievable dual-dock span for step transitions is **$0.50\text{--}0.60\text{ m}$**. 
  * This spacing fits perfectly into a single-cluster desktop footprint, allowing Dock A to service the printer bed while Dock B directly overlooks the assembly table and tool bay.

---

### 3.4 Scheme S3 — Symmetric Dual-Ended Walking Manipulator
* **Printable Segments vs. Size Limit ($\le 175\text{--}180 \text{ mm}$):**
  * Nominal link lengths: Link 1 = $350 \text{ mm}$, Link 2 = $350 \text{ mm}$.
  * Each link is segmented into 2 structural tubes of $175 \text{ mm}$ each. Fits the print bed limit, but the higher structural loading of S3's dual-ended walking requires carbon-fiber reinforced filament (PA-CF) or thicker walls, increasing dead-weight.
* **Rough Torque Check (Proximal vs. Distal):**
  * To allow either end to serve as a base, terminal joint clusters (J1–J3 and J5–J7) must use identical proximal-class $20\text{--}25 \text{ N}\cdot\text{m}$ actuators.
  * S3 must carry $3 \text{ kg}$ of total arm weight. When rooted at End-A, the joint J2 must lift Link 1, J4, Link 2, the heavy End-B cluster ($0.8 \text{ kg}$), and the $0.5 \text{ kg}$ payload.
  * Required torque at J2 under full extension: $\approx \mathbf{16.3 \text{ N}\cdot\text{m}}$ static. Adding dynamic acceleration spikes, the system requires $\ge 25\text{--}30 \text{ N}\cdot\text{m}$ of actuator capability. This is a severe thermal bottleneck for 3D-printed/COTS modular gearboxes.
* **Dock Spacing vs. Dual-Dock Reach:**
  * Nominal reach is $0.80 \text{ m}$ (stretch up to $1.0 \text{ m}$). 
  * Due to the 7-DoF redundancy and symmetric ends, the maximum dual-dock walking step span is **$0.60\text{--}0.70\text{ m}$**. 
  * While S3 has the largest step reach, it does so at the cost of a massive weight, thermal, and cost penalty.

---

## 4. K5.3 Recommendation & Down-Select Decision

Based on the scorecard results and physical order-of-magnitude analysis, the schemes are ranked as follows:

### Rank 1: Scheme S2 — Serial 6-DoF Cascaded Mass Bias
* **Why it wins:** S2 represents the absolute best compromise between physical performance and project constraints. Shifting the heavy actuator mass proximally reduces distal inertia, lowering the torque requirements of the base joints, minimizing structural deflection, and maximizing effective payload capacity. The timing belt transmissions are kept fully open and accessible via snap-on plastic covers, satisfying the DFAA V5 maintenance veto. It perfectly fits Power Scenario A, allowing a non-symmetric, lightweight wrist end.
* **Target Spacing:** $0.50\text{--}0.60 \text{ m}$ planar dock spacing.

### Rank 2: Scheme S1 — Serial 6-DoF Modular In-Joint
* **Why it is a strong backup:** S1 is kinematically identical to S2 but uses direct, in-joint actuator pods. It is mechanically simpler (no timing belt runs to align or tension) and has slightly lower acoustic risk. However, carrying distal motors directly at the joint pivots increases shoulder torque demand and slightly reduces maximum payload capacity. S1 remains a highly viable secondary option if timing belt slippage or pre-tensioning issues arise in S2.
* **Target Spacing:** $0.45\text{--}0.55 \text{ m}$ planar dock spacing.

### Rank 3: Scheme S3 — Symmetric Dual-Ended Walking Manipulator
* **Why it is deferred/rejected for Phase 1:** S3 represents an elegant, symmetric "pure walking" concept (Canadarm-style). However, carrying heavy, high-torque proximal actuators on both ends is extremely inefficient. The active end-effector end becomes excessively heavy, which dramatically inflates the shoulder torque requirements to lift the arm itself. To build S3 under a $\$1000$ BOM limit is virtually impossible with current COTS/FDM BLDC technologies.
* **Decision:** S3 is deferred to Phase 2 (or a future scale-up) and is officially excluded from the Phase 1 implementation baseline.

### Next Step for human decision (ADR-0005):
Accept **Scheme S2** as the primary physical architecture for the `sint` interface. Detail the joint layout, link segment joins, and belt channel access covers in the upcoming ADR-0005.

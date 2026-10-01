# Motor catalog sources (C3.1)

- **SoT numbers:** [`0005-motors-catalog.csv`](0005-motors-catalog.csv)
- **Scraped / notes:**
  - iPower: https://iflight-rc.eu/en-fr/collections/gimbal-motors
  - T-Motor: https://store.tmotor.com/categorys/gimbal-motor
  - Fulling: https://www.fullingmotor.com/en/product
  - CubeMars: https://www.cubemars.com/categorys/product
  - SteadyWin: https://steadywin-motor.com/collections/all
- **Caveats:**
  - iPower/T-Motor «load torque» ≠ industrial continuous stall — treat as optimistic
  - J_rotor often missing for gimbal; Fulling BLW often publishes J
  - **CubeMars / Fulling iSVD / SteadyWin / similar QDD:** `torque_rated_nm` is **output** (after built-in N); integrated FOC + encoder(s) unless noted (e.g. AKE* = motor+G, **no** driver)
  - **J_rotor on CubeMars AK*:** treat as **motor-side**; joint reflected inertia scales ~\(J N^2\) (+ gearbox). Do not treat catalog J as output inertia
  - Prefer **N ≈ 6…15** for MVP QDD; models with N ≥ ~36 (AK45-36, AK60-39, AK80-64, AKH70-48, …) are non-default
  - Bus: gimbal ~12–20 V; many QDD modules **24/48 V** — check vs ADR; 24 V driver must not be fed 48 V
  - `role_hint` is provisional until shortlist down-select
  - Prices in notes are list/OOM only; RU availability and landed cost are separate gates

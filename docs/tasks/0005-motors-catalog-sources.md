# Motor catalog sources (C3.1)

- **SoT numbers:** [`0005-motors-catalog.csv`](0005-motors-catalog.csv)
- **Scraped / notes:**
  - iPower: https://iflight-rc.eu/en-fr/collections/gimbal-motors
  - T-Motor: https://store.tmotor.com/categorys/gimbal-motor
  - Fulling: https://www.fullingmotor.com/en/product
- **Caveats:**
  - iPower/T-Motor «load torque» ≠ industrial continuous stall — treat as optimistic
  - J_rotor often missing for gimbal; Fulling BLW often publishes J
  - Fulling iSVD* = integrated FOC + gearbox; **output** torque already reduced (N built-in)
  - Bus: many gimbal ~12–20 V; Fulling iSVD often **48 V** — check vs ADR 24 V
  - `role_hint` is provisional until shortlist down-select

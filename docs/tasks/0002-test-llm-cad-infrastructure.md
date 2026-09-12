# Task: Test LLM + build123d infrastructure

**Status:** open  
**Related:** docs/decisions/0001-cad-tooling-and-llm-interaction.md, docs/build123d-guidelines.md, scripts/cad-show.py, scripts/cad-export.py  
**Goal:** Verify that the current tooling allows an LLM agent to design, run, export and iteratively fix mechanical parts with minimal human help.

## Context

- Primary CAD stack is build123d (OpenCASCADE).
- Model scripts must stay pure (no ocp_vscode / show calls).
- Viewer: `scripts/cad-show.py`
- Headless export: `scripts/cad-export.py` → STEP (source of truth) + optional STL
- Guidelines for the agent: `docs/build123d-guidelines.md`

## Test scenarios (minimum)

### S1 — Parametric plate [COMPLETED 2026-09-13]
- Rectangular plate with 4 mounting holes and edge fillet/chamfer.
- All key dimensions as named constants at the top of the file.
- Located at: `hardware/s1_parametric_plate.py`
- Exported files: `hardware/s1_parametric_plate.step`, `hardware/s1_parametric_plate.stl`
- Number of LLM iterations: **2**

### S2 — Simple joint-like module
- Housing / flange with bore, bolt circle, optional pocket or boss.
- Closer to real sint joint geometry (still simplified).

### S3 — Mini assembly (optional but desirable)
- 2–3 bodies combined via `Compound` or located copies.
- Check that multi-body export to STEP works cleanly.

## Execution protocol (per scenario)

1. **Generate**  
   LLM produces a pure `hardware/.../*.py` script following `build123d-guidelines.md`.

2. **Run / view**  
   ```bash
   python scripts/cad-show.py hardware/.../part.py
   ```

3. **Export**  
   ```bash
   python scripts/cad-export.py hardware/.../part.py
   # optional: --stl
   ```

4. **Inspect**  
   - Visual check (ocp-vscode)  
   - Open STEP in another viewer if needed  
   - Note topology errors, wrong selectors, bad fillets, etc.

5. **Fix loop**  
   Feed traceback / description of the problem back to the LLM.  
   Repeat until the part is correct or a clear blocker is found.

6. **Record**  
   - Number of LLM iterations  
   - Class of errors (selector, Mode, fillet radius, import, …)  
   - Final script + STEP committed under `hardware/`

## Success criteria

- [x] S1 completes with ≤ 2–3 LLM iterations in typical case (Completed in 2 iterations)
- [ ] S2 completes without manual rewriting of core logic
- [ ] `cad-export.py` reliably produces valid STEP
- [ ] Scripts stay pure and guidelines are sufficient (or gaps are documented)

## Deliverables

1. Working example scripts + STEP files under `hardware/` for S1–S2 (and S3 if done)
2. Short notes in `docs/conversations/`:
   - what worked
   - what guidelines/scripts need improvement
3. Decision: infrastructure is ready for regular agent use / needs specific follow-up tasks

## Out of scope for this task

- Final choice between build123d features vs CadQuery (already decided)
- Full CI rendering pipeline (can be a follow-up)
- Real kinematic joint of the robot (comes later)

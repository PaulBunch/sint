---
title: Component composition (COTS candidates)
date_created: 2026-09-17
date_updated: 2026-09-17
participants: [Bunch, Grok]
status: open
language: ru
tags: [components, COTS, S2]
related:
  - docs/tasks/0005-component-composition.md
  - docs/decisions/0003-core-numerical-characteristics.md
  - docs/decisions/0005-kinematic-scheme.md
  - docs/tasks/0004-placement-policy.md
  - docs/implementation-concepts.md
---

# Component composition — discussion

## Summary

(Заполняется перед закрытием: shortlist классов, спорные SKU, BOM risk.)

## Goals for this workstream

- Подобрать **COTS-кандидатов** (не единственный вечный SKU) под схему **S2** (ADR-0005).
- Уложить в ADR-0003: torque bands, 24 V class, N6 acoustics, N7 BOM, DFAA replaceable modules.
- Зафиксировать baseline composition ADR; детали закупки — после.

## Non-goals

- Полный joint CAD / belt channel drawings
- Финальный freeze одной марки на 5 лет
- Wall/ceiling climb actuators
- Собственный ASIC / закрытый SCA-клон без repair path

## Discussion

---
**2026-09-17**
---

---
**Grok 4.5 Fast**

## Kickoff

Инфраструктура: task `0005-component-composition.md`.  
Входы: ADR-0003, ADR-0005 (S2 cascade), placement policy, implementation-concepts (GLUON quiet FOC, printable actuator ideas, SimpleFOC-class).

---

---
title: 
date_created: 2026-09-06
date_updated: 2026-09-12
participants: [Bunch, Grok]
status: open
closed_reason:
language: ru
tags: [cad, tasks]
related:
  - docs/decisions/0001-cad-tooling-and-llm-interaction.md
---

# 

## Summary


## Discussion

---
**2026-09-06**
---

---
**Bunch**

В ROADMAP проекта:
https://github.com/PaulBunch/sint
Есть задача:
```md
- [ ] Select CAD software (and other required tools) that LLM can interact with independently with minimal human assistance
```

Какие у тебя есть пожелания на этот счёт?

Для быстрой синхронизации с проектом можешь ознакомиться с AGENITS.md

Я думаю, для выбора CAD нужно в первую очередь опираться на open source инструменты с учётом возможного заимстования необходимого функционала у проприетарных проектов. Например, для выбора формата сохранения было бы неплохо рассмотреть варианты, которые позволяют создать подобие git сохранения для деталей и узлов. Такая фишка релизована в CAD onshape. Как думаешь, можно реализовать подобный функционал используя исключительно открытые инструменты и форматы?

---
**Grok 4.5 Fast**

**Да, open-source first + возможность git-like версионирования — правильный приоритет для sint.**

Проект находится в Phase 1 (Foundation & Planning). Ключевое требование к CAD/инструментам: LLM/агент должен работать с ними **самостоятельно с минимальной помощью человека**. Это сильно ограничивает выбор (GUI-heavy проприетарные CAD почти сразу выпадают).

### Мои пожелания / критерии выбора

1. **Максимальная LLM-friendly-ность**  
   Предпочтение code-CAD / Python/TS-скриптам, а не GUI. LLM отлично пишет/чинит код, плохо «щёлкает мышью». Идеально: headless-режим + структурированный вывод (ошибки, метрики, рендеры, diff геометрии) + MCP/CLI.

2. **Open-source + зрелое ядро**  
   OpenCASCADE (через CadQuery / build123d / FreeCAD / OCP / Replicad) — практически безальтернативная база. OpenSCAD проще для старта, но слабее для сложных сборок, сопряжений и downstream-задач.

3. **Экспорт в нормальные форматы**  
   STEP/BREP как основной обменный формат + STL/3MF для печати + возможность параметрического исходника в репозитории.

4. **Хорошая интеграция с симуляцией**  
   MuJoCo / Isaac (уже упомянуты в ROADMAP) + возможность быстрого экспорта кинематики/мешей.

5. **Версионирование и diff**  
   Как раз то, что ты поднял.

### Можно ли сделать git-like версионирование (как в Onshape) на открытых инструментах?

**Да, и довольно близко.** Onshape даёт feature-level history, branching/merging и визуальные 3D-diff прямо в модели. Полного 1-в-1 open-source аналога нет, но практически полезный уровень достигается.

Реалистичные варианты:

- **Code-CAD + обычный Git** (самый чистый и мощный путь для агентов)  
  CadQuery / build123d / OpenSCAD / Replicad. Исходник — текст.  
  - Идеальные diff’ы, branching, PR-review, CI (рендер превью, проверка сборки, экспорт STEP/STL).  
  - Агент может сам править код, запускать, смотреть ошибки/рендеры, откатывать.  
  - Для сборок/узлов — модульная структура файлов + параметрические скрипты.  
  Это ближе всего к «git для деталей».

- **FreeCAD + Git + дополнительные инструменты**  
  - Есть History Workbench / DiffCAD-подобные проекты, которые дают 3D-сравнение и сравнение дерева модели.  
  - Python API + headless + MCP-серверы уже существуют (есть рабочие примеры автоматизации через FastMCP).  
  - Файлы `.FCStd` бинарные → для нормального Git лучше хранить Python-макросы / скрипты генерации + экспорт STEP.  
  - Можно добавить собственный слой истории поверх.

- **Другие подходы**  
  - Текстовые/YAML/JSON-описания модели + детерминированный «компилятор» в геометрию (идеи вроде SplitCAD).  
  - Кастомный feature-tree в текстовом виде поверх OpenCASCADE.  
  - Git LFS + автоматическая генерация превью и 3D-diff в CI.

Что **сложно** повторить на 100 %:
- Настоящий feature-level merge с автоматическим разрешением конфликтов геометрии (как в Onshape).
- Полностью визуальный 3D-diff прямо в интерактивной среде без дополнительной работы.

Но для агентного workflow это не критично. Агенту гораздо удобнее работать с кодом + структурированными отчётами («вот что изменилось в геометрии, вот diff параметров, вот рендер с цветовой подсветкой изменений»), чем с GUI-историей.

### Конкретные рекомендации по стеку (на текущий момент)

**Основной кандидат:**
- **CadQuery** или **build123d** (оба на OpenCASCADE) + Git + CI (рендеры, экспорт, проверки).
- Для ещё большей LLM-дружелюбности — посмотреть **llmcad** (минимальный API специально под LLM).
- FreeCAD — как второй вариант / для тех случаев, когда нужен более «классический» parametric tree и уже есть MCP-обвязки.

**Дополнительно:**
- OpenSCAD — только для очень простых деталей (быстрый старт, отличный Git-дифф).
- Replicad (WASM) — если захочется браузерный/лёгкий runtime.
- Обязательно предусмотреть headless-рендер (PNG/viewport) и экспорт STEP/STL, чтобы агент мог «видеть» результат.

**Версионирование узлов:**
- Каждый модуль/joint/link — отдельный параметрический скрипт + STEP-экспорт.
- Сборки — отдельные скрипты, которые импортируют модули.
- Всё лежит в `hardware/` (или `cad/`) и живёт в обычном Git. Агент может делать ветки, PR, откаты полностью самостоятельно.

### Что я бы предложил сделать дальше

1. Зафиксировать критерии в ADR (LLM-friendliness, open-source, Git-native, headless, экспорт, симуляция).
2. Провести короткое сравнительное исследование 3–4 кандидатов (CadQuery/build123d, FreeCAD+MCP, OpenSCAD, возможно llmcad/Replicad) с простым тестовым заданием: «агент должен сгенерировать, параметризовать, собрать и экспортировать простой joint module».
3. Выбрать primary + fallback.
4. Сразу заложить структуру репозитория под code-CAD + CI-превью.

Если хочешь, могу помочь набросать черновик ADR по выбору CAD или список конкретных тестовых сценариев для оценки кандидатов.

---
**Bunch**

С FreeCAD я знаком. LLM чере з MCP не подключал, но писал python скрипты для FreeCAD при помощи LLM.

1. Дай ссылки на репозитарии или официальные сайты основных CAD-кандидатов. Все вырианты которые ты перечислил работают на движке OpenCASCADE?
2. STEP и BREP это текстовые форматы? Я склоняюсь больше к твёрдотельным форматом (типа STEP) — они больше подходят для инженерных разработок, нежели STL с его треугольниками. STL можно использовать для специализированных задач, но источником истины должны быть твёрдотельные типы файлов.
3. При выборе инструементов стоит сразу учитывать смежные инструменты для проектирвоания печатных плат, а также двухмерных схем? И более того: проведение численных расчётов конструкции (прочностных, тепловых, механических и т.п.)?
4. Так как эта задача достаточна объёмная, предлагаю разбить её на подзадачи. Составиь чек-лист список подзадач.

---
**Grok 4.5 Fast**

Отвечаю по пунктам.

### 1. Ссылки на основные CAD-кандидаты и ядро

| Инструмент | Ссылки | Ядро |
|------------|--------|------|
| **CadQuery** | [GitHub](https://github.com/CadQuery/cadquery), [сайт/docs](https://cadquery.readthedocs.io/) | **OpenCASCADE (OCCT)** через OCP |
| **build123d** | [GitHub](https://github.com/gumyr/build123d), [docs](https://build123d.readthedocs.io/) | **OpenCASCADE (OCCT)** |
| **FreeCAD** | [сайт](https://www.freecad.org/), [GitHub](https://github.com/FreeCAD/FreeCAD) | **OpenCASCADE (OCCT)** |
| **llmcad** | [сайт](https://llmcad.org/), [GitHub](https://github.com/llmcad/llmcad) | **OpenCASCADE (OCCT)** через OCP |
| **Replicad** | [сайт](https://replicad.xyz/), [GitHub](https://github.com/sgenoud/replicad) | **OpenCASCADE (WASM)** |
| **OpenSCAD** | [сайт](https://openscad.org/), [GitHub](https://github.com/openscad/openscad) | **Нет** — CGAL (mesh/CSG), не B-rep |

**Итог:** CadQuery, build123d, FreeCAD, llmcad и Replicad — все на OpenCASCADE. OpenSCAD — отдельная история (mesh-based CSG). Для инженерного твёрдотельного моделирования и STEP как источника истины OpenCASCADE-варианты предпочтительнее.

---

### 2. STEP и BREP — текстовые ли?

**STEP (ISO 10303, файлы `.step` / `.stp`):**
- Стандартное представление — **текстовый ASCII** (ISO 10303-21 Clear Text Encoding).
- Файл начинается с `ISO-10303-21;` и содержит HEADER + DATA с сущностями.
- Есть и бинарные варианты, но на практике почти всегда используют текстовый.
- Это именно **B-rep** (boundary representation) — точная математическая геометрия (плоскости, цилиндры, NURBS и т.д.), а не треугольная сетка.

**BREP (нативный формат OpenCASCADE):**
- Есть **ASCII**-вариант (`BRepTools`) и **бинарный** (`BinTools`).
- Хранит топологию и геометрию OpenCASCADE.

**Вывод для sint:**  
Согласен полностью. **STEP (B-rep)** должен быть основным обменным и архивным форматом — источником истины. STL/3MF — производные для печати, слайсинга, быстрой визуализации. Параметрический исходник (Python/TS-скрипт) + STEP-экспорт даёт и Git-friendly версионирование, и инженерную точность.

---

### 3. Учитывать ли PCB, 2D-схемы и численные расчёты сразу?

**Кратко: учитывать в критериях и архитектуре — да, выбирать всё сразу — нет.**

- **PCB / электроника**  
  Основной open-source стек — **KiCad**.  
  Интеграция с механикой обычно через STEP-экспорт корпуса/платы + ручное или скриптовое сопоставление.  
  Полноценный ECAD-MCAD sync (как в проприетарных системах) в open-source пока слабый.  
  Для sint на ранних фазах достаточно: механический CAD умеет импортировать/экспортировать STEP, а платы живут в отдельном репозитории/папке.

- **2D-схемы / чертежи**  
  FreeCAD TechDraw, CadQuery/build123d → DXF/SVG, отдельный LibreCAD/QCAD.  
  Не критично на старте, но полезно заложить экспорт 2D.

- **Численные расчёты (FEM, тепло, механика)**  
  - FreeCAD имеет встроенный FEM workbench (CalculiX и др.).  
  - Отдельно: CalculiX, Code_Aster, FEniCS, OpenFOAM (CFD), Gmsh и т.д.  
  - Современный путь: STEP → mesh → солвер.  
  Для агентного workflow важнее возможность **скриптового** пайплайна (экспорт геометрии → генерация сетки → запуск расчёта → парсинг результатов), чем GUI.

**Рекомендация:**  
В критерии выбора CAD добавить:
- качественный STEP import/export;
- возможность headless/скриптовой работы;
- лёгкость интеграции с внешними mesh/FEM-инструментами.

Выбор конкретного FEM/CFD-стека и KiCad-процесса — отдельные подзадачи Phase 1–2, не блокирующие выбор основного CAD.

---

### 4. Чек-лист подзадач (разбиение задачи выбора CAD)

```markdown
## Подзадачи: Select CAD software (and related tools)

### A. Критерии и рамки
- [ ] A1. Зафиксировать обязательные критерии (LLM-friendliness, open-source, headless/CLI/MCP, STEP как SoT, Git-native, экспорт STL/3MF, скриптовость)
- [ ] A2. Зафиксировать желательные критерии (сборка/assemblies, named faces/edges, интеграция с FEM, PCB/STEP, симуляция MuJoCo/Isaac)
- [ ] A3. Определить приоритеты (что must-have vs nice-to-have для Phase 1–2)
- [ ] A4. Создать черновик ADR «CAD Tool Selection» (пока без финального выбора)

### B. Исследование кандидатов
- [ ] B1. CadQuery — зрелость, API, LLM-опыт, assemblies, экспорт, headless
- [ ] B2. build123d — сравнение с CadQuery, стиль API, документация, экосистема
- [ ] B3. FreeCAD (Python API + headless + MCP) — возможности, ограничения, FEM
- [ ] B4. llmcad — насколько минималистичный API реально помогает LLM
- [ ] B5. Replicad — браузерный/TS-вариант, ограничения WASM
- [ ] B6. OpenSCAD — только как baseline/fallback для простых деталей
- [ ] B7. Сводная сравнительная таблица (критерии × кандидаты)

### C. Практические тесты (минимальный benchmark)
- [ ] C1. Определить 2–3 тестовых сценария (например: простой joint module, parametric plate + holes + fillet, простая assembly из 2–3 деталей)
- [ ] C2. Для каждого кандидата: генерация скрипта LLM → запуск → STEP + STL + screenshot/viewport
- [ ] C3. Оценка: сколько итераций нужно LLM, качество геометрии, удобство отладки, стабильность
- [ ] C4. Проверка Git-workflow (diff скрипта, CI-рендер, экспорт)

### D. Смежные инструменты (учёт, не полный выбор)
- [ ] D1. PCB: подтвердить KiCad как основной, проверить STEP-обмен с выбранным CAD
- [ ] D2. 2D/чертежи: минимальные требования (DXF/SVG/TechDraw)
- [ ] D3. FEM/тепло/механика: список кандидатов (FreeCAD FEM, CalculiX, Gmsh…) и требования к геометрии (STEP → mesh)
- [ ] D4. Симуляция: совместимость экспорта с MuJoCo / Isaac (меши, коллизии, инерция)

### E. Версионирование и структура репозитория
- [ ] E1. Предложить структуру `hardware/` (или `cad/`) под code-CAD + STEP
- [ ] E2. Описать workflow: скрипт → STEP (SoT) → STL/3MF (производные)
- [ ] E3. CI: автоматический рендер превью + проверка сборки STEP
- [ ] E4. Оценить возможность 3D-diff / history (History Workbench, кастомные скрипты)

### F. Решение и фиксация
- [ ] F1. Выбрать primary CAD + fallback
- [ ] F2. Заполнить ADR с обоснованием
- [ ] F3. Обновить `docs/ROADMAP.md` и `docs/current-state.md`
- [ ] F4. Зафиксировать минимальный tool-chain (CAD + экспорт + просмотр + CI)
- [ ] F5. (Опционально) Набросать первые шаблоны модулей под выбранный CAD
```

Этот чек-лист можно прямо положить в `docs/conversations/` или в начало ADR и отмечать прогресс.

Если нужно — могу сразу набросать черновик ADR или более детальные тестовые сценарии для benchmark’а.

---
**Bunch**

Что такое headless-путь, о котором ты постояно упоминаешь? Если я правильно поинмаю, ты хочешь строить геометрию через код/скрипт. После написания скрипта, деталь будет сохранена в STEP, так? Но что означает headless?

---
**Grok 4.5 Fast**

**Headless** — это режим работы программы **без графического интерфейса** (без окон, кнопок, 3D-вьюпорта на экране).

### Простыми словами

Обычный путь (с GUI):
1. Открываешь FreeCAD / CQ-editor / другое окно.
2. Пишешь или загружаешь скрипт.
3. Смотришь модель мышкой, крутишь, жмёшь «Export to STEP».

**Headless-путь**:
1. Есть только скрипт (Python/TS).
2. Ты (или LLM-агент) запускаешь его из терминала / через API / в CI:
   ```bash
   python generate_joint.py --output joint.step
   ```
   или
   ```bash
   freecadcmd generate_joint.py
   ```
3. Программа **без единого окна** считает геометрию, сохраняет STEP (и при необходимости STL, PNG-превью, отчёт) и завершается.

Никакого монитора, мыши и GUI-процесса не требуется.

### Зачем это нужно в sint

- LLM/агент должен работать **самостоятельно**. Ему неудобно «нажимать кнопки» в окне.
- Агент может в цикле:
  1. Сгенерировать/поправить скрипт,
  2. Запустить его headless,
  3. Получить STEP + скриншот + лог ошибок,
  4. Проанализировать результат и исправить код.
- То же самое можно запускать в CI, на сервере, в Docker, на машине без дисплея.

### Как это выглядит на практике

| Инструмент       | Headless-пример |
|------------------|-----------------|
| CadQuery / build123d | Обычный `python script.py` (они изначально библиотеки) |
| FreeCAD          | `freecadcmd script.py` или `FreeCADCmd` |
| OpenSCAD         | `openscad -o part.stl part.scad` |
| Replicad         | Node.js / WASM в worker’е без браузерного UI |

### Связь со STEP

Да, твоё понимание верное:

1. Источник истины для параметров и логики — **скрипт** (хорошо ложится в Git).
2. После выполнения скрипта (обычно headless) получается **STEP** — точная твёрдотельная геометрия (B-rep).
3. Из STEP уже можно делать STL для печати, сетку для FEM, импорт в другие CAD и т.д.

**Headless** — это просто способ **запустить** этот скрипт без графической оболочки, чтобы весь процесс мог управляться кодом/агентом.

---
**Bunch**

Теперь понятно. Полностью поддерживаю — LLM не должна нажимать на кнопки!

Подготовь ADR в соответствии с политиками проекта sint и тем, что мы здесь обсудили и решили. Где разместить этот ADR в структуре проекта?

---
**Grok 4.5 Fast**

**Размещение ADR**

По политикам проекта (`AGENTS.md`, `docs/long-term-memory.md`):

- Все Architecture Decision Records живут в **`docs/decisions/`**.
- Имя файла — kebab-case, обычно с номером:  
  `docs/decisions/0001-cad-tooling-and-llm-interaction.md`  
  (или `adr-0001-cad-tooling-and-llm-interaction.md` — на твой вкус; главное — единообразие).

Сейчас папки `docs/decisions/` в репозитории ещё нет — её нужно создать при первом коммите ADR.

Ниже готовый текст ADR в соответствии с тем, что мы обсудили и зафиксировали. Язык — английский (canonical). SPDX-заголовок добавлен.

```markdown
<!--
SPDX-FileCopyrightText: 2026 sint project contributors
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# ADR-0001: CAD Tooling Strategy for LLM-Autonomous Design

- **Status:** Accepted
- **Date:** 2026-09-06
- **Deciders:** Project maintainers / agents working on Phase 1
- **Related:** `docs/ROADMAP.md` (Phase 1 — Select CAD software…), `docs/spec.md`, conversation on CAD selection

## Context

sint requires that an LLM / VLA agent be able to design, modify, version, and export mechanical parts and assemblies with **minimal human assistance**.  

Traditional GUI-centric CAD tools force the agent into brittle “click the button” interaction, which is unreliable and hard to automate.  

Key constraints from the project:
- 100 % open / consumer-accessible tooling preferred.
- Designs must support Design-for-Autonomous-Assembly (DFAA).
- Geometry must be precise enough for engineering use (not just visual meshes).
- Everything should live comfortably in Git.
- Downstream needs: 3D printing (STL/3MF), possible FEM, PCB mechanical integration (STEP exchange), simulation (MuJoCo / Isaac).

## Decision

We adopt the following strategy for CAD and related geometry tooling:

1. **Primary paradigm: Code-CAD (script-driven geometry)**  
   Geometry is defined and generated by executable scripts (Python preferred).  
   The LLM writes, edits, and debugs code — not GUI actions.

2. **Headless execution is mandatory**  
   All generation, validation, export, and rendering must be runnable without a graphical interface (CLI / library call / CI).  
   This enables fully autonomous agent loops and server/CI usage.

3. **Source of truth hierarchy**
   - Parametric script (Python) — primary, Git-friendly source.
   - STEP (ISO 10303, B-rep) — canonical solid geometry exchange and archive format.
   - STL / 3MF — derived artefacts for printing and quick visualisation only.

4. **Preferred technology stack (OpenCASCADE-based)**  
   Primary candidates (all based on the OpenCASCADE kernel):
   - CadQuery
   - build123d
   - FreeCAD (via its Python API + headless mode)
   - llmcad (minimal LLM-oriented API on top of OCP)

   OpenSCAD is accepted only as a lightweight fallback for very simple parts (it is mesh/CSG-based, not true B-rep).

5. **Versioning model**  
   Git on the scripts + deterministic generation of STEP (and optional preview images) gives us a practical equivalent of “git for parts”.  
   Feature-level visual history like Onshape is desirable long-term but not required for the first milestones; it can be added later via additional tooling.

6. **Related domains (acknowledged, not decided yet)**
   - PCB: KiCad remains the expected open-source choice; mechanical integration via STEP.
   - 2D drawings / schematics: secondary; DXF/SVG export is sufficient for early phases.
   - Numerical simulation (FEM, thermal, etc.): will consume STEP → mesh; concrete solvers to be selected later.

## Options Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| GUI-only traditional CAD (FreeCAD GUI, etc.) | Mature feature set | Poor LLM autonomy, hard to headless, binary files | Rejected as primary |
| Pure OpenSCAD | Excellent Git diff, simple, headless | Mesh-based, weaker for complex engineering geometry & STEP fidelity | Fallback only |
| CadQuery / build123d / llmcad / FreeCAD Python | True B-rep, STEP, scriptable, headless, open-source | Learning curve, some topological naming issues | **Preferred family** |
| Proprietary cloud CAD (Onshape etc.) | Excellent versioning & collaboration | Not open, not self-hostable, LLM interaction limited | Out of scope |

## Consequences

### Positive
- LLM can operate in a tight edit → run-headless → inspect-STEP/screenshot → fix loop.
- Full history and branching via ordinary Git.
- High-quality solid geometry suitable for downstream engineering tasks.
- Aligns with DFAA and recursive improvement goals.

### Negative / Risks
- Agent must be good at writing and debugging CAD scripts (mitigated by choosing LLM-friendly APIs such as llmcad or well-documented CadQuery/build123d).
- Topological naming and robust feature identification remain challenging in OpenCASCADE-based tools.
- Initial setup of a reliable headless + CI preview pipeline requires some investment.

### Neutral
- Final choice among CadQuery / build123d / FreeCAD / llmcad is deferred to a short evaluation (benchmark scripts + LLM success rate). This ADR only locks the overall strategy.

## Implementation Notes (next steps)

- Create `docs/decisions/` and land this ADR.
- Run a small comparative evaluation of the OpenCASCADE-based candidates using 2–3 realistic joint/link examples.
- Define repository layout under `hardware/` (or `cad/`) for scripts + generated STEP.
- Add basic CI job that executes scripts headlessly and publishes STEP + preview images.
- Update `docs/ROADMAP.md` and `docs/current-state.md` once the concrete primary tool is selected.

## References

- Project ROADMAP Phase 1 task: “Select CAD software (and other required tools) that LLM can interact with independently with minimal human assistance”
- Discussion (2026-09-06) on open-source Code-CAD, STEP as source of truth, headless execution, and git-like versioning.
```

---

**Как использовать**

1. Создай папку `docs/decisions/`.
2. Положи туда файл `0001-cad-tooling-and-llm-interaction.md` (или с префиксом `adr-`).
3. После принятия можешь отметить соответствующий пункт в `docs/ROADMAP.md` как выполненный (или частично выполненный — стратегия принята, конкретный инструмент ещё выбирается).
4. При желании сразу создай запись в `docs/conversations/` со ссылкой на этот ADR и закрой её (`status: closed`, `closed_reason: decided`).

Если нужно — могу сразу подготовить также короткий патч для `current-state.md` / `ROADMAP.md` или шаблон следующего ADR по результатам benchmark’а кандидатов.

---
**2026-09-12**
---

---
**Bunch**

У нас есть высокоуровневый план в Roadmap. Имеет ли смысл создать в `docs/` директорию, например, `tasks/`, в которую будут помещаться чек‐листы с более атомарными задачами вроде `Подзадачи: Select CAD software (and related tools)`? Или лучше подзадачи размещать в ADR или такое смшенеие задач и ADR превратит нормативные ADR в кашу, потому что задачи по своей сути сущность более гибкая и текучая, чем зафиксированные решения? Если имеет смысл подзадачи выделять в отдельные документы, то как лучше именовать эти документы? Допустимо ли подзадачи вести на русском языке? Не усложнит ли это проект или это необходимая сложность для такого крупного проекта?

---
**Grok 4.5 Fast**

**Короткий ответ:**  
Отдельная директория для атомарных чек-листов **имеет смысл**, но **не стоит смешивать их с ADR**. ADR должны оставаться стабильными нормативными решениями. Задачи — текучая рабочая сущность.

### Почему не класть подзадачи внутрь ADR

| Сущность | Характер | Что должно происходить |
|----------|----------|------------------------|
| **ADR** | Нормативное решение | Приняли → зафиксировали → почти не трогаем (только статус или supersede) |
| **Подзадачи / чек-листы** | Операционная работа | Часто меняются, отмечаются, дробятся, откладываются, переписываются |

Если засовывать живые чек-листы внутрь ADR, документ быстро превращается в кашу: «решение» размывается деталями выполнения. Это противоречит самой идее ADR.

### Рекомендуемая структура

Оставить чёткое разделение:

```
docs/
├── ROADMAP.md              # высокоуровневые фазы (уже есть)
├── decisions/              # ADR — только решения
│   └── 0001-cad-tooling-and-llm-interaction.md
├── tasks/                  # ← новая директория (или work-packages/)
│   ├── 0001-select-cad-software.md
│   └── ...
├── conversations/          # сырые обсуждения
├── current-state.md
└── handoff-latest.md
```

**Альтернативные имена директории** (на выбор):
- `docs/tasks/` — просто и понятно
- `docs/work-packages/` — чуть более «инженерно»
- `docs/checklists/` — если хочется подчеркнуть чек-листную природу

Я бы выбрал **`docs/tasks/`**.

### Как именовать файлы задач

Рекомендуемый формат:

```
docs/tasks/NNNN-short-kebab-description.md
```

Примеры:
- `0001-select-cad-software.md`
- `0002-define-core-numerical-characteristics.md`
- `0003-evaluate-simulation-tools.md`

Внутри файла — чек-лист + ссылка на соответствующий пункт ROADMAP и (если есть) на ADR.

### Язык подзадач

По текущим правилам проекта:

- **Canonical documents** (`spec.md`, ADR, `current-state.md`, ROADMAP) → **English**
- Conversation files → могут быть на русском
- Agent notes → English или Russian

**Рекомендация:**  
Заголовки и структуру задач держать на **английском** (чтобы ROADMAP ↔ tasks ↔ ADR были согласованы).  
Тело чек-листа, комментарии и рабочие заметки **допустимо вести на русском**, особенно пока проект в основном ведётся тобой. Это не ломает систему и снижает трение.

Если позже появится больше англоязычных участников/агентов — можно ужесточить.

### Не усложнит ли это проект?

Для текущего масштаба (Phase 1, один основной контрибьютор + агенты) — **необходимая и полезная сложность**, а не оверинжиниринг.

Почему:
- ROADMAP уже становится длинным списком.
- Одна задача «Select CAD software…» реально распадается на 10–15 атомарных шагов.
- Агенту удобнее получать конкретный чек-лист, чем каждый раз заново дробить ROADMAP.
- При этом ADR остаются чистыми.

Правило простое:

> **ROADMAP** = что должно быть сделано на уровне фазы  
> **tasks/** = как именно сейчас ломаем это на шаги  
> **decisions/** = какие архитектурные выборы мы уже зафиксировали  
> **current-state + handoff** = что актуально прямо сейчас

Когда задача закрыта — чек-лист можно оставить (для истории) или переместить в `docs/tasks/done/`, а в ROADMAP поставить `[x]`.

### Практическое предложение

1. Создать `docs/tasks/`.
2. Перенести туда чек-лист, который мы составляли для CAD (`0001-select-cad-software.md`).
3. В ROADMAP оставить только высокоуровневый пункт + ссылку на task-файл.
4. В ADR-0001 оставить только решение и consequences, без живого чек-листа выполнения.

Это сохраняет чистоту нормативных документов и даёт агентам/тебе удобный операционный слой.

Если хочешь, могу сразу набросать шаблон файла задачи и содержимое `0001-select-cad-software.md` в этом стиле.

---
**Bunch**

Нужно ли упоминать в политиках AGENTS.md или long-term-memory.md о новой категории `tasks\` или достаточно напротив конкретно пункта ROADMAP.md указать ссылку на конкретный список задач, например так: `- [/] Select CAD software (and other required tools) that LLM can interact with independently with minimal human assistance (ADR-0001 adopted, benchmark pending) ([tasks](docs/tasks/0001-select-cad-software.md))`?

---
**Grok 4.5 Flash**

**Достаточно ссылки из ROADMAP + минимального упоминания в политиках.**

Полностью описывать `tasks/` как новую «критическую» сущность в каждом документе не нужно — это создаст лишнюю жёсткость. Но полностью молчать тоже плохо: агент, который читает только `AGENTS.md`, не узнает, куда смотреть за атомарными шагами.

### Рекомендуемый баланс

| Документ | Что сделать | Насколько подробно |
|----------|-------------|---------------------|
| **ROADMAP.md** | Обязательно ставить ссылку на конкретный task-файл | Да, как ты предложил |
| **AGENTS.md** | Коротко добавить `docs/tasks/` в Layout | 1 строка |
| **long-term-memory.md** | Упомянуть tasks как операционный слой между ROADMAP и работой | 2–3 предложения |
| **current-state.md / handoff** | Ссылаться на активные tasks при необходимости | По ситуации |

### Конкретно по ROADMAP

Твой вариант хороший и даже предпочтительный:

```markdown
- [/] Select CAD software (and other required tools) that LLM can interact with independently with minimal human assistance (ADR-0001 adopted, benchmark pending) → [tasks/0001-select-cad-software.md](tasks/0001-select-cad-software.md)
```

Или чуть аккуратнее:

```markdown
- [/] Select CAD software … (ADR-0001 adopted, benchmark pending)  
  Detailed checklist: [`docs/tasks/0001-select-cad-software.md`](tasks/0001-select-cad-software.md)
```

Так ROADMAP остаётся высокоуровневым, а детали живут в tasks.

### Что добавить в AGENTS.md (Layout)

Достаточно одной строки:

```markdown
- `docs/tasks/` — atomic checklists / work packages that break down ROADMAP items
```

И (по желанию) в Workflow добавить правило:

```markdown
When working on a ROADMAP item that has a linked task file — read and update that checklist.
```

### Что добавить в long-term-memory.md

В раздел про иерархию документов (Level 3) можно вставить коротко:

```markdown
- `docs/tasks/` — operational checklists that decompose ROADMAP items into atomic steps.  
  These are living working documents (more fluid than ADRs).  
  ROADMAP points to them; ADRs remain pure decision records.
```

Этого хватит, чтобы агент понимал разделение ролей:
- ROADMAP = фазы и крупные цели  
- tasks = текущие атомарные шаги  
- decisions = зафиксированные решения  
- current-state / handoff = что актуально прямо сейчас

### Итог

- **Ссылка из ROADMAP** — обязательна и является основным механизмом навигации.  
- **Упоминание в AGENTS.md и long-term-memory.md** — желательно, но минимальное (1–3 строки).  
- Не нужно создавать отдельную большую политику про tasks.

Так ты получаешь ясность без бюрократии.

---
**Bunch**

Я провёл экспресс обзор предложенных тобой CAD инструментов:
CadQuery
build123
FreeCAD
llmcad
Replicad
OpenSCA

Вот к чему я пришёл изучив информацию на их официальных ресурсах:

1. CadQuery и build123 имеют очень серьёзный уровень проработки. При этом по моим субъективным ощцщениям у CadQuery более простой (человечный) синтаксис, а build123 имеет больше возможностей в сложных построениях и сборках. Эти выводы я сделал исключительно по их документации. Требуется практическое сравнение достинств и недостатков. Пока это мои фаорит для нашего проекта и я не знаю какой из них выбрать.

2. FreeCAD отличный интрумент, но он изначально ориентирован под человека, а не LLM. Тем не менее интеграция с LLM есть. Думаю, этот CAD нам точно пригодится, как минимум в FEM анализе.

3. llmcad на данный момент не имеет открытого резпозитария на github — ошибка 404. Сложилось такое ощущение, что разработчики закрыли репо, и переквалифицировали свои наработки в плантныи продукт buildcad.ai. Пэтому для наших задач данный инструмент не подходит.

4. Replicad — интересный экземпляр. Понравилось, что сразу есть интерактивное 3D‐preview прямов на страницах документации. Это privew очень напомнило 3D‐view из blender. Вероятно ребята дёрнули код визуальной части от туда. Тем не менее этот проект мне показался слабее, чем CadQuery и build123.

5. OpenSCA не развивается уже около 5 лет. И изначально не совсем вписывается под наши критерии. Поэтому не будем тратить на него время.

Достаточно ли такого анализа для закрытия задач из нашего плана?
```md
## B. Исследование кандидатов
- [ ] B1. CadQuery — зрелость, API, LLM-опыт, assemblies, экспорт, headless
- [ ] B2. build123d — сравнение с CadQuery, стиль API, документация, экосистема
- [ ] B3. FreeCAD (Python API + headless + MCP) — возможности, ограничения, FEM
- [ ] B4. llmcad — насколько минималистичный API реально помогает LLM
- [ ] B5. Replicad — браузерный/TS-вариант, ограничения WASM
- [ ] B6. OpenSCAD — только как baseline/fallback для простых деталей
- [ ] B7. Сводная сравнительная таблица (критерии × кандидаты)
```

Интересно твоё мнение, согласен ли ты с моими оценками? Можешь дполнить и усилить мой анализ, чтобы закрыть поставленные задачи?

---
**Grok 4.5 Fast**

**Короткий ответ:** твоего обзора **почти достаточно**, чтобы закрыть блок **B (Исследование кандидатов)** на уровне «документального скрининга». Для полного закрытия не хватает только небольшой формализации (сводная таблица + явное решение по статусам) и, по желанию, одного практического микро-бенчмарка между CadQuery и build123d.

Ниже — усиленный и структурированный анализ, который можно почти дословно положить в task-файл.

---

### Усиленный анализ кандидатов

#### 1. CadQuery и build123d — явные фавориты

Ты прав: это два самых зрелых и подходящих варианта.

| Критерий | CadQuery | build123d |
|----------|----------|-----------|
| Ядро | OpenCASCADE (OCP) | OpenCASCADE (OCP) — тот же биндинг |
| Стиль API | Fluent (method chaining) | Более «питоничный» (context managers, явные объекты) |
| Субъективная «человечность» | Часто ощущается проще для простых деталей | Чуть круче кривая входа, но лучше для сложной логики |
| Сборки / сложные построения | Хорошие | Обычно считаются сильнее |
| Зрелость / сообщество | Более зрелый, больше примеров и LLM-опыта в дикой природе | Активно растёт, много свежей энергии |
| Headless | Отличный | Отличный |
| STEP / STL | Отличный | Отличный |
| LLM-дружелюбность | Хорошая (много обучающих данных) | Хорошая, иногда даже лучше за счёт явного стиля |

**Вывод:** оба полностью соответствуют ADR-0001.  
Выбор между ними — **не стратегический**, а тактический. Его можно отложить до короткого практического сравнения (один-два joint/link модуля). Пока можно держать оба как primary candidates.

#### 2. FreeCAD

Согласен полностью.

- Изначально GUI-ориентирован → хуже как основной инструмент для LLM-агента.
- Python API + `FreeCADCmd` дают нормальный headless-путь.
- Сильная сторона — **FEM workbench** и экосистема анализа.
- Есть MCP-обвязки.

**Статус для sint:**  
**Вспомогательный / специальный инструмент** (FEM, occasional human inspection, legacy-совместимость). Не primary Code-CAD.

#### 3. llmcad

Здесь важное уточнение.

- Сайт llmcad.org и документация **живы**.
- Пакет есть на PyPI (`pip install llmcad`).
- GitHub-репозиторий, на который ссылается сайт, действительно отдаёт 404 (или сильно ограничен).
- Проект явно связан с коммерческим BuildCAD AI.

**Практический вывод для open-source проекта sint:**  
Даже если библиотека технически устанавливается, отсутствие нормального открытого репозитория, issue-tracker и гарантированной долгосрочной открытости делает её **неприемлемой** как dependency.  
**Статус: исключён** (не primary, не fallback).

#### 4. Replicad

Согласен с оценкой.

- Плюсы: браузерный, красивый live-preview, TypeScript, OpenCASCADE WASM, STEP.
- Минусы: слабее экосистема и зрелость по сравнению с CadQuery/build123d; WASM-ограничения; меньше «тяжёлой» инженерной практики.

**Статус:** интересный secondary/experimental вариант (особенно если когда-нибудь понадобится веб-интерфейс). Не primary.

#### 5. OpenSCAD

Почти согласен, с небольшой поправкой.

- Последний **стабильный** релиз действительно старый (2021.01).
- Разработка **не умерла** полностью (есть nightlies, GSoC, активность в репозитории), но темп и приоритеты другие.
- Главное: это **mesh/CSG**, а не полноценный B-rep → хуже соответствует нашему требованию «STEP как источник истины».

**Статус:** можно держать в уме как очень лёгкий fallback для простейших деталей, но **не тратить время** в текущем плане. Практически исключён из основного трека.

---

### Сводная таблица (B7)

| Кандидат | OpenCASCADE / B-rep | Headless | LLM-friendliness | Зрелость | Сборки | Рекомендация для sint |
|----------|---------------------|----------|------------------|----------|--------|-----------------------|
| **CadQuery** | Да | Отлично | Высокая | Высокая | Хорошо | **Primary candidate** |
| **build123d** | Да | Отлично | Высокая | Высокая / растущая | Очень хорошо | **Primary candidate** |
| **FreeCAD** | Да | Хорошо (Cmd) | Средняя | Очень высокая | Хорошо | Secondary (FEM + human) |
| **llmcad** | Да | Да | Очень высокая (заявлено) | Низкая открытость | ? | **Исключён** |
| **Replicad** | Да (WASM) | Ограниченно | Средняя+ | Средняя | Средне | Experimental / web |
| **OpenSCAD** | Нет (CGAL/mesh) | Отлично | Высокая (простой язык) | Стабильный, но медленный | Слабо | Исключён из основного трека |

---

### Достаточно ли этого, чтобы закрыть блок B?

**Да — для этапа «исследование по документации».**

Можно ставить:

- [x] B1–B6 (с пометками выше)
- [x] B7 (таблица выше)

**Что ещё желательно перед финальным выбором primary (это уже блок C):**

1. Один маленький практический бенчмарк:  
   одна и та же деталь (например, parametric joint housing) на CadQuery и build123d.  
   Критерии: сколько правок нужно LLM, читаемость кода, стабильность STEP, удобство именования граней.
2. После этого — либо выбрать одного победителя, либо официально зафиксировать «dual primary: CadQuery + build123d» на ближайшие месяцы.

---

### Итоговое мнение

Твои оценки в целом **точные и хорошо совпадают с реальностью**. Я бы только:

- чуть смягчил формулировку про «OpenSCAD не развивается» → «стабильный релиз старый, основной трек нам не подходит»;
- явно зафиксировал **исключение llmcad** из-за проблем с открытостью репозитория;
- поднял CadQuery и build123d в статус равных primary candidates до практического сравнения.

Этого анализа + таблицы достаточно, чтобы закрыть исследовательскую часть (блок B) и переходить к практическому сравнению / финальному выбору.

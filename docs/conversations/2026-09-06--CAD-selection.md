---
title: 
date_created: 2026-09-06
date_updated: 2026-09-12
participants: [Bunch, Grok, Gemini]
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

---
**Bunch**

1. Как развернуть CadQuery и build123 на Arch и начать пользоваться?
2. Как настроить интеграцию CadQuery и build123 с LLM?

---
**Gemini 3.6 Flash Extended**

**Оценка неопределенности:** ~0.20 (превышает порог 0.1 из-за множества вариантов интеграции с LLM и выбора рабочей среды для 3D-просмотра). Ниже представлен базовый и наиболее надежный порядок настройки.

**1. Развертывание CadQuery и build123d на Arch Linux**

На Arch Linux действует PEP 668 (запрет прямой установки через `pip` в системное окружение). Оптимальный стек для работы — виртуальное окружение Python и просмотр геометрии через расширение `ocp-vscode`.

**Шаг 1. Подготовка системных зависимостей**
Установите Python, git и VS Code (или VSCodium) из официальных репозиториев:

```bash
sudo pacman -S python python-pip vscode git
```

**Шаг 2. Создание виртуального окружения и установка пакетов**

```bash
python -m venv ~/.venv/cad
source ~/.venv/cad/bin/activate
pip install --upgrade pip
pip install cadquery build123d ocp-vscode
```

**Шаг 3. Настройка просмотрщика OCP Viewer**

1. Откройте VS Code и установите расширение **OCP CAD Viewer** (`OCP CAD Viewer for VS Code`).
2. Укажите интерпретатор Python: `Ctrl+Shift+P` $\rightarrow$ `Python: Select Interpreter` $\rightarrow$ выберите `~/.venv/cad/bin/python`.
3. Запустите просмотрщик: `Ctrl+Shift+P` $\rightarrow$ `OCP: Start Viewer`.

**Тестовый запуск (build123d):**
Создайте файл `test_model.py`:

```python
from build123d import *
from ocp_vscode import show

with BuildPart() as model:
    Box(20, 20, 10)
    cyl = Cylinder(radius=5, height=10, mode=Mode.SUBTRACT)

show(model)
```

Запустите файл из терминала с активным `venv` (`python test_model.py`). Модель отобразится в окне OCP Viewer внутри VS Code.

---

**2. Варианты интеграции с LLM**

Так как синтаксис CadQuery и build123d со временем обновлялся (в build123d активнее используется контекстный менеджер `with BuildPart():`), стандартные LLM склонны галлюцинировать устаревшим кодом.

* **Вариант А: Интеграция в IDE (Cursor / VS Code + Continue / Claude Dev)**
* **Контекст документации:** Скачайте репозиторий документации [build123d](https://github.com/gumyr/build123d) или [CadQuery](https://github.com/CadQuery/cadquery) в формате `.md` и прикрепите к рабочей области IDE.
* **Системный промпт:** В файле настроек ассистента (`.cursorrules` или системном промпте Continue) укажите точную версионность и правила построения (например, запрет использования устаревшего синтаксиса `cq.Workplane`).

* **Вариант Б: Автономный агент с циклом обратной связи (Feedback Loop)**
* LLM генерирует Python-скрипт.
* Локальный скрипт исполняет код (`exec()` или subprocess).
* При ошибке выполнения (Traceback) логи ошибок автоматически отправляются обратно в нейросеть для исправления кода до тех пор, пока геометрия не будет успешно собрана.

* **Вариант В: MCP (Model Context Protocol)**
* Подключение LLM к локальному MCP-серверу, предоставляющему инструмент `run_cad_code`, который возвращает статус генерации и рендерит STL/PNG-превью для visual-LLM.

---

**Уточняющие вопросы (для снижения неопределенности до < 0.1):**

Какая модель интеграции с LLM вам предпочтительна: интерактивный помощник прямо в редакторе кода (Cursor / VS Code) или автономный Python-агент, генерирующий 3D-файлы по текстовому описанию? Уточнение позволит предоставить готовые конфигурационные файлы и системные промпты.

---
**Bunch**

Хорошо. Давай сначала разберёмся с установкой и тестовым ручным запуском. А уже после успеха перейдём к ингреации с LLM.

1. Обязательно ли устанавливать пакеты CadQuery и build123 в вируальное окружение? Могу я воспользоваться pipx или `sudo pacman -S` для установки в «корень» системы для испльзования в любой директории ОС?
2. Варианты предварительного просмотра существуют только для VSCode? Возможно, есть нативная среда проектирования непосредственно от разработчиков CadQuery и build123? Мне предпочтительнее редактор Zed, но полагаю, что там нет предпросмотра OCP.

---
**Gemini 3.6 Flash Extended**

**Оценка неопределенности:** < 0.1 (поведение PEP 668 в Arch Linux, ограничения pipx и экосистема CadQuery/build123d строго определены).

**1. Установка: виртуальное окружение vs глобальная система**

* **`sudo pacman -S` не сработает:** CadQuery и build123d отсутствуют в официальных репозиториях Arch Linux (а пакеты из AUR для Python часто устаревают).
* **`pipx` не подходит:** `pipx` предназначен исключительно для CLI-приложений с исполняемыми файлами (например, `black` или `youtube-dl`). Он изолирует пакет в отдельном изолированном окружении и не позволяет делать `import cadquery` или `import build123d` в твоих собственных скриптах.
* **`pip install --user` заблокирован:** В Arch Linux действует PEP 668 (`EXTERNALLY-MANAGED`), запрещающий установку Python-пакетов в корень или системный профиль пользователя, чтобы не сломать системные зависимости `pacman`.

**Как использовать библиотеки из любой директории без ручной активации venv:**

1. **Менеджер `uv` (самый удобный способ):**
Установите `uv` через pacman: `sudo pacman -S uv`.
Далее вы можете запускать любой скрипт из любой папки одной командой без предварительного создания или активации venv — `uv` сам создаст кэш и запустит код:
```bash
uv run --with build123d --with ocp-vscode python my_script.py
```

2. **Глобальный пользовательский venv:**
Создайте одно общее окружение `python -m venv ~/.venv/cad`, установите туда библиотеки и добавьте автозагрузку в shell-конфиг (`~/.bashrc` или `~/.zshrc`):
```bash
source ~/.venv/cad/bin/activate
```

После этого во всех терминалах ОС по умолчанию будет активен этот venv со всеми установленными CAD-библиотеками.

---

**2. Предпросмотр: CQ-Editor, автономное окно и Zed**

Предпросмотр **не привязан жестко к VS Code**. Существует нативное приложение от разработчиков CadQuery и решения для сторонних редакторов.

| Инструмент | Как работает | Подходит ли для Zed |
| --- | --- | --- |
| **CQ-Editor** | Официальное GUI-приложение на PyQt от авторов CadQuery. Содержит встроенный редактор кода и 3D-окно на движке OpenCASCADE. Поддерживает и CadQuery, и build123d. | Используется как самостоятельная IDE вместо Zed. |
| **OCP Viewer (Standalone Window)** | Пакет `ocp-vscode` умеет запускать просмотрщик как отдельное приложение/окно вне VS Code. При вызове `show_object()` или `show()` открывается независимое окно с 3D-сценой. | **Идеальное решение для Zed.** |
| **Экспорт в STEP / STL** | Сохранение геометрии на диск с последующим просмотром через внешние утилиты (FreeCAD, FDM-слайсеры вроде Bambu Studio / PrusaSlicer). | Работает везде, но нет моментального авто-обновления scenes. |

**Как настроить удобную работу в Zed:**

1. Установите `build123d` и `ocp-vscode` в ваше окружение.
2. Пишите код модели в **Zed**.
3. Добавьте в конец скрипта вызов standalone-просмотрщика:
```python
from build123d import *
from ocp_vscode import show

with BuildPart() as model:
    Box(10, 20, 30)

# Запускает автономный сервер просмотрщика и открывает окно
show(model)
```

4. Запускайте файл прямо из встроенного терминала Zed (`python test.py` или `uv run --with build123d --with ocp-vscode test.py`). При первом запуске откроется отдельное окно с 3D-моделью, которое будет автоматически обновлять геометрию при повторных запусках скрипта.

---
**Bunch**

Возможно мы сможем сделать выбор между CadQuery и build123 без траты времени на установку, интеграцию с LLM каждого из них и анализ результатов. Для этого я хочу, чтобы ты проверил тезисы об этих CAD, которые мне сообщила LLM Gemini:

1. build123d — это следующее поколение CadQuery от тех же разработчиков. Термин «следующее поколение» здесь используется не в маркетинговом смысле, а в сугубо техническом и хронологическом.
2. Ключевой автор и мейнтейнер build123d — разработчик под ником @gumyr (Paul Albanese). До того как создать build123d, он долгое время являлся одним из главных контрибьюторов и мейнтейнеров самого проекта CadQuery (вы можете легко проверить его коммиты в репозитории CadQuery).
3. build123d создавался как прямая эволюция и исправление архитектурных ошибок CadQuery:
  - Отказ от Fluent API: Главная фишка CadQuery — «текучий интерфейс» (когда команды пишутся через точку: `cq.Workplane().box().edges().fillet())`. Со временем разработчики поняли, что такая цепочка скрывает внутреннее состояние программы, усложняет автодополнение кода в IDE (типа VS Code) и делает невозможным использование стандартных циклов `for` внутри цепочки. Если вы захотите внутри цепочки поставить условие `if` или перебрать грани в цикле `for` — цепочка сломается. IDE часто путается и не может подсказать, какие методы доступны после очередной точки.
  - Переход на Context Managers: В build123d авторы полностью переписали этот подход, внедрив нативные контекстные менеджеры Python (блоки `with BuildPart():`). Это позволило писать код в стандартном PEP8-стиле Python, где объекты можно нормально присваивать переменным, дебажить в любой строчке и использовать встроенные инструменты языка. В build123d вы работаете как в обычном Python. Каждый объект, грань или ребро — это осязаемая переменная. Вы можете использовать циклы, функции, легко дебажить код построчно, а автодополнение в IDE работает безупречно.
  - Общий фундамент: Обе библиотеки используют один и тот же сложнейший технологический стек: ядро OpenCASCADE и бинарную обертку OCP (OpenCascade Python). Объекты между CadQuery и build123d можно буквально налету конвертировать друг в друга внутри одного скрипта через свойство `.wrapped`.
4. build123d — это проект, созданный ключевым разработчиком CadQuery с целью переосмыслить API, сделав его более «питоничным». CadQuery по-прежнему поддерживается, но для новых проектов само комьюнити и авторы сейчас рекомендуют выбирать именно build123d как более современный стандарт Code-CAD.
5. Как ни странно, для совсем простых деталей цепочечный синтаксис CadQuery (`.box().hole()`) короче и интуитивнее для новичков. Он напоминает jQuery в веб-разработке.
6. CadQuery — это стабильная классика на жизнеобеспечении, а build123d — это площадка для инноваций, куда ушли самые активные разработчики.

---
**Grok 4.5 Fast**

Проверил тезисы Gemini по источникам. Вот точный разбор.

### 1. «build123d — следующее поколение CadQuery от тех же разработчиков»

**Частично верно, с важными уточнениями.**

- build123d **действительно** позиционируется (в том числе официально) как эволюция / переосмысление подхода CadQuery: отказ от Fluent API в пользу context managers и более «питоничного» стиля.
- В README build123d прямо написано: *«build123d is derived from portions of CadQuery, but is extensively refactored…»*.
- На сайте Open Cascade Technology build123d описан почти теми же словами: *«could be considered as an evolution of CadQuery where the somewhat restrictive Fluent API is replaced with stateful context managers»*.

Но формулировка «от тех же разработчиков» (во множественном числе, как будто вся команда CadQuery) — **преувеличение**. Это в первую очередь работа одного ключевого человека + его окружения, а не официальный «CadQuery 3.0» от core-команды CadQuery.

### 2. Ключевой автор — @gumyr (и имя)

**В основном верно, имя — нет.**

- Автор и основной мейнтейнер build123d — **@gumyr**.
- Настоящее имя — **Roger Maitland**, а не Paul Albanese (Gemini ошибся с именем).
- До build123d он был заметным контрибьютором экосистемы CadQuery (в частности, сделал популярную библиотеку `cq_warehouse` и другие вещи). Он **не** был одним из главных core-maintainers CadQuery (core — в основном Adam Urbanczyk, Jeremy Wright / jmwright и др.).

То есть: важный и опытный участник экосистемы → создал независимое следующее поколение API. Не «бывший главный мейнтейнер CadQuery».

### 3. Архитектурные причины создания build123d

**В целом верно и хорошо сформулировано.**

- Fluent API CadQuery действительно удобен для коротких цепочек, но плохо сочетается с обычным Python (циклы, условия, нормальные переменные, отладка, автодополнение IDE).
- build123d сознательно ушёл от этого к context managers (`with BuildPart():` и т.п.) и более явной объектной модели.
- Обе библиотеки сидят на одном фундаменте: **OpenCASCADE + OCP**. Объекты можно конвертировать через `.wrapped` — это официально документировано.

Здесь Gemini прав.

### 4. «Сообщество и авторы сейчас рекомендуют build123d для новых проектов»

**Частично верно, но не как официальный вердикт CadQuery.**

- В части сообщества (особенно среди тех, кто пишет более сложный код и ценит IDE/отладку) build123d действительно часто рекомендуют как более современный выбор для **новых** проектов.
- Инструменты вроде agentcad по умолчанию ставят build123d и держат CadQuery как compatibility-режим.
- Сама команда CadQuery **не объявляла** build123d официальным преемником и не сказала «переставайте использовать CadQuery». CadQuery продолжает жить своей жизнью.

То есть тренд есть, но это не единый официальный консенсус «авторов CadQuery».

### 5. Для простых деталей синтаксис CadQuery короче и интуитивнее

**Верно.**

Цепочки вида `.box().faces(">Z").hole()` многим кажутся проще и короче на старте (аналогия с jQuery уместна). build123d за эту «питоничность» платит чуть большей многословностью на простых примерах.

### 6. «CadQuery — на жизнеобеспечении, build123d — площадка инноваций»

**Сильно преувеличено / неверно.**

- CadQuery **не** на жизнеобеспечении. Релизы продолжаются (в 2026 выходил 2.8.0), есть активные мейнтейнеры (Adam Urbanczyk, Jeremy Wright и др.), Open Collective, регулярные обновления.
- build123d действительно более динамичен в плане API-экспериментов и воспринимается как «новое поколение», но CadQuery остаётся живым и стабильным проектом с большой установленной базой.

Формулировка Gemini здесь слишком драматичная.

---

### Итоговая оценка тезисов

| Тезис | Вердикт | Комментарий |
|-------|---------|-------------|
| 1. Следующее поколение от тех же разработчиков | Частично | Эволюция подхода — да; «те же разработчики» — преувеличение |
| 2. @gumyr = ключевой автор, бывший главный мейнтейнер CQ | Частично | Автор — да; имя неверное; «главный мейнтейнер CQ» — нет |
| 3. Отказ от Fluent → Context Managers + общий OCP | Верно | Хорошо описано |
| 4. Сообщество рекомендует build123d для новых проектов | Частично | Тренд есть, но не официальный вердикт CadQuery |
| 5. Для простых деталей CQ короче | Верно | |
| 6. CQ на жизнеобеспечении | Неверно | CadQuery активно поддерживается |

---

### Практический вывод для sint

Тезисы Gemini в целом **полезны**, но содержат несколько важных преувеличений. После коррекции картина такая:

- build123d — осознанная эволюция API от сильного участника экосистемы CadQuery, с лучшей интеграцией в обычный Python.
- CadQuery — зрелая, всё ещё активно поддерживаемая классика.
- Для **нового** проекта вроде sint, где важны сложные параметрические модели, сборки, отладка агентом и IDE, **build123d выглядит предпочтительнее** как primary.
- CadQuery остаётся отличным и полностью жизнеспособным запасным/совместимым вариантом (общий OCP + `.wrapped`).

Это уже достаточно весомый аргумент, чтобы **склониться к build123d без полноценного практического бенчмарка**, особенно если ты готов принять чуть более многословный стиль на простых деталях в обмен на лучшую работу с циклами, условиями и отладкой.

Если хочешь максимальную осторожность — можно всё же сделать один очень маленький side-by-side тест (одна деталь), но для принятия решения уровня ADR текущего анализа уже хватает.

---
**Bunch**

Хорошо! Напиши последовательность шагов, как мне установить build123d и ocp_vscode в глобальный пользовательский venv, с предварительной настройкой глобального venv. Утилита uv у меня уже установлена.

---
**Gemini 3.6 Fast Extended**

Для настройки постоянного доступа к **build123d** и автономному просмотрщику **ocp-vscode** из любой директории выполните следующую последовательность команд.

1. **Создание виртуального окружения:** Окружение будет размещено в ~/.venv/cad.
Выполните команду для создания изолированного каталога окружения:

```bash
uv venv ~/.venv/cad
```

2. **Настройка автоактивации venv:** Выберите конфигурационный файл вашей оболочки (Zsh или Bash).
Добавьте строчку автозагрузки в конфиг оболочки.

Для **Zsh**:

```bash
echo 'source ~/.venv/cad/bin/activate' >> ~/.zshrc
source ~/.zshrc
```

Для **Bash**:

```bash
echo 'source ~/.venv/cad/bin/activate' >> ~/.bashrc
source ~/.bashrc
```

*После этого при открытии любого нового терминала venv с именем `(cad)` будет активироваться автоматически.*

3. **Установка build123d и ocp-vscode:** Выполняется через быстрый менеджер uv pip.
Установите пакеты в созданный venv:

```bash
uv pip install build123d ocp-vscode
```

4. **Проверка работы standalone-просмотрщика:** Запуск можно выполнять из любого каталога ОС.
Перейдите в любую удобную папку и создайте файл `test_cad.py`:

```python
from build123d import *
from ocp_vscode import show

with BuildPart() as model:
    Box(30, 30, 10)
    Cylinder(radius=8, height=10, mode=Mode.SUBTRACT)

show(model)
```

Запустите скрипт базовым системным вызовом:

```bash
python test_cad.py
```

При выполнении скрипта `ocp-vscode` автоматически инициализирует локальный сервер и запустит отдельное окно с 3D-моделью детали.


---
**Bunch**

1. Да, переходим к настройке интеграции, если она требуется. Ознакомься с проектом для понимания контекста задачи: https://github.com/PaulBunch/sint
2. В рамках проекта я не уверен, что в каждом python CAD скрипете нужно импортировать `from ocp_vscode import show`. Думаю, логичнее было бы сделать alias на уровне ОС, типа `cad-py show trash/test_cad.py`, который будет интегрировать на лету нужный импорт в скрипт, а в конце вызывать `show`, не внося измененияв сам файл python CAD скрипта.

---
**Geimi 3.6 Flash Extended**

Разделение чистой геометрии и кода просмотра — верное архитектурное решение. Это делает CAD-файлы проекта **sint** автономными модулями, которые можно беспроблемно импортировать в сборки, экпортировать в STEP/STL или рендерить любым просмотрщиком.

---

### 1. Реализация обёртки просмотрщика (`cad-show`)

Создайте универсальный Python-раннер, который выполняет CAD-скрипт и автоматически вылавливает все созданные 3D-объекты через `ocp_vscode.show_all()`.

**Шаг 1. Создание скрипта-раннера**
Создайте файл `~/.local/bin/cad-show`:

```python
#!/home/user/.venv/cad/bin/python
import sys
import runpy
import inspect
import ocp_vscode

if len(sys.argv) < 2:
    print("Использование: cad-show <path/to/script.py>")
    sys.exit(1)

target_script = sys.argv[1]
global_vars = runpy.run_path(target_script, run_name="__main__")

cad_objects = []
for name, val in global_vars.items():
    # Игнорируем приватные переменные, функции, модули и КЛАССЫ (Box, Cylinder и т.д.)
    if name.startswith("_") or inspect.isclass(val) or inspect.isroutine(val):
        continue

    # Проверяем, что перед нами экземпляр контекстного менеджера или 3D-геометрии
    if hasattr(val, "part") or hasattr(val, "sketch") or hasattr(val, "wrapped"):
        cad_objects.append(val)

if cad_objects:
    ocp_vscode.show(*cad_objects)
else:
    print("Предупреждение: в скрипте не найдено 3D-объектов для отображения.")
```

**Шаг 2. Права и настройка алиаса**

```bash
chmod +x ~/.local/bin/cad-show
```

Если `~/.local/bin` у вас в `PATH`, вы можете запускать просмотр из любой папки:

```bash
cad-show trash/test_cad.py
```

При таком подходе чистый файл модели `trash/test_cad.py` выглядит лаконично и без зависимости от `ocp-vscode`:

```python
from build123d import *

with BuildPart() as model:
    Box(30, 30, 10)
    Cylinder(radius=8, height=10, mode=Mode.SUBTRACT)
```

---

### 2. Интеграция build123d с LLM (для Zed и систем разработки)

Ключевая проблема при генерации кода для `build123d` нейросетями — галлюцинации устаревшим синтаксисом CadQuery (`cq.Workplane`) или использование устаревших методов `build123d`.

Для проекта **sint** рекомендуется использовать трёхкомпонентную структуру контекста:

#### 1. Системный промпт (Правила генерации)

Добавьте в правила LLM (в Zed / Assistant / Cursor) следующий системный контекст:

```markdown
You are an expert in 3D CAD modeling using Python and build123d.
Follow these mandatory rules:
1. ALWAYS use build123d standard context managers (`with BuildPart():`, `with BuildSketch():`, `with BuildLine():`).
2. NEVER use legacy CadQuery `cq.Workplane` syntax.
3. Keep CAD scripts pure: DO NOT import `ocp_vscode` or call `show()`/`show_all()`.
4. Output parametric design using named arguments for key dimensions at the top of the file.
5. Use modern selectors: `faces().sort_by(Axis.Z)[-1]`, `edges().filter_by(GeomType.CIRCLE)`.
6. Ensure correct boolean operations with explicit modes (`Mode.ADD`, `Mode.SUBTRACT`, `Mode.INTERSECT`).
```

#### 2. Базовый справочный контекст (Cheatsheet)

Поскольку библиотека `build123d` активно развивается, сохраните в репозитории проекта файл `.zed/build123d_ref.md` или `docs/build123d_ref.md` с эталонными шаблонами:

```python
# Базовый деталь (BuildPart)
with BuildPart() as part:
    Box(width, length, height)
    with BuildSketch(part.faces().sort_by(Axis.Z)[-1]) as sketch:
        Circle(radius=5)
    extrude(amount=-height, mode=Mode.SUBTRACT)

# Сборка (Compound / Assemblies)
gear_1 = Gear(...)
gear_2 = Gear(...)
assembly = Compound(children=[gear_1, gear_2.locate(Pos(x=50))])
```

#### 3. Патерн авто-исправления (Feedback Loop)

В Zed при работе через Assistant встроенный терминал с `cad-show` мгновенно подсвечивает ошибки компиляции CAD-ядра (например, ошибки топологии `OpenCASCADE` или `ValueError` при скруглениях `fillet`).

При возникновении ошибки достаточно передавать Traceback обратно в LLM с промптом:

> `"Фигура упала с ошибкой OpenCASCADE: [Traceback]. Исправь селектор граней или радиус скругления."`

---
**Bunch**

Для перехода от теории к практике. Я установил build123d и ocp-vscode в глобальное окружение `~/.venv/cad/` и настроил скрипты на уровне ОС для запуска python-CAD-скриптов. В этом мне помогала нейросеть Gemini. Тем не менее, у меня есть предчуствие, что возможно данные скрипты нужно разместить не на уровне ОС, а на уровен проекта, чтобы другие разработчики и LLM могли ими пользоваться. Как настроить окружение проекта и скрипты оптимально? При этом я терпеть не могу poetry и подобные системы, потому что с ними больше геморроя, чем пользы.
В ручном режиме сейчас всё работает. Мне нужно настроить корректную интеграцию build123d с LLM. Вот что рекомендует Gemini, но он не учитывает контекст проекта, в который ты погружён. Интересно узнать твоё мнение.
*Сюда прекреплён предыдущй ответ Gemini*

---
**Grok 4.5 Fast**

**Короткий ответ:**  
Да, скрипты и окружение лучше держать **на уровне проекта**, а не только в глобальном `~/.venv/cad/` и `~/.local/bin`. Глобальная установка удобна тебе лично, но для других людей и LLM-агентов она непрозрачна. При этом Poetry (и подобные менеджеры) использовать не обязательно — достаточно обычного `venv` + `requirements.txt` / `pyproject.toml` без poetry.

Ниже — оптимальная схема именно под sint и ADR-0001.

---

### 1. Рекомендуемая структура окружения проекта

```
sint/
├── .venv/                    # локальный venv проекта (в .gitignore)
├── requirements-cad.txt      # или requirements.txt
├── scripts/                  # утилиты проекта
│   ├── cad-show.py
│   └── cad-export.py         # (опционально: headless STEP/STL)
├── hardware/                 # или cad/
│   └── ...                   # чистые build123d-скрипты моделей
├── docs/
│   ├── decisions/
│   ├── tasks/
│   └── build123d-guidelines.md   # правила + cheatsheet для LLM
└── ...
```

**Почему так:**
- `.venv` внутри проекта → любой человек/агент делает `python -m venv .venv && source .venv/bin/activate && pip install -r requirements-cad.txt`.
- Скрипты в `scripts/` версионируются и доступны всем.
- Модели остаются «чистыми» (без `ocp_vscode`).

Глобальный `~/.venv/cad/` можешь оставить для личных экспериментов, но **канонический** путь для проекта — локальный.

---

### 2. Минимальный `requirements-cad.txt` (без Poetry)

```text
build123d>=0.11
ocp-vscode
# при необходимости позже:
# cadquery          # только если понадобится совместимость
```

Установка:
```bash
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
pip install -U pip
pip install -r requirements-cad.txt
```

Этого достаточно. Никакого poetry/lock-файла на старте не нужно.

---

### 3. Скрипт `scripts/cad-show.py` (улучшенная версия)

Идея Gemini правильная, но лучше сделать её проектной и чуть надёжнее:

```python
#!/usr/bin/env python3
"""Run a pure build123d script and show resulting geometry in ocp-vscode."""
import sys
import runpy
import inspect
from pathlib import Path

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/cad-show.py <path/to/model.py>")
        sys.exit(1)

    target = Path(sys.argv[1]).resolve()
    if not target.exists():
        print(f"File not found: {target}")
        sys.exit(1)

    # Выполняем скрипт
    global_vars = runpy.run_path(str(target), run_name="__main__")

    # Собираем кандидатов на показ
    cad_objects = []
    for name, val in global_vars.items():
        if name.startswith("_"):
            continue
        if inspect.isclass(val) or inspect.isroutine(val) or inspect.ismodule(val):
            continue
        # build123d / OCP объекты
        if hasattr(val, "wrapped") or hasattr(val, "part") or hasattr(val, "sketch"):
            cad_objects.append(val)

    if not cad_objects:
        print("Warning: no CAD objects found to display.")
        sys.exit(0)

    try:
        import ocp_vscode
        ocp_vscode.show(*cad_objects)
    except ImportError:
        print("ocp_vscode is not installed. Install it or use a different viewer.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

Запуск из корня проекта:
```bash
source .venv/bin/activate
python scripts/cad-show.py hardware/joint_module.py
```

Можно добавить удобный алиас в `README` или в `scripts/`:
```bash
# scripts/cad-show (shell wrapper)
#!/usr/bin/env bash
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec "$ROOT/.venv/bin/python" "$ROOT/scripts/cad-show.py" "$@"
```

---

### 4. Чистые модели (как и рекомендовал Gemini)

```python
# hardware/example_plate.py
from build123d import *

# Параметры сверху — удобно и человеку, и LLM
WIDTH = 80
LENGTH = 50
THICKNESS = 8
HOLE_DIA = 6

with BuildPart() as plate:
    Box(WIDTH, LENGTH, THICKNESS)
    with Locations(plate.faces().sort_by(Axis.Z)[-1]):
        with GridLocations(WIDTH - 20, LENGTH - 20, 2, 2):
            Hole(radius=HOLE_DIA / 2, depth=THICKNESS)

# Можно явно экспортировать результат, если нужно
result = plate.part
```

Никакого `ocp_vscode` внутри модели.

---

### 5. Интеграция с LLM (важнее, чем скрипт просмотрщика)

Рекомендации Gemini в целом здравые, но их нужно привязать к sint.

**Что сделать обязательно:**

1. **Файл правил для агентов**  
   Создай `docs/build123d-guidelines.md` (или `.zed/rules` / аналог в твоём редакторе) со строгими правилами:

```markdown
# build123d rules for sint

- Use ONLY build123d (never CadQuery `cq.Workplane`).
- Prefer context managers: `with BuildPart()`, `with BuildSketch()`, `with BuildLine()`.
- Keep model scripts pure: no `ocp_vscode`, no `show()`, no side-effect imports.
- Put all key dimensions as named constants at the top of the file.
- Prefer explicit `Mode.ADD` / `Mode.SUBTRACT` / `Mode.INTERSECT`.
- Use modern selectors (`faces().sort_by(Axis.Z)[-1]`, `edges().filter_by(...)`).
- After generation the script must be runnable headlessly and exportable to STEP.
```

2. **Cheatsheet**  
   В том же файле или отдельно — 5–10 эталонных паттернов (пластина с отверстиями, fillet, простой joint, Compound-сборка).

3. **Feedback loop**  
   Агент должен уметь:
   - запустить `python scripts/cad-show.py ...` или headless-экспорт;
   - получить traceback / скриншот / STEP;
   - исправить код.

Это уже покрывается ADR-0001 + task-файлом.

---

### 6. Headless-экспорт (очень желательно добавить сразу)

Для агентов важнее не только `show`, но и детерминированный экспорт:

```python
# scripts/cad-export.py (эскиз)
from build123d import export_step, export_stl
# ... выполнить скрипт, найти главный Solid/Part, сделать export_step(..., "out.step")
```

Тогда LLM-цикл становится полностью без GUI:
`generate → run → export STEP → inspect / measure → fix`.

---

### 7. Что я бы сделал на твоём месте прямо сейчас

1. Создать в корне `requirements-cad.txt` + локальный `.venv`.
2. Перенести `cad-show` в `scripts/cad-show.py`.
3. Добавить `docs/build123d-guidelines.md` с правилами + коротким cheatsheet.
4. Договориться, что все модели лежат в `hardware/` (или `cad/`) и не содержат viewer-кода.
5. Глобальный `~/.venv/cad/` оставить только для личных быстрых опытов.

Так ты получаешь:
- воспроизводимость для других людей и агентов;
- отсутствие Poetry;
- чистое разделение геометрии и просмотра;
- хорошую базу для LLM-цикла.

Если хочешь, могу сразу набросать готовые тексты `requirements-cad.txt`, `scripts/cad-show.py` и черновик `docs/build123d-guidelines.md` в стиле проекта sint.

---
**Bunch**

1. cad-show и requirements-cad.txt размещены в локальной области проекта — работает!

2. build123d-guidelines.md создан в нём размещены тезисные правила, которые ты предложил. cheatsheet отсутствуют. Если ты считаешь, что нужно обязательно там разместить cheatsheet, напиши их, а я добавлю. Кроме того build123d-guidelines.md пока нигде не упомянается. Возможно, было бы правильно его упоминуть в локальном агенте, который будет заниматься именно CAD‐проектированием. С описанием жизненого цикла разработки конкретной детали/сборки `generate → run → export STEP → inspect / measure → fix`.

3. python-CAD-скрипты и экспортируемые из них step-файлы будут находиться в одной директории `hardware/`?

4. Подготовь код для скрипта `cad-export.py`

---
**Grok 4.5 Fast**

### 1–2. Guidelines + cheatsheet + где упоминать

**Cheatsheet стоит добавить.**  
Короткие эталонные паттерны сильно снижают галлюцинации LLM. Ниже готовый блок — можешь просто вставить в `docs/build123d-guidelines.md`.

````markdown
## Quick Cheatsheet

### Basic parametric part
```python
from build123d import *

WIDTH, LENGTH, HEIGHT = 80, 50, 10
HOLE_R = 3.0

with BuildPart() as part:
    Box(WIDTH, LENGTH, HEIGHT)
    with Locations(part.faces().sort_by(Axis.Z)[-1]):
        with GridLocations(WIDTH - 20, LENGTH - 20, 2, 2):
            Hole(radius=HOLE_R, depth=HEIGHT)

result = part.part
```

### Sketch + extrude (subtract)
```python
with BuildPart() as part:
    Box(60, 40, 12)
    with BuildSketch(part.faces().sort_by(Axis.Z)[-1]):
        Circle(8)
    extrude(amount=-12, mode=Mode.SUBTRACT)
```

### Fillet / chamfer
```python
with BuildPart() as part:
    Box(30, 30, 15)
    fillet(part.edges().filter_by(Axis.Z), radius=2)
    # or: chamfer(part.edges(), length=1)
```

### Simple Compound (assembly-like)
```python
from build123d import *

a = Box(20, 20, 10)
b = Cylinder(radius=5, height=20).locate(Pos(x=30))
assembly = Compound(children=[a, b])
```

### Selectors (most used)
- Top face: `faces().sort_by(Axis.Z)[-1]`
- Bottom face: `faces().sort_by(Axis.Z)[0]`
- Vertical edges: `edges().filter_by(Axis.Z)`
- Circular edges: `edges().filter_by(GeomType.CIRCLE)`
````

**Где упоминать файл**

Да, его нужно явно подключить к CAD-агенту / правилам.

Рекомендуемые места:
- В системном промпте / rules локального CAD-агента (Zed, Cursor и т.п.).
- Коротко в `AGENTS.md` или в task-файле по CAD (ссылка + жизненный цикл).

Пример формулировки для агента:

```text
When working on hardware geometry:
1. Read docs/build123d-guidelines.md
2. Follow the pure-script rules (no ocp_vscode inside models)
3. Lifecycle for every part/assembly:
   generate → run (cad-show or cad-export) → export STEP → inspect/measure → fix
```

---

### 3. Где лежат скрипты и STEP?

**Да, лучше в одной директории `hardware/`** (или `cad/`), но с понятным разделением.

Рекомендуемый вариант:

```text
hardware/
├── joints/
│   ├── joint_module_v1.py      # исходник
│   ├── joint_module_v1.step    # экспорт (можно генерировать)
│   └── joint_module_v1.stl     # опционально
├── links/
└── assemblies/
```

Правила:
- **Источник истины** — `.py`.
- `.step` — канонический экспорт (B-rep).
- `.stl` / `.3mf` — производные для печати.
- Сгенерированные файлы можно либо коммитить (удобно для обзора), либо держать в `.gitignore` и собирать в CI. На старте проще коммитить STEP вместе со скриптом.

Главное — не разносить исходник и STEP по разным деревьям без необходимости.

---

### 4. Скрипт `scripts/cad-export.py`

```python
#!/usr/bin/env python3
"""
Headless runner for pure build123d scripts.
Executes the script and exports found geometry to STEP (and optionally STL).

Usage:
  python scripts/cad-export.py path/to/model.py
  python scripts/cad-export.py path/to/model.py --stl
  python scripts/cad-export.py path/to/model.py -o out/dir
"""

from __future__ import annotations

import argparse
import inspect
import runpy
import sys
from pathlib import Path
from typing import Any, List

def is_cad_object(obj: Any) -> bool:
    """Heuristic: build123d / OCP-like geometry objects."""
    if obj is None:
        return False
    if inspect.isclass(obj) or inspect.isroutine(obj) or inspect.ismodule(obj):
        return False
    return (
        hasattr(obj, "wrapped")
        or hasattr(obj, "part")
        or hasattr(obj, "sketch")
        or hasattr(obj, "solid")
    )


def unwrap(obj: Any) -> Any:
    """Prefer the actual solid/part when a builder context is returned."""
    if hasattr(obj, "part") and obj.part is not None:
        return obj.part
    if hasattr(obj, "solid") and callable(obj.solid):
        try:
            return obj.solid()
        except Exception:
            pass
    return obj


def collect_cad_objects(namespace: dict) -> List[Any]:
    objects = []
    for name, val in namespace.items():
        if name.startswith("_"):
            continue
        if is_cad_object(val):
            objects.append(unwrap(val))
    return objects


def export_objects(objects: List[Any], out_base: Path, do_stl: bool) -> None:
    from build123d import export_step, export_stl, Compound

    if not objects:
        print("No CAD objects found to export.")
        sys.exit(1)

    # One object → direct export; several → Compound
    if len(objects) == 1:
        shape = objects[0]
    else:
        shape = Compound(children=objects)

    step_path = out_base.with_suffix(".step")
    export_step(shape, step_path)
    print(f"STEP written: {step_path}")

    if do_stl:
        stl_path = out_base.with_suffix(".stl")
        export_stl(shape, stl_path)
        print(f"STL written:  {stl_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export build123d script to STEP/STL")
    parser.add_argument("script", type=Path, help="Path to pure build123d .py script")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for output files (default: same as script)",
    )
    parser.add_argument(
        "--stl",
        action="store_true",
        help="Also export STL",
    )
    args = parser.parse_args()

    script_path = args.script.resolve()
    if not script_path.exists():
        print(f"File not found: {script_path}")
        sys.exit(1)

    # Run the pure model script
    namespace = runpy.run_path(str(script_path), run_name="__main__")
    objects = collect_cad_objects(namespace)

    out_dir = args.output_dir.resolve() if args.output_dir else script_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_base = out_dir / script_path.stem

    export_objects(objects, out_base, do_stl=args.stl)


if __name__ == "__main__":
    main()
```

**Примеры использования:**

```bash
source .venv/bin/activate

# STEP рядом со скриптом
python scripts/cad-export.py hardware/joints/joint_module_v1.py

# STEP + STL
python scripts/cad-export.py hardware/joints/joint_module_v1.py --stl

# в другую папку
python scripts/cad-export.py hardware/joints/joint_module_v1.py -o build/export
```

---

### Краткий чеклист на сейчас

- [x] `requirements-cad.txt` + локальный venv  
- [x] `scripts/cad-show.py`  
- [ ] `scripts/cad-export.py` (код выше)  
- [ ] Дописать cheatsheet в `docs/build123d-guidelines.md`  
- [ ] Упомянуть guidelines + lifecycle в правилах CAD-агента  
- [ ] Договориться о раскладке `hardware/.../*.py` + `*.step`

После этого цикл `generate → run/export → inspect → fix` становится полностью рабочим и для тебя, и для LLM.

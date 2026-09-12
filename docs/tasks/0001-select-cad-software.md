# Select CAD software (and related tools)

## A. Критерии и рамки
- [ ] A1. Зафиксировать обязательные критерии (LLM-friendliness, open-source, headless/CLI/MCP, STEP как SoT, Git-native, экспорт STL/3MF, скриптовость)
- [ ] A2. Зафиксировать желательные критерии (сборка/assemblies, named faces/edges, интеграция с FEM, PCB/STEP, симуляция MuJoCo/Isaac)
- [ ] A3. Определить приоритеты (что must-have vs nice-to-have для Phase 1–2)
- [ ] A4. Создать черновик ADR «CAD Tool Selection» (пока без финального выбора)

## B. Исследование кандидатов
- [ ] B1. CadQuery — зрелость, API, LLM-опыт, assemblies, экспорт, headless
- [ ] B2. build123d — сравнение с CadQuery, стиль API, документация, экосистема
- [ ] B3. FreeCAD (Python API + headless + MCP) — возможности, ограничения, FEM
- [ ] B4. llmcad — насколько минималистичный API реально помогает LLM
- [ ] B5. Replicad — браузерный/TS-вариант, ограничения WASM
- [ ] B6. OpenSCAD — только как baseline/fallback для простых деталей
- [ ] B7. Сводная сравнительная таблица (критерии × кандидаты)

## C. Практические тесты (минимальный benchmark)
- [ ] C1. Определить 2–3 тестовых сценария (например: простой joint module, parametric plate + holes + fillet, простая assembly из 2–3 деталей)
- [ ] C2. Для каждого кандидата: генерация скрипта LLM → запуск → STEP + STL + screenshot/viewport
- [ ] C3. Оценка: сколько итераций нужно LLM, качество геометрии, удобство отладки, стабильность
- [ ] C4. Проверка Git-workflow (diff скрипта, CI-рендер, экспорт)

## D. Смежные инструменты (учёт, не полный выбор)
- [ ] D1. PCB: подтвердить KiCad как основной, проверить STEP-обмен с выбранным CAD
- [ ] D2. 2D/чертежи: минимальные требования (DXF/SVG/TechDraw)
- [ ] D3. FEM/тепло/механика: список кандидатов (FreeCAD FEM, CalculiX, Gmsh…) и требования к геометрии (STEP → mesh)
- [ ] D4. Симуляция: совместимость экспорта с MuJoCo / Isaac (меши, коллизии, инерция)

## E. Версионирование и структура репозитория
- [ ] E1. Предложить структуру `hardware/` (или `cad/`) под code-CAD + STEP
- [ ] E2. Описать workflow: скрипт → STEP (SoT) → STL/3MF (производные)
- [ ] E3. CI: автоматический рендер превью + проверка сборки STEP
- [ ] E4. Оценить возможность 3D-diff / history (History Workbench, кастомные скрипты)

## F. Решение и фиксация
- [ ] F1. Выбрать primary CAD + fallback
- [ ] F2. Заполнить ADR с обоснованием
- [ ] F3. Обновить `docs/ROADMAP.md` и `docs/current-state.md`
- [ ] F4. Зафиксировать минимальный tool-chain (CAD + экспорт + просмотр + CI)
- [ ] F5. (Опционально) Набросать первые шаблоны модулей под выбранный CAD

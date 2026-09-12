---
title: Тестирование инфраструктуры LLM + CAD (Тест S1)
date_created: 2026-09-13
date_updated: 2026-09-13
participants: [Bunch, Gemini]
status: open
closed_reason:
language: ru
tags: [cad, tasks, testing]
related:
  - docs/tasks/0002-test-llm-cad-infrastructure.md
  - docs/build123d-guidelines.md
---

# Тестирование инфраструктуры LLM + CAD (Тест S1 — Parametric Plate)

## Summary
Проведено первое тестирование автоматического создания, валидации и экспорта деталей с использованием build123d в рамках сценария S1. Успешно сгенерирована параметрическая пластина, выполнен экспорт в STEP и STL. Выявлена важная особенность окружения (venvPath в домашней директории) и ограничение песочницы для ocp-vscode.

## Discussion

---
**2026-09-13**
---

---
**Bunch**

Проведи тест S1 из `docs/tasks/0002-test-llm-cad-infrastructure.md`.

---
**Gemini**

Я провел успешное тестирование сценария S1. Вот подробный отчет по шагам протокола выполнения:

### 1. Выявление настроек окружения
Для запуска скриптов CAD используется виртуальное окружение, расположенное по пути:
`/home/bunch/.venv/cad/bin/python` (согласно конфигурации `pyrightconfig.json`).
Запуск команд напрямую через данный интерпретатор позволяет избежать необходимости ручной активации shell-окружения на каждом шаге.

### 2. Генерация скрипта (S1)
Создан файл `hardware/s1_parametric_plate.py` с чистым Python-кодом build123d, соответствующий всем требованиям:
- Переменные размеров вынесены наверх в виде констант (`PLATE_WIDTH`, `PLATE_LENGTH`, `PLATE_THICKNESS` и др.).
- Все промежуточные CAD-переменные (такие как `vertical_edges`, `top_face` и др.) снабжены префиксом `_` (`_vertical_edges`, `_top_face`), чтобы сборщик объектов экспорта (`scripts/cad-export.py` и `scripts/cad-show.py`) не пытался добавить их в `Compound` вместе с финальным телом. Это решает проблему дублирования/ошибок топологии при автоматическом сборе объектов из пространства имен модуля.

### 3. Запуск и headless экспорт (STEP & STL)
Скрипт экспорта успешно запущен:
```bash
/home/bunch/.venv/cad/bin/python scripts/cad-export.py hardware/s1_parametric_plate.py --stl
```
Результат работы:
- STEP успешно экспортирован в `hardware/s1_parametric_plate.step`
- STL успешно экспортирован в `hardware/s1_parametric_plate.stl`

Число итераций агента для создания корректного STEP: **2 итерации** (на первой итерации возникла ошибка импорта из-за venv и сборщика `collect_cad_objects` из-за промежуточных переменных, на второй итерации всё исправлено).

### 4. Узкое место и ограничение `ocp-vscode` (Визуализация)
При попытке визуализации с помощью `scripts/cad-show.py`:
```bash
/home/bunch/.venv/cad/bin/python scripts/cad-show.py hardware/s1_parametric_plate.py
```
Произошла ошибка выполнения:
`OSError: [Errno 30] Read-only file system: '/home/bunch/.ocpvscode.lock'`

**Причина:** Библиотека `ocp_vscode` пытается записать файл блокировки в домашний каталог пользователя (`/home/bunch/.ocpvscode.lock`). В рамках безопасной песочницы агента запись вне рабочей директории проекта и `/tmp` заблокирована.
**Рекомендация:** 
1. Для headless-валидации и экспорта моделей агенту не следует запускать `cad-show.py`. Достаточно убедиться в успешной компиляции и экспорте в STEP через `cad-export.py`.
2. Добавить это ограничение в `docs/build123d-guidelines.md` в раздел правил для агента.

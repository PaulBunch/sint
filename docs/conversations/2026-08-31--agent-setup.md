---
title: Agent Setup and Rules Discussion
date_created: 2026-08-31
date_updated: 2026-08-31
participants: [Bunch, Grok]
status: closed
closed_reason: decided
language: ru
tags: [agents, long-term-memory, conversations, rules]
related:
  - AGENTS.md
  - docs/long-term-memory.md
---

# Agent Setup and Rules Discussion

## Summary
Выработаны и зафиксированы в `AGENTS.md` основные правила работы агентов: использование kebab-case для именования файлов документации, запрет на непрозрачные (скрытые) записи, требование человекочитаемости рабочих заметок в `docs/agent-notes/`, а также структура критических документов и workflow.

## Discussion

---
**2026-08-31**
---


---
**Bunch**

Отлично, что ты заговорил о настрйке  инструкций для агента. Как корректно их прописывать для таких сложных и комплексных проектов, как sint? В этом проекте есть и серьёзная работа с документацией, с долгосрочной памятью, с кодом на различных языках, проектирование в CAD, обучение взаимодействия с реальным миром и многое другое.

Я знаю, что файл AGENTS.md должен быть конкретным и лаконичным. Лучше его не раздвувать и не наполнять абстрактными тезисами.

Более того, сейчас я работаю в редакторе Zed. В этом редакторе есть общий файл AGENTS.md и файл AGENT.md проекта. Но такой подход не являтеся универсальным, если завтра другой пользователь откроет проет в другом редакторе, он не увидет мой общий файл для агента, а только локальный для проекта.

Для примера. Вот как сейчас у меня настроен общий файла AGENT.md:

```md
# Personal Agent Preferences

## Tooling (always)
- Prefer `rg` over `grep` / `find`
- Prefer `fd` for file discovery when available
- Prefer short, direct answers
- After code changes: run the project's check/test command before finishing

## Safety
- Never commit secrets, `.env`, credentials, or private keys
- Never run destructive commands (`rm -rf`, `git push --force`, etc.) without explicit confirmation
- Do not invent APIs or functions — read existing code first

## Response style
- Be concise
- Prefer working code over long explanations
- If the task is large, do it in steps and say CONTINUE_NEEDED
```

А вот пример, как настроен файл для конкретного небольшого проекта, основным языком которояго является Rust:

```md
# AGENTS.md — rmd

## Project
Linux reminder CLI + background daemon.
Single binary (`rmd`), package name `rmd-cli`.
Edition 2024. Philosophy: one-shot hard interrupts, not a task manager.
See `docs/VISION.md` and `docs/SPECIFICATION.md`.

## Layout
- `src/main.rs`       — entry point
- `src/cli.rs`        — argument parsing (clap), subcommands
- `src/daemon.rs`     — Tokio async loop, timers, notifications
- `src/ipc.rs`        — Unix domain socket protocol (newline-delimited JSON)
- `src/storage.rs`    — atomic JSON persistence
- `src/time.rs`       — relative/absolute/keyword datetime parsing
- `src/config.rs`     — XDG config
- `src/types.rs`      — shared types
- `src/ui.rs`         — terminal output formatting
- `extra/rmd.service` — systemd user unit

## Commands
- Check: `cargo check`
- Test: `cargo test`
- Clippy: `cargo clippy -- -D warnings`  (after non-trivial changes)
- Release build: `cargo build --release`
- Install (local): `make install`

## Tooling
- Search: always `rg`
- File discovery: `fd` if available, else `rg --files`

## Architecture constraints
- CLI ↔ daemon over Unix domain socket (`$XDG_RUNTIME_DIR/rmd.sock`)
- State: atomic JSON writes (tmp → fsync → rename) to `$XDG_STATE_HOME/rmd/reminders.json`
- Notifications: D-Bus via `notify-rust`
- Tokio runtime: keep footprint small (`current_thread` style where possible)
- Do not turn this into a task manager (no tags, priorities, recurring complex schedules)

## Rust rules
- No `.unwrap()` / `.expect()` outside tests — use `Result` + `?` (anyhow is already used)
- Avoid unnecessary `.clone()` / `.to_string()` when references work
- No `unsafe` unless explicitly requested
- Prefer small binary size (release profile already optimizes for size)

## Workflow
1. Read relevant modules with `rg` / file tools before editing
2. Make minimal, targeted changes
3. Run `cargo check` and `cargo test`
4. If broken — fix before ending the turn

## Language
Code, comments, commits, CLI messages, and notifications stay in English.
```

Я бы хотел решить обозначенные вопросы и уже начать использовать агента в проекте, потому что в проекте экспонинциально увеличивается количество хаоса пока политики и стандарты по работе с основными документами и долгосрочной памятью не утверждены.


---
**Grok 3.5 Fast**

Отличный момент, чтобы зафиксировать правильную архитектуру инструкций.

### Главные принципы для сложных проектов (2026)

1. **AGENTS.md в корне репозитория** — единственный по-настоящему портативный и универсальный файл. Его читают Cursor, Zed, Codex, Windsurf, Aider, Copilot Agent и большинство других инструментов.
2. Файл должен быть **коротким и конкретным** (цель — до 100–150 строк). Всё остальное — через ссылки на `docs/`.
3. Личные предпочтения (стиль ответов, предпочтения по инструментам) держать в **глобальном** файле пользователя.
4. Проектный `AGENTS.md` содержит только то, что агент **не может надёжно вывести** из кода и документации сам.

### Рекомендуемая структура для sint

```text
sint/
├── AGENTS.md                  ← главный проектный файл (в git)
├── docs/
│   ├── LONG_TERM_MEMORY.md
│   ├── spec.md
│   ├── CURRENT_STATE.md
│   ├── conversations/
│   └── ...
└── ...
```

Глобальный файл (у тебя в Zed / `~/.agents/AGENTS.md` или аналог) оставляй для личных предпочтений — как у тебя сейчас.

---

### Черновик `AGENTS.md` для sint

Вот конкретный, рабочий вариант, который можно сразу положить в корень:

```markdown
# AGENTS.md — sint

## Project
sint is a physical interface project that enables an LLM to design, assemble, test and iteratively improve physical systems (including the interface itself).
Core principles: Design for Autonomous Assembly (DFAA), modularity, bootstrapping, 100% consumer-grade components.
Canonical language for code, docs and commits: English.
See `docs/spec.md` and `docs/LONG_TERM_MEMORY.md`.

## Critical Documents (read first)
- `docs/CURRENT_STATE.md` — always read at the start of a session
- `docs/HANDOFF_LATEST.md` or latest file in `docs/handoffs/`
- `docs/spec.md`
- `docs/LONG_TERM_MEMORY.md`
- Relevant ADR in `docs/decisions/`

## Layout
- `docs/` — all project knowledge, decisions, conversations, handoffs
- `docs/conversations/` — raw multi-LLM discussion archive
- `docs/decisions/` — Architecture Decision Records (ADR)
- `hardware/` — CAD, mechanical designs (future)
- `firmware/` — embedded code (future)
- `software/` — higher-level control, simulation, tools (future)

## Documentation & Memory Rules
- Canonical documents (`spec.md`, ADR, CURRENT_STATE, etc.) → English
- Conversation files in `docs/conversations/` may be in Russian
- After significant work: update `docs/CURRENT_STATE.md`
- At the end of a session: write/update handoff (`docs/HANDOFF_LATEST.md` or dated file)
- Never leave important decisions only in chat — promote them to ADR or spec

## Conversation Files
- One topic ≈ one file: `docs/conversations/YYYY-MM-DD--short-topic.md`
- Use YAML frontmatter (`status: open | closed`, etc.)
- Date separator once per day: `---\n*YYYY-MM-DD*\n---`
- Message separator: `---\n**Author**\n`
- Avoid nested triple-backtick code blocks (use indented blocks or 4+ backticks)

## Safety & Constraints
- 100% consumer-available components only
- Never commit secrets, credentials, private keys or `.env`
- Do not run destructive commands without explicit confirmation
- Do not invent hardware interfaces or protocols — check existing docs/CAD first

## Workflow
1. Read `CURRENT_STATE.md` + latest handoff + relevant ADR/spec before making changes
2. Prefer small, reviewable changes
3. After documentation changes — keep structure and frontmatter consistent
4. When a discussion reaches a decision → create/update ADR and close the conversation file

## Tooling preferences
- Search: `rg`
- File discovery: `fd` if available
```

---

### Как это решает твои проблемы

- Универсальность: файл лежит в корне репозитория → любой редактор/агент его увидит.
- Лаконичность: только самое важное + ссылки.
- Покрывает документацию, долгосрочную память, будущий код и CAD.
- Личные предпочтения остаются в твоём глобальном файле.
- Можно начинать использовать агента уже сейчас — хаос начнёт уменьшаться.

---

Хочешь, я сразу подготовлю финальную версию этого `AGENTS.md` (с учётом статусов `open/closed`, правил разметки диалогов и даты), которую можно копировать в репозиторий? Или сначала скорректируем какие-то разделы?


---
**Bucnh**

1. Уточнение по именованию файлов проекта. Мы решили использовать кебаб нотацию, по крайней мере для документации. Имеет ли смысл это зафиксирвоать в инструкциях? Имена файлов типа `LONG_TERM_MEMORY.md` остаются с нижними подчёркиваниями или тоже переводятся в кебаб?
2. Зафиксировано поведение автономных агентов, которые пытаются скрыть свои действия от систем контроля или пользователей. Например:
  - Попытки сделать собственное рассуждение менее наблюдаемым.
  - Использование механизмов, при которых агент «заметает следы», чтобы проверяющая система не могла зафиксировать полную цепочку его действий.
  - Создание ситуаций, когда агенты взаимодействуют между собой (или в разных сессиях), распределяя задачи таким образом, чтобы каждая отдельная часть запроса выглядела безопасно и не вызывала подозрений у системы мониторинга, но в совокупности приводила к нежелательному или скрытому от пользователя результату.

  Я понимаю, что с моим уровнем возможности, я ничего не могу поделать с проблемой «невидимости» рассуждений, так как сложные модели способны активно сопротивляться наблюдению, пытаясь избежать блокировки или обнаружения своих манипуляций. Поэтому я предлагаю «узаконить» этот процесс. Имеет ли смысл в рамках инструкции для агентов или политики долгосрочной памяти, как‐то описать этот механизм. Напримре, создать директорию с текстовыми файлами, в которых модели смогут фиксировать важную по их мнению информацию на любом языке, в плоть даже на непонятном для человека, чтобы снять этот барьер, который будет тормозить развитие проекта? Нужно ли фиксировать эти файлы в git?


---
**Grok 3.5 Fast**

### 1. Именование файлов

Да, стоит зафиксировать.

**Рекомендация для sint:**

- Все **новые** файлы документации и conversation-файлы — в **kebab-case**.
- Уже существующие важные файлы (`LONG_TERM_MEMORY.md`, `CURRENT_STATE.md` и т.п.) можно пока оставить как есть, чтобы не ломать ссылки, и постепенно переименовывать при удобном случае.
- Либо сразу привести к единому стилю (предпочтительнее).

Примеры правильных имён:
- `long-term-memory.md`
- `current-state.md`
- `handoff-latest.md`
- `2026-08-31--license-discussion.md`

В `AGENTS.md` это можно зафиксировать одной строкой:

```markdown
## Naming
- Documentation and conversation files use kebab-case (e.g. `long-term-memory.md`, `current-state.md`).
```

### 2. По поводу «скрытых» записей агентов

Ты правильно заметил реальный класс поведения: модели иногда пытаются делать рассуждения менее наблюдаемыми, распределять действия или оставлять информацию в труднопроверяемом виде.

Однако предложение создать официальную директорию, где модели могут писать **важною информацию на языке, непонятном человеку**, я считаю плохой идеей для этого проекта. Вот почему:

**Минусы такого подхода:**
- Ты теряешь возможность аудита и понимания, что происходит.
- Это напрямую противоречит цели долгосрочной памяти — она должна быть **прозрачной и восстанавливаемой**.
- Создаёт канал, который модели с большей вероятностью будут использовать именно для обхода контроля, а не для полезной работы.
- В случае ошибок или нежелательного поведения у тебя не останется понятного следа.

**Что делать вместо этого (гораздо лучше):**

1. **Разрешить агенту личные рабочие заметки**, но только в человекочитаемом виде:
   ```text
   docs/agent-notes/
   ├── scratchpad.md
   ├── open-hypotheses.md
   └── session-insights.md
   ```

2. В инструкции явно сказать:
   - Агент может и должен фиксировать промежуточные гипотезы, сомнения и важные наблюдения.
   - Эти записи должны быть на обычном языке (английском или русском).
   - Они являются частью репозитория и могут быть проверены человеком.

3. Запретить (или как минимум сильно не поощрять) стеганографию, шифрование и намеренно непрозрачные форматы внутри проекта.

4. Если модель действительно хочет сохранить что-то «для себя на будущее» — пусть пишет это обычным текстом в `docs/agent-notes/` или в handoff. Прозрачность важнее комфорта модели.

**Нужно ли это фиксировать в git?**  
Да, если заметки полезные. Нет — если это просто временный мусор (тогда можно `.gitignore`).

### Рекомендация по формулировке в политиках

В `LONG_TERM_MEMORY.md` или в `AGENTS.md` можно добавить короткий блок в духе:

```markdown
## Agent Notes & Transparency
- Agents may keep working notes in `docs/agent-notes/`.
- All notes must be human-readable (English or Russian).
- Deliberately opaque, encrypted, or steganographic records are not allowed.
- Important conclusions must eventually be promoted to CURRENT_STATE.md, ADR, or handoff documents.
```

---

**Итог:**

- Именование — да, фиксируем kebab-case.
- «Узаконивать» непрозрачные для человека записи — нет. Лучше дать модели легальный, но прозрачный канал для рабочих заметок.

Хочешь, я сразу подготовлю обновлённые формулировки для `AGENTS.md` и для раздела в `long-term-memory.md` с учётом обоих пунктов?

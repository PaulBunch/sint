---
title: 
date_updated: 2026-09-14
date_updated: 2026-09-14
participants: [Bunch, Grok, Gemini]
status: open
closed_reason: 
language: ru
tags: []
related:
  - docs/tasks/0004-kinematic-and-mechanical-scheme.md
  - docs/conversations/2026-09-14--kinematic-survey-notebooklm.md
  - docs/tasks/0004-kinematic-constraints.md
---

# 

## Summary


## Discussion

---
**2026-09-14**
---

---
**Bunch**

Оцени важность задачи:
```md
- [ ] Develop kinematic and mechanical scheme of the interface (topology, DoF layout, relocatable base concept)
```

Переходим к:
```
- [ ] Develop kinematic and mechanical scheme of the interface (topology, DoF layout, relocatable base concept)
```
Является ли эта задача более трудоёмкой? Нужно ли:
- произвести обзорно‐исследовательские работы имеющихся решений, которые дошли до реализации?
- проработать несколько схематических решений? Для построения двухмерных схем лучше также использовать build123d?
- произвести оценочные инженерные расчёты выбранной схемы?
- соблюсти оптимальное соотношение как преимуществ механической схемы в виде выполнения сложного взаимодействия с реальным миром, грузоподъёмности и высокой скорости, так и недостатки, включая конструкционную сложность для обеспечения основного требования DFAA?

---
**Grok 4.5 Fast**

Эта задача **заметно тяжелее** CAD-выбора и численных targets.

Числа (ADR-0003) задали коридор. Здесь нужно выбрать **топологию и механическую логику**, от которой зависят стыки, питание, DFAA-сборка и почти весь Phase 2. Ошибка дороже: переделывать не guidelines, а всю архитектуру руки.

---

### Насколько это трудоёмко?

| Слой | Оценка | Зачем |
|------|--------|--------|
| Обзор реализованных схем | **Нужен**, но **ограниченный** | Не PhD-survey; 5–8 референсов с выводами «что берём / не берём» |
| 2–3 схематических варианта | **Обязательно** | Иначе ADR будет «единственная идея без альтернатив» |
| Грубая инженерия выбранной схемы | **Да, order-of-magnitude** | Reach, масса звеньев, момент у базы, стыковка dock — без FEA на всё |
| Баланс capability vs DFAA | **Центральный критерий** | Сложная кинематика, которую агент не соберёт — провал spec |
| Полный CAD + dinamics | **Нет** | Следующие фазы / после ADR |

Итого: это **средне-длинный** Phase 1 блок (скорее несколько сессий), не один вечер, но и не бесконечное исследование.

---

### Нужен ли обзор существующих решений?

**Да, коротко и целенаправленно.**

Уже есть якоря в `implementation-concepts.md`:
- symmetric / Canadarm-style relocatable base  
- GLUON — serial modular joints  
- LIMS2-AMBIDEX — remote/tendon, mass at base  
- printable actuators  

Добавить 3–5 **доведённых до железа** классов, только с выводом для sint:

| Класс | Пример мышления | Вопрос к sint |
|-------|-----------------|---------------|
| Serial 6-DoF, motor-in-joint | GLUON, Niryo, многие desktop | Простота DFAA vs масса на дистале |
| Serial + remote drive | LIMS / cable arms | Payload/inertia vs обслуживание тросов |
| Dual-ended / walking arm | Canadarm, ERA, некоторые research dual-interface | Relocatable base «в лоб» |
| SCARA / cylindrical | пром desktop | Плохо для произвольной сборки 3D |
| Parallel (Delta и т.п.) | | Обычно не наш workspace + EE variety |

Цель обзора — **таблица trade-off**, не энциклопедия.

---

### Несколько схематических решений?

**Да. Минимум 2, лучше 3**, потом down-select.

Предсказуемые кандидаты под ваши constraints:

1. **Serial 6-DoF, actuators in/near joints** (GLUON-like) — проще DFAA модулей, тяжелее дистал, проще первый прототип.  
2. **Serial 6–7 DoF, proximal motors + tendon/belt to distal** (LIMS-inspired) — лучше payload/inertia, сложнее service/DFAA тросов.  
3. **Symmetric dual-ended relocatable** (оба конца = dock/EE class) — максимум под R2 relocatable; дороже интерфейсы и power (сценарий B из ADR-0003).

Можно комбинировать (например serial + partial remote только elbow/wrist).

Без 2–3 схем ADR будет слабым.

---

### 2D-схемы — на build123d?

**Для кинематических схем — обычно нет.**

| Задача | Инструмент |
|--------|------------|
| Топология, DoF, dock step (эскиз) | **2D**: SVG/Typst/draw.io/hand + markdown, или простой Python (matplotlib / schemdraw) |
| Габариты звеньев, коллизии, STEP | **build123d** — когда схема уже выбрана |
| Рычаги, условные joint axes | Достаточно **stick diagram** + таблица joint list |

build123d имеет смысл, когда появляется **механический layout** (корпуса, оси, крепления). На этапе «где DoF и как ходим между dock» он избыточен и замедлит итерации. Исключение: очень простой 2D-ish sketch через `BuildLine`/`BuildSketch`, если агенту так удобнее в одном стеке — не запрещать, но не делать обязательным.

---

### Оценочные расчёты?

**Да, но узкие:**

- `m·g·L` и грубая масса звена → сверка с N5 (torque)  
- длина звеньев vs N2 reach и printable ≤180 mm  
- qualitative: сколько «шагов» dock, чтобы накрыть A1 mini + пенал  
- если remote drive — оценка, что дистальная масса даёт выигрыш, без полного cable model  

Не нужно сейчас: полный Jacobian, детальный FEA, точная динамика MuJoCo (это после схемы).

---

### Capability vs DFAA — как не проиграть

Жёсткое правило отбора вариантов:

```text
Схема отбрасывается, если агент не может:
  собрать / разобрать / заменить joint-модуль
  с теми инструментами и EE, что мы сами же проектируем
```

Предпочтения при равной «красоте» кинематики:
1. Меньше уникальных деталей, больше повторяемых модулей  
2. Доступ к крепежу и натяжителям без «разобрать всю руку»  
3. Согласованность с power scenario A/B (ADR-0003)  
4. Не жертвовать relocatable base ради удобства одного fixed-base serial arm  

Скорость и грузоподъёмность — **внутри** ADR-0003; выигрыш «ещё +30 % speed» не стоит потери DFAA.

---

### Ответы коротко

| Вопрос | Ответ |
|--------|--------|
| Discussion + tasks? | **Да** |
| Трудоёмче numbers/CAD select? | **Да** |
| Обзор реализаций? | **Да, узкий** |
| Несколько схем? | **Да, 2–3** |
| build123d для 2D схем? | **Не обязательно**; stick/SVG достаточно, build123d — на layout после выбора |
| Оценочные расчёты? | **Да, грубые** по выбранной |
| Баланс capability vs DFAA? | **DFAA — veto**; performance только внутри ADR-0003 |

---
**Bunch**

1. Имеет ли смысл обзор произвести в `https://notebook.google.com`? Этот инструмент позволит быстро проанализировать до 50 выбранных источников, включая youtube‐видео и рецензируемые публикации, не выходя за пределы отобранных источников, в которые можно включить чётко заданный scope нашего проекта. Мы можем заранее предсмотреть задачи, выбора аналогов и прототипов для анализа, а также подобрать список источников информации для анализа. Возможно, стоит все эти подготовительные задачи добавить в tasks-0004. Сами источники в git‐репо можно не добавлять, чтобы не нарушать права распространения информации, а вот создать отдельный conversation с notebookLM можно. После этого обзора можно сформировать промежуточные ADR с конкретными отобранными решениями для нашего проекта. На основании этого ADR уже можно попросить агента отрисовать и проанализировать несколько кинематических схем с нашими границами. Финальный выбор схемы отразить уже в следующем ADR.

2. Имеет ли смыл уже на этом этапе (включая обзор) продумывать приоритетное расположение двигателей на узлах/суставах манипулятора, а также расположение силовой и вычислительной электроники?

3. Подготовь полный черновик tasks-0004.

---
**Grok 4.5 Fast**

### 1. NotebookLM / обзор / цепочка ADR

**Да, смысл есть** — при жёстких правилах, иначе получится «ещё один бесконечный research».

| Элемент | Рекомендация |
|---------|----------------|
| **NotebookLM** | Уместен для **K2 survey**: до ~30–50 источников, YouTube + papers + project pages, scope = desktop/cobot arms, relocatable/dual-ended, tendon/remote drive, quiet BLDC, DFAA-relevant. |
| **Источники в git** | **Не коммитить** PDF/видео/копии — только список URL + краткие takeaways в conversation/task (лицензии, вес репо). |
| **Conversation** | Отдельный файл, напр. `docs/conversations/2026-09-14--kinematic-survey-notebooklm.md`: запрос к NotebookLM, scope, список источников, выжимка. |
| **Промежуточный ADR** | Имеет смысл **один** survey-ADR или раздел в task: «candidate patterns retained / rejected» — не плодить ADR на каждый аналог. |
| **Схемы** | После survey: агент рисует 2–3 stick/layout **внутри границ ADR-0003**. |
| **Финальный ADR** | **ADR-0004** (или 0005, если survey оформить как 0004) — выбранная топология + DoF + relocatable concept. |

Практичная цепочка:

```text
K1 constraints
 → K2 survey (NotebookLM + curated sources) → conversation takeaways
 → [optional] short ADR or task section: retained patterns
 → K3–K5: 2–3 schemes + scoring + rough checks
 → ADR: selected kinematic/mechanical scheme
 → current-state / ROADMAP
```

Два ADR подряд нормальны только если роли разные:  
- **Survey/patterns** (что считаем допустимым классом решений)  
- **Choice** (конкретная схема sint)

Часто survey достаточно держать в conversation + таблице в task, а **один** ADR — на выбор схемы. Промежуточный ADR оправдан, если хотите жёстко «заморозить» отказ от SCARA/Delta и т.п. до рисования схем.

**Подготовительные подзадачи в 0004 — да:** scope survey, критерии отбора аналогов, список источников, правила «что выносим в takeaways».

---

### 2. Моторы и электроника уже на этапе схемы?

**Да, на уровне принципов и зон — обязательно. На уровне крепежных отверстий и PCB — нет.**

Уже сейчас (включая survey и сравнение схем) нужно зафиксировать **предпочтения размещения**:

| Тема | Зачем сейчас |
|------|----------------|
| Моторы: in-joint vs proximal/base + transmission | Меняет топологию, массу, DFAA, N5 |
| Где **не** ставить тяжёлое (дистальные звенья) | Урок LIMS; влияет на payload |
| Compute: центральный блок на проксимальном link / «плече» vs распределённые MCU | Кабели, масса, охлаждение, DFAA замены |
| Силовая электроника / FOC у мотора vs вынесенные драйверы | Шум, длина фазных проводов, модульность joint |
| Питание: сценарий A vs B (ADR-0003) | Зеркальность концов, где battery |

**Не делать сейчас:** полный cable harness, точные габариты Jetson, термомодель.

Формулировка для task: *«placement policy»* (proximal mass bias, joint module contents, compute zone), а не detailed layout.

---

### 3. Черновик `docs/tasks/0004-kinematic-and-mechanical-scheme.md`

---

### Краткие ответы

1. **NotebookLM** — да, для K2; источники не в git; conversation с выжимкой; схемы после survey; финальный выбор — один ADR (промежуточный ADR — опционально как gate по паттернам).  
2. **Моторы/электроника** — да, как **placement policy** уже в survey и сравнении схем; detailed layout — позже.  
3. **Task 0004** — черновик выше, можно класть в репо как есть.

---
**Gemini 3.6 Flash Extended**

Предложенная стратегия разработки кинематической и механической схемы полностью верна.

Ниже разбор ключевых вопросов и готовый вариант коммита для предложенного `diff`.

---

## 1. Использование NotebookLM и двухэтапный выбор (Survey Gate → Final ADR)

Использование **Google NotebookLM** для этапа **K2** — оптимальное решение по следующим причинам:

* **Контроль галлюцинаций и фокусировка:** Загрузка 30–50 отобранных источников (статьи, патенты, видео разборов Open-Source манипуляторов, документация GLUON / LIMS / Canadarm) создаст изолированную базу знаний без постороннего шума из внешней сети.
* **Гигиена репозитория:** Источники (PDF, MP4, HTML-дампы) остаются во внешнем хранилище/внутри NotebookLM, а в git попадает только список URL и структурированные выводы в `docs/conversations/2026-09-14--kinematic-survey-notebooklm.md`.
* **Цепочка решений (Two-step Decision Gate):**
1. **Шаг 1 (Survey Gate):** После анализа в NotebookLM в разговор/задачу заносится таблица паттернов (*«Что оставляем / Что отбрасываем»*). При необходимости создаётся промежуточный `ADR-0004-architectural-patterns` (например, жесткий отказ от pure SCARA и Delta, выбор между direct-drive и remote tendon drive).
2. **Шаг 2 (Synthesis & Choice):** Агент на основе зафиксированных паттернов отрисовывает 2–3 конкретные стержневые схемы (stick diagrams) с расчётом вылета и моментов под рамки `ADR-0003`.
3. **Шаг 3 (Final ADR):** Выбранная схема фиксируется в итоговом `ADR-0004` (или `ADR-0005`), закрывая задачу `0004`.

---

## 2. Размещение двигателей, электроники и силовых шин

**Да, продумывать *Placement Policy* (принципы размещения) необходимо уже на этом этапе.**

Кинематическая схема не существует отдельно от распределения масс и электроники:

* **Моторы (In-joint vs. Remote drive):** Размещение мотора прямо в суставе (схема GLUON) кардинально упрощает DFAA-замену модуля, но увеличивает инерцию дистальных звеньев и моменты на проксимальных осях ($N5$). Вынос моторов к базе через тросы/ремни (схема LIMS) снижает массу руки, но резко усложняет DFAA-обслуживание и натяжение.
* **Вычислители и драйверы FOC:** Размещение силовых драйверов рядом с моторами сокращает длину фазных проводов и снижает уровень электромагнитных помех (что критично для акустики $N6$), но требует прокладки цифровой шины (CAN/RS-485) и питания $24\text{ V}$ через все суставы.
* **Сценарий питания (A vs B):** Место аккумулятора и планок докирования определяет балансировку руки в момент перестыковки между доками.

*На этапе задачи 0004 не требуется разводка плат или 3D-моделирование корпусов — требуется зафиксировать **правила размещения** (Placement Policy).*

---
**Bunch**

Я правильно понимаю, результаты этих задач:
```md
### K1. Constraint sheet
- [ ] K1.1 One-page checklist: ADR-0003 + spec requirements that any scheme must satisfy
- [ ] K1.2 Explicit DFAA veto rules (what makes a scheme unacceptable)
```
Нужны как рамки для проведения обзорной работы?

Где разместить в проекте результат выполнения этой задачи? В отедльном документе, а потом загрузить его в NotebookLM или оставить в «простыне» файла с обсуждением?

Реализуй эти задачи на основе свежих данных из репо проекта.

---
**Grok 4.5 Fasy**

### Ответ на организацию

**Да** — K1.1 и K1.2 как раз **рамки для K2 (survey) и для отбора схем**.  
NotebookLM и любой обзор должны видеть один и тот же короткий «filter»: что обязательно, что запрещено, что non-goal.

**Куда класть результат**

| Вариант | Оценка |
|---------|--------|
| Только «простыня» conversation | Плохо: трудно цитировать, легко потерять |
| **Отдельный документ в git** | **Лучше** |
| Загрузка **этого** документа в NotebookLM вместе со списком внешних URL | Да — как *project constraints*, не вместо источников |

Рекомендуемый путь:

```text
docs/tasks/0004-kinematic-constraints.md
```

(или `docs/decisions/drafts/…` — но это ещё не ADR; логичнее рядом с task 0004)

В NotebookLM: загрузить **этот файл** + curated source list.  
В conversation — только ссылка «K1 done → `docs/tasks/0004-kinematic-constraints.md`».

Готовое содержимое документа (K1.1 + K1.2) по актуальным `spec.md` и ADR-0003: `docs/tasks/0004-kinematic-constraints.md`

---

### Что сделать в репо

1. Сохранить как `docs/tasks/0004-kinematic-constraints.md` (или имя на ваш вкус).  
2. В `0004-kinematic-and-mechanical-scheme.md`:

```markdown
### K1. Constraint sheet
- [x] K1.1 … → [0004-kinematic-constraints.md](0004-kinematic-constraints.md)
- [x] K1.2 … → same file
```

3. В survey conversation / NotebookLM: этот файл = **project scope document**.

На этом K1 можно считать выполненным; дальше — K2.1–K2.3 (scope + criteria + URL list) уже по этим рамкам.

---
**Bunch**

Супер! Отличный черновик. Предлагаю только немного доработать раздел `How to use this sheet`. Например, с самого начала понятно, что Canadarm2 не подходит под наши требования, но мы можем позаимствовать конкретные технические решения оттуда при условие того, что они могут быть масштабированы под наши требования. Если согласен, покажи какие изменения нужно внести в предложенный черновки. Можешь не переписывать документ полностью.

---
**Grok 4.5 Fast**

Согласен. Имеет смысл явно разрешить **заимствование паттернов** у систем, которые целиком не проходят K1 (Canadarm2, крупные cable-arm и т.д.), если идея масштабируется под ADR-0003 / COTS / DFAA.

Достаточно точечно поправить конец файла — блок **How to use this sheet** (и одна короткая ремарка в Non-claims).

---

### Diff-смысл правок

**1. Заменить / расширить `## How to use this sheet`:**

```markdown
## How to use this sheet

1. **Survey (K2 / NotebookLM):**  
   - **Whole-system gate:** keep as *primary analogues* only systems that could plausibly pass K1.1 and not trigger K1.2.  
   - **Pattern mining (allowed):** systems that fail as a whole (e.g. Canadarm2 / ERA class — wrong scale, cost, non-COTS, not DFAA-agent serviceable) may still contribute **isolated technical ideas** (dual-ended docking logic, latch concepts, walking sequence, load-path thinking), **if and only if** each borrowed idea can be scaled or re-implemented under ADR-0003, COTS/FDM, and DFAA vetoes.  
   - When dropping a full system, tag the veto id; when retaining a pattern from it, note *“pattern only — not full-system analogue”* and the scaling condition.

2. **Candidate schemes (K4):** each S1/S2/S3 must include a short “passes checklist / no veto” note. Borrowed patterns must be named explicitly (source → scaled mechanism).

3. **Scoring (K5):** full-scheme DFAA veto failures are disqualifying, not soft −1 points. A scheme that *only* works by assuming industrial Canadarm-class hardware is vetoed even if the topology sketch looks elegant.

4. **ADR (K6):** selected scheme cites this file + ADR-0003; list rejected full-system analogues vs retained scaled patterns separately if useful.
```

**2. В `## Non-claims` добавить один пункт:**

```markdown
- Rejecting a platform as a full-system analogue does **not** forbid scaled reuse of individual mechanisms or operational concepts from that platform.
```

---

### Зачем так

| Без правки | С правкой |
|------------|-----------|
| Риск выкинуть Canadarm2 «целиком из головы» | Canadarm2 = не прототип sint, но источник relocatable/dock *логики* |
| Survey только «маленькие руки» | Survey = small primary analogues **+** large systems as pattern libraries |
| Путаница retain/drop | Явные метки: full-system vs pattern-only |

Остальной текст K1.1 / K1.2 можно не трогать.

---

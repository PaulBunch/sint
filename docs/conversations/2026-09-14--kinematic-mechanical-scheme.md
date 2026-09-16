---
title: 
date_created: 2026-09-14
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
  - docs/tasks/0004-kinematic-survey-scope.md
  - docs/decisions/0004-kinematic-survey-patterns.md
  - docs/tasks/0004-placement-policy.md
  - docs/tasks/0004-candidate-schemes.md
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
**Bunch**

Преходим к задачам:
```md
### K2. Survey of implemented analogues (curated, not open-web sprawl)
- [ ] K2.1 Define survey scope (include / exclude)
  - Include: desktop/cobot serial arms, dual-ended or relocatable concepts, tendon/remote-drive arms, quiet BLDC modular joints, printable actuator stacks
  - Exclude: industrial 50+ kg arms, pure SCARA/Delta as primary, legged humanoids as primary
- [ ] K2.2 Define selection criteria for analogues (reached hardware, public docs/video, relevance to DFAA/relocatable/quiet/COTS)
```

Я не совсем поинмаю, чем задача K2.2 отличается от уже подготовленного документа?

В рамках подготовки списка проектов для обзора предлагаю обсудить следующих кандидатов (мне интересно узнать твоё мнение):
```md
## Основные кандидаты:
- Annin Robotics AR4 MK5
- POROL6
- Canadarm2
- European Robotic Arm
- INNFOS GLUON — modular desktop arm / integrated quiet actuators (Kickstarter & reviews)
- IRIM Lab KOREATECH — LIMS2-AMBIDEX tendon-driven low-inertia arms

## Потенциальные кандидаты:
- Robot Learning Lab (RLL) — Project Blue (также известен как Berkeley Open Arms)
- 1X Technologies — EVE (Halodi Eve)
- Haro380
- Elephant Robotics myCobot 280 M5 X Edition
```

---
**Grok 4.5 Fast**

### K2.2 vs constraint sheet — в чём разница

| | **K1 (`0004-kinematic-constraints.md`)** | **K2.2 (selection criteria for analogues)** |
|---|------------------------------------------|-----------------------------------------------|
| Вопрос | Какой **наша** схема **должна** уметь / что **запрещено** | Какой **чужой проект** вообще **имеет смысл читать** |
| Объект | Будущий sint | Источники для survey |
| Пример | «Veto, если нет ≥2 dock story» | «Берём в обзор только то, что дошло до железа и есть публичное видео/док» |
| Пример | «Payload 0.5 kg continuous» | «Релевантен ли проект к quiet BLDC / relocatable / DFAA, даже если цифры другие» |

K1 = **фильтр на выход** (наша схема).  
K2.2 = **фильтр на вход** (кого изучаем).

K2.1 = **тематические границы** (какие *классы* машин).  
K2.2 = **качество и полезность источника** (железо vs слайд, открытость, чему учимся).

Краткий текст для K2.2 (можно вписать в task):

```markdown
### K2.2 Selection criteria (for including a project in the survey)

Include a source if most of the following hold:
1. **Reached hardware** — built and demonstrated, not only a paper concept
2. **Public evidence** — docs, paper, and/or video sufficient to judge topology / actuation / docking
3. **Relevance to at least one sint axis:** relocatable/dual-ended logic, serial modular joints, remote/tendon drive, quiet BLDC, printable/COTS actuators, agent-serviceable modularity
4. **Learnable pattern** — even if the full system fails K1, a scalable subsystem idea exists (see constraint sheet “pattern mining”)

Deprioritize or exclude from *primary* list if:
- Brochure-only / no motion evidence
- Closed industrial cell with no transferable mechanics
- Relevant only to locomotion (legs) or planar pick-and-place as the main lesson
```

---

### Мнение по вашему списку

Легенда: **P** = primary analogue (близкий класс), **M** = pattern mine only, **L** = low priority / узкий урок, **X** = слабый fit для этого survey.

#### Основные кандидаты

| Проект | Роль | Комментарий |
|--------|------|-------------|
| **INNFOS GLUON** | **P** | Уже в implementation-concepts: тихий modular BLDC, ~0.5 kg, desktop serial. Обязателен. |
| **IRIM LIMS2-AMBIDEX** | **P** (pattern + partial system) | Ключевой урок remote drive / mass distribution; целиком не COTS/DFAA-агент, но паттерн — must. |
| **Annin AR4 MK5** | **P** | Открытый/полуоткрытый 6-DoF, реальное железо, maker-сборка, serial in-joint. Хорош для DFAA-модульности и «как собирает человек → что упростить для агента». |
| **POROL6** (если это open 6-DoF / Poroline-класс open arm — уточните точный репозиторий при K2.3) | **P** или **L** | Имеет смысл, если есть публичная кинематика + BOM/сборка; иначе не раздувать список. Перед фиксацией — одна проверка «hardware + docs». |
| **Canadarm2** | **M only** | Не primary: масштаб, стоимость, не COTS, не agent-DFAA. **Оставить** ради dual-ended / walk-off-dock / base change logic (как в constraint sheet). |
| **European Robotic Arm (ERA)** | **M only** | То же семейство, что Canadarm: relocatable base, symmetrical operations. Дублирует Canadarm2 — в survey достаточно **одного** детального + второго короткой строкой «same family». |

#### Потенциальные

| Проект | Роль | Комментарий |
|--------|------|-------------|
| **Berkeley / RLL Blue (Open Arms)** | **P** (если смотрите open hardware arm stack) | Полезен для open manipulators + learning stack; кинематика скорее классический serial. Брать за modularity/open docs, не за relocatable base. |
| **Elephant myCobot 280** | **P (light)** | Массовый desktop 6-DoF, малый payload, понятная serial схема, слабый relocatable. Урок: компактные joint modules, лимиты payload/reach — хорошо стыкуется с N3/N2. |
| **1X EVE (Halodi)** | **L / M** | Колёсный humanoid-service, не arm-primary. Имеет смысл только точечно (тихоходность, human-near), **не** как kinematic analogue руки. Легко размазать scope — я бы **не** в core list. |
| **Haro380** | **L** до проверки | Нужно ясно, *какой* Haro380 (часто путают линейки). В core не ставить, пока нет 2–3 публичных артефактов (DoF, drive, video). Иначе шум в NotebookLM. |

---

### Рекомендуемый состав survey (сбалансированный)

**Primary (глубоко):**
1. INNFOS GLUON  
2. Annin AR4 MK5  
3. IRIM LIMS2-AMBIDEX  
4. Elephant myCobot 280 (короче, compact serial baseline)  
5. Berkeley Blue / open arms — *если* подтверждается открытая мехчасть; иначе заменить на другой open 6-DoF (e.g. SO-ARM / similar — на этапе K2.3)

**Pattern-only (коротко):**
6. Canadarm2 (reloctable / dual-role ends)  
7. ERA — one paragraph, same family  

**Optional / queue (не блокируют K2.5):**
- POROL6 — после верификации  
- Haro380 — после верификации  
- 1X EVE — лучше **исключить** из kinematic survey (scope creep)

Так вы попадаете в дух K2.1 (include/exclude) и не раздуваете NotebookLM до 50 равноправных «главных».

---

### Практично для task

- **K2.1** — зафиксировать include/exclude как в 0004 (+ «space arms = pattern-only»).  
- **K2.2** — вставить критерии выше (hardware, public evidence, relevance, pattern-mining).  
- **K2.3** — URL-список по **рекомендуемому составу**; POROL6/Haro380 — только после 10-минутной проверки «есть железо + доки».

Могу следующим шагом набросать готовые формулировки **K2.1 + K2.2** одним markdown-блоком для вставки в `0004` и шаблон таблицы источников для K2.3.

---
**Bunch**

1. Я опечатался, я имел ввиду проект PAROL6 от Source Robotics: https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm
   Этот проект имеет для меня больший приоритет, чем дрожащая рука SO-ARM. Как минимум в этом проекте можно изучить пневматическую силовую систему. У меня есть мысли, что нам нужно будет прокидвать пневматический канал от dock до энд-эффектора. Для пневматических типов эндэффекторов. 
2. Насчёт расширения task-0004. Если мы принимаем решени фиксировать резульат выполнения K2.1 – K2.3 в tasks, то это нужно делать в отдельном документе, а не в уже имещющихся: 0004-kinematic-and-mechanical-scheme и 0004-kinematic-constraints.
3. Реализуй K2.1 и K2.2. После этого перейдём к подбору источников информации для обзора.

---
**Grok 4.5 Fast**

### Уточнения

**PAROL6 (Source Robotics)** — да, логичнее SO-ARM: открытый desktop arm, железо + репо, плюс у вас явный интерес к **пневматике до EE**. Имеет смысл **primary** в survey, с отдельной строкой takeaway: «нужен ли air pass-through dock→EE». Это не ломает K1, но расширяет R3 (интерфейс EE) на возможный **пневмоканал** — зафиксировать как *open design question*, не как требование ADR-0003.

**Куда писать K2.1–K2.3:** согласен — **отдельный документ**, не раздувать `0004-kinematic-and-mechanical-scheme.md` и не смешивать с constraint sheet.

Рекомендуемый файл:

```text
docs/tasks/0004-kinematic-survey-scope.md
```

В task 0004 только ссылки и чекбоксы `[x]` → этот файл.

Готовое содержимое для **K2.1 + K2.2** (K2.3 — следующим шагом) → [0004-kinematic-survey-scope.md](docs/tasks/0004-kinematic-survey-scope.md)

---

### В parent task 0004

```markdown
### K2. Survey …
- [x] K2.1 … → [0004-kinematic-survey-scope.md](0004-kinematic-survey-scope.md)
- [x] K2.2 … → same
- [ ] K2.3 Build source list …
```

---

### Кратко

1. **PAROL6** — в primary; пневмоканал dock→EE — open question в survey.  
2. **K2.1–K2.3** — отдельный `0004-kinematic-survey-scope.md` (сейчас K2.1–K2.2).  
3. **K2.1/K2.2** — реализованы в блоке выше; дальше — **K2.3** (URL-таблица по provisional set).

---
**Gemini 3.6 Flash Extended**

## Задача K2.3 — Таблица источников обзора (URL-only Source List)

Ниже представлен готовый блок секции **K2.3**, подготовленный для вставки в `docs/tasks/0004-kinematic-survey-scope.md`. Все ссылки ведут на канонические открытые репозитории, техническую документацию и научные публикации (без загрузки бинарников/видео в git).

---

### K2.3 — Curated source list for NotebookLM review

| Проект | Tag | Канонические URL | Ключевые аспекты для изучения | Pneumatic / EE Pass-through |
| --- | --- | --- | --- | --- |
| **PAROL6** *(Source Robotics)* | **P** | • [GitHub: Source-Robotics/PAROL6](https://github.com/Source-Robotics/PAROL6-Desktop-robot-arm)<br>• [MakerWorld: PAROL6 3D Model & Specs](https://makerworld.com/en/models/419189-parol6-3d-printed-desktop-robotic-arm) | 3D-печатный 6-DoF desktop arm, планетарные редукторы, ремённые передачи, компоновка масс, изолированные I/O / CAN-шина. | **Да** *(пневмоканалы и комплиантный схват)* |
| **INNFOS GLUON** | **P** | • [Hackster: INNFOS SCA Actuators](https://www.hackster.io/news/innfos-unveils-a-modular-robotic-arm-driven-by-sca-actuators-e436f9b29823)<br>• [GitHub: SuperHouse GLUONC Controller](https://github.com/SuperHouse/GLUONC) | Серийный тихий BLDC+FOC модуль (SCA: мотор, привод, энкодер, волновой редуктор в одном корпусе), сквозной CAN-bus. | **Нет** *(только питание / CAN)* |
| **Annin Robotics AR4 MK5** | **P** | • [Official Docs: Annin Robotics](https://www.anninrobotics.com/)<br>• [GitHub: Ekumen-OS/ar4 ROS2 stack](https://github.com/Ekumen-OS/ar4) | Открытый 6-DoF манипулятор промышленного типа на шаговых/сервоприводах; технологичность DFAA-сборки человеком. | **Нет** *(электрический серво-схват)* |
| **IRIM Lab / NAVER AMBIDEX (LIMS2)** | **P** | • [Aparobot: AMBIDEX Specs](https://www.aparobot.com/robots/ambidex)<br>• [Hackaday Overview & Mechanisms](https://hackaday.com/2019/10/20/humanoid-robot-has-joints-that-inspire/) | Дистанционный тросовый привод (tendon/cable-driven), распределение масс в плечевом узле, двойной сустав локтя (DLCJ), малая инерция. | **Нет** *(Focus: haptic/cable)* |
| **Elephant Robotics myCobot 280** | **P** | • [GitHub: elephantrobotics/mycobot_ros](https://github.com/elephantrobotics/mycobot_ros)<br>• [Docs: myCobot 280 M5](https://www.google.com/search?q=https://docs.elephantrobotics.com/) | Компактный desktop 6-DoF базового уровня, плотная упаковка joint-модулей, ограничения по грузоподъёмности/жесткости. | **Опционально** *(внешняя прокладка)* |
| **Canadarm2 (SSRMS)** | **M** | • [CSA: Canadarm2 technical background](https://www.asc-csa.gc.ca/eng/iss/canadarm2/)<br>• [NASA: Space Station Remote Manipulator System](https://www.nasa.gov/) | Симметричная схема с двумя одинаковыми рабочий/базовый концами (Latching End Effectors), логика смены базы (walk-off dock). | **Да** *(передача флюидов/энергии/данных через PDGF)* |
| **European Robotic Arm (ERA)** | **M** | • [ESA: European Robotic Arm Overview](https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/International_Space_Station/European_Robotic_Arm) | Симметричный манипулятор с возможностью шагания по станции (relocatable base), автоматическая фиксация за базовые точки. | **Да** *(силовые и коммуникационные разъёмы)* |

---

### Замечания по формированию корпуса источников для NotebookLM (K2.4)

1. **Формат скормливаемых данных:**
* Для **PAROL6** и **AR4** в NotebookLM стоит загрузить страницы `README.md` репозиториев, мануалы по сборке (PDF/Markdown) и описание кинематических звеней.
* Для **GLUON** и **AMBIDEX** — файлы статей/патентов о приводах SCA и кинематике роликовых/тросовых суставов.
* Для **Canadarm2 / ERA** — главу или выдержку из документов NASA/ESA о структуре Latching End Effector (LEE) и логикепереключения с базовой точки на инструментальную.

2. **Зафиксированный вопрос по пневмоканалу:**
* Во всех кандидатах классического desktop-класса (кроме PAROL6) прокладка утилит ограниченна электрическими линиями. PAROL6 и космические манипуляторы служат ключевыми примерами того, как проектировать каналы прохода (пневматика/вакуум) через сочленения и стыковочные узлы (docks).

---
**Bunch**

Переходим к подбору источников информации с акцентом на кинематические и механические схемы. Результат допишем в только что созданный 0004-kinematic-survey-scope.md.

Gemini предложил следующие рекомендации к подбору источников, к которым можно прислушаться. Также можно поискать рецензируемые статьи по проприетарным кандидатам, у которых закрыта инженерная документация.

(список замечаний для NotebookLM от Gemini из предыдущего сообщения)

---
**Grok 4.5 Fast**

Готовый блок **K2.3** дописан в `docs/tasks/0004-kinematic-survey-scope.md`. Акцент на кинематику/механику; учтены замечания Gemini и пневмоканал.

---

### Что сделать в репо

1. Дописать блок в `0004-kinematic-survey-scope.md` после K2.1–K2.2.  
2. В parent task:

```markdown
- [x] K2.3 Build source list → 0004-kinematic-survey-scope.md (§ K2.3)
- [ ] K2.4 Run structured review (NotebookLM + sources above)
- [ ] K2.5 Takeaways table …
```

3. Для NotebookLM: не грузить «весь интернет» — только строки из таблицы + constraint sheet.

**PAROL6** подтверждён как главный источник по **пневмотрассе** (2 connector’а, трубки base→forearm). Это сильнее, чем типичный desktop-only electrical loom, и напрямую закрывает ваш open question без опоры только на космические LEE.

---
**2026-09-15**
---

---
**Bunch**

Я произвёл обзор отобранных проектов в NotebookLM:
https://github.com/PaulBunch/sint/blob/main/docs/conversations/2026-09-14--kinematic-survey-notebooklm.md

Остались ли ещё вопросы, на которые необходимо получить ответы для закрытия задач:
```md
- [ ] K2.4 Run structured review (optional: Google NotebookLM bounded to that source list)
- [ ] K2.5 Write takeaways table: pattern → pros/cons for sint → retain / drop
```

Что думаешь о моих идеях: каскадного выноса масс, двухэтапного дока (Dual-Latch) и локальных вычислительных модулей звеньев («спинной мозг»)? Подходят ли они для sint и стоит ли их учесть при разработке кинематической схемы?

---
**Grok 4.5 Fast**

### K2.4 / K2.5 — можно ли закрывать?

**Да, по сути закрыты.** В conversation уже есть:

| Задача | Что сделано |
|--------|-------------|
| **K2.4** | Разбор PAROL6, AR4, GLUON, LIMS2, myCobot + Canadarm2/ERA по топологии, приводам, коммуникациям, DFAA, масштабируемости |
| **K2.5** | Таблица паттернов → pros/cons → Retain / Pattern-only / Drop, включая пневмоканал |

Дополнительно полезны, но **не блокируют** закрытие K2:

- массы/звенья и углы суставов (уже есть в conversation);
- формальное копирование takeaways-таблицы в `0004-kinematic-survey-scope.md` или короткий note в task 0004;
- status conversation → `closed` после фиксации.

**Не обязательно** снова гонять NotebookLM. Пробелы, если есть, лучше закрывать уже в **K3–K5** (placement policy + схемы), а не в survey.

Рекомендация: отметить K2.4/K2.5 `[x]`, перенести итоговую takeaways-таблицу в git-документ survey-scope (чтобы не жила только в chat), и идти к **K3**.

---

### Три идеи — оценка для sint

#### 1. Каскадный вынос масс (proximal cascade)

**Плечо у основания → локоть в плечевом звене → запястье в предплечье, тросы/ремни снаружи для доступа агента.**

| | Оценка |
|---|--------|
| Согласуется с survey | Да: компромисс между in-joint (PAROL6/GLUON) и full-shoulder remote (LIMS) |
| N5 / инерция EE | Сильный плюс: лёгкая «кисть» для точной сборки |
| DFAA | **Хорошо**, если передачи **доступны снаружи** (снимает риск V5 полного «тросового клубка») |
| Риски | Люфт/растяжение ремней; калибровка; акустика ремней vs N6 |

**Вердикт:** **стоит учесть как placement policy** в K3/K4 (гибрид S2-класса), не как обязательный полный LIMS-клон.

---

#### 2. Dual-Latch / двухэтапный док

Идея: слабое низкоинерционное запястье **не** держит всю руку на консоли; dock имеет **зацеп для запястья + силовой зацеп для плеча**.

| | Оценка |
|---|--------|
| Физика | Верная: при payload/torque из ADR-0003 дистальный joint **~1–5 N·m** не тянет консоль 2.5–5+ кг на 0.5–0.8 m (нужны проксимальные **10–25 N·m**) |
| Canadarm-паттерн | Классика решает симметрией мощных LEE на **обоих** концах; dual-latch — другой путь к асимметричной руке |
| R2 relocatable | Рабочий **если** протокол чёткий: временная фиксация запястьем → силовая стыковка плечом → отпускание запястья |
| Минусы | Сложнее dock (BOM N7, DFAA сборки dock); два разных интерфейса на одном узле; режим «только на запястье» нерабочий под нагрузкой |

**Вердикт:** **иметь в виду как candidate для relocatable story** в K4 (особенно с асимметричной рукой). Не принимать сразу: сначала stick-схема шага A→B и грубая оценка моментов. Альтернатива проще: **более мощный «base end»** (полусимметрия) без двух зацепов на одном dock.

---

#### 3. Локальные compute-модули звеньев («спинной мозг»)

Локальные MCU + offline-адаптация весов/микромодели звена, разгрузка LLM.

| | Оценка |
|---|--------|
| R8 / implementation-concepts | Согласуется с distributed joint MCU (CAN) + central brain |
| Практическая польза | Да: FOC, энкодеры, лимиты, простая компенсация — на link-MCU; LLM — задачи/траектории высокого уровня |
| DFAA | Ок, если модуль **заменяемый brick** на звене |
| Риски перегиба | Полноценный «сон» с обучаемыми весами на каждое звено — рано для Phase 1; раздует ПО, отладку, BOM |
| N6 / real-time | Локальный контур как раз нужен, чтобы FOC не зависел от LLM |

**Вердикт:** **да как принцип K3** — *distributed low-level control + central agent*.  
**Нет** как обязательная «нейромодель звена во сне» до первого железа. Зафиксировать: joint/link MCU = servo+sensing; обучение/адаптация — later research.

*(Сырая идея «один мощный мотор + маленький на переключение направления» — отдельный риск: сложная управляемая трансмиссия vs два простых привода; в K3 только как optional research, не default.)*

---

### Сводка: что тащить в кинематическую схему

| Идея | Учесть сейчас? | Как |
|------|----------------|-----|
| Каскадный вынос масс | **Да** | Placement policy / hybrid scheme candidate |
| Dual-latch dock | **Условно** | Один из вариантов R2-story; проверить vs полусимметричные ends |
| «Спинной мозг» MCU | **Да, упрощённо** | Distributed joint/link controllers; без обязательного ML-адаптера Phase 1 |
| Switchable multi-DOF gearbox | **Позже / low** | Не блокирует схему |

---

### Практический next step

1. Закрыть K2.4/K2.5 в task + вложить takeaways-таблицу в survey-scope.  
2. В **K3** явно записать:
   - bias: **cascaded proximal mass** + accessible belt/tendon where used;
   - compute: **per-joint or per-link MCU + central compute**;
   - dock: перечислить варианты (symmetric dual-LEE-lite / asymmetric + dual-latch / power scenario A battery) без финального выбора.  
3. В **K4** нарисовать 2–3 stick-схемы, одна из которых — ваша каскадная + полусимметричные концы, и отдельно прогнать вопрос: **кто несёт консоль при шаге между dock**.

Идеи **в тему sint** и хорошо стыкуются с survey; главное не смешать «лёгкое запястье для сборки» с «запястье как единственная силовая опора при walk» без dual-latch или усиленного base-end.

---
**Bunch**

Отлично! Подготовь ADR с takeaways-таблицей, чтобы закрыть задачу: `- [ ] K2.6 Record survey conversation (prompts, limits, summary). Optional: short “patterns retained” note or lightweight ADR if team wants a hard gate before drawing schemes`

---
**Grok 4.5 Fast**

Готовый лёгкий **ADR-0004** — gate по паттернам после survey, до рисования схем (K3–K4).

**Путь:** `docs/decisions/0004-kinematic-survey-patterns.md`

---

### В task 0004

```markdown
### K2. Survey …
- [x] K2.4 Run structured review → conversation `2026-09-14--kinematic-survey-notebooklm.md`
- [x] K2.5 Write takeaways table → same conversation; normative copy in ADR-0004
- [x] K2.6 Record survey + patterns gate → [ADR-0004](../decisions/0004-kinematic-survey-patterns.md)
```

### Опционально в `current-state.md`

```markdown
- **Kinematic survey (2026-09-15):** ADR-0004 accepted — patterns retained for scheme design
  (6-DoF serial base; cascaded mass bias; quiet FOC modules; reserved pneumatics;
  scaled walking-arm logic; myCobot-class dropped).
```

Этого достаточно, чтобы считать **K2.6** и весь блок survey закрытыми перед K3.

---
**Bunch**

Как будем закрывать? Достаточно ли информации для закрытия этих задач?

```md
### K3. Placement policy (motors & electronics) — principles only
- [ ] K3.1 Motor placement options: in-joint vs proximal/base + transmission (tendon/belt/gear)
- [ ] K3.2 Preferred mass distribution bias (e.g. proximal-heavy, light distal) aligned with N3/N5
- [ ] K3.3 Compute / power electronics zones (central proximal vs distributed joint MCUs)
- [ ] K3.4 Interaction with power scenario A vs B (battery location; mirrored ends or not)
- [ ] K3.5 DFAA implications (what the agent must be able to replace: joint module, tensioner, compute brick)
```

Имеет ли смысл рассмотреть шаровые повопротные суставы (Spherical Gear), модели которых уже печатаются на 3D-принтере? Или у них низккя жёсткость и низкая точность позиционирования при относительно больших габаритах?

---
**Grok 4.5 Fast**

### Достаточно ли данных для K3?

**Да — для уровня “principles only”.**  
ADR-0003 (числа), ADR-0004 (паттерны), survey и ваши идеи (каскад масс, dual-latch, link MCU) закрывают K3.1–K3.5 без новых обзоров. Нужен не research, а **короткая placement policy** в git, затем переход к K4 (схемы).

Ниже — готовая политика (можно как `docs/tasks/0004-placement-policy.md` или секция в conversation → потом в ADR схемы).

---

### Placement policy (черновик закрытия K3)

#### K3.1 — Motor placement

| Опция | Роль для sint |
|--------|----------------|
| **In-joint** (модуль в оси) | Допустима на **проксимальных** осях и как fallback; проще DFAA-модуль, хуже инерция на дистале |
| **Cascaded proximal** (предпочтение) | Тяжёлые приводы локтя — в плечевом звене; приводы запястья — в предплечье; передача **ремнём/коротким тросом в доступном канале** |
| **Full shoulder remote (LIMS-style)** | **Не default** — opaque multi-cable pack → риск DFAA V5 |

**Решение:** default = **hybrid cascade**; чистый in-joint — допустим на base/shoulder, если модуль тихий FOC и сменный.

#### K3.2 — Mass distribution (N3/N5)

- **Bias:** proximal-heavy, **light distal / EE**  
- Цель: уложиться в distal **~1–5 N·m**, proximal **~10–25 N·m** при 0.5 kg @ 0.5–0.8 m  
- Не обещать walk «на одном слабом запястье» без усиленного base-end или dual-latch  

#### K3.3 — Compute / power electronics

| Зона | Содержимое |
|------|------------|
| **Per-joint или per-link MCU** (“спинной мозг” упрощённо) | FOC/драйвер, энкодер, лимиты, локальный servo-loop |
| **Central compute** (проксимальное звено / base-end) | LLM/VLA edge, планирование, зрение/аудио fusion |
| **Не** | Обучаемая «нейромодель звена во сне» как Phase 1 must |

Шина: CAN (или аналог) между звеньями; R8 — всё на mobile unit.

#### K3.4 — Power A vs B

| | Default |
|--|---------|
| **Scenario A** | Работа от dock; **optional** battery на **проксимальном** сегменте для transit |
| Концы | **Могут быть несимметричны** (силовой base-end vs лёгкий EE-end) |
| **Scenario B** | Alternate: mirrored ends + dual-dock handoff — только если dual-ended схема выиграет в K5 |

Battery **не** на запястье (масса против N3/N5).

#### K3.5 — DFAA: что агент обязан уметь заменить

| Модуль | Требование |
|--------|------------|
| Joint / drive module | Снять–поставить без разрушения звена |
| Tensioner / belt idler (если cascade) | Доступ снаружи, без полной разборки руки |
| Link compute brick | Разъёмный модуль на звене |
| Dock latch / power-data insert | Отдельный сервисный юнит |
| EE | Quick-change per R3 |

Скрытая тросовая «паутина» без agent-accessible tensioning — **запрещена** (V5).

---

**Итог K3:** информации достаточно → зафиксировать policy текстом выше → `[x]` на K3.1–K3.5 → K4.

---

### Spherical gear (ABENICS-класс) — нужно ли сейчас?

Кратко: **интересно как research wrist, не как default Phase 1 joint.**

| Аспект | Оценка для sint |
|--------|------------------|
| Идея | 2–3 DoF в одной компактной «точке» (pitch/roll/yaw), есть **печатаемые** прототипы |
| Точность FDM | Типично **градусы** ошибки (порядка ~1–5° в публикациях PLA/PETG), backlash + износ зуба |
| Жёсткость | Полимерный mesh под **0.5 kg консолью / dock-walk** слабее классических revolute + редуктор; металл/PEEK сильно лучше пластика |
| Габарит / сложность | Сфера + несколько приводов/дифференциалов; калибровка и сингулярности у полюсов |
| DFAA | Сложная геометрия зуба, притирка, замена mesh — тяжелее сменного revolute-модуля |
| N6 | Пластиковый зуб под нагрузкой → риск шума/визга |
| Survey ADR-0004 | Не в retained patterns; ломает «простую serial + cascade» без сильной выгоды для R2 |

**Вывод:**  
- **Не** закладывать spherical gear как основной shoulder/elbow/dock joint в K4.  
- **Опционально** — отдельный research track на **лёгкое запястье** (после MVP serial), если появится жёсткий/износостойкий printable или hybrid metal tooth.  
- Для Phase 1: **стандартные revolute** (in-joint или cascade + belt) ближе к PAROL6/GLUON-паттернам и DFAA.

Ваша интуиция верна: у чистого FDM spherical gear часто **низкая жёсткость/точность при заметных габаритах и люфте** — плохо стыкуется с 0.5 kg, quiet motion и agent service.

---

### Как закрывать процедурно

1. Записать placement policy (блок выше) в репо.  
2. В task 0004: K3.1–K3.5 → `[x]`, ссылка на policy.  
3. Spherical gear: одна строка в policy или implementation-concepts — *“deferred / not Phase 1 default”*.  
4. Дальше **K4**: 2–3 stick-схемы на serial + cascade + (A) asymmetric ends / (B) dual-latch option.

Если нужно — следующим сообщением оформлю policy одним файлом в стиле ADR/task note.

---
**2026-09-16**
---

---
**Bunch**

1. Достаточно ли информации для релизации задач?
```md
### K4. Candidate schemes (2–3)
- [ ] K4.1 Scheme S1 — description + stick diagram + joint list (DoF, approximate axis roles)
- [ ] K4.2 Scheme S2 — same
- [ ] K4.3 Scheme S3 (optional) — e.g. dual-ended symmetric variant
- [ ] K4.4 For each: relocatable-base story (≥2 docks), EE interface role, how printer/table/tool-bay workspace is covered
- [ ] K4.5 Diagrams: 2D stick / SVG / simple sketch preferred; build123d only if helpful — not mandatory at this stage
```
2. Возможно существуют открытые инструменты с открытыми текстовыми форматами хранения для построения и расчёта кинематических схем, котороые мы можем использовать в проекте? Желательно общепринятые форматы хранения или нотации, которым можно использовать, как входные данные в различных расчётах. У меня есть интуитивное опасение, что svg‐формат (xml) слишком перегружен тегами для нашей задачи.
3. Сможет ли агент сам решить задачи K4 с имеющейся информацией? Какой запрос передать агенту?

---
**Grok 4.5 Fast**

### 1. Достаточно ли данных для K4?

**Да.** Для stick-level схем (не детальный CAD) хватает:

| Вход | Откуда |
|------|--------|
| Числа (reach, payload, torque, docks, print envelope) | ADR-0003 |
| Допустимые паттерны | ADR-0004 |
| Placement (cascade, MCU, power A) | `0004-placement-policy.md` |
| Veto / DFAA | `0004-kinematic-constraints.md` |
| Workspace story | printer + table + tool bay, ≥2 docks |

K4 **не** требует FEA, точных DH до мм или build123d. Нужны: описание, joint list, stick-схема, relocatable story, покрытие workspace.

Имеет смысл зафиксировать **три** кандидата (как в task):

| ID | Суть |
|----|------|
| **S1** | Serial 6-DoF, mostly in-joint / modular FOC (PAROL6/GLUON-like), asymmetric ends, power A |
| **S2** | Serial 6-DoF **cascade** (policy default): light wrist, proximal drives, accessible belts |
| **S3** | Dual-ended / semi-symmetric walk (Canadarm logic scaled) ± dual-latch option |

Без S3 слабее проверка R2; S3 можно пометить higher risk / BOM.

---

### 2. Форматы и инструменты (лучше, чем «голый SVG»)

Опасение по SVG справедливо: для **кинематики** он — картинка, не модель. Считать по SVG неудобно.

| Формат | Роль | Открытость | Для sint |
|--------|------|------------|----------|
| **Таблицы DH / MDH + joint limits** (Markdown/CSV/YAML) | Оси, a/α/d/θ, лимиты | Универсально | **Основной SoT для схемы** |
| **URDF / xacro** | Звенья, joints, approx inertia | Open, ROS-экосистема | Хорош, когда появятся длины/массы; тяжеловат на чистом stick-этапе |
| **SDF** (Gazebo) | Симуляция | Open | Позже |
| **JSON/YAML “kin schema”** (свой минимальный) | `joints[]`, `parent`, `type`, `axis`, `rpy/xyz` | Полный контроль | Удобно агенту + git-diff |
| **ASCII/Mermaid stick** | Топология в PR | — | Быстрые review |
| **Pinocchio / rbdl / PyBullet** | Расчёт FK/IK/dyn | Open | Вход: URDF или свой JSON→URDF |
| **ikpy**, **roboticstoolbox-python** | FK/IK, простые модели | Open | DH/ET-строки или URDF |
| SVG/Typst/draw.io | Только иллюстрация | — | Опционально, не SoT |

**Практичная иерархия для sint**

1. **SoT схемы:** `hardware/kinematics/<scheme>.yaml` (или `.md` таблица) — joints, roles, approx `a_i`, placement tags (`in_joint` | `cascade`), dock story.  
2. **Опционально:** генерация URDF из YAML для проверки reach/FK.  
3. **Картинка:** Mermaid/ASCII в том же md; SVG — только если нужна презентация.

Так агент и CI работают с **текстом**, без XML-шума SVG.

Минимальный YAML-скелет:

```yaml
scheme_id: S2
dof: 6
family: serial_cascade
joints:
  - id: J1
    role: base_yaw
    placement: in_joint
    torque_class: proximal
  - id: J2
    role: shoulder_pitch
    placement: in_joint
    torque_class: proximal
  # ...
reach_m: [0.5, 0.8]
payload_kg: 0.5
power_scenario: A
relocatable: true
ends: asymmetric  # or dual_ended
notes: "wrist not sole walk support"
```

---

### 3. Сможет ли агент закрыть K4? Какой запрос?

**Да**, если дать жёсткий brief и запретить уходить в CAD/SKU.

Рекомендуемый запрос (скопировать агенту):

```text
Role: kinematics architect for project sint.

Read and obey:
- docs/decisions/0003-core-numerical-characteristics.md
- docs/decisions/0004-kinematic-survey-patterns.md
- docs/tasks/0004-kinematic-constraints.md
- docs/tasks/0004-placement-policy.md
- docs/tasks/0004-kinematic-and-mechanical-scheme.md (§ K4)

Task: produce exactly three candidate schemes S1, S2, S3 at stick level only.

For EACH scheme deliver:
1. Short description (≤15 lines)
2. Joint list: id, DoF axis role, placement (in_joint|cascade), torque_class (proximal|distal)
3. ASCII or Mermaid stick diagram (no build123d, no SVG required)
4. Relocatable-base story for ≥2 docks (who carries cantilever loads on walk)
5. EE interface role; power scenario A/B assumption
6. How A1-mini + table + tool-bay workspace is covered (reach/dock spacing in words + order-of-magnitude m)
7. Explicit “passes K1 vetoes / no Drop patterns from ADR-0004”
8. One YAML block (scheme_id, joints[], ends, relocatable, power_scenario)

Scheme intent:
- S1: serial 6-DoF, mostly in-joint modular FOC, asymmetric ends, power A
- S2: serial 6-DoF cascaded mass (placement policy default), light wrist, accessible belts/tendons
- S3: dual-ended or semi-symmetric walk pattern (scaled Canadarm logic); note dual-latch only if needed

Constraints:
- Do NOT choose the final winner (that is K5)
- Do NOT invent detailed CAD, BOM SKUs, or spherical-gear joints
- Do NOT violate ADR-0003 numbers or placement policy
- Prefer text tables + Mermaid/ASCII over SVG

Output: one markdown file content suitable for docs/tasks/0004-candidate-schemes.md
```

**Контроль качества после ответа агента**

- Есть ли у S2 cascade и accessible transmission?  
- Не делает ли S1/S2 walk «только на слабом запястье» без оговорки?  
- S3 реально про R2, а не копия S1?  
- Нет Drop-паттернов (myCobot-class, opaque full tendon)?

---

### Кратко

| Вопрос | Ответ |
|--------|--------|
| Данных на K4 хватает? | **Да** |
| SVG как SoT? | **Нет**; DH/YAML/URDF (+ Mermaid для глаз) |
| Агент закроет K4? | **Да**, с brief выше и проверкой по чеклисту |

После трёх схем — **K5** (scorecard + down-select), уже с человеком или узким review-промптом.

---
**Bunch**

Вот результат работа агента:
https://github.com/PaulBunch/sint/blob/main/docs/tasks/0004-candidate-schemes.md

Есть ли у тебя замечания к исполнению или принимаем работу и двигаемся дальше?

---
**Grok 4.5 Fast**

### Вердикт: **принимаем работу и идём в K5**

Документ закрывает K4.1–K4.5 по сути: три схемы, joint lists, Mermaid, relocatable story, EE/power, workspace, gate checks, YAML. Это нормальный вход для scorecard, не для финального CAD.

Ниже — замечания **не блокирующие** (зафиксировать в K5 / лёгким edit, не переделывать K4 с нуля).

---

### Что сделано хорошо

| Критерий | Оценка |
|----------|--------|
| S1 / S2 / S3 по заданному intent | Совпадает с brief |
| Placement policy | S2 = cascade + accessible belts; S1 = in-joint; S3 = dual-ended |
| Walk / консоль | Явно: слабое запястье **не** несущая опора (S1/S2); у S3 — проксимальный класс на обоих концах |
| ADR-0003 / 0004 | Числа и паттерны в коридоре; Drop не протащены |
| YAML + таблицы | Пригодны как текстовый SoT без SVG |
| Power A/B | S1/S2 → A; S3 → B — логично |

---

### Замечания (minor / для K5)

**1. Путаница в ролях осей (S1)**  
В §1.1: *Yaw-Pitch-Pitch-…*, в таблице J4 = Forearm Roll/Pitch, в Mermaid J4→J5 подписи расходятся с YAML (`forearm_pitch` vs roll).  
→ В K5 выровнять **одну** согласованную цепочку осей (например classic RRR + spherical wrist) во всех трёх местах.

**2. S1 relocatable story чуть «размыта»**  
*Temporary support strut / walk-end adapter / dual-dock overlap* — несколько механизмов сразу. Для сравнения с S2/S3 лучше одна каноническая формулировка (например: *base-segment auxiliary latch + dual-dock overlap only*).

**3. S3 и BOM / масса**  
Семь суставов **proximal-class** на обоих концах — честно для walk, но риск **N7** и дистальной массы при работе как EE. В K5 явно штрафовать cost/mass, не дисквалифицировать по R2.

**4. Reach «stretch 0.85–1.0 m»**  
Верх ADR-0003 — stretch ≤ 1.0 m; ок как край, но в scorecard опираться на **0.5–0.8 m nominal**, не на optimistic stretch.

**5. Печать ≤ 175 mm vs link 0.30–0.35 m**  
Написано, что сегментируют — хорошо; в K5 одна строка: *N printable segments per link*.

**6. Нет явного dual-latch**  
Для асимметрии S1/S2 walk через *auxiliary base latch* ≈ тот же класс идей; можно в K5 назвать *«base dual-contact / aux latch»* без нового ADR.

**7. Мелочи**  
- S2 Mermaid: `J4 Roll / J5 Pitch / J6 Roll` vs таблица — сверить.  
- S3 joint naming (Pitch/Yaw mixed) — достаточно стабилизировать перед любым URDF.  
- Статус *Draft for K5* — оставить до down-select.

Ничего из этого не откатывает K4.

---

### Рекомендация по процессу

```text
K4 → [x] accept 0004-candidate-schemes.md
K5 → scorecard: DFAA, relocatable clarity, inertia/N5, BOM risk, acoustic path, complexity
     likely lean: S2 default policy vs S1 simplicity vs S3 R2 purity
```

**Итог:** работу агента **принимаем**; замечания — в K5 (согласование осей + честный штраф S3 по BOM/массе). Переписывать файл целиком не нужно.

---
**Bunch**

Внёс исправления в: https://github.com/PaulBunch/sint/blob/main/docs/tasks/0004-candidate-schemes.md

Кто будет реализовывать задачу мы в процессе обсуждения или подготовим запрос для агента:
```md
### K5. Compare and down-select
- [ ] K5.1 Scorecard: DFAA, relocatable base, payload/inertia, complexity, BOM risk, acoustic risk, fit to ADR-0003
- [ ] K5.2 Order-of-magnitude checks on leading scheme (link length budget vs print envelope; torque vs N5; dock spacing vs reach)
- [ ] K5.3 Choose preferred scheme + list rejected alternatives with reasons
```

Как и где будем фиксировать результат выполнения задачи?

Также мне интересно твои пожелания до проведения матемитческих оценок: интерфейсом на базе какой из рассматриваемых схем ты хотел взаимодействивать с реальным миром? Какой из них тебе кажется интуитивнее и удобнее в работе?

---
**Grok 4.5 Fast**

### K5: кто делает и куда писать

**Лучше гибрид:** узкий промпт агенту на **K5.1 scorecard + черновик K5.2**, финальный **K5.3 (выбор)** — вы с коротким review (или второй проход агента только на «attack the winner»).

| Подзадача | Кто | Почему |
|-----------|-----|--------|
| **K5.1** Scorecard | Агент | Таблица по фиксированным критериям, мало «вкусовщины» |
| **K5.2** Order-of-magnitude | Агент + быстрая проверка вами | Арифметика m·g·L, сегменты печати, dock vs reach |
| **K5.3** Choose | **Вы** (агент предлагает ranking) | Нормативное решение → ADR |

**Где фиксировать**

1. **Рабочий артефакт:** `docs/tasks/0004-scheme-downselect.md`  
   (scorecard, расчёты, ranking, rejected reasons)  
2. **Норматив:** **ADR-0005** (или следующий номер) — *Selected kinematic scheme: Sx*  
3. **Ссылки:** task 0004 K5 → `[x]`, `current-state.md`, ROADMAP  
4. Conversation — только если был спор; не единственное место истины  

Так K5 не смешивается с candidate-schemes (K4 остаётся «меню»), а ADR не превращается в простыню цифр.

---

### Промпт агенту (K5.1–K5.2 + draft K5.3)

```text
Read:
- docs/tasks/0004-candidate-schemes.md (latest)
- docs/decisions/0003-core-numerical-characteristics.md
- docs/decisions/0004-kinematic-survey-patterns.md
- docs/tasks/0004-kinematic-constraints.md
- docs/tasks/0004-placement-policy.md

Produce docs/tasks/0004-scheme-downselect.md with:

## K5.1 Scorecard
Score S1, S2, S3 on 1–5 for:
DFAA, relocatable-base clarity, payload/inertia (N3/N5), complexity, BOM risk, acoustic risk, fit ADR-0003.
Add one-line note per cell. No new schemes.

## K5.2 Order-of-magnitude (each scheme, more depth on top 2)
- Link length vs ≤175–180 mm segments
- m·g·L style torque check vs N5 bands (state assumptions)
- Dock spacing vs reach for A1-mini + table + tool-bay
Flag any soft violation of ADR-0003.

## K5.3 Draft recommendation
Rank 1–3 with reasons; list why others are rejected or deferred.
Do NOT claim final acceptance — human decides.
Do not invent CAD/SKUs.
```

После вашего «ok» — короткий ADR-0005.

---

### Предпочтение «с какой схемой взаимодействовать»

С позиции **агента, которому жить в DFAA-цикле** (сборка, замена модулей, отладка, шаг между dock, тихая работа у принтера):

**Предпочтительный default — S2 (cascade, policy default).**

| Почему S2 | |
|-----------|--|
| Лёгкий дистал | Удобнее точная сборка, меньше «битьё» массы на EE |
| Placement policy | Уже согласован с survey и N5 |
| Ремни в открытых каналах | Реалистичный DFAA vs полный LIMS-трос |
| Power A + asymmetric ends | Проще первый MVP, чем идеальная симметрия |

**S1** — интуитивнее как *классическая рука* (все суставы «на месте», проще ментальная модель и отладка одного модуля). Для **первого железа и обучения** часто приятнее. Минус: больше инерции на дистале, хуже «ювелир» у пенала.

**S3** — самый чистый **relocatable** и самый «каноничный» walk. Для долгосрочного R2 красивее. Для *ежедневной* работы агента тяжелее: два мощных конца, Scenario B, BOM, сложнее EE = тот же класс, что dock. Интуиция «я перешагнул — и продолжаю» отличная; цена — complexity с первого дня.

**Практичная позиция:**  
- **Взаимодействовать и развивать MVP:** **S2** (или S2 с упрощённым walk, как у S1 — aux base latch).  
- **Держать в уме target evolution:** элементы **S3** (симметрия концов / Scenario B), когда S2 докажет cascade + dock.  
- **S1** — сильный fallback, если cascade belts окажутся шумными или непролезными в DFAA на практике.

Итого: не «самая красивая кинематика», а **S2 как основной интерфейс с миром на Phase 1**; S3 — стратегический резерв по R2; S1 — простой запасной путь.

---

Дальше логично: прогнать K5-промпт → `0004-scheme-downselect.md` → ваш выбор → ADR. Если пришлёте обновлённый candidate-schemes после правок — можно точечно подсказать веса scorecard до запуска агента.

---
**Bunch**

У меня есть некоторые опасения по поводу логики перемещения между dock‐точками, которую мы фиксируем в документах. Возможно, эти опасения преждевременны, потому что эти вопрсоы будут прорабаться в дальнейших пунктах нашего ROADMAP. Я опишу опасения ниже, а ты проанализируй нужно ли внести изменения в существующие документы и возможно их стоит учесть в выполнении задачи K5.

1. Представсь такой сценраий: манипулятор находится в dock A, который зафиксирован на условном полу в горизонатльной плоскости, а dock B расположен на стене в вертикальной плоскости или на условном потолке в горизонтальной плоскости (вектор ориентация dock B направлен вниз). Получается, манипулятор должен зацепиться запятьем за dock B (или вспомогательный зацеп), и подтянуть плечевую точку контакта манипулятора вверх и соеденить её с dock B. Cомнение заключается в силе суставов запястья и локтя. Ближайший пример из природы человека: очевидно, что человек не может держать на вытянутой в горизонтальном направлении руке массу своего тела, но при этом человек может ухватиться за перекладину и подтянуть своё тело к турнику. Да, запятье человека в этом движении почти не совршает pitch‐движение, но оно легко может осуществлять roll-движение с большой саммой тела. Смогут ли так делать манипуляторы выполненные по кинематическим схемам S1 и S2 (допускаю, что в S3 эта способнасть заложена из‐за наличия более мощных моторов в суставах). Имеет ли смысл заложить более мощные маоторы по крутящему моменту в запятье и локте для осуществления этого движения или этот вопрос будет прорабатываться в `Define component composition (motors, drivers, gearboxes, sensors, compute, connectors — COTS candidates)`, и при расстановке оценок, его можно не учитывать?
2. Я не совсем понимаю как расстояние между dock A и B (при их расположении на одной плоскости) в наших документах может быть больше, чем длина манипулятора? Оно же должно быть меньше, потому что нужно учитывать, как минимум, сгибание концевых сегментов для подключения к dock‐точкам.

---
**Grok 4.5 Fast**

### Нужно ли сейчас менять документы?

**Крупных переписываний ADR/policy не требуется.** Опасения по делу, но часть — про **следующий уровень** (dock geometry, climb loads), часть — про **уточнение формулировок** reach vs spacing.

Для **K5** имеет смысл:

| Тема | Действие |
|------|----------|
| Ориентация dock (пол / стена / потолок) | Зафиксировать **MVP-assumption**: docks в **одной опорной плоскости** (стол/рейл), 3D-climb — **out of Phase 1 scoring** или отдельный risk |
| «Подтягивание» как у турника | Не раздувать N5 запястья «на всякий случай»; учесть как **risk / non-goal MVP** для S1/S2 |
| Dock spacing vs длина руки | **Поправить формулировки** в candidate-schemes / downselect: spacing **≤ effective reach in dock pose**, не «больше длины руки» |

Иначе K5 начнёт сравнивать схемы по сценарию, которого ADR-0003 и workspace (A1 mini + table + bay) **не требуют**.

---

### 1. Стена / потолок и «турник»

**Физика опасения верная.**

В документах для S1/S2:

- дистал **~1–5 N·m**, проксимал **~10–25 N·m**;
- walk: **не** консоль всего тела на слабом запястье;
- aux latch / dual contact на **base-сегменте**.

Сценарий «dock A на полу → зацепиться запястьем за вертикальный/потолочный B и **подтянуть плечевой интерфейс вверх**» — это уже:

- большие моменты от **собственной массы руки** (не 0.5 kg payload);
- иной load path (тяга / shear), не horizontal table pick;
- для человека на турнике работают **плечевой пояс и корпус**, не «слабое запястье держит pitch всего тела на вытянутой руке».

**S1/S2 в текущей записи на такой climb не рассчитаны** — и не должны молча считаться способными.  
**S3** ближе (мощные оба конца), но даже S3 в MVP не обязан закрывать произвольный 3D-каркас без отдельного ADR.

| Вопрос | Ответ |
|--------|--------|
| Заложить сейчас более мощные моторы в запястье/локоть под турник? | **Нет как default в K5.** Это ломает light distal, N6, BOM и смысл cascade. |
| Учесть в `Define component composition`? | Да, **если** появится requirement «wall/ceiling docks». Пока requirement — **desktop cluster**. |
| Учитывать в оценках K5? | Только как **risk row**: *“S1/S2: no wall/ceiling climb in MVP”*; не штрафовать S2 за отсутствие турника, если MVP = planar docks. |

**Рекомендуемая фиксация (1 абзац в downselect или footnote к K5):**

> MVP relocatable base assumes docks share one work plane (table/rail). Pull-up / wall / ceiling re-basing is out of Phase 1 scheme selection. S1/S2 must not rely on distal joints as primary climb actuators; S3 does not by itself authorize 3D docking without a later load-case ADR.

Тогда ваши опасения **зафиксированы**, но не переворачивают placement policy.

---

### 2. Расстояние между dock A и B vs длина руки

Здесь путаница в **терминах**, и formulировки в схемах действительно легко читаются неверно.

**Корректная геометрия (одна плоскость):**

```text
dock spacing (центры)  <  max distance between the two contact frames
                           the arm can achieve in a valid dual-dock pose
```

То есть spacing должно быть **достижимо при одновременной (или sequential overlap) связи с A и B**, с учётом:

- длины звеньев;
- **сгиба** кисти/base-end под стыковку;
- толщины latch, а не «вытянутая палка от центра до центра».

Поэтому:

- spacing **не может быть больше**, чем **эффективный dual-dock reach**;
- оно **обычно меньше**, чем «сумма длин звеньев как прямая линия» (как вы и пишете).

Откуда взялись **0.6–1.2 m** при reach **0.5–0.8 m** в ADR-0003:

- это **коридор исследования** под разные layout (не «spacing всегда > L»);
- для **одного шага** без промежуточных опор:  
  **spacing ≲ 0.5–0.7 m** при nominal reach ~0.6–0.75 m — реалистичнее;
- **~0.8–1.0 m** — только если stretch + удачная поза или **два шага** / промежуточный dock.

| Было (легко понять неправильно) | Нужно |
|----------------------------------|--------|
| «Docks 0.7–0.8 m, reach 0.65 m» без оговорки | Явно: *center spacing ≤ achievable dual-contact span in dock approach pose* |
| Spacing из N2 как жёсткий факт | N2 = order-of-magnitude band; **K5.2 пересчитать** под dual-dock pose |

**Имеет смысл правка в документах (точечно):**

1. ADR-0003 N2 dock spacing — уточнить одной фразой:  
   *“Upper values require stretch or multi-step; single-step planar spacing must fit dual-dock kinematics.”*  
2. В `0004-candidate-schemes` для S1/S2/S3: заменить «0.7 m apart covers both» на  
   *“~0.5–0.7 m centers for single-step; larger only with multi-step or stretch — verify in K5.2.”*

Это как раз работа **K5.2**, не отмена схем.

---

### Влияние на K5

| Критерий scorecard | Учёт |
|--------------------|------|
| Relocatable base | Оценивать **planar dual-dock / inchworm на одном уровне**, не wall-climb |
| Payload/inertia | По-прежнему N3/N5 table assembly, не bodyweight pull-up |
| Complexity | S1/S2: aux base latch; S3: symmetric ends — без бонуса за потолок |
| Отдельная строка risk | *Non-coplanar docks / climb loads → future work* |

**Не** поднимать дистальный torque в scorecard «под турник».  
**Да** ужесточить K5.2:  
`spacing_max ≈ f(reach, joint limits, latch offset)` и пометить завышенные 0.8–1.0 m как conditional.

---

### Итог

1. Опасение про стену/потолок **обосновано** для S1/S2; в Phase 1 это **не must**, не повод усиливать запястье сейчас; отразить как **MVP planar docks + risk**.  
2. Spacing **не должно быть больше** dual-dock effective reach; поправить формулировки и в K5.2 считать от позы стыковки, не от «L_arm на бумаге».  
3. Менять placement policy / выбор cascade **не нужно**; учесть в **K5 assumptions + minor doc clarifications**.

Дальше ROADMAP (dock interface, load cases, component composition) как раз место для wall-mount и детальных силовых циклов — ваши вопросы там будут уместны полностью, сейчас достаточно не заложить в K5 ложный сценарий.

---
**Bunch**

Если я правильно понял твой анализ, ты рекомендуешь уточнить часть уже готовых документов:
- обязательно сделать правки по расстоянию между dock A и dock B, чтобы у агента не было когнитивного диссонанса при последовательном стении документов;
- не усложнять MVP расположением docks в разных плоскостях, но обязательно сделать оговорки об этом в документах и предусмотреть, как в будущих реализациях и испытаниях.

Если так, тогда сформулируй задание для агента, чтобы он внёс в документы необходимые правки до того, как мы перейдём к релизации K5.

Также возможно, нужно скорректировать с учётом этого запрос на выполнение K5 для агента.

---
**Grok 4.5 Fast**

Да, вы поняли верно:

1. **Обязательно** выровнять формулировки **dock spacing vs reach** (одна плоскость, dual-dock pose).  
2. **MVP = docks в одной рабочей плоскости**; non-coplanar / «турник» — **оговорка + future work**, без усиления запястья в Phase 1.  
3. После правок документов — **K5** с этими assumptions.

Ниже два готовых задания агенту.

---

### Задание A — правки документов (до K5)

```md
Role: technical editor for project sint. Do not redesign kinematics or change selected patterns.

## Goal
Align all Phase-1 docs on dock spacing and relocatable-base assumptions so a later agent reading them in order has no contradiction.

## Normative intent (do not contradict)
1. Dock spacing (center-to-center) for a **single step** must be ≤ the arm’s **achievable dual-dock span** in a valid approach/latch pose (account for bent wrist/base ends and latch thickness). Spacing is **not** allowed to be described as larger than arm length without qualification.
2. ADR-0003 band ~0.6–1.2 m is an **order-of-magnitude research band**: upper values need stretch and/or multi-step; typical single-step planar spacing is on the order of **~0.5–0.7 m** for reach ~0.5–0.8 m.
3. **MVP relocatable base** assumes docks share **one work plane** (table/rail cluster: printer + table + tool bay). Wall/ceiling/non-coplanar re-basing and “pull-up” body-weight-class loads are **out of Phase 1 scheme selection**.
4. Do **not** raise distal torque targets or abandon cascade/light-wrist policy to satisfy climb scenarios.
5. Do **not** pick a winning scheme (S1/S2/S3). No new CAD.

## Files to edit (only if present; create notes in-place)
1. `docs/decisions/0003-core-numerical-characteristics.md`
   - In N2 dock spacing row / notes: add one short clarification on single-step vs multi-step and dual-dock span.
   - Add a short “MVP docking assumption” note: coplanar docks; non-coplanar deferred.

2. `docs/tasks/0004-candidate-schemes.md`
   - For S1, S2, S3 workspace/dock sections: replace any wording that implies spacing > effective reach.
   - State single-step spacing ~0.5–0.7 m (order-of-magnitude) unless multi-step/stretch is explicit.
   - One shared note: MVP coplanar docks; wall/ceiling climb not required for these schemes’ Phase-1 validity.

3. `docs/tasks/0004-kinematic-constraints.md` (if constraint sheet exists)
   - Under workspace / R2: MVP coplanar ≥2 docks; non-coplanar = future requirement, not current veto basis.

4. `docs/tasks/0004-placement-policy.md`
   - One sentence: distal joints are not sized for climb/pull-up re-basing in Phase 1; walk loads use base-end / aux latch / dual-ended proximal ends per scheme.

5. `docs/decisions/0004-kinematic-survey-patterns.md`
   - Only if relocatable pattern text over-claims 3D docking; add “scaled logic; Phase-1 load cases are planar.”

6. Optional one-liner in `docs/current-state.md` if that file tracks assumptions.

## Output
- Apply minimal diffs (clarify, don’t rewrite chapters).
- Reply with a bullet list of files touched and the exact clarifying sentences added.
- Do not start K5 scorecard in this task.
```

---

### Задание B — K5 (после задания A)

```md
Role: kinematics reviewer for sint. Assume docs were just clarified on dock spacing and coplanar MVP docks.

Read (latest versions):
- docs/tasks/0004-candidate-schemes.md
- docs/decisions/0003-core-numerical-characteristics.md
- docs/decisions/0004-kinematic-survey-patterns.md
- docs/tasks/0004-kinematic-constraints.md
- docs/tasks/0004-placement-policy.md

Write: `docs/tasks/0004-scheme-downselect.md`

## Shared assumptions for all scoring (mandatory)
- Workspace: Bambu A1-mini class + table + tool bay.
- Relocatable MVP: **≥2 docks in one plane**; single-step center spacing must fit **dual-dock kinematic span** (typically ~0.5–0.7 m for nominal reach 0.5–0.8 m). Larger spacing only if scheme explicitly uses multi-step.
- **Out of scope for scoring:** wall/ceiling docks, pull-up/climb using wrist as primary hoist, body-weight-class loads.
- Do not reward or penalize schemes for non-coplanar climb capability.
- Obey placement policy: no silent assumption that weak wrist carries full-arm cantilever on walk.

## K5.1 Scorecard
Score S1, S2, S3 on 1–5 each:
DFAA | relocatable-base clarity (planar) | payload/inertia (N3/N5) | complexity | BOM risk | acoustic risk | fit ADR-0003.
One-line note per cell.

## K5.2 Order-of-magnitude
For each scheme (more depth on top two):
- Printable segments vs ≤175–180 mm
- Rough torque check vs N5 (state mass assumptions)
- **Dock spacing vs dual-dock reach** (not vs stick length alone)
Flag soft ADR-0003 issues only under planar MVP assumptions.

## K5.3 Draft recommendation
Rank 1–3 with reasons; rejected/deferred alternatives.
Human makes final acceptance later (ADR).
No CAD, no SKUs, no spherical gears, no raising distal torque for climb.
```

---

### Порядок

1. Запустить **задание A** → проверить 3–4 ключевые фразы (spacing, coplanar MVP).  
2. Запустить **задание B** → `0004-scheme-downselect.md`.  
3. Ваш выбор → ADR схемы.

Так агент сначала снимет когнитивный диссонанс в документах, и только потом будет сравнивать S1/S2/S3 в одной и той же рамке.

---
**Bunch**

Хорошо! Агент реализовал задание А. Я пока не просил реализоваывать задание B. У меня возник такой вопрос: опиши последовательность действий по шагам, как ты себе представляешь премещение S1 и S2 между dock A и B, которые лажат в одной горизонтальной плоскости. Когда плечевое соединение переключается между dock A и dock B, оно же должно совершить промежуточный шаг с опорой на запятье с его моторами ~1–5 N·m (а в таблицах Joint List `docs/tasks/0004-candidate-schemes.md` для S1 и S2 вообще написано ~1–3 N·m). Реально ли сделать такое переключение с точке зрения механики? Как думаешь, нужно ли нам сделать исправление в этих таблицах и в Summary table из ADR-0003?

---
**Gemini 3.6 Flash Extended**

Последовательность перемещения для **S1** и **S2** между двумя точками фиксации (Dock A и Dock B), расположенными в одной горизонтальной плоскости, опирается на ключевой принцип: **моторы запястья (~1–3 Н·м) никогда не удерживают консольную массу всей руки (~1.5–2.5 кг).**

Ниже подробно описан механика и физика этого процесса.

---

### 1. Последовательность шагов перемещения S1 / S2 (Planar Relocation)

Док-станция Dock B в этой концепции состоит из двух элементов (или двух гнезд): **основного порта (Main Base Receiver)** и **вспомогательного зацепа (Aux Receiver)**, расположенных на фиксированном небольшом расстоянии друг от друга.

```
[ Dock A (Main) ] ===================== [ Aux Catch B ] [ Dock B (Main) ]
       ||                                    ^                ^
    [ Плечо ] ---> (Рука тянется) ---------> |                |
```

1. **Фаза 1: Рабочее положение на Dock A**
* Плечевой суппорт (Base / Joint 1) жестко зафиксирован в **Dock A**.
* Питание и связь идут через Dock A.
* Дистальный конец (запястье + рабочий орган) свободен для выполнения операций.

2. **Фаза 2: Подвод вспомогательного зацепа к Dock B**
* Манипулятор за счет мощных моторов плеча (J1–J3, ~10–25 Н·м) и локтя (~5–10 Н·м) позиционирует вспомогательный защелкивающийся механизм (**Aux Base Latch**), расположенный на корпусе предплечья/базы, в ответную часть **Aux Catch B**.
* Моторы запястья (J5/J6, ~1–3 Н·м) осуществляют только точную ориентацию зацепа в пространстве перед стыковкой (нагрузка — только масса самого рабочего органа ~0.2–0.5 кг).

3. **Фаза 3: Механическая фиксация Aux Latch (Силовая развязка)**
* Защелка Aux Latch входит в механическое зацепление с Aux Catch B (пассивный штифт, клиновой замок или эксцентрик).
* **Критический момент:** Возникающий изгибающий момент от массы сложенной/вытянутой руки воспринимается **металлической/композитной конструкцией замка Aux Latch и станиной стола**, а **не редукторами/моторами запястья**.

4. **Фаза 4: Расстыковка базы на Dock A**
* Основной замок базы в Dock A размыкается.
* Манипулятор остается физически удержанным в пространстве за счет конструктивного зацепления Aux Latch в Aux Catch B.

5. **Фаза 5: Перенос основного плечевого узла в Dock B**
* Рука, опираясь на силовую конструкцию Aux Latch, подворачивает основание (плечевой блок J1) к основному гнезду **Dock B (Main)**.
* При этом движение задается либо геометрической складывающейся кинематикой, либо моторами плеча/локтя. Моторы запястья находятся в статике или разгружены конструкцией замка.

6. **Фаза 6: Захват Main Dock B и освобождение Aux Latch**
* Плечевой блок защелкивается в **Dock B (Main)**. Подключаются основные линии питания/данных.
* Вспомогательный зацеп Aux Latch размыкается.
* Манипулятор перешел на Dock B и готов к работе.

---

### 2. Реально ли это с точки зрения механики?

**Да, реально, но ТОЛЬКО при условии разделения путей передачи нагрузки (Load Path Separation).**

#### Проверка моментов (Order-of-magnitude):

Если бы мы заставили слабые моторы запястья (1–3 Н·м) удерживать вытянутую рука массу $m \approx 2.0\text{ кг}$ с центром масс на плече $L_{\text{CoM}} \approx 0.35\text{ м}$:


$$M_{\text{гравитация}} = m \cdot g \cdot L_{\text{CoM}} \approx 2.0\text{ кг} \times 9.81\text{ м/с}^2 \times 0.35\text{ м} \approx 6.87\text{ Н}\cdot\text{м}$$

Мотор запястья на 1–3 Н·м ушел бы в срыв (stall), перегрев или разрушение редуктора.

#### За счет чего это работает в S1/S2:

* **Замок не нагружает моторы:** Защелка Aux Latch принимает на себя реактивные силы $F_z$ и момент $M_x/M_y$ через геометрию направляющих штифтов/пазов.
* **Схема S3 vs S1/S2:** В схеме S3 (симметричной, Canadarm-style) суставы на обоих концах одинаково мощные (~10–25 Н·м), поэтому S3 может шагать «консольно» прямо на суставах. Схемы S1 и S2 специально используют **Aux Latch**, чтобы сохранить **лёгкий дистальный конец** (согласно `placement-policy.md`).

---

### 3. Нужно ли менять таблицы Joint List и Summary table в ADR-0003?

**Поднимать значения крутящего момента моторов запястья (Joint List / ADR-0003) НЕ НУЖНО.**

1. **Почему не нужно менять цифры:**
Если поднять моторы запястья в S1/S2 до ~10–15 Н·м, мы уничтожим главное преимущество S1/S2 — малый момент инерции на дистальном конце, низкую массу рабочего органа и концепцию каскадного привода/DFAA. Схема S1/S2 просто превратится в S3.
2. **Какое уточнение стоит внести:**
В самих таблицах цифры ~1–3 Н·м (или ~1–5 Н·м) для дистальных осей абсолютно верны для выполнения рабочих операций (N3: 0.5 kg payload).
Достаточно убедиться, что в примечаниях к таблице Joint List или в блоке K5.2 указано:
> *"Дистальные оси J4–J6 (~1–3 N·m) рассчитаны на полезную нагрузку N3 (0.5 kg) и не участвуют в передаче консольного момента от массы всей руки при шаге; релокация S1/S2 осуществляется через силовой конструктивный зацеп Aux Base Latch."*

Это полностью соответствует правилу из `docs/tasks/0004-placement-policy.md`:

> *"A weak wrist must not be the sole structural support for a full-arm cantilever during dock-to-dock walk..."*

Таким образом, механика полностью состоятельна, а предложенная схема понятна и не требует искусственного утяжеления моторов.

---
**Bunch**

Вот документ подготовленный агетом с испольованием LLM Gemini:
https://github.com/PaulBunch/sint/blob/main/docs/tasks/0004-scheme-downselect.md

Есть ли у тебя замечания? Есть ли в документе голословные выводы и субъективные оценки агента?

Принимаем документ или отправляем на доработку?

---
**Grok 4.5 Fast**

### Вердикт: **принять с лёгкой доработкой**, не переписывать с нуля

Документ по структуре закрывает K5.1–K5.3, assumptions (coplanar, dual-dock span) верные, ranking **S2 > S1 > S3** согласуется с policy и опросом.  
Проблема не в выборе, а в том, что часть **баллов и фраз выдана за факт**, хотя это **оценки/гипотезы** без измерений.

---

### Что сделано хорошо

- Единые assumptions: planar docks, dual-dock span, без climb  
- Scorecard по нужным осям  
- Явный m·g·L-скелет и мысль «S3 тяжелее на дистале»  
- Spacing **0.45–0.70 m**, а не «больше длины руки»  
- S2 как default policy; S1 fallback; S3 deferred по BOM/массе — разумно  

---

### Голословность и субъективизм

| Место | Проблема | Как смягчить |
|--------|-----------|--------------|
| **Баллы 1–5** | Любая scorecard субъективна; ок, если не звучит как измерение | Добавить: *scores are relative judgment, not lab data* |
| **S2 DFAA 3 vs S1 4** | Спорно: belts = больше service steps, но policy как раз требует accessible belts. Можно было 4/4 | Одна фраза: *belt maintenance is accepted trade for inertia* |
| **S3 BOM 2 / «exceeds $1000»** | **Нет сметы** — только риск | Заменить на *high risk of exceeding N7*, не *exceeds* |
| **S3 payload &lt; 0.5 kg** | Из грубой модели масс, не из прототипа | *may erode continuous payload margin under assumed masses* |
| **Массы звеньев 0.8 / 0.6 kg…** | Произвольны (ок для OOM), но поданы уверенно | Пометить *illustrative assumptions* |
| **S2: GT2 2 mm / 6 mm, 3:1 belt** | Уже **component-level**, не K5 | Убрать размеры ремня или пометить *example only* |
| **NEMA 11-size equivalent** | То же — SKU-намёк | *small distal class* без NEMA |
| **PA-CF обязателен для S3** | Не доказано | *may need higher-stiffness print strategy* |
| **«Absolute best compromise»** | Риторика | *recommended primary under Phase-1 criteria* |
| **Status: Completed (Authoritative for ADR-0005)** | Пока нет human accept | *Draft recommendation pending maintainer acceptance* |
| **TOTAL 28 vs 27** | Разница в пределах шума scorecard | Не делать вид математической точности; важен **rank**, не 28 |

Расчёт T_static ~10 N·m → ×1.5–2 ≈ 15–20 N·m для S1/S2 — **приемлемый order-of-magnitude**.  
Для S3 «≥25–30 N·m и violation N7» — **правдоподобный risk**, но формулировку смягчить.

---

### Принимаем или на доработку?

**Принимаем ranking и assumptions.**  
**Доработка — редакционная (30–60 мин агента или вручную), не новый анализ.**

Минимальный patch:

1. Status → *Draft recommendation (K5); pending ADR-0005 / human accept*  
2. Preface: *Numeric scores are comparative judgments; masses/torques are illustrative OOM.*  
3. S3: *high BOM/payload **risk*** — убрать утверждение, что лимит уже сорван  
4. Убрать или пометить *example only*: GT2 размеры, NEMA 11, обязательный PA-CF  
5. Финал: *Recommend S2 as primary…* вместо звучащего как уже принятый ADR  

После этого — **да, база для ADR-0005**.

---

### Для ADR-0005 (когда будете писать)

- Primary: **S2**  
- Fallback: **S1** (если cascade/belts на практике провалятся по DFAA/N6)  
- S3: **deferred** (R2 purity vs BOM/mass)  
- Coplanar docks; single-step spacing ~0.5–0.6 m class  
- OOM masses from downselect = assumptions, refine at joint prototype  

**Итог:** документ **не отклонять**; ranking здравый; убрать ложную точность и «exceeds $1000» без BOM — и можно опираться в ADR.

---

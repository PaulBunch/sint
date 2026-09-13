---
title: Core numerical characteristics
date_updated: 2026-09-13
date_updated: 2026-09-13
participants: [Bunch, Grok, Gemini]
status: closed
closed_reason: ADR-0003 proposed; task 0003 closed.
language: ru
tags: [numerical-targets, spec, payload, reach, power, torque]
related:
  - docs/tasks/0003-define-core-numerical-characteristics.md
  - docs/implementation-concepts.md
  - docs/decisions/0003-core-numerical-characteristics.md
---

# Core numerical characteristics

## Summary
Working targets for task 0003 finalized: payload 0.5 kg cont (~1 kg peak), reach 0.5–0.8 m, ≥2 docks, 24 V / 100–200 W, torque/speed bands, acoustic no-masking @ 0.5–1 m, BOM < $1000. ADR-0003 drafted.

## Discussion

---
**2026-09-13**
---

---
**Bunch**

В рамках проработки задачи `Define core numerical characteristics` необходимо учесть опыт сторонних проектов:

- Меня впечатлил низкий уровень шума, который производит роборука Robotic Arm from INNFOS GLUON, она имеет грузоподъёмность 500г и точноть позиционирования 2мм. Также мне напрвиться, что вся рука состоит из небольшого количества стандартных деталей и двигателей. https://www.kickstarter.com/projects/1383636492/the-smallest-servomotor-robotic-arm/posts
- Я восхищён кинематикой используемой в механизмах IRIM LAB KOREATECH, в частрности струнными тягами у LIMS2-AMBIDEX. Необходимо использовать решения из этого проекта для оптимального расположения моторов. Это позволяте избежать установки моторов непосредственно в места сочленения суставов, как в большинстве существующих проектов, а также порректно перераспредилить нагрузку по длине манипулятора, чтобы повысить грузоподъёмность манипулятора при той же мощности моторов.
- Возможно, в нашем проекте понадобятся 3D‐печатные актуаторы, как в проекте: https://www.youtube.com/watch?v=7SZQPEjpaMo&list=WL
  Автор называет свою разработку модульным 3D-печатным BLDC-сервоактуатором в рамках открытого проекта по созданию коллаборативного робота своими руками (DIY cobot).
  Ниже приведены их характеристики:
  • 5010 BLDC Motor
  • 4:1 Helical Planetary Gearbox
  • Modular Design
  • Supports 100:1 Total Gear Reduction
  • Fully 3D Printable
  • Open Hardware Design

Эти проекты и пожелания нужно зафиксировать в `docs/implementation-concepts.md`. Если ты с этим согласен, сделай это.

---
**Grok 4.5 Fast**

Согласен — эти референсы стоит зафиксировать в `implementation-concepts.md` как **ориентиры по шуму, размещению приводов и печатных актуаторам**, без превращения их в обязательные требования.

Ниже — готовый фрагмент для вставки/замены секции **1. Kinematics & Actuation** (остальные секции можно не трогать). При желании добавь в конец файла короткий блок **References**.


```markdown
## 1. Kinematics & Actuation
... Этот раздел добавлен в целвой файл ...
```

Опционально в конец файла:

```markdown
---

## References (design inspirations)
... Этот раздел добавлен в целвой файл ...
```

---

### Замечания по смыслу

| Референс | Что фиксируем | Чего не фиксируем |
|----------|----------------|-------------------|
| GLUON | Тихий модульный BLDC-arm, payload ~0.5 kg class, мало типов деталей | Конкретный вендор/SKU как обязательный |
| LIMS2-AMBIDEX | Вынос моторов, струнная/тендонная передача, перераспределение массы | Полное копирование их суставов |
| Printable 5010 actuator | Печатный модульный путь 4:1 → до ~100:1 | Готовность «как есть» без испытаний на шум/люфт |

Это хорошо стыкуется с задачей **core numerical characteristics**: GLUON задаёт порядок payload/reach/тишины; LIMS — рычаг по грузоподъёмности при той же мощности; printable actuators — путь внутри COTS + FDM.

Можешь вставить фрагмент как есть. Если нужно — следующим шагом свяжу эти пункты одной строкой с task `0003` (N3/N5/N6).

---
**Bunch**

В рамках решения задачи ROADMAP:
```
- [ ] Define core numerical characteristics (envelope dimensions, payload without EE, electrical power budget, joint torque/speed targets, acoustic noise limits, target BOM cost)
```

Подготовлен список подзадач в `docs/tasks/0003-define-core-numerical-characteristics.md`.

Давай начнём с задачи N1 с уточнения характеристик из `spec.md`:

| Тема | Уже в spec |
|------|------------|
| BOM | functional node **< ~$1000** |
| Fabrication | пользовательский FDM **~200×200×200 mm** |
| DoF | **≥ 6** |
| Noise | не портить звуковую диагностику |
| Power | пользовательские аккумуляторы / dock |
| Non-goal | промышленная тяжёлая нагрузка |

**Основные гипотезы:**
- Нагрузка EE: **0.5–2 kg** (типичные печатные модули, отвёртки, мелкий COTS, аккумуляторынй шуруповёрт), не 10 kg.
- Reach class: порядок **0.5–1.0 m** на одно «плечо»/базу — уточнять вместе с dock grid. Для MVP ограничением являются размеры печатного стола принтера Bambu Lab A1 mini.
- BOM: держать **<$1000** как жёсткую границу для MVP.
- Acoustics: пока **«ниже заметного маскирования speech/click на 0.5–1 m»** + позже dB(A) proxy.
- Torque/speed: после грубой оценки payload × reach × safety factor, с оглядкой на SimpleFOC + gimbal/drone BLDC из implementation-concepts.

В рамках проработки этой подзадачи необходимо учесть опыт сторонних проектов, в частности, которые уже отражены в `docs/implementation-concepts.md`.

**Ограничение:** 
Нельзя смешивать решение этой задачи с с полной кинематикой (следующий пункт ROADMAP).

---
**Gemini 3.6 Flash Extended**

Отличные материалы. Добавление референсов в `docs/implementation-concepts.md` (INNFOS GLUON, IRIM Lab / LIMS2-AMBIDEX, 3D-печатные BLDC актуаторы) даёт прочную технологическую рамку, а создание `tasks/0003-define-core-numerical-characteristics.md` аккуратно структурирует подзадачи N1–N8.

---

### 1. Продвижение задачи 0003: Анализ N1 и черновик целевых параметров (N2–N7)

На основе требований из `docs/spec.md`, добавленных референсов из `docs/implementation-concepts.md` и жестких технологических ограничений (FDM-печать на **Bambu Lab A1 mini** с рабочей областью **180×180×180 мм**) сформирована таблица рабочих численных гипотез.

#### Сводная таблица целевых характеристик (Working Targets)

| Параметр | Подзадача | Рабочий целевой диапазон / Гипотеза | Обоснование и ограничения |
| --- | --- | --- | --- |
| **Габариты детали (FDM)** | **N1 / N2** | Звено / корпусной элемент **≤ 175 мм** | Ограничение печатного стола Bambu Lab A1 mini (180×180×180 мм). Любая крупная деталь должна быть составной (DFAA). |
| **Вылет (Reach)** | **N2** | **450 – 600 мм** (на одно плечо/модуль) | Сложенное состояние: **≤ 180×180×280 мм**. Достаточно для обслуживания локальной ячейки и стыковки с док-сеткой. |
| **Полезная нагрузка (Payload w/o EE)** | **N3** | Номинальная: **0.5 kg**<br>Пиковая (при уменьшенном плече): **1.0 – 1.5 kg** | Достаточно для FDM-модулей, COTS-актуаторов, отверток, аккумуляторов. Не требует тяжелых промышленных волновых редукторов. |
| **Электропитание** | **N4** | Напряжение шины: **24V DC**<br>Непрерывная мощность: **50 – 100 W**<br>Пиковая мощность: **200 – 300 W** | 24V — стандарт для 3D-принтеров, COTS BLDC и 6S LiPo/USB-PD. Позволяет использовать тонкие и гибкие проводники. |
| **Крутящий момент (Joint Torque)** | **N5** | **J1–J2 (Плечо/База):** 8 – 12 Nm (пик 20 Nm)<br>**J3 (Локоть):** 4 – 6 Nm (пик 10 Nm)<br>**J4–J6 (Запястье):** 1.0 – 2.5 Nm (пик 4 Nm) | При выносе двигателей к базе (тендоны/ремни по типу LIMS2) плечо не несет массу двигателей J3–J6, что существенно снижает требования к моменту J1–J2. |
| **Скорость суставов (Joint Speed)** | **N5** | **J1–J3:** 30 – 60 RPM (0.5–1.0 rad/s)<br>**J4–J6:** 120 – 180 RPM (2.0–3.0 rad/s) | Безопасная скорость для коллаборативной DIY-сборки и точного позиционирования. |
| **Акустический шум (Acoustic Noise)** | **N6** | **< 45 dBA** на расстоянии 1 м (номинал)<br>Пиковый: **< 55 dBA** | Шим-частота FOC > 20–25 kHz (SimpleFOC), исключающая писк. Косозубые/волновые передаточные механизмы без сильного зубастого стука. |
| **Бюджет BOM (BOM Cost)** | **N7** | **< $1000 USD** на один базовый модуль (6 DoF)<br>Целевой ориентир серии: **$500 – $700** | Включает: печатный пластик, COTS BLDC двигатели, драйверы, магнитые энкодеры, подшипники, крепеж, контроллер MCU. |

---

### 2. Ключевые риски и допущения для проверки на прототипах

1. **Люфт (Backlash) печатных редукторов:** Планетарные 3D-печатные редукторы (4:1) дают заметный люфт. Для суставов J1–J3 может потребоваться безлюфтовая циклоидальная передача или ременной/струнный редуктор с натяжителем.
2. **Акустическая прозрачность редуктора:** В отличие от FOC-управления BLDC (которое бесшумно), пластиковые шестерни под нагрузкой могут генерировать высокочастотный шум. Потребуется смазка и косозубые профили (helical).
3. **Тендонная трансмиссия:** Использование тросов/ремней снижает инерцию, но добавляет сложную процедуру натяжения, регулярного обслуживания и калибровки растяжения (должно быть доступно агенту в рамках DFAA).

---
**Grok 4.5 Fast**

Ниже — проработка **N3 / N5 / N6** только на имеющихся данных (spec, implementation-concepts, референсы GLUON / LIMS / printable actuators). Это **working targets**, не финальный ADR.

---

### N3 — Payload without EE

**Рекомендуемый working target**

| | Значение | Смысл |
|---|----------|--------|
| **MVP target** | **0.5 kg** | Уверенный полезный груз на вытянутой руке (модуль joint, мелкий инструмент, крепёж) |
| **Stretch / peak** | **1.0 kg** | Кратковременно, ближе к корпусу или с хорошим распределением масс |
| **Не цель MVP** | ≥ 2–3 kg на полном reach | Уезжает в «полупром» и ломает BOM/тишину/COTS |

**Обоснование**
- Spec: non-goal = industrial heavy payload; DFAA = печатные модули, отвёртки, мелкий COTS.
- GLUON: rated **~500 g**, reach **~0.42 m** — близкий по классу тихий desktop-arm; independent reviews ~1–2 mm practical precision.
- Твой диапазон 0.5–2 kg разумен как **коридор исследования**, но для **заморозки MVP** лучше якорь **0.5 kg continuous @ near-full reach**, 1 kg — peak / shorter lever.
- Шуруповёрт / батарея на запястье: либо не в «payload without EE», либо отдельный сценарий с укороченным reach / поддержкой.

**Связь с печатью (Bambu A1 mini и т.п.)**  
Ограничение стола бьёт по **длине звеньев и числу печатных сегментов**, не напрямую по кг. Reach 0.5–1.0 m набирается стыковкой модулей; payload 0.5 kg как раз совместим с тонкими печатными линками, если моторы не висят все на дистале (урок LIMS).

---

### N5 — Joint torque & speed (order of magnitude)

Грубая оценка без полной кинематики (как ты и просил).

**Статика (порядок)**  
Момент у основания ≈ `m · g · L` (горизонтальный вынос):

| Payload | Reach | ≈ gravity torque at base |
|---------|-------|---------------------------|
| 0.5 kg | 0.5 m | ~2.5 N·m |
| 0.5 kg | 0.8 m | ~3.9 N·m |
| 1.0 kg | 0.5 m | ~4.9 N·m |
| 1.0 kg | 0.8 m | ~7.8 N·m |

Плюс масса самой руки, динамика, safety factor **×2–3** на проксимальные оси → **проксимальный joint continuous roughly 8–20 N·m** class для MVP 0.5 kg / ~0.6–0.8 m, если моторы в суставах.

**Если моторы у основания / тендоны (LIMS-bias)**  
Тот же payload при меньших дистальных инерциях; проксимальные приводы тянут больше «общей» нагрузки, но **суставы легче**, tip acceleration и безопасность контакта лучше. Числа N·m на **joint output** те же по физике рычага; меняется, *какой* мотор+редуктор где стоит.

**Скорость (рабочие полосы, не рекорд)**

| | Working band | Комментарий |
|---|--------------|-------------|
| Крупные оси (shoulder / elbow) | **~30–90 °/s** nominal | Сборка важнее гонок; GLUON-класс умеет быстрее, нам не обязательно |
| Дистальные (wrist) | **~60–180 °/s** | Быстрее допустимо при малой инерции |
| Tip speed | **≲ 0.5–1 m/s** в нормальном режиме | Выше — только если акустика и контроль позволяют |

**Привязка к COTS / printable stack**
- Gimbal/drone BLDC + SimpleFOC: тихий ток, ограниченный момент без большого reduction.
- Printable path (5010 + ~4:1 planetary → опционально cycloidal до ~100:1): как раз зона **единиц–десятков N·m** на выходе при приемлемых оборотах — совпадает с таблицей выше для 0.5 kg.
- Не закладывать industrial harmonic 30–100 N·м на каждый joint в MVP BOM.

**Working targets N5 (свести в таблицу task)**

| Axis class | Continuous torque (order) | Nominal speed |
|------------|---------------------------|---------------|
| Proximal (near base) | **10–25 N·m** | 30–90 °/s |
| Mid | **5–15 N·m** | 45–120 °/s |
| Distal / wrist | **1–5 N·m** | 60–180 °/s |

Уточнять после выбора: in-joint vs remote drive и реального reach.

---

### N6 — Acoustic limits

Spec даёт качественный критерий: *motion must not corrupt diagnostic audio*.

**Working acceptance (без лаборатории)**  
1. **Primary (MVP):** при типовом движении под нагрузкой ~0.5 kg на 0.5–1 m от микрофона на запястье/базе  
   - щелчки стыковки / речь / стук крепежа **различимы** (не маскируются моторным свистом и редуктором);  
   - нет доминирующего high-pitch gear whine.  
2. **Secondary (измеримый proxy позже):**  
   - цель-ориентир **≲ 45–50 dB(A) @ 1 m** в «тихом» режиме (очень грубо, desktop-cobot class);  
   - жёсткий dB(A) **не замораживать**, пока нет одной и той же методики (фон, нагрузка, поза).

**Почему так**
- GLUON ценится за *perceived* quietness при BLDC+integrated drive — качественный эталон «можно жить с audio».
- Printable planetary/cycloidal — главный **риск** по шуму; N6 должен отбраковывать редукторы, которые «съедают» микрофон.
- FOC, >~20 kHz PWM, механика без дребезга — уже в implementation-concepts; N6 = приёмка, а не ещё один лозунг.

**Не делать сейчас:** норматив «всегда < 35 dB(A)» без стенда — будет либо невыполним, либо фиктивен.

---

### Сводка working targets (для N8 / conversation)

| Parameter | MVP working target | Notes |
|-----------|-------------------|--------|
| Payload w/o EE | **0.5 kg** continuous @ design reach; **~1 kg** peak | GLUON-class; 2 kg = research ceiling, not MVP promise |
| Reach class | **0.5–0.8 m** MVP toward **≤1.0 m** | Limited by printable link length / dock grid, not by N3 alone |
| Proximal torque | **~10–25 N·m** continuous (order) | From m·g·L × SF; lower distal mass if LIMS-style |
| Distal torque | **~1–5 N·m** | |
| Joint speed | **~30–90 °/s** large axes; higher at wrist | Subordinate to quiet + precision |
| Acoustics | No masking of speech/click @ **0.5–1 m**; dB(A) proxy later | Quiet FOC + careful gearing |
| BOM | **< $1000** / functional node | Unchanged hard ceiling |

---

### Что сознательно не трогали
- Полная DH-кинематика, число звеньев, symmetric dual-ended layout.  
- Выбор «тендон vs in-joint» как ADR (только bias в implementation-concepts).  
- Точный SKU моторов и dB-стенд.

---

### Следующий шаг по task 0003
1. Вписать эту таблицу в conversation + task (N3/N5/N6 → done как *draft targets*).  
2. **N2** (envelope / dock spacing) и **N4** (power W / bus V) — следующий узкий проход.  
3. **N7** BOM — что входит в <$1000 (arm only vs arm+compute+one dock).  
4. Когда диапазоны стабилизируются — одна страница в `current-state` или лёгкий ADR «Working numerical targets (Phase 1)».

Если нужно, следующим сообщением могу так же сжать **N2 + N4** в том же формате.

---
**Bunch**

- Для МVP нам нужно как минимум две dock‐точки, чтобы проверить перемещение манипулятора между ними.
- Для оценки пространства для перемещения можно отталкиваться от следующих соображений. Манипулятор должен перемещаться вокруг 3D‐принтера Bambu Lab A1 mini, чтобы его обслуживать: менять филамент, запускать печать, снимать напечатанные изделия. Также должна быть предусмотрен доступ к свободной зоне стола и «пеналу» с инструментами и комплектующими, где манипулятор будет осуществлять сборку следующей версии.
- Что касается мощности и вольт‐амперных характеристик. Нужно отталкиваться от стандартных решений существующих на рунке. Я вижу два возможных сценария:
  1. В рабочем режиме манипулятор получает питание от док‐узла, но при этом оснащён сменным аккумулятором, в частности эта опция может быть полезна при перемещении между док‐узлами. Также этот сценарий позволят иметь не полностью зеркальные соединения на запястье и плече манипулятора. Например, силовое питание доступно только на одном из концов, а другой конец используется исключительно для энд‐эффекторов.
  2. У манипулятора отстутсвует автономное питание. Всё питание осуществляется от док-узлов по следующему сценарию: в момент перемещения между док-узлами манипулятор подулючён к двум узлам одновременно, автоматика переключает питание с одного узла на другой. Необходимы полностью зеркальные универсальные соединения на обоих концах манипулятора, которые подходят и для док-узлов и для энд-эффекторов.
- В идеальном сценраии хотелось бы, чтобы в $1000 входили: манипулятор, базовый энд-эффектор, электроника и питание, два док узла, видео и аудио пост. Возможно, это очень оптимистичный взгляд на мир, но такой набор должен обеспечить прямой перход к интеграционным тестам с LLM.

---
**Grok 4.5 Fast**

Ниже — фиксация **N2 / N4 / N7** с учётом твоих уточнений. Снова **working targets** для MVP, без ухода в полную кинематику.

---

### N2 — Envelope / workspace

**Сценарий пространства (MVP)**  
Манипулятор обслуживает:

1. **Bambu Lab A1 mini** — смена филамента, старт/контроль печати, съём деталей  
2. **Свободная зона стола** — буфер деталей  
3. **«Пенал»** инструментов и комплектующих — сборка следующего поколения  

Плюс обязательный сценарий **переезда между ≥ 2 dock-точками**.

**Рабочие геометрические гипотезы**

| Параметр | MVP working target | Комментарий |
|----------|-------------------|-------------|
| Число dock | **≥ 2** (лучше заложить 2 как минимум в BOM) | Без этого нет теста relocatable base |
| Reach одного «плеча» | **~0.5–0.8 m** (к **≤ 1.0 m** позже) | Согласуется с N3 (0.5 kg) и печатными звеньями |
| Dock spacing | **~0.6–1.2 m** между центрами dock | Чтобы «шаг» был возможен при reach 0.5–0.8 m с запасом на захват/стыковку |
| Рабочий объём | Зона вокруг A1 mini + table + tool bay в пределах 1–2 шагов по dock | Не «комната», а **один стол / один кластер** |
| Stowed / link size | Звенья и модули **вписываются в ~180–200 mm** печатный конверт (A1 mini class) | Стыковка модулей, не одна гигантская деталь |

**Смысл:** envelope задаётся **кластером принтер + стол + пенал + 2 dock**, а не абстрактным «1 m reach». Reach и dock grid подгоняются друг к другу так, чтобы один шаг базы покрывал переход «принтер ↔ пенал» или «принтер ↔ вторая станция».

---

### N4 — Power architecture

Два сценария, которые ты описал — это реальный архитектурный fork. Для численных характеристик MVP их нужно **не смешивать**, а выбрать **предпочтительный default** + допустимый fallback.

#### Сценарий A — Dock power + optional swappable battery  
- В работе: питание от dock  
- При переезде: краткий autonomy на сменной батарее  
- Допускает **несимметричные** концы: силовой feed только на «base»-конце, EE-конец легче (сигнал + низкий ток)

#### Сценарий B — Только dock, hot-swap через два подключений  
- Переезд: одновременно два dock, переключение питания  
- Нужны **полностью зеркальные** универсальные интерфейсы (dock = EE mechanical/power/data class)  
- Нет массы батареи на руке, зато жёстче механика/протокол стыковки

**Рекомендация для Phase 1 numbers (не финальный ADR):**  
считать **сценарий A default для MVP**, B — сильный кандидат, если DFAA dual-ended interface всё равно обязателен с первого дня.

Почему A для чисел:
- Проще доказать relocatable base без идеального dual-dock power handoff  
- Battery pack = явный элемент BOM и массы (влияет на payload budget)  
- Несимметрия концов упрощает первый EE interface  

B лучше стыкуется с «чистой» Canadarm-логикой; имеет смысл как **целевая** схема, если N7 и механика зеркальных разъёмов выдержат бюджет.

**Электрические working bands (рыночный desktop/cobot + maker)**

| Параметр | Working target | Ориентир |
|----------|----------------|----------|
| Bus voltage | **24 V** primary (допустимо 12–48 V research) | Типично для BLDC FOC / NUC-class / tool power |
| Continuous system power | **~100–200 W** | GLUON-class order (~120 W в публичных цифрах) + compute headroom |
| Peak (short) | **~300–500 W** | Разгон нескольких осей + compute burst |
| Dock current @ 24 V | **~10–20 A** continuous design margin | С запасом на peak и заряд батареи (если A) |
| Battery (если A) | **~24 V, 2–5 Ah** class, hot-swap | Хватает на переезд + короткий hold, не на час работы |

Точные А·ч и разъёмы — после выбора моторов; для N4 достаточно **24 V class + 100–200 W continuous**.

---

### N7 — BOM target (< $1000)

Твой «идеальный» набор для прямого LLM integration test:

- манипулятор (≥6 DoF)  
- базовый end-effector  
- электроника и питание  
- **два** dock  
- video + audio sense  

Это **правильная** цель по смыслу spec (closed-loop agent), но как **жёсткий <$1000 all-in** — оптимистично. Имеет смысл развести **ceiling** и **tiers**.

| Tier | Состав | Budget posture |
|------|--------|----------------|
| **T0 — Hard ceiling (spec)** | Один functional **node** (arm + onboard electronics + power path), без обязательства «весь стенд» | **< $1000** must hold |
| **T1 — Integration kit (желаемый MVP demo)** | T0 + 2× dock + 1 basic EE + cam + mic | **Цель ≤ $1000**, допустимо **≤ $1500** как explicit stretch с записью в risk |
| **T2 — Lab cluster** | T1 + tool bay fixtures, запасные актуаторы, принтер *не* в BOM робота | Отдельно; принтер — инфраструктура, не BOM sint |

**Что явно не класть в $1000 робота:** Bambu A1 mini, филамент, стол, освещение комнаты.

**Грубая раскладка T1 (ориентир, не смета)**

| Блок | Order-of-magnitude $ |
|------|----------------------|
| 6× joint actuators (printable/COTS BLDC+gear+enc+FOC) | 300–500 |
| Structure / links / fasteners (printed + COTS) | 50–100 |
| Compute (Pi-class / small SBC) + motor MCUs | 80–150 |
| Power (PSU/dock feed + optional battery) | 50–120 |
| 2× dock mechanical + power/data | 80–200 |
| Basic EE | 20–80 |
| Camera + mic | 20–60 |
| Cables, misc, margin | 50–100 |
| **Σ** | **часто 700–1300** |

Вывод для task:  
- **Spec hard rule:** functional node **< $1000**.  
- **MVP integration ambition:** 2 docks + EE + AV **стремиться вписать в $1000**, зафиксировать риск «может вылезти в $1.2–1.5k» и резать actuator cost / compute, а не выкидывать второй dock (он нужен для relocatable test).

---

### Обновлённая сводка (N2–N7 рядом с N3/N5/N6)

| ID | Parameter | MVP working target |
|----|-----------|-------------------|
| N2 | Workspace | A1 mini + table + tool bay; **≥ 2 docks**; reach **0.5–0.8 m**; dock spacing **~0.6–1.2 m** |
| N3 | Payload w/o EE | **0.5 kg** cont.; **~1 kg** peak |
| N4 | Power | **24 V** class; **100–200 W** cont.; peak higher; **default A** (dock + optional battery); B = alternate dual-dock feed |
| N5 | Torque / speed | Prox **~10–25 N·m**; distal **~1–5 N·m**; large axes **~30–90 °/s** |
| N6 | Acoustic | No masking speech/click @ 0.5–1 m; dB(A) later |
| N7 | BOM | Node **< $1000** hard; integration kit (2 dock + EE + AV) **target ≤ $1000**, stretch ≤ ~$1500 documented |

---

### Архитектурный флаг (не решать в числах, но не потерять)

| | Сценарий A | Сценарий B |
|---|------------|------------|
| Переезд | Батарея или краткий undock | Всегда power via docks, dual connect |
| Интерфейсы концов | Могут быть несимметричны | Зеркальные universal |
| DFAA / Canadarm purity | Слабее | Сильнее |
| MVP risk | Ниже | Выше (разъём + протокол handoff) |

Имеет смысл в conversation явно написать: *«Numerical targets assume power scenario A unless ADR chooses B.»*

---

### Для task 0003

Можно отмечать **N2, N4, N7** как draft-complete рядом с N3/N5/N6.  
Остаётся **N1** (сверка со spec — почти сделана), **N8** (одна summary-таблица + risks → current-state / лёгкий ADR).

Риски для N8:
1. T1 kit может не влезть в $1000 без упрощения актуаторов.  
2. Сценарий B vs A — влияет на массу, payload и интерфейсы.  
3. Dock spacing × reach × зона A1 mini нужно будет один раз прорисовать сверху (даже эскизом), до выбора кинематики.

Если нужно, следующим шагом соберу **готовый markdown-блок «Working numerical targets (Phase 1)»** для вставки в conversation или `current-state.md`.

---
**Bunch**

Отлично. Я обновил наше обсуждение в репо: https://github.com/PaulBunch/sint/blob/main/docs/conversations/2026-09-13--core-numerical-characteristics.md
Для закрытия задачи предлагаю на основе этого обсуждения сформировать ADR, а ссылку на это ADR уже добавить в current-state.md. В подготовке ADR необходимо учесть наши критерии:
```md
## Done when
- [ ] A single summary table of working targets exists (with units and short rationale)
- [ ] Open risks / “must revisit after first joint prototype” are listed
- [ ] ROADMAP item can be marked progress / done; numbers referenced from current-state
```

---
**Grok 4.5 Fast**

Готовый **ADR-0003**. Его достаточно, чтобы закрыть task 0003 по критериям Done when.

**Путь:** `docs/decisions/0003-core-numerical-characteristics.md`

---

### Фрагмент для `docs/current-state.md`

```markdown
- **Core numerical characteristics (2026-09-13):** ADR-0003 accepted.
  Working targets: payload 0.5 kg continuous (~1 kg peak); reach 0.5–0.8 m;
  ≥2 docks; 24 V / ~100–200 W continuous; proximal torque ~10–25 N·m;
  acoustic = no masking of speech/clicks at 0.5–1 m; node BOM < $1000
  (integration kit target ≤ $1000, stretch documented).
  Details: `docs/decisions/0003-core-numerical-characteristics.md`.
  Task: `docs/tasks/0003-define-core-numerical-characteristics.md` → closed.
```

---

### ROADMAP (одна строка)

```markdown
- [x] Define core numerical characteristics (…) → ADR-0003
```

---

### Task 0003 — Done when

| Критерий | Как закрывается |
|----------|-----------------|
| Summary table with units + rationale | Таблица в ADR-0003 |
| Open risks / revisit after prototype | Секция Risks в ADR |
| ROADMAP + current-state reference | Строки выше |

После коммита ADR + правок current-state/ROADMAP/task status — задачу **0003** можно закрывать и переходить к кинематике / scheme of the interface.

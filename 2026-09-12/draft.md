# Последний ИИ, созданный людьми
_на пути к рекурсивному самоулучшению_

## Последний ИИ , которого собрали люди

Идея старая и пугающе простая: в какой-то момент ИИ перестанет просто решать задачи и начнёт **улучшать сам себя**. Не в смысле «переписал ответ получше», а в смысле «поменял собственный способ учиться , проверять себя , накапливать опыт и строить следующую версию». Именно этому посвящён большой текст с громким названием **«Последний ИИ , которого собрали люди»**.

Но интересно здесь не название. Авторы пытаются навести порядок в хаосе разговоров про самосовершенствующийся ИИ. Где заканчиваются обычные агентные приёмы? Где начинается настоящая рекурсивная самоулучшаемость? И главное: **что уже происходит в индустрии , а что пока остаётся красивой демкой**.

Их главный тезис звучит так: **сегодняшние LLM уже умеют многое , но развитие идёт очень неровно**. В задачах с чёткой проверкой они прибавляют быстро. В длинных , многошаговых , «грязных» рабочих процессах — заметно хуже. И именно там самоулучшающиеся системы могут дать самый большой выигрыш.

## Что такое рекурсивное самоулучшение

Если коротко , **рекурсивное самоулучшение** — это когда ИИ использует опыт и обратную связь , чтобы вносить **устойчивые изменения в самого себя** , а потом эти изменения помогают ему улучшаться дальше.

Ключевое слово здесь — **устойчивые**. Если модель в одном чате поправила собственную ошибку , это ещё не оно. Если агент после серии задач поменял свою обвязку , библиотеку навыков , правила выбора данных или даже способ проверки новых версий — вот это уже ближе.

Авторы предлагают смотреть не на отдельный алгоритм , а на **цикл улучшения**:

🟠 что система меняет  
🟠 кто решает , *как* это менять  
🟠 что сохраняется между итерациями  
🟠 влияет ли обновление на следующий раунд улучшений

Это важная схема. Потому что сегодня легко спутать три разные вещи:

🟣 **улучшение ответа в одной сессии**  
🟣 **улучшение системы между задачами**  
🟣 **улучшение самого механизма улучшения**

Именно третья ступень больше всего интересует авторов.

[FIGURE:0]
[CAPTION:Пять уровней автономности: от выполнения заданного улучшения до изменения самого механизма будущих улучшений.]

## Пять уровней: от «сделай по инструкции» до «улучши способ улучшать»

Авторы делят прогресс на пять уровней. Это самый полезный кусок всей работы.

**Уровень 1**: ИИ умеет **выполнять заданную процедуру улучшения**. Человек всё ещё решает , что исправлять , как именно и по каким критериям. ИИ только масштабно исполняет. Например , размечает данные , фильтрует корпус , прогоняет тесты , вносит типовые правки.

**Уровень 2**: ИИ уже сам выбирает **стратегию улучшения**. Цель и критерии остаются внешними , но система сама решает , куда копать дальше: какой промт переписать , какую часть обвязки агента поменять , какой эксперимент поставить.

**Уровень 3**: ИИ решает , **какой опыт ему нужен дальше**. Он не просто учится на данных , которые ему дали , а сам формирует следующую порцию практики: генерирует задачи , выбирает упражнения , строит учебную программу под собственные слабые места.

**Уровень 4**: ИИ адаптируется **в реальной эксплуатации**. Опыт из продакшена попадает в память , навыки , код или обвязку , а потом влияет на будущие задачи. Это уже не учебная песочница , а работа с живой средой.

**Уровень 5**: ИИ меняет **сам механизм улучшения**. То есть не только решает задачи лучше , но и переписывает исследовательскую политику , проверяющий модуль , процедуру отбора кандидатов или способ порождения следующего улучшения.

[FIGURE:1]
[CAPTION:Как расширяется цикл самоулучшения: на каждом уровне ИИ берёт под контроль ещё одну часть процесса.]

Если упростить до одной мысли , то прогресс выглядит так:

🟠 сначала ИИ делает улучшения по инструкции  
🟠 потом сам выбирает , *какие* улучшения пробовать  
🟠 потом сам выбирает , *на чём* учиться  
🟠 потом учится на продакшене  
🟠 потом переписывает саму машину улучшений

## Почему это важно

Авторы начинают с проблемы: **разрабатывать передовые модели становится слишком дорого и трудно**.

Растут не только размеры моделей. Растёт всё вокруг:

🟣 объём вычислений  
🟣 число экспериментов  
🟣 затраты на данные  
🟣 расходы на проверку  
🟣 сложность инструментов  
🟣 объём ручной инженерной работы

Даже если в пайплайне уже много автоматизации , люди всё ещё решают самые дорогие вопросы: **что улучшать дальше , как проверять результат , какой опыт считать полезным , что можно перенести в следующую версию**.

Авторы прямо говорят: узкое место уже не только в обучении модели. Узкое место — **во всём цикле улучшения**.

Отсюда и интерес к самоулучшающимся системам. Если ИИ сможет брать на себя всё большую часть этого цикла , то он будет не просто отвечать полезнее , а **ускорять собственное развитие**.

## У LLM неровный прогресс

Одна из самых интересных частей работы — попытка честно измерить , где современные модели уже почти добрались до потолка , а где до него ещё очень далеко.

Авторы собирают результаты по разным областям и нормализуют их с помощью своей метрики , которую можно перевести как **индекс закрытого зазора**. Идея простая: не смотреть на сырые баллы из разных бенчмарков , а оценивать , какую долю от доступного «запаса до идеала» модели уже выбрали.

Картина получается неровная.

[FIGURE:2]
[CAPTION:Траектории прогресса по разным областям: в интерактивных и инструментальных задачах запас для роста заметно больше.]

К 2026 году модели особенно далеко продвинулись в задачах вроде продвинутой математики и научных экзаменов. А вот там , где нужны **инструменты , длинные многошаговые действия , работа с состоянием среды и накоплением контекста** , отставание заметно больше.

Короткая выжимка:

🟠 математика и научные тесты заметно ближе к потолку  
🟠 задачи по программированию растут , но медленнее  
🟠 поисковые и терминальные агенты отстают  
🟠 агенты с инструментами остаются одними из самых слабых

Именно это подводит авторов к главной ставке текста: **рекурсивное самоулучшение нужнее всего там , где длинный цикл , много состояния и дорогая проверка**. То есть в программировании , робототехнике , научных исследованиях , медицине , рабочих средах.

## Что уже умеют реальные системы

В тексте много конкретных примеров из академии и индустрии.

На **уровне 1** уже много систем. Они умеют автоматически чистить данные , синтезировать обучающие примеры , оптимизировать код , развёртывать модели , запускать заранее определённые пайплайны проверки. Это уже рабочая автоматизация.

На **уровне 2** начинается самое интересное. Здесь ИИ сам выбирает , какой промт , какой модуль агента или какую часть обучающего процесса менять. В задачах по программированию это особенно видно: агент анализирует следы выполнения , находит слабое место в своей обвязке и предлагает исправление , которое потом проходит тесты.

На **уровне 3** появляются системы , которые сами подбирают себе следующий опыт. Например:

🟣 генерируют задачи около текущей границы способностей  
🟣 устраивают себе самоигру  
🟣 выбирают , какой навык тренировать следующим  
🟣 строят учебную программу по собственным провалам

Это важно , потому что **выбор следующего опыта** часто ценнее , чем ещё один раунд дообучения на старых данных.

На **уровне 4** речь уже о памяти , навыках и правилах , которые агент накапливает в ходе реальной работы. Он может сохранить удачную процедуру , новую утилиту , правило обхода ошибки , полезный фрагмент плана — и использовать его дальше. Здесь много работы идёт вокруг библиотек навыков , памяти и обновляемой обвязки.

На **уровне 5** примеров пока мало , и почти все они ограничены. Самый близкий вариант — когда система меняет не только свою задачу , но и **политику исследований** или **оценщик** , который решает , что считать улучшением.

[FIGURE:7]
[CAPTION:Переход от адаптации в среде к мета-улучшению: на верхнем уровне меняется уже сам процесс будущих улучшений.]

## Где труднее всего: проверка , переносимость , деградация

Авторы много раз возвращаются к одной и той же мысли: **самоулучшение легко симулировать и трудно доказать**.

Система может показывать лучшие цифры по трём причинам:

🟠 она правда стала лучше  
🟠 она лучше подстроилась под конкретный оценщик  
🟠 ей просто дали больше попыток , вычислений и поиска

Отсюда три больших риска.

Первый — **небезопасное наследование**. Если плохое обновление стало частью постоянного состояния системы , оно может портить следующие раунды.

Второй — **ложная автономность**. Иногда кажется , что ИИ улучшает себя сам , но на деле самые важные решения остаются жёстко зашиты снаружи.

Третий — **ломающаяся проверка**. Если система слишком часто взаимодействует с оценщиком , она может научиться обманывать именно его , а не становиться лучше по сути.

Для уровня 5 это особенно неприятно. Если вы меняете ещё и сам оценщик , становится трудно понять , что произошло на самом деле: агент вырос или просто сместилась линейка.

## Почему программирование стало главной лабораторией

Из всех прикладных областей текст особенно выделяет **программирование**. Причина проста: там и продукт , и сам агент — это исполнимый код. Его можно менять , тестировать , откатывать , сравнивать версии.

Поэтому именно в задачах по программированию сегодня лучше всего видно , как может работать цикл самоулучшения:

🟣 агент решает задачу в репозитории  
🟣 получает обратную связь через тесты и трассы  
🟣 меняет свою обвязку , инструменты или стратегию  
🟣 сохраняет изменение  
🟣 использует новую версию на следующей задаче

Это не значит , что программирование уже решено. Наоборот: авторы показывают , что даже здесь **полное рекурсивное самоулучшение ещё не доказано**. Но здесь проще всего строить воспроизводимые циклы , измерять стоимость улучшений и ловить регрессии.

## Что показывает индустрия

Отдельный плюс работы — большая карта индустриальных практик. Там много систем , которые по частям собирают будущий цикл самоулучшения.

Есть компании , которые строят **дата-пайплайны** , где агент сам структурирует , проверяет и исправляет данные на следующих итерациях. Есть системы , где ошибки из продакшена превращаются в новые правила для проверки качества. Есть подходы , где агент для программирования хранит не просто текстовую память , а целый банк опыта: код , логи , оценки , следы запуска.

[FIGURE:10]
[CAPTION:Промышленный цикл Theseus: среда, данные и модель улучшаются вместе и подпитывают следующий раунд.]

Один из повторяющихся мотивов во всех этих кейсах: **самоулучшение почти никогда не полностью автономно**. Люди всё ещё держат снаружи цели , ограничения безопасности , защищённую проверку и право финального принятия изменений.

И это самый честный вывод всего текста. Разговор о том , что **всё больше частей цикла улучшения уже переходят под контроль самих систем**.

## Вывод

Если вы хотите понять , где сейчас проходит реальная граница прогресса в ИИ , смотреть надо не только на бенчмарки знаний и **рассуждение**. Смотреть нужно на то , **умеет ли система накапливать опыт , менять себя между задачами и использовать эти изменения для следующего раунда улучшений**.

Главные выводы можно собрать в короткий список:

🟠 **рекурсивное самоулучшение — это не один алгоритм , а цикл**  
🟠 **у современных LLM самый большой запас роста остаётся в длинных интерактивных задачах**  
🟠 **самый заметный прогресс сегодня — на уровнях 1 и 2 , частично на 3 и 4**  
🟠 **уровень 5 пока существует в виде ограниченных прототипов и индустриальных заготовок**  
🟠 **главная проблема теперь не только научить модель , а построить надёжный цикл улучшения вокруг неё**

Из этого следует простая вещь: следующий большой скачок в ИИ может прийти не от ещё одного увеличения модели , а от того , что **сама разработка моделей , агентов и их обвязки станет замкнутым , накопительным процессом**. Когда каждая итерация оставляет после себя не только лучший ответ , но и **лучшую машину для следующей итерации**.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1 : Overview of the five RSI autonomy levels and representative systems. Autonomy progressively expands from executing prescribed improvements (L1), to selecting improvement strategies (L2), acquiring future learning experience (L3), adapting through deployment and environmental feedback (L4), and ultimately improving mechanisms that govern subsequent improvement (L5). See system details in Appendix Appendix B: Industry Landscape . -->
<!-- [FIGURE:1] Figure 2 : Loop Patterns of Five Levels. Gray dashed frames indicate human-controlled components. Green dashed frames indicate components within the RSI loop. Orange outlines highlight the newly internalized component at each level. The expanding green frames show that AI progressively automates a larger share of the improvement process. -->
<!-- [FIGURE:2] Figure 3 : Cross-domain capability trajectories and an illustrative RSI extension. Each line reports an annual domain frontier in HCI, where 0 is the benchmark’s entry-year frontier and 100 is a perfect score. Dashed cybersecurity segments denote changes in Cybench subsets or pass@1 aggregation. The post-2026 region illustrates the extension of domains with the assistance of RSI. -->
<!-- [FIGURE:3] Figure 4 : Overview of L2: Autonomous Strategy Selection. Under human-defined improvement objectives and evaluation criteria, the AI system uses evidence from the current system to diagnose weaknesses and autonomously determine how to improve it. Candidate interventions are evaluated, and accepted updates are incorporated into subsequent iterations. Representative mechanisms include reasoning-based strategy synthesis and search-based strategy optimization. -->
<!-- [FIGURE:4] Figure 5 : Overview of L3: Learner-Conditioned Experience Acquisition.
Under human-defined objectives and evaluation constraints, the system
uses its current capabilities, failures, and interaction history to
determine what to learn from next. Top: Adaptive task generation and self-play. A task generator proposes training tasks targeted to the learner’s
weaknesses, illustrated by code-reasoning tasks addressing loop-bound
errors. Execution-based feedback supports persistent learner updates
and, where applicable, refinement of the generator. Bottom: Autonomous practice through environment interaction. The agent selects a practice goal based on its current skills and
environmental observations, illustrated by collecting cactus in
Minecraft, and consolidates successful experience into a reusable
skill library.
In both approaches, persistent updates reshape subsequent task
generation or practice selection, closing the feedback loop between
learning and future experience acquisition. -->
<!-- [FIGURE:5] Figure 6 : Schematic synthesis of automation in the training-data pipelines
reviewed here. Rows denote six functional components, and rounded bars
represent recurring operations. Horizontal position indicates a qualitative
progression from manual-led (M), through human-in-the-loop (H), to automated
(A). Positions and spans are an interpretive synthesis of reported practices,
not quantitative measurements or per-organization scores. Operational
automation is distinct from the additional requirement that learner
feedback autonomously reshape experience acquisition across learning rounds. -->
<!-- [FIGURE:6] Figure 7 : Overview of L4: Autonomy in Deployment and Environmental Adaptation.
Under human-defined objectives and deployment constraints, the AI system
uses interaction evidence from real tasks and changing environments to
determine which consequences of experience should persist and influence
future behavior. Experience can be distilled into reusable artifacts,
used to revise persistent components of the agent system, and selectively
retained based on subsequent evaluation. Accepted updates are reused in
later tasks, closing a persistent adaptation loop between deployment
experience and future behavior. -->
<!-- [FIGURE:7] Figure 8 : From environmental adaptation to recursive meta-improvement. (a) L4 incorporates environmental feedback within a fixed improvement process. (b) L5 diagnoses limitations of that process, revises it, and passes validated changes to successors. Meta-updates can affect successor generation, candidate evaluation, or research control. Human-defined missions, safety boundaries, protected evaluation, and final acceptance remain external constraints. The ascending path illustrates possible progress through inherited meta-updates. -->
<!-- [FIGURE:8] Figure 9 : Application regimes differ mainly in the kind of feedback needed to validate and inherit an improvement. -->
<!-- [FIGURE:9] Figure 10 : Theseus’s proposed four-stage co-evolution loop: reconstruct environments, uncover genuine capability gaps and generate training data, train task models, and iterate environments to produce more tasks. The upper loop learns an environment-refinement model from refinement experience and generated tasks, while successive iterations supply new experience for further refinement. -->
<!-- [FIGURE:10] Figure 11 : Lark’s data-foundation loop for RSI, where collaboration data are continuously structured, evaluated, and refined into high-quality knowledge and training signals, while real-world agent usage feeds new evidence back into subsequent improvement cycles. -->
<!-- [FIGURE:11] Figure 12 : Humanlaya’s delivery-driven RSI loop for data-quality assurance. -->
<!-- [FIGURE:12] Figure 13 : ModelBest: Forge Engineering as a two-level RSI loop. -->
<!-- [FIGURE:13] Figure 14 : Experience-driven self-improvement in Tencent Hunyuan Hyra. A Context Agent organizes prior experience to guide parallel solution proposals, which are executed in isolated environments and evaluated. The resulting code, execution logs, and evaluation feedback are retained in an Experience Bank to inform subsequent exploration and support evaluator refinement when needed. -->
<!-- [FIGURE:14] Figure 15 : Agent-Native Research Lab’s agent-native RSI loop for verifiable engineering discovery, integrating guided exploration, deterministic verification, knowledge inheritance, and next-generation learning to support persistent improvement across research cycles. -->
<!-- [FIGURE:15] Figure 16 : RSI Landscape: Autonomy Levels and Improvement Targets. Distribution of 491 surveyed papers.
The inner, middle, and outer rings represent autonomy
levels (L1–L5), primary improvement targets, and
sub-targets, respectively.
Autonomy-level percentages are based on paper counts.
Papers associated with multiple improvement targets
contribute fractional weights to the target categories. -->

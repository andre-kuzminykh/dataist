# Почему ИИ-агенту трудно действовать в реальном мире

## Робот, который понимает задачу, проверяет результат и умеет передумать

Роботу говорят: «Найди красную чашку и принеси её к столу». Он должен не просто распознать чашку и выполнить заученное движение. Нужно понять, чего хочет человек, найти предмет, выбрать способ его взять, заметить, получилось ли это, и изменить план, если чашка выскользнула или человек передумал.

Именно такой подход авторы статьи называют **агентной робототехникой**. Они предлагают строить роботов вокруг универсальной модели, которая планирует действия, вызывает нужные инструменты и проверяет результат. Это отличается от привычной схемы, где для каждого класса задач обучают отдельную политику — модель, напрямую связывающую наблюдения с командами.

Статья описывает направление исследований: как устроить такого робота, как проверять его способности и что ещё предстоит решить. **Модель может рассуждать о задаче, но для надёжной работы ей нужны обвязка, быстрые контроллеры и независимая проверка того, что произошло в мире.**

## От отдельных навыков — к управлению задачей

Модели, которые напрямую связывают изображение и инструкцию с движением робота, уже умеют выполнять широкий круг действий. Но они всё ещё часто зависят от конкретного устройства, среды и формулировки команды. Если сцена немного меняется, навык может перестать работать.

Авторы предлагают дополнить такие модели универсальным планировщиком. Он не обязан сам управлять каждым мотором. Его роль — определить цель, разбить её на шаги, выбрать подходящие навыки и инструменты, а затем проверить, что они дали нужный результат.

Для описания этой системы авторы используют три уровня:

🟠 **Система 2** понимает намерение человека, выбирает следующие шаги, вызывает инструменты и оценивает результат.

🟠 **Система 1** предоставляет навыки: например, распознавание объектов, захват, перемещение или прокладку маршрута.

🟠 **Система 0** управляет телом робота в реальном времени: поддерживает равновесие, исполняет движения и соблюдает ограничения оборудования.

Это разделение обязанностей, а не обязательное деление на три отдельные модели. Один компонент может выполнять несколько ролей. Система 2 может вызвать готовый навык, отправить цель прямо контроллеру или написать программу, которая объединит несколько действий.

[FIGURE:2]
[CAPTION:Три уровня робота: модель принимает решения, навыки выполняют порученные действия, а контроллер управляет телом.]

### Результат нужно проверять по фактам

Работа системы строится как повторяющийся цикл: понять задачу, решить, что делать, вызвать нужный инструмент, дождаться выполнения и проверить результат. После этого робот продолжает, меняет план, задаёт вопрос или сообщает о завершении.

Представим, что робот должен взять синюю чашку. Навык захвата сообщает об успехе, но камера показывает: чашка всё ещё стоит на полке. Команда могла быть выполнена правильно, а сам захват — не получиться. Надёжный робот не должен считать возвращённый статус доказательством успеха. Он должен заметить промах, осмотреть предмет с другого угла и попробовать иначе.

Похожий принцип нужен при отмене действия. Если человек говорит «не эту чашку», недостаточно отправить команду остановки. Система должна убедиться, что движение действительно прекратилось и робот находится в безопасном положении.

Поэтому **проверка результата — часть принятия решений**. Робот должен различать четыре вещи: приняли ли команду, завершилось ли действие, возник ли нужный физический эффект и достигнута ли цель человека.

## Почему физический мир сложнее цифрового

Компьютерный агент может проверить программу тестами, отменить изменение и начать заново. Робот часто не может. Он работает с частичными наблюдениями, а его действия могут быть необратимы. Уронить предмет, задеть человека или опрокинуть коробки — не то же самое, что отменить команду в редакторе кода.

Есть и проблема времени. Низкоуровневый контроллер может обновлять команды десятки или сотни раз в секунду. Система 2 на основе крупной модели может принимать решение несколько секунд или дольше. Пока она думает, предмет может сдвинуться, человек — войти в комнату, а робот — продолжить движение.

[FIGURE:7]
[CAPTION:Роботу нужно становиться умнее, не выходя за ограниченное время на принятие решения.]

Авторы называют желаемый режим **масштабированием в пределах срока**: улучшать качество решений при фиксированном времени, а не просто разрешать модели рассуждать дольше. Быстрые реакции следует оставить контроллерам и специальным навыкам. Система 2 должна подключаться там, где нужно выбрать цель, изменить план или справиться с неожиданностью.

Для этого нужна обвязка — программный слой вокруг модели. Она собирает наблюдения, хранит историю, предоставляет инструменты, следит за планом и проверяет результат. Например, она должна помнить, когда и с какой точки робот видел чашку: старая запись не гарантирует, что чашка всё ещё стоит там же.

## Как измерять возможности робота

Одна из центральных проблем сейчас — разные команды измеряют разные вещи. На одном и том же бенчмарке результат модели может сильно меняться в зависимости от доступных инструментов, промтов, числа попыток и правил проверки. Иногда среда останавливается, пока модель думает. Такой тест не показывает, как система поведёт себя, когда мир продолжает меняться.

Авторы предлагают оценивать робота на двух уровнях. Первый — сама модель: что она знает, как понимает сцену и какие решения предлагает. Второй — вся система: как модель работает с обвязкой, навыками и контроллерами в замкнутом цикле.

Оценка должна охватывать девять направлений, включая знания, понимание ситуации, рассуждение, работу с инструментами, память, перенос между разными роботами, безопасность, скорость и стоимость. Авторы советуют не сводить всё к одному числу. Высокий балл за выполнение задач не показывает, насколько робот надёжен, быстро ли реагирует и сколько помощи ему понадобилось.

[FIGURE:9]
[CAPTION:Девять направлений оценки — от знаний и планирования до безопасности, скорости и стоимости.]

Для честного сравнения нужно фиксировать, что именно видит робот, какими инструментами пользуется и сколько времени ему дают. Успех должен проверять независимый наблюдатель, а не сама модель. Испытания в режиме, где симулятор ждёт ответа, нужно отделять от испытаний на живых часах.

Разница может быть большой. На сложных маршрутах в одном исследовании безопасный успех упал с 19,8% в остановленной среде до 0,7%, когда среда продолжала работать. Число столкновений выросло в 12,3 раза. Это показывает, почему скорость — часть качества робота, а не просто техническая деталь.

Результаты уже обнадёживают на некоторых узких задачах: универсальные модели с обвязкой сравниваются с обученными политиками или превосходят их в отдельных симуляциях. Но в более широких условиях показатели гораздо ниже. В одном бенчмарке лучший результат составил 19%, в другом — 23,2%. Поиск предмета тоже не означает завершение задачи: робот может найти цель, но не суметь её взять или доставить.

## Четыре ступени ответственности

Вместо того чтобы измерять прогресс только числом задач, авторы предлагают смотреть на то, какую ответственность можно доверить роботу.

[FIGURE:12]
[CAPTION:Лестница ответственности: от отдельного движения к постоянной роли робота.]

Первая ступень — отдельный навык, например взять чашку. Вторая — целая задача: приготовить кофе и принести его человеку. Третья — рабочий процесс из связанных задач: подготовить завтрак для нескольких людей к нужному времени. Четвёртая — постоянная роль: каждый день заботиться о завтраке, учитывая расписание и предпочтения жильцов.

Сегодня роботы уже выполняют отдельные навыки и целые задачи в некоторых средах. Рабочие процессы пока показывают главным образом отдельные компании и исследовательские группы. Убедительных примеров, где робот долго выполняет постоянную роль без помощи человека, авторы не находят.

Дальше важны четыре направления: научить модели принимать решения в установленные сроки; поддерживать достоверную память о задачах и местах; переносить навыки на новые тела и среды; улучшать систему по результатам работы. Но последнее требует строгой проверки. Если робот меняет свои инструменты или навыки, нужно показать, что эти изменения помогают на новых задачах и не ухудшают уже освоенные.

## Вывод

**Агентная робототехника предлагает строить роботов, которые управляют задачей по кругу: планируют, действуют, проверяют и меняют решение.** Универсальная модель может связать понимание человеческой цели с набором уже доступных навыков. Но сама по себе она не решает проблем безопасности, задержек и неполных наблюдений.

Роботу важно не только правильно рассуждать, но и успеть принять решение, остановиться по команде и подтвердить, что действие действительно изменило мир так, как нужно. Поэтому прогресс зависит не от одной модели, а от всей системы: её обвязки, навыков, контроллеров, памяти и независимой оценки результатов. Именно эти части должны превратить удачные опыты в работу, которой можно доверить всё более широкую ответственность.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:2] (схема, нарисуем в стиле сайта) Figure 2: Two paradigms. (a) An action policy maps the task instruction and observation to action targets. It might include reasoning, subtask prediction, or in-context adaptation. (b) S2 combines a foundation model with an embodied harness. Together, they interpret intent, orchestrate skills and tools, verify outcomes, and adapt subsequent decisions. S1 provides callable skills and tools. S0 performs body control. The S1 path is illustrative; S2 may also call S0 or external tools. -->
<!-- [FIGURE:3] (схема, нарисуем в стиле сайта) Figure 3: A reference framework for agentic robotics. An Embodied S2 consists of a foundation model and an
embodied harness, whose five core parts manage context, tools, planning, memory, and
verification. S2 runs on demand or in response to events, whereas S1 and S0 execute at
their own rates. A real-time event monitor outside the three systems watches the user,
the robot body, and the physical world at a high rate. It interrupts S2 when an event may
change the task and, under predefined safety rules, triggers an immediate reaction in S0
without waiting for S2. S2 may call S0 directly through the tool interface;
S0 keeps its own real-time loop. -->
<!-- [FIGURE:4] (схема, нарисуем в стиле сайта) Figure 4: Three typical execution paths. One system may use all three paths within a single task. For simplicity, the robot body is omitted. (a) Layered orchestration: S2 invokes S1 skills and tools, which produce control targets that S0 executes. (b) Direct control: S2 controls S0 directly through an action interface; S0 still runs its own real-time control loop. (c) Code as policy: S2 writes code that a runtime interpreter executes in the role of S1. -->
<!-- [FIGURE:5] (схема, нарисуем в стиле сайта) Figure 5: The agentic loop. Top: one cycle comprises six steps.
S2 interprets intent, reasons about goals and constraints to decide how to proceed, and invokes an S1 skill, an S0 interface, or an external tool as needed.
The invoked capability executes under its contract.
S2 then observes and verifies the outcome by answering four questions (whether the request was accepted, whether execution terminated, whether the physical effect holds, and whether the user’s intent is satisfied).
Based on the verification, it continues, recovers, asks, or reports.
The real-time event monitor, which watches the user, the body, and the scene, can interrupt S2 at any point.
Bottom: the same steps on a schematic time axis, labeled with their step numbers and colors.
S2 deliberates on demand, S1 runs while a tool executes, and S0 runs continuously;
after an interruption, S2 cancels the running tool call and replans while S0 keeps the body stable; the hatched segment marks the canceled execution. -->
<!-- [FIGURE:7] (схема, нарисуем в стиле сайта) Figure 7: Capped scaling. Frontier models scale monotonically: greater capability comes with longer latency. Embodied S2 must instead become more capable within a fixed decision deadline. A decision that arrives after the deadline is usually too late, even if it is correct: the situation has already changed, so acting on it could fail the task or create a hazard.
Note that the curves are schematic: they illustrate the qualitative relationship, not measured data. -->
<!-- [FIGURE:8] (схема, нарисуем в стиле сайта) Figure 8: How long each layer takes per decision or control update. All values are given as times, with the equivalent rate in parentheses (time = 1 / rate =1/\text{rate} ).
The S0 and S1 bands are indicative ranges.
The S1 band covers control skills only, since the perception and planning modules of S1 are invoked on demand and have no fixed rate.
S2 is event-driven rather than periodic, so we plot time per decision; the S2 band is a target for dynamic manipulation, not a requirement for every task.
Helix’s “System 2” is a vendor label: its output is a latent representation, so our criterion does not classify it as S2 (Section 3.1 ); we include it as the fastest upper-level module plotted.
The Astra measurements come from different tasks and settings and are not directly comparable with one another. -->
<!-- [FIGURE:9] (схема, нарисуем в стиле сайта) Figure 9: The S2 evaluation recipe at a glance: the 9 dimensions (inner ring) and their
53 sub-dimensions (outer ring). Darker cells mark the 29 embodiment-related sub-dimensions:
those specific to embodiment or strongly dependent on it; standard evaluations of general language
models rarely cover these sub-dimensions. -->
<!-- [FIGURE:10] Figure 10: The four enabling conditions of digital agents, and how far each domain satisfies them. The domains illustrate how the conditions vary across task settings rather than forming a strict progression of capability or difficulty. -->
<!-- [FIGURE:11] Figure 11: What physical agents must rebuild. Foundations replace the four enabling conditions of Figure 10 ; runtime constraints, which follow from time, irreversibility, and a changing body, govern how the system operates; and evaluation in the running world validates its claims. -->
<!-- [FIGURE:12] (схема, нарисуем в стиле сайта) Figure 12: Ladder of delegable work. Progress is measured by the responsibility that a robot can be
trusted to carry alone. Each of the four levels includes those below it; typical durations are illustrative. -->
<!-- [FIGURE:13] Figure 13: Spatial scope of delegated work, from a workcell within the robot’s reach to a site with several buildings and outdoor routes. The illustration is conceptual. -->

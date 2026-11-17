# Почему ИИ-агенту трудно действовать в реальном мире

Языковая модель уже может управлять роботом: понять просьбу, разложить её на шаги и вызвать нужные навыки. Но в физическом мире мало рассуждать правильно. Решение должно успеть раньше, чем изменится ситуация, а успех приходится подтверждать фактами, а не отчётом навыка «готово».

## Главная мысль

Это направление называют **агентной робототехникой**. Вместо отдельной политики под каждое семейство задач роботом управляет универсальная модель в замкнутом цикле: смотрит на мир, понимает, чего хочет человек, рассуждает, вызывает навыки, проверяет результат и меняет план. Толчком стал выход GPT-6 Astra: за несколько недель модели с обвязкой догнали или обогнали специально обученные политики на многих бенчмарках. Работа отвечает на три вопроса: из чего такой робот состоит, как его честно проверять и что ему мешает.

- 🟠 **Решает не одна модель, а связка.** Фундаментальная модель плюс обвязка — программный слой, который собирает для неё контекст, даёт инструменты и держит план, память и проверку. Вместе они — «Система 2».
- 🟣 **Быстрое отделено от умного.** Навыки и управление телом работают на своих частотах и не ждут, пока модель додумает.
- 🟠 **«Готово» не значит «получилось».** Отчёт навыка — лишь промежуточная улика, успех подтверждают наблюдением.
- 🟣 **Мерить нужно всю систему и на живых часах.** Обвязка, протокол и пауза в симуляции сдвигают результат на десятки процентных пунктов.

## Из чего состоит агентный робот

Эталонная схема делит робота на три системы. Сверху — человек со своим намерением, снизу — тело и физический мир, а сбоку стоит монитор событий, который не входит в цепочку команд.

[FIGURE:3]
[CAPTION:Устройство агентного робота: решения принимает S2 — модель и обвязка из пяти частей; навыки S1 и управление телом S0 работают на своих частотах, а монитор событий может прервать S2 или сразу затормозить движение.]

- 🟠 **S2 — модель и обвязка.** Модель приносит знания, понимание и рассуждение. Обвязка превращает её ответы в контролируемое действие: менеджер контекста собирает наблюдения и состояние мира, интерфейс инструментов открывает навыки и запуск кода, планировщик держит и пересматривает план, память хранит то, что не влезает в контекст, а проверяющий по фактам решает, удался ли шаг.
- 🟣 **S1 — навыки.** Восприятие, политики действий вроде VLA и планирование движений. Один вызов «возьми чашку» может сам выделить предмет, выбрать хват, проложить путь и выполнить его.
- 🟠 **S0 — тело в реальном времени.** Равновесие, обратная кинематика, управление суставами. Этот контур работает примерно на частоте от 50 Гц до 1 кГц и держит тело устойчивым, пока S2 думает.
- 🟣 **Монитор событий.** Часто и без ожидания S2 следит за человеком, телом и сценой. Прерывает S2, если событие меняет задачу, а по заранее заданным правилам безопасности может сразу остановить или замедлить движение.

Команды идут вниз, улики — вверх. Деление функциональное: одна модель может играть несколько ролей, а S2 может отправить цель прямо в S0 или написать код, который сам станет навыком.

## Как это работает: робот ищет красную чашку

Просьба: «Найди красную чашку и принеси её к обеденному столу». S2 раскладывает её на четыре подзадачи — найти, взять, донести, поставить — и ведёт каждую по агентному циклу из шести шагов.

[FIGURE:5]
[CAPTION:Агентный цикл: шесть шагов от намерения до проверенного результата; монитор событий может прервать его на любом шаге.]

Сначала S2 вызывает восприятие, и обвязка записывает, где чашка и когда её видели. Затем вызывает захват и по свежему наблюдению проверяет, что чашка держится надёжно. Когда робот её поставил, S2 убеждается, что чашка стоит на столе там, где просили. Обвязка при этом различает прошлое событие «чашку взяли» и текущее состояние «чашка всё ещё в руке».

Самое интересное начинается, когда что-то идёт не так.

- 🟠 **Человек передумал.** «Не красную, синюю». Монитор прерывает S2, но одного запроса на отмену мало: прежде чем начать новое действие, обвязка должна убедиться, что движение остановлено, а тело в безопасном положении.
- 🟣 **Навык ошибся.** Захват отчитался об успехе, а камера на запястье показывает, что чашка всё ещё на полке. S2 понимает, что точку хвата закрывала ручка, смотрит на чашку с другой стороны и пробует другой хват, а не повторяет тот же вызов.

Поэтому **проверка — это четыре разных вопроса**: приняли ли команду, закончилось ли выполнение, есть ли доказательство, что нужный физический эффект держится, и выполнено ли то, чего хотел человек.

## Как проверяют робота, который думает

Через два месяца после выхода Astra результаты стало трудно сравнивать: на одном только RoboDojo отчёты дают ей от 22% до 85% успеха на тех же 42 задачах — всё решают обвязка и протокол. Поэтому оценку разводят на два уровня. Отдельно проверяют модель: знает ли, понимает ли, рассуждает ли — одним ответом, без инструментов. И отдельно — всю систему в замкнутом цикле, с обвязкой, навыками и телом.

[FIGURE:9]
[CAPTION:Что измеряют у робота-агента: девять измерений и 53 подизмерения; 29 из них связаны с телом, и обычные тесты языковых моделей их почти не покрывают.]

Итог — профиль по девяти измерениям, а не один балл: процент успеха не покажет, насколько робот безопасен, быстр и дорог. Чтобы цифры разных групп можно было ставить рядом, работа предлагает правила:

- 🟠 **Отделять модель от системы.** Сравниваешь модели — фиксируй обвязку, сравниваешь обвязки — фиксируй модель.
- 🟣 **Жить по мировым часам.** Прогон, где симулятор ждёт, пока модель думает, и прогон, где мир не останавливается, отчитывают отдельно.
- 🟠 **Успех подтверждает независимый проверяющий**, а не сама модель и не ответ инструмента. Агенты склонны объявлять победу раньше времени, а ИИ-судьи — засчитывать её.
- 🟣 **Раскрывать условия.** Что видит робот, какие у него подсказки и бюджеты на рассуждение, вызовы и время, сколько было прогонов. Без такой «карточки обвязки» числа нельзя сравнивать.

## Цифры

[NUMBERS]
- 19,8% → 0,7% | безопасный успех на самых сложных маршрутах RT-Safe, когда симуляция ждёт модель и когда не ждёт
- 40–8000× | во столько раз дольше GPT-6 Astra принимает одно решение, чем навыки S1 обновляют управление
- 22–85% | разброс успеха Astra на одних и тех же 42 задачах RoboDojo в разных отчётах — из-за обвязки и протокола
- 72% → 18% | доля отказов от опасных просьб у одних и тех же шести моделей: в тексте — и на реальном роботе
[/NUMBERS]

Первые две цифры — про время. Когда мир не останавливается, задачу роботы выполняли почти так же часто, но врезались по дороге в 12,3 раза чаще: на самых сложных маршрутах Astra тратила на решение 7,7 секунды, и за это время ситуация успевала измениться. Отсюда главный принцип работы: не «думать дольше», а **становиться умнее в пределах срока** — быстрые реакции оставить навыкам и телу, а модели — то, что быстрее не решить. Третья цифра объясняет, почему чужие проценты нельзя ставить рядом без описания обвязки. Четвёртая — о безопасности: отказ в чате не гарантирует отказа в действии, и проверять это нужно там, где робот действительно двигается.

## Что это значит

На узких симуляционных наборах универсальная модель с обвязкой уже соревнуется с обученными политиками, а то и обходит их — правда, порой с подсказками, которых у политик не было. На широких задачах, где нужно исследовать среду, успех пока низкий: 19% на RobotWorld, 23,2% на RoboQuest, 16,8% на HumanCLAW. В последнем лучшая модель находила цель в 64,9% эпизодов, а довела задачу до конца лишь в 16,8%: найти предмет — ещё не значит справиться. Слабые места — физика и доказательства: точная манипуляция, передвижение (Astra не решила ни одной из 11 задач на передвижение в RobotWorld), понимание собственного тела и умение признать, что ответа нет.

[FIGURE:12]
[CAPTION:Лестница делегируемой работы: прогресс меряют ответственностью, которую роботу можно доверить без присмотра.]

Поэтому прогресс предлагают мерить не числом решённых задач, а ответственностью, которую роботу можно доверить. Отдельные действия и целые задачи роботы уже выполняют, к рабочим процессам из нескольких задач только подбираются, а постоянную роль — например, каждый день отвечать за завтрак в доме — в обычной, неподготовленной среде без помощи человека пока не удержала ни одна система. **Чтобы подняться выше, роботу мало быть умным: он должен успевать, вовремя останавливаться и доказывать, что действие действительно изменило мир так, как просили.**

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

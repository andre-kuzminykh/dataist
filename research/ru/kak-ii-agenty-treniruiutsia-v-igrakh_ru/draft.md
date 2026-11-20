# Как ИИ-агенты тренируются в играх

Игровые миры можно превратить в проверяемые учебные задачи, а прохождение этих задач — в данные для обучения зрительных ИИ-агентов. В Game2Player игры проверяют сами игроки: их ошибки помогают исправлять среду, а каждое действие связывается с измеримым прогрессом. Обученная на таких данных модель чаще продвигается к цели даже в незнакомых играх.

## Главная мысль

Чтобы учить ИИ играть, нужны не просто видео, а записи с понятной целью, действиями и достоверной оценкой результата. Game2Player автоматически готовит такие данные из веб-игр и использует прогресс в игре, чтобы выделять полезные действия.

🟠 Сборщик адаптирует игру и задаёт задачи, чей прогресс и успех измеряются по внутреннему состоянию игры.  
🟠 Два игрока тестируют среду разными способами и сообщают о проблемах.  
🟠 Исправленные игры дают траектории — последовательности экранов, действий и оценок прогресса.  
🟠 Обучение сильнее учитывает действия, после которых игрок продвинулся к цели.

## Что такое Game2Player

Game2Player — это пайплайн из поиска игр, их адаптации и проверки, сбора игровых записей и обучения модели. **Среда и игроки дорабатывают друг друга:** игроки находят ошибки, которые не заметил сборщик, а сборщик проверяет их сообщения по записи прохождения.

[FIGURE:2]
[CAPTION:Game2Player подготавливает игру, проверяет её двумя игроками, исправляет найденные проблемы и собирает данные для обучения.]

🟠 **Искатель** отбирает игры, которые можно запускать офлайн в браузере, проходить в одиночку и надёжно перезапускать.  
🟠 **Сборщик** упаковывает игру в воспроизводимую среду, задаёт начальные условия и создаёт задачи. Для каждой он определяет, как измерять промежуточный прогресс и что считать успехом.  
🟠 **Игрок с изображениями** видит снимок экрана и выбирает действие, после чего игра останавливается до следующего решения. Он играет в режиме, близком к тому, как будет действовать обученная модель.  
🟠 **Игрок с программой** пишет отдельную программу для каждой игры. Она читает доступные игроку сведения о видимых объектах и действует в реальном времени без вызова модели на каждом шаге.  
🟠 **Проверка сообщений**: игроки сообщают о неисправных кнопках, неверной оценке прогресса или нехватке наблюдаемых данных. Сборщик сверяет жалобы с видеозаписью и состоянием игры, затем исправляет подтверждённые проблемы.  
🟠 **Отбор данных** повышает вес действий, за которыми последовал заметный прогресс, и снижает вес повторов и финальных шагов неудачных попыток.

## Как это работает: задача в веб-игре

Представим задачу, где нужно доставить железо и купить бур первого уровня. Система должна записать нажатия и отличить движение к цели от бесцельной игры.

[FIGURE:3]
[CAPTION:Игрок с программой действует по наблюдаемым данным в реальном времени, а игрок с изображениями выбирает действие по снимку экрана; их записи приводятся к общему формату.]

Сначала сборщик находит в коде игры данные о запасе железа и покупке бура. По этим данным он задаёт шкалу прогресса: каждое доставленное железо увеличивает оценку, а покупка бура означает успех. **Оценка опирается на состояние игры**, а не на мнение другой модели.

Затем игроки пытаются выполнить задачу. Игрок с изображениями видит экран, читает описание управления и выбирает действие, например нажимает клавишу движения. Игрок с программой получает сведения о видимых объектах и может точнее рассчитывать, когда нажать или отпустить клавишу.

Если железо доставлено, но оценка прогресса не меняется, игрок сообщает о возможной ошибке. Сборщик пересматривает запись и проверяет, правильно ли он связал показатель прогресса с игровым событием. Если проверка подтверждает проблему, он исправляет измерение, после чего игроки проходят задачу повторно. Здесь возможны сбои: сообщение может быть ошибочным, игровое состояние — прочитано неверно, а сама задача — оказаться невыполнимой. Поэтому сборщик должен подтвердить каждую жалобу и проверить результат исправления.

Когда среда принята, прохождения превращаются в обучающие примеры. Система связывает каждый экран и предшествующую историю с нужным действием. Примеры, после которых прогресс вырос, чаще попадают в обучение; бесполезные повторы получают меньший вес. Так модель учится выбирать действия, которые помогают двигаться к задаче.

## Как проверяют результаты

Авторы проверяют качество игровых сред и пользу собранных данных. Для первого теста они сравнивают полный цикл с вариантом без сообщений игроков и с обычным агентом для программирования, у которого нет специальных инструментов. Задачи заранее зафиксированы, а правильность среды проверяется сверкой с исходной игрой; проверку оценок дополнительно просматривают люди.

Для оценки обученной модели используют два бенчмарка: Player Bench из 50 игр, отложенных от обучения, и внешний GameWorld из 34 игр, которых нет в обучающей коллекции. В каждом измеряют **прогресс** — среднюю долю пути к цели, и **успех** — долю полностью выполненных задач. Игры в обучающей выборке не пересекаются с Player Bench; GameWorld тоже не пересекается с коллекцией.

Сравнение включает исходные модели, обученные Game2Player модели и другие зрительные модели. Участникам и моделям дают описания задач и управления, а попытки ограничивают одинаковым пределом в 100 шагов. Есть оговорка: модели останавливают игру на время каждого решения, поэтому тест не проверяет, как они справятся с задержками в реальном времени.

[FIGURE:6]
[CAPTION:В исследовании на 20 играх сообщения игроков повысили число правильно реализованных задач и задач, которые удалось пройти.]

## Цифры

[NUMBERS]
- 568 игр | столько игр превратили в проверяемые среды
- 3 436 задач | для каждой измеряются прогресс и условие успеха
- 15,7 тыс. траекторий | столько прохождений собрали; их общая длительность — 307 часов
- 14,3% → 31,2% | прогресс модели Qwen3.5-9B на Player Bench после обучения
- 30,0% → 53,1% | прогресс той же модели на внешнем бенчмарке GameWorld
[/NUMBERS]

Модель заметно улучшилась на обеих проверках, в том числе на играх, которых не было в обучающем наборе. В отдельном испытании на 20 играх сообщения игроков повысили долю правильно реализованных задач с 65% до 72%, а число задач, решённых программами-игроками, — с 34 до 46. Совместная проверка помогает собирать больше записей и исправлять условия, на которых они основаны.

## Вывод

Game2Player автоматизирует сбор игровых данных с проверяемыми целями: программу-игрока можно запускать много раз без отдельных вызовов модели на каждом шаге, а игрок с изображениями добавляет примеры решений, близких к восприятию будущей модели. Веса по прогрессу помогают модели учиться на действиях, которые действительно продвигают задачу.

Проверка не гарантирует, что каждая среда безошибочна: в исследовании часть задач после сборки оказалась реализована неверно. Набор ограничен одиночными играми, которые запускаются офлайн в браузере; онлайн-игры, многопользовательские режимы и крупные коммерческие проекты не охвачены. Кроме того, модели помогают собирать игровые миры и проверять жалобы, а их отдельные версии со временем меняются.

Пока результаты показывают, что такой подход полезен для обучения и тестирования зрительных агентов в играх. Следующий шаг — выяснить, сохранится ли эффект в более сложных средах, где решения приходится принимать без остановки игры и учитывать реальное время.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0]  -->
<!-- [FIGURE:2] Figure 2 : Overview of Game 2 Player . The Scout selects games from web portals ( top ).
In the co-development loop ( middle ), the Builder turns each game into an environment with state-verified tasks, the VLM Player and the Coding Player play every task and report faults of the game, and the Builder checks each report against the recording before repairing it.
Both players then record gameplay in the accepted environments to train Game 2 Player with progress-weighted SFT ( bottom ). -->
<!-- [FIGURE:3] Figure 3 : Two players on the same task and one training format. The code policy reads the player observation ψ \psi and sends keys at every frame without calling a model ( top ).
The VLM Player sees only the screenshot and pauses the game to choose each action ( bottom ).
The code policy’s keys are cut into steps in the VLM Player’s format, so both players yield the same kind of training example ( middle ). -->
<!-- [FIGURE:4] Figure 4 : The Game 2 Player collection and its training data. The 568 games cover diverse genres, of which the ten most common are shown ( left ). Share of each player in the training data, and the best progress of its training trajectories ( right ). Figure 19 compares all genres and engines with Player Bench . -->
<!-- [FIGURE:5] Figure 5 : Progress-weighted sampling. Actions receive weights from progress and repetition during play (1), followed by terminal outcomes (2). Paired bars compare the action budgets before and after game balancing (3), in units of the median game size M M . Stochastic rounding converts the weights into integer numbers of context–target pairs ( x , y ) (x,y) (4). Solid cards are guaranteed copies, and dashed cards are drawn with the displayed probabilities. The examples are schematic and use the factors in Tab. 11 . -->
<!-- [FIGURE:6] Figure 6 : Task outcomes of co-development on 20 games and 145 frozen tasks, with a GPT-6.1 Terra Builder and GPT-6.1 Sol players. -->
<!-- [FIGURE:7] Figure 7 : Recording gameplay with GPT-6.1 Sol. The cost of recording gameplay for one game ( left ) and the harness steps recorded per hour of wall-clock time ( right ), by the VLM Player and by the code policy. -->
<!-- [FIGURE:8] Figure 8 : Base and Game 2 Player models with thinking on and off. Progress ( top ) and success ( bottom ) in % of each Qwen3.5 base model (light) and its Game 2 Player counterpart (dark) on both benchmarks. -->
<!-- [FIGURE:9] Figure 9 : Human play by difficulty tier on Player Bench . Left: progress and success in %, averaged over the tasks of each tier, with the number of tasks under each tier. Right: median length of all attempts in seconds. -->
<!-- [FIGURE:10] Figure 10 : Training data and training steps. Progress and success on Player Bench and GameWorld with 0, 100K, 400K, 800K and all 1.56M training examples ( left ) and after 0, 3K, 6K and all 9.2K training steps ( right ). Hollow points at zero denote the untrained Qwen3.5 base models. -->
<!-- [FIGURE:11] Figure 11 : Qwen3.5-4B and Game2Player-4B on four held-out Player Bench tasks , with thinking on and at most 100 steps. Each panel shows the final frame of each model with its final progress, and the best progress reached after each step. -->
<!-- [FIGURE:13] (схема, нарисуем в стиле сайта) Figure 13 : Rules quoted from the agent prompts. The Scout selects games, the Builder freezes the tasks, measures progress toward the objective, plays from the player’s view and checks player reports against recordings, and the Coding Player reads only its probe and asks only for observable state. Grey brackets mark omitted text. -->
<!-- [FIGURE:14] Figure 14 : Code policies against VLM Players, game by game. Each dot is one of the 50 Player Bench games. Dots above the diagonal are games on which the Coding Player reaches higher progress than all four compared VLM Players, Qwen3.8-Flash, DeepSeek-V4.1-Flash, GLM-5.3-Flash and Gemini-3.8-Flash. -->
<!-- [FIGURE:15] Figure 15 : Progress of repeated code policy runs. Top, progress of the ten runs of the same code policy on each of twelve tasks drawn at random from the tasks with ten runs, with the progress distance D prog D_{\mathrm{prog}} of each task. Bottom, the density of D prog D_{\mathrm{prog}} over tasks for the code policies and for repeated runs of MiniMax-M3.1-Flash. -->
<!-- [FIGURE:16] Figure 16 : Key presses of repeated code policy runs. Top, the key presses in the first ten seconds of the ten runs of the same code policy on each of six tasks drawn at random from the tasks whose runs press different keys, one lane per run and one colour per key, with the key distance D key D_{\mathrm{key}} of each task. Bottom, the density of D key D_{\mathrm{key}} over tasks for the code policies and for repeated runs of MiniMax-M3.1-Flash. -->
<!-- [FIGURE:17] Figure 17 : Characteristics of the training data. (a) Cumulative fraction of trajectories by the number of eligible steps after segmentation and filtering, before resampling. The VLM Player has a 100-step budget. (b) Action composition of the final training examples. Individual keyboard actions, key sequences, mouse actions and waits are counted separately. (c) Distribution of samples per game before and after resampling. Each point counts the games in a sample-count interval, with neighboring interval counts connected by lines. Intervals use a logarithmic scale. -->
<!-- [FIGURE:18] (схема, нарисуем в стиле сайта) Figure 18 : Prompt of a VLM Player at one step, with thinking on. Grey text in angle brackets stands for the game rules, controls and task instruction written by the Builder and for the content of earlier steps. The user message holds up to 50 previous steps for open-weight models and all previous steps for API models, the last six with their screenshots, and the current screenshot. -->
<!-- [FIGURE:19] Figure 19 : The collection and the held-out split in full. Every genre and engine of the 568 games and the difficulty tiers of their 3,436 tasks, as shares of the whole collection (light) and of Player Bench (dark). The single-game genres are dress-up, interactive fiction, narrative, party, puzzle horror, runner, tower defense, typing and visual novel, and unclassified games fit none of the listed genres. -->
<!-- [FIGURE:21] Figure 21 : Task outcomes of all three settings in both experiments. A task is solved when its environment is correct and the final code policy completes it. -->
<!-- [FIGURE:22] Figure 22 : A VLM Player and a code policy on the same task. In each game, the upper row shows four steps of an episode of Claude Haiku 5.5 with the screenshot it saw, its action and its note, and the lower row four moments of a code policy episode that completes the task, each at a key press or click, with the frame, the keys held and fields of the policy’s observation. Pointers mark clicks. The bar and p p give the progress the VLM Player reaches. -->
<!-- [FIGURE:23] Figure 23 : Base and trained models on held-out Player Bench tasks , with thinking on and at most 100 steps. Each row shows the task, the initial frame and the final frames of Qwen3.5-4B and Game2Player-4B. The curves show the best progress reached after each step. -->
<!-- [FIGURE:24] Figure 24 : Participants of the human study. (a) Age group and gender. (b) Attempts of each participant, split into successful and unsuccessful ones. -->

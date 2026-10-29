# Как ИИ-агенты учатся общим навыкам на разных задачах

## Агент учится на общих навыках

В одном бенчмарке нужно разгадывать правила настольной игры, в другом — проходить лабиринт, в третьем — управлять роботом. На первый взгляд, это совсем разные задачи. Но за каждой может стоять одна и та же способность: следить за состоянием мира и не забывать, что изменилось после действия.

На этом наблюдении построена **The Trinity** — система, которая улучшает обвязку ИИ-агента не отдельно для каждой задачи, а с учётом общих требований к способностям. Авторы оставили саму модель неизменной. Менялись инструменты и правила, которые направляют её работу: как собирать факты, проверять варианты, планировать действия и решать, когда пора остановиться.

В результате система улучшила средний результат на 34 пункта на 28 обучающих бенчмарках и на 26 пунктов на 18 ранее не встречавшихся. Среди проверок были и задачи на настоящих роботах.

## Почему задачам нужны общие способности

Многие современные ИИ-агенты должны работать долго и в разных форматах: читать текст, разбирать изображения и видео, выбирать действия и учитывать их последствия. Ошибка на раннем шаге может испортить всё продолжение: агент неверно понял сцену, сделал неподходящий ход, а затем строит план на ошибочном представлении.

Обычно такую проблему решают отдельно для каждого набора задач. Но отдельные настройки плохо переносятся на другие условия. И одна общая обвязка тоже может быть неудобна: задачи требуют разных навыков и иногда спорят друг с другом. Например, осторожность помогает не делать необратимых ходов, но может мешать действовать быстро.

Авторы предлагают группировать задачи по нужным способностям, а не по внешнему сходству. Разгадывание сетки и движение по лабиринту выглядят по-разному. Но обе задачи требуют замечать изменения и вести точный учёт состояния. Если обучить этому общему навыку, он может помочь сразу в нескольких средах.

В системе задействованы три роли:

🟠 **Создатель** придумывает небольшие учебные миры с понятными правилами и проверяемыми результатами.  
🟠 **Исследователь** проходит эти миры и собирает примеры удачных и неудачных действий.  
🟠 **Эволюционер** разбирает эти примеры, группирует задачи по нужным способностям и предлагает изменения обвязки.

[FIGURE:0]  
[CAPTION:Три роли системы связывают задачи, учебные миры и развитие обвязки ИИ-агента.]

## Как способности превращаются в модули

Сначала команда собрала 44 бенчмарка: 28 для обучения и 18 для проверки на новых задачах. Они охватывают головоломки, видеозадачи, игры с другими участниками, управление и робототехнику. Часть сред исследователи воссоздали по опубликованным правилам.

Затем систему запускали на обучающих задачах и изучали записи её действий. Так исследователи выделили шесть общих способностей: отслеживание восприятия и состояния, проверку гипотез, работу с ограничениями, выбор цели, поиск нужных кадров в видео и понимание событий между кадрами.

Из этих способностей собрали дерево. Узел отвечает за сочетание требований, а задачи из разных областей могут оказаться в одной ветке. Например, планирование, осмотр объектов и движение по лабиринту могут требовать похожего контроля состояния и проверки результата. Дерево фиксирует общие навыки, а не внешнее сходство задач.

Дальше для каждого узла Создатель строит упрощённый учебный мир. Если нужная способность — проверять, действительно ли цель достигнута, среда может учить этому на простой задаче с предметами и правилами. Она должна быть достаточно понятной для проверки, но при этом сохранять ключевую логику исходных задач. Результаты затем измеряют на первоначальных бенчмарках: так проверяют, перенёсся ли навык за пределы учебного мира.

[FIGURE:1]  
[CAPTION:Учебный мир создаётся из общей способности, нужной нескольким разным задачам.]

Сама обвязка состоит из модулей: одни помогают воспринимать данные, другие — вести память, проверять гипотезы или выбирать действия. ИИ-агент не меняет веса модели. Он улучшает эти модули по записям взаимодействий: сравнивает успешные и неудачные попытки и предлагает точечные изменения.

Новые модули проходят проверки: у них должны быть понятные входы и выходы, они должны опираться на реальные примеры и соответствовать версии, которую заменяют. Дочерние ветки дерева могут наследовать модули родителей, но сохранять собственные настройки. Так формируются разные обвязки для разных сочетаний способностей.

Это решает ещё одну задачу: не нужно каждый раз собирать всю систему заново. Модуль, который помогает отслеживать состояние, можно повторно использовать в нескольких ветках. А неподходящие решения не обязаны распространяться на все задачи.

## Что показали эксперименты

Авторы сравнили разные способы организации обвязок. Один общий набор модулей, отдельная настройка для каждой категории задач и группировка по способностям давали разные результаты. Лучше всех на новых задачах показало себя дерево способностей, обучавшееся в созданных системой мирах: оно набрало 47,26 пункта против 42,92 у общей обвязки. На обучающих задачах результат составил 56,95 против 53,04.

Затем систему улучшали в течение четырёх циклов. Средний результат на обучающей выборке вырос с 39,1 до 73,2 пункта, на новых задачах — с 42,1 до 64,1. Самый большой прирост пришёлся на первый цикл, но следующие три тоже добавили очки.

Улучшение распределилось неравномерно. Например, результат в ARC-AGI-3 вырос с 41,0 до 53,6 пункта, а в SciGym — с 45,2 до 57,1. На бенчмарке Eleusis итог, напротив, оказался немного ниже, чем после первого цикла. Средние значения скрывают такие различия, поэтому их важно смотреть вместе с результатами отдельных задач.

Маршрутизатор выбирает подходящую обвязку для каждой задачи по открытым данным о ней и проверенному опыту прошлых запусков. На обучающих бенчмарках он набрал 71,27 пункта, на новых — 60,96. Для сравнения, подбор лучшей обвязки задним числом давал 73,16 и 63,61 пункта соответственно. Значит, выбор можно автоматизировать почти без потери результата. Маршрутизатор при этом не получает правильные ответы из проверочной выборки: он использует только доступное описание задачи и опыт, собранный на обучающих запусках.

[FIGURE:2]  
[CAPTION:Средние результаты растут с каждым циклом, а стоимость повторного обучения снижается при повторном использовании учебных миров.]

Отдельно проверили, помогают ли подходящие модули сами по себе. Добавление модуля, связанного с нужной способностью, подняло результат базовой обвязки на 19,39 пункта. Случайный модуль, не связанный с задачей, дал прирост только в 1,02 пункта. А удаление подходящего модуля из улучшенной обвязки снизило результат на 2,74 пункта. Это подтверждает, что модули стоит подбирать под требуемые способности, а не наращивать без разбора.

Наконец, эволюционировавшие обвязки проверили на двух роботах. В одном опыте робот должен был подойти к столу и дотянуться до него. В другом — найти кубик, спрятанный под чашками, и определить его цвет и положение. На версиях, обученных системой, роботы чаще успешно выполняли обе задачи в симуляции и в реальности. Например, в задаче с чашками базовая обвязка могла заявить, что кубика нет, так и не осмотрев нужную чашку. Улучшенная последовательно проверяла предметы и отвечала после того, как находила кубик.

[FIGURE:6]  
[CAPTION:Робот с улучшенной обвязкой точнее подходит к цели и проверяет чашки, прежде чем сообщить, где находится кубик.]

## Чего результаты пока не доказывают

Эксперименты показывают рост средних результатов и перенос на новые задачи, но не гарантируют одинакового улучшения во всех областях. В отдельных бенчмарках прогресс небольшой, а некоторые задачи — например Crafter и DiG-bench — система решала хуже двух систем сравнения.

Результаты по робототехнике тоже стоит рассматривать с учётом устройства проверки. Авторы сравнивали целые связки «обвязка плюс подготовленные навыки», поэтому нельзя точно отделить вклад модулей от вклада этих навыков. Кроме того, физических задач было только две, а число испытаний на них ограничено.

Есть и практический компромисс: создание учебных миров требует ресурсов. Авторы отмечают, что в первом цикле генерация сред составляла значительную часть затрат, зато позднее среды можно было использовать повторно. Подход становится выгоднее, если учебный мир помогает улучшать обвязку в нескольких циклах и переносить результат на разные задачи.

## Вывод

**The Trinity переносит развитие ИИ-агента с уровня отдельных задач на уровень общих способностей.** Вместо того чтобы писать специальную обвязку для каждой игры, головоломки или робота, система ищет повторяющиеся требования, создаёт для них проверяемые учебные миры и постепенно улучшает подходящие модули.

Результаты на новых бенчмарках и роботах показывают, что такой перенос возможен. Но система пока не улучшает все задачи одинаково, а оценка в робототехнике охватывает только два сценария. Следующий шаг — проверить, насколько хорошо дерево способностей расширяется на новые требования и работает в более широком наборе реальных условий.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 2 : Detailed pipeline of The Trinity. Three stages build task, capability, and Harness trees.
Worlds are verified and screened; Harnesses evolve through selective inheritance and local refinement.
Routing selects one compatible Harness and stores verified feedback for later tasks. -->
<!-- [FIGURE:1] Figure 3 : Capability-driven world creation at node d. -->
<!-- [FIGURE:2] Figure 4 : Training cost and Train performance across RSI iterations. -->
<!-- [FIGURE:3] Figure 5 : Benchmark-level Harness evolution. Left: Train; right: Unseen. Radial bars show Base and Iterations 1–4; * Agent-built from web-searched sources. -->
<!-- [FIGURE:4] Figure 6 : RSI mean performance across benchmarks. Horizontal lines show Codex and DeepSeek reference means. -->
<!-- [FIGURE:5] Figure 7 : Capability–protocol correlations across six protocols. Red is positive; blue is negative. -->
<!-- [FIGURE:6] Figure 8 : Embodied Transfer of Capability-Evolved Harnesses. Real scenes, simulators, and robot trials (SOON E01; CaP-X C-01). The circle marks the revealed cube. -->
<!-- [FIGURE:7] Figure 9 : Task tree. The 44 benchmarks are grouped into five domains and 15 subclasses. Training benchmarks take the colour of their domain and unseen benchmarks a lighter shade of it; SOON and CaP-X show their simulation and real-robot versions; * marks environments rebuilt from published rules. -->
<!-- [FIGURE:8] Figure 10 : Flat capability tree. Bricks keep the colours of Figure 9 ; unseen benchmarks are in italics; * marks rebuilt environments. -->
<!-- [FIGURE:9] Figure 11 : Capability tree. Each node is one combination of capabilities, read along the branch from the root, and each benchmark sits at the node of its combination. Bricks keep the colours of Figure 9 ; unseen benchmarks are in italics; * marks rebuilt environments. -->
<!-- [FIGURE:10] Figure 12 : Explorer Harness tree. Every node Harness starts from H 0 and combines the modules it selectively inherits with its own local modules. Brick colours mark capability families, and labels give module IDs. -->
<!-- [FIGURE:11] Figure 13 : Creator shared Harness. The root is the Base Harness H 0 with the pre-RSI modules. Each node shows the modules proposed or revised at that node. The modules of all nodes are merged and deduplicated into one shared library of 25 modules. Brick colours group the library by function. -->
<!-- [FIGURE:12] Figure 14 : AdaPlanBench (train) -->
<!-- [FIGURE:13] Figure 15 : Among Us (train) -->
<!-- [FIGURE:14] Figure 16 : ARC-AGI-3 (train) -->
<!-- [FIGURE:15] Figure 17 : BoxingGym (train) -->
<!-- [FIGURE:16] Figure 18 : Chess Tactics (train) -->
<!-- [FIGURE:17] Figure 19 : Codenames (train) -->
<!-- [FIGURE:18] Figure 20 : Colonel Blotto (train) -->
<!-- [FIGURE:19] Figure 21 : DiscoverPhysics (train) -->
<!-- [FIGURE:20] Figure 22 : Eleusis (train) -->
<!-- [FIGURE:21] Figure 23 : Euro NCAP AEB (train) -->
<!-- [FIGURE:22] Figure 24 : GLEE Persuasion (train) -->
<!-- [FIGURE:23] Figure 25 : Master Keying (train) -->
<!-- [FIGURE:24] Figure 26 : Mastermind (train) -->
<!-- [FIGURE:25] Figure 27 : Memory Maze (train) -->
<!-- [FIGURE:26] Figure 28 : Micromouse (train) -->
<!-- [FIGURE:27] Figure 29 : Pallet Rack Inspection (train) -->
<!-- [FIGURE:28] Figure 30 : PInVerify (train) -->
<!-- [FIGURE:29] Figure 31 : Pooltool Billiards (train) -->
<!-- [FIGURE:30] Figure 32 : puzz.link / Penpa+ (train) -->
<!-- [FIGURE:31] Figure 33 : PuzzleScript (train) -->
<!-- [FIGURE:32] Figure 34 : Saboteur (train) -->
<!-- [FIGURE:33] Figure 35 : TextQuests (train) -->
<!-- [FIGURE:34] Figure 36 : The Long Dark (train) -->
<!-- [FIGURE:35] Figure 37 : Video-Index (train) -->
<!-- [FIGURE:36] Figure 38 : WCA Cube Solving (train) -->
<!-- [FIGURE:37] Figure 39 : WILT (train) -->
<!-- [FIGURE:38] Figure 40 : ActiView (unseen) -->
<!-- [FIGURE:39] Figure 41 : ALE-Bench (unseen) -->
<!-- [FIGURE:40] Figure 42 : BuildArena (unseen) -->
<!-- [FIGURE:41] Figure 43 : Coup (unseen) -->
<!-- [FIGURE:42] Figure 44 : Crafter (unseen) -->
<!-- [FIGURE:43] Figure 45 : DiG-bench (unseen) -->
<!-- [FIGURE:44] Figure 46 : Entity Deduction Arena (unseen) -->
<!-- [FIGURE:45] Figure 47 : Hanabi (unseen) -->
<!-- [FIGURE:46] Figure 48 : Heads-Up NL Hold’em (unseen) -->
<!-- [FIGURE:47] Figure 49 : MiniHack Boxoban (unseen) -->
<!-- [FIGURE:48] Figure 50 : MiniHack Maze / Corridor (unseen) -->
<!-- [FIGURE:49] Figure 51 : NetHack (unseen) -->
<!-- [FIGURE:50] Figure 52 : Pencil Puzzle Bench (unseen) -->
<!-- [FIGURE:51] Figure 53 : PHYRE (unseen) -->
<!-- [FIGURE:52] Figure 54 : SciGym (unseen) -->
<!-- [FIGURE:53] Figure 55 : Video-MME-v2 (unseen) -->
<!-- [FIGURE:54] Figure 56 : SOON (embodied, simulation) -->
<!-- [FIGURE:55] Figure 57 : CaP-X (embodied, simulation) -->
<!-- [FIGURE:56] Figure 58 : c: Gate Planning & Reachability -->
<!-- [FIGURE:57] Figure 59 : c → \to d: Value & Goal Commitment -->
<!-- [FIGURE:58] Figure 60 : c → \to d → \to a: Execution & Revision Memory -->
<!-- [FIGURE:59] Figure 61 : c → \to a: Identity, Order & Memory -->
<!-- [FIGURE:60] Figure 62 : d: Evidence-Gated Commitment -->
<!-- [FIGURE:61] Figure 63 : d → \to a: Exploration & Routing -->
<!-- [FIGURE:62] Figure 64 : d → \to b: Hypothesis Tracking & Probing -->
<!-- [FIGURE:63] Figure 65 : a: Evidence & Inspection -->
<!-- [FIGURE:64] Figure 66 : b: Signaling & Counterpart Decisions -->
<!-- [FIGURE:65] Figure 67 : e: Video Evidence Acquisition -->
<!-- [FIGURE:66] Figure 68 : e → \to f: Video Events & Frame Association -->
<!-- [FIGURE:67] Figure 69 : Embodied environments. Real scenes appear above their simulated counterparts, with SOON on the left and CaP-X on the right. -->
<!-- [FIGURE:68] Figure 70 : SOON with the Base Harness. Rows show simulation and real-robot views from the fixed office camera, followed by the head camera. The robot walks from the side room along the aisle, looks around, and turns towards the desk beside the fan, but reaches out before the desk is within reach in both settings. -->
<!-- [FIGURE:69] Figure 71 : SOON with the evolved Harness. Rows follow Figure 70 . In simulation the robot turns right past the doorway, walks diagonally towards the desk beside the fan, and slows to small steps before touching it. The real robot also approaches in small steps and completes the task. -->
<!-- [FIGURE:70] Figure 72 : CaP-X with the Base Harness. Rows show head, side, and wrist cameras in simulation, followed by the real robot. In both settings the robot manipulates other cups without inspecting the target cup and incorrectly reports that no cube is present. -->
<!-- [FIGURE:71] Figure 73 : CaP-X with the evolved Harness. Rows follow Figure 72 . In simulation the robot checks the cups and retries a missed grasp until the cube is visible. On the real robot it sweeps the cups aside to uncover the cube; both runs then report its colour and location. -->

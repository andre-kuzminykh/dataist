# Как один ИИ-агент работает в телефоне, браузере и на компьютере

## Qwen-UI-Agent: ИИ-агент, который пользуется телефоном и компьютером

Все хотят универсального ИИ-агента. Такого, которому можно сказать: «Разберись». Он сам откроет приложения, найдёт нужные кнопки, сравнит варианты, поправит файл на компьютере, а если прилетело уведомление об отмене рейса — предложит готовый план действий.

Проблема в том, что почти все такие демонстрации хорошо выглядят на вылизанных тестах и заметно хуже — в живых приложениях. На настоящем смартфоне всё мешает: всплывающие окна, слетевшие логины, капча, странная вёрстка, медленная сеть, неожиданные экраны подтверждения. На компьютере другая проблема: одних кликов мало. Иногда быстрее и надёжнее сделать часть работы через командную строку.

Именно эту проблему решает команда Alibaba в большом техническом отчёте про **Qwen-UI-Agent**. Это ИИ-агент для графических интерфейсов, который работает сразу в нескольких средах: на телефоне, на компьютере, в браузере и в режиме поиска по интернету. Если вы хотите полезного ИИ-агента, мало обучить модель нажимать на кнопки. Нужно строить всю систему целиком — среду, данные, обучение, проверку и продуктовую обвязку.

## Что здесь сделали

Qwen-UI-Agent — это не просто ещё одна модель, которая умеет кликать по экрану. Это целый стек.

🟠 Агент работает с мобильными приложениями, настольными программами, браузером и внешними сервисами поиска.

🟠 Он умеет не только нажимать и печатать в интерфейсе, но и выполнять команды в командной строке, а также обращаться к API.

🟠 Он может выдавать не одно действие за шаг, а пачку действий, если между ними не нужно каждый раз ждать новый экран.

🟠 Его обучали не только на коротких сценариях, но и на длинных траекториях — больше 100 шагов.

🟠 Поверх агента есть отдельный слой, который позволяет запускать задачи по уведомлениям и переносить работу между телефоном и компьютером.

У обычных демонстраций ИИ-агентов часто одна и та же слабость: они выглядят как набор отдельных фокусов. Здесь авторы пытаются собрать из этого рабочую операционную систему для агента.

[FIGURE:2]

## Почему упор на реальные устройства

Разрыв между симуляцией и реальностью для мобильных агентов большой.

В песочнице всё удобно. Приложение можно сбросить в начальное состояние. Нужные данные уже лежат на месте. Нет внезапной капчи. Нет рекламы. Нет нестабильной сети. Но пользователь живёт не в песочнице.

Авторы поэтому построили парк из более чем 100 физических телефонов и более 150 приложений. Это не просто набор гаджетов на столе. Там есть диспетчер, который следит, какой телефон исправен, где какой аккаунт залогинен, какая сеть доступна, где сломалась среда, а где ошибся сам агент.

Система умеет различать ошибку модели и ошибку среды. Если приложение зависло или сеть отвалилась, это не должно записываться в промах агента. Для этого они отдельно анализируют полную траекторию выполнения.

[FIGURE:6]

Отсюда же появился новый бенчмарк **MobileWorld-Real** — 409 задач в 104 приложениях на живых Android-устройствах. Это один из вкладов работы. Он показывает, насколько тяжело ИИ-агенту в обычной мобильной жизни. И именно там Qwen-UI-Agent набрал **92,2%** успешных выполнений. Для сравнения, у закрытых моделей результат ниже: Gemini 3.1 Pro — 86,2%, GPT-5.6 Sol — 85,4%, Claude Opus 4.8 — 84,7%.

Это важно. Это проверка того, переносится ли навык из лаборатории на реальный экран.

## Как агент действует: интерфейс, командная строка и пачки действий

У Qwen-UI-Agent единое пространство действий. Он может:

🟣 кликать, свайпать, печатать, открывать приложения и нажимать системные кнопки;

🟣 выполнять команды в командной строке;

🟣 вызывать API;

🟣 спрашивать пользователя, если нужно подтверждение или не хватает данных;

🟣 завершать задачу с результатом.

На бумаге это выглядит очевидно. Вместо логики «всё делаем только мышкой и глазами» здесь есть несколько способов действия. Но часть задач через интерфейс делать долго и бессмысленно.

Пример из статьи: если надо найти правильную фотографию среди множества похожих, агент не открывает каждую по отдельности. Он может одной командой в командной строке собрать коллаж из миниатюр, быстро посмотреть на него, а потом уже через интерфейс выбрать нужное. То есть командная строка становится быстрыми руками, а графический интерфейс — глазами для проверки.

[FIGURE:8]

Это даёт два эффекта сразу.

🟠 Задачи решаются быстрее, потому что часть рутины уходит в командную строку.

🟠 Агент покрывает больше типов задач: от визуальной навигации до обработки файлов и данных.

Ещё одна деталь — **пакетные действия**. Если агент понимает, что может подряд сделать несколько предсказуемых шагов, он не тратит отдельный шаг модели на каждый клик. Например, открыть поиск по странице, ввести запрос и нажать Enter. Или пройти длинную последовательность заполнения формы, пока не появится место, где снова нужно подумать.

На сложном компьютерном бенчмарке OSWorld-v2 это дало заметную экономию шагов. У Qwen-UI-Agent среднее число шагов на задачу — 135,8. Это меньше, чем у ряда открытых моделей, которые тратят 170–320 шагов.

## Как его обучали

Архитектура здесь интересна, но основной вклад всё же в дата-пайплайн и обучение.

Сначала авторы собирают данные для обучения с учителем: траектории, где агент шаг за шагом решает задачи. Но они не полагаются только на ручную разметку. У них есть автоматический цикл улучшения данных — своего рода маховик.

[FIGURE:4]

Схема примерно такая:

🟣 сильные модели помогают придумывать новые задачи;

🟣 агенты создают состояния среды под эти задачи;

🟣 затем другие агенты или проверяющие модели анализируют, где текущая версия проваливается;

🟣 после этого система генерирует новую порцию данных ровно под слабые места;

🟣 следующая итерация обучения использует эти данные.

Поверх обычного обучения с учителем идут два слоя обучения с подкреплением.

Первый слой — исправление типовых локальных ошибок. Авторы перечисляют шесть повторяющихся паттернов: агент путает похожие кнопки, ошибается в сортировке, не добирает все нужные элементы, слишком рано объявляет успех, зацикливается на одном действии, плохо использует редкие, но важные действия вроде долгого нажатия или запроса к пользователю.

Под это они собрали отдельные данные и обучили политику штрафовать такие ошибки. Результат — меньше циклов и меньше ложных завершений.

Второй слой — длинные траектории. Здесь агента учат доводить задачу до конца, а не просто красиво делать отдельные шаги. Для этого используют обучение с подкреплением по итоговому результату задачи. Среда запускается параллельно примерно в 10 тысячах экземпляров, чтобы ускорить сбор опыта.

Ключевой эффект такого обучения: агент начинает чаще **проверять**, что задача реально выполнена. Не «я вроде создал файл, значит всё в порядке», а «я снова открою файл и посмотрю, есть ли там нужный график». Это улучшение поведения, близкое к человеческому.

## Что получилось в цифрах

С результатами здесь всё довольно убедительно. Qwen-UI-Agent оказался не узким мобильным агентом, а системой сразу в нескольких режимах.

На мобильных задачах:

🟠 82,1% на MobileWorld

🟠 92,2% на MobileWorld-Real

🟠 97,5% на AndroidDaily

На компьютерных задачах:

🟠 79,5% на OSWorld-Verified

🟠 40,0% по метрике частичного прогресса на OSWorld-v2

На браузерных задачах:

🟠 73,6% на WebArena

На привязке к элементам интерфейса:

🟠 81,5% на ScreenSpot-Pro в режиме с увеличением

[FIGURE:0]

Особенно показателен не один рекорд, а разброс. Обычно модели хороши либо в мобильных задачах, либо в браузере, либо в компьютерных сценариях. Здесь видно, что авторы строили базового агента для цифровой среды в целом.

## Самая интересная часть: проактивность и работа между устройствами

Поверх модели авторы добавили отдельный слой, который превращает набор действий в помощника.

Пример из статьи: на телефон приходит уведомление об отмене рейса. Вместо того чтобы ждать команду пользователя, система связывает это событие с поездкой, встречами в календаре и личными предпочтениями. Потом ищет альтернативные перелёты и поезда, проверяет, на что вы успеваете, и готовит вариант решения. А уже действия с последствиями — например, перебронирование — просит подтвердить.

[FIGURE:10]

Это уже похоже на продуктовую логику помощника. Там есть понятия события, текущего дела, памяти о пользователе и состояния задачи.

Похожая идея работает и для задач между устройствами. Агент может что-то найти на телефоне, продолжить обработку на компьютере, отправить результат и потом вернуть финальный выбор обратно в мобильное приложение. Контекст при этом не теряется.

Для пользователя это важнее, чем ещё плюс 2% на бенчмарке. Большая часть реальной цифровой жизни размазана между приложениями и устройствами. Если агент не умеет переносить состояние между ними, он быстро упирается в потолок пользы.

## Где пока есть ограничения

Авторы сами честно показывают ограничения.

🟣 На реальных устройствах успех оценивает не жёсткий программный проверяющий модуль, а автоматический судья по траектории. Он точен, но не идеален.

🟣 Полная автоматизация улучшения агента пока не работает. Люди всё равно следят за пайплайном и вмешиваются.

🟣 Реальные устройства сложно масштабировать. Они дорогие, нестабильные и требуют постоянного обслуживания.

🟣 Даже с пакетными действиями задержка остаётся проблемой. Длинные задачи всё ещё занимают много времени.

Вокруг ИИ-агентов часто много разговоров про универсальность, но меньше — про операционную реальность. А здесь видно, где система упирается в инфраструктуру, а не только в качество модели.

## Вывод

Если вы хотите понять, куда движутся ИИ-агенты для интерфейсов, смотреть нужно не только на то, как модель находит кнопку на скриншоте. Смотреть нужно на всю систему.

Qwen-UI-Agent показывает три вещи.

🟠 Реальные устройства важнее красивых симуляций, если вы хотите довести агента до живого применения.

🟠 Гибрид из графического интерфейса, командной строки и API работает лучше, чем ставка на один способ действия.

🟠 Длинные задачи требуют не только рассуждения, но и проверки результата, исправления ошибок, памяти о состоянии и хорошего дата-пайплайна.

В этом направлении ИИ-агенты становятся ближе к полезному цифровому помощнику. К системе, которая умеет последовательно доводить дело до конца на реальных экранах.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1: Qwen-UI-Agent demonstrates leading or competitive performance across diverse GUI settings. -->
<!-- [FIGURE:1] Figure 2: An illustrative trajectory of Qwen-UI-Agent for proactive cross-platform task execution. The left panel summarizes the system capabilities underlying the trajectory, including cross-platform execution, a hybrid action space spanning GUI, CLI, and API operations, and environments ranging from large-scale sandboxes to real devices. The right panel illustrates a travel-recovery scenario triggered by a flight-cancellation notification. After identifying the affected tasks and commitments, the agent searches for alternative flights through an API, requests user approval before rebooking via a mobile GUI, updates the affected meeting schedule through desktop GUI and CLI actions, and sends the revised artifact to the relevant recipients. -->
<!-- [FIGURE:2] Figure 3: The environment infrastructure of Qwen-UI-Agent. (a) Scalable sandbox environments spanning mobile-use, computer-use, browser-use, and DeepSearch provide controllability and repeatable evaluation for data synthesis and training. (b) A sim-to-real bridge extends agents to real devices with real applications, networks, and account states, supporting user takeover for login, payment, permission, and confirmation. (c) A hybrid GUI+CLI action space interleaves graphical operations with direct command execution. (d) A unified interface standardizes the thinking–action–observation loop across heterogeneous environments. -->
<!-- [FIGURE:3] Figure 4: Real-device mobile runtime with closed-loop environment governance. The health-aware scheduler routes each task to an eligible phone, App/account, and display; unhealthy targets remain blacklisted until repair and revalidation. Virtual displays allow one phone to run multiple Apps concurrently. Evidence-based review separates task success, model failure, and environment failure from the complete trajectory, and confirmed environment issues are fed back to the scheduler. -->
<!-- [FIGURE:4] Figure 5: The data flywheel of Qwen-UI-Agent. Domain capability bootstrapping initializes training, iterative refinement loop identifies capability weaknesses and generate targeted tasks, and the resulting data improve the next training iteration. -->
<!-- [FIGURE:5] Figure 6: Overview of our harness for proactive service initiation and cross-platform execution. (I) Without the harness, users must manually interpret notifications, retrieve related context, and provide instructions for the agent. The proactive harness instead detects a flight cancellation, reasons over relevant affairs, proactively implement flight rebooking, railway alternatives, and meeting-conflict checks, and report an actionable plan. (II) The harness also maintains task state and support cross-platform execution. In the restaurant-selection example, Qwen-UI-Agent discovers candidates on mobile, organizes them in a desktop spreadsheet, sends the artifact for approval, and saves the selected locations back to mobile. -->
<!-- [FIGURE:6] Figure 7: Overview of MobileWorld-Real, a real-device benchmark with human-written tasks that reflect the breadth of everyday mobile use. Representative examples and aggregate statistics show broad domain coverage and a long-tailed App distribution. Matched-model results further show lower success rates and longer trajectories than on AndroidDaily, highlighting the challenge of real-world mobile interaction. -->
<!-- [FIGURE:7] Figure 8: Demonstration of real-device mobile GUI execution. The trajectory is rendered as key frames with the executed action annotated beneath each frame. In this cross-app task, the agent looks up the target address on Amap, finds the most popular café nearby on Dianping, and posts a summary of the findings on RedNote. -->
<!-- [FIGURE:8] Figure 9: Demonstration of hybrid GUI+CLI execution in computer-use tasks. Key frames are shown with the emitted actions, where CLI commands are highlighted in blue, GUI actions in red, and each step carries a short annotation of its intent.
In this example, the agent selects the target photo and filters by stitching all candidates into a single montage via CLI for one-shot visual inspection, rather than opening each image individually. It then leverages hybrid execution to combine CLI-based processing with GUI-based verification for the final output. -->
<!-- [FIGURE:9] Figure 10: Demonstration of DeepSearch-assisted GUI execution. The upper panels show the multi-round search process, including keyword-based DeepSearch, targeted web fetches with intermediate thoughts, and the final search summary; the lower row shows the subsequent GUI trajectory. DeepSearch resolves the knowledge and reasoning problem before GUI execution, converting the vague cross-source request into an explicit target: Qwen-UI-Agent identifies the largest comeback in the World Cup knockout stage through DeepSearch, then opens RedNote and navigates directly to the highest-engagement related post from the past week without blind in-app searching. -->
<!-- [FIGURE:10] Figure 11: Demonstration of proactive service based on mobile notifications. The trajectory is organized into highlighted stages: proactive task initiation from a detected notification, proactive execution phases, and a decision-ready result, with the executed action annotated beneath each key frame. Flight-cancellation recovery: when the user’s next-morning flight is canceled and a 14:00 demo is at risk, the harness proactively searches alternative flights and high-speed trains, evaluates which options arrive on time, and presents a decision-ready travel recovery plan. -->
<!-- [FIGURE:11] Figure 12: Demonstration of cross-platform task execution. In this workflow, mobile subtasks run on virtual screens of the physical device, so execution does not block the user’s own actions. Parallel multi-app search: the agent searches sushi restaurants on Dianping, Meituan, and Amap concurrently through multiple virtual screens, consolidates their ratings, and summarizes the top three options in a local report opened on the computer. -->
<!-- [FIGURE:12] Figure 13: Representative real-device failure patterns of Qwen 3.7 Plus. Execution capability limitations: (a) exploration failure, (b) erroneous action loops, (c) lost execution state. Real-world scenario challenges: (d) UI misreading, (e) pop-up interference, (f) physical widget control. Speech bubbles quote the model’s abridged thinking, with the critical fallacy in purple. -->
<!-- [FIGURE:13] Figure 14: Representative GUI interaction patterns. The panels show (a) filling structured spreadsheet content,
(b) finding content with in-page search, (c) visual navigation through
scrolling, (d) use of a native media-timeline feature,
(e) continuous spatial interaction, and (f) zooming in for fine-grained
inspection. Each panel pairs the rendered action with its resulting
application state. -->
<!-- [FIGURE:14] Figure 15: Representative CLI interaction patterns. The model uses CLI tools to (a) retrieve relevant documents from a mixed
corpus, (b) parse machine-readable artifact structure, (c) compress many
visual candidates into one labeled comparison, (d) transform an artifact
programmatically, (e) execute a repeated computation and materialize its
outputs, and (f) verify exact output and process postconditions. Each panel
juxtaposes the application context with a command excerpt and its
task-specific purpose. -->
<!-- [FIGURE:15] Figure 16: Representative batched-action patterns. (a) a compact GUI macro for
in-page search, (b) a 21-action dependent form sequence that stops at the
next uncertain dialog, and (c) a GUI–CLI handoff that verifies a spatial
manipulation through structured task state. Each row pairs the rendered
batch with the first post-batch observation. -->
<!-- [FIGURE:16] Figure 17: Representative trajectory of tightly coupled GUI–CLI collaboration. The task requires Qwen-UI-Agent to achieve a score of at least 100 in a browser-based dinosaur game without using DevTools or CDP. GUI observations provide evidence for measuring jump dynamics, diagnosing failed control policies, and recognizing changes between day and night modes, while CLI code iteratively implements stateful key control and adaptive obstacle detection. -->
<!-- [FIGURE:17] Figure 18: Action RL case study. The SFT model navigates to the account page and repeatedly clicks the share icon before navigating back, becoming trapped in an ineffective local loop. In contrast, the model after action RL recognizes that it is on the wrong page, switches to exploring Mastodon’s web interface, locates the correct entry point, and successfully configures the target invite link with the required settings. -->
<!-- [FIGURE:18] Figure 19: Online RL elicits verification and self-correction. On the same task, the online RL policy (bottom) succeeds where the SFT policy (top) fails, because it reopens the application to inspect the actual result and corrects the problem it finds before finishing. The SFT policy trusts a superficial script check that only counts the chart, never looks at the rendered output, and ships an empty chart with no data series, whereas the RL policy reopens the file to verify, finds that a leftover application instance would overwrite the chart, removes it so the chart persists, and confirms that the full clustered chart is actually rendered before terminating. -->
<!-- [FIGURE:19] Figure 20: Online RL elicits emergent cross-modal action. On the same task, the online RL policy (bottom) succeeds where the SFT policy (top) fails, because it grounds its decisions in what it visually observes and verifies the result before finishing. The SFT policy reads the receipt from OCR text alone, mistakes a Cash Out for income, and declares success without checking, whereas the RL policy opens the receipt image to visually read it, records it correctly as an expense, and reads the spreadsheet back to verify before terminating. -->
<!-- [FIGURE:20] Figure 21: Online RL improves long-horizon search and verification. Without online RL, the model follows incorrect entity associations and reaches the unsupported answer Guangzhou. With online RL, it identifies the key chain of Hai Yan, Nirvana in Fire , Huang Weide, and Chengdu. -->

# Путь к более общему ИИ лежит через модель мира

## Когда модели перестают угадывать следующий токен и начинают «понимать, что будет дальше»

В ИИ сейчас много сильных систем. Одни красиво пишут текст. Другие рисуют картинки. Третьи управляют роботами. Но почти все они учатся в рамках своей узкой задачи: предсказать следующий токен, следующий кадр или следующее действие.

Авторы Orca предлагают шаг в сторону более общего подхода. Их идея простая и амбициозная одновременно: <strong>модель должна учиться не отдельным форматам вывода, а изменениям состояния мира</strong>. Не «какое слово дальше», не «какой пиксель дальше», а «что вообще произойдет потом».

Это звучит как философия, но статья очень практичная. Исследователи берут большую мультимодальную систему, учат ее на видео, событиях и вопросах по видео, а потом проверяют: можно ли из выученного внутреннего представления мира получить хорошие ответы в тексте, предсказание изображений и даже действия робота.

Если коротко, результат такой: <strong>да, можно</strong>. И это, пожалуй, главный сигнал статьи.

## Что такое Orca и в чем ее главная идея

Orca — это ранняя версия того, что авторы называют общей фундаментальной моделью мира. У нее есть кодировщик и декодеры. Кодировщик смотрит на сигналы из мира — пока в основном на видео и текст — и строит общее скрытое состояние. А уже потом разные декодеры «считывают» из него нужный формат: текст, изображение или действие.

[FIGURE:0]
[CAPTION:Общая схема Orca: сначала строится единое скрытое состояние мира, затем из него считываются текст, изображение и действия.]

Ключевой сдвиг здесь в том, <strong>что именно считается целью обучения</strong>. Вместо привычной специализации на одном канале модель учат предсказывать следующее состояние. Это ближе к тому, как мы сами воспринимаем мир: чашка падает — значит разобьется; робот тянется к ложке — может промахнуться, но потом скорректироваться; человек открывает коробку — содержимое изменит вид сцены.

Такая постановка важна по двум причинам.

Во-первых, она обещает единый фундамент для разных задач. Если модель действительно понимает, как меняется сцена, это пригодится и для ответа на вопрос, и для генерации будущего кадра, и для управления роботом.

Во-вторых, это путь к более устойчивому ИИ. Сегодня многие системы впечатляют, но легко ломаются вне знакомого сценария. Модель мира потенциально должна лучше переносить знания между доменами, потому что учится не шаблонам ответов, а динамике объектов, причинности и взаимодействиям.

## Как Orca учится: «бессознательно» и «сознательно»

Самая интересная часть статьи — схема обучения. Авторы делят ее на два режима: <strong>бессознательное обучение</strong> и <strong>сознательное обучение</strong>.

Бессознательное обучение — это когда модель просто смотрит на непрерывные видео и учится плотным естественным переходам состояния. Один кадр сменяет другой. Предметы двигаются. Что-то перекрывает обзор. Что-то падает, открывается, сдвигается. Здесь нет явной инструкции, что именно важно. Модель должна сама уловить физику и временную логику происходящего.

Сознательное обучение — это уже обучение при смысловом условии. Тут в дело вступает язык: описание события, намерение, вопрос по видео. Модель получает не только кадр, но и текстовую подсказку вроде «следующий шаг», «предыдущее событие» или вопрос о происходящем. Так она учится не просто видеть движение, а связывать его со смыслом и причинностью.

[FIGURE:1]
[CAPTION:Два режима обучения Orca: плотные естественные переходы из видео и осмысленные переходы при языковом условии.]

Это удачное разделение. Бессознательная часть помогает набрать «интуицию мира»: инерция, движение, контакт, скрытие объектов. Сознательная — добавляет семантику: зачем это делается, к чему ведет, что было до и что будет после.

На практике модель учат на трех задачах:

- предсказать ближайший следующий визуальный переход;
- предсказать переход, заданный событием или инструкцией;
- отвечать на вопросы по видео.

Важно, что в первых двух случаях Orca не генерирует картинку напрямую по пикселям. Она предсказывает представление следующего состояния в скрытом пространстве. Это заметно упрощает задачу и смещает фокус с «нарисуй красиво» на «пойми, что изменилось».

## На каких данных это все строится

Масштаб у работы серьезный. Для предобучения авторы собрали:

- 125 тысяч часов видео;
- 160 миллионов аннотаций событий;
- 11,5 миллиона примеров для вопросов и ответов по видео.

Но есть нюанс: в этой версии использовали только десятую часть видеоданных. То есть статья еще и намекает, что запас по масштабу у подхода большой.

[FIGURE:2]
[CAPTION:Из каких данных учится Orca: видео для естественных переходов, события для осмысленных переходов и вопросы по видео для смысловой привязки.]

Данные организованы вокруг трех источников сигнала.

Первый — обычные видео из реального мира: от взаимодействий от первого лица до манипуляций с объектами и записей роботов. Второй — событийные аннотации: видео режут на смысловые сегменты и снабжают текстовыми описаниями шагов. Третий — наборы вопросов и ответов по видео.

Это хорошая инженерная идея. Видео дает плотную временную структуру. События — грубую, но очень полезную смысловую разметку. А вопросы по видео помогают не потерять языковой интерфейс.

## Как проверяли, что модель мира действительно чему-то научилась

Самая сильная часть статьи — схема проверки. Авторы не говорят: «посмотрите, как красиво работает сквозной режим». Они делают жестче.

После предобучения <strong>кодировщик замораживают</strong>. То есть скрытое состояние мира больше не меняется. А дальше обучают только легкие декодеры под конкретные задачи: текст, изображение, действие.

Это важно. Такой протокол отвечает на честный вопрос: <strong>содержит ли само скрытое состояние полезное знание о мире?</strong> Если да, то даже маленький декодер должен суметь это знание «вытащить».

Именно это и происходит.

## Что показали результаты: лучше скрытое состояние — лучше все остальное

Авторы сначала проверяют базовую гипотезу: масштабируется ли сам подход. Ответ — да. И с ростом модели, и с ростом данных функция потерь продолжает снижаться. То есть схема обучения не упирается слишком рано в потолок.

[FIGURE:5]
[CAPTION:Чем больше модель и данные, тем лучше работают считыватели в текст, изображение и действия.]

Но куда интереснее второй вывод: <strong>по мере улучшения предобучения улучшаются все три выходных канала</strong> — текст, изображение и действие. Это и есть главный аргумент в пользу модели мира как общего основания.

В текстовых задачах Orca-4B показывает средний результат 51,8 и обходит сопоставимые по размеру модели вроде Qwen3.5-4B с 46,7. Особенно заметен выигрыш в задачах на временную динамику, причинность и здравый смысл.

Авторы дополнительно разбирают способности по категориям. Самый большой прирост — в понимании переходов состояния и динамического движения. Это хорошо ложится на саму идею работы: если модель учится переходам, она и должна быть сильнее именно там, где надо понять, как сцена меняется во времени.

В задаче предсказания изображений на реальных взаимодействиях Orca тоже смотрится убедительно. Средняя оценка на бенчмарке PRICE-V0.1 — 59,8 против 56,1 у FLUX.2. Причем авторы подчеркивают не только число, но и характер ошибок: обычные генеративные модели склонны «телепортировать» результат, дорисовывать лишние объекты или ломать позу робота. Orca лучше сохраняет контакт, геометрию сцены и причинную связность.

Для роботов результат, пожалуй, еще интереснее. В предобучении Orca вообще не видела данных с метками действий. Но когда поверх замороженного скрытого состояния обучили модуль действий, система оказалась конкурентной с сильной специализированной моделью π0.5, которую заранее учили на больших робототехнических данных.

На реальном роботе Orca выигрывает у Qwen3.5 и V-JEPA 2.1 в сложных условиях вне распределения. А в некоторых случаях почти догоняет или превосходит π0.5. Особенно любопытно, что Orca лучше восстанавливается после ошибок: если схват не удался, она чаще пробует снова и продвигается дальше по задаче.

[FIGURE:7]
[CAPTION:Пример качественного сравнения: Orca лучше предсказывает физически правдоподобный результат взаимодействия в реальной сцене.]

Это сильный момент статьи. <strong>Оказывается, если хорошо учить модель видеодинамике и смысловым переходам, это потом помогает даже в действиях робота</strong>. Для области, где размеченных робототехнических данных всегда мало и они дорогие, это очень важная мысль.

## Почему это важно не только для роботов

На первый взгляд Orca можно принять за еще одну красивую «большую мультимодальную штуку». Но здесь есть более общий смысл.

Сейчас индустрия живет в мире отдельных моделей:
- одна отвечает;
- другая генерирует;
- третья управляет;
- четвертая оценивает.

Orca предлагает собирать все это от общего основания — через внутреннюю модель изменений мира. Если такой подход полетит, он может стать мостом между LLM, генеративными моделями и embodied-системами.

Это важно и для ИИ-агентов. Любой сильный агент рано или поздно упирается в вопрос: что произойдет после моего действия? Если у него нет рабочей модели мира, он вынужден либо слепо пробовать, либо бесконечно опираться на шаблоны. Orca — это попытка положить под агента именно такой фундамент.

Еще один важный сигнал — авторы не гонятся за «красотой вывода». Они прямо говорят: цель не в том, чтобы сделать лучшую систему для рисования картинок. Цель — проверить, можно ли из единого скрытого состояния достать разные виды полезного поведения. Это здоровая исследовательская позиция.

## Где у Orca слабые места

Статья честно перечисляет ограничения, и это добавляет ей веса.

Во-первых, модальностей пока мало. В реальном мире важны звук, тактильные сигналы, усилия, проприоцепция. По видео не всегда поймешь, кипит ли вода или проскальзывает ли объект в захвате.

Во-вторых, визуальная часть все еще привязана к готовому пространству признаков уже обученной модели зрения. То есть это не совсем «нативная» модель мира с нуля. Скорее аккуратная надстройка поверх существующего мультимодального фундамента.

В-третьих, масштабы пока скромные: 0,8B и 4B. Для такой амбициозной идеи этого явно мало. Авторы сами пишут, что видят компромисс между текстом, изображением и действиями, особенно на меньшей модели.

И наконец, пока речь в основном о коротких переходах. Модель неплохо понимает, что произойдет через секунду, шаг или локальное событие. Но длинные цепочки изменений на горизонте часов или дней — это уже совсем другой уровень сложности.

## Вывод

Orca — не законченный продукт и не финальный ответ на вопрос, как строить общий ИИ. Но это <strong>очень содержательный шаг в правильную сторону</strong>.

Главная ценность статьи не в том, что очередная модель немного обошла соседей на нескольких тестах. А в том, что она аккуратно показывает: если учить систему <strong>изменениям состояния мира</strong>, а не отдельным форматам вывода, то из этого действительно можно получить выигрыш сразу в нескольких задачах.

Текст становится осмысленнее. Предсказание изображений — физически правдоподобнее. Действия робота — устойчивее.

Пока Orca — это скорее черновик будущей модели мира, чем сама такая модель в полном смысле. Но черновик очень интересный. Он показывает, что следующий большой рывок ИИ может прийти не от еще более длинного контекста и не от еще более дорогого файн-тюнинга, а от более простого и фундаментального вопроса:

<strong>понимает ли модель, как мир меняется от состояния к состоянию?</strong>

Судя по этой работе, именно здесь сейчас начинается самое интересное.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1 : The Orca’s overall framework. Orca follows an Encoder-Decoder architecture. Given multimodal world signals, the Encoder learns a world latent through two complementary paradigms: unconscious learning and conscious learning . Unconscious learning captures dense natural state transitions, while conscious learning captures sparse meaningful state transitions. To prove that the learned latent is effective, the Encoder is frozen after pre-training, and only the lightweight modality-specific decoders are trainable separately. The Decoder reads out the latent into text, images, actions, and other modalities. -->
<!-- [FIGURE:1] Figure 2 : Overview of Encoder. Orca learns a world latent representation through two learning paradigms. Unconscious learning uses video data to capture dense and natural state transitions. Conscious learning uses language instructions as explicit semantic conditions to capture sparse and meaningful state transitions. -->
<!-- [FIGURE:2] Figure 3 : Overview of pre-training data. Orca’s pre-training data includes video, event, and VQA data. A. Video Data supports 1) Observation-only state transition , A. Video Data and B. Event Data support 2) Event-conditioned state transition , and C. VQA Data supports 3) VQA response generation . -->
<!-- [FIGURE:3] Figure 4 : Downstream readout architectures. To language reuses the LM head for text readout. To vision only trains an MLP adaptor and LoRA on top of a frozen SD3.5 to readout images. To action trains an MLP adaptor and a DiT-based Action Expert from scratch. Action Expert receives the latent, robot proprioception state, and noisy action to generate action chunks. The specific settings are shown in Appendix C.2 . -->
<!-- [FIGURE:4] Figure 5 : Loss of model and data scaling. -->
<!-- [FIGURE:5] Figure 6 : Scaling behavior on downstream readouts performance. -->
<!-- [FIGURE:6] Figure 7 : Visual comparison of image prediction in the real world. -->
<!-- [FIGURE:7] Figure 8 : Recovery after repeated grasp failures. Orca recovers from early spoon-grasp failures and eventually makes progress, while π 0.5 \pi_{0.5} remains unstable with repeated failed attempts. -->
<!-- [FIGURE:8] Figure A1 : Conceptual illustration of Orca . Existing models are often organized around passive task-driven prediction, including next-token, next-frame, and next-action prediction. Orca shifts the modeling target toward next-state prediction, where multimodal world signals are used to learn a unified world latent. Unconscious learning captures dense natural dynamics from continuous observation, while conscious learning captures meaningful state transitions guided by language, events, and intentions. The learned world latent supports downstream readouts to language, vision, and action. -->
<!-- [FIGURE:9] Figure C1 : The implementation of Queries. -->
<!-- [FIGURE:10] Figure E1 : PRICE-V0.1 Examples. -->
<!-- [FIGURE:11] Figure E2 : Real-robot benchmark. We evaluate the dual-arm wheeled robot on five manipulation tasks and construct OOD settings for environment and object generalization. -->
<!-- [FIGURE:12] Figure E3 : Failure with higher intermediate progress in Stamp. Orca grasps and transports the stamp toward the ink pad before dropping it near the end, while Qwen3.5 fails to maintain a meaningful stamp grasp and remains at low progress. -->
<!-- [FIGURE:13] Figure E4 : Failure with higher intermediate progress in Pull Out Tissue. Orca reaches the tissue-grasping stage and achieves substantially higher intermediate progress, while π 0.5 \pi_{0.5} only approaches the tissue box and fails to grasp the tissue. -->
<!-- [FIGURE:14] Figure E5 : Failure with higher intermediate progress in Stacked Bowls. Orca advances through multiple bowl-stacking stages, while π 0.5 \pi_{0.5} repeatedly fails to grasp the bowl and remains at lower progress. -->
<!-- [FIGURE:15] Figure E6 : Partial recovery after spoon-grasp failure in Scoop Sugar. Orca retries after failing to grasp the spoon and recovers some lost progress, while Qwen3.5 shakes in place without effective re-grasping. -->
<!-- [FIGURE:16] Figure E7 : Recovery through repeated spoon-grasp attempts in Scoop Sugar. Orca makes multiple recovery attempts and eventually grasps the spoon successfully, while JEPA remains largely stagnant with limited task progress. -->
<!-- [FIGURE:17] Figure F1 : Cross-benchmark examples of state transition. This dimension evaluates a model’s understanding of causal temporal dynamics and physical state changes, namely its ability to predict or recognize the evolution of an object from state A to state B. The improvement is particularly evident in tasks involving irreversible physical processes. -->
<!-- [FIGURE:18] Figure F2 : More cross-benchmark examples of state transition. -->
<!-- [FIGURE:19] Figure F3 : Cross-benchmark examples of commonsense reasoning. The advantage of Orca is particularly pronounced in complex VQA scenarios that require reasoning beyond the visible scene and inferring hypothetical outcomes. -->
<!-- [FIGURE:20] Figure F4 : Cross-benchmark examples of dynamic motion. The proposed unconscious learning paradigm enables Orca to naturally acquire temporal continuity and motion inertia, leading to stronger forward simulation capabilities for dynamic object behaviors. -->
<!-- [FIGURE:21] Figure F5 : Cross-benchmark examples of spatial relations. The results demonstrate strong robustness in scenarios involving complex occlusions and multi-object spatial reasoning. -->

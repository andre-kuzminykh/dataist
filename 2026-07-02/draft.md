# Путь к более общему ИИ лежит через модель мира

## Когда модели перестанут просто болтать и начнут <strong>понимать, что происходит в мире</strong>

Последние пару лет ИИ учился очень разным фокусам. Одни модели хорошо продолжают текст. Другие дорисовывают картинку. Третьи пытаются управлять роботом. Но почти все они решают <strong>частные задачи</strong>: предсказать следующий токен, следующий кадр или следующее действие.

Авторы Orca предлагают посмотреть на проблему иначе. А что, если модели нужно учиться не “следующему слову” и не “следующему пикселю”, а <strong>следующему состоянию мира</strong>? То есть не просто угадать форму ответа, а внутренне понять: что изменится в сцене, если человек что-то сделал, объект сдвинулся, чашка упала, робот промахнулся и попробовал снова.

Звучит амбициозно. И местами даже слишком. Но работа интересна не громкими обещаниями, а тем, что в ней есть внятная инженерная ставка: собрать общую <strong>модель мира</strong>, обучить её на видео, событиях и вопросах по видео, а потом проверить, можно ли из одной и той же внутренней репрезентации “считывать” текст, изображения и действия робота.

Если коротко: идея сильная, результаты местами реально впечатляют, особенно для роботов. Но это пока именно <strong>ранний шаг</strong>, а не готовая универсальная машина понимания мира.

## В чём главная идея Orca

Вместо того чтобы строить отдельные модели под текст, видео и роботов, Orca пытается выучить единое <strong>скрытое состояние</strong> мира. Это внутреннее представление должно отвечать на простой вопрос: “что сейчас происходит и как это может измениться дальше?”

Авторы делают ставку на два режима обучения.

Первый — <strong>“бессознательное” обучение</strong>. Модель смотрит на непрерывные видео и учится предсказывать, каким будет следующее состояние сцены. Без явных подписей. Просто из потока наблюдений. Так она должна схватывать плотную, естественную динамику: движение объектов, столкновения, перекрытия, инерцию, бытовую физику.

Второй — <strong>“сознательное” обучение</strong>. Здесь к видео добавляют язык: описания событий, инструкции, вопросы и ответы. Модель учится не просто угадывать ближайшее будущее, а понимать <strong>осмысленные переходы</strong>: “до” и “после” действия, цель, намерение, причинную связь.

[FIGURE:0]
[CAPTION:Общая схема Orca: один кодировщик учит скрытое состояние мира, а отдельные лёгкие декодеры превращают его в текст, изображение или действие.]

Архитектурно всё устроено довольно аккуратно. Есть кодировщик и декодер. Кодировщик учит это единое внутреннее пространство. Дальше его <strong>замораживают</strong>, а поверх обучают лёгкие модули чтения в нужную модальность: текст, картинку или управление роботом. Это важный момент. Он нужен, чтобы показать: дело не в том, что под каждую задачу отдельно дообучили большую модель. Дело именно в качестве общего скрытого состояния.

Почему это важно? Потому что в идеале такая схема ближе к тому, как мы сами думаем о мире. У нас нет отдельного “мозга для текста” и отдельного “мозга для захвата ложки”. Есть общая картина происходящего, из которой уже рождаются слова, ожидания и действия.

## Как Orca обучали

С данными авторы размахнулись широко. Они собрали набор для “обучения миру”, который включает:

- 125 тысяч часов видео,
- 160 миллионов аннотаций событий,
- 11,5 миллиона примеров вопросов и ответов по видео.

Правда, в этой версии использовали только десятую часть видеоданных. Уже само это говорит, что авторы думают о проекте как о долгой линии, а не о разовом эксперименте.

[FIGURE:2]
[CAPTION:Какие данные использует Orca: непрерывное видео для естественных переходов, события с текстом для осмысленных изменений и VQA для семантики и здравого смысла.]

Предобучение строится на трёх задачах.

Первая — предсказать следующее состояние по текущему кадру. Это и есть “бессознательная” часть.

Вторая — предсказать состояние, заданное через событие или инструкцию. Например, модель видит сцену и текстовое условие, которое указывает на предыдущее или следующее значимое событие. Это уже “сознательная” часть.

Третья — отвечать на вопросы по видео. Это нужно, чтобы в скрытое состояние лучше встраивались язык, семантика и бытовой здравый смысл.

Любопытно, что Orca не учат восстанавливать пиксели напрямую. Она предсказывает представление следующего состояния в пространстве визуального кодировщика. То есть ставка не на красивую картинку как таковую, а на <strong>смысловую динамику сцены</strong>.

После этого кодировщик замораживают. И отдельно обучают три выхода:

- в текст — через уже имеющуюся языковую голову;
- в изображение — через лёгкий адаптер и замороженную генеративную модель изображений;
- в действия — через отдельный модуль для управления роботом.

Это хороший дизайн для проверки гипотезы. Если при замороженном “ядре” качество в трёх разных задачах растёт, значит внутренняя репрезентация и правда несёт полезную информацию о мире.

## Что получилось: главный тезис работы подтверждается

Первая важная проверка — масштабируемость. Если идея правильная, потери при обучении должны снижаться с ростом модели и данных. Так и происходит.

[FIGURE:5]
[CAPTION:Чем больше модель и данных, тем лучше работают декодеры: улучшаются текст, предсказание изображений и действия робота.]

Но гораздо интереснее вторая проверка: помогает ли более сильная модель мира в прикладных задачах? Здесь ответ тоже положительный. По мере роста предобучения улучшаются все три считывания — текст, изображение и действия.

Это, пожалуй, самый важный результат статьи. Он показывает, что авторы не просто обучили очередную видеомодель, а действительно получили <strong>общее внутреннее представление</strong>, которое переносится между задачами.

Особенно интересно, что выигрыш есть и в робототехнике, хотя на этапе предобучения модель не видела размеченных действий. Для области, где данных с реальных роботов всегда мало и они дорогие, это очень сильный сигнал: возможно, часть навыков можно выращивать из обычного видео, если модель умеет понимать переходы состояний.

## Текст: Orca лучше понимает изменения, причинность и движение

В текстовых тестах Orca проверяли на четырёх бенчмарках, связанных с пониманием видео, временной динамикой, пространственными отношениями и причинными вопросами.

Результат у Orca-4B сильный: в среднем она обходит сопоставимые по размеру модели и некоторые специализированные подходы. Особенно заметен прирост в задачах, где важно не просто распознать объект, а понять <strong>как сцена меняется во времени</strong>.

Авторы отдельно разбили качество по четырём большим категориям:

- переходы состояний,
- рассуждение на основе здравого смысла,
- пространственные отношения,
- динамика движения.

Там Orca особенно хорошо выглядит именно в переходах состояний и динамике. Это логично: если ты учился по видео и событиям, то должен лучше схватывать, что из чего следует.

Важно, что здесь не заявляется магия уровня “всё понимает лучше всех”. В пространственных задачах отрыв уже небольшой. Но общая картина ясна: ставка на предсказание следующего состояния действительно помогает в тех вопросах, где нужно мыслить во времени, а не просто смотреть на один кадр.

## Изображения: не “красивее”, а <strong>физичнее</strong>

Часть про изображения, пожалуй, самая необычная. Авторы не хотят соревноваться в художественной генерации. Их интересует другое: может ли скрытое состояние Orca помочь предсказать, <strong>как изменится реальная сцена после действия</strong>.

Для этого они сделали собственный бенчмарк реальных взаимодействий. На вход подаются исходное изображение и инструкция. На выходе нужно получить картинку результата. Причём оценивается не красота, а соответствие действию, сохранение сцены и физическая правдоподобность.

Здесь Orca-4B показывает лучший средний результат среди сравниваемых моделей. По описанию и примерам видно, где именно преимущество: меньше “телепортации” объектов, меньше лишних предметов из воздуха, лучше сохраняется поза робота, связи контакта и логика сцены.

[FIGURE:6]
[CAPTION:Сравнение предсказания изображений в реальных сценах: Orca лучше сохраняет структуру сцены, объекты и правдоподобные изменения после действия.]

Это тонкий, но важный сдвиг. Обычно генеративные модели изображений очень хороши в визуальном правдоподобии, но могут быть плохи в <strong>причинной правдоподобности</strong>. То есть картинка красивая, но непонятно, как мир до такого состояния дошёл. Orca, судя по результатам, лучше держится за причинную нить.

## Роботы: самая сильная часть статьи

Самая живая и убедительная часть работы — эксперименты на реальном двухруком роботе. Пять задач. Два жёстких режима обобщения: новые окружения и новые объекты. Для дообучения всего по 200 траекторий на задачу. Это мало.

И вот здесь Orca показывает, что идея модели мира может быть полезна не только в тестах на понимание, но и в физическом действии. В среднем она заметно обходит Qwen3.5 с тем же модулем действий и оказывается сопоставима, а местами лучше сильной специализированной робототехнической модели π0.5, которая предобучалась на больших робототехнических данных.

[FIGURE:7]
[CAPTION:Orca лучше восстанавливается после неудачных захватов: робот не застывает, а пробует ещё раз и продвигается по задаче.]

Самое интересное тут даже не сухая успешность. Авторы смотрят на <strong>промежуточный прогресс</strong> и способность восстанавливаться после ошибок. И Orca выглядит сильнее именно как система, которая “понимает, что пошло не так” и пытается вернуться в рабочее состояние. Например, если робот неудачно схватил ложку, Orca чаще делает повторные осмысленные попытки, а не зависает.

Это очень хороший признак. В реальном мире провалы случаются постоянно. Робот, который просто следует шаблону, ломается от первого отклонения. Робот, у которого есть хотя бы грубая модель состояния мира, может заметить, что цель не достигнута, и скорректироваться.

## Что в работе особенно ценно

У статьи есть несколько по-настоящему сильных сторон.

Во-первых, <strong>правильная постановка задачи</strong>. Переход от “следующего токена” к “следующему состоянию” — не просто маркетинг. Это полезная рамка, если мы хотим систем, которые понимают мир, а не только имитируют ответы.

Во-вторых, <strong>проверка одной идеи сразу в трёх каналах</strong>: текст, изображения, действия. Это делает работу гораздо убедительнее.

В-третьих, <strong>хорошая методическая честность</strong>. Авторы замораживают ядро и обучают только лёгкие выходы. Это снижает риск, что успех объясняется просто большим числом обучаемых параметров в конкретной задаче.

В-четвёртых, <strong>акцент на реальном мире</strong>. Не на синтетике, не на красивой генерации, а на сценах, где есть объекты, контакт, ошибка, повторная попытка.

## Где слабые места и почему до “универсального мира” ещё далеко

При всей силе идеи, статья честно показывает и свои ограничения.

Первое: Orca пока в основном живёт в зрении и языке. А реальный мир — это ещё звук, тактильность, сила, температура, собственное состояние тела. Без этого модель мира остаётся неполной.

Второе: модель учится предсказывать состояние не напрямую, а в пространстве уже готового визуального кодировщика. Это удобно инженерно, но значит, что “мир” частично наследует ограничения чужого визуального пространства.

Третье: масштаб пока умеренный — 0.8B и 4B. Для настолько амбициозной идеи этого явно мало. Авторы сами пишут, что между текстом, изображением и действием у небольшой модели возникает компромисс.

Четвёртое: горизонт предсказания короткий. Orca хорошо учится локальным переходам состояния, но это ещё не модель длительных процессов на часы или дни.

И наконец, часть оценок, особенно в изображениях, всё ещё довольно сырая. Собственный бенчмарк — это хорошо, но его ещё нужно обкатать сообществом.

## Вывод

Orca — это не “ещё одна LLM с видео”. И не просто очередная робототехническая модель. Это попытка переопределить сам объект обучения: вместо слов, кадров и действий — <strong>состояния мира и их переходы</strong>.

Получилось не всё. До общей модели мира здесь огромная дистанция. Но работа уже даёт важный практический вывод: если учить систему на естественной динамике видео, осмысленных событиях и языковых условиях, можно получить внутреннее представление, которое полезно сразу для нескольких разных задач.

Главная ценность Orca в том, что она возвращает разговор об ИИ к более фундаментальному вопросу: <strong>понимает ли модель, как мир меняется</strong>. И вот на этот вопрос статья впервые даёт не философский, а вполне инженерный ответ.

Пока осторожный. Но уже очень интересный.

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

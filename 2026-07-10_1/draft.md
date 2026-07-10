# Как заставить ИИ-судью меньше ошибаться в сложных агентных задачах

## Когда LLM учится не только отвечать, но и проверять

У больших языковых моделей есть странная слабость. Они все лучше <strong>генерируют</strong> решения, но все еще не очень хорошо <strong>понимают, какое из решений действительно правильное</strong>. А это уже не мелочь. Если у вас ИИ-агент пишет код, ходит по терминалу, управляет манипулятором или работает с медицинскими данными, то главный вопрос не «может ли он выдать вариант?», а «можем ли мы надежно выбрать хороший вариант среди нескольких?».

Именно на этом построена статья <strong>LLM-as-a-Verifier</strong> от исследователей из Стэнфорда, Беркли и NVIDIA Research. Авторы предлагают смотреть на проверку не как на вспомогательную функцию, а как на <strong>отдельную ось масштабирования</strong>. То есть модели можно улучшать не только за счет предобучения, дообучения и большего бюджета на инференс, но и за счет более умной верификации.

Звучит просто. Но за этим стоит важная идея: если модель умеет неплохо проверять, то она может лучше выбирать среди собственных попыток. А значит, качество системы растет даже без дополнительного обучения.

## В чем проблема обычных ИИ-судей

Сегодня популярный подход такой: мы просим LLM выступить «судьей» и поставить решению оценку. Например, от 1 до 5 или от 1 до 10. Потом берем лучший вариант.

Проблема в том, что это слишком грубо. Если два решения оба «почти правильные», модель часто выдает им одну и ту же оценку. Возникают ничьи. А когда задача длинная и сложная — например, агент 20 шагов правил код, устанавливал пакеты, запускал тесты и исправлял ошибки, — грубая шкала начинает ломаться.

Авторы предлагают перейти от идеи «судьи» к идее <strong>верификатора</strong>. Судья выносит итоговый вердикт. Верификатор пытается аккуратно оценить, <strong>насколько</strong> решение похоже на правильное и где в нем есть признаки успеха или провала.

Ключевой ход здесь очень изящный. Вместо того чтобы брать один самый вероятный токен оценки, авторы смотрят на <strong>все распределение вероятностей</strong> по токенам оценки и считают ожидаемое значение. Иначе говоря, модель не просто говорит «это 4 из 5», а показывает более плавный сигнал: что-то вроде «это 4.37».

Это сразу дает более тонкое разделение кандидатов.

[FIGURE:1]
[CAPTION:Одна схема для разных модальностей: верификатор дает тонкую обратную связь для кода, видео, медицины и обучения с подкреплением.]

## Что именно предлагают авторы

Их схема называется <strong>LLM-as-a-Verifier</strong>. Она не требует дополнительного обучения. Это важно. Авторы не обучают отдельную модель награды под каждую область, а используют уже готовую LLM или зрительно-языковую модель как универсальный проверяющий модуль.

Метод держится на трех идеях.

Первая — <strong>более мелкая шкала оценок</strong>. Не 1–5, а до 20 уровней. Причем важно не только число уровней, но и то, что используется распределение вероятностей по ним.

Вторая — <strong>повторная проверка</strong>. Один прогон может быть шумным. Несколько независимых оценок снижают разброс.

Третья — <strong>разложение критериев</strong>. Вместо одного вопроса «это правильно?» модель отдельно смотрит, например:
- выполнены ли требования задачи;
- корректен ли итоговый результат;
- есть ли явные ошибки в журналах и действиях.

Это похоже на здравый человеческий процесс проверки. Когда мы оцениваем сложную работу, мы ведь тоже не ставим балл «на глаз». Мы раскладываем ее на части.

[FIGURE:3]
[CAPTION:Точность верификации растет сразу по трем направлениям: более мелкая шкала оценок, повторные проверки и разложение критериев.]

Результат выглядит убедительно. На Terminal-Bench V2 точность попарного сравнения выросла:
- с 73.1% до 77.5% при увеличении «зернистости» оценки;
- с 74.7% до 77.5% при увеличении числа повторных проверок;
- до 78.3% при ансамбле из трех критериев.

Это не косметическое улучшение. В задачах выбора лучшей траектории даже несколько процентов сверху — очень много.

## Почему это важно на практике

Главный посыл статьи такой: <strong>у многих моделей уже есть скрытый запас качества</strong>. Они часто могут решить задачу хотя бы в одной из нескольких попыток. Но системе не хватает хорошего механизма, чтобы эту удачную попытку распознать и выбрать.

Авторы показывают это на Terminal-Bench. Если бы существовал идеальный «оракул», который всегда выбирает лучший ответ из набора кандидатов, то точность доходила бы почти до 99%. Это огромный запас. Значит, проблема часто не в генерации как таковой, а в выборе.

Чтобы сделать выбор не слишком дорогим, авторы добавляют еще один компонент — алгоритм ранжирования кандидатов с ограниченным бюджетом проверок. Он называется <strong>вероятностный турнир с опорными кандидатами</strong>. Идея простая: не сравнивать все со всеми, что дорого, а сначала быстро отобрать сильных кандидатов, а потом тратить основной бюджет на сравнение вокруг лидеров. Это снижает стоимость с квадратичной до почти линейной по числу кандидатов с небольшим множителем.

[FIGURE:5]
[CAPTION:Схема вероятностного турнира: как выбрать лучший вариант из многих, не сравнивая все пары напрямую.]

Для ИИ-агентов это особенно важно. Агент для программирования, как правило, может сделать несколько заходов к одной задаче. Если у вас есть надежный верификатор, система начинает работать в режиме «сгенерируй несколько решений и умно выбери лучшее». Это очень практичный путь к росту качества.

## Результаты: код, робототехника, медицина

Самое сильное место статьи — широта экспериментов. Авторы не ограничились одним бенчмарком и одной областью. Они проверили метод на коде, видео из задач робототехники и медицинских сценариях.

Итоговые числа такие:
- Terminal-Bench V2 — <strong>86.5%</strong>;
- SWE-Bench Verified — <strong>78.2%</strong>;
- RoboRewardBench — <strong>87.4%</strong>;
- MedAgentBench — <strong>73.3%</strong>.

[FIGURE:0]
[CAPTION:Итоговые результаты: метод показывает лучший на данный момент результат сразу в программировании, робототехнике и медицинских задачах.]

Особенно показателен пример с RoboRewardBench. Там нужно понять, какая из двух видеотраекторий робота лучше продвигается к цели. То есть модель должна по кадрам понять физический прогресс задачи. И здесь предложенный подход обходит не только обычного LLM-судью, но и специализированные модели награды, обученные именно на данных из робототехники.

Это важный момент. Мы привыкли думать, что без узкоспециального обучения в такой области никуда. Авторы показывают, что сильный универсальный верификатор иногда может оказаться даже лучше.

## Не только выбор ответа, но и отслеживание прогресса

Еще одна интересная часть статьи — идея использовать сигнал верификатора как <strong>оценку прогресса</strong> по ходу длинной траектории.

Если агент решает задачу шаг за шагом, можно подавать верификатору не только финальный результат, но и промежуточные префиксы траектории. Тогда мы видим: движется ли агент к цели или блуждает.

Авторы показывают красивый пример с задачей по запуску инференса для MNIST. Успешная траектория идет по понятной цепочке шагов, и оценки верификатора постепенно растут. Неудачная — сворачивает не туда, устанавливает лишние пакеты, упирается в нехватку места на диске, и ее оценки заметно ниже.

[FIGURE:7]
[CAPTION:Оценка верификатора растет по мере движения успешной траектории и помогает отличать прогресс от блуждания.]

Это уже не просто инструмент выбора «лучшего из пяти ответов». Это почти приборная панель для ИИ-агента. Можно наблюдать, когда он реально продвигается, а когда застрял. Для долгих запусков агента для программирования такая штука может быть очень полезной: остановить процесс раньше, откатить неудачные действия, переключиться на другой вариант.

## Польза для обучения с подкреплением

Самый неожиданный кусок работы — применение верификатора в обучении с подкреплением.

В таких задачах одна из вечных проблем — <strong>разреженная награда</strong>. Агент часто узнает, что он молодец, только в самом конце. А как понять, какие именно шаги помогли к успеху? Это тяжело.

Авторы используют сигнал верификатора как <strong>плотную награду</strong>. То есть не только «успех/провал», а более плавную оценку прогресса на промежуточных этапах.

В экспериментах это ускорило обучение:
- в задаче из робототехники на LIBERO — примерно в <strong>1.8 раза</strong> по эффективности использования примеров;
- на математическом бенчмарке с GRPO — примерно в <strong>1.1 раза</strong>.

[FIGURE:8]
[CAPTION:Плотная награда от верификатора ускоряет обучение с подкреплением и помогает раньше выходить на тот же уровень качества.]

Это не выглядит как магический скачок, но выглядит как очень практичная вещь. Если вы можете без отдельного обучения получить осмысленный сигнал прогресса, то это серьезно удешевляет настройку систем.

## Где у подхода слабые места

Работа сильная, но не без ограничений.

Во-первых, методу удобно, когда модель отдает логарифмы вероятностей токенов. А многие закрытые API этого не делают. Авторы предлагают обходной путь: одна модель пишет рассуждение, а другая, более открытая, превращает его в непрерывную оценку. Это рабочий костыль, но все же костыль.

Во-вторых, критерии проверки здесь часто задаются вручную. Для кода это еще нормально: требования, вывод, ошибки. Но для новых областей придется продумывать такие разложения отдельно. Напрашивается следующий шаг: чтобы сама модель умела строить критерии динамически.

В-третьих, повторные проверки и более тонкая шкала улучшают ситуацию, но не убирают систематические смещения модели. Если верификатор в каком-то типе задач рассуждает неверно, простое усреднение не спасет.

И все же эти ограничения не портят главный вывод статьи.

## Вывод

Статья предлагает очень своевременный сдвиг оптики. Мы привыкли обсуждать, как сделать генерацию сильнее. Авторы напоминают: <strong>не менее важно научить систему хорошо проверять</strong>.

И это не философия, а рабочая инженерная идея. Вместо грубого «судьи» — вероятностный верификатор с непрерывной оценкой. Вместо одной оценки — масштабирование по трем осям: зернистость, повторение, критерии. Вместо дорогого полного турнира — более экономный отбор лучших кандидатов.

Главное, что все это уже дает практический эффект: лучшее качество в задачах программирования, в робототехнике, в медицине и даже более эффективное обучение с подкреплением.

Если коротко, то мысль статьи такая: <strong>следующий прирост качества ИИ-агентов может прийти не только от того, как они думают, но и от того, как они себя проверяют</strong>. И похоже, это одна из самых полезных идей для систем, которые должны не просто красиво говорить, а надежно действовать.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1 : Overall Performance Results. Our proposed framework, LLM-as-a-Verifier , achieves state-of-the-art performance across coding, robotics, and medical domains: Terminal-Bench V2 (86.5%), SWE-Bench Verified (78.2%), RoboRewardBench (87.4%), and MedAgentBench (73.3%). -->
<!-- [FIGURE:1] Figure 2 : Multiple modalities, many applications, one unified verification framework. We present LLM-as-a-Verifier, a general-purpose framework that provides fine-grained feedback for any modality without requiring additional training. By leveraging the full distribution of scoring-token logits, our method captures evaluation uncertainty and enables verification to scale along three dimensions: score granularity, repeated evaluation, and criteria decomposition. The resulting fine-grained feedback can be used for test-time scaling, progress tracking, and reinforcement learning. -->
<!-- [FIGURE:2] Figure 3 : Scaling paradigms for large language models. -->
<!-- [FIGURE:3] Figure 4 : Verification Scaling. We find that verification accuracy consistently improves as we scale across multiple dimensions: (1) the granularity of score tokens, (2) the number of repeated evaluations, and (3) the decomposition of evaluation criteria. Verification accuracy is measured as the pairwise accuracy of the verifier in assigning a higher score to the ground-truth successful solution than to failed solutions for the same task on Terminal-Bench V2. -->
<!-- [FIGURE:4] Figure 5 : Oracle Pass@ K K reaches 98.9% on Terminal-Bench V2. -->
<!-- [FIGURE:5] Figure 6 : Probabilistic Pivot Tournament. A five-stage pipeline for selecting the best of N N candidates under a constrained verification budget. (1) Candidates: the pool { τ 1 , … , τ N } \{\tau_{1},\dots,\tau_{N}\} to be ranked. (2) Ring pass: a random Hamiltonian cycle scores the N N adjacent pairs so every candidate appears once in the “A” slot and once in “B”, canceling the model’s positional bias. (3) Pivot selection: candidates are ranked by their ring-pass scores w ( i ) w_{(i)} , and the top- k k candidates form the pivot set 𝒫 \mathcal{P} . (4) Pivot tournament: every non-pivot–vs–pivot and pivot–vs–pivot pair is scored via Eq. 3.2 , concentrating the budget on uncertain top candidates and cutting cost from 𝒪 ​ ( N 2 ) \mathcal{O}(N^{2}) to 𝒪 ​ ( N ​ k ) \mathcal{O}(Nk) . (5) Selection: comparisons are aggregated into win mass w i w_{i} and count c i c_{i} , and the candidate with the highest normalized w i / c i w_{i}/c_{i} is returned. -->
<!-- [FIGURE:6] Figure 7 : Verifier (continuous) vs. Judge (discrete) on Terminal-Bench V2 across k ∈ { 1 , 4 , 16 } k\in\{1,4,16\} repeated evaluations. Left: Pairwise verification accuracy. The verifier achieves 74.7 % 74.7\% at k = 1 k{=}1 and improves to 77.5 % 77.5\% at k = 16 k{=}16 , consistently outperforming the judge across all evaluation budgets. Right: Tie rate. The judge produces ties in 26.7 % 26.7\% of comparisons at k = 1 k{=}1 due to coarse discrete scoring, decreasing to 5.5 % 5.5\% at k = 16 k{=}16 as averaging breaks ties. In contrast, the verifier yields zero ties. -->
<!-- [FIGURE:7] Figure 8 : We observe a strong correlation between the chronological progression of code generation steps and the scores from LLM-as-a-Verifier. The example task above requires the agent to run MNIST inference. The successful trajectory follows a coherent sequence of events— Read model.py → \rightarrow Install g++ compiler → \rightarrow Install CPU-only torch → \rightarrow Update hidden_dim → \rightarrow DONE and exhibits consistently increasing verifier scores. In contrast, the failed trajectory is characterized by erroneous behaviors—it unnecessarily installs the large torchvision package, which exhausts the available disk space and hits a compilation error—resulting in significantly lower scores. Results are shown for the pytorch-model-cli task from Terminal-Bench V2, using Gemini 2.5 Pro with Terminus 2 and Gemini 2.5 Flash as the verifier. -->
<!-- [FIGURE:8] Figure 9 : LLM-as-a-Verifier improves RL sample efficiency. Success rate versus training steps for off-policy (left) and on-policy (right) reinforcement learning, comparing sparse-reward baselines with dense rewards from LLM-as-a-Verifier. Left: A π 0 \pi_{0} policy fine-tuned on the LIBERO ketchup task with DSRL-SAC. The verifier progress reward (Eq. 7.1 ) achieves the same success rate using ≈ 1.8 × \approx 1.8\times fewer environment steps and reaches a higher final success rate ( 0.76 0.76 vs. 0.69 0.69 ). Right: Qwen3-8B fine-tuned on MATH with GRPO. The verifier reasoning reward (Eq. 7.2 ) improves sample efficiency by ≈ 1.1 × \approx 1.1\times . Results are averaged over multiple seeds (LIBERO n = 5 n{=}5 , MATH n = 3 n{=}3 ). -->
<!-- [FIGURE:9] Figure 10 : Trajectory-preference accuracy improves consistently as the number of repeated evaluations k k increases, rising from 81.5 % 81.5\% at k = 1 k{=}1 to 87.4 % 87.4\% at k = 8 k{=}8 . LLM-as-a-Verifier outperforms LLM-as-a-Judge and prior reward models (TOPReward, RoboReward-8B, Robometer-4B) across all budgets, with gains saturating at larger k k . -->

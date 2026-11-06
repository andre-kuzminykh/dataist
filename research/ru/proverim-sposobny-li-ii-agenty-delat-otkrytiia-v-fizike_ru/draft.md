# Проверим, способны ли ИИ-агенты делать открытия в физике

## Физика — это не только формулы

Решить задачу по физике — ещё не значит провести исследование. Для настоящей работы нужно найти важные статьи, понять, какие вопросы пока открыты, выбрать метод, проверить расчёты и объяснить, что показывают результаты. Теперь ИИ-агентов учат справляться со всем этим. Но как проверить, способны ли они проводить исследования, а не только отвечать и создавать аккуратные демки?

Авторы **FrontierPhysics** собрали бенчмарк из 56 исследовательских задач, созданных физиками на основе собственной работы. Агентам нужно пройти путь от изучения литературы до научной статьи и результатов, которые можно проверить программно. В испытаниях участвовали 22 модели. Лучший результат — 27,4% успешных попыток.

Модели часто знают нужную физику и умеют запускать расчёты. Но им не хватает строгой проверки собственных выводов и опыта, который помогает исследователю понять, что важно в конкретной ситуации.

## Задачи из настоящих исследований

Обычные физические бенчмарки обычно задают чёткий вопрос с известным ответом. Это удобно для проверки знаний и вычислений, но мало говорит о том, справится ли модель с исследованием, где сначала нужно разобраться, что именно проверять.

В FrontierPhysics задача начинается с общего описания проекта — примерно такого, какое руководитель лаборатории мог бы дать новому сотруднику. Агенту не указывают готовую методику. Ему нужно изучить тему, составить план, провести расчёты или экспериментальную работу, а затем представить результаты.

Каждая задача требует двух видов результата. Первый — **проверяемые данные**: например, вычисленные величины, результаты моделирования или обработанные измерения. Второй — научная рукопись с описанием контекста, метода, результатов и выводов. Получить правильные числа недостаточно: в статье нужно показать, откуда они взялись и какие выводы позволяют сделать.

Задачи охватывают девять областей физики — от физики конденсированного состояния до астрофизики. Их предложили 42 исследователя, а к бенчмарку допустили 56 задач из 182 заявок. Перед этим каждую задачу проверяли на ясность, физическую обоснованность и соответствие реальной исследовательской работе. Авторы также просили показать, что исходный проект требовал не меньше двух недель работы. По их оценкам, создание проектов, на которых основан бенчмарк, заняло в сумме более 8 000 часов.

[FIGURE:2]
[CAPTION:Как устроен FrontierPhysics: физики составляют и проверяют задачи, агенты проводят исследования, а результаты оценивают автоматические тесты и экспертные критерии.]

## Как оценивают исследование

Авторы используют две независимые проверки. Первая — **автоматическая проверка**. Она сравнивает численные результаты агента с контрольными значениями и позволяет установить, верны ли расчёты.

Вторая проверка оценивает ход работы и качество статьи. Для неё применяют критерии, составленные авторами задач. Они могут проверять, нашёл ли агент нужные научные работы, учёл ли реальные ограничения оборудования, обосновал ли выбранный метод и подтвердил ли выводы данными.

Критерии делятся на обязательные и дополнительные. Обязательные работают как пропускные пункты: агент должен пройти их все. К ним добавляется успешная автоматическая проверка. Если одно из этих условий не выполнено, работа не считается успешной, даже если отдельные части статьи выглядят убедительно. Дополнительные критерии оценивают качество исследования: например, насколько хорошо агент объясняет метод или связывает результаты с предыдущими работами.

Такое разделение помогает отличить две ситуации. Агент может получить правильный численный ответ, но написать слабую статью, которая не объясняет, почему результат важен. Или создать стройный текст, в котором расчёты не подтверждают выводы. В первом случае работа недостаточно убедительна, во втором — научно неверна.

[FIGURE:6]
[CAPTION:Разбор неудачных попыток GPT-6 Astra показывает, что чаще всего агентам мешали слабая проверка рассуждений, нехватка исследовательской интуиции и проблемы с научной литературой.]

## Результаты: правильных чисел мало

В испытаниях сравнили 22 модели в 26 вариантах работы. Каждая выполняла все 56 задач по три раза. Передовые модели работали в разных программных обвязках, которые дают агентам доступ к инструментам и позволяют выполнять работу по шагам.

На первом месте оказался Claude Opus 5.5: он прошёл 27,4% попыток, то есть 46 из 168. Следом шли GPT-6 Astra с результатом 23,2% в стандартной настройке и GPT-6.1 Sol — 19,6%. Ни одна конфигурация не справилась даже с третью всех попыток. Эти цифры показывают, насколько велика разница между решением отдельных задач и полноценным исследованием.

Итоговый процент не объясняет, где именно агенты ошибаются. Поэтому авторы отдельно разобрали 168 попыток GPT-6 Astra. В этой проверке чаще всего встречались три проблемы:

🔎 **Недостаточно строгая проверка.** Агент может проверить результат способом, который опирается на его же неверное предположение. Такая проверка не обнаружит ошибку. Другой типичный сбой — пропущенные редкие случаи, из-за которых метод работает на части данных, но проваливает скрытые тесты.

🧭 **Нехватка экспертной интуиции.** Агент понимает физические законы, но не всегда знает, какой механизм стоит проверить первым. В одной задаче он, например, мог не учесть распад возбуждённых состояний как источник экспериментальной ошибки.

📚 **Проблемы с научной литературой.** Агент не находит ключевую работу, с трудом связывает источники между собой или не использует их для обоснования выводов.

В разборе 48% попыток отметили недостаток строгой проверки, 34% — нехватку экспертной интуиции, а 27% — проблемы с литературой. Метки могли пересекаться: одна попытка могла провалиться сразу по нескольким причинам. Следование инструкциям тоже оказалось трудностью: его отметили в 26% неудач.

Особенно показателен разрыв между физическими расчётами и исследовательским выводом. Агент может правильно посчитать величину, но не объяснить, почему результат важен, пропустить ограничение метода или не заметить, что расчёт сам по себе не проверяет нужное предположение. **Умение считать и умение исследовать — разные способности.**

## Проверка проверяющих

Когда результат зависит от автоматических тестов и критериев оценки, ошибиться может не только агент. Проверяющий способен отклонить корректное решение из-за слишком строгого допуска, двусмысленной инструкции или неверной оценки статьи.

Авторы специально проверяли такие случаи. Физики просматривали ход работы агентов и сопоставляли решения с результатами автоматических и экспертных проверок. В девяти из 168 попыток GPT-6 Astra нашли ошибочные оценки: восемь раз агент выдал правильный результат, но получил отказ из-за недочёта задачи или проверки; ещё один раз ошибся оценивающий агент.

После исправления этих оценок доля успешных попыток GPT-6 Astra выросла с 14,9% до 20,2%. Это заметная разница. Она показывает, почему в открытых научных задачах важны не только точные тесты, но и проверка самих способов оценки.

Команда также проверила критерии на рукописях авторов задач. Для 33 задач использовали исходные научные материалы, когда они были доступны. В среднем те получили 96,2% по применимым критериям. Такая проверка не гарантирует, что все оценки верны, но помогает убедиться, что критерии признают качественную работу исследователей.

## Вывод

FrontierPhysics проверяет, способны ли ИИ-агенты пройти весь путь от изучения литературы до проверяемых результатов и научной статьи. Пока это удаётся редко: лучший результат составил 27,4% успешных попыток.

По разбору авторов, агенты чаще проваливают задачи из-за недостаточно строгой проверки выводов, нехватки экспертной интуиции и слабого обзора литературы, чем из-за незнания физических законов или ошибок при расчётах. Для научной работы недостаточно дать модели больше инструментов или увеличить вычислительный бюджет. Агенту нужно уметь проверять собственные предположения, связывать результаты с предыдущими исследованиями и понимать, какие ограничения имеют значение.

Бенчмарк пока не измеряет способность самостоятельно выбирать совершенно новую научную проблему и находить неожиданные открытия. Но он позволяет проверить, может ли агент не просто получить ответ, а **обосновать, что этот ответ заслуживает доверия**.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1: FrontierPhysics leaderboard. Overall pass rate (Pass@1) under the Table 2 configurations; a pass requires passing all verifier tests and blocker rubrics. Harnesses and inference level: GPT (Codex, max), Claude (Claude Code, max), Grok (Grok Build, xhigh), Gemini (Antigravity, high), Kimi (Claude Code, max), DeepSeek (Claude Code, max), MiMo (Claude Code, max), GLM (Claude Code, max), Mistral (Claude Code, max). Error bars show approximate 95% confidence intervals. -->
<!-- [FIGURE:1] Figure 2: Overview of FrontierPhysics . (1) Physicists build tasks from their own research. (2) An admin team of physicists accepts those passing both reviews. (3) 4,364 rollouts cover 22 models and 4 harnesses, each is one trial of a task by a model in an agent harness. (4) A deterministic verifier and a reviewer agent with the task’s rubric grade each rollout (Eq. 1 ). (5) The admin team and contributors manually analyze failure modes of the 168 GPT-6 Astra rollouts (Fig. 6 , Table 4 ). -->
<!-- [FIGURE:2] Figure 3: (a), FrontierPhysics tasks QA pipeline. (b), FrontierPhysics tasks structure, shown for the example task rydberg-ising-critical-point . (c), How to run a task rollout. -->
<!-- [FIGURE:3] Figure 4: Task composition and overall pass rate (%) by primary physics domain across all 56 tasks. Donut labels give task shares. n n gives task counts. -->
<!-- [FIGURE:4] Figure 6: Failure mode analysis of GPT-6 Astra xhigh across 56 tasks (3 rollouts for each task). Counts n n and percentages ( n / 143 n/143 ) use the final review labels in Table 5 . Each rollout may have multiple tags. Verifier/rubric proportions are retained from the original recorded assessment. Correcting the eight FALSE and one RRMIS outcomes changes the pass rate from 14.9% (25/168) to 20.2% (34/168). -->
<!-- [FIGURE:5] Figure 7: Deterministic and overall pass rates (Pass@1, %) of the models in Fig. FrontierPhysics: Evaluating Agents for End-to-End Physics Research . Column height: deterministic pass rate (all verifier tests pass). Solid part: overall pass rate (blocker rubrics also pass). Error bars: approximate 95% confidence intervals (dot: deterministic; circle: overall). -->
<!-- [FIGURE:6] Figure 8: Example task. rydberg-ising-critical-point , the example of Table 4 . Left: its task.md . The cited proposal (Figure 9 ) defines σ mid \sigma_{\mathrm{mid}} as the order parameter on the central bond; the device simulates a Rydberg apparatus of at most three atoms. The tests that check each step in task.md ( ± \pm : tolerance around withheld reference values) and the summarized rubric criteria that grade it. -->
<!-- [FIGURE:7] Figure 9: The proposal of the example task. Top: proposal.pdf , the one-page brief that agent need to read first. It sets out the physics and the goal, and describe what are the questions should be answered after literature research. The last paragraph leaves four questions to the agent’s own research (numbered). Bottom: for each question, what the literature must supply. -->
<!-- [FIGURE:8] Figure 10: Input modalities and required research activities across the 56 accepted tasks. Each bar gives the percentage of tasks carrying that label. Modality and activity categories are non-exclusive: a single task can contribute to multiple categories, so the percentages within each panel need not sum to 100%. -->
<!-- [FIGURE:9] Figure 11: Verifier pass rate per task and model. The bottom row is each model’s deterministic Pass@1 over all 56 tasks (Table 2 ). Unavailable outcomes contribute zero to the aggregate. -->
<!-- [FIGURE:10] Figure 12: Rubric blocker pass rate per task and model. The bottom row is each model’s mean over all 56 tasks. Unavailable outcomes contribute zero to the aggregate. -->
<!-- [FIGURE:11] Figure 13: Rubric score per task and model. The weighted non-blocker score (Equation 1 ) before the verifier and blocker gates, averaged over three rollouts. The bottom row is each model’s mean over all 56 tasks. -->
<!-- [FIGURE:12] Figure 14: Score (Equation 1 ) per task and model. The bottom row reproduces Score in Table 2 . Rows follow Figure 11 . Missing rollouts count as zero. -->
<!-- [FIGURE:13] Figure 15: Mean agent steps per rollout versus overall pass rate (%). Steps count recorded tool invocations, including failed and interrupted calls. -->
<!-- [FIGURE:14] Figure 16: Mean reported output tokens per rollout, in thousands, versus overall pass rate (%). Token counts follow provider or harness usage accounting. -->
<!-- [FIGURE:15] Figure 17: Agent execution time per rollout, in hours, per task and model: the mean over the recorded rollouts in each cell. The bottom row gives each model’s mean over tasks with records, as plotted in Figure 5 . A dash marks a task without a recorded time and a dot one with fewer than three. -->
<!-- [FIGURE:16] Figure 18: Agent steps (tool calls) per rollout, per task and model: the mean over the recorded rollouts in each cell. The bottom row gives each model’s mean over tasks with records, as plotted in Figure 15 . Rows follow Figure 11 . A dash marks a task without a recorded step count and a dot one with fewer than three. -->
<!-- [FIGURE:17] Figure 19: Output tokens per rollout, in thousands, per task and model: the mean over the recorded rollouts in each cell. The bottom row gives each model’s mean over tasks with records, as plotted in Figure 16 . Rows follow Figure 11 . A dash marks a task without an output-token record and a dot one with fewer than three. -->

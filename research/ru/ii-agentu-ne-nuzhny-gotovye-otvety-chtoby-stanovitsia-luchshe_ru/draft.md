# ИИ-агенту не нужны готовые ответы, чтобы становиться лучше

## ИИ-агент может улучшить не только ответ, но и собственную обвязку

Одной и той же языковой модели можно поручить задачу с помощью разных инструментов, промтов и правил работы — и получить разные результаты. Внешняя обвязка определяет, как агент использует инструменты, хранит информацию, проверяет файлы и распределяет работу между исполнителями.

Авторы статьи Harness 2 предлагают дать агенту возможность менять обвязку на ходу: выполнить задачу, заметить проблему, проверить новое правило и применить его в следующий раз. При этом параметры самой модели остаются замороженными. Меняется то, что окружает её при выполнении задачи.

Проверить изменения сложнее, чем может показаться. В реальной работе часто нет готового ответа или проверяющей программы, которые сразу покажут, стало ли лучше. Агент может написать больше инструкций и всё равно ошибиться. А изменение, полезное для одной задачи, способно помешать другой.

## Два уровня улучшения

В основе Harness 2 — два связанных процесса. Первый помогает улучшить обвязку для текущей задачи. Второй сохраняет опыт, который может пригодиться в дальнейшей работе.

Обвязка состоит из восьми частей: системного промта, ограничений, памяти, навыков, подсказок по работе с инструментами, скриптов, подагентов и подключаемых расширений. Они выполняют разные функции. Навык содержит специальную процедуру и загружается по необходимости. Скрипт автоматизирует повторяющееся действие. Подагент выполняет отдельную часть работы в собственном контексте. Расширение может следить за вызовами инструментов и применять правила, которые модель не должна пропустить.

[FIGURE:2]
[CAPTION:Восемь частей обвязки: от системного промта и памяти до скриптов и расширений.]

Для улучшения обвязки текущей задачи Harness 2 использует три шага: **предложить, проверить, собрать**.

Сначала агент изучает исходный запуск задачи: действия исполнителя, использованные инструменты и полученный результат. Правильный ответ ему не показывают. Затем система готовит два варианта изменений. Один нацелен на общие проблемы: например, агент плохо планирует или забывает проверить готовый файл. Второй учитывает особенности конкретной области.

Оба варианта проверяют на той же задаче. Сравнивают не только итоговые файлы, но и ход работы. Если изменение побудило агента запустить нужный инструмент или исправить ошибку, это полезное наблюдение. Но оно не доказывает, что результат верен: в обоих запусках модель может допустить одну и ту же ошибку, а её поведение — меняться от попытки к попытке.

На последнем шаге система выбирает, какие изменения включить в новую обвязку. Можно объединить полезные части двух вариантов, взять один целиком или ничего не менять. Затем агент запускается с итоговой версией обвязки и выдаёт результат для текущей задачи.

[FIGURE:3]
[CAPTION:Сначала система проверяет изменения обвязки на текущей задаче, затем сохраняет пригодный опыт для следующих.]

## Запомнить способ исправления

После завершения работы Harness 2 обновляет библиотеку опыта. В неё попадают принятая обвязка и пояснение: какую проблему заметили, какое изменение попробовали и на каких наблюдениях оно основано. Библиотека не превращается в набор команд, которые автоматически копируются в новую задачу.

Инструкция, полезная для одной работы, может оказаться неверной для другой. Поэтому система каждый раз начинает с общей исходной обвязки и использует библиотеку как источник примеров и идей. Компоненты можно взять за основу, но факты и правила нужно сверять с новой задачей.

Авторы проверили два способа расширить поиск улучшений. **Параллельный режим** создаёт несколько вариантов одновременно: их можно сравнить и собрать из них новую обвязку. **Последовательный режим** меняет её шаг за шагом. Каждый следующий шаг учитывает результаты предыдущего.

В обоих режимах число попыток задаёт бюджет поиска. Больше попыток — больше вычислений и возможностей найти удачное изменение. В параллельном режиме варианты могут выполняться одновременно, если хватает ресурсов.

[FIGURE:4]
[CAPTION:Параллельный режим проверяет несколько вариантов, а последовательный развивает обвязку шаг за шагом.]

## Результаты испытаний

Исследователи проверили систему на трёх бенчмарках: WorkBuddy-Bench для задач по программированию, веб-задач и офисной работы; JobBench для длинных профессиональных задач; и бенчмарке Harvey для юридической работы. Они использовали Gemini 3.5 Flash и GLM-5 с двумя исходными вариантами обвязки. Саму модель в ходе экспериментов не дообучали. Основные результаты усредняли по трём запускам с разным порядком задач.

Уже один цикл улучшения повысил результаты обеих моделей во всех трёх бенчмарках и во всех проверенных сочетаниях модели с обвязкой. На WorkBuddy-Bench прирост GLM-5 достигал 11,5 балла. На JobBench максимум составил 4,5 балла, а в юридическом бенчмарке оценка по пройденным критериям выросла на 11,8 процентного пункта.

Дополнительные циклы давали новый прирост. При параллельном поиске с бюджетом в пять вариантов результаты улучшились ещё на 2,9–3,9 балла на WorkBuddy-Bench и на 3,0–4,2 балла на JobBench. В юридических задачах дополнительный прирост составил 2,6–6,7 процентного пункта.

[FIGURE:1]
[CAPTION:С ростом бюджета поиска результаты Harness 2 улучшаются; в примере для Gemini 3.5 Flash система превосходит исходный вариант обвязки во всех областях WorkBuddy-Bench.]

Прирост особенно заметен там, где исходная модель слабее. На WorkBuddy-Bench GLM-5 после улучшения обвязки в некоторых случаях превзошла Gemini 3.5 Flash с исходной обвязкой. Результат зависит не только от возможностей модели, но и от того, как она работает с инструментами и организует работу.

Авторы также проверили, можно ли перенести накопленный опыт на другие задачи. Библиотека, собранная на JobBench, дала небольшой прирост на WorkBuddy-Bench. А обвязка, созданная для Gemini 3.5 Flash, улучшила результаты других моделей на части задач WorkBuddy-Bench. Эффект различался в зависимости от модели и области: перенос опыта возможен, но не гарантирует одинаковой пользы во всех случаях.

Удаление отдельных частей системы тоже ухудшало результаты. Когда исследователи отключали библиотеку, раздельную работу над общими и предметными проблемами или сборку изменений из разных вариантов, оценки снижались. Прирост зависит от проверки изменений, способа их объединения и накопленного опыта, а не только от одной удачной инструкции.

## Где метод может ошибиться

У Harness 2 нет прямого способа узнать, правильна ли работа. Система опирается на различия между запусками и оценки модели. Это помогает увидеть, что изменилось в поведении агента, но не заменяет проверку результата. Если два запуска основаны на одной и той же ошибочной догадке, сравнение может её не выявить.

Авторы описывают случаи, когда система выбирала слабый вариант ответа. В других примерах слишком узкое изменение мешало учесть все нужные условия. Иногда было трудно отделить эффект обвязки от обычных различий между запусками или особенностей проверки.

Больше вариантов означает больше запусков и затрат на инференс. В экспериментах дополнительные вычисления улучшали результаты, но это не значит, что всегда нужно использовать максимальный бюджет. Системе ещё предстоит научиться оценивать, когда поиск стоит продолжать, а когда данных уже достаточно.

## Вывод

Harness 2 позволяет улучшать **обвязку ИИ-агента для текущей задачи** и сохранять проверенный опыт для будущих. Это помогает повышать качество работы без дообучения модели и переносить удачные подходы между похожими задачами.

Сравнение поведения — лишь косвенная проверка. Оно показывает, что агент стал действовать иначе, но само по себе не доказывает, что результат правильный. Такие системы помогают быстрее улучшать обвязку, но им по-прежнему нужны надёжные проверки качества и контроль затрат на дополнительные запуски.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0]  -->
<!-- [FIGURE:1] Figure 1 : Overall performance. Left: WorkBuddy-Bench by domain for
Gemini 3.5 Flash under OpenCode. Harness 2 with parallel recursion at k = 5 k{=}5 exceeds the strongest baseline in every domain, Meta-Harness, and the number
above each Harness 2 bar is its gain over the base harness. Right: on
WB-code, Harness 2 keeps improving as the budget k k grows. -->
<!-- [FIGURE:2] Figure 2 : The eight harness components in Harness 2 , grouped by their role in the runtime. -->
<!-- [FIGURE:3] Figure 3 : The Harness 2 pipeline. Task-level recursion proposes invariant and
domain-specific harness edits, probes their effects, and composes a successor
execution harness. After each task, harnessing-level recursion updates the
improvement harness with reusable harnesses and lessons from the refinement
process. -->
<!-- [FIGURE:4] Figure 4 : Two forms of task-level recursion. (a) Parallel recursion probes multiple candidates and independently
composes successor harnesses. (b) Sequential recursion carries each refined harness and
accumulated execution evidence into the next step. -->
<!-- [FIGURE:5] Figure 5 : Effect of task-level recursion. Performance comparison on WB-code and WB-office as the scaling budget k k increases . -->
<!-- [FIGURE:6] Figure 6 : Compute–performance trade-off on JobBench
and WorkBuddy-Bench. -->
<!-- [FIGURE:7] Figure 7 : Harnessing-level recursion. Left: direct refinement with the improvement harness.
Right: JobBench-to-WorkBuddy-Bench library transfer for one-step refinement. -->
<!-- [FIGURE:8] Figure 8 : Same model as executor and editor. Base harness versus Harness 2 with OpenCode at k = 2 k{=}2 . Annotations show score gains. -->
<!-- [FIGURE:9] Figure 9 : Case study on JobBench. Left: the task and the two failure modes from the base trajectory. Middle: the improved harness; tinted
components were written at test time, grey ones are inherited from the base.
Right: the outcome of re-running the composed harness. -->
<!-- [FIGURE:10] Figure 10 : Library provenance and the distribution of edits. Left: modified components compared with the library snapshot available
during refinement. Containment measures the share of non-boilerplate
lines found in a library entry for the same component. Lines common to
more than a fifth of a benchmark’s adopted harnesses are excluded.
Right: edit distribution across components. -->
<!-- [FIGURE:11] Figure 11 : Leave-one-out reuse. Each task is re-run with its
own entry excluded from the completed library. Annotations show gains
over the original online run at k = 1 k{=}1 . -->
<!-- [FIGURE:12] Figure 12 : Cross-model transfer on WorkBuddy-Bench. The harness
refined for Gemini 3.5 Flash under OpenCode is applied unchanged to
GLM-5, Gemini 3.7 Flash, and Claude Opus 4.8, and compared with each
executor’s base harness. Annotations show the score gain. -->
<!-- [FIGURE:13] Figure 13 : Comparison with production harnesses on WorkBuddy-Bench. Gemini 3.5 Flash under CodeBuddy, OpenCode, Codex, and Claude Code,
each left unchanged, versus Harness 2 starting from OpenCode at k = 5 k{=}5 .
Annotations give the gain over the strongest fixed harness per domain. -->
<!-- [FIGURE:14] Figure 14 : Failure cases in recursive harnessing. Nine results
below their references, grouped by candidate selection, restrictive
edits, and other execution or evaluation effects. The scores are
retrospective evaluations and are not available to the pipeline. -->
<!-- [FIGURE:15] Figure 15 : WorkBuddy-Bench, Code. The reference emits calls as plain text without running tools. A tool-guidance edit forbidding pseudo-calls raises the score from 60.0 60.0 to 100.0 100.0 . -->
<!-- [FIGURE:16] Figure 16 : WorkBuddy-Bench, Office. The reference aggregates at the wrong grain and no channel row matches the key; a skill pins the grain and the derived fields, and a guardrail treats inputs as read-only and applies the stated cleaning rules before aggregating ( 23.6 → 100.0 23.6\to 100.0 ). -->
<!-- [FIGURE:17] Figure 17 : WorkBuddy-Bench, Web. Page state is frozen at first render, so remapping and export go stale; a skill models the state the specification names and re-derives it on every change, a script checks the artifact opens offline, and a guardrail forbids network dependencies ( 64.0 → 100.0 64.0\to 100.0 ). -->
<!-- [FIGURE:18] Figure 18 : LAB, arbitration. Markup is left in Word's track-changes layer, so read as text the document shows only the accepted wording; a skill records deletions and insertions as in-body character markup, and a guardrail loads it for redline tasks ( 44.4 → 94.5 44.4\to 94.5 ). -->
<!-- [FIGURE:19] Figure 19 : JobBench, social-science research assistant, all eight components written. With Claude Opus 5 as executor and editor, research expands to fill the budget and files stay unwritten near the deadline; the composed harness adds, among other edits, a plugin that appends a warning to tool results after a fixed number of calls without an artifact, a subagent that returns citable tables in its own context, and durable domain memory ( 72.0 → 100.0 72.0\to 100.0 ). -->

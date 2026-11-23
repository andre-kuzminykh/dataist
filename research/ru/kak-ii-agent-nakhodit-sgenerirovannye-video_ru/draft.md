# Как ИИ-агент находит сгенерированные видео

ИИ-видео сложнее распознать, когда подделка прячет дефекты в одном кадре, коротком движении или надписи. WeVisForensics проверяет такие ролики как расследование: выбирает подходящего специалиста, указывает ему нужный момент и собирает отдельные свидетельства, прежде чем вынести вердикт. Со временем улучшается и тот, кто выбирает проверки, и сами специалисты.

## Главная мысль

Надёжное распознавание строится на двух связанных способностях: **выбрать, что и где проверить, и распознать дефект в выбранном фрагменте**. Если улучшать только выбор проверок, система упрётся в ошибки неподвижных специалистов.

🟠 Вместо одного общего рассуждения о ролике система собирает отдельные свидетельства: о внешнем виде, физике, здравом смысле, тексте и звуке.
🟠 Главный агент сам решает, какого специалиста вызвать и на каком отрезке видео.
🟠 Обучение идёт в двух темпах: главный агент обновляется чаще, специалисты — медленнее, по результатам его запросов.
🟠 Специалисты учатся на конкретных ошибках: например, замечать испорченные буквы и не принимать обычное размытие за дефект генерации.

## Из чего состоит WeVisForensics

Система разделяет выбор проверки и анализ изображения. **Главный агент расследует, специалисты осматривают**, а каждый отчёт содержит вывод, уверенность и объяснение с привязкой ко времени.

[FIGURE:2]
[CAPTION:Главный агент выбирает специалиста и временной отрезок, получает отчёт и выносит вердикт; обучение одновременно улучшает расследователя и библиотеку специалистов.]

На схеме показаны три связанные части:

🟣 **Главный агент-расследователь** сначала получает обзор ролика, затем выбирает тип проверки и нужный момент. Он может сделать до четырёх вызовов и должен завершить расследование вердиктом.
🟣 **Библиотека специалистов** включает четыре визуальные роли: внешний вид, физическая согласованность, здравый смысл и экранный текст. Два аудиоинструмента описывают голос и проверяют речь; они остаются неизменными.
🟣 **Двухтемповое обучение** обновляет расследователя после каждой группы запусков, а визуальных специалистов — после накопления подходящих примеров. Так система избегает слишком частых взаимных изменений.
🟣 **Набор данных ForenCue-30K** хранит свидетельства отдельно по ролям и времени. Он также содержит примеры реальных действий агентов, чтобы главный агент учился на ответах специалистов, которые действительно получил.

Разделение ролей делает проверку понятной и проверяемой. Например, специалист по тексту не должен объявлять ролик поддельным только потому, что слово распознано неверно: он ищет видимые дефекты букв, а затем передаёт их расследователю.

## Как это работает: проверка надписи на упаковке

Представим короткий ролик, где человек показывает коробки с товарами. На общем плане видео выглядит обычным, но надписи на упаковках могут меняться или деформироваться. Расследование проходит так:

🟠 **Шаг 1. Обзор.** Главный агент получает несколько кадров с отметками времени. Он замечает коробки и движущуюся руку, но пока не может уверенно судить о подлинности. Если важная надпись не попала в обзорные кадры, агент может её не заметить.
🟠 **Шаг 2. Проверка внешнего вида.** Агент вызывает соответствующего специалиста и задаёт отрезок видео. Тот сравнивает текстуры и границы объектов во времени. Он может отметить слишком гладкую кожу, но такое наблюдение само по себе не доказывает подделку: похожий эффект дают фильтры и обработка изображения.
🟠 **Шаг 3. Проверка текста.** Агент выбирает кадр, где надпись видна лучше. Система распознаёт возможные текстовые области, увеличивает их и проверяет форму букв. Если штрихи сливаются или повторяющиеся символы устроены по-разному, это становится отдельным свидетельством. Если кадр размыт, ответ может быть неопределённым.
🟠 **Шаг 4. Вердикт.** Агент сопоставляет отчёты и решает, достаточно ли оснований. В описанном в работе примере надписи на коробках содержали повторяющиеся искажённые буквы; в сочетании с необычно гладким лицом это привело к вердикту «подделка».

На каждом шаге возможна ошибка: специалист может не заметить слабый дефект, принять стилизацию за генерацию или не получить достаточно чёткий кадр. Поэтому отчёты включают уверенность, а неопределённый ответ не считается доказательством ни подлинности, ни подделки.

## Как проверяют систему

Исследователи измеряют **точность вердикта** и то, насколько уместно агент вызывает специалистов. Для проверки вердиктов используют бенчмарки с видео от знакомых и новых генераторов, а также AgenticCue — набор роликов, сгруппированных по типу дефекта: внешний вид, физика, текст, здравый смысл и звук.

Для проверки действий агента считают точность вызова роли: как часто специалист действительно нужен для данного ролика. Это помогает отличить осмысленный выбор проверок от стратегии «вызвать всех подряд». Точность вызова оценивают вместе с точностью вердиктов: агент не должен улучшать показатель выбора, просто пропуская сложные проверки.

Сравнение включает специализированные детекторы, модели общего назначения, прежнюю версию самой системы и варианты с отключёнными частями обучения. Для всех сравниваемых детекторов используют данные авторов и единый протокол оценки. Отдельно люди проверяют качество размеченных свидетельств: так исследователи оценивают, действительно ли специалист указывает на то, что видно в кадре.

## Цифры

[NUMBERS]
- 95,2% | Средняя точность WeVisForensics на четырёх группах бенчмарков, включая новые генераторы и задачи с выбором специалиста.
- 9,0% | Преимущество над прежним лучшим детектором по средней точности, заявленное авторами.
- 97,0–98,8% | Точность на пяти категориях AgenticCue: визуальные дефекты, физика, текст, здравый смысл и звук.
- 2,19 | Среднее число вызовов специалистов на ролик после обучения с подкреплением.
- 30,5% → 8,0% | Доля ответов специалистов с хотя бы одним замеченным недостатком в парной человеческой проверке до и после улучшения.
[/NUMBERS]

Результаты показывают, что система сохраняет высокую точность на разных типах дефектов и сокращает число проверок по сравнению с исходной версией, которая в среднем делала 2,50 вызова на ролик. Улучшается и итоговый вердикт: специалисты реже пропускают видимые аномалии и дают менее проблемные объяснения.

## Вывод

**Проверка по отдельным свидетельствам помогает находить локальные дефекты, которые можно пропустить при едином просмотре ролика.** Специалисты учатся на запросах главного агента: на примерах из обучения физический специалист, например, стал реже отвечать неопределённо.

Система не доказывает подлинность видео в строгом смысле. Её вывод зависит от того, попали ли нужные кадры в выборку, правильно ли выбран специалист и насколько качественно размечены учебные данные. Звук и распознавание речи тоже не развиваются вместе с визуальными специалистами, а остаются фиксированными инструментами.

Результаты показывают, что подход работает на проверенных наборах, в том числе на видео от генераторов, которых не было в обучении. Остаётся выяснить, как он поведёт себя на новых типах подделок, при иных условиях съёмки и на видео, где несколько неоднозначных сигналов противоречат друг другу. Для практического использования такой вердикт разумно считать **обоснованной оценкой по наблюдаемым признакам**, а не окончательным доказательством.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:2] Figure 2 : Overview of WeVisForensics. Top: the investigator π θ \pi_{\theta} repeatedly calls an inspector s t s_{t} on a temporal scope u t u_{t} , reads its report z t z_{t} , and issues a verdict with the evidence chain. Middle: DTPO updates the investigator on every batch, while the trainable inspectors self-evolve on a slower timescale. Bottom: accuracy on the four evaluation benchmarks against representative detectors. -->
<!-- [FIGURE:3] Figure 3 : WeVisForensics and its training strategy, DTPO. The investigator rolls out with a fixed FSL snapshot and is updated on every batch with outcome rewards and CLUE. Grounded calls ( 𝒟 OPD \mathcal{D}_{\mathrm{OPD}} ) queue by role in the interaction pool, from which the slow process distills privileged EMA teachers into students, revises skill cards, and refreshes the FSL every H H steps. -->
<!-- [FIGURE:4] Figure 4 : Overview of ForenCue-30K. Curated videos are annotated with role-specific artifact evidence and converted into sub-agent records and interaction trajectories, and an RL pool supports DTPO. Examples show artifacts targeted by each sub-agent. -->
<!-- [FIGURE:5] Figure 5 : Self-evolution of the forensic library over training. (a) Sub-agent verdicts on training calls, scored against role-level annotations. Left: moving averages of the miss rate on generated videos and of the verdict F1 over LoRA refreshes (minor ticks). Middle: role-level error per sub-agent across the early, middle, and late phases of training. Right: evidence F1 of the frozen library and of the evolved library at the early, middle, and final checkpoints on four test benchmarks, each spanning the appearance, physical, and OCR axes clockwise. (b) Accepted edits, with one Report and one Ignore rule each. The gray card shows candidate rules that failed the acceptance test. (c) Three generated test videos inspected by the three checkpoints, with verbatim sub-agent excerpts and the agent’s final answer. -->
<!-- [FIGURE:6] Figure 6 : Qualitative comparison on a generated video with warping handwritten text. Left: a) The CoT-based VideoVeritas [ 36 ] dismisses the garbled text as stylistic without inspecting it. b) In the fixed-workflow ARGUS [ 56 ] , texture, lighting, and motion reports outweigh the detected text deformation. Right: The SFT or DTPO-trained main agent paired with the SFT or evolved sub-agents. The evolved sub-agents flag the glyph anomalies, and only the trained main agent, which moves its OCR inspection to the warped text at 7 s, turns them into a fake verdict. -->
<!-- [FIGURE:12] Figure 12 : Comparison of AI-generated video detection paradigms. a) CoT-based reasoning uses textual rationales. b) Multi-agent workflows follow fixed execution structures. c) WeVisForensics adaptively coordinates sub-agents and evolves them together with the main policy. -->
<!-- [FIGURE:13] Figure 13 : Qualitative comparison of investigation paradigms. All three approaches classify the generated video as fake. The CoT-based detector makes unsupported motion claims, and the fixed-workflow detector aggregates predefined observer reports. The adaptive agent requests localized appearance and OCR inspections and grounds its verdict in changing emblem contours and degraded apron lettering. -->
<!-- [FIGURE:14] Figure 14 : Complete evolution comparison. On an AI-generated video, the CoT-based VideoVeritas and the fixed-workflow ARGUS both answer real. Before DTPO (top right), the appearance sub-agent reports no issue and WeVisForensics answers real. After DTPO (bottom right), the same first inspection localizes soft hand and finger boundaries during the opening gesture, and the main agent answers fake. -->

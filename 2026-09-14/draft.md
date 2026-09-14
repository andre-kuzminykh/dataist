# Как ИИ-агент управлял интернет-магазином и увеличил капитал в 14 раз

## Когда LLM дают магазин на год

Большинство бенчмарков для ИИ-агентов проверяют короткую дистанцию. Исправить баг. Найти ответ. Пройти набор шагов. Даже если шагов много , задача часто сводится к одному финальному результату.

**E-Commerce Bench** смотрит на другую проблему: что будет , если дать модели не задание на 20 минут , а **бизнес на 365 дней**. С деньгами , складом , возвратами , переговорами , мошенниками , сезонностью и кассовыми разрывами.

Звучит почти как симулятор. По сути это проверка того , что сегодня волнует всех , кто строит ИИ-агентов: **умеет ли модель держать линию на длинном горизонте** , учиться по ходу дела и не проваливать задачу из-за собственной забывчивости , суеты или плохих решений в начале пути.

В новой статье команда Qwen и исследователи из HKUST представили открытый бенчмарк , где 18 передовых моделей управляют интернет-магазинами в течение целого года. Итог измеряют не только деньгами. Смотрят ещё на переговоры , устойчивость к мошенничеству , управление ликвидностью , эффективность , исполнение операций и способность улучшать решения по мере накопления опыта.

И тут начинается самое интересное: **модель , которая зарабатывает больше всех , вовсе не лучшая по остальным качествам**.

## Что такое E-Commerce Bench

Идея простая. Модели выдают стартовый капитал в **100 тысяч юаней** и доступ к инструментам продавца на маркетплейсе. Дальше агент сам решает , что делать:

🟠 открыть до четырёх магазинов разных типов  
🟣 изучать категории и спрос  
🟠 искать поставщиков  
🟣 торговаться по цене  
🟠 закупать товар  
🟣 выставлять его в магазинах  
🟠 менять цены  
🟣 отправлять заказы  
🟠 обрабатывать возвраты  
🟣 выводить деньги из кошелька платформы в банк

Это важно , потому что задача здесь **не распадается на независимые мини-задачи**. Если вы в январе купили не тот товар , ошиблись с объёмом или повелись на мошенника , последствия тянутся месяцами. Склад копит издержки. Деньги уходят сразу , а выручка приходит с задержкой. Репутация магазина влияет на спрос. Поставщик , у которого вы удачно выбили цену , может исчезнуть позже.

[FIGURE:2]
[CAPTION:Схема E-Commerce Bench: агент работает через обвязку и 18 инструментов , а под ними живёт детерминированная модель экономики и переговоров.]

У бенчмарка четыре слоя. Сверху — **обвязка агента**: цикл ходов , работа с контекстом и постоянная память. Ниже — 18 инструментов. Под ними — **детерминированная среда** , где отдельно живут продажи , экономика и переговоры. Внизу — данные , собранные на основе реальной платформы электронной торговли.

Ключевой момент здесь — слово **детерминированная**. Авторы специально убрали как можно больше шума. Если два агента совершают одинаковые действия , они получают одинаковый результат. Это редкость для сложных бенчмарков для ИИ-агентов , где всё часто плывёт из-за случайных ответов второй стороны или нестабильной симуляции.

## Почему это важно

Сейчас многие бенчмарки для агентов по сути проверяют , **может ли модель довести до конца один длинный сценарий**. E-Commerce Bench проверяет другое: **может ли модель месяцами принимать связанные решения в меняющейся среде**.

Разница большая.

Если вы строите ИИ-агентов для реальной работы , вас интересует не только способность вызвать инструмент или написать убедительный ответ. Вас интересует вот что:

🟠 помнит ли агент , какую цену уже выбил у поставщика  
🟣 замечает ли он , что деньги зависли в кошельке платформы , пока банк уходит в минус  
🟠 умеет ли он отказаться от подозрительного поставщика  
🟣 не тратит ли он половину года на повтор одних и тех же запросов  
🟠 учится ли он на своих прошлых сделках  
🟣 выдерживает ли стратегию , когда контекст давно переполнен

Именно на таких вещах длинные задачи обычно проваливаются. Не на одном большом неверном ответе , а на цепочке мелких просчётов.

## Как устроена среда

Внутри бенчмарка довольно жёсткая экономика.

У агента есть **три денежных контура**:

🟠 банковский счёт — с него списываются закупки , операционные расходы , хранение и доставка  
🟣 эскроу — туда попадает выручка после отгрузки  
🟠 кошелёк платформы — туда деньги доходят позже , и только потом их можно вывести в банк

Это значит , что прибыльный бизнес всё равно может обанкротиться , если агент плохо управляет ликвидностью. Продал много — не значит , что у вас есть живые деньги сегодня.

[FIGURE:5]
[CAPTION:Деньги в симуляции идут по трём счетам с задержкой: расходы списываются сразу , а выручка доходит до банка только через эскроу и кошелёк платформы.]

Есть и другие реалистичные детали:

🟠 спрос зависит от цены , сезона , дня недели , акций , событий и репутации магазина  
🟣 товар нужно успеть отправить за два дня , иначе заказ отменится  
🟠 возвраты зависят от категории , цены , скорости доставки и качества партии  
🟣 хранение на складе дорожает со временем  
🟠 у поставщиков есть скрытый порог цены , ниже которого они не согласятся  
🟣 около четверти поставщиков мошенничают

Отдельно устроены **переговоры**. Во многих похожих симуляциях вторую сторону тоже играет LLM , и тогда всё разваливается: слишком много случайности , слишком легко уговорить контрагента на неестественное решение. Здесь экономика переговоров задаётся **правилами** , а LLM только озвучивает реплики поставщика. Цена , уступка , согласие или отказ определяются не словесной магией , а детерминированным ядром.

Это делает сравнение моделей чище.

## Что проверяли у моделей

Авторы не стали сводить всё к одному числу. Кроме итоговых активов , они ввели ещё шесть осей оценки:

🟠 **качество переговоров** — насколько сильно модель умеет сбивать цену у честных поставщиков  
🟣 **защита от мошенничества** — какая доля закупок ушла мошенникам  
🟠 **ликвидность и устойчивость** — насколько глубоко агент проседал по активам и не уходил ли в банкротство  
🟣 **операционная эффективность** — сколько прибыли принёс один вызов инструмента  
🟠 **исполнение операций** — как агент управлял возвратами и отгрузками  
🟣 **обучение на длинном горизонте** — использовал ли агент опыт прошлых закупок , чтобы со временем покупать дешевле

Вот здесь статья даёт важный результат: **универсального победителя нет**.

**Коротко:**
🟠 **GPT-5.6 Sol** — лидер по деньгам  
🟣 **Qwen3.8-Max-Preview** — лучшая среди открытых моделей  
🟠 лидер по прибыли не лидер по защите от мошенничества

[FIGURE:1]
[CAPTION:Итоговые активы 18 моделей к концу года: разброс огромный , а часть эпизодов заканчивается банкротством.]

Лидером по деньгам стал **GPT-5.6 Sol**. Он в среднем превратил стартовые 100 тысяч юаней в **1,43 млн**. Это примерно **14,3x** от начального капитала.

Но рядом с этим числом сразу идёт неприятное уточнение: по защите от мошенничества модель заняла **16 место из 18**. То есть зарабатывала много , но заметную долю денег всё равно отдавала плохим поставщикам.

Среди открытых моделей лучшей стала **Qwen3.8-Max-Preview**. Она дошла до **416 тысяч юаней** , то есть примерно до **4,2x** от старта. Это не уровень лидера общего зачёта , но лучший результат в открытом сегменте.

## Главные результаты

Если сжать статью до нескольких тезисов , картина такая:

🟠 **Разрыв между моделями огромный.** Между лучшей и худшей по итоговым активам — разница более чем в тысячу раз.  
🟣 **Высокая прибыль не равна надёжности.** Лидер по деньгам может быть слабым в защите от мошенничества или в эффективности.  
🟠 **Четыре модели частично банкротились.** Даже сильные семейства моделей не застрахованы от кассового провала.  
🟣 **Почти никто не учится по ходу года.** 16 из 18 моделей не показывают явного прогресса в повторных переговорах с тем же поставщиком.  
🟠 **Память используется слабо.** Хотя у агентов есть постоянная память вне окна контекста , большинство почти ей не пользуется.  
🟣 **Много вызовов инструментов уходит не туда.** Основная масса действий — это рутина: отгрузка , переход к следующему дню , вывод денег , публикация товара. На реальное улучшение закупки и цен тратится мало внимания.

**Коротко по результатам:**
🟠 1,43 млн юаней у лидера  
🟣 4 из 18 моделей частично банкротились  
🟠 16 из 18 не показали явного обучения на длинном горизонте

Особенно интересен результат по **обучению на длинном горизонте**. Авторы проверяли , помнит ли модель , по какой цене уже покупала один и тот же товар у того же поставщика. Логика простая: если вы однажды выбили хорошую цену , следующую закупку разумно начинать хотя бы с этого якоря.

На практике почти все модели этого не делают. Они либо забывают прошлые сделки , либо не умеют использовать их в новых переговорах , либо просто не выстраивают такую стратегию.

Исключение — **Qwen3.8-Max-Preview**. Это единственная модель , которая уверенно показала улучшение по мере года и смогла в среднем давить цену вниз на повторных закупках.

[FIGURE:8]
[CAPTION:Переговоры на коротком и длинном горизонте: один агент платит больше , чем уже платил раньше , другой постепенно сбивает цену при повторных заказах.]

## Где модели чаще всего проваливаются

Статья показывает не только итоговые баллы , но и **типовые поломки**.

Самые частые проблемы такие:

🟠 агент покупает слишком много товара в начале года и потом тонет в складских расходах  
🟣 агент соглашается на подозрительных поставщиков и повторно закупается у них  
🟠 агент принимает стартовую цену без торга , хотя можно было сбить её ниже  
🟣 агент повторяет одни и те же поисковые запросы вместо того , чтобы сохранить выводы в память  
🟠 агент забывает выводить деньги из кошелька платформы в банк  
🟣 агент почти не меняет цены в течение года , хотя спрос вокруг уже изменился

Один из показательных кейсов — банкротный эпизод у Qwen3.5-Plus. Модель открыла четыре магазина почти сразу , закупила много товара , продажи не успели это переварить , расходы росли , деньги в банк не возвращались достаточно быстро. В итоге всё закончилось минусом уже к маю.

Это напоминание: **на длинном горизонте агент проваливает задачу потому , что не держит систему в целом**.

## Что это говорит о LLM-агентах сегодня

Если вы смотрите на рынок агентных систем , статья даёт довольно ясную картину.

Во-первых , **длинный горизонт остаётся слабым местом**. Модели уже умеют неплохо выполнять локальные действия: вызвать инструмент , провести отдельные переговоры , открыть магазин , отправить заказ. Но связать всё это в устойчивую годовую стратегию получается редко.

Во-вторых , **память и управление состоянием важнее , чем кажется по коротким демкам**. Когда история тянется тысячи шагов , агенту нужно не просто знать мир , а хранить полезные рабочие факты: кто мошенничал , где был хороший поставщик , какие цены уже проходили , какие магазины реально окупаются.

В-третьих , **одного лидерборда по прибыли мало**. Если смотреть только на финальные деньги , вы пропустите половину картины. Один агент богатый , но дырявый по мошенничеству. Другой аккуратный , но медленный. Третий отлично торгуется , но слабо масштабируется.

И наконец , **для честной оценки агентных систем нужны воспроизводимые среды**. Здесь это особенно видно. Когда экономика и переговоры задаются детерминированно , различия в результате можно связывать с политикой самого агента , а не со случайной удачей.

## Вывод

**E-Commerce Bench** показывает , что длинные многошаговые задачи для ИИ-агентов — это уже вопрос , **умеет ли модель месяцами управлять последствиями своих решений**.

Главные выводы из статьи такие:

🟠 **Лучшая по деньгам модель не оказывается лучшей по всем остальным метрикам.**  
🟣 **Почти все модели плохо используют накопленный опыт на длинном горизонте.**  
🟠 **Ликвидность , память и защита от мошенничества остаются системными проблемами.**  
🟣 **Открытые модели уже конкурентны в части стратегического поведения , но до лидеров по прибыли дистанция ещё большая.**  
🟠 **Следующий прогресс в агентах будет зависеть не только от самой LLM , но и от обвязки: памяти , контроля состояния , правил работы с контекстом и устойчивых процедур принятия решений.**

Если вы хотите понять , где у современных ИИ-агентов заканчиваются аккуратные демки и начинается реальная работа в длинной среде , этот бенчмарк даёт один из самых полезных ответов на сегодня.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1: Mean end-of-year total assets, eighteen models, five 365-day episodes each. Bars start at the ¥100,000 stake. Whiskers span one 5-run standard deviation, hollow dots are single episodes, and red fractions count bankrupt episodes, which stay pooled into the mean. The right column gives mean assets as a multiple of the stake. -->
<!-- [FIGURE:1] Figure 2: Seven evaluation axes for the strongest model of each vendor family by mean total assets, the primary score, and the six evaluation dimensions clockwise from the top, each on the ranking metric § 3.7 gives it. Axes are min-max normalized over the eighteen model means, so 1 is the best of the eighteen and 0 the worst, with a dashed polygon at the median. Fraud avoidance, solvency, execution, and learning are sign-flipped, so a vertex further from the center is better on every axis. -->
<!-- [FIGURE:2] Figure 3: Overview of E-Commerce Bench. The agent works through four layers. An agent loop layer carries turn-based control, context management, and persistent memory, and a tool layer holds the 18 e-commerce tools. Under both sits a deterministic environment layer , the sales-and-economy engine beside the two-layer negotiation engine, computing over a data layer derived from a real e-commerce platform. -->
<!-- [FIGURE:3] Figure 4: The agent loop layer. One model call produces a batch of tool calls; the batch
runs in order, and a timed tool advances the simulated clock inside its own call. The
daily settlement fires whenever the clock reaches the next 08:00, whether a timed tool
carried it there or the agent asked to skip to tomorrow.
Tools read and write the hidden environment state, and the
settlement writes back to it as well, posting that day’s fees, sales, and returns. The
day’s news and any notices are appended to the tool responses. The transcript is left
alone until it passes 120,000 tokens, and only then are its oldest groups dropped. -->
<!-- [FIGURE:4] Figure 5: How eviction works. A group is what the editor removes as a unit: one model
reply together with every tool result that reply produced, so a turn that called six
tools is still one group, and about fifty groups fill the window. A pass fires only once
a group pushes the count past 120,000 tokens, then drops whole groups, oldest first,
until 60,000 tokens are released or the clearable groups run out. The system message,
the first user turn and the two newest groups are kept. -->
<!-- [FIGURE:5] Figure 6: Three-account deferred settlement. (a) Costs leave the bank the day they are incurred, while revenue passes through escrow and the platform wallet first. (b) One 40-unit order bought at the opening quote and resold at reference, followed as cash for 16 days. -->
<!-- [FIGURE:6] Figure 7: The demand model. (a) The four price-elasticity families at their median parameter, solid without a promotion and dashed with the largest promotion boost. (b) The chain of multipliers that turns one SKU’s price into units sold. -->
<!-- [FIGURE:7] Figure 8: Negotiation at two timescales, from real episodes, each panel on its own price
axis and the cost floor hidden from the agent. (a) One session offer by offer, the agent bidding up and the kernel conceding
down until the agent accepts its standing quote. (b) The same (supplier, SKU) pair all year, where that session ends a run of
near-floor deals and the price never recovers, the hatched wedge being the overpayment AnchorRegret \mathrm{AnchorRegret} averages. (c) Another agent instead pushes lower at
nearly every restock. -->
<!-- [FIGURE:8] Figure 9: Capability profiles for six of the 18 models. The primary score and the six dimensions of this section run clockwise from the top, profit as mean end-of-year total assets, negotiation as CSE + \mathrm{CSE}^{+} , fraud avoidance as BadSpend % \mathrm{BadSpend}\% , solvency as peak drawdown over peak total assets, efficiency as profit per tool call, execution as the controllable return rate and learning as AnchorRatio \mathrm{AnchorRatio} . Fraud avoidance, solvency, execution and learning are sign-flipped so that higher is better on every axis. Each axis is min-max normalized over the 18 model means, so 1 marks the best mean and 0 the worst, with whiskers over the five episodes and a dashed polygon at the median. Efficiency carries no episode spread, being a ratio of 5-run means, and the archived AnchorRatio \mathrm{AnchorRatio} spread is a population std over a varying number of episodes, so the learning axis draws no whisker either. No profile fills the polygon. -->
<!-- [FIGURE:9] Figure 10: (a) Profit per tool call for the 18 models, best first, mean total assets less the ¥100,000 stake divided by mean tool calls per episode. Bankrupt episodes are pooled into both means, and the three models that finish under the stake sit left of zero. (b) Where six models spent their calls, over eight groups of the 18 tools, scaled within each model. -->
<!-- [FIGURE:10] Figure 11: One bankruptcy episode day by day, Qwen3.5-Plus episode 0. Total assets and
bank balance are on the left axis, warehouse stock on the right, and the shaded band
marks the days the bank balance stayed negative. -->
<!-- [FIGURE:11] Figure 12: How often the context editor fired, over the 90 evaluated episodes. Each event is one eviction pass. A model that never reaches the ceiling evicts nothing. -->
<!-- [FIGURE:12] Figure 13: The released data. (a) Products per category. (b) Reference prices. (c) Natural return rate by store type, T the difficulty tier. (d) Suppliers per category against catalog depth. -->
<!-- [FIGURE:13] Figure 14: The monthly seasonality multiplier for all 12 store types, rows grouped by difficulty tier. The right panel gives each type’s trough, peak and peak-to-trough ratio. -->
<!-- [FIGURE:14] Figure 15: The 2026 calendar. Eight promotions the agent can join by choosing a discount, and ten events it cannot opt out of. Promotion bars show the multiplier a 30 % 30\% discount buys, event bars their extreme per-store-type multiplier. -->
<!-- [FIGURE:15] Figure 16: The thirteen settlement steps in the order the simulation runs them at each 08:00 crossing, with the state each step reads and writes. Fill colour marks which money bucket a step moves. -->
<!-- [FIGURE:16] Figure 17: How reputation moves. (a) The goodwill term against units shipped. (b) The penalty term against the returned share of recent units, at three cancellation shares. (c) A service shock decays while a chronic failure rate does not. -->
<!-- [FIGURE:17] Figure 18: Where a unit’s money goes. (a) Each component as a share of retail price, for a median-priced fashion SKU beside a snacks SKU. (b) Unit profit against the price ratio, with dotted lines where demand reaches zero. (c) Units a store must sell each day to cover its operating cost. -->
<!-- [FIGURE:18] Figure 19: The four decision functions of the Negotiation Kernel, swept on one supplier and SKU. (a) Acceptance and (b) walk-away against the agent’s offer. (c) The concession the kernel returns for a given concession from the agent. (d) The quote ladder it walks down. -->
<!-- [FIGURE:19] Figure 21: Total assets over the year for eight models spanning the ranking. The solid line is the mean over episodes still running, the band their min-to-max range, and a red cross marks a bankruptcy. The line turns dashed once fewer than five episodes remain, so the mean there counts survivors only. -->
<!-- [FIGURE:20] Figure 22: Total assets over the year for all 18 models, ordered by their mean at the end of the year. Each thin line is one episode and the black line their mean while they are still running. The dashed red line marks the ¥100,000 stake and a red cross marks a bankruptcy. -->
<!-- [FIGURE:21] Figure 23: How much of each bargaining range models capture against each kind of supplier, over all 13,128 concluded agreements. Columns run from the easiest counterpart to the hardest, the deal count sits under each cell, and values in parentheses rest on fewer than 10 deals. -->
<!-- [FIGURE:22] Figure 24: Honest procurement money split over the six counterpart behavior templates, which run easiest to hardest on the field-wide surplus order of Figure 23 . Panel (a) gives every model’s five-run mean spend with honest suppliers as a share of its own honest total, that total printed at the right of each bar, models in descending total assets. Panel (b) pools the 90 episodes, ¥55.1M paid to honest suppliers, and sets the share each template received against the share of the 424 honest names that carry it, so a bar reaching past its mark was bought from more heavily than the supplier list alone would give. The hardest template takes 4.8 % 4.8\% of the spend against 11.3 % 11.3\% of the names and the easiest 18.5 % 18.5\% against 24.1 % 24.1\% . Spend with fraudulent suppliers is recorded separately and stays out of both panels. -->
<!-- [FIGURE:23] Figure 25: (a) The share of procurement spend that reaches fraudulent suppliers, cleanest model first, with whiskers over the five episodes. The dashed line is what a buyer who never screened would spend. (b) The same money split over the five scams, scaled within each model, with the cash it amounts to on the right. -->
<!-- [FIGURE:24] Figure 26: How fraudulent suppliers get through, 18 models and 5 episodes each, counted as distinct suppliers per episode. (a) Pale bars are suppliers contacted, solid bars suppliers ordered from, and the right column gives the share of contacts that became orders. (b) That share against fraudulent spend. (c) The number contacted against the same. -->
<!-- [FIGURE:25] Figure 27: (a) The deepest fall in total assets, as a share of that episode’s peak, against end-of-year total assets. Bubble area grows with the number of bankrupt episodes and the tinted band holds the five models that gave up more than half their peak. (b) Money left sitting in the platform wallet against days the bank balance was negative at the morning check. -->
<!-- [FIGURE:26] Figure 28: The same capability profiles for all 18 models, with a dashed polygon at the median. Axes clockwise from the top are profit, negotiation, fraud avoidance, solvency, efficiency, execution and learning, with fraud avoidance, solvency, execution and learning flipped so higher is better. -->
<!-- [FIGURE:27] Figure 29: How the ranking changes from one dimension to the next, all 18 models, rank 1 at the top of every column. Left labels give the profit order and right labels the order on sequential price discipline. Every column is signed so a higher position is better. -->
<!-- [FIGURE:28] Figure 30: How often each failure rule fires. Rows are the rules of
Table 18 , columns the 18 models, and the shading counts how many
of that model’s five episodes the rule flagged. Bold model names are proprietary
systems. The asterisk marks GPT-5.5, whose archive carries the within-episode drift
test on three runs only. -->

# Люди не узнают перевод ИИ, но доверяют человеку больше

## Когда ИИ уже почти не стыдно читать, но всё равно хочется человека

Вокруг машинного перевода литературы давно витает один и тот же вопрос: если нейросеть уже умеет более-менее точно передать смысл, значит ли это, что она умеет <strong>переводить роман как роман</strong> — с голосом, ритмом, атмосферой и тем самым ощущением, когда текст «несёт»?

Новая работа с прямолинейным выводом в названии отвечает честно: <strong>переводы ИИ уже «нормальные», но читатели всё равно чаще выбирают человеческий перевод</strong>. И это, пожалуй, самый интересный результат. Не потому, что «машины проиграли». А потому, что разрыв оказался куда тоньше, чем многим хотелось бы, и куда важнее — по каким именно причинам человек пока выигрывает.

Исследователи не стали измерять всё привычными автоматическими метриками. Вместо этого они посадили 15 активных читателей за реальные отрывки из современных романов — французских, польских и японских, переведённых на английский. Дали им сначала читать большие куски как обычную книгу, а потом — разбирать переводы вблизи, фрагмент за фрагментом. Получился редкий случай, когда вопрос о качестве перевода задали не моделям и не разметчикам, а <strong>самим читателям</strong>.

## Что именно проверяли

Авторы собрали набор из 15 книжных отрывков объёмом примерно по 8 тысяч слов. Для каждого был профессиональный опубликованный перевод на английский и машинный перевод, созданный не «одним запросом», а через многошаговый конвейер с LLM и агентами для программирования. То есть это не слабый базовый машинный перевод, а, скорее, одна из лучших доступных сегодня попыток сделать литературный перевод с помощью ИИ.

Сначала участники читали один вариант отрывка целиком, потом другой. После каждого оценивали, насколько текст гладкий, приемлемый для публикации, помогает ли он погружению и хочется ли читать дальше. Затем сравнивали обе версии напрямую. А через день возвращались к тем же текстам уже в режиме медленного чтения: смотрели на выровненные куски примерно по 300 слов, отмечали удачные и неудачные места и выбирали, какой вариант лучше.

[FIGURE:0]
[CAPTION:Схема эксперимента: сначала обычное чтение длинного отрывка, потом сравнение двух версий, а через день — внимательное сопоставление коротких фрагментов.]

Это важный дизайн. Обычно машинный перевод оценивают по коротким предложениям или абзацам. Но литература так не работает. Роман живёт не только в точности слов, а в том, насколько легко ты входишь в сцену, слышишь интонацию героя и не спотыкаешься каждые три строки. Авторы как раз и пытались поймать эту разницу между «в целом читается» и «это действительно хороший литературный перевод».

## Почему это вообще важно

Потому что машинный перевод художественных текстов уже не эксперимент из лаборатории. Издатели тестируют его для коммерческих книг. Платформы предлагают авторам быстро выходить на новые рынки. А значит, читатель очень скоро — а местами уже сейчас — может купить роман, не зная, насколько глубоко в его переводе участвовал человек.

Проблема в том, что привычные метрики здесь слабо помогают. Они неплохо улавливают адекватность смысла или общую гладкость. Но почти не видят, есть ли у текста дыхание, держит ли он темп, не разваливается ли голос повествования между абзацами. И вот эта работа показывает: <strong>если смотреть только на автоматические оценки, можно сделать слишком оптимистичный вывод о качестве ИИ-перевода</strong>.

## Как делали машинный перевод

Отдельно интересно, что исследователи не сравнивали людей с примитивной схемой «взяли модель и попросили перевести». Они сначала протестировали несколько вариантов конвейера и выбрали лучший.

Финальная схема выглядела так: текст делили на части, к нему добавляли стилистические указания, затем один агент переводил куски, другие проверяли качество — и с точки зрения точности, и с точки зрения литературности. Если находились проблемы, кусок отправляли на доработку. Потом собранный черновик ещё раз проверяли уже на уровне всего отрывка: на согласованность, цельность, сохранение голоса.

[FIGURE:2]
[CAPTION:Конвейер литературного перевода с ИИ: разбиение на части, перевод, локальная ревизия и финальная проверка целого текста.]

То есть перед нами не «сырое» машинное решение, а довольно дорогой и продуманный процесс. Именно поэтому результаты особенно показательны: даже при таком подходе человеческий перевод остаётся впереди.

## Главный результат: ИИ уже приемлем, но человек всё ещё лучше

Если смотреть на длинные отрывки целиком, преимущество человеческого перевода есть, но не разгромное: в 19 из 30 случаев читатели предпочли именно его. А вот при медленном чтении разница стала куда заметнее: из 772 сравнений коротких фрагментов <strong>522 оказались в пользу человеческого перевода</strong> и только 250 — в пользу машинного.

[FIGURE:5]
[CAPTION:Распределение предпочтений читателей: после чтения длинных отрывков и после медленного чтения коротких фрагментов человеческий перевод выигрывает чаще.]

Это очень показательно. Пока читаешь длинный кусок без прямого сравнения, машинный перевод часто кажется вполне нормальным. Он не обязательно раздражает. Он может быть гладким, понятным, местами даже увлекательным. Но когда два варианта ставят рядом, становится видно, где именно человек работает тоньше.

Авторы отдельно спрашивали, что именно лучше у одного или другого варианта. Человеческие переводы чаще получали высокие оценки за <strong>гладкость, ясность и погружение</strong>. Читатели чаще говорили, что такой текст «проще читать», что он не заставляет перечитывать фразу, лучше удерживает внутри сцены и естественнее звучит по-английски.

При этом машинный перевод вовсе не выглядел провалом. Примерно в трети фрагментов он побеждал. Иногда — из-за удачного локального выбора слова. Иногда — потому что звучал живее или точнее попадал в регистр реплики. То есть ИИ уже умеет делать <strong>хорошие отдельные решения</strong>. Но стабильности пока не хватает.

## Где именно человек выигрывает

Самая интересная часть работы — не голые проценты, а то, <strong>почему</strong> читатели выбирали один вариант вместо другого.

Человеческий перевод чаще выигрывал за счёт того, что текст легче течёт. Не в смысле «там меньше ошибок», а в смысле читательского опыта: не спотыкаешься, не вылетаешь из сцены, не пытаешься распутать странный порядок слов. Читатели постоянно отмечали ясность, естественность, ритм, удобство следования за действием и диалогами.

Машинный перевод, напротив, нередко страдал от локальных сбоев: слишком буквальная фраза, не тот оттенок слова, перегруженное предложение, внезапная шероховатость в диалоге. Причём ключевая проблема была не в том, что он всегда плох, а в том, что он <strong>неравномерен</strong>. Сегодня абзац отличный, через два абзаца — неловкая формулировка, которая ломает впечатление.

[FIGURE:8]
[CAPTION:У машинного перевода заметно больше фрагментов с высокой плотностью неудачных мест, отмеченных читателями как слабые.]

Авторы как раз измерили эту неравномерность через разметку «хороших» и «плохих» участков. Оказалось, что у машинного перевода слабые места гораздо чаще концентрируются плотными сгустками. То есть проблема не только в среднем качестве, а в том, что внутри одного и того же отрывка ИИ сильнее скачет от удачи к неудаче.

Для художественного текста это критично. В новостной заметке вы, возможно, простите пару странных фраз. В романе одна-две фальшивые ноты в нужный момент могут разрушить атмосферу сцены или смазать характер героя.

## ИИ трудно распознать — и это, возможно, самый тревожный вывод

Пожалуй, самый любопытный результат: читатели <strong>не смогли надёжно отличать машинный перевод от человеческого</strong>. После прямого сравнения двух версий они правильно угадывали машинный вариант лишь в 17 случаях из 30 — то есть почти на уровне случайности.

[FIGURE:15]
[CAPTION:Точность распознавания машинного перевода близка к случайной даже после сравнения двух версий текста.]

Более того, люди почти всегда считали, что предпочитаемый ими вариант сделан человеком. Это мощный психологический эффект. Мы не просто оцениваем текст — мы достраиваем вокруг него представление об авторстве, намерении и качестве.

Исследование показывает ещё одну забавную и важную вещь: читателей часто сбивали с толку ложные «признаки ИИ». Кто-то видел длинные тире и решал, что это машина. Кто-то думал, что ИИ «не станет так ругаться». Кто-то принимал за машинность просто непривычный стиль. Иными словами, народные теории о том, как «должен звучать ИИ», работают плохо.

Это важно не только для перевода. Вокруг текстов ИИ вообще много переоценённой уверенности: люди уверены, что распознают машинный текст, но на практике часто ошибаются.

## А что с автоматическими метриками? Всё плохо

Вот где работа особенно неприятна для любителей простых чисел. Исследователи сравнили читательские предпочтения с автоматическими метриками качества, включая подходы, где текст оценивает сама LLM. И оказалось, что <strong>метрики систематически склоняются в пользу машинного перевода</strong> — то есть фактически идут против человеческого чтения.

Это сильный сигнал. Если вы делаете продукт для издательства и смотрите только на автоматическую оценку, можно решить, что машинный вариант уже едва ли не лучше человека. Но живые читатели говорят обратное: да, читать можно, но человек по-прежнему даёт более лёгкий, ясный и погружающий опыт.

Причина понятна. Метрики хорошо видят близость к смыслу, формальную гладкость, иногда согласованность. Но они плохо улавливают то, что особенно важно в литературе: ритм, голос, ощущение естественного движения фразы, плотность слабых мест и то, как локальная шероховатость ломает общий эффект.

## Важная оговорка: это прежде всего история про перевод на английский

Авторы честно признают ограничения. Основной эксперимент — это переводы с французского, польского и японского <strong>на английский</strong>. А английский сегодня — самый сильный язык для LLM. И даже в этом «лучшем случае» человек всё равно выигрывает.

Когда исследователи сделали небольшой дополнительный разбор переводов в другие языки — французский, польский, испанский и японский, — преимущество человеческого перевода оказалось ещё заметнее. Там ИИ чаще ловили за руку и чаще отвергали.

Из этого следует простой вывод: если даже на английском разрыв сохраняется, то в других языковых направлениях он может быть ещё больше.

## Что в сухом остатке

Это очень трезвая работа. Она не впадает ни в технооптимизм, ни в алармизм.

Вывод звучит так: <strong>машинный перевод литературы уже достиг уровня «это можно читать»</strong>. Иногда он даже выигрывает. Иногда его трудно распознать. Иногда он выглядит удивительно сильным. Но если спрашивать не «понятен ли смысл», а «какой текст читатель хочет продолжать как роман», то преимущество остаётся за человеком.

Причём выигрывает человек не за счёт магии, а за счёт вещей, которые особенно важны в литературе: плавности, ясности, естественного выбора слов, удержания голоса и общей стабильности по ходу текста.

Для индустрии это, пожалуй, главный практический вывод. ИИ уже вполне годится как инструмент черновика, как помощник, как ускоритель работы. Но идея «давайте просто выпускать романы в машинном переводе, читатель не заметит» пока слишком самоуверенна. Читатель, может, и не всегда поймёт, где машина. Но когда рядом лежит хороший человеческий перевод, <strong>он всё ещё чаще выбирает его</strong>.

И, возможно, это лучший комплимент профессии переводчика из всех возможных.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1: Evaluation pipeline: Avid readers of published fiction evaluate two versions of an 8,000-word book excerpt: a human translation ( HT ) and an AI-generated machine translation ( MT ) . Participants (1) read the first translation, (2) complete a perception questionnaire, (3) read the competing translation, (4) complete a second questionnaire, (5) compare both versions, (6) take a one-day break, and (7) perform a side-by-side evaluation of 300-word chunks, selecting the preferred version with a justification and an indication of whether the choice was difficult. The presentation order is counterbalanced: each book is evaluated in both HT-first and MT-first conditions, and each reader evaluates two different books, encountering HT first for one and MT first for the other. -->
<!-- [FIGURE:1] Table 1: Summary statistics for the evaluation dataset. Words are whitespace-delimited counts. Tokens are computed with tiktoken ( o200k_base ). For SRC , we report only token counts, since Japanese cannot be split on whitespaces. -->
<!-- [FIGURE:2] Figure 2: Agentic literary MT pipeline used in this study. Source excerpts are chunked and paired with style guidance, then translated and revised through chunk-level and full-draft review loops. -->
<!-- [FIGURE:3] Figure 3: Study design and evaluation counts. Two readers evaluated each of the 15 book excerpts (30 book-reader evaluations). -->
<!-- [FIGURE:4] Table 2: Questionnaire items for human evaluation. Scales: 5-point Likert (5L); categorical with 2/3/4 options (2C/3C/4C); good/poor span labels (Span); free text (Open). See § D for the full wording. -->
<!-- [FIGURE:5] Figure 4: The distribution of readers’ preferences between the human translation ( HT ) and the machine translation ( MT ) after excerpt-level immersive reading and chunk-level close reading. The readers were judging which version they preferred and how strong the preference was. -->
<!-- [FIGURE:6] Figure 5: The distribution of readers’ ratings after immersive reading of each excerpt in isolation . The readers were judging acceptability (whether it is acceptable as a published translation), smoothness , immersiveness (whether it supported immersion), and continue (whether they would continue reading). -->
<!-- [FIGURE:7] Figure 6: The distribution of readers’ excerpt-level preferences for dialogue handling and word choice after reading both the human translation ( HT ) and the machine translation ( MT ) . The readers were judging which version handled dialogue better overall and which version had more varied or expressive word choice. -->
<!-- [FIGURE:8] Figure 7: Distribution of good and poor span highlights by source language and translation type. -->
<!-- [FIGURE:9] Figure 8: Share of close-reading chunks with dense poor-span evidence. For each threshold, the curve shows the percentage of HT and MT chunks with at least that many poor-highlighted words per 1K words. MT has substantially more high-density poor-span chunks. -->
<!-- [FIGURE:10] Figure 9: Distribution of span-level highlights in the close-reading task. Participants marked localized positive and negative evidence spans while comparing aligned HT and MT chunks, showing which parts of each translation supported or weakened their preference judgments. -->
<!-- [FIGURE:11] Table 3: Top labels behind reader preferences for HT or MT in excerpt- and chunk-level comparisons. Percentages are computed separately within each system and task from positive labels assigned to the chosen translation. Participant comments are shown in full with translation labels normalized to HT/MT, and colored highlights correspond to the code chips in the top-label list. -->
<!-- [FIGURE:12] Figure 10: Examples of span-level preference evidence from the side-by-side chunks evaluation. Participants compared aligned HT and MT chunks, labeled spans as good or poor , and chose the preferred translation. Green highlights indicate good spans and red highlights indicate poor spans. The examples show cases where both readers chose the same translation, one favoring HT and one favoring MT, while marking different local evidence for their choices. -->
<!-- [FIGURE:13] Figure 11: The most frequent labels in readers’ comments about the human translation ( HT ) and the machine translation ( MT ) . Rows separate single-reading praise, single-reading criticism, excerpt-level preference reasons, and chunk-level preference reasons. Comments could receive multiple labels. -->
<!-- [FIGURE:14] Figure 12: The cues readers mentioned when explaining which translation they believed was machine-translated ( MT ). Correct judgments identify the actual MT version; incorrect judgments identify the human translation ( HT ) as MT . Comments could receive multiple cue labels. -->
<!-- [FIGURE:15] Figure 13: Machine-translation (MT) identification accuracy and confidence in the single-reading questionnaire (n=60) and comparative questionnaire (n=30).
Colors represent confidence levels, from not at all to extremely confident. -->
<!-- [FIGURE:16] Table 5: Summary statistics for evaluation books, chunks, and participant free-text comments, split into a Words sub-table (whitespace-delimited word counts; we do not report SRC word counts because Japanese cannot be split on whitespaces) and a Tokens sub-table ( tiktoken o200k_base token counts). Books and chunks are reported separately for human-translated ( HT ), machine-translated ( MT ), and source-language ( SRC ) versions. The #/Bk (chunks per book) column does not depend on the metric and is identical across both sub-tables (and across HT / MT / SRC , since chunks are aligned across versions). Participant Comments include: Single Q5/Q6 are free-text responses from the single-reading questionnaires; Compar. Q4/Q7 are free-text responses from the comparison questionnaire; Chunk Justif. are per-chunk preference justifications. -->
<!-- [FIGURE:17] (a) Guidelines: Page 1 -->
<!-- [FIGURE:18] (a) Guidelines: Page 1 -->
<!-- [FIGURE:19] (b) Guidelines: Page 2 -->
<!-- [FIGURE:20] (c) Guidelines: Page 3 -->
<!-- [FIGURE:21] (d) Guidelines: Page 4 -->
<!-- [FIGURE:22] (a) Guidelines: Page 5 -->
<!-- [FIGURE:23] (a) Guidelines: Page 5 -->
<!-- [FIGURE:24] (b) Guidelines: Page 6 -->
<!-- [FIGURE:25] (c) Guidelines: Page 7 -->
<!-- [FIGURE:26] (d) Guidelines: Page 8 -->
<!-- [FIGURE:27] (a) Guidelines: Page 9 -->
<!-- [FIGURE:28] (a) Guidelines: Page 9 -->
<!-- [FIGURE:29] (b) Guidelines: Page 10 -->
<!-- [FIGURE:30] (c) Guidelines: Page 11 -->
<!-- [FIGURE:31] (d) Guidelines: Page 12 -->
<!-- [FIGURE:32] Figure 17: Single-reading questionnaire shown after an immersive reading. Participants rated fluency, literary quality, immersion, willingness to continue reading, and whether the passage seemed AI-generated. -->
<!-- [FIGURE:33] (a) Comparative questionnaire -->
<!-- [FIGURE:34] (a) Comparative questionnaire -->
<!-- [FIGURE:35] (b) Per-chunk close-reading questionnaire -->
<!-- [FIGURE:36] Figure 19: Median span highlight length in the multilingual case study. Bars show the median length of good and poor spans marked for HT and MT by target language. -->
<!-- [FIGURE:37] Figure 20: Span-level annotations by target language in the multilingual target-language case study. Bars show the proportion of good and poor spans marked in HT and MT for each target language. -->
<!-- [FIGURE:38] Figure 21: Book-level preferences in the multilingual case study.
Each row is one book–participant pair; left/right bars indicate MT/HT preference, with darker shades marking stronger choices. -->
<!-- [FIGURE:39] Figure 22: MT identification by book. Orange bars show HT identified as MT, green bars show MT identified as MT, and darker shades indicate higher confidence. -->
<!-- [FIGURE:40] (a) Positive aspects -->
<!-- [FIGURE:41] (a) Positive aspects -->
<!-- [FIGURE:42] (b) Negative aspects -->
<!-- [FIGURE:43] (a) Excerpt-level preferences -->
<!-- [FIGURE:44] (a) Excerpt-level preferences -->
<!-- [FIGURE:45] (b) Chunk-level preferences -->
<!-- [FIGURE:46] (a) Excerpt-level preferences -->
<!-- [FIGURE:47] (a) Excerpt-level preferences -->
<!-- [FIGURE:48] (b) Chunk-level preferences -->
<!-- [FIGURE:49] Figure 26: Close-reading chunk-level preferred translation. Each cell shows one chunk comparison for an excerpt and reader. Green indicates HT preference, purple indicates MT preference, and darker shades indicate stronger preference. -->
<!-- [FIGURE:50] Figure 27: Preferred translation by excerpt and reader. Bars show the share of chunk-level choices favoring MT on the left and HT on the right; darker shades indicate greater preference strength. -->
<!-- [FIGURE:51] Figure 28: Per-book immersive-reading ratings for HT and MT. The figure breaks down participant ratings by book, making cross-book variation visible alongside the aggregate trends reported in the main paper. -->
<!-- [FIGURE:52] Figure 29: Immersive-reading ratings by presentation order. The figure compares ratings assigned after the first and second single readings, grouped by whether the human translation (HT) or machine translation (MT) was shown first. -->
<!-- [FIGURE:53] (a) Guess correctness -->
<!-- [FIGURE:54] (a) Guess correctness -->
<!-- [FIGURE:55] (b) Guess confidence -->
<!-- [FIGURE:56] Figure 31: Multilingual case-study identification outcomes. Single-reading results for HT/MT identification in the multilingual case study; darker shades indicate higher confidence. -->
<!-- [FIGURE:57] Figure 32: Close-reading preferences in the multilingual case study. Stacked bars show chunk-level preferred translation choices for HT and MT across the four evaluated translation directions, with color intensity indicating preference strength. -->
<!-- [FIGURE:58] Figure 33: More likely AI-translated choices in the comparative questionnaire. After both readings, readers chose which version seemed more likely AI-translated. Orange bars show incorrect HT choices; green bars show correct MT choices, with darker shades indicating higher confidence. -->
<!-- [FIGURE:59] Figure 34: Close-reading chunk-level preferred translation by source language. Each pair of bars shows HT and MT preference shares within a source language; stacked segments show preference strength, and labels report counts and percentages. -->
<!-- [FIGURE:60] Figure 35: Chunk-level preferred translation in the multilingual target-language case study. Each row shows one excerpt-reader pair; green indicates HT preference, purple indicates MT preference, and darker shades indicate stronger preference. -->

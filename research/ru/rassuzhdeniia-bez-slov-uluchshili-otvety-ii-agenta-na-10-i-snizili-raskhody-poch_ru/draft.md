# Рассуждения без слов улучшили ответы ИИ-агента на 10% и снизили расходы почти в 4 раза

## Агент думает без слов и всё ещё умеет пользоваться инструментами

ИИ-агенту приходится выбирать между двумя неудобствами. Если он рассуждает текстом, его мысли проще проверять, но длинные цепочки слов занимают время и вычислительные ресурсы. Если он рассуждает во внутреннем пространстве представлений модели, то может делать это быстрее, но ход рассуждений сложнее понять, а вызовы инструментов всё равно нужно оформлять текстом.

Авторы предлагают объединить оба режима в одном агенте. Внутренние шаги он выполняет в скрытом пространстве, а для общения с внешней средой — например, для поиска в интернете или запуска кода — переключается на текст. Система сама решает, когда использовать каждый режим.

В испытаниях по математике, науке и медицине, а также в задачах с поиском HybridAgent показал более высокую точность, чем сопоставимые текстовые агенты. При этом он использовал на 35,5–54,7% меньше текстовых токенов и, по оценке авторов, работал в 1,8–2,6 раза быстрее.

## Два режима для одной задачи

Обычный языковой агент строит весь ответ из токенов: рассуждения, запросы к инструментам и итоговый ответ. В гибридном подходе часть рассуждений происходит без перевода в обычные слова. Модель берёт внутреннее представление текущего шага, преобразует его и снова подаёт на вход. Так она продолжает рассуждать, не записывая каждый промежуточный шаг.

Для перехода между режимами авторы добавили небольшой модуль **HybridLink**. Он связывает внутренние представления модели с пространством, в котором та принимает входные токены. В текстовом режиме агент генерирует обычные слова. В скрытом — передаёт внутренние представления по кругу. Специальные маркеры позволяют начать и завершить скрытый фрагмент.

Внешние действия остаются текстовыми. Чтобы выполнить поиск или запустить программу, агент формулирует вызов инструмента, получает результат и продолжает работу. Так роли разделяются: **скрытый режим нужен для внутренних рассуждений, текстовый — для действий и проверки человеком**.

[FIGURE:0]
[CAPTION:HybridAgent переключается между внутренними рассуждениями в скрытом пространстве и текстом для вызова инструментов.]

## Как агент сохраняет контекст

Для многошаговой задачи недостаточно переключаться между режимами: нужно ещё помнить, что происходило раньше. Обычный текстовый агент может добавлять ответы инструментов к текстовой истории и перечитывать её на следующем шаге. Но скрытые представления нельзя просто вставить в такую историю как слова.

Авторы используют рабочую память модели — кэш, в котором хранятся данные, нужные для продолжения вычислений. В него попадают текст, скрытые шаги и ответы инструментов. После обращения к поиску или программе агент продолжает работу с тем же кэшем. Переводить всю историю обратно в текст не нужно.

Для обучения авторы подготовили 54 тысячи примеров, преобразовав готовые последовательности действий агентов в чередование текстовых и скрытых фрагментов. Шаги, которые важно показать для проверки или вызова инструмента, оставляли текстовыми. Остальные могли перевести в скрытый режим. Размечать данные помогали языковые модели-судьи и оценки уверенности самой модели.

Затем HybridAgent дообучали в два этапа. Сначала **HybridSFT** учил модель переключаться между режимами и работать с HybridLink. Здесь есть важная деталь: во время обычного обучения модель видит правильные примеры скрытых шагов, а при реальной работе должна продолжать собственными предсказаниями. Если эти предсказания немного отличаются от примеров, ошибка может накапливаться.

Чтобы уменьшить разрыв, авторы применили обучение с самоподстановкой. Сначала модель делает пробный проход, а затем на втором проходе получает собственные скрытые представления вместо правильных примеров. Так её учат работать в условиях, близких к реальному использованию.

На втором этапе, **HybridRL**, агент обучается с подкреплением. Он получает награду за правильный ответ, соблюдение формата и полезное использование инструментов. Награды за выбор скрытого или текстового режима нет: модель сама учится определять, где уместен каждый режим.

## Результаты испытаний

Авторы проверили три размера модели — 4, 8 и 14 миллиардов параметров — на 11 бенчмарках. Среди задач были математические соревнования, научные и медицинские вопросы, поиск по нескольким источникам и работа с инструментами.

В задачах с поиском HybridAgent с 14 миллиардами параметров в среднем обошёл сильнейший сопоставимый агентный метод на 17,4%. В математике и ответах на вопросы по знаниям он также превзошёл текстовые и скрытые методы, обученные на похожих данных. После обучения с подкреплением точность на MATH500 достигла 84,6% для модели с 8 миллиардами параметров и 88,2% для модели с 14 миллиардами.

Результаты по эффективности зависят от того, что именно считать. В общем сравнении авторы сообщают о снижении числа текстовых токенов на 35,5–54,7% и ускорении инференса в 1,8–2,6 раза. В отдельном сравнении с текстовыми агентами система использовала примерно в 2,7 раза меньше текстовых токенов и сокращала число шагов генерации до 54%. Расчёт вычислительных затрат на генерацию показал экономию в 2,7–3,7 раза. Эти оценки основаны на заданных авторами ценах на GPU и не учитывают подготовку входного контекста и работу внешних инструментов.

[FIGURE:6]
[CAPTION:HybridAgent уменьшает число текстовых токенов и шагов генерации по сравнению с текстовыми агентами.]

Авторы также пытаются сохранить проверяемость скрытых рассуждений. Каждый скрытый шаг можно приблизительно представить ближайшим по смыслу словом из словаря модели. Получается псевдотекст: он не обязательно выглядит как гладкая фраза, но позволяет увидеть, связаны ли внутренние шаги с задачей. По оценкам авторов, после обучения такие представления становятся понятнее и лучше соответствуют исходному вопросу.

Проверки показали, что скрытые шаги участвуют в решении. Если заменить их случайными представлениями или шагами от другой задачи, точность на MATH500 заметно падает. Например, замена скрытых шагов фрагментами от другого вопроса снижает точность примерно на 45–47%. Значит, содержание и порядок скрытых представлений влияют на ответ.

Видимого текста при этом достаточно, чтобы проверить ход решения. По сравнению с текстовым агентом HybridAgent выдавал на 43–49% меньше текстовых токенов, но в видимых фрагментах сохранял больше ключевых шагов на каждые сто токенов. В большинстве случаев проверяющие модели могли найти первую ошибку и предложить полезную поправку. Однако это результат испытаний на выбранных задачах, а не доказательство того, что скрытые рассуждения всегда можно надёжно проверить.

[FIGURE:1]
[CAPTION:Скрытые шаги можно приблизительно прочитать как псевдотекст и сопоставить с соседними объяснениями и вызовами инструментов.]

## Вывод

HybridAgent показывает, как устроить агента, которому не нужно проговаривать каждый шаг, чтобы действовать во внешней среде. Он может использовать скрытые представления для внутренних вычислений, а текст оставлять для вызовов инструментов, важных решений и итогового ответа.

Такой подход усложняет обучение и саму систему. Нужны новый модуль, специальный режим дообучения и программная обвязка, которая сохраняет общую память при переходах между скрытым режимом, текстом и ответами инструментов. Псевдотекст позволяет лишь приблизительно прочитать скрытые представления и не гарантирует, что человек увидит точную причину каждого решения.

Результаты проверяли на моделях Qwen3 и конкретных задачах, с заданными настройками и инструментами. Пока неясно, насколько легко подход перенести на другие модели и реальные длительные рабочие процессы.

**Рассуждения агента можно частично вывести из текстового потока, сохранив текст для действий и проверки.** Это может снизить затраты на генерацию и повысить точность. Для надёжного применения важно понимать, что именно остаётся видимым человеку и насколько хорошо скрытые шаги продолжают направлять ответы.

[FIGURE:5]
[CAPTION:С ростом числа попыток качество HybridAgent на сложных математических и научных задачах продолжает повышаться.]

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1 : HybridAgent Architecture Overview. Left: A HybridLink maps last-layer hidden states back into the input embedding space, letting the agent enter latent mode for recurrent, fast, inspectable inner thinking and return to text mode for tool calls and external monitoring . Right: HybridAgent performs hybrid reasoning that thinks in latent space and acts through text within a single generation process.
Building on this architecture, HybridAgent (i) achieves multi-turn hybrid generation by carrying the entire hybrid context through its own working memory (Section 3 ), and (ii) can be converted from any standard pre-trained LLM through a dedicated post-training pipeline (Section 4 ). -->
<!-- [FIGURE:1] Figure 2 : Interpretable Latent Mode in HybridAgent. All latent steps can be expressed as readable pseudo-text carrying their semantics for external inspection. Left: Quantitatively, latent thoughts are highly readable and context-specific (see Appendix F ). Right: Qualitatively, latent pseudo-text stays semantically aligned with surrounding text reasoning and tool calls. (“Steps” counts forward passes). -->
<!-- [FIGURE:2] Figure 3 : Multi-Turn Hybrid Generation over HybridAgent’s Own Working Memory. HybridAgent accumulates key-value (KV) entries from text, latent thoughts, and tool observations in continuous working memory, directly reusing and updating it across turns to preserve the full hybrid context. -->
<!-- [FIGURE:3] Figure 4 : Self-Conditioned HybridSFT. A teacher-forced first pass produces next-step latent inputs via HybridLink. A second pass replaces ground-truth latent embeddings Emb ( ⋅ ) (\cdot) with the predictions ℛ ⁡ ( h ) \mathcal{R}(h) and jointly trains the backbone and HybridLink using CE at text and regression at latent positions. -->
<!-- [FIGURE:4] Figure 5 : Scalability of HybridAgent at Test-time. We evaluate pass@k ( 4 , 8 , 16 , 32 , 64 4,8,16,32,64 ) performance on 100 hard math and science questions and compare with text agents trained with GRPO. -->
<!-- [FIGURE:5] Figure 6 : Efficient Hybrid Generation of HybridAgent across Model Scales. HybridAgent reduces both text-token usage and total generation steps compared with matched text-based LLM agents. -->
<!-- [FIGURE:6] Figure 7 : Inference time speedup of HybridAgent across all model scales. -->
<!-- [FIGURE:7] Figure 9 : Training Dynamics of HybridRL. As training progresses, HybridAgent shifts more generation from text to latent mode while increasing reward and tool use. These trends reflect how HybridAgent adaptively learns to allocate its reasoning and tool calling efforts across the two modes. -->
<!-- [FIGURE:8] Figure 10 : Agentic Tool-Use Analysis on HybridAgent. Left : Valid tool-call rate across 8B and 14B scales; "Execute Success" measures error-free execution among valid tool calls. Middle : Final-answer accuracy on questions where the agent performs at least one tool call. Right : Useful tool-call rate, measuring the fraction of tool calls whose execution results contain the final answer. -->
<!-- [FIGURE:9] Figure 11 : Train-Inference Mismatch in Latent Reasoning. We illustrate the exposure bias that arises when teacher-forced training meets free-running inference. Left: During activation, the backbone consumes ground-truth embeddings Emb ⁡ ( y ) \mathrm{Emb}(y) at latent positions, while HybridLink outputs ℛ ⁡ ( h ) \mathcal{R}(h) are only trained to match their targets and never fed back as inputs. Right: At inference, every latent input is the model’s own ℛ ⁡ ( h ) \mathcal{R}(h) , so deviations from the target embeddings accumulate across the span. -->
<!-- [FIGURE:10] Figure 12 : Hybrid Data Curation Pipeline. We convert text-based demonstrations into multi-turn hybrid trajectories using complementary signals from LLM judgments and model entropy to assign reasoning modes, followed by a visibility audit that preserves decision-critical steps in text mode. -->

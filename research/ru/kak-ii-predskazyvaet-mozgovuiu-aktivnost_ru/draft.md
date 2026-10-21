# Как ИИ предсказывает мозговую активность

## Как научить модель предсказывать ответы мозга

Пока человек смотрит сериал, его мозг обрабатывает изображение, речь, музыку и смысл происходящего. Можно ли по самому видео, звуку и субтитрам предсказать, как в этот момент изменится активность разных областей мозга?

Такие модели уже умеют строить. Но обычно их обучают осторожно: берут большую нейросеть, оставляют её веса неизменными и учат только небольшой модуль, который переводит внутренние представления модели в сигналы мозга. Новый подход предлагает дать данным мозга немного изменить саму нейросеть — и показывает, что для этого не нужно переобучать её целиком.

В статье исследователи применили **малое дообучение** к мультимодальным моделям, которые понимают видео, аудио и текст. На данных магнитно-резонансной томографии мозга во время просмотра фильмов этот подход улучшил предсказания на девяти моделях. Специальная схема вычислений помогла обучать их быстрее и собирать ансамбли из сотен вариантов.

## Зачем менять большую модель

Модель кодирования мозга получает стимул — например, сцену из фильма — и предсказывает реакцию мозга. Для этого ей нужны хорошие представления о том, что происходит на экране и в звуке. Большие предварительно обученные модели уже умеют извлекать такие признаки, поэтому исследователи часто оставляют их неизменными и обучают только выходной слой.

Это бережёт данные. Записи активности мозга дороги, а примеров обычно слишком мало, чтобы надёжно обновлять миллиарды параметров. Полное дообучение может потратить эти данные впустую и ухудшить результат. Но у замороженной модели есть обратная проблема: её представления не приспособлены специально для предсказания мозга.

Авторы предлагают промежуточный вариант. **Веса большой модели остаются на месте, но небольшие добавочные модули учатся подстраивать её работу.** Один из таких методов называется LoRA. Его идея — внести в модель ограниченное изменение, которое задаётся небольшим числом параметров. Так данные мозга влияют на представления, но модель не приходится обучать заново целиком.

[FIGURE:0]
[CAPTION:Модель можно оставить замороженной или адаптировать небольшими модулями; подход масштабируют за счёт более крупных моделей и множества специализированных вариантов.]

## Как сократить вычисления в 350 раз

Эксперименты проводили на записях активности мозга четырёх людей, которые смотрели эпизоды сериала «Друзья». Данные разделили на обучающую часть, проверку на шестом сезоне и тест на седьмом сезоне. Отдельно оценили перенос на фильмы другого типа. Активность мозга представили в виде сигналов для тысячи областей.

Главная вычислительная трудность — длина видео. Чтобы предсказать сигнал мозга в конкретный момент, прежний подход снова и снова обрабатывал перекрывающиеся отрывки фильма. Один и тот же контекст попадал в модель сотни раз. Авторы заменили эту схему одним проходом по временному окну: модель получает отрывок целиком и сразу выдаёт признаки для многих моментов.

Такое ускорение возможно благодаря устройству модели. Она обрабатывает последовательность с причинной маской: при вычислении представления для одного момента не должна использовать будущие слова и кадры. Значит, вычисления для соседних моментов можно переиспользовать, вместо того чтобы каждый раз начинать обработку окна заново.

На одной видеокарте извлечение признаков сократилось примерно с 700 до 2 часов. Это ускорило именно обработку видео и звука: обучение всей системы заняло около 8,5 часа против примерно 702 часов у прежней схемы. Разница в качестве тоже важна. Одного прохода без дополнительного контекста оказалось недостаточно, особенно в начале окна. Авторы добавили до минуты материала перед целевым отрывком — так модель получала нужный контекст и сохраняла точность.

[FIGURE:1]
[CAPTION:Один проход по временному окну заменяет повторную обработку перекрывающихся отрывков.]

## Малое дообучение улучшает предсказания

В основном эксперименте исследователи добавили модули LoRA в модель Qwen3-Omni и обучили их вместе с компактным выходным слоем. Всего обучались 61,2 миллиона параметров. У прежнего лидирующего подхода, который оставлял большую модель замороженной, выходной модуль содержал 1,1 миллиарда параметров.

На тесте с новыми эпизодами новая модель получила корреляцию 0,327 между предсказаниями и измеренной активностью мозга. Предыдущий результат составлял 0,310. На новых фильмах, которые модель не видела при обучении, показатели составили 0,228 и 0,217 соответственно. Корреляция показывает, насколько похожи изменения предсказанного и измеренного сигналов.

Разница не ограничилась одной моделью. Исследователи проверили девять мультимодальных моделей размером от 4,7 до 104 миллиардов параметров. Малое дообучение улучшило результат каждой из них. При этом размер модели сам по себе не объяснял качество: больше параметров не всегда означало более точное предсказание.

Авторы также сравнили LoRA с полным дообучением. Полное обновление модели с 20,3 миллиарда параметров не дало преимущества, хотя требовало обучать в 330 раз больше параметров. Для имеющегося объёма данных небольшого изменения оказалось достаточно.

[FIGURE:2]
[CAPTION:Добавочные модули улучшили результаты на всех девяти проверенных моделях.]

Есть и проверка на перенос. Модель, обученная на данных трёх участников, почти полностью сохраняла прирост на четвёртом, которого она не видела при дообучении. Авторы также испытали её на другом наборе данных — с другими участниками, сканером и фильмом. Без дополнительного обучения новый модуль увеличил долю объяснённого сигнала мозга на 11,1 процентного пункта относительно предельного уровня, заданного шумом измерений.

## Что модель узнаёт о мозге

Мультимодальная модель смешивает информацию из изображения, звука и текста. Поэтому по её ответу не сразу понятно, какой вход повлиял на предсказание активности конкретной области мозга. Авторы оценили вклад каждого потока отдельно: по очереди убирали содержимое видео, аудио и текста и измеряли, как меняется качество предсказания.

Распределение получилось знакомым нейробиологам. Зрительная кора в основном реагировала на видео, а слуховая — на аудио. В боковых височных областях звук тоже оказался важнее текста. Значит, даже внутри общей мультимодальной модели можно выделить связи между типом стимула и участком мозга.

После дообучения доля аудио в предсказаниях выросла в среднем на 39%, а доля текста снизилась на 17%. Изменилась и работа самой модели: информация из одного потока чаще попадала в представления, связанные с другим. Например, содержимое видео могло влиять на признаки, расположенные на месте аудиотокенов.

Это не означает, что модель воспроизводит работу мозга. Авторы показывают более ограниченный результат: небольшое дообучение меняет то, как модель использует разные виды входных данных, и эти изменения связаны с тем, какие сигналы помогают предсказывать активность отдельных областей.

[FIGURE:3]
[CAPTION:Анализ вкладов связывает видео, аудио и текст с разными областями мозга и показывает, как дообучение меняет их сочетание.]

## Зачем обучать сотни моделей

Даже точная модель может ошибаться там, где другая справляется лучше. Поэтому авторы обучили 261 вариант с разными настройками, выходными слоями и базовыми моделями, а затем объединили их предсказания.

Чтобы обучение не превратилось в сотни отдельных прогонов, исследователи создали вычислительное ядро для одновременной работы с разными наборами LoRA. На одном и том же общем основании оно обновляет много адаптеров за один проход. При 32 адаптерах такой шаг был почти в 30 раз быстрее последовательного обучения. По времени он стоил примерно столько же, сколько обучение одного адаптера на той же совокупности примеров.

Ансамбль из 261 модели достиг корреляции 0,343 на новых эпизодах и 0,248 на новых фильмах. Авторы сообщают, что на момент подготовки статьи это был лучший результат в открытом рейтинге соревнования «Алгонавты». Но точность ансамбля зависела не только от количества моделей, но и от качества отдельных участников и от того, насколько по-разному они ошибались. Новые выходные слои и базовые модели давали больше разнообразия, чем смена случайного начального состояния.

[FIGURE:4]
[CAPTION:Совместное обучение множества адаптеров ускоряет сборку ансамбля, а его точность зависит от числа моделей, их качества и разнообразия ошибок.]

## Вывод

**Большую модель можно приспособить к ограниченным данным мозга, не обновляя её целиком.** В этих опытах малое дообучение улучшило предсказания на девяти мультимодальных моделях и превзошло предыдущий подход, обучая намного меньше параметров. Однопроходная обработка видео снизила вычислительные затраты, а совместное обучение адаптеров позволило собрать большой ансамбль.

Результаты пока ограничены: основная проверка опирается на фильмы и данные четырёх участников. Перенос на другой набор данных обнадёживает, но не показывает, как метод сработает на других видах стимулов и записях мозга. Работа предлагает практичный путь: использовать сильную готовую модель, менять её небольшими модулями и собирать разные варианты там, где особенно важно качество предсказаний.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1 : From frozen backbones to PEFT, and three directions to scale PEFT for brain encoding. (a) The dominant paradigm: a frozen pretrained backbone with readouts trained for brain encoding. The backbone prior is strong, but it is not specialized for brain encoding. (b) We advocate using PEFT to adapt strong pretrained backbones, retaining the powerful prior while allowing flexible neural adaptation.
This suggests three complementary scaling directions: Scale up to stronger priors leveraging more capable backbones; Scale down the size of trainable adapters for brain encoding with limited data; and Scale out the number of adapters with different specializations. -->
<!-- [FIGURE:1] Figure 2 : One causally masked pass replaces a sliding window. The baseline re-encodes an overlapping window per fMRI timestep; a single pass over the window gives features at every timestep. -->
<!-- [FIGURE:2] Figure 3 : Adaptation improves performance on nine tested backbones. All backbones share the same training configuration except for the feature extraction layer (App. 15 ). LoRA improves the performance consistently. -->
<!-- [FIGURE:3] Figure 4 : Modality attribution recovers the canonical topography, and adaptation reweights and mixes the modalities. (a) Contribution to encoding accuracy of the video, audio, and text content, on our LoRA+linear model, left hemisphere (lateral above, medial below). (b) Modality contribution by region. The Shapley terms from the three modalities and a small layout residual sum to the region’s r r . (c) Change in modality contribution from the frozen to the adapted model. Audio contribution increases the most, while text falls. (d) Share of the prediction carried from each stimulus modality (left) to the backbone’s output at each modality’s tokens (right), which is the readout’s input. Crossing ribbons are cross-modal mixing within the backbone, which nearly doubles after adaptation. -->
<!-- [FIGURE:4] Figure 5 : Scaling out: training a population of adapted models. (a) Training-step time for N N rank-16 adapters on a shared backbone: one fused batched gather-matmul vs. N N sequential runs. The fused step matches the cost of a single adapter on the same batch (App. 9 ). (b) Ensemble performance vs. ensemble size, averaged over random subsets of the 261 adapted models, which is nearly a straight line in the log-log space (App. 13 ). (c) Performance of 2,000 random 20-model ensembles vs. the performance predicted linearly on two properties of their members: mean single-model accuracy (quality) and mean pairwise residual correlation (diversity). Neither factor predicts ensemble accuracy alone ( R 2 R^{2} 0.23 and 0.05), but together they predict the performance well ( R 2 = 0.97 R^{2}{=}0.97 ). -->
<!-- [FIGURE:5] Figure 6 : Accuracy within the window. Accuracy against TR position inside the 149 s window for three input designs, scored with the same frozen MIRAGE head on Friends s06 (606 complete interior windows; the band is the s.e.m. over windows for the no-lead configuration). The dashed box marks the first 10 s, where the designs differ. Accuracy here is the per-TR spatial correlation between predicted and measured 1000-parcel patterns, which is defined at a single time point; it is not comparable to the per-parcel headline metric. Without a lead, a window starts 0.110 below its plateau and needs about five TRs to reach it. With a 30 s lead it starts 0.048 below plateau, and with the whole clip 0.051. The first window of each clip is excluded because of a clip-onset transient. -->
<!-- [FIGURE:6] Figure 7 : Accuracy against cost. Held-out Friends S7 accuracy against trainable parameters (a) and against end-to-end compute including feature extraction (b) , both on log scales. Published baselines are squares and our models circles; an N N -model ensemble is plotted at N N times a member’s cost. -->
<!-- [FIGURE:7] Figure 8 : Multi-adapter kernel benchmark. Qwen3-Omni truncated at the feature extraction layer, rank-16 adapters on q / k / v / o q/k/v/o , sequence length 128, one sample per adapter, one A800, median of 5 timed steps after 2 warm-up steps. (a) One fused batched gather-matmul over N N different adapters (blue) matches the same batch through one adapter (grey); running the N N jobs one at a time (orange) grows linearly in N N . (b) The ratio of the fused pass to the single-adapter batch is 1.00 × 1.00\times throughout, up to run-to-run noise of ± 0.03 \pm 0.03 . -->
<!-- [FIGURE:8] Figure 9 : Cross-seed agreement. Mean agreement between adapters over the 15 seeds of the main configuration (105 pairs). (a) At successive levels of the model, from near zero for the weights to near one for the prediction. Levels below the first are cosines between the two seeds’ changes relative to the frozen model, averaged over the audio, video, and text streams. (b) Agreement at every decoder layer, per stream. It
rises through the adapted stack, peaks at the feature extraction layer, and declines slowly through the 16 frozen layers above it. -->
<!-- [FIGURE:9] Figure 10 : Performance against the noise ceiling on NNDb. 20 participants, readout re-fitted per participant on the fixed backbone, over the 816 parcels with an estimable ceiling. (a) Subject-mean r r per parcel against the corrected noise ceiling (dashed line). (b) Mean percentage of the ceiling per Yeo network. -->
<!-- [FIGURE:10] Figure 11 : Validation r r by region, with and without the adapter. Frozen backbone and the same configuration with LoRA, over the n n parcels of each region (Tab. 17 ); bars show the gain, printed at the right. (a) The seven Yeo networks. (b) Ten coordinate-defined ROIs. One run per configuration, paired per parcel; every gain’s 95%
functional-block bootstrap interval excludes zero. -->
<!-- [FIGURE:11] Figure 12 : All subsets of the three input streams. Subject-mean Pearson r r on the 250 validation windows used for attribution, with absent streams replaced by their training-mean embeddings. The top bar of (a) is the full model (dashed line). (a) Any single stream recovers most of the full score, and removing one costs far less than that stream achieves alone: the streams are largely redundant. (b) Cost of removing each stream, before and after adaptation. The video cost barely changes, the audio cost grows, and the transcript cost falls by more than a third. This removes a stream from a trained model and differs from the no-audio configuration of Tab. 2 , which is trained without audio throughout. -->
<!-- [FIGURE:12] Figure 13 : Audio contribution by region, before and after adaptation. Subject-mean contribution of the audio stream to encoding accuracy for the
frozen and LoRA + linear models, with episode block-bootstrap intervals;
labels give the relative change. Auditory cortex gains least; the gain is
largest in regions that relied least on audio before adaptation. -->

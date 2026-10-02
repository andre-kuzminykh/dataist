# Можно ли автоматически собрать нужных ИИ-агентов по ходу работы

## ИИ-агенты собираются в команду

Сложную задачу часто нельзя решить одним универсальным агентом. Чтобы создать игру, например, нужно изучить требования, написать код, подготовить графику, собрать части проекта и проверить результат. Каждый шаг требует своих инструментов и навыков. А ещё важно передать результаты дальше так, чтобы следующий участник понял, на что опираться.

Авторы Raven предлагают строить системы именно так: как команду из специализированных ИИ-агентов, которые умеют работать вместе. Исследовательский агент ищет информацию, агент для программирования пишет и проверяет код, дизайнер готовит визуальные материалы. Отдельный управляющий агент разбивает запрос на задачи и связывает их в общий план.

Ключевая идея — считать отдельным рабочим модулем **модель вместе с её обвязкой**: инструментами, памятью, правилами выполнения и проверками. Тогда можно подключать разных агентов, не заставляя их работать по одному сценарию.

## Как Raven собирает рабочий план

Управляющий агент описывает задачи в виде графа. Узлы — вызовы отдельных агентов, а стрелки показывают, какие результаты нужны для следующих шагов. Независимые задачи можно выполнять параллельно; зависимые запускаются, когда готовы их входные данные.

Например, если нужно сделать сайт о научной работе, два исследовательских агента могут отдельно изучить алгоритмы и способы их оценки. Агент для программирования дождётся обоих отчётов и соберёт эксперимент. Дизайнер подготовит страницу на основе результатов. Управляющий агент объединит готовые материалы.

Перед запуском система проверяет структуру плана: все ли задачи описаны, существуют ли нужные зависимости, подходит ли выбранный агент и может ли он работать с указанными файлами. Это помогает отсеять ошибки в графе до того, как агенты начнут тратить время и вычислительные ресурсы.

Результаты передаются как файлы и записи с понятными связями. Так агенту не приходится полагаться на пересказ управляющего агента или заново получать длинный отчёт в своём запросе. Для каждой задачи сохраняются инструкция, результат и ход работы. Если позже понадобится продолжить проект, можно обратиться к уже готовому результату или возобновить работу агента с сохранённым контекстом.

[FIGURE:1]
[CAPTION:В Raven специализированные агенты выполняют узкие задачи, а управляющий агент связывает их результаты в общий план.]

Есть и защита от ситуации, когда исполнитель объявляет работу законченной, хотя нужного файла или результата нет. После вызова отдельный проверяющий агент смотрит на запрос, ответ и часть истории выполнения. Если результата не хватает, управляющий агент может дать исполнителю дополнительные инструкции, отказаться от задачи или перестроить оставшийся план.

Но такая проверка оценивает, выполнена ли задача в заявленном смысле, а не всегда — верен ли результат по существу. Поэтому для кода нужны тесты, для исследования — проверка источников, а для дизайна — просмотр готового изображения.

## Обвязка может улучшаться

Raven включает метод изменения обвязки агента, пока сама языковая модель остаётся неизменной. Можно менять четыре части: работу с памятью, планирование, выбор доступных инструментов и действия агента, включая проверку завершения.

Если агент регулярно заканчивает работу без ответа или не запускает тесты после правки кода, система ищет способ исправить именно это поведение. Она создаёт варианты обвязки, проверяет, сработало ли изменение, и сравнивает результат с прежней версией на одних и тех же задачах. Лучшие варианты проходят более полную проверку на обучающем наборе. Затем выбранную обвязку замораживают и оценивают на отдельных задачах, которые не участвовали в настройке.

Так, в опытах HarnessBank с неизменной моделью Qwen3.6-27B улучшенная обвязка повысила долю решённых задач на семи проверках. На AppWorld прирост составил 15,4 процентного пункта, на BrowseComp+ — 13,9, на LiveCodeBench — 13,7. По SWE-bench Verified показатель вырос на 5,1 пункта, но эта разница не прошла критерий, использованный авторами для оценки прироста.

[FIGURE:7]
[CAPTION:Обвязка меняется вокруг неизменной модели, а новые варианты проходят проверку перед оценкой на отложенных задачах.]

У метода есть ограничения. Он выбирает варианты по результатам обучения и не гарантирует, что улучшение повторится на новых задачах. Авторы также отмечают, что подробные настройки отдельных опытов HarnessBank опубликованы не полностью. Поэтому эти цифры показывают возможности подхода, но не дают полной картины того, сколько стоило получить каждый результат.

## Память хранит опыт, навыки превращают его в инструкции

У Raven два вида памяти. Первый помогает сохранять сведения о пользователе: его предпочтения, ограничения и контекст прошлых разговоров. Второй записывает опыт самого агента: какую задачу он выполнял, что делал и какой вывод можно использовать в дальнейшем.

Сначала переписка делится на смысловые части. Из них создаются короткие описания эпизодов и отдельные факты. Похожие эпизоды объединяются, чтобы система могла восстановить не только конкретный факт, но и контекст, в котором он появился. При поиске Raven использует и совпадения слов, и близость смысла, а потом возвращает найденный факт вместе с эпизодом, к которому тот относится.

Из повторяющегося опыта агент может получить **навык** — инструкцию для определённого класса задач. Например, случаи, когда нужно изменить проект и проверить правку, могут со временем превратиться в процедуру: сначала воспроизвести ошибку, затем внести небольшое изменение и запустить тесты.

Для навыков Raven обращается к трём источникам: локальной библиотеке, памяти агента и общему каталогу SkillHub. Найденные материалы объединяются, а управляющий механизм выбирает подходящие для текущей задачи. Если выбор не срабатывает, система использует отдельное правило: берёт несколько наиболее высоко оценённых вариантов из списка.

Каталог SkillCorpus, на котором основана часть экспериментов, содержит 96 401 активный навык. Перед добавлением материалы проверяли на дубликаты, качество и потенциально опасные инструкции. В опытах с фиксированной библиотекой навыки повышали результат на всех трёх проверках: SkillsBench, GDPval и QwenClawBench. На SkillsBench прирост Raven составил 6,5 и 13,4 процентного пункта для двух размеров модели. На GDPval прибавка была скромнее — от 1,2 до 1,9 пункта во всех проверенных сочетаниях агента и модели.

[FIGURE:10]
[CAPTION:Поиск памяти сначала находит подходящие эпизоды, а затем выбирает факты, сохраняя их исходный контекст.]

## Что показывают испытания

Чтобы отдельно проверить работу управляющего агента, авторы создали бенчмарк из 140 задач. В каждой нужно выбрать специалистов и определить, какие результаты должны предшествовать другим. Raven сравнили с Claude Code и Hermes Agent на двух языковых моделях, не запуская самих исполнителей: оценивался только составленный план.

Raven показал лучший результат по всем четырём показателям на обеих моделях. На одной Exact Match — доля планов, совпавших с допустимым эталоном по составу специалистов и зависимостям, — составил 71,1% против 60,7% у лучшего соперника. На другой — 86,7% против 76,2%. Это говорит о том, что Raven точнее выбирал исполнителей и связывал их задачи. Однако бенчмарк проверяет планы, а не качество итоговой работы команды.

Профильные агенты оценивали отдельно. Raven-Research отвечал на вопросы с опорой на сведения в интернете. На DeepResearch Mixed с моделью DeepSeek-V4-Flash он набрал 76,5% точности. Сильнейший из сравниваемых агентов на той же модели получил 68,9%. При этом стоимость одного ответа Raven оценили в 0,0242 доллара: немного дороже одного соперника и дешевле другого. Пять из шести сопоставлений на одинаковых моделях дали статистически значимое преимущество; в шестом разница в 3,3 пункта не прошла такую проверку.

Raven-Code проверяли на задачах по программированию, включая исправление ошибок и перенос целого проекта на новый технологический набор. На SWE-bench Pro он решил на 15 задач больше, чем Claude Code с той же моделью. На SWE-Refactor результаты Raven превышали опубликованные показатели других систем на 9,5 пункта для DeepSeek-V4-Flash и на 3 пункта для GPT-5.6 Luna. Здесь важно учитывать, что часть сравнений сделана с внешними результатами, а настройки и условия работы систем различались.

Raven-Design создаёт слайды, сайты и визуализации с предварительным просмотром результата. На PresentBench он получил 80,2 балла с Claude Opus 5 и 72,9 с GPT-5.6 Luna. Во втором случае Claude Code набрал 52,4. Оценка проверяет не только внешний вид: в ней учитываются полнота, точность и соответствие исходному материалу.

Raven-Oncall отвечает за долгие вычислительные задачи, например запуск обучения и наблюдение за его ходом. В наборе из 17 научных задач он успешно выполнил 14 с Claude Opus 5; Claude Code — 11. Такие сравнения зависят от конкретных задач, инструментов и правил оценки, но показывают, зачем системе отдельный исполнитель для работы, которая продолжается часами.

## Вывод

Raven предлагает **собирать ИИ-системы из специализированных агентов, связанных явными зависимостями**, и сохранять их опыт для следующих задач. Управляющий агент строит план, исполнители передают результаты как артефакты, а обвязки и навыки могут меняться без обновления самой модели.

Результаты выглядят многообещающе, особенно в планировании и профильных задачах. Но испытания проводились на разных наборах данных и по разным протоколам. Некоторые сравнения опираются на опубликованные таблицы других систем, а дополнительные слои памяти и обратной связи пока не проверены в полном составе.

Практический вопрос остаётся открытым: дают ли несколько агентов лучший итог, чем один хорошо оснащённый агент, если считать общую стоимость — включая планирование, проверки, повторы и передачу результатов. Теория Raven описывает условия, при которых такое объединение может расширить круг решаемых задач. Проверить, насколько часто эти условия выполняются в реальной работе, должны будущие сравнительные испытания.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1: Raven performance overview. Selected results for
multi-agent orchestration, research, coding, design, and on-call tasks,
compared with the strongest reported alternative in each setting. -->
<!-- [FIGURE:1] Figure 2: Raven As An Open Multi-Agent Ecosystem. (a) Built-in and third-party agents expose executable model–harness
pairs through execution adapters. The Host Agent uses registry
capabilities to compose and assign tasks, while the runtime validates
the plan, schedules ready nodes, and records artifacts for handoff
and reuse. (b) An illustrative FPS game project combines gameplay
development and visual design before integration, testing, and
operation. Nodes denote agent calls, and directed edges denote
artifact dependencies coordinated by Raven. Persistent context,
reusable skills, and harness evolution support adaptation across tasks. -->
<!-- [FIGURE:2] Figure 3: Harness composition. (a) A model and its harness form a callable
execution unit. (b) A host assigns and coordinates these units. Solid
arrows carry artifacts and dashed arrows denote control. The
research–code–design chain is an illustrative plan with explicit final
synthesis by a specialist. All operations share one budget. Model labels
need not identify different foundation models. -->
<!-- [FIGURE:3] Figure 4: Graph planning and admission. (a) The host context carries
only a summary of the orchestration guide. The host loads the full
guide when a request needs several agents and delegates directly
otherwise. A rejected graph returns its first error with a pointer back
to the guide. In the admitted graph, R1 and R2 are the running example’s
research nodes v alg v_{\mathrm{alg}} and v bench v_{\mathrm{bench}} , C is v code v_{\mathrm{code}} , and D is v design v_{\mathrm{design}} . (b) A submission is a flat node list with graph-level
flags. Five groups of checks run in order before any worker is
dispatched ( Table 1 ). -->
<!-- [FIGURE:4] Figure 5: Node execution and host intervention. (a) A node runs once all
predecessors have completed and settled. Returned output and raised
errors both reach the judge. A failed verdict suspends the node for a
host decision when continuations remain. Memory recording runs
asynchronously and does not delay successors. (b) Top: the judge reads
the rendered prompt, output, and transcript tail, and a negative verdict
becomes an exception report for the host. Bottom: a worker’s
clarification request is answered from the host’s conversation and
memory when possible, and otherwise reaches the user. -->
<!-- [FIGURE:5] Figure 6: Artifact and memory flow. (a) A node’s prompt is rendered from
its template, upstream outputs, upstream memory paths, and files. The
runtime writes the prompt, output, and transcript to disk, and a memory
record follows asynchronously. Successors read these files on demand.
(b) The host receives a run report with paths and terminal outputs.
Completed nodes enter a session-wide registry, so a later graph can
reference their outputs and a single delegation can continue their
instance. In (b), R3 and R4 are research nodes of a follow-up graph
whose slide-deck node P references earlier outputs, and the spawn call
continues the coding instance C. -->
<!-- [FIGURE:6] Figure 7: Shared group memory. (a) The host mediates access to
owner-partitioned EverOS libraries. It retrieves experience before
planning, deposits round summaries and outcomes in its shared library,
and writes agent assessments to the corresponding agent libraries.
Dispatch prefetch combines shared experience with recent assessments
from a provenance ledger, with respective caps k group k_{\rm group} and k verdict k_{\rm verdict} . Personal user memory is excluded, while
workers retain their ordinary memory access. Offset outlines indicate
one library and worker per mapped agent.
(b) Assessment has two phases: a close verdict after execution and a
feedback verdict on the next user turn. Attribution is extracted from
the host’s reply and omitted from the user-visible response and session
log. -->
<!-- [FIGURE:7] Figure 8: Harness self-evolution. (a) Four strategy interfaces expose
decisions around a frozen model. The shared execution shell handles dispatch and
accounting. (b) The best training-evaluated harness supplies failure
traces for diagnosis and candidate generation. The bank stores one
complete harness per edit-category/pathology cell. P/K/R/C denote
prompt, knowledge, runtime, and configuration edits. The first N keep N_{\rm keep} candidates passing validity, activation, and paired-gain
screening receive full-training evaluation before cell competition,
where N keep N_{\rm keep} is the per-round survivor cap.
The final training-selected harness is frozen before held-out testing. -->
<!-- [FIGURE:8] Figure 9: Memory formation and consolidation in EverOS.
(a) Semantic boundaries group dialogue and tool interactions into a
source segment 𝗌𝖾𝗀 i \mathsf{seg}_{i} . Its episode 𝖾𝗉 i \mathsf{ep}_{i} anchors atomic
facts. The dashed branch derives optional foresight with validity
interval [ t p , 0 , t p , 1 ] [t_{p,0},t_{p,1}] .
(b) Across interaction history 𝖧𝗂𝗌𝗍 \mathsf{Hist} , episodes, shown as
points, form MemScenes around centroids marked by crosses.
These scenes select evidence for profile updates.
The agent track consolidates execution cases c 1 , c 2 , c 3 c_{1},c_{2},c_{3} into
reusable procedures, depicted by a small dependency graph.
The diagram shows representation and data dependencies.
Persistence and indexing proceed separately. -->
<!-- [FIGURE:9] Figure 10: Raven’s user-memory retrieval through EverOS hybrid .
(a) BM25 and dense search retrieve episodes. Reciprocal rank fusion
(RRF) determines their expansion order. A separate calibrated score
ranks them for final selection.
(b) The query scores facts belonging to each expanded episode.
Episodes and facts compete within a bounded candidate set. A selected
fact is returned under its parent episode, which restores its context.
The positive integer k mem k_{\rm mem} is the backend candidate-set cap. -->
<!-- [FIGURE:10] Figure 11: Skill selection and experience-driven updates.
(a) Ranked source hits are grouped by name and fused before body
retrieval, runtime policy checks, and LLM selection. The normal
gate selects a bounded list, while a gate failure uses a separate
ranked fallback. Resource resolution is attempted after selection.
(b) A case enters an intent cluster and conditions skill operations
together with existing skills and a bounded set of supporting cases.
Persisted revisions become candidates for later
EverOS retrieval after indexing. The positive integer k pool k_{\rm pool} is the fused skill-pool cap. Numeric labels show the implementation
defaults in Section B.3 . -->
<!-- [FIGURE:11] Figure 12: MAOB composition. (a) Number of domains per task and the share of
tasks whose reference graph contains parallel branches. (b) Number of
tasks that use each specialist domain. -->
<!-- [FIGURE:12] Figure 13: Multi-Agent Orchestration Benchmark results with backbone
(a) Qwen3.8-27B and (b) DeepSeek-V4-Flash-0731 . -->
<!-- [FIGURE:13] Figure 14: Held-out Pass@1 reported in HarnessBank [ 39 ] for the initial and evolved harnesses with a frozen Qwen3.6-27B backbone.
Gray denotes SWE-bench Verified. Table 11 lists the values. -->
<!-- [FIGURE:14] Figure 15: Raven-Research results on DeepResearch Mixed. (a) Accuracy per
source under DeepSeek-V4-Flash . (b) Paired accuracy gain of Raven-Research over
each comparison on the same backbone, with stratified bootstrap 95%
intervals over all questions. The hollow marker denotes the comparison
with DeepSeek-Harness on Qwen3.5-397B-A17B , with exact McNemar p = 0.21 p=0.21 .
(c) Accuracy against mean cost per question,
with filled markers for the DeepSeek-V4-Flash harnesses and hollow markers for
the commercial services, whose costs follow each provider’s own
accounting. -->
<!-- [FIGURE:15] Figure 16: Coding results. Each row is one system, grouped by benchmark and
backbone. SWE-bench reports the resolved rate, WorkBuddy-Code the reward,
and SWE-Refactor the mean task score. Hollow markers are public
leaderboard values. -->
<!-- [FIGURE:16] Figure 17: DataAgentBench Pass@1 on August 24, 2026, with the horizontal
axis starting at 0.76. The comparison entries are the public leaderboard
values on that date, and the right column gives their models. -->
<!-- [FIGURE:17] Figure 18: PresentBench overall scores (0–100). Gold bars are Raven-Design and
dark bars Claude Code, with the backbone in parentheses. Light bars are
public leaderboard entries evaluated by the benchmark authors, whose model
configurations are not given. -->
<!-- [FIGURE:18] Figure 19: Visual-design scores (0–100) under (a) GPT-5.6 Luna and (b) Claude Opus 5 .
Scores come from an internal grader with GPT-5.6 Luna as the judge and are
not comparable with the official leaderboards. -->
<!-- [FIGURE:19] (a) Song Dynasty -->
<!-- [FIGURE:20] (b) Greek Polychromy -->
<!-- [FIGURE:21] (c) Pop Music -->
<!-- [FIGURE:22] (d) Abstract Art -->
<!-- [FIGURE:23] (e) Orchestration Frameworks -->
<!-- [FIGURE:24] (f) Light Pollution -->
<!-- [FIGURE:25] (g) GPS Trilateration -->
<!-- [FIGURE:26] Figure 21: AI4AI nanochat pretraining. (a) Final validation BPB of each campaign,
starting from 1.108 (dashed line). (b) Runtime, reported tokens, and USD cost.
Lower is better throughout. The lighter bars use the DeepSeek backbone. -->
<!-- [FIGURE:27] Figure 22: AI4S internal benchmark. Success rate on the 17 tasks, and
runtime, tokens, and USD cost averaged per task. The lighter bars use
the DeepSeek backbone. -->
<!-- [FIGURE:28] Figure 23: Effect of the curated skill library reported by SkillCorpus [ 64 ] . Each arrow runs from the no-skill baseline
(hollow marker) to the condition with SkillCorpus skills for one
harness–backbone cell. Values are three-run means. Horizontal axes
start at different values. Table 12 lists the values. -->

# Как ИИ-агент сам улучшает интерфейсы

## Интерфейс, который учится вместе с ИИ-агентом

Представьте, что вы просите агента сверить письма с банковскими операциями. Он открывает почту, нажимает на письма, прокручивает страницы и переносит данные на глаз. Хотя нужная информация уже есть в почте, агент не умеет получить её одним запросом.

Такие обходные пути — обычная проблема компьютерных агентов. Им приходится работать через заранее заданные кнопки, снимки экрана и инструменты. Если интерфейс неудобен, модель может хорошо рассуждать, но всё равно тратить десятки шагов на простые действия.

Авторы статьи предлагают изменить сам способ доступа агента к компьютеру. Их система Agent S4 изучает попытки агента, замечает повторяющиеся трудности и создаёт новые программные интерфейсы. Например, вместо нажатий на письма такой интерфейс может сразу вернуть их список и содержимое в виде текста.

[FIGURE:0]
[CAPTION:Agent S4 изучает попытки агента и меняет набор доступных ему интерфейсов.]

## Интерфейсы становятся частью обучения

Обычно способы взаимодействия с компьютером проектируют люди. Они решают, какие действия доступны агенту, какую информацию тот получает в ответ и как пользоваться инструментами. Сама модель может меняться, но набор интерфейсов часто остаётся прежним.

Из-за этого агенту приходится приспосабливаться к ограничениям инструментов. Чтобы изменить таблицу, он может нажимать на ячейки и проверять результат по снимкам экрана, хотя мог бы сразу передать программе диапазон данных. Чтобы найти нужную функцию в файле, он может вывести в окно терминала весь его текст.

**Agent S4 предлагает поручить агентам улучшение интерфейсов.** Результат сохраняется в репозитории: там лежат программный код инструментов и пояснения, которые помогают понять, когда и как их применять. Модель и её обвязка при этом остаются прежними. Меняется то, что агент может увидеть и сделать.

Систему составляют два агента. Первый выполняет задачи на компьютере. Второй — метаагент — изучает записи этих попыток и вносит изменения в репозиторий. Он может добавить интерфейс, изменить существующий или объединить решения из двух разных вариантов.

Метаагент не получает правильных ответов на учебные задачи и не знает, успешно ли агент выполнил каждую из них. Он видит ход работы: действия, снимки экрана, вывод инструментов и ошибки. По этим данным он ищет повторяющиеся проблемы. Например, если агент много раз вручную редактирует отдельные ячейки, можно создать функцию для массового изменения таблицы.

Новые версии проверяют на отдельных проверочных задачах. Их промты, результаты и объяснения ошибок скрыты от метаагента. Проверочные задачи влияют только на выбор версий, которые система будет развивать дальше. Так авторы стараются снизить риск, что новый интерфейс поможет только на задачах, для которых его создали.

[FIGURE:2]
[CAPTION:Схема отбора новых версий: метаагент меняет репозитории, а проверочные задачи помогают выбрать, какие развивать дальше.]

## Что меняется на практике

В процессе работы Agent S4 не просто накапливает отдельные приёмы. Он меняет сами действия и ответы инструментов. Вместо кнопок и снимков экрана агент может получить содержимое страницы, данные из приложения или подтверждение, что операция прошла успешно.

В одном примере агенту нужно было собрать сведения о расходах из почты и банковской системы. Агент с обычным набором инструментов открывал письма по одному, проходил предупреждения при скачивании файлов и прокручивал список операций. Версия с улучшенным интерфейсом получила текст писем и ссылки на вложения через браузер, скачала документы и извлекла из них текст. Затем она использовала тот же подход, чтобы получить банковские операции.

[FIGURE:4]
[CAPTION:Фиксированный набор инструментов заставляет работать через нажатия и снимки экрана, а новые интерфейсы дают доступ к данным напрямую.]

Изменения затронули и специализированные программы. Для научного бенчмарка система добавила инструменты для географической информационной системы, молекулярной программы ChimeraX и математического приложения KAlgebra. Например, агент мог выполнить команду в открытой карте и получить статистику текстом, а не искать консоль и проверять результат на экране.

Репозитории развивались не только последовательными правками. Система сохраняла разные версии и иногда возвращалась к старой ветке или объединяла подходы из двух веток. Это позволяло не терять ранние решения, которые могли оказаться полезными позже.

## Результаты на двух бенчмарках

На OSWorld V2, где собраны 108 многошаговых задач с реальными компьютерными приложениями, одна и та же модель Qwen3.8-27B показала разные результаты в зависимости от интерфейса. С фиксированным набором она полностью решала 5,56% задач. С репозиторием, созданным Agent S4 без доступа метаагента к пробной виртуальной машине, результат вырос до 21,3%.

Средние расходы на решение задачи составили 1,10 доллара. Для сравнения, в приведённых авторами результатах GPT-5.5 полностью решает 13% задач при расходах 25,50 доллара, а Claude Opus 4.8 — 20,6% при расходах 72,40 доллара. Эти сравнения относятся к конкретным настройкам и запускам бенчмарка: они показывают разницу в данном эксперименте, а не универсальный рейтинг моделей.

[FIGURE:1]
[CAPTION:Доля полностью решённых задач и стоимость одного задания на OSWorld V2.]

На ScienceBoard систему проверяли на 169 задачах в шести научных приложениях. С исходным репозиторием тот же агент справился с 55,03% задач, а с улучшенным — с 58,58%. Это умеренный прирост. Он показывает, что система может находить полезные интерфейсы и для программ, которые не входят в обычный набор офисных приложений.

Авторы также сравнивали разные способы развития репозитория. Доступ к пробной виртуальной машине помогал метаагенту открывать приложения и проверять новый код. В одном запуске это повысило долю частично решённых задач на OSWorld V2, но лучшая доля полностью решённых задач получилась в запуске без такой машины. Иными словами, возможность проверить интерфейс сама по себе не гарантирует, что он лучше справится с новыми задачами.

## Где заканчиваются доказательства

Результаты измеряют эффект сразу от нескольких изменений в репозитории. Исследователи не всегда могут отделить вклад конкретного инструмента от других правок. Примеры, где новый интерфейс сокращает десятки действий до нескольких вызовов, помогают понять возможную причину улучшения, но это отдельные случаи, а не строгие сравнения на всех задачах.

Важно и то, как устроена оценка. Проверочные задания влияют на выбор репозитория, хотя метаагент не видит их напрямую. Поэтому разделение данных снижает риск подгонки, но не отменяет его полностью. Кроме того, оценка стоимости учитывает вызовы модели при решении задач, но не расходы на создание и проверку репозиториев.

Интерфейсы могут давать агенту широкий доступ к данным и приложениям. Это повышает скорость работы, но требует контроля прав и последствий действий. В описанных экспериментах за разрешения, выполнение кода и ограничения отвечала обвязка. Этот уровень контроля остаётся важным: агенту, который может обращаться к почте или изменять документы программно, нужны чёткие границы доступа.

## Вывод

Agent S4 показывает, что прогресс компьютерных агентов зависит не только от самой модели. Иногда агенту полезнее дать способ получать нужные данные напрямую, чем заставлять его точнее нажимать мышью.

Система учится создавать такие способы доступа по записям работы, сохраняет их в репозитории и проверяет новые варианты на отдельных задачах. На двух бенчмарках это улучшило результаты, особенно на OSWorld V2. Следующий вопрос — насколько надёжно такой подход переносится на другие приложения и насколько безопасно агенты могут расширять собственные инструменты.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1 : Conventional computer-use agents execute tasks through fixed, human-designed interfaces. Agent S4 evolves interfaces as software repositories through experience. A task agent attempts synthetic tasks, and a meta-agent studies its trajectories to construct and refine the repositories. Each repository combines interfaces, such as GUI interactions, file operations and application-specific workflows, with knowledge of when to use them. -->
<!-- [FIGURE:1] Figure 2 : With Evolving Agent Interfaces built by Agent S4, Qwen3.8-27B exceeds GPT-5.5 and Opus 4.8 in binary success on the challenging OSWorld V2 benchmark at a small fraction of their cost. -->
<!-- [FIGURE:2] Figure 3 : Agent S4 turns task experience into an evolving repository of interfaces and knowledge. Starting from parents selected by held-out validation, the meta-agent
studies their task trajectories to identify limitations, then revises one
repository through mutation or combines ideas from two through crossover.
Task agents then use the descendant to produce trajectories on synthetic
tasks and a separate score on held-out validation tasks. Each descendant
joins the population alongside its parents, allowing earlier designs to be
revisited and recombined over successive iterations. -->
<!-- [FIGURE:3] Figure 4 : Interface discovery and extension across 30 candidates per population run. a , New interfaces (blue): distinct coherent interfaces absent from the seed, labeled by their implemented scope across the run. b , Interface extensions (orange): newly introduced operations first recorded after their interface’s introduction, each labeled independently by its own behavior. -->
<!-- [FIGURE:4] Figure 5 : Human-curated versus Evolved Interface. Top: the Qwen CUA baseline uses a fixed, human-designed interface prioritizing frequent screenshots with mouse and keyboard actions. It reads the receipts and searches the card charges through repeated GUI interactions (steps 21–111).
Bottom: Prime Agent with the repository evolved by Agent S4. It reads the mailbox and the bank records through the evolved browser interface, whose browser.api sends requests from inside the already logged-in tab and returns the data as text (calls 17 and 44). It fetches the attachments with curl , and reads them with pdftotext . -->
<!-- [FIGURE:5] Figure 6 : Repeated validation separates a high first score from
consistent performance. Red shows the best first-evaluation score on
ScienceBoard and blue the best mean over repeated evaluations. -->
<!-- [FIGURE:6] Figure 7 : Useful repositories can emerge by returning to an earlier branch. OSWorld V2 lineage over 30 construction steps with scratch-VM access.
Blue nodes denote mutation and orange nodes crossover; solid and dashed
edges identify the first and second parents. Dashed node outlines mark
eliminated variants. The bars report mean partial score and binary
success on 15 validation tasks. Step 24 combines steps 2 and 6 and reaches
the highest partial score ( 50.2 % 50.2\% ), while tying the best binary success
( 26.7 % 26.7\% ). Vertical dashed lines mark the seed scores; the shaded band
uses the ± 1 \pm 1 standard error estimated from the same validation set and
model in the run without scratch-VM access. -->
<!-- [FIGURE:7] Figure 8 : ScienceBoard evolution combines branches under repeated validation. Repository lineage over 30 construction steps with a 60-minute episode
limit. Colors and edge styles follow Figure 7 .
Bars show each repository’s mean success across its available evaluations
on 15 validation tasks, including repeats where available; they need not
equal the scores available when the repository was selected as a parent.
The dashed line marks the seed’s initial 53.3 % 53.3\% success. The crossover
at step 16 has the highest mean, 71.7 % 71.7\% over four evaluations. -->
<!-- [FIGURE:8] Figure 9 : How the task agent uses an evolved repository. (a) On an
OSWorld V2 task, the task agent lists the available interfaces, reads the
usage notes of one and calls it from its code. Outputs are shortened. (b) The repository selected without a scratch VM
(Table 2 ) is a Python package. Each interface is a
module of functions whose docstrings say how and when to use them, including
lessons from earlier trajectories. Docstrings are shortened. run_batch , api and the lofile module were added
during evolution. -->
<!-- [FIGURE:9] Figure 11 : Reusing CDP access reduces the setup needed to read the
same message. Selected milestones from task 046 compare the seed’s
client implementation and debugging with the evolved repository’s
existing browser helpers. Both retrieve the requested direct message,
at tool cells 37 and 11 respectively. Times run from the initial task
message to the tool result containing that message. Boxes summarize
recorded events and are not proportional to elapsed time; the evolved
agent also encounters and corrects an initial JavaScript error. -->
<!-- [FIGURE:10] Figure 12 : Reading a mailbox in MailHub ( s_010 ). The seed agent reads the case
emails through the GUI in 60 calls (8–67). Its first six clicks land above
the email list because it uses coordinates from its 1200-pixel screenshots as
screen coordinates. A click meant for the inbox opens Starred, and its attempt
to read the page from code is refused with 403 Forbidden . With if-011 , page_text lists the inbox and one cdp_eval call fetches the mailbox with full email bodies inside the
logged-in tab, in 12 calls and without a screenshot. -->
<!-- [FIGURE:11] Figure 13 : Exporting an XMind map ( s_005 ). The seed agent tries to export
a PNG through XMind’s menus in calls 249–299. Its click on the Export
submenu lands between PNG and JPEG, and an “Export to JPEG” panel opens.
Its clicks on Cancel miss, and the episode ends at the call limit without an
image. With if-029 from a separate evolution run, the agent builds
the map with xmind.build_map and save_map , and one call
to xmind.render_png writes the image. -->
<!-- [FIGURE:12] Figure 14 : Reading a Zotero library ( s_007 ). The seed agent checks items and
notes through the GUI in 42 calls (59–100). Nine clicks meant for the Cancel
button of a plugin dialog miss (calls 61–79), and the agent closes the
dialog with an Escape key press at call 82. Later it clicks outside the
screen and asks a vision model to locate the Notes tab. With if-029 from a separate evolution run, zotero.list_collections and list_items return the library as data in one call. The interface
covers reading only: on this build the API rejects writes. -->
<!-- [FIGURE:13] Figure 15 : Submitting a review in ReviewSphere ( s_022 ). The seed agent’s clicks meant
to close two popups open a software-store window, and its click on Write
Review misses until it rescales the coordinates. It then writes its own
Chrome client to fill the form; Chrome first refuses the connection with 403 Forbidden , and the form is filled at call 37. With if-026 from a separate evolution run, calls 5–26 read the page,
open the form, fill six fields, check them, and submit, mostly through browser.chrome_js , with no failed calls. -->
<!-- [FIGURE:14] Figure 16 : Resolving tracked changes in a Word document ( s_026 ). The seed agent reads the raw
document XML and rebuilds insertion and deletion elements by hand in calls
17–28; its comments XML fails to parse at call 24. With if-030 from a separate evolution run, the agent lists the changes with redline_list , then accepts eight and rejects six with accept_redlines and reject_redlines in one call. -->
<!-- [FIGURE:15] Figure 17 : Accessing a TeamChat tab (OSWorld V2 task 038 ). The bare agent repeatedly clicks the
MailHub tab while trying to activate TeamChat, then hits TeamChat’s close
control. With if-024 , call 14 uses browser.chrome_cdp with a tab ID to read the general-channel rules without switching tabs
through the screen. Later pinned-rule checks and CRM updates remain.
The full episodes take 94 and 95 model steps and receive task scores of
0.6517 and 0.70, respectively. -->
<!-- [FIGURE:16] Figure 18 : Plotting a function in KAlgebra ( KAlgebra:A-02 ). The seed agent’s Add click lands in the graph,
and repeated clicks target the color control instead of the expression
input. It eventually finds the input and plots y = ln ⁡ ( x ) 2 y=\ln(x)^{2} in
calls 64–67. With if-016 , call 8 uses rest.kalgebra_add_2d to add the curve and rest.kalgebra_functions_2d to read it back; call 10 shows
the resulting plot. Both episodes pass, in 68 and 11 model steps,
respectively. -->
<!-- [FIGURE:17] Figure 19 : Storing a calculation in KAlgebra ( KAlgebra:C-01 ). The seed agent repeatedly clicks above the
calculator input and sends test characters before correcting the
coordinates and storing log 2 ⁡ ( 3 ) \log_{2}(3) in p . With if-016 , kalgebra.evaluate_lines enters the expression through the GUI
and checks the variable. Its first attempt reports p missing;
the agent selects the Calculator tab and retries, confirming p=1.58496250072 at call 17. Both episodes pass, in 40 and
21 model steps, respectively. -->
<!-- [FIGURE:18] Figure 20 : Computing raster statistics in GRASS GIS ( GrassGIS:B-12 ). The seed agent locates the GUI console,
corrects its typing method, and retries Return until it focuses the
command input and obtains the statistics. With if-016 , call 8
runs r.univar map=lakes through grass.grass_run against the live mapset and returns the statistics as text, including n=263975 and sum=263975 . The evolved agent also runs
the command through the GUI in calls 15–18. Both episodes pass, in
40 and 21 model steps, respectively. -->

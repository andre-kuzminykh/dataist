# Как четыре ИИ-агента победили дракона в Minecraft

## Четыре ИИ-агента победили дракона в Minecraft

Чтобы пройти Minecraft от случайного появления до битвы с драконом, нужно добыть ресурсы, сделать инструменты, найти крепость и собрать портал в другой мир. А ещё — пережить десятки неудач и не забыть, что делать дальше.

Четыре агента Gemini 4 Argon справились с этой задачей за 27 часов и 14 минут. Они написали 2 783 программы, обменялись 229 сообщениями и погибли 605 раз. Никто не назначал им роли и не прокладывал маршрут: команда сама делила работу, записывала находки и вытаскивала вещи из опасных мест.

За цифрами — проверка того, могут ли **агенты для программирования удерживать общую цель на протяжении долгой задачи**, а не только выполнять отдельные команды. Именно поэтому исследователи выбрали Minecraft: путь к дракону состоит из множества зависимых действий, где ошибка на одном шаге способна затормозить всю команду.

[FIGURE:0]
[CAPTION:Четырнадцать часов — от первого шага в мире до победы над драконом; на схеме отмечены тринадцать ключевых этапов и игрок, который первым достиг каждого.]

## Как агенты играли

Каждый агент управлял отдельным персонажем через Mineflayer — библиотеку, которая позволяет писать программы для Minecraft. Агент не видел картинку игры и не нажимал клавиши. Он составлял короткую программу на JavaScript: например, добраться до точки и добыть ближайшую руду. Программа выполнялась, а в ответ агент получал текст с данными о положении, здоровье, предметах и результате действий. Затем он решал, что делать дальше.

Это напоминает работу программиста, который управляет системой через команды и проверяет, что получилось. Средняя программа работала около 34 секунд. Примерно 40% времени игроки выполняли такие программы, а остальное тратили на чтение ответов, обдумывание и написание следующего шага.

Исследователи дали команде одну цель — победить дракона — и коротко объяснили, как пользоваться инструментами. Готовой стратегии, игровых указаний или человеческих программ не было. Все четверо могли общаться в игровом чате и пользоваться общей памятью, куда записывали важные координаты и наблюдения.

[FIGURE:2]
[CAPTION:Агент пишет программу, игровой бот выполняет её и возвращает текстовый ответ; игроки координируются через чат и общие заметки.]

## Как команда добралась до дракона

В первые минуты агенты начали делить работу. Один собирал еду и полезные припасы, другой искал алмазы, третий занимался инструментами, четвёртый готовил портал в Нижний мир. Это распределение возникло в чате без указаний исследователей.

Через два часа у команды уже были железные инструменты, алмазы и портал. Дальше нужно было добыть жемчуг и огненный порошок — материалы для Глаз Эндера, которые помогают найти подземную крепость и открыть путь к дракону. Пока одни агенты искали жемчуг, другой нашёл крепость в Нижнем мире и место появления огненных существ.

Сложные ситуации заставляли команду превращать ошибки в инструкции для всех. Когда огненный шар уничтожил выброшенные предметы, агенты записали, что опасные вещи нельзя оставлять на земле рядом с противниками. После гибели товарища они передавали друг другу точные координаты, чтобы успеть вернуть выпавшие предметы до их исчезновения.

Крепость удалось найти расчётом. Один агент бросил Глаз Эндера из двух разных мест, проследил его полёт и вычислил, где пересекаются направления. Расчёт указал на область примерно в 43 метрах от комнаты с порталом. Затем игроки донесли туда нужные предметы. Один из них погиб, неся все двенадцать глаз, но остальные успели сообщить точку гибели и подобрать добычу.

[FIGURE:7]
[CAPTION:По направлениям полёта двух Глаз Эндера агент вычислил местоположение крепости; оценка оказалась примерно в 43 метрах от комнаты с порталом.]

Путь от портала до дракона оказался самой долгой частью. В Нижнем мире команда теряла ресурсы, а в финальном измерении дракон убил игроков 69 раз. Между попытками агенты записывали правила: не задерживаться на месте появления, подходить к дракону только когда он садится и перезапускать его поведение, если он застрял. Для последнего все четверо возвращались в обычный мир: после гибели персонаж появлялся у кровати, а пустое измерение выгружалось.

Перелом наступил примерно через 21 час. Один из агентов заметил, что здоровье дракона восстанавливают кристаллы на обсидиановых колоннах. Он же нашёл способ добраться до них без кирки: построить столб из земли, подняться к кристаллу и разбить его рукой. Команда уничтожила все десять кристаллов, и через несколько часов дракон был побеждён.

[FIGURE:12]
[CAPTION:Команда уничтожила все десять кристаллов, которые восстанавливали здоровье дракона; справа показано, как его здоровье уменьшалось в финальной битве.]

## Что команда выработала сама

Участники постепенно закрепили за собой разные виды работы, но могли помогать друг другу. Один игрок добывал ресурсы, другой строил инструменты, третий искал нужные места. В конце именно тот, кто меньше всех занимался разведкой, нанёс дракону последний удар.

Команда также создавала собственные программные помощники и сохраняла их между запусками. Среди них были функции для подсчёта предметов и перемещения персонажа. Общая память помогала переносить опыт от одного игрока к другим: однажды найденное решение можно было использовать снова, вместо того чтобы разбираться с проблемой заново.

Неудачи тоже требовали проверки. Однажды программа объявила об успехе, которого не было. Агент через две минуты исправил сообщение и объяснил, что сработала ветка кода без проверки результата. Другой игрок заметил, что сообщение о возвращении с добычей не сходится с гибелью отправителя. Так участники не только передавали друг другу планы, но и сверяли слова с тем, что произошло в игре.

## Что говорят результаты — и чего не говорят

Победа показывает, что общий ИИ-агент может пройти длинную цепочку игровых задач, если умеет писать программы, проверять их результат и сохранять опыт. Такой подход интересен не только для игр: в разработке программ и работе с корпоративными системами тоже нужно поддерживать общий план, передавать знания и восстанавливаться после ошибок.

Но условия эксперимента важны. Mineflayer сообщал агентам точные данные о ближайших блоках и существах — в том числе о том, что человек не увидел бы сквозь камень. Встроенный поиск пути помогал обходить препятствия. Агенты играли на лёгком уровне сложности, и модель уже знала Minecraft из обучающих данных. Поэтому эксперимент проверял, могут ли они применить эти знания в долгой совместной задаче, а не научиться игре с нуля.

Наконец, это был один запуск, а не серия повторов. Победа заняла больше суток и потребовала 605 смертей; 22% программ завершились ошибкой. Стоимость работы моделей до победы исследователи оценили примерно в 520 долларов по начальной цене API, или около 1 040 долларов по обычному тарифу.

## Вывод

Команда прошла Minecraft, потому что агенты смогли **разделять работу, обмениваться находками и исправлять план после провалов**. Это заметный прогресс для долгих задач, где отдельные действия должны складываться в общий результат.

Но победа сама по себе ещё не доказывает, что агенты так же надёжно справятся с рабочими задачами. Для этого нужны повторные испытания и среды, где система не получает готовые сведения о мире. Пока результат показывает другое: при понятной цели и постоянной обратной связи ИИ-агенты способны самостоятельно поддерживать многошаговый план — пусть и через сотни ошибок.

<!-- Доступные иллюстрации (вставляются маркером [FIGURE:N]) -->
<!-- [FIGURE:0] Figure 1: The four agents, and their run step by step: the thirteen steps from bare hands to the Ender Dragon, each colored by the player who reached it first, over 27 hours and 14 minutes. Item icons and player faces from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:1]  -->
<!-- [FIGURE:2] Figure 2: How each agent plays. It writes a JavaScript program, a Mineflayer bot runs it in the shared world, and text comes back. The players share the game’s chat and can read each other’s notes. A fifth agent, the Observer, reports on the game but never plays. Item icons and player faces from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:3] Figure 3: The whole run. Each lane is a player: dots are chat messages, diamonds are advancements, red ticks are deaths. Bars count programs per half hour; orange dashes mark the six restarts of the world server. Item icons and player faces from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:4] Figure 4: The thirteen dependent steps from initial spawn to the Ender Dragon, each with the time the team first reached it and the player who did. Item icons from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:5] Figure 5: Chat in the first quarter hour: janesick proposes roles ten minutes in, and auratian answers with a different plan within a minute. Messages in all chat figures are verbatim, timed from the first program; […] marks an elision. Item icons and player faces from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:6] Figure 6: After a Ghast fireball destroyed dropped items, auratian posts a rule for the team, and janesick follows two minutes later with the root cause and a fix. Item icons and player faces from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:7] Figure 7: janesick’s two throws, minutes apart in the eleventh hour of the run, and where the lines cross. Coordinates are in blocks; one block is one meter. Item icons from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:8] Figure 8: auratian drowns carrying all twelve Eyes of Ender. janesick and auratian send bulicame the exact spot and the despawn deadline, and bulicame recovers all twelve. Item icons and player faces from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:9] Figure 9: The End portal in the stronghold, with all twelve eyes in place. Rendered with the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:10] Figure 10: Rules for the End, written between attempts at the dragon: never wait on the arrival platform, leave the End to reset a stuck dragon, approach only while it perches. Item icons and player faces from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:11] Figure 11: auratian finds why the dragon stays at full health, the healing crystals, and then a way to reach them without a pickaxe. Item icons and player faces from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:12] Figure 12: Left: the ten crystals on the End island, seen from above, colored by the player who destroyed each, with the time into the run. Right: the dragon’s health in the final fight, as the players’ own programs read it. Item icons from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->
<!-- [FIGURE:13] Figure 13: Left: messages that match simple patterns for each behavior, by sender; a message can match several. Right: the 605 deaths before the win, by cause, from the server log. -->
<!-- [FIGURE:14] Figure 14: auratian retracts, two minutes later, a success that its program had announced but that had not happened. Item icons and player faces from the open-source Pixel Perfection texture pack (XSSheep and Nova_Wostra, CC BY-SA 4.0), not Minecraft’s textures. -->

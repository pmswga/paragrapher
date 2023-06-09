# paragrapher

Утилита предназначена для анализа текста в pdf документах. Изначальная идея: "что если взять pdf документ, выделить из него абзацы, затем уже производить анализ абзацев?". Выделяя именованные сущности (с последующем обобщением), строя граф связей между абзацами. В результате получая граф и список именованых сущностей, о которых говорится в текстах. Далее можно спомощью yandex/google api получать информацию об именованных сущностях и использовать для анализа.

Из исходного pdf файла выделяются абзацы текста, из каждого абзаца выделяются именованные сущности и полученные результаты сохранются в csv файл:

| par_num| par_text | ents |
|--------|----------|------|
|  1  | Всем привет, я живу в России | [Россия]  |
| ... | ...  | ... |

Выделенные сущности сохраняются в csv файл с привязкой к номеру параграфа.

| par_num| entity |
|--------|------|
|  1  | Россия  |
| ... | ... |

Также формируется мешок сущностей, сохраняемый в json файл

```json
{"Россия": 1}
```

# Ограничения

1) утилита обрабатывает только свёрстанные PDF. То есть такие PDF, в которых текст можно выделить с помощью библиотеки PyPDF2 
2) не учитываются таблицы/списки/картинки/формулы и прочие медиа-материалы. PDF должен содержать по большому счёту полотно текста
3) плохо склеиваются абзацы между концом/началом страниц.

# Запуск

Установить необходимые библиотеки

```bash
pip install -r requirements.txt
```

Указать путь к PDF файлу и страницы для анализа

```python
$ python main.py --pdf='/path/to/mybook.pdf' --spage=10 --endpage=80
```

# Примеры

## Пример на книге "История российской внешней разведки"


```python
$ python main.py --pdf='books/test-1.pdf' --spage=6 --endpage=244
```

Результаты разбиения текста

|par_num|par_text|ents|
|---|---|---|
|1|Предисловие Содержание шестого, заключительного тома «Истории российской внешней разведки» посвящено ее деятельности в 70-90-е годы прошлого столетия и в первые годы нового, XXI века|[]|
|2|Пятый том очерков завершался событиями, связанными с началом периода разрядки в международных отношениях. Шестой том, повествуя о работе внешней разведки в 70-90-е годы, подводит черту под деятельностью разведки в советский период российской истории. В очерках этого тома рассказывается о начале постсоветского периода в жизни разведки, ее перестройке на демократических началах, о новых задачах и направлениях работы, важности добываемой ею информации в обеспечении внешней безопасности страны|[]|
|3|Такое разнообразное по своему историческому осмыслению содержание тома создавало немалые трудности при его подготовке. Вероятно, могут возникнуть сложности и у читателя -ведь речь в томе идет о работе разведки на грани двух эпох, в один из переломных моментов российской и мировой истории|[]|
|4|70-80-е годы -сложный, полный драматизма период отечественной истории, завершившийся исчезновением с политической карты мира великой державы -Советского Союза, политика которого в течение многих десятилетий была одним из определяющих факторов расстановки сил в мире|['Союза']|
|5|Деятельность внешней разведки в эти годы, характер решавшихся ею задач, оперативная и информационно-аналитическая работа в соответствии с директивными указаниями руководства страны определялись особенностями развития международной обстановки и в первую очередь усилиями Советского Союза по обеспечению национальной безопасности страны, защите ее жизненных интересов на международной арене|['Советского Союза']|
|6|Изменения в международных отношениях, последовавшие за дипломатическим разрешением карибского ракетного кризиса, кото-|[]|
|7|рый поставил мир перед реальностью термоядерной войны, казалось, были надежно закреплены в таких основополагающих международно-правовых актах, как подписанный в августе 1975 года в Хельсинки Заключительный акт Совещания по безопасности и сотрудничеству в Европе, принятая ООН в 1977 году по инициативе Советского Союза Декларация об углублении и упрочении разрядки международной напряженности, а также в ряде двусторонних соглашений, подписанных Советским Союзом с ведущими капиталистическими странами в 60-70-е годы|['рый', 'Хельсинки', 'Европе', 'ООН', 'Советского Союза', 'Советским Союзом']|
|...|...|...|

Сущности

|par_num|entity|
|-|-----|
|4|Союза|
|5|Советского Союза|
|7|Хельсинки|
|7|Европе|
|7|ООН|
|7|Советского Союза|
|7|Советским Союзом|
|...|...|


Мешок сущностей

```json
{
"Союза": 3
"Советского Союза": 64,
"Хельсинки": 2,
"Европе": 9,
"ООН": 13
}
```

# Инструментальные средства

- PyPDF2
- pandas
- spacy


# api_yamdb

api YaMDb

### Описание:

Проект YamDb -- это агрегатор рецензий, собирающий отзывы о произведениях культуры в различных категориях: музыка, кино, литература и не только. Каждое произведение внутри категории делится на жанры. На основании собранных отзывов высчитывается средний рейтинг продукта. Это помогает пользователям найти подходящее для себя произведение. Пользователи могут комментировать чужие рецензии: высказывать несогласие с автором или наоборот -- поддерживать мнение, тем самым находить единомышленников и формировать комьюнити.

### Стек технологий:

* Python
* Django
* Django REST framework
* SQLite

### Как развернуть проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:NikitaPreis/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/scripts/activate
```

Обновить pip и установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов и ответов

**Content type**:
```
application/json
```
**request samples №1:**
```
http://127.0.0.1:8000/api/v1/categories/
```
**response samples №1:**
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
    {}
  ]
}
```

**request samples №2:**
```
http://127.0.0.1:8000/api/v1/titles/
```
**payload №2:**
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
**response samples №2:**
```

{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
    + {...}
    ],
    "category": {
    "name": "string",
    "slug": "^-$"
    }
}
```

### Авторы:
* Раиф
* Дмитрий
* Никита
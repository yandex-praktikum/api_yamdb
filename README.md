### Описание:

Проект «API для Yatube» это учебный проект №9 API: интерфейс взаимодействия программ курса Python-разработчик Яндекс Практикум

### Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/isomta/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

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
### Примеры:

* Получение публикаций
GET
http://127.0.0.1:8000/api/v1/posts/

{
"count": 123,
"next": "http://api.example.org/accounts/?offset=400&limit=100",
"previous": "http://api.example.org/accounts/?offset=200&limit=100",
"results": [
{}
]
}

POST
http://127.0.0.1:8000/api/v1/posts/

{
"text": null,
"image": "string",
"group": null
}

* Создание публикации
GET
http://127.0.0.1:8000/api/v1/posts/

{
"text": null,
"image": "string",
"group": null
}

{
"id": null,
"author": null,
"text": null,
"pub_date": "2019-08-24T14:15:22Z",
"image": "string",
"group": null
}

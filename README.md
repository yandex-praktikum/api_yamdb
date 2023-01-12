# Описание проекта api_yamdb

Проект "YaMDb" Проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения разделены по категориям и жанрам.
Для проекта разработана API

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:Zima2022/api_yamdb.git
```

```bash
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```

* Если у вас Linux/macOS

    ```bash
    source env/bin/activate
    ```

* Если у вас windows

    ```bash
    source env/Scripts/activate
    ```

```bash
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python3 manage.py migrate
```

Запустить проект:

```bash
python3 manage.py runserver
```

### Алгоритм регистрации пользователей

1. Пользователь отправляет POST-запрос на добавление нового пользователя
    с параметрами email и username на эндпоинт '/api/v1/auth/signup/'.

2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code)
    на адрес email.

3. Пользователь отправляет POST-запрос с параметрами username и
    confirmation_code на эндпоинт '/api/v1/auth/token/'.
    В ответе на запрос ему приходит token (JWT-токен).

4. При желании пользователь отправляет PATCH-запрос на эндпоинт
    '/api/v1/users/me/' и заполняет поля в своём профайле.

### Примеры запросов к API

Анонимный пользователь может:

1. Получить список всех категорий: GET-запрос на '/api/v1/categories/'
2. Получить список всех жанров: GET-запрос на '/api/v1/genres/'
3. Получить список всех произведений: GET-запрос на '/api/v1/titles/'
4. Получить информацию о произведении:
        GET-запрос на '/api/v1/titles/{titles_id}/'
5. Получить список всех отзывов о произведении:
        GET-запрос на '/api/v1/titles/{title_id}/reviews/'
6. Получить отзыв по id для указанного произведения.
        GET-запрос на '/api/v1/titles/{title_id}/reviews/{review_id}/'
7. Получить список всех комментариев к отзыву по id произведения:
        GET-запрос на '/api/v1/titles/{title_id}/reviews/{review_id}/comments/'
8. Получить комментарий для отзыва по id.
        GET-запрос на
        '/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/'

Аутентифицированный пользователь может:

1. Добавить новый отзыв.
   Пользователь может оставить только один отзыв на произведение.
    POST-запрос на '/api/v1/titles/{title_id}/reviews/'
        {
            "text": "string",
            "score": 1
        }

2. Добавить новый комментарий для отзыва.
    POST-запрос на '/api/v1/titles/{title_id}/reviews/{review_id}/comments/'
        {
            "text": "string"
        }

### Oб авторах

Код этого проекта написала группа начинающих разработчиков:

Ямутин Василий,
Твердохлебов Сергей,
Рощупкина Марина

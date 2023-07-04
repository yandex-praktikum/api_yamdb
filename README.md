# Проект YaMDb 

![Logo](https://cdn-irec.r-99.com/sites/default/files/product-images/399872/EOXOqQkXnjTMTRnIpMUSvQ.jpg)


[Описание](#описание) /
[Техническое описание](#Техническое_описание_проекта_YaMDb) /
[Развернуть локально](#Как_запустить_проект)

## Описание

Проект YaMDb позволяет собирать отзывы пользователей на различные произведения фильмы, музыку, книги. 

Произведению может быть присвоен жанр из существующего списка. 
Добавлять категории и жанры может только администратор.
Пользователи оставляют отзывы и ставят произведению оценку. 
Из пользовательских оценок формируется усреднённый рейтинг. 
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только зарегистрированные пользователи.

### Библиотекм использованные в проекте:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=ffffff&color=043A6B)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=043A6B)](https://jwt.io/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=ffffff&color=043A6B)](https://cloud.yandex.ru/)

## Техническое описание проекта YaMDb:

### Ресурсы API YaMDb:
* auth: аутентификация.
* users: пользователи.
* titles: произведения, к которым пишут отзывы.
* categories: категории (типы) произведений.
* genres: жанры произведений.
* reviews: отзывы на произведения.
* comments: комментарии к отзывам.

### Пользовательские роли:
Неавторизированный пользователь, Аутентифицированный пользователь, Модератор, Администратор, Суперюзер.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone ДОБАВТЬ В КОНЦЕ
```

```
cd api_yamdb
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
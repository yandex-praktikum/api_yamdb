import csv

from django.core.management import BaseCommand

from users.models import User
from titles.models import Title, Category, Genre, GenreTitle
from reviews.models import Review, Comment

CSV_FILES = [
    ['users.csv', User],
    ['category.csv', Category],
    ['genre.csv', Genre],
    ['titles.csv', Title],
    ['genre_title.csv', GenreTitle],
    ['review.csv', Review],
    ['comments.csv', Comment],
]

# Запускается командой python manage.py import_cvs


class Command(BaseCommand):
    help = 'import csv data into database'

    def handle(self, *args, **options):

        self.stdout.write(self.style.NOTICE('Очистка базы данных'))

        for _, model in reversed(CSV_FILES):
            model.objects.all().delete()

        self.stdout.write(self.style.NOTICE('Проверка новых данных'))

        for file, model in CSV_FILES:
            with open('static/data/' + file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for dict_row in reader:
                    model.objects.get_or_create(**dict_row)

        self.stdout.write(
            self.style.SUCCESS('Новые данные успешно внесены в базу')
        )

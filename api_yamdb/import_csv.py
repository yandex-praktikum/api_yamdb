from pandas import read_csv
from sqlalchemy import create_engine

from core.constants import SUCCESSFULL_IMPORT


def import_csv(engine, csv_file, table_name, default_values={}):
    data = read_csv(csv_file)

    for column, default_value in default_values.items():
        if column not in data.columns:
            data[column] = default_value

    data.to_sql(table_name, engine, if_exists='replace', index=False)


engine = create_engine('sqlite:///db.sqlite3')

import_csv(engine, 'static/data/titles.csv',
           'reviews_titles', {'description': '', })
import_csv(engine, 'static/data/category.csv', 'reviews_categories')
import_csv(engine, 'static/data/genre.csv', 'reviews_genres')
import_csv(engine, 'static/data/genre_title.csv', 'reviews_titles_genre')
import_csv(engine, 'static/data/comments.csv', 'reviews_comments')
import_csv(engine, 'static/data/review.csv', 'reviews_reviews')
import_csv(engine, 'static/data/users.csv', 'reviews_users')

print(SUCCESSFULL_IMPORT)

import os
import psycopg2 as pg
from urllib.parse import urlparse

result = urlparse(os.getenv('DATABASE_URL_1'))

# parse url database
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

# connect to database postgresSQL

connection = pg.connect(
    database=database,
    user=username,
    password=password,
    host=hostname
)

# funcion query database


def run(query, params):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
            return True

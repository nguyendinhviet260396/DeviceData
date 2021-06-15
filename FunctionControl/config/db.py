import os
import psycopg2 as pg
from urllib.parse import urlparse

# result = urlparse(os.getenv('DATABASE_URL'))

# # parse url database
# username = result.username
# password = result.password
# database = result.path[1:]
# hostname = result.hostname

# # connect to database postgresSQL

# connection = pg.connect(
#     database=database,
#     user=username,
#     password=password,
#     host=hostname
# )

connection = pg.connect(
    database='smartcabinet',
    user='postgres',
    password='0000',
    host='127.0.0.1'
)

# funcion query database


def run(query, params):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
            return True

import psycopg2
from psycopg2 import sql


class PostgreSQLClient:
    def __init__(self, database_url):
        self.__database_url__ = database_url

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def get_range(self, start, count):
        with self.__conn__.cursor() as cursor:
            cursor.execute(f'SELECT * FROM Vectors LIMIT {count} OFFSET {start}')
            records = cursor.fetchall()
        return records

    def append(self, values):
        with self.__conn__.cursor() as cursor:
            insert = sql.SQL('INSERT INTO Vectors (Vector) VALUES ({})').format(sql.SQL(',').join(map(sql.Literal, values)))
            cursor.execute(insert)

    def get_count(self):
        with self.__conn__.cursor() as cursor:
            cursor.execute('SELECT count(*) FROM Vectors;')
            count = cursor.fetchall()
        return count[0][0]

    def clear_all(self):
        with self.__conn__.cursor() as cursor:
            cursor.execute('TRUNCATE Vectors;')

    def connect(self):
        self.__conn__ = psycopg2.connect(self.__database_url__)
        self.__conn__.autocommit = True

    def close(self):
        self.__conn__.close()
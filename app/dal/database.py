import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    return psycopg2.connect(
        dbname="url_shortener",
        user="postgres",
        password="postgres",
        host="localhost",
        port=6543,
    )

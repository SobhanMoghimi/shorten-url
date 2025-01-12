import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    conn = psycopg2.connect(
        dbname="url_shortener",
        user="url_shortener_app",
        password="4*GB%!VjCF7K48Vh",
        host="localhost",
        port=5432
    )
    return conn

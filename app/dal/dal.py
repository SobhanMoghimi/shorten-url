from app.dal.database import get_db_connection


def save_url_to_db(long_url: str) -> str:
    """
    Save a long URL and its corresponding short URL to the database.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO urls (url) VALUES (%s);", long_url)
            conn.commit()
            cursor.execute("SELECT shortened_url FROM urls WHERE url = %s;", long_url)
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        conn.close()


def fetch_long_url(short_url: str) -> str:
    """
    Fetch the original URL using a short URL.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT url FROM urls WHERE shortened_url = %s;", (short_url,))
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        conn.close()
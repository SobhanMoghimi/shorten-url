from app.dal.database import get_db_connection
from app.models.models import URLsTimeSinceLastAccessDTO, TopAccessedURLDTO, TotalAccessesTodayDTO, NewURLsTodayDTO


def save_url_to_db(long_url: str) -> str:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO urls (url) VALUES (%s);", (long_url,))
            conn.commit()
            cursor.execute("SELECT shortened_url FROM urls WHERE url = %s;", (long_url,))
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        conn.close()


def get_long_url(short_url: str) -> str:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT url FROM get_url(%s);", (short_url,))
            result = cursor.fetchone()
            conn.commit()
            return result[0] if result else None
    finally:
        conn.close()


def get_new_urls_today() -> NewURLsTodayDTO:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM new_urls_today;")
            if result := cursor.fetchone():
                return NewURLsTodayDTO(total_new_urls=result[0])
    finally:
        conn.close()


def get_total_accesses_today() -> TotalAccessesTodayDTO:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM total_accesses_today;")
            if result := cursor.fetchone():
                return TotalAccessesTodayDTO(total_accesses=result[0])
    finally:
        conn.close()


def get_top_3_accessed_urls() -> list[TopAccessedURLDTO]:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT shortened_url, accessed_count FROM top_3_accessed_urls;")
            results = cursor.fetchall()
            return [TopAccessedURLDTO(shortened_url=row[0], accessed_count=row[1]) for row in results]
    finally:
        conn.close()


def get_urls_time_since_last_access() -> list[URLsTimeSinceLastAccessDTO]:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT shortened_url, accessed_count, time_since_last_access FROM urls_time_since_last_access;"
            )
            results = cursor.fetchall()
            return [
                URLsTimeSinceLastAccessDTO(
                    shortened_url=row[0],
                    accessed_count=row[1],
                    time_since_last_access=str(row[2]),  # Assuming PostgreSQL INTERVAL is returned as a string
                )
                for row in results
            ]
    finally:
        conn.close()

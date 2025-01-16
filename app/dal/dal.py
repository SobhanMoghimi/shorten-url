from app.dal.database import get_db_connection
from app.models.models import URLsTimeSinceLastAccessDTO, TopAccessedURLDTO, TotalAccessesTodayDTO, NewURLsTodayDTO, \
    RegisteredURLsEachDayDTO
import matplotlib.pyplot as plt
import pandas as pd
import os

def save_url_to_db(long_url: str) -> str:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO urls (url) VALUES (%s);", (long_url,))
            conn.commit()
            cursor.execute("SELECT get_short_url(%s);", (long_url,))
            result = cursor.fetchone()
            conn.commit()
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


def get_top_3_accessed_urls() -> list[TopAccessedURLDTO]:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT shortened_url, access_count FROM top_3_accessed_urls;")
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
                    time_since_last_access=str(row[2]),
                )
                for row in results
            ]
    finally:
        conn.close()

def get_accesses_per_day_per_url() -> list[dict]:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT shortened_url, access_date, total_accesses
                FROM accesses_per_day_per_url
                ORDER BY access_date DESC, total_accesses DESC;
            """)
            results = cursor.fetchall()
            return [
                {"shortened_url": row[0], "access_date": row[1], "total_accesses": row[2]}
                for row in results
            ]
    finally:
        conn.close()


def get_registered_urls_each_day() -> list[RegisteredURLsEachDayDTO]:
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT registration_date, total_new_urls
                FROM registered_urls_each_day
                ORDER BY registration_date DESC;
            """)
            results = cursor.fetchall()
            return [
                RegisteredURLsEachDayDTO(
                    registration_date=row[0],
                    total_new_urls=row[1]
                )
                for row in results
            ]
    finally:
        conn.close()


def generate_charts():
    charts_folder = "charts"
    os.makedirs(charts_folder, exist_ok=True)

    if registration_data := get_registered_urls_each_day():
        dates = [item.registration_date.strftime('%Y-%m-%d') for item in registration_data]
        counts = [item.total_new_urls for item in registration_data]
        plt.figure(figsize=(10, 6))
        plt.bar(dates, counts, color="blue")
        plt.title("Daily Registrations")
        plt.xlabel("Date")
        plt.ylabel("Total Registrations")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(charts_folder, "daily_registrations.jpeg"))
        plt.close()

    if access_data := get_accesses_per_day_per_url():
        df = pd.DataFrame(access_data)
        df["access_date"] = pd.to_datetime(df["access_date"]).dt.strftime('%Y-%m-%d')

        total_access = df.groupby("access_date")["total_accesses"].sum().reset_index()
        dates = total_access["access_date"]
        counts = total_access["total_accesses"]
        plt.figure(figsize=(10, 6))
        plt.bar(dates, counts, color="orange")
        plt.title("Total Daily Accesses")
        plt.xlabel("Date")
        plt.ylabel("Total Accesses")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(charts_folder, "total_daily_accesses.jpeg"))
        plt.close()

        for shortened_url in df["shortened_url"].unique():
            link_data = df[df["shortened_url"] == shortened_url]
            dates = link_data["access_date"]
            counts = link_data["total_accesses"]
            plt.figure(figsize=(10, 6))
            plt.bar(dates, counts, color="green")
            plt.title(f"Daily Accesses for {shortened_url}")
            plt.xlabel("Date")
            plt.ylabel("Access Count")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(charts_folder, f"access_per_day_{shortened_url}.jpeg"))
            plt.close()

def delete_inactive_urls():
    """
    Delete URLs that have not been accessed for more than 7 days.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("CALL delete_inactive_urls();")
            conn.commit()
    finally:
        conn.close()

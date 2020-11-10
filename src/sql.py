import logging
import sqlite3
import logging
import datetime

from src.setup import db_file_path

def insert_to_sqlite(df):
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    try:
        c.executemany(f"""
            INSERT OR IGNORE INTO scrobbles ({", ".join([f"'{i}'" for i in df.columns])}) 
            VALUES({(len(df.columns)*"? ")[:-1].replace(" ", ",")})""", 
            list(df.to_records(index=False)))
        conn.commit()
    except:
        logging.error("error, closing connection", exc_info=True)
    finally:
        c.close()
        conn.close()

def get_last_scrobble_datetime():
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    try:
        c.execute("select max(datetime(date)) from scrobbles")
        max_date = c.fetchone()[0]
        max_date = datetime.datetime.strptime(max_date, "%Y-%m-%d %H:%M:%S")
    except:
        logging.error("error, closing connection", exc_info=True)
    finally:
        c.close()
        conn.close()
    return max_date

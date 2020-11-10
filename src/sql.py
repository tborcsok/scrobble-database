import logging
import sqlite3
import logging
import datetime

import pandas as pd

from src.setup import db_file_path

def connect_to_db():
    conn = sqlite3.connect(db_file_path)
    return conn

def sql_query(query):
    conn = connect_to_db()
    try:
        df = pd.read_sql(query, conn)
    except:
        df = None
    finally:
        conn.close()
    return df

def insert_to_sqlite(df, table):
    conn = connect_to_db()
    c = conn.cursor()
    try:
        c.executemany(f"""
            INSERT OR IGNORE INTO {table} ({", ".join([f"'{i}'" for i in df.columns])}) 
            VALUES({(len(df.columns)*"? ")[:-1].replace(" ", ",")})""", 
            list(df.to_records(index=False)))
        conn.commit()
    except:
        logging.error("error, closing connection", exc_info=True)
    finally:
        c.close()
        conn.close()

def upsert_to_sqlite(df, table, unique_col):
    conn = connect_to_db()
    c = conn.cursor()
    try:
        c.executemany(f"""
            INSERT INTO {table} ({", ".join([f"'{i}'" for i in df.columns])}) 
            VALUES({(len(df.columns)*"? ")[:-1].replace(" ", ",")})
            ON CONFLICT({unique_col}) DO UPDATE SET {", ".join([f"{i}=excluded.{i}" for i in df.columns])}""", 
            list(df.to_records(index=False)))
        conn.commit()
    except:
        logging.error("error, closing connection", exc_info=True)
    finally:
        c.close()
        conn.close()

def get_last_scrobble_datetime():
    conn = connect_to_db()
    c = conn.cursor()
    max_date = None
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

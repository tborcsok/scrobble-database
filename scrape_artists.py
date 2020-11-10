import logging
import time
from tqdm import tqdm
import pandas as pd

from src import sql
from src import utils
from src.lastfm import artists

def main():
    artists_list = sql.sql_query('select distinct artist_id from scrobbles').dropna().artist_id.values

    records = list()
    logging.info('Getting artists')
    for a in tqdm(artists_list):
        response, download_time = artists.get_artist(a)
        record = [a] + artists.extract_artist(response) + [download_time]
        records.append(record)
        time.sleep(0.5)

    logging.info('Inserting to DB')
    df = pd.DataFrame(records, 
                        columns=["artist_id", "listeners", "playcount", "created"])

    sql.insert_to_sqlite(df, "artists")

if __name__=='__main__':
    utils.custom_logger()
    main()
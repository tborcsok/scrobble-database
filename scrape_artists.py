import logging
import time
from typing import final
from tqdm import tqdm
import pandas as pd

from src import sql
from src import utils
from src.lastfm import artists

def main():
    artists_list = sql.sql_query('select distinct artist_id from scrobbles').dropna().artist_id.values

    records = list()
    errors = list()
    logging.info('Getting artists')
    for a in tqdm(artists_list):
        try:
            response, download_time = artists.get_artist(a)
            record = artists.extract_artist(response, a, download_time)
            records.append(record)
        except KeyboardInterrupt:
            break
        except:
            logging.error('Error', exc_info=True)
            errors.append(a)
        finally:
            time.sleep(0.5)

    logging.info('Inserting to DB')
    df = pd.DataFrame(records, 
                        columns=["artist_id", "listeners", "playcount", "created"])

    sql.upsert_to_sqlite(df, "artists", unique_col='artist_id')

if __name__=='__main__':
    utils.custom_logger()
    main()
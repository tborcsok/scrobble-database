import logging
import time

from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

from src import sql, utils
from src.lastfm import scrobbles


def main():

    last_timestamp = None

    total_pages = scrobbles.get_total_pages(from_ts=last_timestamp)
    errors = list()
    for p in tqdm(range(total_pages)):
        try:
            response = scrobbles.get_history(page=p + 1, from_ts=last_timestamp)
            records = scrobbles.extract_page(response)
            sql.insert_to_scrobbles(records)
        except KeyboardInterrupt:
            break
        except:
            logging.error("Error", exc_info=True)
            errors.append(p + 1)
        finally:
            time.sleep(0.5)

    print(errors)


if __name__ == "__main__":

    utils.custom_logger()
    main()

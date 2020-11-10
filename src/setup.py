import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

db_file_path = Path(__file__).parents[1]/'data'/'lastfm_data.db'

LASTFM_API_USER = os.getenv("LASTFM_API_USER")
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

import os
from pathlib import Path

db_file_path = Path() / "data" / "lastfm_data.db"
db_file_path.mkdir(exist_ok=True)

LASTFM_API_USER = os.getenv("LASTFM_API_USER")
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

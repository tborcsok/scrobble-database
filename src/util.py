from pathlib import Path


def check_db_exists() -> bool:
    """Check if database file exists"""

    return Path("lastfm.db").exists()


def raise_missing_db() -> None:
    """Raise error if database file does not exist

    Raises:
        FileNotFoundError if file does not exist
    """
    if not Path("lastfm.db").exists():
        raise FileNotFoundError('Database file not found. Run the "db init" command first to initialize the database!')

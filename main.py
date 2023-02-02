import logging
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from src.cli import cli

root = Path(__file__).parent / "logs"

if __name__ == "__main__":
    root.mkdir(exist_ok=True)

    started = datetime.utcnow()

    logging.basicConfig(
        format="%(levelname)s:%(asctime)s:%(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S%z",
        handlers=[
            logging.FileHandler(root / f"{started.date().isoformat()}.log"),
            logging.StreamHandler(),
        ],
    )

    cli()

import logging

from dotenv import load_dotenv

load_dotenv()

from src.cli import cli

if __name__ == "__main__":

    logging.basicConfig(
        format="%(levelname)s:%(asctime)s:%(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S%z",
    )

    cli()

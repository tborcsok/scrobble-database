from sqlalchemy import create_engine

from src.setup import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH.absolute()}", echo=False)

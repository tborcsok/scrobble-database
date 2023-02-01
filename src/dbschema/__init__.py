from sqlalchemy import create_engine

from src.setup import DB_FILE

engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)

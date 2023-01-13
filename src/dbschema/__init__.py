from sqlalchemy import create_engine

engine = create_engine("sqlite:///lastfm.db", echo=False)

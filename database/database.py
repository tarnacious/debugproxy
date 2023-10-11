from config import read_config

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


config = read_config()
database_uri = config["SQLALCHEMY_DATABASE_URI"]

engine = create_engine(database_uri)
Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine)
db_session = scoped_session(Session)
session = db_session
Base = declarative_base()
Base.query = db_session.query_property()

def create_all():
    import database.models
    Base.metadata.create_all(bind=engine)

def drop_all():
    import database.models
    Base.metadata.drop_all(bind=engine)

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import database.models
    Base.metadata.create_all(bind=engine)

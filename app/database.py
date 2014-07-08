from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

db_path = os.environ['EATSAFE_DATABASE_PATH']

engine = create_engine(db_path)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

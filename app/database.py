from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASES

engine = create_engine(DATABASES['PREFIX'] + DATABASES['NAME'])
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

from eatsafeapp import eatsafeapp
from flask.ext.sqlalchemy import SQLAlchemy
import os

eatsafeapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(eatsafeapp)

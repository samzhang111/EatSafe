from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from eatsafeapp import eatsafeapp
from eatsafeapp.database import db
import os

migrate = Migrate(eatsafeapp, db)
manager = Manager(eatsafeapp)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

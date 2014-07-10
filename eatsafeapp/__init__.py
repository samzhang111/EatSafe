from flask import Flask

app = Flask(__name__)

app.config['WHOOSH_BASE'] = '/home/sam/battlehack/EatSafe/db/food_inspections.whoosh'

from eatsafeapp import views

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import select
from app.settings import DATABASES
from app.schema import *

engine = create_engine(DATABASES['PREFIX'] + DATABASES['NAME'])
Base.metadata.tables['restaurants_indexed'].create(engine, checkfirst=True)

conn = engine.connect()
#restaurant = Restaurant()
#restaurant.create(engine)

Session = scoped_session(sessionmaker(bind=engine))
session = Session()
#rows = session.query(Restaurant_old).fetchall()
selected = select([Restaurant_old])
rows = list(conn.execute(selected))

#print 'Shape of incoming session: {}'.format(len(rows))
for i, row in enumerate(rows):
    d = dict(zip(row.keys(), row))
    #d = row.__dict__
    #d.pop('_sa_instance_state', None)
    r = Restaurant(**d)
    session.add(r)
    if i%1000 == 0:
        print "Executed {} rows".format(i)
        print d
        session.commit()

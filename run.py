from eatsafeapp import eatsafeapp
import psycopg2
import sys, os

if __name__ == '__main__':
    esdb = os.environ['EATSAFE_DATABASE_PATH']
    print esdb
    conn = psycopg2.connect(database='eatsafe')
    eatsafeapp.debug = True
    eatsafeapp.run()

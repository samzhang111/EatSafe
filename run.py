from eatsafeapp import eatsafeapp
import sys, os, psycopg2

if __name__ == '__main__':
    database = os.environ['EATSAFE_DB']
    user = os.environ['EATSAFE_USER']
    pw = os.environ['EATSAFE_PW']
    host = os.environ['EATSAFE_HOST']

    db_str = 'dbname={db} host={host} user={user} password={pw}'.format(
            db=database,
            host=host,
            user=user,
            pw=pw)

    conn = psycopg2.connect(db_str)
    print conn.status

    eatsafeapp.debug = True
    eatsafeapp.run()

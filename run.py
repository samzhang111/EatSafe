from eatsafeapp import eatsafeapp
from werkzeug.contrib.fixers import ProxyFix

eatsafeapp.wsgi_app = ProxyFix(eatsafeapp.wsgi_app)

if __name__ == '__main__':
    eatsafeapp.debug = True
    eatsafeapp.run()

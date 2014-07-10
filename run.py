from eatsafeapp import eatsafeapp
import sys, os, inspect

if __name__ == '__main__':
    print os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    eatsafeapp.debug = True
    eatsafeapp.run()

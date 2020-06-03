from some_app import app


if __name__ == "__main__":
    app.run()

# import imp
# import os
# import sys
#
# sys.path.insert(0, os.path.dirname(__file__))
#
# wsgi = imp.load_source('wsgi', 'some_app.py')
# app = wsgi.app
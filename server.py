
import sys

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

from bottle import Bottle, SimpleTemplate, request, response
import string
import pickledb
import random

import NimHandler as handler
import pages


DB_FILE = sys.argv[1] if len(sys.argv) > 1 else "turnbased_server.db"
COOKIE = "SESSION_ID"
COOKIE_KEY = "cookie|"
COOKIE_LEN = 8 

db = pickledb.load(DB_FILE, False)
app = Bottle()


def gen_randomstring(n):
    return ''.join(random.choice(string.ascii_letters) for x in range(n))
def gen_cookie():
    return gen_randomstring(COOKIE_LEN)


def session():
    cookie = request.get_cookie(COOKIE)

    # check if cookie is valid
    if cookie and db.get(COOKIE_KEY + cookie):
        return cookie

    cookie = gen_cookie()
    response.set_cookie(COOKIE, cookie, path='/')
    db.set(COOKIE_KEY + cookie, cookie)
    db.dump()

    return cookie


@app.route('/')
def index():
    cookie = session()
    return pages.index_src
    
@app.route('/docs')
def docs():
    return pages.doc_src

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=False)




import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

from bottle import Bottle, SimpleTemplate, request, response
import string
import pickledb
import random

import NimHandler as handler
import game_handler as game
import pages


DATA_FOLDER = sys.argv[1] if len(sys.argv) > 1 else 'data'
DB_FILE = "turnbased_server.db"
COOKIE = "SESSION_ID"
COOKIE_KEY = "cookie|"
COOKIE_LEN = 8 
COOKIE_TRIES = 6 


if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
db = pickledb.load(DATA_FOLDER + "/" + DB_FILE, True)
app = Bottle()


# TODO list paradigms


def gen_randomstring(n):
    return ''.join(random.choice(string.ascii_letters) for x in range(n))

def gen_cookie():
    for i in range(COOKIE_TRIES):
        cookie = gen_randomstring(COOKIE_LEN)
        if not db.get(COOKIE_KEY + cookie):
            return cookie
    raise Exception("No cookies left in the jar")
    # raise Exception("Could not find available cookie")


def get_session():
    cookie = request.get_cookie(COOKIE)

    # check if cookie is valid
    if cookie and db.get(COOKIE_KEY + cookie):
        return cookie

    cookie = gen_cookie()
    response.set_cookie(COOKIE, cookie, path='/')
    db.set(COOKIE_KEY + cookie, cookie)

    return cookie


@app.route('/')
def index():
    cookie = get_session()
    return pages.index_html
    
@app.route('/docs')
def docs():
    return pages.docs_html

@app.route('/games/list')
def games_list():
    pass

newgame_template = SimpleTemplate(pages.new_game_tmpl)
@app.route('/games/new', method='GET')
def games_new_page():
    data = {
        "paradigms" : ["Nim", "Chess"],
    }
    return newgame_template.render(data=data)

@app.route('/games/new', method='POST')
def games_new_page():
    s = " TODO create new game<br>"
    for key in request.forms:
        s += key + ": " + request.forms[key] + "<br>"
    return s
    #return "new game post handler"

@app.route('/game/<id:int>/sit')
def game_sit(id):
    return "game sit page goes here."

@app.route('/game/<id:int>/stand')
def game_stand():
    pass

@app.route('/game/<id:int>/move')
def game_move():
    cookie = get_session()
    pass


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=False)



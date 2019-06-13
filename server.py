
import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

from bottle import Bottle, request, response, template, abort
import string
import pickledb
import random
import json

import games.nim as handler
import GameHandler


DATA_FOLDER = sys.argv[1] if len(sys.argv) > 1 else 'data'
DB_FILE = "server_data.db"
COOKIE = "SESSION_ID"
COOKIE_KEY = "cookie|"
COOKIE_LEN = 8 
COOKIE_TRIES = 6 


if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

db = pickledb.load(DATA_FOLDER + "/" + DB_FILE, True)
app = Bottle()


# TODO list paradigms


def read_file(name):
    return open(name).read()

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
    return template('templates/index')
    
docs_html = read_file('static/docs.html')

@app.route('/docs')
def docs():
    return docs_html

@app.route('/list')
def games_list():
    game_list = GameHandler.list_games()
    return template('templates/list_games', game_list=json.dumps(game_list))


#newgame_template = SimpleTemplate(pages.new_game_tmpl)
@app.route('/new', method='GET')
def games_new_page():
    data = {
        "paradigms" : [
          {"name": "Nim", "version":"dev", "min_players": 2, "max_players":2 },
          {"name": "Chess", "version":"dev", "min_players": 2, "max_players":2 },
          {"name": "Chinese Chess", "version":"dev", "min_players": 2, "max_players":6 },
        ],
    }
    return template('templates/new_game', data=data)

# TODO json api vs page navigation.
@app.route('/new', method='POST')
def games_new_page():
    game_args = {
        'paradigm': request.forms.get('game_paradigm'),
        'min_players': request.forms.get('min_players'),
        'max_players': request.forms.get('max_players'),
    }
    game_id = GameHandler.new_game(game_args)
    if game_id == None:
        abort(404, "Cannot create new game.")
    else:
        return template('templates/new_redirect', game_id=game_id)
    #return "new game post handler"

@app.route('/game/<id:re:[a-zA-Z]*>/lobby')
def game_lobby(id):
    info = GameHandler.game_info(id)
    if info == None:
        abort(404, "Unknown game id.")
    return template('templates/lobby', game_id=id, info=info)


@app.route('/game/<id:re:[a-zA-Z]*>/sit')
def game_sit(id):
    return "game sit page goes here."


@app.route('/game/<id:re:[a-zA-Z]*>/stand')
def game_stand():
    pass

@app.route('/game/<id:re:[a-zA-Z]*>/move')
def game_move():
    cookie = get_session()
    pass


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=False)




import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

from bottle import Bottle, request, response, template, abort, \
                   static_file, BaseTemplate
import string
import pickledb
import random
import json

import games.nim as handler
import game_handler
from games import games

game_paradigms = []

for game in games:
	game_paradigms.append(game.info)


DATA_FOLDER = sys.argv[1] if len(sys.argv) > 1 else 'data'
NAV_TEMPLATE_FILE = "templates/nav.html.tpl"
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
    _f = open(name)
    result = _f.read()
    _f.close()
    return result

nav_html_contents = read_file(NAV_TEMPLATE_FILE)

BaseTemplate.defaults['nav_header'] = nav_html_contents
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


@app.route('/static/<filepath:re:.*>', method="GET")
def static_resource(filepath):
    return static_file(filepath, root="static")

@app.route('/list')
def games_list():
    game_list = game_handler.list_games()
    return template('templates/list_games', game_list=json.dumps(game_list))

@app.route('/mygames')
def my_games():
    #todo handler.my_games()
    game_list = game_handler.list_games()
    return template('templates/my_games', game_list=json.dumps(game_list))


#newgame_template = SimpleTemplate(pages.new_game_tmpl)
@app.route('/new', method='GET')
def games_new_page():
    data = {
        "paradigms" : game_paradigms
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
    game_id = game_handler.new_game(game_args)
    if game_id == None:
        abort(404, "Cannot create new game.")
    else:
        return template('templates/new_redirect', game_id=game_id)
    #return "new game post handler"

@app.route('/game/<id:re:[a-zA-Z]*>/lobby')
def game_lobby(id):
    info = game_handler.game_info(id)
    print('game', info);
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




import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

import json, string
import settings, util
import server_data as data

from bottle import Bottle, request, response, template, abort, \
                   static_file, BaseTemplate, redirect

from games import games
game_paradigms = {}
for game in games:
	game_paradigms[game.info.name] = game

def get_session():
    cookie = request.get_cookie(settings.COOKIE_NAME)
    # check if cookie is exists
    if cookie and cookie in data.cookies:
        return cookie
    cookie = util.gen_token(settings.COOKIE_LEN, chars=string.ascii_letters.upper())
    response.set_cookie(settings.COOKIE_NAME, cookie)
    data.cookies.add(cookie)
    return cookie


app = Bottle()
@app.route('/')
def index():
    get_session()
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
        'choose_seats': request.forms.get('choose_seats'),
    }
    paradigm = game_args['paradigm']
    if paradigm == None:
        raise ValueError('new_game: no paradigm attribute')
    try:
        handler = game_handlers[paradigm]
    except KeyError:
        raise ValueError('new_game: unknown game paradigm: ' + paradigm)

    game_id = util.gen_token()

    game = {}
    game.info = copy.deepcopy(game_args)
    data.games[game_id] = game

    return redirect('/game/' + game_id + '/lobby')

@app.route('/game/<id:re:[a-zA-Z]*>/lobby', method="GET")
@app.route('/game/<id:re:[a-zA-Z]*>/lobby', method="POST")
def game_lobby(id):
    cookie = get_session()
    user_token = cookie
    info = game_handler.game_info(id)
    error_message = None
    if request.method == "POST":
        print(request.forms)
        sit_index = int(request.forms.get("sit_index"))
        if sit_index != None:
            print("sitting:", sit_index)
            if sit_index < 0:
                if not game_handler.game_stand(id, user_token):
                    error_message = "Could not stand. Perhaps you are not seated?"
            elif not game_handler.game_sit(id, user_token, sit_index):
                error_message = "Could not sit. Seat may be taken or seats may be full."
    # print('game lobby info', info);
    if info == None:
        abort(404, "Unknown game id.")
    seats = game_handler.game_list_seats(id)
    my_seat = game_handler.game_get_seat(id, user_token)
    print("user 'my_seat'", my_seat)

    data = {
        "game_id" : id,
        "info" : info,
        "seats" : seats,
        "my_seat" : my_seat,
        "error_message" : error_message,
    }

    return template('templates/lobby', **data)


"""
@app.route('/game/<id:re:[a-zA-Z]*>/sit')
def game_sit(id):
    return "game sit page goes here."


@app.route('/game/<id:re:[a-zA-Z]*>/stand')
def game_stand():
    pass
"""

@app.route('/game/<id:re:[a-zA-Z]*>/move')
def game_move():
    cookie = get_session()
    pass


if __name__ == "__main__":
    with open(settings.NAV_FILE) as file:
        BaseTemplate.defaults['nav_header'] = file.read()
    app.run(debug=True)
    #app.run(debug=False)



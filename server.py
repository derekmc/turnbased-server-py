
import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

import json, string, copy
import settings, util
import server_data as data

from bottle import Bottle, request, response, template, abort, \
                   static_file, BaseTemplate, redirect

from games import games
game_paradigms = {}
for game in games:
	game_paradigms[game.info['name']] = game

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
    game_list = []
    for game in data.games:
        game_list.append(game)
    return template('templates/list_games', game_list=json.dumps(game_list))

@app.route('/mygames')
def my_games():
    #todo handler.my_games()
    game_list = []
    for game in data.games:
        game_list.append(game)
    return template('templates/my_games', game_list=json.dumps(game_list))


#newgame_template = SimpleTemplate(pages.new_game_tmpl)
@app.route('/new', method='GET')
def games_new_page():
    _data = {
        "paradigms" : game_paradigms
    }
    return template('templates/new_game', data=_data)


# TODO json api vs page navigation.
@app.route('/new', method='POST')
def games_new_page():
    paradigm = request.forms.get('game_paradigm')
    min_players = request.forms.get('min_players')
    max_players = request.forms.get('max_players')
    choose_seats = request.forms.get('choose_seats')

    if paradigm == None:
        raise ValueError('new_game: no paradigm attribute')
    try:
        info = game_paradigms[paradigm].info
    except KeyError:
        raise ValueError('new_game: unknown game paradigm: ' + paradigm)

    # check against paradigm allowed values.
    __max_players = info['max_players']
    __min_players = info['min_players']

    if min_players == "" or min_players < __min_players:
        min_players = __min_players
    if max_players == "" or max_players > __max_players:
        max_players = __max_players

    game_args = {
        'paradigm': paradigm,
        'min_players': min_players,
        'max_players': max_players,
        'choose_seats': choose_seats,
    }
    print('game_args', game_args)

    game_id = util.gen_token(settings.GAME_ID_LEN)

    game = {"seats":[]}
    game['info'] = copy.deepcopy(game_args)
    data.games[game_id] = game

    return redirect('/game/' + game_id + '/lobby')

@app.route('/game/<id:re:[a-zA-Z]*>/lobby', method="GET")
@app.route('/game/<id:re:[a-zA-Z]*>/lobby', method="POST")
def game_lobby(id):
    cookie = get_session()
    user_token = cookie
    error_data = {
      "error_message": "An error ocurred.",
      "destination": "/game/" + id + "/lobby/",
    }
    try:
        game = data.games[id]
    except KeyError:
        error_data['destination'] = '/'
        # the id should be clean because it matches the id regex which only allows letters.
        error_data['error_message'] = "Unknown game: '" + id + '" '
        return template('templates/error', **error_data)


    if not id in data.games:
        return abort(404, "Unknown game id.")
    game = data.games[id]
    info = game['info']
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
    info = game['info']
    seats = game['seats']
    my_seat = 0
    for i in range(len(seats)):
        if seats[i] == cookie:
            my_seat = i + 1
            
    print("user 'my_seat'", my_seat)

    template_data = {
        "game_id" : id,
        "info" : info,
        "seats" : seats,
        "my_seat" : my_seat,
        "error_message" : error_message,
    }

    return template('templates/lobby', **template_data)

@app.route('/game/<id:re:[a-zA-Z]*>/sit', method="POST")
def game_sit(id):
    cookie = get_session()
    error_data = {
      "error_message": "An error ocurred.",
      "destination": "/game/" + id + "/lobby/",
    }
    try:
        game = data.games[id]
    except KeyError:
        error_data['destination'] = '/'
        # the id should be clean because it matches the id regex which only allows letters.
        error_data['error_message'] = "Unknown game: '" + id + '" '
        return template('templates/error', **error_data)

    print('game sit form', request.forms)
    info = game['info']
    seats = game['seats']
    sit_index = int(request.forms.get("seat_index"))
    if sit_index != None:
        print("sitting:", sit_index)
        if sit_index < 0:
            if not cookie in seats:
                error_data['error_message'] = "Could not stand. Perhaps you are not seated?"
                return template('templates/error', **error_data)
            else:
                if len(seats) < sit_index + 1:
                    # extend array
                    seats = seats + [""] * (sit_index + 1 - len(seats))
                seats[sit_index] = cookie
        else:
            if sit_index > info['max_players']:
                error_data['error_message'] = "Could not sit. Only " + str(info['max_players']) + " allowed."
                return template('templates/error', **error_data)
            if len(seats) > sit_index and seats[sit_index] != "":
                error_data['error_message'] = "Could not sit. Seat " + str(sit_index + 1) + " taken."
                return template('templates/error', **error_data)
                
            error_message = "Could not sit. Seat may be taken or seats may be full."

    return redirect('/game/' + id + '/lobby')


"""

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



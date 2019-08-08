
import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")

import json, string, copy
import settings, util
import data
from value_types import typecheck as T

from bottle import Bottle, request, response, template, abort, \
                   static_file, BaseTemplate, redirect

from games import games
game_paradigms = {}
paradigm_info = {}
for game in games:
    paradigm_info[game.info['paradigm']] = T(data.GameInfo, game.info)
    game_paradigms[game.info['paradigm']] = game

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
    get_session()
    game_infos = []
    for game_id in data.games:
        game_info = copy.deepcopy(data.games[game_id]['info'])
        game_info['id'] = game_id
        game_infos.append(game_info)
    return template('templates/list_games', game_list=game_infos)

@app.route('/mygames')
def my_games():
    get_session()
    #todo handler.my_games()
    game_list = []
    for game in data.games:
        game_list.append(game)
    return template('templates/my_games', game_list=json.dumps(game_list))


#newgame_template = SimpleTemplate(pages.new_game_tmpl)
@app.route('/new', method='GET')
def games_new_page():
    get_session()
    _data = {
        "paradigms" : paradigm_info
    }
    return template('templates/new_game', data=_data)


# TODO json api vs page navigation.
@app.route('/new', method='POST')
def games_new_page():
    get_session()
    paradigm = request.forms.get('game_paradigm')
    min_players = int(request.forms.get('min_players'))
    max_players = int(request.forms.get('max_players'))
    choose_seats = request.forms.get('choose_seats') == 'on'

    
    if paradigm == None:
        raise ValueError('new_game: no paradigm attribute')
    try:
        game_handler = game_paradigms[paradigm]
        info = game_handler.info
    except KeyError:
        raise ValueError('new_game: unknown game paradigm: ' + paradigm)

    # check against paradigm allowed values.
    info_max_players = info['max_players']
    info_min_players = info['min_players']

    if min_players == "" or min_players < info_min_players:
        min_players = info_min_players
    if max_players == "" or max_players > info_max_players:
        max_players = info_max_players
        
    game_args = {
        'paradigm': paradigm,
        'min_players': min_players,
        'max_players': max_players,
        'choose_seats': choose_seats,
    }
    
    # TODO handle initial state when first move is made.
    #init_state = {}
    #if hasattr(game_handler, "init"):
    #    init_state = game_handler.init(game_args)

    print('game_args', game_args)

    game_id = util.gen_token(settings.GAME_ID_LEN)

    game = {"state": None,
            "info": copy.deepcopy(game_args),
            "status": {"is_started": False, "is_finished": False},
            "chat": "",
            "seats": []}
    data.games[game_id] = game

    return redirect('/game/' + game_id + '/lobby')

@app.route('/game/<id:re:[a-zA-Z]*>/lobby', method="GET")
@app.route('/game/<id:re:[a-zA-Z]*>/lobby', method="POST")
def game_lobby(id):
    cookie = get_session()
    user_token = cookie
    error_data = {
      "error_message": "An error ocurred.",
      "destination": "/game/" + id + "/lobby",
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
    #if request.method == "POST":
    #    print(request.forms)
    #    sit_index = int(request.forms.get("sit_index"))
    #    if sit_index != None:
    #        print("sitting:", sit_index)
    #        if sit_index < 0:
    #            if not game_handler.game_stand(id, user_token):
    #                error_message = "Could not stand. Perhaps you are not seated?"
    #        elif not game_handler.game_sit(id, user_token, sit_index):
    #            error_message = "Could not sit. Seat may be taken or seats may be full."
    info = game['info']
    seats = game['seats']
    my_seat = 0
    for i in range(len(seats)):
        if seats[i] == cookie:
            my_seat = i + 1
            
    print("user 'my_seat'", my_seat)
    print("seats", seats)

    template_data = {
        "game_id" : id,
        "info" : info,
        "seats" : ["x" if len(seat) else "" for seat in seats],
        "my_seat" : my_seat,
        "error_message" : error_message,
    }

    return template('templates/lobby', **template_data)

# seat_index of -1 is used to stand.
@app.route('/game/<id:re:[a-zA-Z]*>/sit', method="POST")
def game_sit(id):
    print("Game Sit called.")
    cookie = get_session()
    error_data = {
      "error_message": "An error ocurred.",
      "destination": "/game/" + id + "/lobby",
    }
    try:
        game = T(data.Game, data.games[id])
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
                seats[seats.index(cookie)] = ""
        else:
            if sit_index == 0:
                sit_index = 1
                while sit_index - 1 < len(seats) and seats[sit_index - 1] != "":
                    sit_index += 1
            if sit_index > info['max_players']:
                error_data['error_message'] = "Could not sit. Only " + str(info['max_players']) + " allowed."
                return template('templates/error', **error_data)
            if len(seats) < sit_index:
                seats = seats + [""] * (sit_index - len(seats))
                game['seats'] = seats
            if seats[sit_index - 1] == "":
                seats[sit_index - 1] = cookie
            else:
                error_data['error_message'] = "Could not sit. Seat " + str(sit_index) + " taken."
                return template('templates/error', **error_data)
            print("seats", seats)
                
            error_message = "Could not sit. Seat may be taken or seats may be full."

    return redirect('/game/' + id + '/lobby')

@app.route('/game/<id:re:[a-zA-Z]*>/textplay')
def game_play_text(id):
    print("'Game Play Text' called.")
    cookie = get_session()
    error_data = {
      "error_message": "An error ocurred.",
      "destination": "/game/" + id + "/textplay",
    }
    try:
        game = T(data.Game, data.games[id])
    except KeyError:
        error_data['destination'] = '/'
        # the id should be clean because it matches the id regex which only allows letters.
        error_data['error_message'] = "Unknown game: '" + id + '" '
        return template('templates/error', **error_data)
    paradigm = game_paradigms[game['info']['paradigm']]
    info = game['info']
    status = game['status']
    seats = game['seats']
    my_seat = 0
    player_count = 0
    for i in range(len(seats)):
        if len(seats[i]):
            player_count += 1
        if seats[i] == cookie:
            my_seat = i + 1

    if not status['is_started']:
        # make sure only players can start the game, not spectators.
        if my_seat == 0:
            error_data['error_message'] = "Game hasn't started."
            error_data['destination'] = "/game/" + id + "/lobby"
            return template('templates/error', **error_data)

        # check minimum player count
        if player_count < info['min_players']:
            error_data['error_message'] = "Not enough players to start."
            error_data['destination'] = "/game/" + id + "/lobby"
            return template('templates/error', **error_data)

        # remove empty seats
        game['seats'] = [seat for seat in seats if len(seat)]
        init_args = {
            "player_count" : player_count
        }
        #print(init_args)

        game['state'] = paradigm.init(init_args)
        status['is_started'] = True


    text_handler = paradigm.text_handler
    view = text_handler['view']
    # TODO handle post request
    # parseMove = text_handler['parseMove']
    # move = parseMove(
    print(game)
    game_text = view(game['state'])

    template_data = {
        "game_id" : id,
        "game_text" : game_text,
        "seats" : ["x" if len(seat) else "" for seat in seats],
        "my_seat" : my_seat,
        "info" : info,
    }

    return template('templates/text_game', **template_data)





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



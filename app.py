
import sys, os

# require python 3
if sys.version_info[0] != 3:
    raise Exception("Python 3 required.")


import json, string, copy, re, random
import settings, util, data

from value_types import typecheck as T

import bottle
from bottle import Bottle, request, response, template, abort, \
                   static_file, BaseTemplate, redirect

from games import games

abs_app_dir_path = os.path.dirname(os.path.realpath(__file__))
abs_views_path = os.path.join(abs_app_dir_path, 'views')
bottle.TEMPLATE_PATH.insert(0, abs_views_path )
print("Template Path", bottle.TEMPLATE_PATH)

with open(settings.NAV_FILE) as file:
    BaseTemplate.defaults['nav_header'] = file.read()


game_paradigms = {}
paradigm_info = {}
for game in games:
    paradigm_info[game.info['paradigm']] = T(data.GameParadigmInfo, game.info)
    game_paradigms[game.info['paradigm']] = game

def get_session():
    cookie = request.get_cookie(settings.COOKIE_NAME)
    # check if cookie is exists
    if cookie and cookie in data.cookies:
        data.save_if_time()
        return cookie
    cookie = util.gen_token(settings.COOKIE_LEN, tries=settings.GEN_ID_TRIES,
                            taken=data.cookies, chars=string.ascii_letters.upper())
    response.set_cookie(settings.COOKIE_NAME, cookie)
    data.cookies.add(cookie)
    data.save_if_time()
    return cookie


app = Bottle()
@app.route('/')
def index():
    get_session()
    return redirect('/opengames')

@app.route('/static/<filepath:re:.*>', method="GET")
def static_resource(filepath):
    return static_file(filepath, root="static")

def list_game_info_helper(games, game_filter):
    game_info_list = []
    for game_id, game in games.items():
        status = game['status']
        game_info = copy.deepcopy(game['info'])
        game_info['id'] = game_id
        play_state = ""
        if status['is_started']:
            if status['is_finished']:
                play_state = "Finished"
            else:
                play_state = "Active"
        else:
            if status['is_finished']:
                play_state = "Aborted"
            else:
                play_state = "Open"
        game_info['play_state'] = play_state
        # filter the game list
        if not game_filter(game_info):
            continue
        game_info_list.append(T(data.GameListInfo, game_info))
    game_info_list.sort(key=lambda x: {"Open":0, "Active": 1, "Finished": 2, "Aborted": 3}[x['play_state']])
    return T([data.GameListInfo], game_info_list)



@app.route('/opengames')
def open_games():
    get_session()
    game_info_list = list_game_info_helper(data.games,
        lambda game: game['play_state'] == "Open")
    data.save_if_time()
    return template('list_games', game_list=game_info_list, list_title="Open")



@app.route('/activegames')
def active_games():
    get_session()
    game_info_list = list_game_info_helper(data.games,
        lambda game: game['play_state'] == "Active")
    data.save_if_time()
    return template('list_games', game_list=game_info_list, list_title="Active")



@app.route('/mygames')
def my_games():
    cookie = get_session()
    player_game_set = T(data.PlayerGames, data.player_games).get(cookie, set())
    player_game_dict = {}
    for game_id in player_game_set:
        player_game_dict[game_id] = data.games[game_id]

    game_info_list = list_game_info_helper(player_game_dict,
        lambda game: True)
    data.save_if_time()
    return template('list_games', game_list=game_info_list, list_title="My")

#newgame_template = SimpleTemplate(pages.new_game_tmpl)
@app.route('/new', method='GET')
def games_new_page():
    get_session()
    _data = {
        "paradigms" : paradigm_info
    }
    data.save_if_time()
    return template('new_game', data=_data)


# TODO json api vs page navigation.
@app.route('/new', method='POST')
def games_new_page():
    get_session()
    paradigm_name = request.forms.get('game_paradigm')
    min_players = int(request.forms.get('min_players'))
    max_players = int(request.forms.get('max_players'))
    live_seating = request.forms.get('live_seating', 'off') == 'on'
    choose_seats = request.forms.get('choose_seats') == 'on'
    enforce_turn_sequence = request.forms.get('enforce_turn_sequence', 'on') == 'on'


    if paradigm_name == None:
        raise ValueError('new_game: no paradigm attribute')
    try:
        game_paradigm_handler = game_paradigms[paradigm_name]
        paradigm_info = game_paradigm_handler.info
    except KeyError:
        raise ValueError('new_game: unknown game paradigm: ' + paradigm)

    # check against paradigm allowed values.
    paradigm_max_players = paradigm_info.get('max_allowed_players', 30)
    paradigm_min_players = paradigm_info.get('min_allowed_players', 1)

    if min_players == "" or min_players < paradigm_min_players:
        min_players = paradigm_min_players
    if max_players == "" or max_players > paradigm_max_players:
        max_players = paradigm_max_players

    game_args = {
        'paradigm': paradigm_name,
        'min_players': min_players,
        'max_players': max_players,
        'choose_seats': paradigm_info.get('allow_choose_seats', True) and choose_seats,
        'live_seating': paradigm_info.get('allow_live_seating', False) and live_seating,
        'enforce_turn_sequence' : "default_turn_sequence" in paradigm_info or
                                  paradigm_info.get('require_enforce_turn_sequence', True) or 
                                  enforce_turn_sequence,
    }

    game_info = { **copy.deepcopy(paradigm_info), **game_args }

    # init is handled when a player clicks start game.
    # init_state = {}
    # if hasattr(game_paradigm_handler, "init"):
    #    init_state = game_paradigm_handler.init(game_args)

    #print('game_args', game_args)

    game_id = util.gen_token(settings.GAME_ID_LEN)

    game = T(data.Game, {
        "state": None,
        "info": game_info,
        "status": {
            "is_started": False,
            "is_finished": False,
            "turn_count": 0},
        "chat": "",
        "seats": []
    })
    data.games[game_id] = game

    data.save_if_time()
    return redirect('/game/' + game_id + '/lobby')

@app.route('/game/<id:re:[a-zA-Z]*>/lobby', method="GET")
#@app.route('/game/<id:re:[a-zA-Z]*>/lobby', method="POST")
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
        return template('error', **error_data)


    if not id in data.games:
        return abort(404, "Unknown game id.")
    game = data.games[id]
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
    status = game['status']
    allow_seating = info.get('live_seating', False) or not status['is_started']
    seat_count = sum(x is not "" for x in seats)
    my_seat = 0
    for i in range(len(seats)):
        if seats[i] == cookie:
            my_seat = i + 1
    can_start = my_seat > 0 and (not status['is_started']) and seat_count >= info.get('min_players', 0)
    filtered_seats = ["x" if len(seat) else "" for seat in seats]
    #print("seat count, min_seats, can_start", seat_count, info.get('min_players', 0), can_start)

    #print("user 'my_seat'", my_seat)
    #print("seats", seats)

    template_data = {
        "game_id" : id,
        "can_start": can_start,
        "allow_seating" : allow_seating,
        "info" : info,
        "status" : status,
        "seats" : filtered_seats,
        "my_seat" : my_seat,
        "error_message" : error_message,
    }

    return template('lobby', **template_data)

# seat_index of -1 is used to stand.
@app.route('/game/<id:re:[a-zA-Z]*>/sit', method="POST")
def game_sit(id):
    #print("Game Sit called.")
    cookie = get_session()
    error_data = {
      "error_message": "An error ocurred.",
      "destination": "/game/" + id + "/lobby",
    }
    try:
        game = T(data.Game, data.games[id])
        player_games = T(data.PlayerGames, data.player_games)
        if not cookie in player_games:
            player_games[cookie] = set()
        player_games_set = player_games[cookie]
    except KeyError:
        error_data['destination'] = '/'
        # the id should be clean because it matches the id regex which only allows letters.
        error_data['error_message'] = "Unknown game: '" + id + '" '
        return template('error', **error_data)

    #print('game sit form', request.forms)
    info = game['info']
    seats = game['seats']
    status = game['status']
    allow_seating = info.get('live_seating', False) or not status['is_started']
    sit_index = int(request.forms.get("seat_index"))
    if not allow_seating:
        error_data['error_message'] = "Game started. Sitting or standing not allowed."
        return template('error', **error_data)
    else:
        if sit_index != None:
            #print("sitting:", sit_index)
            if sit_index < 0:
                if not cookie in seats:
                    error_data['error_message'] = "Could not stand. Perhaps you are not seated?"
                    return template('error', **error_data)
                else:
                    seats[seats.index(cookie)] = ""
                    player_games_set.remove(id)
            else:
                if sit_index == 0:
                    sit_index = 1
                    while sit_index - 1 < len(seats) and seats[sit_index - 1] != "":
                        sit_index += 1
                if sit_index > info['max_players']:
                    error_data['error_message'] = "Could not sit. Only " + str(info['max_players']) + " allowed."
                    return template('error', **error_data)
                if len(seats) < sit_index:
                    # fill in rest of blank seats
                    seats = seats + [""] * (sit_index - len(seats))
                    game['seats'] = seats
                if seats[sit_index - 1] == "":
                    seats[sit_index - 1] = cookie
                    player_games_set.add(id)
                else:
                    error_data['error_message'] = "Could not sit. Seat " + str(sit_index) + " taken."
                    return template('error', **error_data)

    data.save_if_time()
    return redirect('/game/' + id + '/lobby')

@app.route('/game/<id:re:[a-zA-Z]*>/textplay', method="POST")
@app.route('/game/<id:re:[a-zA-Z]*>/textplay', method="GET")
def game_play_text(id):
    #print("'Game Play Text' called.")
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
        return template('error', **error_data)
    paradigm = game_paradigms[game['info']['paradigm']]
    info = game['info']
    status = game['status']
    seats = game['seats']
    game_state = game['state']
    my_seat = 0
    player_count = 0
    enforce_turns = info.get("enforce_turn_sequence", True)
    turn_sequence = None
    if "turn_sequence" in info:
        turn_sequence = info["turn_sequence"]
        enforce_turns = True
    turn_count = status["turn_count"]
    my_turn = True
    turn_index = None # if turn order is not enforced, turn_index is meaningless.
    turn_count = status['turn_count']
    def process_turn_info():
        nonlocal my_turn
        nonlocal turn_count
        nonlocal turn_index
        my_turn = True
        turn_count = status['turn_count']
        if enforce_turns:
            turn_remainder = turn_count % player_count
            # the turn index may only correspond with filled seats.
            turn_index = 0
            while turn_remainder >= 0:
                turn_index += 1
                if turn_index > len(seats):
                    error_data['error_message'] = "Server error processing current turn."
                    error_data['destination'] = "/game/" + id + "/lobby"
                    return template('error', **error_data)
                if len(seats[turn_index - 1]) > 0:
                    turn_remainder -= 1
            if turn_sequence is not None:
                # if the turn sequence is less than the number of players, some won't ever get to move!
                if turn_remainder >= len(turn_sequence):
                    print("Warning: turn sequence is less than player count.")
                    turn_remainder = turn_count % len(turn_sequence)
                turn_index = turn_sequence[turn_index - 1]
            if turn_index == my_seat:
                my_turn = True
            else:
                my_turn = False

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
            return template('error', **error_data)

        # remove empty seats
        # randomize seating if choose_seats is allowed
        seats = [seat for seat in seats if len(seat)]
        # print('seat order', seats)
        if not info['choose_seats']:
            seats_left = seats.copy()
            seats = []
            while len(seats_left):
                seat = random.choice(seats_left)
                seats.append(seat)
                seats_left.remove(seat)
            # print('randomized seat order', seats)
        game['seats'] = seats
        init_args = {
            "player_count" : player_count
        }
        #print(init_args)

        game['state'] = paradigm.init(init_args)


        status['is_started'] = True

    process_turn_info()

    if not hasattr(paradigm, 'text_handler'):
        error_data['error_message'] = "Game has no text handler, cannot play in text mode."
        error_data['destination'] = "/game/" + id + "/lobby"
        return template('error', **error_data)

    text_handler = T(data.TextHandler, paradigm.text_handler)

    # TODO handle post request
    if request.method == "POST":
        if not my_turn:
            error_data['error_message'] = "" + game['info']['paradigm'] + ": Not your turn."
            error_data['destination'] = "/game/" + id + "/textplay"
            return template('error', **error_data)

        parseMove = text_handler['parseMove']
        # print(request.forms)
        move_text = request.forms.get("move_text")
        try:
            move = parseMove(move_text)
        except Exception as e:
            print("error while parsing text move: " + str(e))
            error_data['error_message'] = "" + game['info']['paradigm'] + ": Could not parse text move '" + move_text + "'"
            error_data['destination'] = "/game/" + id + "/textplay"
            return template('error', **error_data)

        try:
            if not paradigm.verify(game_state, move, my_seat):
                error_data['error_message'] = "" + game['info']['paradigm'] + ": \"" + move_text + "\" is not a legal move. "
                error_data['destination'] = "/game/" + id + "/textplay"
                return template('error', **error_data)
        except AssertionError as e:
            error_data['error_message'] = "" + game['info']['paradigm'] + ": \"" + move_text + "\" is not a legal move. " + str(e)
            error_data['destination'] = "/game/" + id + "/textplay"
            return template('error', **error_data)

        updated_game_state = paradigm.update(game_state, move, my_seat)
        game['state'] = updated_game_state
        game['status']['turn_count'] += 1
        score_result = paradigm.score(updated_game_state,)
        game['status']['score'] = score_result
        if score_result.get("game_over", False):
            game['status']['is_finished'] = True
        process_turn_info()

    view = text_handler['view']
    game_text = view(game['state'])
    square_link_template = "<a class='text_square' onclick='squareClick(\"%s\")' id='square_%s'>%s</a>"
    # todo handle csvView
    if 'csvNames' in text_handler:
        names = re.split(',\s+', text_handler['csvNames'])
        lines = [list(filter((lambda x: x != " "), list(line))) for line in game_text.split("\n")]
        # print('lines', lines)
        values = []
        for line in lines:
            if len(line) > 0:
                line[-1] += "\n"
            values.extend(line)
        squares = zip(names, values)
        # print('squares', squares)
        game_text = "".join([square_link_template % (name, name, value) for (name, value) in squares])
        # print('game_text', game_text)

    # print(game_text)
    move_list = None
    if "moves" in text_handler:
        move_list = text_handler['moves'](game['state'])

    #print("move_list", move_list)

    template_data = {
        "game_id" : id,
        "game_name" : info['paradigm'],
        "info" : info,
        "game_text" : game_text,
        "move_list" : move_list,
        "seats" : ["x" if len(seat) else "" for seat in seats],
        "my_seat" : my_seat,
        "my_turn" : my_turn,
        "turn_index" : turn_index,
        "turn_count" : turn_count,
        "status" : game['status'],
        "score" : game['status'].get('score', None),
    }

    # save data
    data.save_if_time()
    return template('text_game', **template_data)


"""

@app.route('/game/<id:re:[a-zA-Z]*>/stand')
def game_stand():
    pass
"""

@app.route('/game/<id:re:[a-zA-Z]*>/move')
def game_move():
    cookie = get_session()
    pass

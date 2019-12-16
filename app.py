
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

login_info = {
    "logged_in": False,
    "is_admin": False,
}

BaseTemplate.defaults['login_info'] = login_info
login_info['logged_in'] = True

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
        user_id = data.cookies[cookie]
        return user_id
    cookie = util.gen_token(settings.COOKIE_LEN, tries=settings.COOKIE_TRIES,
                            taken=data.cookies)
    user_id = util.gen_token(settings.USER_ID_LEN, tries=settings.GEN_ID_TRIES,
                            taken=data.user_ids)
    response.set_cookie(settings.COOKIE_NAME, cookie)
    data.user_ids.add(user_id)
    data.cookies[cookie] = user_id
    data.save_if_time()
    return user_id


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

@app.route('/lists')
def list_links():
    get_session()
    return template('list_links')


@app.route('/opengames')
def open_games():
    get_session()
    game_info_list = list_game_info_helper(data.games,
        lambda game: game['play_state'] == "Open")
    data.save_if_time()
    return template('list_games', game_list=game_info_list, list_title="open")




@app.route('/activegames')
def active_games():
    get_session()
    game_info_list = list_game_info_helper(data.games,
        lambda game: game['play_state'] == "Active")
    data.save_if_time()
    return template('list_games', game_list=game_info_list, list_title="active")

@app.route('/finishedgames')
def finished_games():
    get_session()
    game_info_list = list_game_info_helper(data.games,
        lambda game: game['play_state'] == "Finished")
    data.save_if_time()
    return template('list_games', game_list=game_info_list, list_title="finished")


@app.route('/admin')
def admin():
    return template('admin')

@app.route('/mygames')
def my_games():
    cookie = get_session()
    player_game_set = T(data.PlayerGames, data.player_games).get(cookie, set())
    player_game_dict = {}
    # all the games a player has joined and not left, but only non-deleted games are listed.
    for game_id in player_game_set:
        player_game_dict[game_id] = data.games[game_id]

    game_info_list = list_game_info_helper(player_game_dict,
        lambda game: True)
    data.save_if_time()
    return template('list_games', game_list=game_info_list, list_title="my")

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
    multi_sit = request.forms.get('multi_sit', 'off') == 'on'
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
        'multi_sit' : multi_sit,
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

    game_id = util.gen_token(settings.GAME_ID_LEN, taken=data.games, tries=settings.GEN_ID_TRIES, chars=string.ascii_uppercase)

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


@app.route('/game/<id:re:[a-zA-Z]*>/delete', method="POST")
def delete_game():
    cookie = get_session()
    pass
    # if settings.ALL_ADMIN or data.user_info[]
    

    

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
    is_seated = False
    player_number = 0
    filtered_seats = []
    cookie_seats = {}
    #### print('seat', seats, 'cookie', cookie)
    for i in range(len(seats)):
        seat_cookie = seats[i]
        if seat_cookie == cookie:
            is_seated = True
        if len(seat_cookie):
            cookie_seat_list = cookie_seats.get(seat_cookie, [])
            cookie_seat_list.append(i + 1)
            cookie_seats[seat_cookie] = cookie_seat_list
            if seat_cookie == cookie:
                filtered_seats.append("me")
            else:
                player_number = cookie_seat_list[0]
                filtered_seats.append(str(player_number))
        else:
            filtered_seats.append("")
    can_start = is_seated and (not status['is_started']) and seat_count >= info.get('min_players', 0)

    #print("seat count, min_seats, can_start", seat_count, info.get('min_players', 0), can_start)

    #print("seats", seats)

    template_data = {
        "game_id" : id,
        "can_start": can_start,
        "allow_seating" : allow_seating,
        "info" : info,
        "status" : status,
        "is_seated" : is_seated,
        "seats" : filtered_seats,
        "error_message" : error_message,
    }

    return template('lobby', **template_data)

# a negative sit_index is used to stand from the specified seat.
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
    multi_sit = info.get('multi_sit', False)
    is_seated = cookie in seats
    if not allow_seating:
        error_data['error_message'] = "Game started. Sitting or standing not allowed."
        return template('error', **error_data)
    else:
        if sit_index != None:
            #print("sitting:", sit_index)
            if sit_index < 0:
                sit_index = -sit_index
                if sit_index > len(seats) or seats[sit_index - 1] != cookie:
                    error_data['error_message'] = "Could not stand from seat %s. Perhaps you are not seated there?" % (sit_index)
                    return template('error', **error_data)
                else:
                    seats[sit_index-1] = ""
                    if not (cookie in seats):
                        player_games_set.remove(id)
            elif not is_seated or multi_sit:
                if sit_index == 0:
                    sit_index = 1
                    while sit_index - 1 < len(seats) and seats[sit_index - 1] != "":
                        sit_index += 1
                seat = seats[sit_index - 1] if sit_index - 1 < len(seats) else ""
                # ensure at least one empty slot in seats
                if sit_index > info['max_players']:
                    error_data['error_message'] = "Could not sit. Only " + str(info['max_players']) + " allowed."
                    return template('error', **error_data)
                if len(seats) < sit_index:
                    # fill in rest of blank seats
                    seats = seats + [""] * (sit_index - len(seats))
                    game['seats'] = seats
                if seat == "":
                    seats[sit_index - 1] = cookie
                    player_games_set.add(id)
                else:
                    error_data['error_message'] = "Could not sit. Seat " + str(sit_index) + " taken."
                    return template('error', **error_data)
            else:
                error_data['error_message'] = "Could not sit because you were already seated and multi-sit is not allowed."
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
    player_count = 0
    enforce_turns = info.get("enforce_turn_sequence", True)
    turn_sequence = None
    if "turn_sequence" in info:
        turn_sequence = info["turn_sequence"]
        enforce_turns = True
    turn_count = status["turn_count"]
    my_turn = True
    seat_number = None # if turn order is not enforced, seat_number for the current turn is meaningless.
    player_number = 0
    def process_turn_info():
        nonlocal my_turn
        nonlocal turn_count
        nonlocal seat_number
        my_turn = True
        turn_count = status['turn_count']
        if enforce_turns:
            turn_remainder = turn_count % player_count
            # the turn index may only correspond with filled seats.
            seat_number = 0
            while turn_remainder >= 0:
                seat_number += 1
                if seat_number > len(seats):
                    error_data['error_message'] = "Server error processing current turn."
                    error_data['destination'] = "/game/" + id + "/lobby"
                    return template('error', **error_data)
                if len(seats[seat_number - 1]) > 0:
                    turn_remainder -= 1
            if turn_sequence is not None:
                # if the turn sequence is less than the number of players, some won't ever get to move!
                if turn_remainder >= len(turn_sequence):
                    print("Warning: turn sequence is less than player count.")
                    turn_remainder = turn_count % len(turn_sequence)
                seat_number = turn_sequence[seat_number - 1]
            if seats[seat_number - 1] == cookie:
                my_turn = True
            else:
                my_turn = False

    for i in range(len(seats)):
        if len(seats[i]):
            player_count += 1
        if seats[i] == cookie and player_number == 0:
            player_number = i + 1

    if not status['is_started']:
        # make sure only players can start the game, not spectators.
        if player_number == 0:
            error_data['error_message'] = "Game hasn't started."
            error_data['destination'] = "/game/" + id + "/lobby"
            return template('error', **error_data)

        # check minimum player count
        if player_count < info['min_players']:
            error_data['error_message'] = "Not enough players to start."
            error_data['destination'] = "/game/" + id + "/lobby"
            return template('error', **error_data)

        # remove empty seats
        # randomize seating if choose_seats is not allowed
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

    illegal_move = None

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
            #print('move', move)
        except Exception as e:
            print("error while parsing text move: " + str(e))
            error_data['error_message'] = "" + game['info']['paradigm'] + ": Could not parse text move '" + move_text + "'"
            error_data['destination'] = "/game/" + id + "/textplay"
            return template('error', **error_data)

        try:
            if not paradigm.verify(game_state, move, seat_number):
                illegal_move = move_text
        except AssertionError as e:
            illegal_move = move_text
            error_data['error_message'] = "" + game['info']['paradigm'] + ": \"" + move_text + "\" is not a legal move. " + str(e)
            error_data['destination'] = "/game/" + id + "/textplay"
            return template('error', **error_data)

        if not illegal_move:
            updated_game_state = paradigm.update(game_state, move, seat_number)
            game['state'] = updated_game_state
            game['status']['turn_count'] += 1
            if hasattr(paradigm, 'score'):
                score_result = paradigm.score(updated_game_state,)
                game['status']['score'] = score_result
                if score_result.get("game_over", False):
                    game['status']['is_finished'] = True
            process_turn_info()

    view = text_handler['view']
    try:
        #print('game state', game['state'])
        game_text = view(game['state'])
    except Exception as e:
        error_data['error_message'] = "" + game['info']['paradigm'] + ": error rendering view. " + str(e)
        error_data['destination'] = "/game/" + id + "/textplay"
        return template('error', **error_data)
        
    square_link_template = "<a class='text_square' onclick='squareClick(\"%s\")' id='square_%s'>%s</a>"
    static_square_template = "<span class='text_square'>%s</span>"
    render_square = (lambda name, value:
        (square_link_template % (name, name, value)) if my_turn else (static_square_template % value))

    # todo handle csvView
    if 'squareNames' in text_handler:
        names = re.split(',\s*', text_handler['squareNames'])
        lines = [list(filter((lambda x: x != " "), list(line))) for line in game_text.split("\n")]
        values = []
        for line in lines:
            if len(line) > 0:
                line[-1] += "\n"
            values.extend(line)
        squares = zip(names, values)
        game_text = "".join([render_square(name, value) for (name, value) in squares])

    move_list = None
    if "moves" in text_handler:
        move_list = text_handler['moves'](game['state'])

    seat_count = sum(x is not "" for x in seats)
    is_seated = False
    filtered_seats = []
    cookie_seats = {}
    is_multi_player = False
    player_number = 0
    #### print('seat', seats, 'cookie', cookie)
    for i in range(len(seats)):
        seat_cookie = seats[i]
        if seat_cookie == cookie:
            is_seated = True
        if len(seat_cookie):
            cookie_seat_list = cookie_seats.get(seat_cookie, [])
            cookie_seat_list.append(i + 1)
            if seat_number:
                if i == seat_number -1:
                    player_number = cookie_seat_list[0]
                if len(cookie_seat_list) > 1:
                    is_multi_player = True
            cookie_seats[seat_cookie] = cookie_seat_list
            if seat_cookie == cookie:
                filtered_seats.append("me")
            else:
                player_number = cookie_seat_list[0]
                filtered_seats.append(str(player_number))
        else:
            filtered_seats.append("")
    #if 
    move_prompt = ""
    if seat_number > 0:
       if my_turn:
           move_prompt += "Your Turn: "
       #move_prompt += "Turn: "
       move_prompt += "<b>"
       move_prompt += "Player " + str(player_number)
       if is_multi_player:
           move_prompt += ", Seat " + str(seat_number) + "."
       move_prompt += "</b>"
    else:
       move_prompt = "No fixed turn sequence."

    end_game_message = ""
    score = game['status'].get('score', None)
    if score:
        if "winners" in score:
            for winner in score["winners"]:
                end_game_message += "<br>"
                if seats[winner - 1] == cookie:
                    end_game_message += "You won: "
                else:
                    end_game_message += "Winner(s): "
                winner_player_number = None
                try: # catch any index errors
                    winner_cookie = seats[winner - 1]
                    cookie_seat_list = cookie_seats.get(winner_cookie, [])
                    winner_player_number = cookie_seat_list[0]
                except:
                    pass
                end_game_message += "Player " + str(player_number)
                if is_multi_player:
                    end_game_message += ", Seat " + str(winner)
        if "losers" in score:
            for loser in score["losers"]:
                end_game_message += "<br>"
                if seats[loser - 1] == cookie:
                    end_game_message += "You lost: "
                else:
                    end_game_message += "Loser(s): "
                loser_player_number = None
                try: # catch any index errors
                    loser_cookie = seats[loser - 1]
                    cookie_seat_list = cookie_seats.get(loser_cookie, [])
                    loser_player_number = cookie_seat_list[0]
                except:
                    pass
                end_game_message += "Player " + str(loser_player_number)
                if is_multi_player:
                    end_game_message += ", Seat " + str(loser)
                
    # print("game_text", game_text)

    template_data = {
        "game_id" : id,
        "game_name" : info['paradigm'],
        "info" : info,
        "game_text" : game_text,
        "move_list" : move_list,
        "seats" : ["x" if len(seat) else "" for seat in seats],
        #"my_seat" : my_seat,
        "my_turn" : my_turn,
        "player_number" : player_number,
        "seat_number" : seat_number,
        "is_multi_player" : is_multi_player,
        "move_prompt": move_prompt,
        "turn_count" : turn_count,
        "status" : game['status'],
        "score" : game['status'].get('score', None),
        "illegal_move" : illegal_move,
        "multi_move" : text_handler.get("multiMove", False),
        "single_move" : text_handler.get("singleMove", False),
        "end_game_message": end_game_message,
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

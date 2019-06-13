

import pickledb
import os
import random
import string
import copy

try:
    from jsonschema import validate
except:
    print("jsonschema not available, no validation will be performed.")
    validate = lambda x,y: True

import games.nim as NimHandler

handler_list = [NimHandler] 
handlers = {}
for handler in handler_list:
    handlers[handler.info['name']] = handler

def default(_default, value):
    if value == None or value == False:
        return _default
    return value

# todo factor to config.py
DATA_FOLDER = 'data'
GAME_DATA_FOLDER = DATA_FOLDER + "/games"
META_DB = 'games_info.db'


# keys with another part only have a trailing pipe on the prefix.
# single keys have leading and trailing pipe.

# meta keys
GAME_INFO_KEY = 'game_info|'
GAME_LIST_KEY = '|game_list|'

# per game keys
SEATS_KEY = 'player_seats|'
STATE_KEY = '|game_state|'
SCORE_KEY = '|game_score|'

GEN_ID_TRIES = 6 
ID_LEN = 4

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

if not os.path.exists(GAME_DATA_FOLDER):
    os.makedirs(GAME_DATA_FOLDER)

meta_db = pickledb.load(DATA_FOLDER + "/" + META_DB, False)

def __gen_randomstring(n):
    return ''.join(random.choice(string.ascii_letters) for x in range(n))

def __gen_game_id():
    for i in range(GEN_ID_TRIES):
        id = __gen_randomstring(ID_LEN)
        if not meta_db.get(GAME_INFO_KEY + id):
            return id
    raise Exception("Could not find available id")
 
def __get_game_db(game_id):
    if not meta_db.get(GAME_INFO_KEY + game_id):
        raise ValueError("unknown game id: " + game_id)
    db = pickledb.load(GAME_DATA_FOLDER + "/" + game_id + ".db", True)
    return db
    
#TODO schema for settings
GameArgsSchema = {
    "type": "object"}

  

# TODO handle concurrent access

# for now, the user token is the users session cookie, but that could be changed to an internal per game identifier, such as player index.

def new_game(args):
    paradigm = args['paradigm']
    try:
        handler = handlers[paradigm]
    except KeyError:
        raise ArgumentError('GameHandler.new_game: paradigm required.')
    game_id = __gen_game_id()
    """
    try:
        validate(args, GameArgsSchema)
    except:
        return None"""
    game_list = default([], meta_db.get(GAME_LIST_KEY))
    game_list_entry = copy.deepcopy(args)
    game_list_entry['id'] = game_id
    game_list_entry['paradigm'] = paradigm
    game_list.append(game_list_entry)
    meta_db.set(GAME_INFO_KEY + game_id, args)
    meta_db.set(GAME_LIST_KEY, game_list)
    meta_db.dump()
    game_db = __get_game_db(game_id)
    #game_db.set

    return game_id

def list_games():
    return default([], meta_db.get(GAME_LIST_KEY))

def game_info(game_id):
    return default(None, meta_db.get(GAME_INFO_KEY + game_id))

def game_move(game_id, user_token, move):
    game_db = __game_db(game_id)
    pass

def game_sit(game_id, user_token, seat):
    game_db = __game_db(game_id)
    db = pickledb.load()
    pass

# 0 if they are not in this game.
def game_seat(game_id, user_token):
    game_db = __game_db(game_id)
    pass

def game_stand(game_id, user_token):
    game_db = __game_db(game_id)
    pass


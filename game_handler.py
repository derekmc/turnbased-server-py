

import pickledb
import os

# todo factor to config.py
DATA_FOLDER = 'data'
GAME_DATA_FOLDER = DATA_FOLDER + "/games"
META_DB = 'games_info.db'


# keys with another part only have a trailing pipe on the prefix.
# single keys have leading and trailing pipe.

# meta keys
GAME_INFO_KEY = 'game_info|'

# per game keys
SEATS_KEY = 'player_seats|'
STATE_KEY = '|game_state|'
SCORE_KEY = '|game_score|'


if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

if not os.path.exists(GAME_DATA_FOLDER):
    os.makedirs(GAME_DATA_FOLDER)

meta_db = pickledb.load(DATA_FOLDER + "/" + META_DB, True)

   

# TODO handle concurrent access

# for now, the user token is the users session cookie, but that could be changed to an internal per game identifier, such as player index.

def new_game():
    pass

def game_move(game_id, user_token, move):
    if not meta_db.get(GAME_INFO_KEY + game_id):
        return "unknown game"

    db = pickledb.load(GAME_DATA_FOLDER + "/" + game_id + ".db", True)
    pass

def game_sit(game_id, user_token, seat):
    db = pickledb.load()
    pass

def game_stand(game_id, user_token):
   pass


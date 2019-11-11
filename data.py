

import settings, sched, time, pickle, datetime

from value_types import typecheck as T

# seconds to wait between saving
# set to 0 to save after every operation.
SAVE_TIME = 30 
last_save = datetime.datetime.now()

# for now, the user_token is just their cookie
games = {} # {"id": {state, info, status, chat, "seats": [user_token]}
player_games = {} # {"user_token": [game_id]}
cookies = set()  # { "woiSSeDJ" }
       

#"status": {seat_scores, seat_ranks, seat_winners, seat_losers, is_started, is_finished}
STATUS_STARTED = "STARTED"
STATUS_NEW = "NEW"
STATUS_FINISHED = "FINISHED"

# ValueTypes type definitions for Game Datastructures
SeatIndex = 0
NumericScore = 0
SeatRank = 0 # a seat rank value of zero means no rank.
UserToken = "example_token" # for now this is just the cookie
GameID = "example_game_id"
PlayerGames = {"" : set([""])} # for now this is just a string -> [string] dictionary.

GameScore = { "$seat_scores": [NumericScore],
              "$seat_ranks": [SeatRank],
              "$winners": [SeatIndex],
              "$losers": [SeatIndex],
              "$game_over": False,}

GameStatus = { "is_started": False,
               "is_finished": False,
               "turn_count": 0,
               "$score": GameScore }

GameParadigmInfo = {
    "paradigm": "",
    "$version": "",
    "$min_allowed_players": 0,
    "$max_allowed_players": 0,
    "$default_turn_sequence": [0],
    "$require_enforce_turn_sequence": True, # if there is a default turn sequence, this is ignored and assumed to be true.  Also defaults to true if left blank.
    "$allow_live_seating": False,
    "$allow_choose_seats": True, }

GameInfo = {
   **GameParadigmInfo,
    "min_players": 0,
    "max_players": 0,
   # turn timing
   "$initial_time": 0, # total starting time
   "$turn_time": 0, # fixed amount of time per turn
   "$turn_time_increment": 0, # time added to total time each turn.
   # player stuff
   # An instantiated game may overwrite the following properties from its paradigm:
   # min_players, max_players
   # Values for the following properties are restricted based on the paradigms value
   "$live_seating" : False, # may only be true if "allow_live_seating" is True.
   "$choose_seats" : False, # may only be true if "allow_choose_seats" is True.
   "$enforce_turn_sequence" : True, # must be true if "require_enforce_turn_sequence" is True.
   "$turn_sequence" : [0], # TODO copied from "default_turn_sequence", unless the initialized state has a key called "turn_sequenc"
}

GameListInfo = {
  **GameInfo,
  "id" : GameID,
  "play_state": "Open|Active|Finished|Aborted", } # todo value types should handle this enumerated string value literal.

TextHandler = {
    "parseMove" : None, # currently valuetypes does not handle functions
    "view" : None,
    "$moves" : None, # optional function computing legal moves
}

Game = { "state": None,
         "info": GameInfo,
         "status": GameStatus,
         "$chat": "",
         "seats": [UserToken]}

def dump():
    state = {"games": games, "player_games": player_games, "cookies": cookies}
    try:
        with open(settings.DATA_FILE, 'wb') as f:
            pickle.dump(state, f)
        if settings.VERBOSE:
            print("Data saved successfully.")
    except IOError as e:
        print("\"%s\" could not save data file." % (settings.DATA_FILE,))
        print(e)
    except pickle.PicklingError as e:
        print("\"%s\" data file could not be pickled." % (settings.DATA_FILE,))
        print(e)

def load():
    global games, player_games, cookies
    try:
        with open(settings.DATA_FILE, 'rb') as f:
            state = pickle.load(f)
        games = T({"": Game}, state['games'])
        player_games = T(PlayerGames, state['player_games'])
        cookies = T({UserToken}, state['cookies'])
        if settings.VERBOSE:
            print("Data loaded successfully.")
    except FileNotFoundError as e:
        print("\"%s\" data file not found." % (settings.DATA_FILE,))
        print(e)
    except pickle.UnpicklingError as e:
        print("\"%s\" data file could not be unpickled." % (settings.DATA_FILE,))
        print(e)
    except TypeError as e:
        print("\"%s\" data was invalid type." % (settings.DATA_FILE,))
        print(e)

# dumps the data if a sufficient delay has passed since last save
def save_if_time():
    now = datetime.datetime.now()
    global last_save
    delay = now - last_save
    #print('last save was ' + str(delay.seconds) + ' seconds ago.')
    if delay.days > 0 or delay.seconds > SAVE_TIME:
        if settings.VERBOSE:
            print("Saving data...", now)
        dump()
        last_save = now



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
               "$score": GameScore}

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

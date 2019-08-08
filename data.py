

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
GameScore = { "$seat_scores": [NumericScore],
              "$seat_ranks": [SeatRank], 
              "$winners": [SeatIndex],
              "$losers": [SeatIndex], 
              "$game_over": False,}

GameStatus = { "is_started": False,
               "is_finished": False,
               "$score": GameScore}

GameInfo = {
             "paradigm": "",
             "$version": "",
             # configuration and turn stuff
             "$turn_sequence": [0],
             "$initial_time": 0, # total starting time
             "$turn_time": 0, # fixed amount of time per turn
             "$turn_time_increment": 0, # time added to total time each turn.
             #player stuff
             "min_players": 0,
             "max_players": 0,
             # TODO "$live_seating": False,
             "$choose_seats": False, }

Game = { "state": None,
         "info": GameInfo,
         "status": GameStatus,
         "$chat": "",
         "seats": [UserToken]}



games = {} # {"id": {state, info, status, chat, "seats": [cookies]}
cookies = set()  # { "woiSSeDJ" }

#"status": {seat_scores, seat_ranks, seat_winners, seat_losers, is_started, is_finished}
STATUS_STARTED = "STARTED"
STATUS_NEW = "NEW"
STATUS_FINISHED = "FINISHED"

# Value Types for Game Datastructures
SeatIndex = 0
GameScore = {"$seat_scores": [0], "$seat_ranks": [0], "$winners": [SeatIndex], "$losers": [SeatIndex]}
GameStatus = {"is_started": False, "is_finished": False, "$score": GameScore}
GameInfo = { "name": "", "$version": "", "min_players": 0, "max_players": 0, "live_seating": False }
Game = {"state": None, "info": GameInfo, "status": GameStatus, "$chat": "", "seats": ["cookie"]}


from value_types import typecheck as T
import re

info = {
    "paradigm": "Tic Tac Toe",
    "version": "dev",
    "allow_live_seating": False,
    "min_allowed_players": 2,
    "max_allowed_players": 2,
    "require_enforce_turn_sequence" : True,
}


TTTBoard = [0,0,0, 0,0,0, 0,0,0]

__pieces = "-XO"
__square_names = "a1, a2, a3, b1, b2, b3, c1, c2, c3"
__square_map = {}

for i,square in enumerate(re.split(',\s*', __square_names)):
    __square_map[square] = i

def __board_to_text(board):
    #print('board to text', board)
    board = [__pieces[n] for n in board]
    row1 = " ".join(board[0:3])
    row2 = " ".join(board[3:6])
    row3 = " ".join(board[6:9])
    return "\n".join([row1, row2, row3])
 

def __parse_move(move):
    # print('move, map, result', move, __square_map)
    return __square_map[move]

text_handler = {
    "view": lambda data: __board_to_text(data['board']),
    "parseMove": __parse_move,
    "squareNames": __square_names,
    "singleMove" : True,
}

def init(init_args):
    data = {
        "board": [0,0,0,0,0,0,0,0,0]
    }
    return data

def verify(data, move, seat):
    board = data['board']
    assert board[move] == 0, "square is not empty"
    return True

def update(data, move, seat):
    board = data['board']
    board[move] = seat
    return data

# def view
def score(state, seat=0):
    board = state['board']
    runs = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [6,4,2]]
    for run in runs:
        [a, b, c] = [board[x] for x in run]
        if a>0 and a==b and b==c:
            return {'winners': [a], 'game_over': True}
    return {}




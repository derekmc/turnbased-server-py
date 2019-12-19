
from value_types import typecheck as T
import re, string

info = {
    "paradigm": "Four In a Line",
    "version": "dev",
    "allow_live_seating": False,
    "min_allowed_players": 2,
    "max_allowed_players": 4,
    "require_enforce_turn_sequence" : True,
}

"""
"""
def genColumnNames(n):
    letters = string.ascii_lowercase
    count = len(letters)
    if n <= count:
        return letters[0:n].split()
    if n <= count*count:
        return [a + b for a in letters for b in letters][0:n]
    if n <= count*count*count:
        return [a + b + c for a in letters for b in letters for c in letters][0:n]
    raise ValueError("n is too big to generate column names.")

RANKS = 6
COLUMNS = 7
N = COLUMNS * RANKS
FourInALineBoard = [0] * N
COLUMN_NAMES = genColumnNames(N)
RUN_LENGTH = 4

__pieces = "-XOYZ"
__square_names = ", ".join([column + str(rank) for column in COLUMN_NAMES for rank in reversed(range(1, RANKS+1))])
__square_map = {}

for i,square in enumerate(re.split(',\s*', __square_names)):
    __square_map[square] = i

def __board_to_text(board):
    #print('board to text', board)
    board = [__pieces[n] for n in board]
    result = ""
    for i in reversed(range(RANKS)):
        result += " ".join(board[i*COLUMNS : (i+1) * COLUMNS])
        result += "\n"
    return result
 

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
    #TODO require even number of players
    data = {
        "board": FourInALineBoard.copy()
    }
    return data

def verify(data, move, seat):
    board = data['board']
    square = move % COLUMNS
    while board[square] > 0:
        square += COLUMNS
        if square >= RANKS * COLUMNS:
            raise Exception("Column is full")
    return True

def update(data, move, seat):
    board = data['board']
    square = move % COLUMNS
    while board[square] > 0:
        square += COLUMNS
        if square >= RANKS * COLUMNS:
            raise Exception("Column is full")
    board[square] = seat
    return data

def genRuns():
    runs = []
    for i in range(COLUMNS):
        for j in range(RANKS):
            start = i + j*COLUMNS
            # vertical
            if j <= RANKS - RUN_LENGTH:
                offset = COLUMNS
                runs.append([start + k*offset for k in range(RUN_LENGTH)])
            # horizontal
            if i <= COLUMNS - RUN_LENGTH:
                offset = 1
                runs.append([start + k*offset for k in range(RUN_LENGTH)])
            # diagonal 1
            if j <= RANKS - RUN_LENGTH and i <= COLUMNS - RUN_LENGTH:
                offset = 1 + COLUMNS
                runs.append([start + k*offset for k in range(RUN_LENGTH)])
            # diagonal 2
            if j <= RANKS - RUN_LENGTH and i >= RUN_LENGTH - 1:
                offset = COLUMNS - 1
                runs.append([start + k*offset for k in range(RUN_LENGTH)])
    return runs

           

# def view
def score(state, seat=0):
    board = state['board']
    runs = genRuns()
    for run in runs:
        player = board[run[0]]
        if player > 0:
            is_run = True
            for i in range(1,RUN_LENGTH):
                if player != board[run[i]]:
                    is_run = False
                    break
            if is_run:
                return {'winners': [player], 'game_over': True}
    return {}

def test():
    print("Four in a line tests!")
    runs = genRuns()
    print("Runs", [",".join(map(str, run)) for run in runs])
    print('9 columns: ', " ".join(genColumnNames(47)))
    print('47 columns: ', " ".join(genColumnNames(47)))
    print('999 columns: ', " ".join(genColumnNames(999)))
    # should throw error
    #print('99999 columns: ', " ".join(genColumnNames(99999)))

if __name__ == "__main__":
    test()


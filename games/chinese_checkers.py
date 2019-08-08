
info = {
    "paradigm": "Chinese Checkers",
    "version": "dev",
    "live_seating": False,
    # TODO make sure turns go around the board counter clockwise, instead of in 
    "turn_sequence": [1, 4, 5, 2, 3, 6],
    "min_players": 2,
    "max_players": 6,
}

def __board_to_text(board):
    lines = board.split("\n")
    n = len(lines)
    result = ""
    for i in range(n):
        line = lines[i]
        result += " " * (n - i - 1) + " ".join(line.split("")) + "\n"
    return result

def __parse_move(move):
    array = move.split(',')
    return zip(array[0::2], array[1::2])

text_handler = {
   "view" : lambda data: __board_to_text(data['board']),
   "parseMove" : __parse_move,
}

# visual board layout
"""
             1
            1 1
           1 1 1
          1 1 1 1 
 6 6 6 6           4 4 4 4
  6 6 6             4 4 4
   6 6               4 4
    6                 4

    3                 5
   3 3               5 5
  3 3 3             5 5 5
 3 3 3 3           5 5 5 5
          2 2 2 2
           2 2 2
            2 2
             2
"""



# dashes represent squares that can't be filled.
start_board_str = """
----1
----11
----111
----1111 
6666     4444
-666      444
--66       44
---6        4
----         -
----3        5
----33       55
----333      555
----3333     5555
---------2222
----------222
-----------22
------------2
"""

pieces_str = '- 123456'

piece_dict = {}

for i in range(len(pieces_str)):
    piece = pieces_str[i]
    # first piece is negative 1
    piece_dict[piece] = i - 1


def parse_board(s):
    return [row.split("") for row in s.split("\n")]


def __get_board(board, pos):
    x = pos[0]
    y = pos[1]

    if y < 0 or y >= len(board):
        return -1

    row = board[y]

    if x < 0 or x >= len(row):
        return -1

    piece = piece_dict.get(row[x], -1)

    return piece



def __set_board(board, pos, piece):
    x = pos[0]
    y = pos[1]

    if y < 0 or y >= len(board):
        return False

    row = board[y]

    if x < 0 or x >= len(row):
        return False

    if piece < -1 or piece > 6:
        piece = -1

    piece_character = pieces_str[piece - 1]
    row[x] = piece_character

    return True



def __is_valid_move(board, pos_list):

    single_step = (len(pos_list) == 2)

    for i in range(len(pos_list) - 1):
        a = pos_list[i]
        b = pos_list[i+1]

        dx = b[0] - a[0]
        dy = b[1] - a[1]
        adx = abs(dx)
        ady = abs(dy)

        # midpoint of a, b
        c = (a[0] + dx/2, a[1] + dy/2)

        # source piece
        p = __get_board(board, a)

        # destination piece
        q = __get_board(board, b)

        # middle piece
        r = __get_board(board, c)

        # cannot go off board
        if q == -1:
            return False

        # source must have piece, destination and intermediate steps may not
        if ((i==0) != (p > 0)) or q > 0:
            return False

        valid_step = False

        # move or jump in y direction.
        valid_step = (valid_step or
            dx == 0 and (ady == 1 and single_step or
                         ady == 2 and r > 0))

        # move or jump in x direction.
        valid_step = (valid_step or
            dy == 0 and (adx == 1 and single_step or
                         adx == 2 and r > 0))

        # move or jump along y=x diagonal
        valid_step = (valid_step or
            abx == 1 and aby == 1 and dx == dy and single_step or
            abx == 2 and aby == 2 and dx == dy and r > 0)

        if not valid_step:
            return False



def __make_move(board, pos_list):
    a = pos_list[0]
    b = pos_list[len(pos_list) - 1]
    piece = __get_board(board, a)
    __set_board(board, b, piece)



def init(init_args):
    player_count = init_args.get('player_count', 2),
    board_str = start_board_str

    for i in range(player_count + 1, 6):
        board_str = board_str.replace
    data = {
        'player_count' : player_count,
        'board' : start_board_str,
    }
    return data

# move is a list of position tuples, but fixed length arrays should also work.
def verify(data, move, seat):
    board = parse_board(data.board)
    piece = __get_board(board, move[0])

    # TODO validation of datstructures.
    return __is_valid_move(board, move)


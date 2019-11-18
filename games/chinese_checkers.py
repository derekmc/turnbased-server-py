
info = {
    "paradigm": "Chinese Checkers",
    "version": "dev",
    "allow_live_seating": False,
    # TODO make sure turns go around the board counter clockwise, instead of in 
    "default_turn_sequence": [1, 4, 5, 2, 3, 6],
    "require_enforce_turn_sequence" : True,
    "min_allowed_players": 2,
    "max_allowed_players": 6,
}

def __board_to_text(board):
    lines = board.replace('-', '').replace(' ', '.').split("\n")
    return "\n".join([" ".join(list(line)) for line in lines])

def __raw_board_str(board):
    return "\n".join(["".join(row) for row in board])


def __parse_move(move):
    squares = move.split('-')
    return [(ord(square[0]) - ord('a') + 1, int(square[1:]) - 1) for square in squares]

text_handler = {
   "view" : lambda data: __board_to_text(data['board']),
   "parseMove" : __parse_move,
   "multiMove" : True,
   "squareNames" : "e1, e2, f2, e3, f3, g3, e4, f4, g4, h4, " +
                "a5, b5, c5, d5, e5, f5, g5, h5, i5, j5, k5, l5, m5, " +
                "b6, c6, d6, e6, f6, g6, h6, i6, j6, k6, l6, m6, " +
                "c7, d7, e7, f7, g7, h7, i7, j7, k7, l7, m7, " +
                "d8, e8, f8, g8, h8, i8, j8, k8, l8, m8, " +
                "e9, f9, g9, h9, i9, j9, k9, l9, m9, " +
                "e10, f10, g10, h10, i10, j10, k10, l10, m10, n10, " +
                "e11, f11, g11, h11, i11, j11, k11, l11, m11, n11, o11, " +
                "e12, f12, g12, h12, i12, j12, k12, l12, m12, n12, o12, p12, " +
                "e13, f13, g13, h13, i13, j13, k13, l13, m13, n13, o13, p13, q13, " +
                "j14, k14, l14, m14, k15, l15, m15, l16, m16, m17",
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
#ABCDEFGHIJKLMNOPQ#
start_board_str = """
-----1-------------
-----11------------
-----111-----------
-----1111----------
-6666     4444-----
--666      444-----
---66       44-----
----6        4-----
-----         -----
-----3        5----
-----33       55---
-----333      555--
-----3333     5555-
----------2222-----
-----------222-----
------------22-----
-------------2-----
"""

pieces_str = '- 123456'

piece_dict = {}

for i in range(len(pieces_str)):
    piece = pieces_str[i]
    # first piece is negative 1
    piece_dict[piece] = i - 1


def parse_board(s):
    return [list(row) for row in s.strip().split("\n")]


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

    #row[x] = piece
    piece_character = pieces_str[piece + 1]
    row[x] = piece_character

    return True



def __is_valid_move(board, pos_list):

    if len(pos_list) < 2: # must move to a new square
        return False

    single_step = (len(pos_list) == 2)

    for i in range(len(pos_list) - 1):
        a = pos_list[i]
        b = pos_list[i+1]

        dx = b[0] - a[0]
        dy = b[1] - a[1]
        adx = abs(dx)
        ady = abs(dy)

        # must move to new square.
        if dx == 0 and dy == 0:
            return False

        # midpoint of a, b
        c = (a[0] + int(dx/2), a[1] + int(dy/2))

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
            adx == 1 and ady == 1 and dx == dy and single_step or
            adx == 2 and ady == 2 and dx == dy and r > 0)

        if not valid_step:
            return False
    return True



def __make_move(board, pos_list):
    a = pos_list[0]
    b = pos_list[-1]
    piece = __get_board(board, a)
    __set_board(board, b, piece)
    __set_board(board, a, 0)



def init(init_args):
    print('init chinese checkers', init_args)
    player_count = 2
    if 'player_count' in init_args:
        player_count = init_args['player_count']
    board_str = start_board_str

    for i in range(int(player_count) + 1, 7):
        board_str = board_str.replace(str(i), " ")
    data = {
        'player_count' : player_count,
        'board' : board_str
    }
    return data

# move is a list of position tuples, but fixed length arrays should also work.
def verify(data, move, seat):
    board = parse_board(data['board'])
    piece = __get_board(board, move[0])

    # TODO validation of datstructures.
    return __is_valid_move(board, move)

def update(data, move, seat):
    board = parse_board(data['board'])
    __make_move(board, move)
    data['board'] = __raw_board_str(board)
    return data


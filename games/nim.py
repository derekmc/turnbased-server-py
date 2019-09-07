
from value_types import typecheck as T

NimMove = {"take": 0}
NimInit = {"$stones": 0}
NimState = {"turn": 0, "stones": 0}

def __turn_seat(turn, seats=2):
    return (turn - 1)%seats + 1

text_handler = {
   "view" : lambda state: str(state['stones']) + " stones remain.",
   "moves" : lambda state: ["1"] if state["stones"] == 1 else ["1", "2"],
   "parseMove" : lambda move_text: {"take": int(move_text)},
}

info = {
  "paradigm": "Nim",
  "version" : 'dev',
  "enforce_turn_sequence" : True,
  "live_seating" : False,
  "min_players": 2,
  "max_players": 2,
}



def init(init_args):
    state = {
        'turn': 1,
        'stones': 10
    }
    if init_args:
        #validate(init_args, NimInitSchema)
        if 'stones' in init_args:
            state['stones'] = init_args['stones']
    return state


def verify(state, move, seat):
    T(NimState, state);
    T(NimMove, move);
    stones = state['stones']
    turn = state['turn']
    take = move['take']
    assert take == 1 and take == 2,  "must take 1 or 2 stones"
    assert take <= stones,          "cannot take " + take + " stones, only " + stones + " remain(s)."
    assert seat == 1 or seat == 2,  "only 2 seats allowed"
    assert seat == __turn_seat(turn), "not your turn"
    return True

def update(state, move, seat):
    state['stones'] -= move['take']
    state['turn'] += 1
    return state

def view(state, seat=0):
    return state

def score(state, seat=0):
    stones = state['stones']
    turn = state['turn']
    if stones <= 0:
        return {'winners': [__turn_seat(turn)], 'losers': [__turn_seat(turn+1)], 'game_over': True}
    return {}

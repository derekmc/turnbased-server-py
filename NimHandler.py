
import json
try:
    from jsonschema import validate
except:
    print("jsonschema not available, no validation will be performed.")
    validate = lambda x,y: True

NimStateSchema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "turn": {"type": "integer"},
        "stones": {"type": "integer"}}}

NimMoveSchema = {
    "type": "object",
    "additionalProperties": False,
    "properties" : {
      "take" : {"type": "integer"}}}

NimInitSchema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "stones": {"type": "integer"}}}



def init(init_args):
    data = {
        'turn': 1,
        'stones': 10
    }
    if init_args:
        validate(init_args, NimInitSchema)
        data['stones'] = init_args['stones']
    return data
    

def verify(data, move, seat):
    validate(data, NimStateSchema);
    validate(move, NimMoveSchema);
    stones = data['stones']
    turn = data['turn']
    take = move['take']
    assert take ==1 or take==2,    "must take 1 or 2 stones"
    assert take <= stones,         "cannot take " + take + " stones, only " + stones + " remains."
    assert seat==1 or seat==2,     "only 2 seats allowed"
    assert seat == [2, 1][turn%2], "not your turn"
    return True
    # print(state, move)

def update(data, move, seat):
    data['stones'] -= move['take']
    data['turn'] += 1
    return data

def view(data, seat=0):
    return data

def score(data, seat=0):
    stones = data['stones']
    turn = data['turn']
    if stones <= 0:
        return {'winner': [2, 1][turn%2], 'finished': True}
    return {}



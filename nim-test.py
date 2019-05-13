
import json
import NimHandler as handler

GameScoreSchema = {
    "type": "object"
}

def test():
    data_str = '{"stones": 5, "turn":5}'
    move_str = '{"take":1}'

    data = json.loads(data_str)
    move = json.loads(move_str)

    print('verify', handler.verify(data, move, 1))
    print('update', handler.update(data, move, 1))



test()


from json import loads
import unittest
import NimHandler as handler

GameScoreSchema = {
    "type": "object"
}

class NimTest(unittest.TestCase):
    def test(self):
        # print("Testing Game:", handler.GameParadigm, "version:", handler.Version)
        handler.verify(
            loads('{"stones": 10, "turn":1}'),
            loads('{"take":2}'),
            seat=1)

        self.assertRaises(AssertionError, handler.verify,
            loads('{"stones": 10, "turn":1}'),
            loads('{"take":2}'),
            seat=2)

        self.assertRaises(AssertionError, handler.verify,
            loads('{"stones": 10, "turn":2}'),
            loads('{"take":3}'),
            seat=2)
         
def test():
    unittest.main(exit=False)

test()


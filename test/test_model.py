from unittest import TestCase
from src.model import Model
from pprint import pprint

class TestModel(TestCase):


    def test_segments(self):
        terrain_map = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [1, 1, 1, 0, 1],
            [1, 1, 0, 0, 1],
            [1, 1, 0, 0, 0]
        ]

        start = (3, 4)
        finish = (0, 1)
        model = Model(terrain_map, n_turns=3, start=start, finish=finish)

        turns = [(3, 2), (3, 0), (1, 0)]
        expected = [((3, 4), (3, 2)),
                    ((3, 2), (3, 0)),
                    ((3, 0), (1, 0)),
                    ((1, 0), (0, 1))]
        self.assertSequenceEqual(model._segments(turns), expected)






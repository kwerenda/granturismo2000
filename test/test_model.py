from unittest import TestCase
from src.model import Model, Point
from pprint import pprint
import math

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
        model = Model(terrain_map, n_turns=3, start=start, finish=finish,
                      weight_segment=1, weight_turn=1)

        turns = [(3, 2), (3, 0), (1, 0)]
        # turns = [Point(*x) for x in turns]
        expected = [((3, 4), (3, 2)),
                    ((3, 2), (3, 0)),
                    ((3, 0), (1, 0)),
                    ((1, 0), (0, 1))]
        # expected = [(Point(*x), Point(*y)) for x, y in expected]
        self.assertSequenceEqual(model._segments(turns), expected)


    def test_fitness(self):
        terrain_map = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [1, 1, 1, 0, 1],
            [1, 1, 0, 0, 1],
            [1, 1, 0, 0, 0]
        ]

        start = Point(3, 4)
        finish = Point(0, 1)
        model = Model(terrain_map, n_turns=3, start=start, finish=finish,
                      weight_segment=1, weight_turn=0)

        turns = [Point(*x) for x in [(3, 2), (3, 0), (1, 0)]]

        fitness = model.get_fitness(turns)

        self.assertAlmostEqual(fitness, 6 + math.sqrt(2))






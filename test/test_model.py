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

    def test_discrete_line(self):
        self.assertSequenceEqual(Model._discrete_line(Point(1, 2), Point(3, 6)),
                                 [Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 4), Point(2, 5), Point(3, 5),
                                  Point(3, 6)])
        self.assertSequenceEqual(Model._discrete_line(Point(1, 1), Point(4, 4)),
                                 [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)])
        self.assertSequenceEqual(Model._discrete_line(Point(1, 1), Point(1, 4)),
                                 [Point(1, 1), Point(1, 2), Point(1, 3), Point(1, 4)])
        self.assertSequenceEqual(Model._discrete_line(Point(1, 4), Point(1, 1)),
                                 [Point(1, 4), Point(1, 3), Point(1, 2), Point(1, 1)])



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






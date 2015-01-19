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
        self.assertSequenceEqual(Model.discrete_line(Point(1, 2), Point(3, 6)),
                                 [Point(1, 2), Point(1, 3), Point(2, 3), Point(2, 4), Point(2, 5), Point(3, 5),
                                  Point(3, 6)])
        self.assertSequenceEqual(Model.discrete_line(Point(1, 1), Point(4, 4)),
                                 [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)])
        self.assertSequenceEqual(Model.discrete_line(Point(1, 1), Point(1, 4)),
                                 [Point(1, 1), Point(1, 2), Point(1, 3), Point(1, 4)])
        self.assertSequenceEqual(Model.discrete_line(Point(1, 4), Point(1, 1)),
                                 [Point(1, 4), Point(1, 3), Point(1, 2), Point(1, 1)])



    def test_fitness(self):
        terrain_map = [
            [0.1, 0.1, 0.1, 0.1, 0.1],
            [0.1, 1, 1,  0.1, 0.1],
            [1, 1, 1, 0.1, 1],
            [1, 1, 0.1, 0.1, 1],
            [1, 1, 0.1, 0.1, 0.1]
        ]

        start = Point(3, 4)
        finish = Point(0, 1)
        model = Model(terrain_map, n_turns=3, start=start, finish=finish,
                      weight_segment=1, weight_turn=0)

        turns = [Point(*x) for x in [(3, 2), (3, 0), (1, 0)]]

        fitness = model.get_fitness(turns)

        # self.assertAlmostEqual(fitness, 6 + math.sqrt(2))
        self.assertEqual(fitness, 0.4) #TODO wyliczyc co tu powinno


    def test_dist(self):
        self.assertEqual(Point.dist(Point(0, 0), Point(0, 0)), 0)

        self.assertEqual(Point.dist(Point(0, 0), Point(0, 1)), 1)

        self.assertEqual(Point.dist(Point(0, 1), Point(0, 0)), 1)

        self.assertAlmostEqual(Point.dist(Point(0, 0), Point(1, 1)), math.sqrt(2))

    def _angle_tester(self, A, B, P, expected):
            ang = Model._angle((A, P), (P, B))
            self.assertAlmostEqual(ang, expected)

    def test_angle_straight(self):
        A = Point(0, 2)
        P = Point(0, 1)
        B = Point(0, 0)
        self._angle_tester(A, B, P, math.pi)
        # ang = Model._angle((A, P), (P, B))
        # self.assertAlmostEqual(ang, math.pi)

    def test_angle_go_back(self):
        A = Point(0, 1)
        P = Point(0, 0)
        B = A
        self._angle_tester(A, B, P, 0)

    def test_angle_right(self):
        A = Point(0, 1)
        P = Point(0, 0)
        B = Point(1, 0)
        self._angle_tester(A, B, P, math.pi/2)

    def test_angle_obtuse(self):
        A = Point(0, 3)
        P = Point(0, 2)
        B = Point(1, 0)
        self._angle_tester(A, B, P, math.pi/2 + math.acos(1/math.sqrt(5)))

    def test_angle_obtuse_same(self):
        A = Point(1, 3)
        P = Point(1, 2)
        B = Point(0, 0)
        self._angle_tester(A, B, P, math.pi/2 + math.acos(1/math.sqrt(5)))

    def test_angle_acute(self):
        A = Point(1, 2)
        P = Point(1, 0)
        B = Point(0, 1)
        self._angle_tester(A, B, P, math.pi/4)

    def test_angle_acute_same(self):
        A = Point(1, 2)
        P = Point(1, 0)
        B = Point(2, 1)
        self._angle_tester(A, B, P, math.pi/4)







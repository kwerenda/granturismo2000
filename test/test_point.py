from unittest import TestCase

from src.model import Point
import math


class TestPoint(TestCase):

    def test_dist(self):
        A = Point(1, 1)
        B = Point(0, 3)
        self.assertAlmostEquals(Point.dist(A, B), math.sqrt(5))

    def test_create_random(self):
        max_x = 100
        max_y = 10
        A = Point.create_random(max_x, max_y)
        self.assertLess(A.x, max_x)
        self.assertGreater(A.x, 0)
        self.assertLess(A.y, max_y)
        self.assertGreater(A.y, 0)

    def test_eq(self):
        A = Point(10, 2)
        v = Point(-3, 4)

        self.assertFalse(A == v)
        self.assertTrue(A != v)

    def test_mult_vec(self):
        A = Point(10, 2)
        v = Point(-3, 4)

        self.assertEqual(A*v, Point(10*(-3), 2*4))

    def test_mult_scalar(self):
        A = Point(10, 2)
        s = -3.5
        self.assertEqual(s*A, Point((-3.5)*10, (-3.5)*2))


    def test_precedence(self):
        A = Point(10, 2)
        v = Point(-3, 4)

        B = Point(7, 6)
        self.assertEqual(A + v * B, Point(10 + (-3)*7, 2 + 4*6))

    def test_add(self):
        A = Point(-2.3, 12)
        B = Point(-3, 7)

        self.assertEqual(A+B, Point(-5.3, 19))

    def test_sub(self):
        A = Point(-2, 12)
        B = Point(-3, 7)

        self.assertEqual(A-B, Point(1, 5))

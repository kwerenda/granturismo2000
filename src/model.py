import math
from random import randrange
from src.scribe import ScribeEmpty


class Model(object):
    def __init__(self, terrain_map, n_turns, start, finish, weight_segment,
                 weight_turn, turn_penalty=lambda x: x ** 2):
        self.terrain_map = terrain_map
        self.n_turns = n_turns
        self.start = start
        self.finish = finish
        self.min_x = 0
        self.min_y = 0
        self.max_x = len(terrain_map) - 1
        self.max_y = len(terrain_map[0]) - 1
        self.weight_segment = weight_segment
        self.weight_turn = weight_turn
        self.turn_penalty = turn_penalty
        self.scribe = ScribeEmpty()

    def set_scribe(self, scribe):
        self.scribe = scribe

    def get_fitness(self, turns):
        time_segments = 0
        segments = self._segments(turns)
        tiles = []
        for segment in segments:
            for tile in self.discrete_line(segment[0], segment[1]):
                if not tiles or tiles[-1] != tile:
                    tiles.append(tile)

        for tile in tiles:
            time_segments += self.terrain_map[tile.x][tile.y]

        time_turns = 0
        for turn_nr in range(self.n_turns):
            time_turns += self._calculate_turn_penalty(segments[turn_nr], segments[turn_nr + 1])
        fitness = self.weight_segment * time_segments + self.weight_turn * time_turns
        self.scribe.increment_evaluation()
        return fitness

    @staticmethod
    def discrete_line(start_point, end_point):
        """
        vision line algorithm
        :return: list of points creating discrete line
        """

        x = start_point.x
        y = start_point.y
        result = [start_point]
        dx = end_point.x - start_point.x
        dy = end_point.y - start_point.y
        y_step = 1 if dy >= 0 else -1
        dy = -dy if dy < 0 else dy
        x_step = 1 if dx >= 0 else -1
        dx = -dx if dx < 0 else dx
        ddx = 2 * dx
        ddy = 2 * dy
        if ddx >= ddy:
            errorprev = error = dx
            for i in range(0, dx):
                x += x_step
                error += ddy
                if error > ddx:
                    y += y_step
                    error -= ddx
                    if error + errorprev < ddx:
                        result.append(Point(x, y - y_step))
                    elif error + errorprev > ddx:
                        result.append(Point(x - x_step, y))
                    else:
                        pass
                result.append(Point(x, y))
                errorprev = error
        else:
            errorprev = error = dy
            for i in range(0, dy):
                y += y_step
                error += ddx
                if error > ddy:
                    x += x_step
                    error -= ddy
                    if error + errorprev < ddy:
                        result.append(Point(x - x_step, y))
                    elif error + errorprev > ddy:
                        result.append(Point(x, y - y_step))
                    else:
                        pass
                result.append(Point(x, y))
                errorprev = error
        return result

    def _calculate_turn_penalty(self, segment1, segment2):
        angle = self._angle(segment1, segment2)
        return self.turn_penalty(math.pi - angle)

    @staticmethod
    def _angle(segment1, segment2):
        """Get angle between two segments in radians, in [0, pi]`"""
        assert (segment1[1] == segment2[0])
        A = segment1[0]
        B = segment2[1]
        P = segment1[1]

        a = Point.dist(A, P)
        b = Point.dist(P, B)
        c = Point.dist(A, B)

        denom = 2 * a * b
        if denom == 0:
            return 0
        arg = (a ** 2 + b ** 2 - c ** 2) / denom
        if -1 <= arg <= 1:
            return math.acos(arg)
        return 0

    def _segments(self, turns):
        solution = [self.start] + turns + [self.finish]
        return [(solution[i], solution[i + 1]) for i in range(self.n_turns + 1)]


class Point:
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + (-1)*other

    def __mul__(self, other):
        try:
            return Point(self.x*other.x, self.y*other.y)        # point, but actually vector
        except AttributeError:
            try:
                return Point(self.x*other[0], self.y*other[1])  # vector
            except TypeError:
                return Point(self.x*other, self.y*other)        # scalar


    def __rmul__(self, other):
        return self.__mul__(other)

    @staticmethod
    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    @staticmethod
    def create_random(max_x, max_y):
        return Point(randrange(max_x), randrange(max_y))


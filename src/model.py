import math


class Model(object):
    
    def __init__(self, terrain_map, n_turns, start, finish, weight_segment,
                 weight_turn, turn_penalty=lambda x: x**2):
        self.terrain_map = terrain_map
        self.n_turns = n_turns
        self.start = start
        self.finish = finish
        self.max_x = len(terrain_map[0])
        self.max_y = len(terrain_map)
        self.weight_segment = weight_segment
        self.weight_turn = weight_turn
        self.turn_penalty = turn_penalty


    def get_fitness(self, turns):

        # solution = [self.start] + turns + [self.finish]
        # segments = [(solution[i], solution[i+1]) for i in range(self.n_turns + 1)]

        time_segments = 0
        segments = self._segments(turns)
        for segment in segments:
            dist = Point.dist(segment[0], segment[1])

            time_segments += self.weight_segment*dist

        time_turns = 0
        for turn_nr in range(self.n_turns):
            angle = self._angle(segments[turn_nr], segments[turn_nr + 1])
            time_turns += self.weight_turn*self.turn_penalty(angle)

        return time_segments + time_turns


    @staticmethod
    def _angle(seg1, seg2):
        return 0 #TODO


    def _segment_len(self, segment):
        return math.sqrt(segment())


    def _segments(self, turns):
        solution = [self.start] + turns + [self.finish]
        return [(solution[i], solution[i+1]) for i in range(self.n_turns + 1)]



    # def get_random_solution(self):


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

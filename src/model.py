
class Model(object):
    
    def __init__(self, terrain_map, n_turns, start, finish):
        self.terrain_map = terrain_map
        self.n_turns = n_turns
        self.start = start
        self.finish = finish
        self.max_x = len(terrain_map[0])
        self.max_y = len(terrain_map)


    def get_fitness(self, turns):
        time = 0
        # solution = [self.start] + turns + [self.finish]
        # segments = [(solution[i], solution[i+1]) for i in range(self.n_turns + 1)]

        for segment in self._segments(turns):



    def _segments(self, turns):
        solution = [self.start] + turns + [self.finish]
        return [(solution[i], solution[i+1]) for i in range(self.n_turns + 1)]


    # def get_random_solution(self):



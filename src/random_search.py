from engine import Engine
from random import randrange
from model import Point

class RandomSearch(Engine):

    def step(self):
        pass

    def solve(self, iterations):
        it = 0
        best_fitness = float('inf')
        best_solution = []
        for it in range(iterations):
            solution = [Point(randrange(self._model.max_x), randrange(self._model.max_y)) for dim in self.dims]
            fitness = self._model.get_fitness(solution)
            if fitness > best_fitness:
                best_fitness = fitness
                best_solution = solution

        return best_fitness, best_solution





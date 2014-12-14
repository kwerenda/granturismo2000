from engine import Engine
from random import randrange


class RandomSearch(Engine):

    def step(self):
        pass

    def solve(self, iterations):
        it = 0
        bestFitness = float('inf')
        bestSolution = []
        for it in range(iterations):
            solution = [(randrange(self._model.max_x), randrange(self._model.max_y)) for dim in self.dims]
            fitness = self.model.get_fitness(solution)





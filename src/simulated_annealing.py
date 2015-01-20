import math
from src.engine import Engine
from random import randrange, random
from src.model import Point


class SimulatedAnnealing(Engine):
    T0 = 1000

    def _temperature(self, x):
        return x * self.T0

    def _neighbour(self, solution, T):
        area_x = int((T / self.T0 * self._model.max_x)) + 1
        area_y = int((T / self.T0 * self._model.max_y)) + 1
        point_finder = lambda val, area, max_val: min(max(randrange(val - area, val + area), 0), max_val)
        neighbour = [Point(point_finder(p.x, area_x, self._model.max_x-1),
                           point_finder(p.y, area_y, self._model.max_y-1)) for p in solution]
        return neighbour

    @staticmethod
    def _good_enough(fitness, new_fitness, T):
        dFitness = new_fitness - fitness
        return (dFitness >= 0.0 and math.exp(-dFitness / T) < random()) or dFitness < 0.0

    def step(self):
        pass

    def solve(self, iterations):
        solution = [Point(randrange(self._model.max_x), randrange(self._model.max_y)) for _ in range(self._dims)]
        fitness = self._model.get_fitness(solution)
        best_solution = solution
        best_fitness = fitness
        for it in range(iterations):
            T = self._temperature((iterations - it) / iterations)
            new_solution = self._neighbour(solution, T)
            new_fitness = self._model.get_fitness(new_solution)
            if self._good_enough(fitness, new_fitness, T):
                fitness = new_fitness
                solution = new_solution
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_solution = solution

        return best_fitness, best_solution
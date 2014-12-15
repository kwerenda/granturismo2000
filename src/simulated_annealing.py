from src.engine import Engine
from random import randrange
from src.model import Point


class SimulatedAnnealing(Engine):

    T0 = 100

    def _temperature(self, x):
        return x * self.T0

    def _neighbour(self, solution, T):
        #TODO: calculation of neighbour (take into consideration T?)
        pass

    def _good_enough(self, fitness, new_fitness, temperature):
        #TODO: check if good enough to move (with randomization)
        return True

    def step(self):
        pass

    def solve(self, iterations):
        solution = [Point(randrange(self._model.max_x), randrange(self._model.max_y)) for _ in self._dims]
        fitness = self._model.get_fitness(solution)
        best_solution = solution
        best_fitness = fitness
        for it in range(iterations):
            T = self._temperature((iterations-it)/iterations)
            new_solution = self._neighbour(solution, T)
            new_fitness = self._model.get_fitness(solution)
            if self._good_enough(fitness, new_fitness, T):
                fitness = new_fitness
                solution = new_solution
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_solution = solution

        return best_fitness, best_solution
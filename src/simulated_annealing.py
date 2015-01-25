import math
from src.engine import Engine
from random import randrange, random
from src.model import Point


class SimulatedAnnealing(Engine):

    def __init__(self, model, initial_temperature=1000, temperature_function=lambda init, param: init*param):
        super(SimulatedAnnealing, self).__init__(model)
        self._temperature_function = temperature_function
        self.T0 = initial_temperature
        self.T = self.T0
        self.fitness = 0

    @staticmethod
    def _good_enough(fitness, new_fitness, T):
        dFitness = new_fitness - fitness
        if math.exp(-dFitness / T) >= random():
            # print("Worse, but take T:{0}, exp: {1}, dFitness:{2}".format(T, math.exp(-dFitness / T), dFitness))
            return True
        else:
            return False

    def step(self):
        pass

    def _neighbour(self, solution):
        area_x = self._model.max_x // 10 + 1
        area_y = self._model.max_y // 10 + 1
        point_finder = lambda val, area, max_val: min(max(randrange(val - area, val + area), 0), max_val)
        neighbour = [Point(point_finder(p.x, area_x, self._model.max_x-1),
                           point_finder(p.y, area_y, self._model.max_y-1)) for p in solution]
        return neighbour

    def solve(self, iterations):
        solution = [Point(randrange(self._model.max_x), randrange(self._model.max_y)) for _ in range(self._dims)]
        self.fitness = self._model.get_fitness(solution)
        best_solution = solution
        self._best_fitness = self.fitness
        for it in range(iterations):
            self.T = self._temperature_function(self.T0, (iterations - it) / iterations)
            new_solution = self._neighbour(solution)
            new_fitness = self._model.get_fitness(new_solution)
            if self._good_enough(self.fitness, new_fitness, self.T):
                self.fitness = new_fitness
                solution = new_solution
                if self.fitness < self._best_fitness:
                    self._best_fitness = self.fitness
                    best_solution = solution

        return self._best_fitness, best_solution

    def get_fitness(self):
        return self.fitness


class SimulatedAnnealingVariableArea(SimulatedAnnealing):

    def _neighbour(self, solution):
        area_x = int((self.T / self.T0 * self._model.max_x)) + 1
        area_y = int((self.T / self.T0 * self._model.max_y)) + 1
        point_finder = lambda val, area, max_val: min(max(randrange(val - area, val + area), 0), max_val)
        neighbour = [Point(point_finder(p.x, area_x, self._model.max_x-1),
                           point_finder(p.y, area_y, self._model.max_y-1)) for p in solution]
        return neighbour
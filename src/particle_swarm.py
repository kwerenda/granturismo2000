from src.engine import Engine
from src.model import Point

from random import randrange, random


class ParticleSwarm(Engine):

    def __init__(self, model, swarm_size=1000, inertia=0.729, c_personal=1.49, c_social=1.49):
        super().__init__(model)
        self.swarm_size = swarm_size
        self.inertia = inertia
        self.c_personal = c_personal
        self.c_social = c_social

        self._global_best_fitness = float('inf')
        self._global_best_solution = []

    def step(self):
        pass

    def solve(self, iterations):
        self._initialize()

        for it in range(iterations):
            for particle in self._particles:
                particle.velocity = [self._new_velocity(particle, dim) for dim in range(self._dims)]
                particle.solution = [s + v for s, v in zip(particle.solution, particle.velocity)]
                particle.fitness = self._model.get_fitness(self._discretize(particle.solution))
                self._save_solution_if_better(particle)

        return self._global_best_fitness, self._global_best_solution

    def _new_velocity(self, particle, dim):
        v_inertia = self.inertia * particle.velocity[dim]
        v_personal = random()*(particle.best_solution[dim] - particle.solution[dim])
        v_social = random()*(self._global_best_solution[dim] - particle.solution[dim])
        return v_inertia + self.c_personal*v_personal + self.c_social*v_social

    def _initialize(self):
        self._particles = []
        for _ in range(self.swarm_size):
            new_solution = [Point.create_random(self._model.max_x, self._model.max_y) for _ in range(self._dims)]
            fitness = self._model.get_fitness(self._discretize(new_solution))
            start_velocity = [Point(0, 0)]*self._dims
            new_particle = Particle(new_solution, fitness, start_velocity)
            self._particles.append(new_particle)
            self._save_solution_if_better(new_particle)

    @staticmethod
    def _discretize(solution):
        return [Point(int(p.x), int(p.y)) for p in solution]

    # NEXT THING TODO: ADD BOUNDARIES TO VELOCITY





    def _save_solution_if_better(self, particle):
        if particle.fitness <= particle.best_fitness:
            particle.best_solution = particle.solution
            particle.best_fitness = particle.fitness
            if particle.fitness < self._global_best_fitness:
                        self._global_best_solution = particle.solution
                        self._global_best_fitness = particle.fitness

    def get_best_fitness(self):
        return self._global_best_fitness


class Particle(object):
    """Each particle in a swarm holds n-dimensional position and velocity in solutions space"""

    def __init__(self, solution, start_fitness, velocity):
        self.solution = solution
        self.fitness = start_fitness
        self.best_solution = solution
        self.best_fitness = self.fitness
        self.velocity = velocity






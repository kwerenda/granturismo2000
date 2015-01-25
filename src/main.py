from src.model import Model, Point
from src.random_search import RandomSearch
from src.scribe import ScribeInMemory, ScribeInMemoryFitness
from src.simulated_annealing import SimulatedAnnealing, SimulatedAnnealingVariableArea
from src.particle_swarm import ParticleSwarm
from pprint import pprint
from matplotlib import pyplot
import json
from src.terrain import *

BASE_WEIGHT = 0.1
MAP_HEIGHT = 60
MAP_WIDTH = 60
START = Point(0, MAP_HEIGHT-5)
FINISH = Point(MAP_WIDTH-1, 4)

WEIGHT_SEGMENT = 20.0
WEIGHT_TURN = 14.0
N_TURNS = 10
ITERATIONS = 10000

EXPERIMENTS = 10

N_HILLS = 10
MIN_RADIUS = 10
MAX_RADIUS = 20


def test_annealing(model, scribe):

    fitness, solution, best_fitness_array_var, fitness_array_var = run_experiments(model, scribe, SimulatedAnnealingVariableArea(model, temperature_function=lambda temp, param: temp*param**2),
                                                                                   EXPERIMENTS, True)
    fitness, solution, best_fitness_array, fitness_array = run_experiments(model, scribe, SimulatedAnnealing(model, temperature_function=lambda temp, param: temp*param**2),
                                                                           EXPERIMENTS, True)

    pyplot.figure()
    pyplot.title("Symulowane wyżarzanie - zmienny skok")
    pyplot.plot(best_fitness_array_var)
    pyplot.plot(fitness_array_var)

    pyplot.figure()
    pyplot.title("Symulowane wyżarzanie - bazowe")
    pyplot.plot(best_fitness_array)
    pyplot.plot(fitness_array)

    pyplot.figure()
    pyplot.title("Symulowanie wyżarzanie  - porównanie")
    pyplot.plot(best_fitness_array_var, label='Zmienny skok')
    pyplot.plot(best_fitness_array, label='Bazowe')
    pyplot.legend(loc='upper right')

    scribe.reset()

    return fitness, solution


def run_experiments(model, scribe, engine, number_of_experiments, with_fitness=False):

    best_fitness_arrays = []
    fitness_arrays = []
    fitness = float("inf")
    solution = []
    for i in range(number_of_experiments):
        fitness, solution = run_test(model, scribe, engine)
        best_fitness_arrays.append(scribe.get_best_fitness())
        if with_fitness:
            fitness_arrays.append(scribe.get_fitness())

    best_fitness_array = [sum(e)/len(e) for e in zip(*best_fitness_arrays)]
    fitness_array = [sum(e)/len(e) for e in zip(*fitness_arrays)]
    return fitness, solution, best_fitness_array, fitness_array


def run_test(model, scribe, engine):
    model.set_scribe(scribe)
    scribe.reset()
    scribe.set_engine(engine)
    fitness, solution = engine.solve(ITERATIONS)

    return fitness, solution


def print_solution(fitness, solution, terrain_map):
    print("Fitness: {0}".format(fitness))
    print("Solution:\n{}".format("\n".join([str(x) for x in solution])))
    json_solution = json.dumps([{"x": p.x, "y": p.y} for p in solution])
    json_map = json.dumps(terrain_map)
    discrete_solution = model.discrete_line(START, solution[0])
    discrete_solution.extend(model.discrete_line(solution[-1], FINISH))
    for i in range(len(solution)-1):
        discrete_solution.extend(model.discrete_line(solution[i], solution[i+1]))
    json_discrete_solution = json.dumps([{"x": p.x, "y": p.y} for p in discrete_solution])
    with open("../web/map.js", "w+") as output_data:
        output_data.write("map = {0};\n".format(json_map))
        output_data.write("start = {{x:{0},y:{1}}};\n".format(START.x, START.y))
        output_data.write("end = {{x:{0},y:{1}}};\n".format(FINISH.x, FINISH.y))
        output_data.write("route = {0};\n".format(json_solution))
        output_data.write("discrete_route = {0};\n".format(json_discrete_solution))


if __name__ == '__main__':

    terrain_map = generate_hill_terrain(MAP_WIDTH, MAP_HEIGHT, BASE_WEIGHT, N_HILLS, MIN_RADIUS, MAX_RADIUS)
    # terrain_map = terrain_map_1
    model = Model(terrain_map, N_TURNS, START, FINISH, WEIGHT_SEGMENT, WEIGHT_TURN, turn_penalty=lambda x: x**3)
    # engine = RandomSearch(model)
    # engine = SimulatedAnnealing(model)
    # engine = SimulatedAnnealingVariableArea(model)
    # engine = ParticleSwarm(model)

    # scribe = ScribeInMemory(engine)

    # fitness, solution = engine.solve(ITERATIONS)
    fitness, solution = test_annealing(model, ScribeInMemoryFitness())
    print_solution(fitness, solution, terrain_map)
    pyplot.show()


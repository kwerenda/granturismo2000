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
MAP_HEIGHT = 15
MAP_WIDTH = 90
START = Point(0, MAP_HEIGHT-5)
FINISH = Point(MAP_WIDTH-1, 4)

WEIGHT_SEGMENT = 20.0
WEIGHT_TURN = 14.0
N_TURNS = 8
ITERATIONS = 11000

EXPERIMENTS = 10

N_HILLS = 6
MIN_RADIUS = 6
MAX_RADIUS = 8


def get_it(data, it_number):
    return [x[it_number//10] for x in data]

# def plot_box(data, it_number, label):
#     pyplot.boxplot([x[it_number//10] for x in data])#, label=label)


def test_comparison(mode, scribe):
    nr_experiments = 10


    pso = run_experiments_all(model, scribe, ParticleSwarm(model), nr_experiments)

    eng_pso_var_temp = ParticleSwarm(model, inertia=0.9, inertion_cooling=True)
    pso_temp = run_experiments_all(model, scribe, eng_pso_var_temp, nr_experiments)

    eng_sa = SimulatedAnnealing(model, temperature_function=lambda temp, param: temp*param)
    sa = run_experiments_all(model, scribe, eng_sa, nr_experiments)

    eng_sa_var_temp = SimulatedAnnealingVariableArea(model, temperature_function=lambda temp, param: temp*param)
    sa_var = run_experiments_all(model, scribe, eng_sa_var_temp, nr_experiments)

    eng_ran = RandomSearch(model)
    ran = run_experiments_all(model, scribe, eng_ran, nr_experiments)

    for it_number in [100, 200, 1000, 5000, 10000]:

        pyplot.figure()
        pyplot.title("{} iterations, comparison".format(it_number))
        # pyplot.xlabel("Evaluations")
        pyplot.ylabel("Fitness")

        boxes = []
        boxes.append(get_it(pso, it_number))
        boxes.append(get_it(pso_temp, it_number))
        boxes.append(get_it(sa, it_number))
        boxes.append(get_it(sa_var, it_number))
        boxes.append(get_it(ran, it_number))
        # plot_box(pso, it_number, "PSO")
        # plot_box(pso_temp, it_number, "PSO inertion cooling")
        # plot_box(sa, it_number, "SA")
        # plot_box(sa_var, it_number, "SA variable area")
        # plot_box(ran, it_number, "Random search")

        pyplot.boxplot(boxes, labels=["PSO", "PSO inertion cooling", "SA", "SA variable area", "Random search"])
    # pyplot.legend()
    pyplot.show()


def test_pso_swarm_sizes(model, scribe):
    nr_experiments = 10
    pyplot.figure()
    pyplot.title("PSO - swarm size")
    pyplot.xlabel("Evaluations")
    pyplot.ylabel("Fitness")

    for swarm_size in [10, 100, 500, 1000]:

        _fitness, _solution, best_fitness_array, _ = run_experiments(
            model, scribe, ParticleSwarm(model, swarm_size=swarm_size), nr_experiments)
        scribe.reset()
        its = range(0, ITERATIONS, scribe.period)
        pyplot.plot(its, best_fitness_array[:len(its)], label="Swarm size {}".format(swarm_size))

    pyplot.legend()
    pyplot.show()

def test_pso_draw(model, scribe):
    nr_experiments = 10
    fitness, solution, best_fitness_array, _ = run_experiments(model, scribe, ParticleSwarm(model, swarm_size=100), nr_experiments)
    return fitness, solution

def test_pso(model, scribe):
    nr_experiments = 10
    its = range(0, ITERATIONS, scribe.period)

    pyplot.figure()
    # pyplot.title("PSO")
    pyplot.xlabel("Evaluations")
    pyplot.ylabel("Fitness")

    fitness, solution, best_fitness_array, _ = run_experiments(model, scribe, ParticleSwarm(model, swarm_size=100), nr_experiments)
    pyplot.plot(its, best_fitness_array[:len(its)], label="plain PSO")


    fitness, solution, best_fitness_array, _ = run_experiments(model, scribe, ParticleSwarm(model, swarm_size=100, inertia=0.9, inertion_cooling=True), nr_experiments)

    pyplot.plot(its, best_fitness_array[:len(its)], label="PSO with inertion cooling")

    fitness, solution, best_fitness_array, _ = run_experiments(model, scribe, RandomSearch(model), nr_experiments)
    pyplot.plot(its, best_fitness_array[:len(its)], label="Random search")

    pyplot.legend()
    # pyplot.show()

    # pyplot.plot(fitness_array)


    scribe.reset()

    return fitness, solution

def test_annealing(model, scribe):

    fitness, solution, best_fitness_array_var, fitness_array_var = run_experiments(model, scribe, SimulatedAnnealingVariableArea(model, temperature_function=lambda temp, param: temp*param),
                                                                                   EXPERIMENTS, True)
    fitness, solution, best_fitness_array, fitness_array = run_experiments(model, scribe, SimulatedAnnealing(model, temperature_function=lambda temp, param: temp*param),
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


def run_experiments_all(model, scribe, engine, number_of_experiments):

    best_fitness_arrays = []

    for i in range(number_of_experiments):
        fitness, solution = run_test(model, scribe, engine)

        best_fitness_arrays.append(scribe.get_best_fitness())

    # best_fitness_array = [sum(e)/len(e) for e in zip(*best_fitness_arrays)]
    # fitness_array = [sum(e)/len(e) for e in zip(*fitness_arrays)]
    # return best_fit, best_sol, best_fitness_array, fitness_array
    return best_fitness_arrays


def run_experiments(model, scribe, engine, number_of_experiments, with_fitness=False):

    best_fitness_arrays = []
    fitness_arrays = []
    best_fit = float("inf")
    best_sol = []
    for i in range(number_of_experiments):
        fitness, solution = run_test(model, scribe, engine)
        if best_fit > fitness:
            best_fit = fitness
            best_sol = solution
        best_fitness_arrays.append(scribe.get_best_fitness())
        if with_fitness:
            fitness_arrays.append(scribe.get_fitness())

    best_fitness_array = [sum(e)/len(e) for e in zip(*best_fitness_arrays)]
    fitness_array = [sum(e)/len(e) for e in zip(*fitness_arrays)]
    return best_fit, best_sol, best_fitness_array, fitness_array


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

    # terrain_map = generate_hill_terrain(MAP_WIDTH, MAP_HEIGHT, BASE_WEIGHT, N_HILLS, MIN_RADIUS, MAX_RADIUS)
    terrain_map = terrain_map_7
    model = Model(terrain_map, N_TURNS, START, FINISH, WEIGHT_SEGMENT, WEIGHT_TURN, turn_penalty=lambda x: x**3)
    # engine = RandomSearch(model)
    # engine = SimulatedAnnealing(model)
    # engine = SimulatedAnnealingVariableArea(model)
    # engine = ParticleSwarm(model)

    # scribe = ScribeInMemory(engine)

    # fitness, solution = engine.solve(ITERATIONS)
    # fitness, solution = test_annealing(model, ScribeInMemory(period=10))

    # test_pso_swarm_sizes(model, ScribeInMemory(period=10))
    # test_comparison(model, ScribeInMemory(period=10))
    # test_pso(model, ScribeInMemory(period=10))

    fitness, solution = test_pso_draw(model, ScribeInMemory(period=10))
    print_solution(fitness, solution, terrain_map)
    pyplot.show()


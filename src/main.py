from src.model import Model, Point
from src.random_search import RandomSearch
from src.simulated_annealing import SimulatedAnnealing
from src.particle_swarm import ParticleSwarm
from pprint import pprint
import json
from src.terrain import generate_hill_terrain

BASE_WEIGHT = 0.1
MAP_HEIGHT = 30
MAP_WIDTH = 30
START = Point(0, MAP_HEIGHT-5)
FINISH = Point(MAP_WIDTH-1, 4)

WEIGHT_SEGMENT = 2.0
WEIGHT_TURN = 14.0
N_TURNS = 5
ITERATIONS = 1000

N_HILLS = 50


if __name__ == '__main__':

    # terrain_map = [
    #     [0.1, 0.1, 0.1, 0.1, 0.1],
    #     [0.1, 1, 0.5, 0.1, 0.1],
    #     [0.3, 1, 1, 0.1, 1],
    #     [0.7, 1, 0.1, 0.1, 1],
    #     [0.7, 0.8, 0.1, 0.1, 0.1]
    # ]

    terrain_map = generate_hill_terrain(MAP_WIDTH, MAP_HEIGHT, BASE_WEIGHT, N_HILLS)

    model = Model(terrain_map, N_TURNS, START, FINISH, WEIGHT_SEGMENT, WEIGHT_TURN)  # engine = RandomSearch(model)
    engine = SimulatedAnnealing(model)
<<<<<<< HEAD
    # engine = ParticleSwarm(model)
    fitness, solution = engine.solve(iterations)
=======
    fitness, solution = engine.solve(ITERATIONS)
>>>>>>> 44a1b1c361321b4e2e605a388d78ffae36c3276c
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

    # solution - lista punktow i jakosc rozwiazania


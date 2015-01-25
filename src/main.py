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
ITERATIONS = 10

N_HILLS = 10

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

    # terrain_map = [
    #     [0.1, 0.1, 0.1, 0.1, 0.1],
    #     [0.1, 1, 0.5, 0.1, 0.1],
    #     [0.3, 1, 1, 0.1, 1],
    #     [0.7, 1, 0.1, 0.1, 1],
    #     [0.7, 0.8, 0.1, 0.1, 0.1]
    # ]

    terrain_map = generate_hill_terrain(MAP_WIDTH, MAP_HEIGHT, BASE_WEIGHT, N_HILLS)

    # terrain_map = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 1, 1, 1, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.3333333333333333, 0.419753086419753, 0.5740740740740741, 0.6666666666666666, 1, 1, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.34074074074074073, 0.4259259259259259, 0.5679012345679012, 0.5, 0.6666666666666666, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.26666666666666666, 0.3333333333333333, 0.4888888888888889, 0.7037037037037036, 0.5679012345679012, 0.5740740740740741, 0.419753086419753, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.34074074074074073, 0.3333333333333333, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5555555555555555, 0.5679012345679012, 0.4259259259259259, 0.34074074074074073, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.3333333333333333, 0.34074074074074073, 0.3333333333333333, 0.26666666666666666, 0.1, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 1, 1, 1, 0.7037037037037036, 0.4888888888888889, 0.3333333333333333, 0.1, 0.1, 0.1, 0.1], [0.16666666666666666, 0.14285714285714285, 0.2222222222222222, 0.14285714285714285, 0.16666666666666666, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1], [0.19047619047619047, 0.16666666666666666, 0.26666666666666666, 0.16666666666666666, 0.19047619047619047, 0.16666666666666666, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.26666666666666666, 0.3333333333333333, 0.26666666666666666, 0.1, 0.19047619047619047, 0.16666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 1, 1, 1, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.1, 0.1, 0.26666666666666666, 0.3703703703703704, 0.3962962962962962, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.19047619047619047, 0.29629629629629634, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.3703703703703704, 0.3962962962962962, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.19047619047619047, 0.29629629629629634, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.16666666666666666, 0.14285714285714285, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.19047619047619047, 0.16666666666666666, 0.26666666666666666, 0.16666666666666666, 0.19047619047619047], [0.6666666666666666, 1, 1, 1, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.2222222222222222, 0.1, 0.26666666666666666, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 1, 1, 1, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.19047619047619047, 0.1, 0.26666666666666666, 0.3333333333333333, 0.26666666666666666, 0.1], [0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.16666666666666666, 0.14285714285714285, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3962962962962962, 0.5185185185185185, 0.5111111111111111, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.3068783068783069, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666], [0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.19047619047619047, 0.16666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3703703703703704, 0.4753086419753087, 0.5185185185185185, 0.674074074074074, 0.4444444444444444, 0.3333333333333333, 0.3068783068783069, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333], [0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.19047619047619047, 0.16666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5185185185185186, 0.4753086419753087, 0.5185185185185185, 0.3962962962962962, 0.26666666666666666, 0.16666666666666666, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444], [0.1, 0.26666666666666666, 0.3333333333333333, 0.26666666666666666, 0.1, 0.19047619047619047, 0.16666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.4444444444444444, 0.4753086419753087, 0.3703703703703704, 0.26666666666666666, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 1, 1, 1, 0.6666666666666666], [0.19047619047619047, 0.16666666666666666, 0.26666666666666666, 0.16666666666666666, 0.19047619047619047, 0.16666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 1, 1, 1, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.16666666666666666, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444], [0.16666666666666666, 0.14285714285714285, 0.2222222222222222, 0.14285714285714285, 0.16666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5, 1, 0.5, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.19047619047619047, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.5185185185185186, 0.4753086419753087, 0.3703703703703704], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.6666666666666666, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.19047619047619047, 0.1, 0.26666666666666666, 0.3868312757201646, 0.48902606310013724, 0.45267489711934156, 0.3962962962962962], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.4444444444444444, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1, 0.19047619047619047, 0.34074074074074073, 0.453909465020576, 0.6008230452674898, 0.577366255144033, 0.419753086419753], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.3333333333333333, 0.26666666666666666, 0.1, 0.1, 0.1, 0.1, 0.1, 0.34074074074074073, 0.43885949441504996, 0.5679012345679012, 0.782716049382716, 0.8148148148148148, 0.482363315696649], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.26666666666666666, 0.4259259259259259, 0.5679012345679012, 0.7777777777777777, 1, 1, 0.8148148148148148], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3333333333333333, 0.4888888888888889, 0.7037037037037036, 1, 1, 1, 0.7777777777777777]];
    # start = {x:0, y:25}
    # end = {x:29,y:4}

    # model = Model(terrain_map, N_TURNS, START, FINISH, WEIGHT_SEGMENT, WEIGHT_TURN)  # engine = RandomSearch(model)
    model = Model(terrain_map, N_TURNS, START, FINISH, WEIGHT_SEGMENT, WEIGHT_TURN)
    # engine = SimulatedAnnealing(model)
    engine = ParticleSwarm(model)
    fitness, solution = engine.solve(ITERATIONS)
    print_solution(fitness, solution, terrain_map)


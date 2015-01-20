from src.model import Model, Point
from src.random_search import RandomSearch
from src.simulated_annealing import SimulatedAnnealing
from pprint import pprint
import json
from random import randint

BASE_WEIGHT = 0.1
MAP_HEIGHT = 30
MAP_WIDTH = 30
START = Point(0, 20)
FINISH = Point(29, 4)

WEIGHT_SEGMENT = 2.0
WEIGHT_TURN = 10.0
N_TURNS = 5
ITERATIONS = 1000

N_HILLS = 10


def add_point_if_possible(terrain, width, height, mid_x, mid_y, x, y):
    if 0 <= x < width and 0 <= y < height:
        if x != mid_x or y != mid_y:
            if terrain[x][y] == BASE_WEIGHT:
                terrain[x][y] = 1 / (abs(mid_x - x) + abs(mid_y - y))
            else:
                terrain[x][y] = min(1, (terrain[x][y] + 1 / (abs(mid_x - x) + abs(mid_y - y)))/2)


def generate_hill_map(width, height, n_points, min_radius=5, max_radius=8):
    terrain = [[BASE_WEIGHT for _ in range(height)] for _ in range(width)]
    for _ in range(n_points):
        mid_x = randint(0, width - 1)
        mid_y = randint(0, height - 1)
        terrain[mid_x][mid_y] = 1
        max_radius = randint(min_radius, max_radius)
        for radius in range(1, max_radius):
            y = 0
            x = radius
            radiusError = 1 - x

            while radius >= y:

                add_point_if_possible(terrain, width, height, mid_x, mid_y, x + mid_x, y + mid_y)
                add_point_if_possible(terrain, width, height, mid_x, mid_y, y + mid_x, x + mid_y)
                add_point_if_possible(terrain, width, height, mid_x, mid_y, -x + mid_x, y + mid_y)
                add_point_if_possible(terrain, width, height, mid_x, mid_y, -y + mid_x, x + mid_y)
                add_point_if_possible(terrain, width, height, mid_x, mid_y, -x + mid_x, -y + mid_y)
                add_point_if_possible(terrain, width, height, mid_x, mid_y, -y + mid_x, -x + mid_y)
                add_point_if_possible(terrain, width, height, mid_x, mid_y, x + mid_x, -y + mid_y)
                add_point_if_possible(terrain, width, height, mid_x, mid_y, y + mid_x, -x + mid_y)

                y += 1
                if radiusError < 0:
                    radiusError += 2 * y + 1
                else:
                    x -= 1
                    radiusError += 2 * (y - x + 1)
        if max_radius >= 1:
            add_point_if_possible(terrain, width, height, mid_x, mid_y, mid_x+1, mid_y+1)
            add_point_if_possible(terrain, width, height, mid_x, mid_y, mid_x+1, mid_y-1)
            add_point_if_possible(terrain, width, height, mid_x, mid_y, mid_x-1, mid_y+1)
            add_point_if_possible(terrain, width, height, mid_x, mid_y, mid_x-1, mid_y-1)

    return terrain


if __name__ == '__main__':

    # terrain_map = [
    #     [0.1, 0.1, 0.1, 0.1, 0.1],
    #     [0.1, 1, 0.5, 0.1, 0.1],
    #     [0.3, 1, 1, 0.1, 1],
    #     [0.7, 1, 0.1, 0.1, 1],
    #     [0.7, 0.8, 0.1, 0.1, 0.1]
    # ]

    terrain_map = generate_hill_map(MAP_WIDTH, MAP_HEIGHT, N_HILLS)
    model = Model(terrain_map, N_TURNS, START, FINISH, WEIGHT_SEGMENT, WEIGHT_TURN)  # engine = RandomSearch(model)
    engine = SimulatedAnnealing(model)
    fitness, solution = engine.solve(ITERATIONS)
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


from src.model import Model, Point
from src.random_search import RandomSearch
from src.simulated_annealing import SimulatedAnnealing
import json


if __name__ == '__main__':

    terrain_map = [
        [0.1, 0.1, 0.1, 0.1, 0.1],
        [0.1, 1, 0.5,  0.1, 0.1],
        [0.3, 1, 1, 0.1, 1],
        [0.7, 1, 0.1, 0.1, 1],
        [0.7, 0.8, 0.1, 0.1, 0.1]
    ]
    n_turns = 5
    start = Point(3, 4)  # x, y
    finish = Point(0, 1)
    weight_segement = 1.0
    weight_turn = 15.0

    iterations = 1000
    model = Model(terrain_map, n_turns, start, finish, weight_segement, weight_turn)
    # engine = RandomSearch(model)
    engine = SimulatedAnnealing(model)
    solution = engine.solve(iterations)
    print("Fitness: {0}".format([solution[0]]))
    json_solution = json.dumps([{"x": p.x, "y": p.y} for p in solution[1]])
    json_map = json.dumps(terrain_map)
    with open("../web/map.js", "w+") as output_data:
        output_data.write("map = {0};\n".format(json_map))
        output_data.write("start = {{x:{0},y:{1}}};\n".format(start.x, start.y))
        output_data.write("end = {{x:{0},y:{1}}};\n".format(finish.x, finish.y))
        output_data.write("route = {0};\n".format(json_solution))

    # solution - lista punktow i jakosc rozwiazania


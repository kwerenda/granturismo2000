from src.model import Model, Point
from src.random_search import RandomSearch
from src.simulated_annealing import SimulatedAnnealing


if __name__ == '__main__':

    terrain_map = [
        [0.1, 0.1, 0.1, 0.1, 0.1],
        [0.1, 10, 10,  0.1, 0.1],
        [10, 10, 10, 0.1, 1],
        [10, 10, 0.1, 0.1, 1],
        [10, 10, 0.1, 0.1, 0.1]
    ]
    n_turns = 4
    start = Point(3, 4)  # x, y
    finish = Point(0, 1)
    weight_segement = 1.0
    weight_turn = 5.0

    iterations = 100
    model = Model(terrain_map, n_turns, start, finish, weight_segement, weight_turn)
    # engine = RandomSearch(model)
    engine = SimulatedAnnealing(model)
    solution = engine.solve(iterations)
    print("Fitness: {0}".format(solution[0]))
    for point in solution[1]:
        print("{{x:{0},y:{1}}}".format(point.x, point.y))

    # solution - lista punktow i jakosc rozwiazania


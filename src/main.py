from model import Model, Point
from random_search import RandomSearch


if __name__ == '__main__':

    terrain_map = [
        [0.1, 0.1, 0.1, 0.1, 0.1],
        [0.1, 1, 1,  0.1, 0.1],
        [1, 1, 1, 0.1, 1],
        [1, 1, 0.1, 0.1, 1],
        [1, 1, 0.1, 0.1, 0.1]
    ]
    n_turns = 8
    start = Point(3, 4)  # x, y
    finish = Point(0, 1)

    iterations = 100
    model = Model(terrain_map, n_turns, start, finish)
    engine = RandomSearch(model)
    solution = engine.solve(iterations)
    print(solution)

    # solution - lista punktow i jakosc rozwiazania


from model import Model
from random_search import RandomSearch


if __name__ == '__main__':
    print("Igus")

    terrain_map = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 0]
    ]
    n_turns = 8
    start = (3, 4)  # x, y
    finish = (0, 1)

    iterations = 100
    model = Model(terrain_map, n_turns, start, finish)
    engine = RandomSearch(model)
    solution = engine.solve(iterations)
    print(solution)

    # solution - lista punktow i jakosc rozwiazania


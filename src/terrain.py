from random import randint


def add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, x, y):
    if 0 <= x < width and 0 <= y < height:
        if x != mid_x or y != mid_y:
            if terrain[x][y] <= base_weight:
                terrain[x][y] = 1 / (abs(mid_x - x) + abs(mid_y - y))
            else:
                terrain[x][y] = min(1, (terrain[x][y] + 1 / (abs(mid_x - x) + abs(mid_y - y)))/1.5)


def generate_hill_terrain(width, height, base_weight, n_points, min_radius=5, max_radius=8):
    terrain = [[base_weight for _ in range(height)] for _ in range(width)]
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

                add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, x + mid_x, y + mid_y)
                add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, y + mid_x, x + mid_y)
                add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, -x + mid_x, y + mid_y)
                add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, -y + mid_x, x + mid_y)
                add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, -x + mid_x, -y + mid_y)
                add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, -y + mid_x, -x + mid_y)
                add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, x + mid_x, -y + mid_y)
                add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, y + mid_x, -x + mid_y)

                y += 1
                if radiusError < 0:
                    radiusError += 2 * y + 1
                else:
                    x -= 1
                    radiusError += 2 * (y - x + 1)
        if max_radius >= 1:
            add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, mid_x+1, mid_y+1)
            add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, mid_x+1, mid_y-1)
            add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, mid_x-1, mid_y+1)
            add_point_to_circle_if_possible(terrain, base_weight, width, height, mid_x, mid_y, mid_x-1, mid_y-1)

    return terrain
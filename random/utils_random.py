def get_neighbors(pos, size):
    x, y = pos
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # Lef, Right, Down, Up
    return [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < size and 0 <= y + dy < size]

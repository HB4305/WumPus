import heapq
from .utils import get_neighbors

# Bảo thêm dô
def heuristic(pos, goal=(0, 0)):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])  # khoảng cách Manhattan

def a_star(start, goal, is_safe, size):
    open_set = [(heuristic(start, goal), 0, start, [])]
    visited = set()

    while open_set:
        est_total, cost, current, path = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path + [current]

        for neighbor in get_neighbors(current, size):
            if neighbor not in visited and is_safe(neighbor):
                new_cost = cost + 1
                new_path = path + [current]
                est = new_cost + heuristic(neighbor, goal)
                heapq.heappush(open_set, (est, new_cost, neighbor, new_path))

    return []

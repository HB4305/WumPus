import heapq
from .utils import get_neighbors

def a_star(start, goal, heuristic, is_safe, size):
    open_set = [(heuristic(start), 0, start, [])]
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
                est = new_cost + heuristic(neighbor)
                heapq.heappush(open_set, (est, new_cost, neighbor, new_path))
    return []


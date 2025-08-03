# import heapq
# from .utils import get_neighbors

# def a_star(start, goal, heuristic, is_safe, size):
#     open_set = [(heuristic(start), 0, start, [])]
#     visited = set()

#     while open_set:
#         est_total, cost, current, path = heapq.heappop(open_set)
#         if current in visited:
#             continue
#         visited.add(current)

#         if current == goal:
#             return path + [current]

#         for neighbor in get_neighbors(current, size):
#             if neighbor not in visited and is_safe(neighbor):
#                 new_cost = cost + 1
#                 new_path = path + [current]
#                 est = new_cost + heuristic(neighbor)
#                 heapq.heappush(open_set, (est, new_cost, neighbor, new_path))
#     return []
import heapq
from .utils import get_neighbors

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_search(start, goal, is_safe_func, size):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for neighbor in get_neighbors(current, size):
            if not is_safe_func(neighbor):
                continue
            new_cost = cost_so_far[current] + 1  # Giả sử chi phí là 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(goal, neighbor)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    # reconstruct path
    if goal not in came_from:
        return None  # không tìm được đường đi
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
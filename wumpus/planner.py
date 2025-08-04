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
    if start == goal:
        return []
        
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
                
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(goal, neighbor)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    # Reconstruct path
    if goal not in came_from:
        return []
        
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def safe_path_to_unexplored(start, inference, size):
    """Find safe path to nearest unexplored safe cell"""
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    visited = set()

    while frontier:
        _, current = heapq.heappop(frontier)
        
        if current in visited:
            continue
        visited.add(current)

        # Check if current is unexplored and safe
        kb_info = inference.kb.get(current, {})
        if (not kb_info.get('visited', False) and 
            inference.is_definitely_safe(current)):
            # Reconstruct path
            path = []
            pos = current
            while pos != start:
                path.append(pos)
                pos = came_from[pos]
            path.reverse()
            return path

        for neighbor in get_neighbors(current, size):
            if neighbor in visited:
                continue
                
            if inference.is_definitely_safe(neighbor):
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    # Prioritize unexplored cells
                    kb_info = inference.kb.get(neighbor, {})
                    priority = new_cost
                    if not kb_info.get('visited', False):
                        priority -= 10  # Bonus for unexplored
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

    return []
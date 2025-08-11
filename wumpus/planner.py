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

def dfs_search(start, goal, passable, size, randomize=False):
    # normalize goal to callable
    if callable(goal):
        is_goal = goal
    else:
        target = tuple(goal)
        is_goal = lambda n: n == target

    stack = [(start, [start])]
    visited = set([start])

    while stack:
        node, path = stack.pop()
        if is_goal(node):
            return path  # found (start..node)

        neighs = [n for n in get_neighbors(node, size) if 0 <= n[0] < size and 0 <= n[1] < size and passable(n)]
        if randomize:
            random.shuffle(neighs)
        # push neighbors onto stack; to preserve 'natural' DFS order push in reverse
        for n in reversed(neighs):
            if n not in visited:
                visited.add(n)
                stack.append((n, path + [n]))

    return []
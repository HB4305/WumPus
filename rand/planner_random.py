import heapq
import random
from .utils_random import get_neighbors


def dfs_search(start, goal, is_safe_fn, size, visited_global=None, verbose=False):
    """
    DFS search tránh loop:
    - visited_local: mỗi lần gọi
    - visited_global: các ô đã đi qua toàn game
    """
    def in_bounds(pos):
        x, y = pos
        return 0 <= x < size and 0 <= y < size

    start = tuple(start)
    is_goal_callable = callable(goal)
    target = tuple(goal) if (not is_goal_callable and goal is not None) else None

    if (not is_goal_callable) and target == start:
        return []

    visited_local = set([start])
    if visited_global:
        visited_local.update(visited_global)

    parent = {}
    stack = [start]
    visited_order = []

    while stack:
        node = stack.pop()

        # --- Goal check ---
        if is_goal_callable:
            try:
                if goal(node):
                    return _reconstruct_path(parent, start, node)
            except Exception:
                pass
        else:
            if node == target:
                return _reconstruct_path(parent, start, node)

        if node != start and (not visited_global or node not in visited_global):
            visited_order.append(node)

        # --- Neighbors ---
        x, y = node
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

        for nbr in neighbors:
            if not in_bounds(nbr):
                continue
            if nbr in visited_local:
                continue
            try:
                if not is_safe_fn(nbr):
                    continue
            except Exception:
                continue
            visited_local.add(nbr)
            parent[nbr] = node
            stack.append(nbr)

    return visited_order if is_goal_callable else []


def _reconstruct_path(parent, start, node):
    path = []
    cur = node
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

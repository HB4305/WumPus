import heapq
import random
from .utils_random import get_neighbors

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
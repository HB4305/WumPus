import heapq
import random
from .utils_random import get_neighbors


def dfs_search(start, goal, is_safe_fn, size, verbose=False):
    """
    DFS search có 2 chế độ:
    - Nếu `goal` là tuple (gx, gy): tìm đường từ start tới goal và trả về list các ô (exclude start),
      ví dụ [(nx1,ny1), (nx2,ny2), ..., (gx,gy)]. Nếu goal không reachable => trả về [].
    - Nếu `goal` là callable: gọi goal(node) để kiểm tra. Nếu goal bao giờ cũng False (ví dụ lambda n: False),
      hàm sẽ duyệt toàn bộ vùng có thể tới được (theo DFS) và trả về danh sách các node đã thăm (exclude start),
      theo thứ tự duyệt.
    - is_safe_fn(pos) -> bool: kiểm tra ô có an toàn để bước tới (dùng inference.is_safe).
    - size: kích thước board (n x n). Pos dạng (x,y) với 0 <= x,y < size.
    """
    from collections import deque

    # helper
    def in_bounds(pos):
        x, y = pos
        return 0 <= x < size and 0 <= y < size

    start = tuple(start)

    is_goal_callable = callable(goal)
    target = tuple(goal) if (not is_goal_callable and goal is not None) else None

    # Quick: nếu start là goal coordinate
    if (not is_goal_callable) and target == start:
        return []

    visited = set([start])
    parent = {}  # parent[pos] = previous_pos, để reconstruct path khi tìm thấy goal

    # classic DFS stack: store node
    stack = [start]

    # visited_order for the "explore-all" mode (callable goal that never true)
    visited_order = []

    while stack:
        node = stack.pop()
        # check goal
        if is_goal_callable:
            try:
                if goal(node):  # goal satisfied
                    # reconstruct path from start -> node (exclude start)
                    path = []
                    cur = node
                    while cur != start:
                        path.append(cur)
                        cur = parent[cur]
                    path.reverse()
                    return path
            except Exception:
                # defensive: if user's callable errors, ignore and continue
                pass
        else:
            if node == target:
                # reconstruct path
                path = []
                cur = node
                while cur != start:
                    path.append(cur)
                    cur = parent[cur]
                path.reverse()
                return path

        # record visited order for explore-all mode (exclude start)
        if node != start:
            visited_order.append(node)

        # neighbors: EAST, WEST, NORTH, SOUTH — order can affect DFS shape
        x, y = node
        neighbors = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

        # push neighbors (we push only safe & unvisited)
        for nbr in neighbors:
            if not in_bounds(nbr):
                continue
            if nbr in visited:
                continue
            # check safe (use provided is_safe_fn). If is_safe_fn expects visited info, it's up to it.
            try:
                safe = is_safe_fn(nbr)
            except Exception:
                safe = False
            if not safe:
                continue
            visited.add(nbr)
            parent[nbr] = node
            stack.append(nbr)

    # nếu đến đây: không tìm thấy goal coordinate, hoặc callable không bao giờ trả True
    if is_goal_callable:
        # trả về danh sách các ô đã thăm (exclude start) để dùng cho heuristics như bạn đang làm
        return visited_order
    else:
        return []

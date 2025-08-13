import heapq
import random
from .utils_random import get_neighbors


def dfs_search(start, goal, is_safe_fn, size, visited_global=None, verbose=False):
    """
    DFS search tránh loop.
    - Nếu caller truyền visited_global là set -> sẽ cập nhật IN-PLACE.
    - Nếu is_safe_fn(nbr) ném exception thì vẫn mark nbr là đã thử để tránh thử lại vô hạn.
    Trả về:
    - Nếu goal là vị trí: path (list) nếu tìm thấy, else [].
    - Nếu goal là callable: path nếu tìm thấy, else visited_order (danh sách ô đã duyệt trong lần gọi này).
    """
    def in_bounds(pos):
        x, y = pos
        return 0 <= x < size and 0 <= y < size

    start = tuple(start)
    is_goal_callable = callable(goal)
    target = tuple(goal) if (not is_goal_callable and goal is not None) else None

    # chuẩn hóa và phát hiện có thể cập nhật in-place không
    visited_global_inplace = None
    if visited_global is None:
        visited_global_set = set()
    elif isinstance(visited_global, set):
        visited_global_set = visited_global
        visited_global_inplace = visited_global  # pointer để cập nhật in-place
    else:
        visited_global_set = set(visited_global)

    # quick goal check at start
    if is_goal_callable:
        try:
            if goal(start):
                if visited_global_inplace is not None:
                    visited_global_inplace.add(start)
                return []
        except Exception:
            pass
    else:
        if target == start:
            if visited_global_inplace is not None:
                visited_global_inplace.add(start)
            return []

    visited_local = set([start])
    if visited_global_set:
        visited_local.update(visited_global_set)

    parent = {}
    stack = [start]
    visited_order = []

    while stack:
        node = stack.pop()

        # --- Goal check ---
        if is_goal_callable:
            try:
                if goal(node):
                    path = _reconstruct_path(parent, start, node)
                    # mark path as visited in global if possible
                    if visited_global_inplace is not None:
                        for p in path:
                            visited_global_inplace.add(p)
                        visited_global_inplace.add(start)
                    return path
            except Exception:
                pass
        else:
            if node == target:
                path = _reconstruct_path(parent, start, node)
                if visited_global_inplace is not None:
                    for p in path:
                        visited_global_inplace.add(p)
                    visited_global_inplace.add(start)
                return path

        # record visited order for callable-goal case
        if node != start and (not visited_global_set or node not in visited_global_set):
            visited_order.append(node)

        # --- Neighbors ---
        x, y = node
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

        for nbr in neighbors:
            if not in_bounds(nbr):
                continue
            if nbr in visited_local:
                continue
            # gọi is_safe_fn an toàn; nếu lỗi, đánh dấu đã thử (để tránh thử lại)
            try:
                safe = is_safe_fn(nbr)
            except Exception:
                # đánh dấu đã thử để tránh infinite retry
                visited_local.add(nbr)
                if visited_global_inplace is not None:
                    visited_global_inplace.add(nbr)
                continue

            if not safe:
                # không an toàn -> mark đã thử và bỏ qua
                visited_local.add(nbr)
                if visited_global_inplace is not None:
                    visited_global_inplace.add(nbr)
                continue

            # safe -> add parent + push stack + mark visited local (chưa mark global ngay,
            # sẽ mark global khi pop / hoặc khi trả path, nhưng cũng có thể mark để tránh nhiều tìm)
            parent[nbr] = node
            visited_local.add(nbr)
            # Nếu muốn, có thể thêm vào visited_global_inplace ngay khi khám phá:
            if visited_global_inplace is not None:
                visited_global_inplace.add(nbr)
            stack.append(nbr)

    # Nếu không tìm được goal, cập nhật visited_global (nếu in-place)
    if visited_global_inplace is not None:
        visited_global_inplace.update(visited_local)

    return visited_order if is_goal_callable else []

def _reconstruct_path(parent, start, node):
    """Trả về path từ start -> node (không bao gồm start)."""
    path = []
    cur = node
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path
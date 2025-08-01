# from .utils import get_neighbors

# class InferenceEngine:
#     def __init__(self, size):
#         self.size = size
#         self.safe = set()
#         self.unsafe = set()
#         self.unknown = set((i, j) for i in range(size) for j in range(size))
#         self.percepts = dict()

#     def get_possible_wumpus(self):
#         # Trả về danh sách ô có khả năng chứa Wumpus
#         return list(self.possible_wumpus_cells)

#     def is_wumpus_certain(self, pos):
#         # Trả về True nếu inference chắc chắn Wumpus ở ô này
#         return pos in self.confirmed_wumpus_cells

#     def update_knowledge(self, position, percept):
#         self.percepts[position] = percept
#         if not percept["breeze"] and not percept["stench"]:
#             for n in get_neighbors(position, self.size):
#                 self.safe.add(n)
#                 self.unknown.discard(n)
#         else:
#             self.unknown.add(position)

#     def is_safe(self, pos):
#         return pos in self.safe
from .utils import get_neighbors

class InferenceEngine:
    def __init__(self, size):
        self.size = size
        self.safe = set()
        self.unsafe = set()
        self.unknown = set((i, j) for i in range(size) for j in range(size))
        self.percepts = dict()

        # ✅ Thêm 2 thuộc tính này để tránh lỗi AttributeError
        self.possible_wumpus_cells = set()
        self.confirmed_wumpus_cells = set()
        # ✅ Đánh dấu (0, 0) là safe ngay từ đầu
        self.safe.add((0, 0))
        self.visited = set()
        self.safe_cells = set()

    def update_knowledge(self, position, percept):
        self.percepts[position] = percept
        self.visited.add(position)
        self.safe_cells.add(position)  # ✅ phải có dòng này!

        if not percept["breeze"] and not percept["stench"]:
            for n in get_neighbors(position, self.size):
                self.safe.add(n)
                self.unknown.discard(n)
        else:
            self.unknown.add(position)

        # ✅ Cập nhật các ô nghi ngờ Wumpus nếu có stench
        if percept["stench"]:
            neighbors = get_neighbors(position, self.size)
            for n in neighbors:
                if n not in self.safe:
                    self.possible_wumpus_cells.add(n)

        # ✅ Suy luận đơn giản: nếu chỉ còn đúng 1 ô nghi Wumpus và nó nằm trong tất cả stench, ta xác nhận nó
        self.infer_wumpus_certainty()

    def infer_wumpus_certainty(self):
        stench_positions = [pos for pos, p in self.percepts.items() if p["stench"]]
        if not stench_positions:
            return

        # Giao nhau các ô lân cận của tất cả vị trí có stench
        possible = set(get_neighbors(stench_positions[0], self.size))
        for pos in stench_positions[1:]:
            possible &= set(get_neighbors(pos, self.size))

        # Loại trừ các ô đã xác định an toàn
        possible -= self.safe

        if len(possible) == 1:
            self.confirmed_wumpus_cells = possible

    def get_possible_wumpus(self):
        return list(self.possible_wumpus_cells)

    def is_wumpus_certain(self, pos):
        return pos in self.confirmed_wumpus_cells

    def is_safe(self, pos):
        return pos in self.safe

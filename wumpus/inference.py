# from .utils import get_neighbors

# class InferenceEngine:
#     def __init__(self, size):
#         self.size = size
#         self.safe = set()
#         self.unsafe = set()
#         self.unknown = set((i, j) for i in range(size) for j in range(size))
#         self.percepts = dict()

#         # ✅ Thêm 2 thuộc tính này để tránh lỗi AttributeError
#         self.possible_wumpus_cells = set()
#         self.confirmed_wumpus_cells = set()
#         # ✅ Đánh dấu (0, 0) là safe ngay từ đầu
#         self.safe.add((0, 0))
#         self.visited = set()
#         self.safe_cells = set()

#     def update_knowledge(self, position, percept):
#         self.percepts[position] = percept
#         self.visited.add(position)
#         self.safe_cells.add(position)  # ✅ phải có dòng này!

#         if not percept["breeze"] and not percept["stench"]:
#             for n in get_neighbors(position, self.size):
#                 self.safe.add(n)
#                 self.unknown.discard(n)
#         else:
#             self.unknown.add(position)

#         # ✅ Cập nhật các ô nghi ngờ Wumpus nếu có stench
#         if percept["stench"]:
#             neighbors = get_neighbors(position, self.size)
#             for n in neighbors:
#                 if n not in self.safe:
#                     self.possible_wumpus_cells.add(n)


#         # ✅ Suy luận đơn giản: nếu chỉ còn đúng 1 ô nghi Wumpus và nó nằm trong tất cả stench, ta xác nhận nó
#         self.infer_wumpus_certainty()

#     def infer_wumpus_certainty(self):
#         stench_positions = [pos for pos, p in self.percepts.items() if p["stench"]]
#         if not stench_positions:
#             return

#         # Giao nhau các ô lân cận của tất cả vị trí có stench
#         possible = set(get_neighbors(stench_positions[0], self.size))
#         for pos in stench_positions[1:]:
#             possible &= set(get_neighbors(pos, self.size))

#         # Loại trừ các ô đã xác định an toàn
#         possible -= self.safe

#         if len(possible) == 1:
#             self.confirmed_wumpus_cells = possible

#     def get_possible_wumpus(self):
#         return list(self.possible_wumpus_cells)

#     def is_wumpus_certain(self, pos):
#         return pos in self.confirmed_wumpus_cells

#     def is_safe(self, pos):
#         return pos in self.safe
from .utils import get_neighbors
from collections import defaultdict

class InferenceEngine:
    def __init__(self, size):
        self.size = size
        self.visited = set()
        self.safe = set([(0, 0)])
        self.unknown = set((i, j) for i in range(size) for j in range(size))
        self.knowledge = defaultdict(lambda: {
            "possible_pit": False,
            "possible_wumpus": False,
            "confirmed_pit": False,
            "confirmed_wumpus": False,
            "safe": False
        })
        self.percepts = {}

    def update_knowledge(self, pos, percept):
        self.percepts[pos] = percept
        self.visited.add(pos)
        self.safe.add(pos)
        self.unknown.discard(pos)
        self.knowledge[pos]["safe"] = True

        neighbors = get_neighbors(pos, self.size)

        # Nếu không có breeze hoặc stench → tất cả neighbors an toàn
        if not percept["breeze"] and not percept["stench"]:
            for n in neighbors:
                self.safe.add(n)
                self.knowledge[n]["safe"] = True
                self.knowledge[n]["possible_pit"] = False
                self.knowledge[n]["possible_wumpus"] = False
                self.unknown.discard(n)

        # Nếu có breeze → đánh dấu neighbors là "có thể có pit"
        if percept["breeze"]:
            for n in neighbors:
                if n not in self.safe and n not in self.visited:
                    self.knowledge[n]["possible_pit"] = True

        # Nếu có stench → đánh dấu neighbors là "có thể có wumpus"
        if percept["stench"]:
            for n in neighbors:
                if n not in self.safe and n not in self.visited:
                    self.knowledge[n]["possible_wumpus"] = True

        # Nếu đã đến ô không có stench nhưng trước đó nghi ngờ Wumpus ở neighbor → loại bỏ
        if not percept["stench"]:
            for n in neighbors:
                self.knowledge[n]["possible_wumpus"] = False

        if not percept["breeze"]:
            for n in neighbors:
                self.knowledge[n]["possible_pit"] = False

        # Sau đó cố gắng infer chắc chắn pit/wumpus từ giao nhau
        self.infer_certain_threats()

    def infer_certain_threats(self):
        # Tìm tất cả vị trí có stench
        stench_positions = [pos for pos, p in self.percepts.items() if p["stench"]]
        if stench_positions:
            common_wumpus = set(get_neighbors(stench_positions[0], self.size))
            for pos in stench_positions[1:]:
                common_wumpus &= set(get_neighbors(pos, self.size))

            # Loại bỏ các ô đã an toàn
            common_wumpus = {pos for pos in common_wumpus if not self.knowledge[pos]["safe"]}
            if len(common_wumpus) == 1:
                pos = list(common_wumpus)[0]
                self.knowledge[pos]["confirmed_wumpus"] = True

        # Tương tự cho pit
        breeze_positions = [pos for pos, p in self.percepts.items() if p["breeze"]]
        if breeze_positions:
            common_pit = set(get_neighbors(breeze_positions[0], self.size))
            for pos in breeze_positions[1:]:
                common_pit &= set(get_neighbors(pos, self.size))

            common_pit = {pos for pos in common_pit if not self.knowledge[pos]["safe"]}
            if len(common_pit) == 1:
                pos = list(common_pit)[0]
                self.knowledge[pos]["confirmed_pit"] = True

    def is_safe(self, pos):
        return self.knowledge[pos]["safe"] and not self.knowledge[pos]["confirmed_pit"] and not self.knowledge[pos]["confirmed_wumpus"]

    def is_possible_pit(self, pos):
        return self.knowledge[pos]["possible_pit"]

    def is_possible_wumpus(self, pos):
        return self.knowledge[pos]["possible_wumpus"]

    def is_confirmed_pit(self, pos):
        return self.knowledge[pos]["confirmed_pit"]

    def is_confirmed_wumpus(self, pos):
        return self.knowledge[pos]["confirmed_wumpus"]

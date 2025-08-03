# from .utils import get_neighbors
# from collections import defaultdict

# class InferenceEngine:
#     def __init__(self, size):
#         self.size = size
#         self.visited = set()
#         self.safe = set([(0, 0)])
#         self.unknown = set((i, j) for i in range(size) for j in range(size))
#         self.knowledge = defaultdict(lambda: {
#             "possible_pit": False,
#             "possible_wumpus": False,
#             "confirmed_pit": False,
#             "confirmed_wumpus": False,
#             "safe": False
#         })
#         self.percepts = {}

#     def update_knowledge(self, pos, percept):
#         self.percepts[pos] = percept
#         self.visited.add(pos)
#         self.safe.add(pos)
#         self.unknown.discard(pos)
#         self.knowledge[pos]["safe"] = True

#         neighbors = get_neighbors(pos, self.size)

#         # Nếu không có breeze hoặc stench → tất cả neighbors an toàn
#         if not percept["breeze"] and not percept["stench"]:
#             for n in neighbors:
#                 self.safe.add(n)
#                 self.knowledge[n]["safe"] = True
#                 self.knowledge[n]["possible_pit"] = False
#                 self.knowledge[n]["possible_wumpus"] = False
#                 self.unknown.discard(n)

#         # Nếu có breeze → đánh dấu neighbors là "có thể có pit"
#         if percept["breeze"]:
#             for n in neighbors:
#                 if n not in self.safe and n not in self.visited:
#                     self.knowledge[n]["possible_pit"] = True

#         # Nếu có stench → đánh dấu neighbors là "có thể có wumpus"
#         if percept["stench"]:
#             for n in neighbors:
#                 if n not in self.safe and n not in self.visited:
#                     self.knowledge[n]["possible_wumpus"] = True

#         # Nếu đã đến ô không có stench nhưng trước đó nghi ngờ Wumpus ở neighbor → loại bỏ
#         if not percept["stench"]:
#             for n in neighbors:
#                 self.knowledge[n]["possible_wumpus"] = False

#         if not percept["breeze"]:
#             for n in neighbors:
#                 self.knowledge[n]["possible_pit"] = False

#         # Sau đó cố gắng infer chắc chắn pit/wumpus từ giao nhau
#         self.infer_certain_threats()

#     def infer_certain_threats(self):
#         # Tìm tất cả vị trí có stench
#         stench_positions = [pos for pos, p in self.percepts.items() if p["stench"]]
#         if stench_positions:
#             common_wumpus = set(get_neighbors(stench_positions[0], self.size))
#             for pos in stench_positions[1:]:
#                 common_wumpus &= set(get_neighbors(pos, self.size))

#             # Loại bỏ các ô đã an toàn
#             common_wumpus = {pos for pos in common_wumpus if not self.knowledge[pos]["safe"]}
#             if len(common_wumpus) == 1:
#                 pos = list(common_wumpus)[0]
#                 self.knowledge[pos]["confirmed_wumpus"] = True

#         # Tương tự cho pit
#         breeze_positions = [pos for pos, p in self.percepts.items() if p["breeze"]]
#         if breeze_positions:
#             common_pit = set(get_neighbors(breeze_positions[0], self.size))
#             for pos in breeze_positions[1:]:
#                 common_pit &= set(get_neighbors(pos, self.size))

#             common_pit = {pos for pos in common_pit if not self.knowledge[pos]["safe"]}
#             if len(common_pit) == 1:
#                 pos = list(common_pit)[0]
#                 self.knowledge[pos]["confirmed_pit"] = True

#     def is_safe(self, pos):
#         return self.knowledge[pos]["safe"] and not self.knowledge[pos]["confirmed_pit"] and not self.knowledge[pos]["confirmed_wumpus"]

#     def is_possible_pit(self, pos):
#         return self.knowledge[pos]["possible_pit"]

#     def is_possible_wumpus(self, pos):
#         return self.knowledge[pos]["possible_wumpus"]

#     def is_confirmed_pit(self, pos):
#         return self.knowledge[pos]["confirmed_pit"]

#     def is_confirmed_wumpus(self, pos):
#         return self.knowledge[pos]["confirmed_wumpus"]
from collections import defaultdict
from .utils import get_neighbors

class Inference:
    def __init__(self, size):
        self.size = size
        self.kb = {}  # {(x, y): {'visited': bool, 'safe': bool, 'possible_pit': bool, 'possible_wumpus': bool}}
        self.percepts = {}  # {(x, y): {'stench': bool, 'breeze': bool, 'glitter': bool}}

    def update_knowledge(self, position, percept):
        x, y = position
        self.kb.setdefault((x, y), {
            'visited': True, 'safe': True,
            'possible_pit': False, 'possible_wumpus': False
        })
        self.kb[(x, y)]['visited'] = True
        self.kb[(x, y)]['safe'] = True  # đã đi được tới thì nó an toàn

        # lưu percept
        self.percepts[(x, y)] = percept

        # lấy hàng xóm
        neighbors = get_neighbors((x, y), self.size)

        # nếu không có breeze, các ô xung quanh không có pit
        if not percept['breeze']:
            for nx, ny in neighbors: # bỏ nghi ngờ mấy ô xung quanh là pit
                self._ensure_kb((nx, ny))
                self.kb[(nx, ny)]['possible_pit'] = False

        # nếu không có stench, các ô xung quanh không có wumpus
        if not percept['stench']:
            for nx, ny in neighbors: # bỏ nghi ngờ mấy ô xung quanh là wumbus
                self._ensure_kb((nx, ny))
                self.kb[(nx, ny)]['possible_wumpus'] = False
                # Nếu không có cả stench lẫn breeze thì safe
                if not self.kb[(nx, ny)]['possible_pit']:
                    self.kb[(nx, ny)]['safe'] = True

        # nếu có breeze hoặc stench, không khẳng định chắc chắn được nên đánh dấu là có thể nguy hiểm
        if percept['breeze']:
            for nx, ny in neighbors:
                self._ensure_kb((nx, ny))
                if not self.kb[(nx, ny)]['visited'] and self.kb[(nx, ny)]['possible_pit'] is False:
                    # Kiểm tra mâu thuẫn với ô khác xung quanh ô nghi ngờ liệu không có breeze
                    if all(self.percepts.get((ox, oy), {}).get('breeze', True)
                        for (ox, oy) in get_neighbors((nx, ny), self.size)):
                        self.kb[(nx, ny)]['possible_pit'] = True


        if percept['stench']:
            for nx, ny in neighbors:
                self._ensure_kb((nx, ny))
                if not self.kb[(nx, ny)]['visited'] and self.kb[(nx, ny)]['possible_wumpus'] is False:
                    # Chỉ đánh dấu là Wumpus nếu không mâu thuẫn với ô hàng xóm
                    if all(self.percepts.get((ox, oy), {}).get('stench', True)
                        for (ox, oy) in get_neighbors((nx, ny), self.size)):
                        self.kb[(nx, ny)]['possible_wumpus'] = True

    def _ensure_kb(self, pos): # đảm bảo ô (x, y) đã có trong knowledge base
        if pos not in self.kb:
            self.kb[pos] = {
                'visited': False,
                'safe': False,
                'possible_pit': False,
                'possible_wumpus': False
            }

    def is_safe(self, pos):
        self._ensure_kb(pos)
        return self.kb[pos]['safe'] and not self.kb[pos]['possible_pit'] and not self.kb[pos]['possible_wumpus']

    def get_safe_unvisited_neighbors(self, current_pos): # tìm ô an toàn chưa đi
        neighbors = get_neighbors(current_pos, self.size)
        return [pos for pos in neighbors if self.is_safe(pos) and not self.kb[pos]['visited']]

    def get_kb(self):
        return self.kb

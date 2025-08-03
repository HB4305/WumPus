# from collections import defaultdict
# from .utils import get_neighbors

# class Inference:
#     def __init__(self, size):
#         self.size = size
#         self.kb = {}  # {(x, y): {'visited': bool, 'safe': bool, 'possible_pit': bool, 'possible_wumpus': bool}}
#         self.percepts = {}  # {(x, y): {'stench': bool, 'breeze': bool, 'glitter': bool}}

#     def update_knowledge(self, position, percept):
#         x, y = position
#         self.kb.setdefault((x, y), {
#             'visited': True, 'safe': True,
#             'possible_pit': False, 'possible_wumpus': False
#         })
#         self.kb[(x, y)]['visited'] = True
#         self.kb[(x, y)]['safe'] = True  # đã đi được tới thì nó an toàn

#         # lưu percept
#         self.percepts[(x, y)] = percept

#         # lấy hàng xóm
#         neighbors = get_neighbors((x, y), self.size)

#         # nếu không có breeze, các ô xung quanh không có pit
#         if not percept['breeze']:
#             for nx, ny in neighbors: # bỏ nghi ngờ mấy ô xung quanh là pit
#                 self._ensure_kb((nx, ny))
#                 self.kb[(nx, ny)]['possible_pit'] = False

#         # nếu không có stench, các ô xung quanh không có wumpus
#         if not percept['stench']:
#             for nx, ny in neighbors: # bỏ nghi ngờ mấy ô xung quanh là wumbus
#                 self._ensure_kb((nx, ny))
#                 self.kb[(nx, ny)]['possible_wumpus'] = False

#         # nếu có breeze hoặc stench, không khẳng định chắc chắn được nên đánh dấu là có thể nguy hiểm
#         if percept['breeze']:
#             for nx, ny in neighbors:
#                 self._ensure_kb((nx, ny))
#                 if not self.kb[(nx, ny)]['visited'] and self.kb[(nx, ny)]['possible_pit'] is False:
#                     # Kiểm tra mâu thuẫn với ô khác xung quanh ô nghi ngờ liệu không có breeze
#                     if all(self.percepts.get((ox, oy), {}).get('breeze', True)
#                         for (ox, oy) in get_neighbors((nx, ny), self.size)):
#                         self.kb[(nx, ny)]['possible_pit'] = True


#         if percept['stench']:
#             for nx, ny in neighbors:
#                 self._ensure_kb((nx, ny))
#                 if not self.kb[(nx, ny)]['visited'] and self.kb[(nx, ny)]['possible_wumpus'] is False:
#                     # Chỉ đánh dấu là Wumpus nếu không mâu thuẫn với ô hàng xóm
#                     if all(self.percepts.get((ox, oy), {}).get('stench', True)
#                         for (ox, oy) in get_neighbors((nx, ny), self.size)):
#                         self.kb[(nx, ny)]['possible_wumpus'] = True

#         # Đánh dấu safe rõ ràng: không pit, không wumpus ⇒ safe
#         for (pos, facts) in self.kb.items():
#             if not facts['possible_pit'] and not facts['possible_wumpus']:
#                 self.kb[pos]['safe'] = True

#     def _ensure_kb(self, pos): # đảm bảo ô (x, y) đã có trong knowledge base
#         if pos not in self.kb:
#             self.kb[pos] = {
#                 'visited': False,
#                 'safe': False,
#                 'possible_pit': False,
#                 'possible_wumpus': False
#             }

#     def is_safe(self, pos):
#         self._ensure_kb(pos)
#         return self.kb[pos]['safe'] and not self.kb[pos]['possible_pit'] and not self.kb[pos]['possible_wumpus']

#     def get_safe_unvisited_neighbors(self, current_pos): # tìm ô an toàn chưa đi
#         neighbors = get_neighbors(current_pos, self.size)
#         return [pos for pos in neighbors if self.is_safe(pos) and not self.kb[pos]['visited']]

#     def get_kb(self):
#         return self.kb
from .planner import astar_search
from .utils import get_neighbors

class Agent:
    def __init__(self, env, inference_engine):
        self.env = env
        self.inference = inference_engine
        self.x, self.y = 0, 0
        self.orientation = "EAST"
        self.has_gold = False
        self.has_arrow = True
        self.path = [(0, 0)]
        self.action_log = []
        self.escaped = False

    def step(self):
        if self.escaped:
            return "Already escaped."

        percepts = self.env.get_percepts(self.x, self.y)
        self.inference.update_knowledge((self.x, self.y), percepts)

        # Nếu có gold => grab
        if percepts["glitter"] and not self.has_gold:
            self.has_gold = True
            result = self.env.grab_gold()
            self.action_log.append("GRAB")
            return "Grabbed gold."

        # Nếu có gold và đang ở (0,0) => climb ra
        if self.has_gold and (self.x, self.y) == (0, 0):
            result = self.env.climb_out()
            self.escaped = result["escaped"]
            self.action_log.append("CLIMB")
            return "Climbed out with gold!" if self.escaped else "Climb failed."

        # Nếu có gold, lên kế hoạch quay về (0,0)
        if self.has_gold:
            path_home = astar_search((self.x, self.y), (0, 0), self.inference.is_safe, self.env.size)
            if path_home:
                next_move = path_home[0]
                self.move_to(next_move)
                return f"Move home to {next_move}"
            else:
                return "No path home!"

        # Nếu chưa có gold, tìm ô an toàn để đi tới
        targets = self.inference.get_safe_unvisited_neighbors((self.x, self.y))
        if targets:
            target = targets[0]
            path = astar_search((self.x, self.y), target, self.inference.is_safe, self.env.size)
            if path:
                next_move = path[0]
                self.move_to(next_move)
                return f"Move to safe cell {next_move}"

        # Nếu không còn ô an toàn để đi và chưa có gold
        return "Stuck. No safe moves."

    def move_to(self, next_pos):
        self.x, self.y = next_pos
        self.path.append(next_pos)
        self.env.move_agent(self.x, self.y)
        self.action_log.append(f"MOVE to {next_pos}")

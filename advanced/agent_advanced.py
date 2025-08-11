# from wumpus.planner import astar_search
# from wumpus.algorithm import heuristic
# from wumpus.utils import get_neighbors

# class AgentAdvanced:
#     def __init__(self, env, inference):
#         self.env = env
#         self.inference = inference
#         self.x, self.y = 0, 0
#         self.direction = "EAST"
#         self.has_gold = False
#         self.has_arrow = True
#         self.point = 0
#         self.path = [(0, 0)]
#         self.action_log = []
#         self.escaped = False
#         self.dead = False
#         self.action_counter = 0  # Đếm tổng số hành động agent đã làm

#     def _increment_action(self):
#         self.action_counter += 1
#         # Mỗi 5 hành động, gọi inference xử lý di chuyển Wumpus
#         if self.action_counter % 5 == 0:
#             try:
#                 self.inference.update_wumpus_positions_after_move((self.x, self.y))
#             except Exception as e:
#                 # Nếu agent bị Wumpus ăn chết
#                 print(f"[AGENT_ADVANCED] {str(e)}")
#                 self.dead = True

#     # Các hàm xoay giữ nguyên, thêm _increment_action vào mỗi action thay đổi trạng thái
#     def turn_left(self):
#         dirs = ["NORTH", "WEST", "SOUTH", "EAST"]
#         idx = dirs.index(self.direction)
#         self.direction = dirs[(idx + 1) % 4]
#         self.action_log.append("TURN_LEFT")
#         self._increment_action()
#         return "TURN_LEFT"

#     def turn_right(self):
#         dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
#         idx = dirs.index(self.direction)
#         self.direction = dirs[(idx + 1) % 4]
#         self.action_log.append("TURN_RIGHT")
#         self._increment_action()
#         return "TURN_RIGHT"

#     def turn_towards(self, target_dir):
#         dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
#         cur_idx = dirs.index(self.direction)
#         tgt_idx = dirs.index(target_dir)

#         if (cur_idx - tgt_idx) % 4 == 1:
#             return self.turn_left()
#         elif (tgt_idx - cur_idx) % 4 == 1:
#             return self.turn_right()
#         else:
#             return self.turn_left()
    
#     def get_direction_to(self, next_pos):
#         nx, ny = next_pos
#         if nx > self.x: return "EAST"
#         if nx < self.x: return "WEST"
#         if ny > self.y: return "NORTH"
#         if ny < self.y: return "SOUTH"
#         return self.direction


#     def get_wumpus_direction(self):
#         possible_wumpus_cells = self.inference.get_possible_wumpus()
#         if not possible_wumpus_cells:
#             return None

#         min_dist = float('inf')
#         target_dir = None
#         for (wx, wy) in possible_wumpus_cells:
#             # Chỉ xét nếu cùng hàng hoặc cùng cột
#             if wx == self.x or wy == self.y:
#                 dist = abs(wx - self.x) + abs(wy - self.y)
#                 if dist < min_dist:
#                     min_dist = dist
#                     if wx > self.x:
#                         target_dir = "EAST"
#                     elif wx < self.x:
#                         target_dir = "WEST"
#                     elif wy > self.y:
#                         target_dir = "NORTH"
#                     elif wy < self.y:
#                         target_dir = "SOUTH"
#         return target_dir


#     def move_to(self, next_pos):
#         if not self.is_move_safe(next_pos):
#             print(f"[AGENT_ADVANCED] Warning: unsafe move to {next_pos}")
#             return False
#         old_pos = (self.x, self.y)
#         self.x, self.y = next_pos
#         self.path.append(next_pos)
#         result = self.env.move_agent(self.x, self.y)
#         self.action_log.append(f"MOVE to {next_pos}")
#         self.point -= 1

#         self._increment_action()

#         if self.check_death():
#             self.dead = True
#             self.point -= 1000
#             print(f"[AGENT_ADVANCED] Agent died moving from {old_pos} to {next_pos}")
#         return True

#     def step(self):
#         if self.escaped or self.dead:
#             return "STAY"

#         if self.check_death():
#             self.dead = True
#             self.point -= 1000
#             return "DIE"

#         percepts = self.env.get_percepts(self.x, self.y)
#         self.inference.update_knowledge((self.x, self.y), percepts)

#         # ---- GRAB GOLD ----
#         if percepts["glitter"] and not self.has_gold:
#             self.has_gold = True
#             result = self.env.grab_gold()
#             if result.get("eaten", False):
#                 self.dead = True
#                 return "DIE"
#             self.action_log.append("GRAB")
#             self.point += 10
#             self._increment_action()
#             return "GRAB"

#         # ---- CLIMB OUT ----
#         if self.has_gold and (self.x, self.y) == (0, 0):
#             result = self.env.climb_out()
#             if result.get("eaten", False):
#                 self.dead = True
#                 return "DIE"
#             self.escaped = result["escaped"]
#             self.point += 1000
#             self.action_log.append("CLIMB")
#             self._increment_action()
#             return "CLIMB"

#         # ---- GO HOME WITH GOLD ----
#         if self.has_gold:
#             path_home = astar_search((self.x, self.y), (0, 0),
#                                     self.inference.is_safe, self.env.size)
#             if path_home:
#                 next_pos = path_home[0]
#                 target_dir = self.get_direction_to(next_pos)
#                 if self.direction != target_dir:
#                     return self.turn_towards(target_dir)
#                 if self.is_move_safe(next_pos):
#                     self.move_to(next_pos)
#                     return "MOVE"
#                 return "STUCK"
#             return "STUCK"

#         # ---- SHOOT WUMPUS ----
#         if self.has_arrow and percepts["stench"] and self.can_shoot_wumpus_safely():
#             target_dir = self.get_wumpus_direction()
#             if target_dir and self.direction != target_dir:
#                 return self.turn_towards(target_dir)
#             result = self.env.shoot_arrow(self.direction)
#             if result.get("eaten", False):
#                 self.dead = True
#                 return "DIE"
#             self.has_arrow = False
#             self.point -= 10
#             if result["scream"]:
#                 self.inference.remove_wumpus_after_kill((self.x, self.y), self.direction)
#                 self.action_log.append("SHOOT_HIT")
#                 self._increment_action()
#                 return "SHOOT_HIT"
#             else:
#                 self.action_log.append("SHOOT_MISS")
#                 self._increment_action()
#                 return "SHOOT_MISS"

#         # ---- MOVE TO SAFE NEIGHBOR ----
#         safe_neighbors = self.get_truly_safe_neighbors()
#         if safe_neighbors:
#             best_neighbor = self.choose_best_neighbor(safe_neighbors)
#             target_dir = self.get_direction_to(best_neighbor)
#             if self.direction != target_dir:
#                 return self.turn_towards(target_dir)
#             self.move_to(best_neighbor)
#             return "MOVE"

#         # ---- RETURN HOME IF NOTHING ELSE ----
#         if not self.has_gold and (self.x, self.y) != (0, 0):
#             path_home = astar_search((self.x, self.y), (0, 0),
#                                     self.inference.is_safe, self.env.size)
#             if path_home:
#                 target_dir = self.get_direction_to(path_home[0])
#                 if self.direction != target_dir:
#                     return self.turn_towards(target_dir)
#                 if self.is_move_safe(path_home[0]):
#                     self.move_to(path_home[0])
#                     return "MOVE"

#         return "STAY"

#     # Các hàm phụ (check_death, is_move_safe, get_truly_safe_neighbors, get_direction_to, get_wumpus_direction,
#     # choose_best_neighbor, can_shoot_wumpus_safely, ... ) giữ nguyên từ class Agent của bạn
#     # Chỉ cần copy lại nguyên, thêm hoặc sửa nơi gọi _increment_action khi có hành động

#     # Ví dụ hàm check_death
#     # def check_death(self):
#     #     current_cell = self.env.grid[self.y][self.x]
#     #     return current_cell.pit or current_cell.wumpus

#     # def is_move_safe(self, next_pos):
#     #     next_x, next_y = next_pos
#     #     if not (0 <= next_x < self.env.size and 0 <= next_y < self.env.size):
#     #         return False
#     #     if (next_x, next_y) in self.inference.confirmed_pits:
#     #         return False
#     #     if (next_x, next_y) in self.inference.confirmed_wumpus:
#     #         return False
#     #     kb_info = self.inference.kb.get((next_x, next_y), {})
#     #     if kb_info.get('visited', False):
#     #         return True
#     #     if not kb_info.get('possible_pit', False) and not kb_info.get('possible_wumpus', False):
#     #         return True
#     #     return False

#     def check_death(self):
#         """Check if agent is in a deadly cell"""
#         current_cell = self.env.grid[self.y][self.x]  # Note: grid[y][x] format
#         return current_cell.pit or current_cell.wumpus

#     def is_move_safe(self, next_pos):
#         next_x, next_y = next_pos
        
#         # Kiểm tra giới hạn
#         if not (0 <= next_x < self.env.size and 0 <= next_y < self.env.size):
#             return False
            
#         # Kiểm tra từ inference
#         kb_info = self.inference.kb.get((next_x, next_y), {})
        
#         # Nếu đã thăm và có pit hoặc wumpus thì không an toàn
#         if (next_x, next_y) in self.inference.confirmed_pits:
#             return False
#         if (next_x, next_y) in self.inference.confirmed_wumpus:
#             return False
#         if kb_info.get('visited', False):
#             return True
#         if not kb_info.get('possible_pit', False) and not kb_info.get('possible_wumpus', False):
#             return True

#         return False
    
#     def get_truly_safe_neighbors(self):
#         neighbors = get_neighbors((self.x, self.y), self.env.size)
#         safe_neighbors = []
        
#         # Ưu tiên các ô chưa visited
#         for pos in neighbors:
#             if self.is_move_safe(pos) and not self.inference.kb.get(pos, {}).get('visited', False):
#                 safe_neighbors.append(pos)
#                 self.inference.mark_safe_and_neighbors(pos)

#         # Nếu không còn ô chưa visited, cho phép đi lại ô đã visited (an toàn)
#         if not safe_neighbors:
#             for pos in neighbors:
#                 if self.is_move_safe(pos):
#                     safe_neighbors.append(pos)

#         return safe_neighbors

#     def choose_best_neighbor(self, safe_neighbors):
#         """Choose the best neighbor to explore"""
#         if not safe_neighbors:
#             return None
            
#         # Prefer neighbors that are closer to the center for better exploration
#         center = (self.env.size // 2, self.env.size // 2)
#         return min(safe_neighbors, key=lambda pos: heuristic(pos, center))

#     def find_safe_exploration_target(self):
#         """Find a safe unexplored cell to target"""
#         for x in range(self.env.size):
#             for y in range(self.env.size):
#                 pos = (x, y)
#                 kb_info = self.inference.kb.get(pos, {})
#                 if (not kb_info.get('visited', False) and 
#                     self.inference.is_safe(pos) and
#                     self.is_move_safe(pos)):
#                     return pos
#         return None

#     def can_shoot_wumpus_safely(self):
#         """Check if shooting would be beneficial and safe"""
#         if not self.has_arrow:
#             return False
            
#         # Check if there's likely a wumpus in shooting direction
#         x, y = self.x, self.y
#         dx, dy = {
#             "NORTH": (0, 1),
#             "EAST": (1, 0),
#             "SOUTH": (0, -1),
#             "WEST": (-1, 0)
#         }.get(self.direction, (0, 0))
        
#         # Look ahead in shooting direction
#         check_x, check_y = x + dx, y + dy
#         while (0 <= check_x < self.env.size and 0 <= check_y < self.env.size):
#             pos = (check_x, check_y)
#             if self.inference.kb.get(pos, {}).get('possible_wumpus', False):
#                 return True
#             check_x += dx
#             check_y += dy
            
#         return False

#     def move_to(self, next_pos):
#         """Move agent to next position"""
#         # Double-check safety before moving
#         if not self.is_move_safe(next_pos):
#             print(f"[AGENT] Warning: Attempting unsafe move to {next_pos}")
#             return False
            
#         old_pos = (self.x, self.y)
#         self.x, self.y = next_pos
#         self.path.append(next_pos)
        
#         result = self.env.move_agent(self.x, self.y)
#         if result.get("eaten", False):
#             self.dead = True
#             print(f"[AGENT_ADVANCED] Agent bị Wumpus ăn khi di chuyển đến {next_pos}")
#             return False
#         self.action_log.append(f"MOVE to {next_pos}")
#         self.point -= 1
        
#         self._increment_action()
#         # Check for death after moving
#         if self.check_death():
#             self.dead = True
#             self.point -= 1000
#             print(f"[AGENT] Agent died moving from {old_pos} to {next_pos}")
            
#         return True

#     def finished(self):
#         return self.escaped or self.dead

#     def take_action(self, action):
#         """Backward compatibility method"""
#         if action == "Move Forward":
#             self.point -= 1
#         elif action == "Grab":
#             self.point += 10
#         elif action == "Climb":
#             self.point += 1000 if self.has_gold else 0
#         elif action == "Shoot":
#             self.point -= 10

#     def _handle_breeze_situation(self):
#         """Xử lý khi agent phát hiện breeze - phiên bản nâng cao"""
#         confirmed_pits = self.inference.confirmed_pits
#         possible_pits = self.inference.get_possible_pits()
        
#         # Ưu tiên 1: Tìm đường tránh confirmed pits
#         if confirmed_pits:
#             safe_path = self.find_path_avoiding_pits(confirmed_pits)
#             if safe_path:
#                 return self._execute_move(safe_path[0])
        
#         # Ưu tiên 2: Nếu bị kẹt giữa possible pits, quay lại ô đã visited
#         if possible_pits:
#             # Tìm ô đã visited gần nhất không có breeze
#             safe_retreat = self._find_safe_retreat()
#             if safe_retreat:
#                 path = astar_search((self.x, self.y), safe_retreat,
#                                 self.inference.is_safe, self.env.size)
#                 if path:
#                     return self._execute_move(path[0])
        
#         # Ưu tiên 3: Thử di chuyển đến ô có ít possible pits xung quanh nhất
#         safe_moves = self._get_safest_possible_moves()
#         if safe_moves:
#             return self._execute_move(safe_moves[0][0])
        
#         # Cuối cùng: Thử quay về (0,0)
#         if (self.x, self.y) != (0, 0):
#             path_home = astar_search((self.x, self.y), (0, 0),
#                                 self.inference.is_safe, self.env.size)
#             if path_home:
#                 return self._execute_move(path_home[0])
            

#     def _get_safest_possible_moves(self):
        
#         neighbors = get_neighbors((self.x, self.y), self.env.size)
#         possible_pits = self.inference.get_possible_pits()
#         safe_moves = []
        
#         for pos in neighbors:
#             if self.is_move_safe(pos):
#                 # Tính risk (số possible pits xung quanh ô đích)
#                 risk = sum(1 for p in get_neighbors(pos, self.env.size) 
#                         if p in possible_pits)
#                 safe_moves.append((pos, risk))
        
#         # Sắp xếp theo risk tăng dần
#         safe_moves.sort(key=lambda x: x[1])
#         return safe_moves
    
#     def _find_safe_retreat(self):
#         visited_safe = []
#         for pos, data in self.inference.kb.items():
#             if data['visited']:
#                 # Lấy percepts từ environment thay vì từ self.percepts
#                 percepts = self.env.get_percepts(pos[0], pos[1]) # lát check
#                 if not percepts.get('breeze', False):
#                     visited_safe.append(pos)
        
#         if not visited_safe:
#             return None
            
#         # Tìm ô gần nhất
#         return min(visited_safe, key=lambda p: heuristic((self.x, self.y), p))


#     def find_path_avoiding_pits(self, pits):
#         def is_safe_but_avoid_pits(pos):
#             if pos in pits:
#                 return False
#             return self.inference.is_safe(pos)

#         return astar_search((self.x, self.y), (0, 0), is_safe_but_avoid_pits, self.env.size)

#     def find_safest_path(self, possible_pits):
#         def safety_cost(pos):
#             if pos in possible_pits:
#                 return 100  # Phạt nặng các ô possible pit
#             return 1
        
#         # Sử dụng A* với hàm cost tùy chỉnh
#         path = []
#         min_cost = float('inf')
        
#         # Thử tìm đường đến các ô safe unvisited trước
#         safe_targets = self.inference.get_safe_unvisited_neighbors((self.x, self.y))
#         for target in safe_targets:
#             current_path = astar_search((self.x, self.y), target,
#                                     self.inference.is_safe, self.env.size)
#             if current_path:
#                 current_cost = sum(safety_cost(p) for p in current_path)
#                 if current_cost < min_cost:
#                     min_cost = current_cost
#                     path = current_path
        
#         # Nếu không tìm được, thử về (0,0)
#         if not path:
#             path = astar_search((self.x, self.y), (0, 0),
#                             self.inference.is_safe, self.env.size)
#         return path
#     # Hãy nhớ gọi self._increment_action() mỗi khi agent làm hành động: move, turn, grab, shoot, climb
from wumpus.planner import astar_search
from wumpus.algorithm import heuristic
from wumpus.utils import get_neighbors

class AgentAdvanced:
    def __init__(self, env, inference):
        self.env = env
        self.inference = inference
        self.x, self.y = 0, 0
        self.direction = "EAST"
        self.has_gold = False
        self.has_arrow = True
        self.point = 0
        self.path = [(0, 0)]
        self.action_log = []
        self.escaped = False
        self.dead = False
        # nhớ ô trước khi di chuyển để tránh back-and-forth
        self.prev_pos = None

    def turn_left(self):
        dirs = ["NORTH", "WEST", "SOUTH", "EAST"]
        idx = dirs.index(self.direction)
        self.direction = dirs[(idx + 1) % 4]
        self.action_log.append("TURN_LEFT")
        # Không gọi _increment_action nữa
        return "TURN_LEFT"

    def turn_right(self):
        dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
        idx = dirs.index(self.direction)
        self.direction = dirs[(idx + 1) % 4]
        self.action_log.append("TURN_RIGHT")
        return "TURN_RIGHT"

    def turn_towards(self, target_dir):
        dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
        cur_idx = dirs.index(self.direction)
        tgt_idx = dirs.index(target_dir)

        if (cur_idx - tgt_idx) % 4 == 1:
            return self.turn_left()
        elif (tgt_idx - cur_idx) % 4 == 1:
            return self.turn_right()
        else:
            return self.turn_left()

    def get_direction_to(self, next_pos):
        nx, ny = next_pos
        if nx > self.x: return "EAST"
        if nx < self.x: return "WEST"
        if ny > self.y: return "NORTH"
        if ny < self.y: return "SOUTH"
        return self.direction

    def get_wumpus_direction(self):
        possible_wumpus_cells = self.inference.get_possible_wumpus()
        if not possible_wumpus_cells:
            return None

        min_dist = float('inf')
        target_dir = None
        for (wx, wy) in possible_wumpus_cells:
            if wx == self.x or wy == self.y:
                dist = abs(wx - self.x) + abs(wy - self.y)
                if dist < min_dist:
                    min_dist = dist
                    if wx > self.x:
                        target_dir = "EAST"
                    elif wx < self.x:
                        target_dir = "WEST"
                    elif wy > self.y:
                        target_dir = "NORTH"
                    elif wy < self.y:
                        target_dir = "SOUTH"
        return target_dir

    def is_move_safe(self, next_pos):
        next_x, next_y = next_pos

        if not (0 <= next_x < self.env.size and 0 <= next_y < self.env.size):
            return False
        if (next_x, next_y) in self.inference.confirmed_pits:
            return False
        if (next_x, next_y) in self.inference.confirmed_wumpus:
            return False
        kb_info = self.inference.kb.get((next_x, next_y), {})
        if kb_info.get('visited', False):
            return True
        if not kb_info.get('possible_pit', False) and not kb_info.get('possible_wumpus', False):
            return True
        return False

    def check_death(self):
        current_cell = self.env.grid[self.y][self.x]
        return current_cell.pit or current_cell.wumpus

    def get_truly_safe_neighbors(self):
        neighbors = get_neighbors((self.x, self.y), self.env.size)
        safe_neighbors = []

        # Lấy tất cả ô an toàn theo is_move_safe
        for pos in neighbors:
            if self.is_move_safe(pos):
                safe_neighbors.append(pos)

        if not safe_neighbors:
            return []

        # Nếu có nhiều lựa chọn, tránh immediate backtrack về prev_pos (nếu prev_pos tồn tại)
        if self.prev_pos and self.prev_pos in safe_neighbors and len(safe_neighbors) > 1:
            safe_neighbors.remove(self.prev_pos)

        # Sắp xếp ưu tiên:
        # 1) unvisited trước (False < True)
        # 2) nhiều unexplored neighbors hơn (desc)
        # 3) gần center hơn (tie-break)
        center = (self.env.size // 2, self.env.size // 2)
        def unexplored_count(pos):
            return self.count_unexplored_neighbors(pos)

        safe_neighbors.sort(key=lambda p: (
            self.inference.kb.get(p, {}).get('visited', False),   # False (unvisited) < True (visited)
            -unexplored_count(p),                                 # more unexplored neighbors first
            heuristic(p, center)                                  # smaller distance to center
        ))
        return safe_neighbors



    def choose_best_neighbor(self, safe_neighbors):
        """Chọn ô tốt nhất dựa trên độ ưu tiên khám phá, tránh prev_pos nếu có thể."""
        if not safe_neighbors:
            return None

        # nếu prev_pos có trong danh sách và còn lựa chọn khác, không chọn prev_pos
        candidates = list(safe_neighbors)
        if self.prev_pos and self.prev_pos in candidates and len(candidates) > 1:
            candidates.remove(self.prev_pos)

        # Phân loại unvisited / visited
        unvisited = [pos for pos in candidates 
                     if not self.inference.kb.get(pos, {}).get('visited', False)]
        visited = [pos for pos in candidates 
                   if self.inference.kb.get(pos, {}).get('visited', False)]

        # Nếu có unvisited -> chọn ô có nhiều unexplored neighbors nhất
        if unvisited:
            return max(unvisited, key=lambda pos: self.count_unexplored_neighbors(pos))

        # Nếu không có unvisited -> chọn visited dẫn tới nhiều unexplored neighbors
        if visited:
            return max(visited, key=lambda pos: self.count_unexplored_neighbors(pos))

        # Fallback
        return candidates[0]

    def count_unexplored_neighbors(self, pos):
        neighbors = get_neighbors(pos, self.env.size)
        count = 0
        for n in neighbors:
            kb_info = self.inference.kb.get(n, {})
            # coi là 'chưa khám phá' nếu chưa visited và có thể di chuyển (is_move_safe)
            if not kb_info.get('visited', False) and self.is_move_safe(n):
                count += 1
        return count


    def can_shoot_wumpus_safely(self):
        if not self.has_arrow:
            return False
        x, y = self.x, self.y
        dx, dy = {
            "NORTH": (0, 1),
            "EAST": (1, 0),
            "SOUTH": (0, -1),
            "WEST": (-1, 0)
        }.get(self.direction, (0, 0))

        check_x, check_y = x + dx, y + dy
        while (0 <= check_x < self.env.size and 0 <= check_y < self.env.size):
            pos = (check_x, check_y)
            if self.inference.kb.get(pos, {}).get('possible_wumpus', False):
                return True
            check_x += dx
            check_y += dy

        return False

    def move_to(self, next_pos):
        if not self.is_move_safe(next_pos):
            print(f"[AGENT_ADVANCED] Warning: unsafe move to {next_pos}")
            return False
        old_pos = (self.x, self.y)
        self.x, self.y = next_pos
        self.path.append(next_pos)
        result = self.env.move_agent(self.x, self.y)  # Môi trường đếm action và xử lý Wumpus

        self.action_log.append(f"MOVE to {next_pos}")
        self.point -= 1

        # cập nhật prev_pos **chỉ khi** di chuyển thành công
        self.prev_pos = old_pos

        if result.get("eaten", False):
            self.dead = True
            print(f"[AGENT_ADVANCED] Agent bị Wumpus ăn khi di chuyển đến {next_pos}")
            return False
        
        if self.check_death():
            self.dead = True
            self.point -= 1000
            print(f"[AGENT_ADVANCED] Agent died moving from {old_pos} to {next_pos}")

        return True

    def finished(self):
        return self.escaped or self.dead

    def step(self):
        if self.escaped or self.dead:
            return "STAY"

        if self.check_death():
            self.dead = True
            self.point -= 1000
            return "DIE"

        percepts = self.env.get_percepts(self.x, self.y)
        self.inference.update_knowledge((self.x, self.y), percepts)

        # GRAB GOLD
        if percepts["glitter"] and not self.has_gold:
            self.has_gold = True
            result = self.env.grab_gold()
            if result.get("eaten", False):
                self.dead = True
                return "DIE"
            self.action_log.append("GRAB")
            self.point += 10
            return "GRAB"

        # CLIMB OUT
        if self.has_gold and (self.x, self.y) == (0, 0):
            result = self.env.climb_out()
            if result.get("eaten", False):
                self.dead = True
                return "DIE"
            self.escaped = result["escaped"]
            self.point += 1000
            self.action_log.append("CLIMB")
            return "CLIMB"

        # GO HOME WITH GOLD
        if self.has_gold:
            path_home = astar_search((self.x, self.y), (0, 0),
                                    self.inference.is_safe, self.env.size)
            if path_home:
                next_pos = path_home[0]
                target_dir = self.get_direction_to(next_pos)
                if self.direction != target_dir:
                    return self.turn_towards(target_dir)
                if self.is_move_safe(next_pos):
                    self.move_to(next_pos)
                    return "MOVE"
                return "STUCK"
            return "STUCK"

        # SHOOT WUMPUS
        if self.has_arrow and percepts["stench"] and self.can_shoot_wumpus_safely():
            target_dir = self.get_wumpus_direction()
            if target_dir and self.direction != target_dir:
                return self.turn_towards(target_dir)
            result = self.env.shoot_arrow(self.direction)
            if result.get("eaten", False):
                self.dead = True
                return "DIE"
            self.has_arrow = False
            self.point -= 10
            if result["scream"]:
                self.inference.remove_wumpus_after_kill((self.x, self.y), self.direction)
                self.action_log.append("SHOOT_HIT")
                return "SHOOT_HIT"
            else:
                self.action_log.append("SHOOT_MISS")
                return "SHOOT_MISS"

        # MOVE TO SAFE NEIGHBOR
        safe_neighbors = self.get_truly_safe_neighbors()
        if safe_neighbors:
            best_neighbor = self.choose_best_neighbor(safe_neighbors)
            target_dir = self.get_direction_to(best_neighbor)
            if self.direction != target_dir:
                return self.turn_towards(target_dir)
            self.move_to(best_neighbor)
            return "MOVE"

        # RETURN HOME IF NOTHING ELSE
        if not self.has_gold and (self.x, self.y) != (0, 0):
            path_home = astar_search((self.x, self.y), (0, 0),
                                    self.inference.is_safe, self.env.size)
            if path_home:
                target_dir = self.get_direction_to(path_home[0])
                if self.direction != target_dir:
                    return self.turn_towards(target_dir)
                if self.is_move_safe(path_home[0]):
                    self.move_to(path_home[0])
                    return "MOVE"

        return "STAY"


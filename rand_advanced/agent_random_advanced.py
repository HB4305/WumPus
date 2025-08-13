from rand.planner_random import dfs_search
from rand.utils_random import get_neighbors
from .environment_random_advanced import EnvironmentRandomAdvanced
import random

class AgentRandomAdvanced:
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
        # self.action_counter = 0  # Đếm tổng số hành động agent đã làm

    def _increment_action(self):
        # self.action_counter += 1
        self.env.register_action()
        # Mỗi 5 hành động, gọi inference xử lý di chuyển Wumpus
        if self.env.action_count % 5 == 1 and self.env.action_count // 5 >= 1:
            try:
                self.inference.update_wumpus_positions_after_move((self.x, self.y))
            except Exception as e:
                # Nếu agent bị Wumpus ăn chết
                print(f"[AGENT_ADVANCED] {str(e)}")
                self.dead = True

    # Các hàm xoay giữ nguyên, thêm _increment_action vào mỗi action thay đổi trạng thái
    def turn_left(self):
        dirs = ["NORTH", "WEST", "SOUTH", "EAST"]
        idx = dirs.index(self.direction)
        self.direction = dirs[(idx + 1) % 4]
        self.action_log.append("TURN_LEFT")
        self._increment_action()
        return "TURN_LEFT"

    def turn_right(self):
        dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
        idx = dirs.index(self.direction)
        self.direction = dirs[(idx + 1) % 4]
        self.action_log.append("TURN_RIGHT")
        self._increment_action()
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
            # Chỉ xét nếu cùng hàng hoặc cùng cột
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


    def move_to(self, next_pos):
        if not self.is_move_safe(next_pos):
            print(f"[AGENT_ADVANCED] Warning: unsafe move to {next_pos}")
            return False
        old_pos = (self.x, self.y)
        self.x, self.y = next_pos
        self.path.append(next_pos)
        result = self.env.move_agent(self.x, self.y)
        self.action_log.append(f"MOVE to {next_pos}")
        self.point -= 1

        print(f"[AGENT_ADVANCED] Moving")
        self._increment_action()

        if self.check_death():
            self.dead = True
            self.point -= 1000
            print(f"[AGENT_ADVANCED] Agent died moving from {old_pos} to {next_pos}")
        return True
    
    def climb_out(self):
        """Climb out of the cave"""
        if (self.x, self.y) == (0, 0):
            result = self.env.climb_out()
            self.escaped = result["escaped"]
            self.action_log.append("CLIMB")
            if self.escaped:
                self.point += 1000 if self.has_gold else 0
            return True
        return False

    def backtrack_next(self):
        """Lấy ô trước đó theo lịch sử self.path (None nếu không có)."""
        if len(self.path) < 2:
            return None
        return self.path[-2]   # path[-1] là vị trí hiện tại

    
    def step(self):
        # if self.escaped or self.dead:
        #     return "STAY"
        
        # if self.x == 0 and self.y == 0 and len(self.path) > 1:
        

        if self.check_death():
            self.dead = True
            self.point -= 1000
            return "DIE"

        percepts = self.env.get_percepts(self.x, self.y)
        self.inference.update_knowledge((self.x, self.y), percepts)

        # ---- GRAB GOLD ----
        if percepts["glitter"] and not self.has_gold:
            self.has_gold = True
            self.env.grab_gold()
            self.action_log.append("GRAB")
            self.point += 10
            return "GRAB"

        # ---- CLIMB OUT ----
        if self.has_gold and (self.x, self.y) == (0, 0):
            result = self.env.climb_out()
            self.escaped = result["escaped"]
            self.action_log.append("CLIMB")
            if self.escaped:
                self.point += 1000
            return "CLIMB"

        # ---- GO HOME WITH GOLD ----
        if self.has_gold:
            # 1) Thử backtrack theo lịch sử (chắc chắn)
            next_pos = self.backtrack_next()
            if next_pos:
                # bật cờ để agent biết đang quay về (nếu bạn có dùng cờ)
                try:
                    self.backtracking_home = True
                except Exception:
                    pass

                target_dir = self.get_direction_to(next_pos)
                if self.direction != target_dir:
                    return self.turn_towards(target_dir)  # xoay trước
                # move_to đã xử lý pop/append phù hợp khi backtracking
                if self.move_to(next_pos):
                    return "MOVE"
                return "DIE"

            # 2) Nếu không có history (hiếm) => fallback: thử dùng dfs search an toàn
            path_home = dfs_search((self.x, self.y), (0, 0),
                                     self.inference.is_safe, self.env.size)
            if path_home:
                next_pos = path_home[0]
                target_dir = self.get_direction_to(next_pos)
                if self.direction != target_dir:
                    return self.turn_towards(target_dir)  # xoay trước
                # cho phép di chuyển nếu an toàn hoặc ô đó đã từng visited (fallback)
                if self.is_move_safe(next_pos) or self.inference.kb.get(next_pos, {}).get('visited', False):
                    if self.move_to(next_pos):
                        return "MOVE"
                    return "DIE"
                return "STUCK"
            # không tìm được đường nào
            return "STUCK"

        # ---- SHOOT WUMPUS ----
        if self.has_arrow and percepts["stench"] and self.can_shoot_wumpus_safely():
            target_dir = self.get_wumpus_direction()
            if target_dir and self.direction != target_dir:
                return self.turn_towards(target_dir)  # xoay trước khi bắn
            result = self.env.shoot_arrow(self.direction)
            self.has_arrow = False
            self.point -= 10
            if result["scream"]:
                self.inference.remove_wumpus_after_kill((self.x, self.y), self.direction)
                self.action_log.append("SHOOT_HIT")
                return "SHOOT_HIT"
            else:
                self.action_log.append("SHOOT_MISS")
                return "SHOOT_MISS"

        # ---- MOVE TO SAFE NEIGHBOR ----
        safe_neighbors = self.get_truly_safe_neighbors()
        if safe_neighbors:
            best_neighbor = self.choose_best_neighbor(safe_neighbors) # ưu tiên ô gần trung tâm
            target_dir = self.get_direction_to(best_neighbor)
            if self.direction != target_dir:
                return self.turn_towards(target_dir)  # xoay trước khi đi
            # self.move_to(best_neighbor)
            move_result = self.move_to(best_neighbor)
            if not move_result:  # Nếu move_to trả về False (agent chết)
                return "DIE"
            return "MOVE"

        # ---- EXPLORE SAFE UNKNOWN ----
        exploration_target = self.find_safe_exploration_target()
        if exploration_target:
            path = dfs_search((self.x, self.y), exploration_target,
                                self.inference.is_safe, self.env.size)
            if path:
                target_dir = self.get_direction_to(path[0])
                if self.direction != target_dir:
                    return self.turn_towards(target_dir)
                if self.is_move_safe(path[0]):
                    # self.move_to(path[0])
                    move_result = self.move_to(path[0])
                    if not move_result:  # Nếu move_to trả về False (agent chết)
                        return "DIE"
                    return "MOVE"

        # ---- RETURN HOME IF NOTHING ELSE ----
        if not self.has_gold and (self.x, self.y) != (0, 0):
            # BACKTRACK THE SURE WAY: dùng lịch sử self.path (không phụ thuộc vào dfs/inference)
            next_pos = self.backtrack_next()
            if next_pos:
                target_dir = self.get_direction_to(next_pos)
                if self.direction != target_dir:
                    return self.turn_towards(target_dir)
                if self.move_to(next_pos):
                    return "MOVE"
                return "DIE"
            # Nếu không có history để backtrack (hiếm vì path khởi tạo [(0,0)]), fallback risky:
            next_pos = self._get_direction_toward_home_risky()
            if next_pos:
                target_dir = self.get_direction_to(next_pos)
                if self.direction != target_dir:
                    return self.turn_towards(target_dir)
                if self.move_to(next_pos):
                    return "MOVE"
                return "DIE"

        
        if self.x == 0 and self.y == 0:
            self.climb_out()
            return "CLIMB"
        

        # ---- HANDLE BREEZE ----
        if percepts["breeze"]:
            self._handle_breeze_situation()
        
        return "STAY"

    # Các hàm phụ (check_death, is_move_safe, get_truly_safe_neighbors, get_direction_to, get_wumpus_direction,
    # choose_best_neighbor, can_shoot_wumpus_safely, ... ) giữ nguyên từ class Agent của bạn
    # Chỉ cần copy lại nguyên, thêm hoặc sửa nơi gọi _increment_action khi có hành động

    # Ví dụ hàm check_death
    # def check_death(self):
    #     current_cell = self.env.grid[self.y][self.x]
    #     return current_cell.pit or current_cell.wumpus

    # def is_move_safe(self, next_pos):
    #     next_x, next_y = next_pos
    #     if not (0 <= next_x < self.env.size and 0 <= next_y < self.env.size):
    #         return False
    #     if (next_x, next_y) in self.inference.confirmed_pits:
    #         return False
    #     if (next_x, next_y) in self.inference.confirmed_wumpus:
    #         return False
    #     kb_info = self.inference.kb.get((next_x, next_y), {})
    #     if kb_info.get('visited', False):
    #         return True
    #     if not kb_info.get('possible_pit', False) and not kb_info.get('possible_wumpus', False):
    #         return True
    #     return False

    def check_death(self):
        """Check if agent is in a deadly cell"""
        current_cell = self.env.grid[self.y][self.x]  # Note: grid[y][x] format
        return current_cell.pit or current_cell.wumpus

    def is_move_safe(self, next_pos):
        next_x, next_y = next_pos
        
        # Kiểm tra giới hạn
        if not (0 <= next_x < self.env.size and 0 <= next_y < self.env.size):
            return False
            
        # Kiểm tra từ inference
        kb_info = self.inference.kb.get((next_x, next_y), {})
        
        # Nếu đã thăm và có pit hoặc wumpus thì không an toàn
        if (next_x, next_y) in self.inference.confirmed_pits:
            return False
        if (next_x, next_y) in self.inference.confirmed_wumpus:
            return False
        if kb_info.get('visited', False):
            return True
        if not kb_info.get('possible_pit', False) and not kb_info.get('possible_wumpus', False):
            return True

        return False
    
    def get_truly_safe_neighbors(self):
        neighbors = get_neighbors((self.x, self.y), self.env.size)
        safe_neighbors = []
        
        for pos in neighbors:
            if self.is_move_safe(pos) and not self.inference.kb.get(pos, {}).get('visited', False):
                safe_neighbors.append(pos)
                # mark neighbors of pos safe luôn
                self.inference.mark_safe_and_neighbors(pos)
        
        return safe_neighbors

    def choose_best_neighbor(self, safe_neighbors):
        """tìm ô an toàn chưa thăm bằng bfs không bằng random tránh backtracking"""
        from collections import deque
        if not safe_neighbors:
            return None

        # Ưu tiên ô chưa thăm gần nhất tính từ vị trí hiện tại
        def bfs_find_closest(targets):
            visited = set()
            queue = deque([(self.x, self.y, [])])
            while queue:
                cx, cy, path = queue.popleft()
                if (cx, cy) in visited:
                    continue
                visited.add((cx, cy))
                if (cx, cy) in targets:
                    return path[0] if path else (cx, cy)
                for nx, ny in get_neighbors((cx, cy), self.env.size):
                    if self.is_move_safe((nx, ny)):
                        queue.append((nx, ny, path + [(nx, ny)]))
            return None

        return bfs_find_closest(set(safe_neighbors))

    def find_safe_exploration_target(self):
        targets = []
        for pos, data in self.inference.kb.items():
            if (not data.get('visited', False) and 
                self.inference.is_safe(pos) and 
                self.is_move_safe(pos)):
                targets.append(pos)

        if not targets:
            return None

        # Tìm ô gần nhất theo BFS
        from collections import deque
        visited = set()
        queue = deque([(self.x, self.y)])
        parent = { (self.x, self.y): None }

        while queue:
            current = queue.popleft()
            if current in targets:
                # Lấy bước đầu tiên của đường đi
                while parent[current] != (self.x, self.y) and parent[current] is not None:
                    current = parent[current]
                return current

            for neighbor in get_neighbors(current, self.env.size):
                if neighbor not in visited and self.is_move_safe(neighbor):
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return None

    def can_shoot_wumpus_safely(self):
        """Check if shooting would be beneficial and safe"""
        if not self.has_arrow:
            return False
            
        # Check if there's likely a wumpus in shooting direction
        x, y = self.x, self.y
        dx, dy = {
            "NORTH": (0, 1),
            "EAST": (1, 0),
            "SOUTH": (0, -1),
            "WEST": (-1, 0)
        }.get(self.direction, (0, 0))
        
        # Look ahead in shooting direction
        check_x, check_y = x + dx, y + dy
        while (0 <= check_x < self.env.size and 0 <= check_y < self.env.size):
            pos = (check_x, check_y)
            if self.inference.kb.get(pos, {}).get('possible_wumpus', False):
                return True
            check_x += dx
            check_y += dy
            
        return False

    def move_to(self, next_pos):
        """Move agent to next position; nếu đang backtrack theo lịch sử thì pop last, không append."""
        # Cho phép backtrack qua ô đã visited; nếu ô chưa visited thì vẫn require is_move_safe
        if not self.is_move_safe(next_pos) and not self.inference.kb.get(next_pos, {}).get('visited', False):
            print(f"[AGENT] Warning: Attempting unsafe move to {next_pos}")
            return False

        old_pos = (self.x, self.y)

        # Nếu prev in path là next_pos => đây là backtrack: pop last element thay vì append
        if len(self.path) >= 2 and self.path[-2] == next_pos:
            # backtrack thực sự: loại bỏ vị trí hiện tại khỏi lịch sử
            self.path.pop()
        else:
            # normal forward move: append
            self.path.append(next_pos)

        # cập nhật vị trí
        self.x, self.y = next_pos

        # thực hiện move lên environment
        result = self.env.move_agent(self.x, self.y)
        self.action_log.append(f"MOVE to {next_pos}")
        self.point -= 1
        self._increment_action()

        # mark visited ngay khi move thành công
        kb_entry = self.inference.kb.setdefault((self.x, self.y), {})
        kb_entry['visited'] = True

        # Check for death after moving
        if self.check_death():
            self.dead = True
            self.point -= 1000
            print(f"[AGENT] Agent died moving from {old_pos} to {next_pos}")
            return False
        return True

    def finished(self):
        return self.escaped or self.dead

    def take_action(self, action):
        """Backward compatibility method"""
        if action == "Move Forward":
            self.point -= 1
        elif action == "Grab":
            self.point += 10
        elif action == "Climb":
            self.point += 1000 if self.has_gold else 0
        elif action == "Shoot":
            self.point -= 10

    def _handle_breeze_situation(self):
        """Xử lý khi agent phát hiện breeze - phiên bản nâng cao"""
        confirmed_pits = self.inference.confirmed_pits
        possible_pits = self.inference.get_possible_pits()
        
        # Ưu tiên 1: Tìm đường tránh confirmed pits
        if confirmed_pits:
            safe_path = self.find_path_avoiding_pits(confirmed_pits)
            if safe_path:
                return self._execute_move(safe_path[0])
        
        # Ưu tiên 2: Nếu bị kẹt giữa possible pits, quay lại ô đã visited
        if possible_pits:
            # Tìm ô đã visited gần nhất không có breeze
            safe_retreat = self._find_safe_retreat()
            if safe_retreat:
                path = dfs_search((self.x, self.y), safe_retreat,
                                self.inference.is_safe, self.env.size)
                if path:
                    return self._execute_move(path[0])
        
        # Ưu tiên 3: Thử di chuyển đến ô có ít possible pits xung quanh nhất
        safe_moves = self._get_safest_possible_moves()
        if safe_moves:
            return self._execute_move(safe_moves[0][0])
        
        # Cuối cùng: Thử quay về (0,0)
        if (self.x, self.y) != (0, 0):
            path_home = dfs_search((self.x, self.y), (0, 0),
                                self.inference.is_safe, self.env.size)
            if path_home:
                return self._execute_move(path_home[0])
            

    def _get_safest_possible_moves(self):
        
        neighbors = get_neighbors((self.x, self.y), self.env.size)
        possible_pits = self.inference.get_possible_pits()
        safe_moves = []
        
        for pos in neighbors:
            if self.is_move_safe(pos):
                # Tính risk (số possible pits xung quanh ô đích)
                risk = sum(1 for p in get_neighbors(pos, self.env.size) 
                        if p in possible_pits)
                safe_moves.append((pos, risk))
        
        # Sắp xếp theo risk tăng dần
        safe_moves.sort(key=lambda x: x[1])
        return safe_moves
    
    def _find_safe_retreat(self):
        visited_safe = []
        for pos, data in self.inference.kb.items():
            if data['visited']:
                # Lấy percepts từ environment thay vì từ self.percepts
                percepts = self.env.get_percepts(pos[0], pos[1]) # lát check
                if not percepts.get('breeze', False):
                    visited_safe.append(pos)
        
        if not visited_safe:
            return None
            
        # Tìm ô gần nhất
        return random.choice(visited_safe)


    def find_path_avoiding_pits(self, pits):
        def is_safe_but_avoid_pits(pos):
            if pos in pits:
                return False
            return self.inference.is_safe(pos)

        return dfs_search((self.x, self.y), (0, 0), is_safe_but_avoid_pits, self.env.size)

    def find_safest_path(self, possible_pits):
        def safety_cost(pos):
            if pos in possible_pits:
                return 100  # Phạt nặng các ô possible pit
            return 1
        
        # Sử dụng A* với hàm cost tùy chỉnh
        path = []
        min_cost = float('inf')
        
        # Thử tìm đường đến các ô safe unvisited trước
        safe_targets = self.inference.get_safe_unvisited_neighbors((self.x, self.y))
        for target in safe_targets:
            current_path = dfs_search((self.x, self.y), target,
                                    self.inference.is_safe, self.env.size)
            if current_path:
                current_cost = sum(safety_cost(p) for p in current_path)
                if current_cost < min_cost:
                    min_cost = current_cost
                    path = current_path
        
        # Nếu không tìm được, thử về (0,0)
        if not path:
            path = dfs_search((self.x, self.y), (0, 0),
                            self.inference.is_safe, self.env.size)
        return path
    # Hãy nhớ gọi self._increment_action() mỗi khi agent làm hành động: move, turn, grab, shoot, climb



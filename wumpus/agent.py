from .planner import astar_search
from .algorithm import heuristic
from .utils import get_neighbors

class Agent:
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
    
   # ======== HÀM XOAY ======== #
    def turn_left(self):
        dirs = ["NORTH", "WEST", "SOUTH", "EAST"]
        idx = dirs.index(self.direction)
        self.direction = dirs[(idx + 1) % 4]
        self.action_log.append("TURN_LEFT")
        return "TURN_LEFT"

    def turn_right(self):
        dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
        idx = dirs.index(self.direction)
        self.direction = dirs[(idx + 1) % 4]
        self.action_log.append("TURN_RIGHT")
        return "TURN_RIGHT"

    def turn_towards(self, target_dir):
        """Chỉ xoay trái hoặc phải 1 bước mỗi lượt"""
        dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
        cur_idx = dirs.index(self.direction)
        tgt_idx = dirs.index(target_dir)

        # Xác định xoay trái hay phải
        if (cur_idx - tgt_idx) % 4 == 1:
            return self.turn_left()
        elif (tgt_idx - cur_idx) % 4 == 1:
            return self.turn_right()
        else:
            # Nếu khác 180° → xoay trái hoặc phải tùy ý (ưu tiên trái)
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

    # def step(self):
    #     if self.escaped or self.dead:
    #         return "STAY"

    #     # Check if agent died BEFORE taking action
    #     if self.check_death():
    #         self.dead = True
    #         self.point -= 1000
    #         return "DIE"

    #     # Get current percepts and update knowledge
    #     percepts = self.env.get_percepts(self.x, self.y)
    #     self.inference.update_knowledge((self.x, self.y), percepts)

    #     # If found gold, grab it
    #     if percepts["glitter"] and not self.has_gold:
    #         self.has_gold = True
    #         result = self.env.grab_gold()
    #         self.action_log.append("GRAB")
    #         self.point += 10
    #         return "GRAB"

    #     # If has gold and at start, climb out
    #     if self.has_gold and (self.x, self.y) == (0, 0):
    #         result = self.env.climb_out()
    #         self.escaped = result["escaped"]
    #         self.action_log.append("CLIMB")
    #         if self.escaped:
    #             self.point += 1000
    #         return "CLIMB"

    #     # If has gold, go home
    #     if self.has_gold:
    #         path_home = astar_search((self.x, self.y), (0, 0), 
    #                                self.inference.is_safe, self.env.size)
    #         if path_home:
    #             next_pos = path_home[0]
    #             # self.face_towards(next_pos)   # ✅ xoay trước
    #             if self.is_move_safe(next_pos):
    #                 self.move_to(next_pos)
    #                 return "MOVE"
    #             else:
    #                 return "STUCK"
    #         else:
    #             return "STUCK"

    #     # Try to shoot wumpus if possible and beneficial
    #     if (self.has_arrow and percepts["stench"] and self.can_shoot_wumpus_safely()):
    #         # result = self.env.shoot_arrow()
    #         # self.has_arrow = False
    #         # self.point -= 10
    #         # if result["scream"]:
    #         #     self.inference.remove_wumpus_after_kill((self.x, self.y), self.direction)
    #         #     self.action_log.append("SHOOT_HIT")
    #         #     return "SHOOT_HIT"
    #         # else:
    #         #     self.action_log.append("SHOOT_MISS")
    #         #     return "SHOOT_MISS"
    #         target_dir = self.get_wumpus_direction()
    #         if target_dir and self.direction != target_dir:
    #             return self.turn_towards(target_dir)
    #         result = self.env.shoot_arrow()
    #         self.has_arrow = False
    #         self.point -= 10
    #         if result["scream"]:
    #             self.inference.remove_wumpus_after_kill((self.x, self.y), self.direction)
    #             self.action_log.append("SHOOT_HIT")
    #             return "SHOOT_HIT"
    #         else:
    #             self.action_log.append("SHOOT_MISS")
    #             return "SHOOT_MISS"

    #     # Look for safe unvisited neighbors
    #     safe_neighbors = self.get_truly_safe_neighbors()
    #     if safe_neighbors:
    #         # Choose the best neighbor (closest to center or unexplored)
    #         best_neighbor = self.choose_best_neighbor(safe_neighbors)
    #         self.move_to(best_neighbor)
    #         return "MOVE"

    #     # Find path to safe unexplored area
    #     exploration_target = self.find_safe_exploration_target()
    #     if exploration_target:
    #         path = astar_search((self.x, self.y), exploration_target,
    #                           self.inference.is_safe, self.env.size)
    #         if path and self.is_move_safe(path[0]):
    #             self.move_to(path[0])
    #             return "MOVE"

    #     # If no safe moves available and no gold, try to go back to start
    #     if not self.has_gold and (self.x, self.y) != (0, 0):
    #         path_home = astar_search((self.x, self.y), (0, 0),
    #                                self.inference.is_safe, self.env.size)
    #         if path_home and self.is_move_safe(path_home[0]):
    #             self.move_to(path_home[0])
    #             return "MOVE"


    #     if percepts["breeze"]:
    #         self._handle_breeze_situation()

    #     # No safe moves available
    #     return "STAY"

    # ======== STEP ======== #
    def step(self):
        if self.escaped or self.dead:
            return "STAY"

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
            path_home = astar_search((self.x, self.y), (0, 0),
                                     self.inference.is_safe, self.env.size)
            if path_home:
                next_pos = path_home[0]
                target_dir = self.get_direction_to(next_pos)
                if self.direction != target_dir:
                    return self.turn_towards(target_dir)  # xoay trước
                if self.is_move_safe(next_pos):
                    self.move_to(next_pos)
                    return "MOVE"
                return "STUCK"
            return "STUCK"

        # ---- SHOOT WUMPUS ----
        if self.has_arrow and percepts["stench"] and self.can_shoot_wumpus_safely():
            target_dir = self.get_wumpus_direction()
            if target_dir and self.direction != target_dir:
                return self.turn_towards(target_dir)  # xoay trước khi bắn
            result = self.env.shoot_arrow()
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
            best_neighbor = self.choose_best_neighbor(safe_neighbors)
            target_dir = self.get_direction_to(best_neighbor)
            if self.direction != target_dir:
                return self.turn_towards(target_dir)  # xoay trước khi đi
            self.move_to(best_neighbor)
            return "MOVE"

        # ---- EXPLORE SAFE UNKNOWN ----
        exploration_target = self.find_safe_exploration_target()
        if exploration_target:
            path = astar_search((self.x, self.y), exploration_target,
                                self.inference.is_safe, self.env.size)
            if path:
                target_dir = self.get_direction_to(path[0])
                if self.direction != target_dir:
                    return self.turn_towards(target_dir)
                if self.is_move_safe(path[0]):
                    self.move_to(path[0])
                    return "MOVE"

        # ---- RETURN HOME IF NOTHING ELSE ----
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

        # ---- HANDLE BREEZE ----
        if percepts["breeze"]:
            self._handle_breeze_situation()

        return "STAY"


    def check_death(self):
        """Check if agent is in a deadly cell"""
        current_cell = self.env.grid[self.y][self.x]  # Note: grid[y][x] format
        return current_cell.pit or current_cell.wumpus

    def is_move_safe(self, next_pos):
        next_x, next_y = next_pos
        
        # Kiểm tra giới hạn
        if not (0 <= next_x < self.env.size and 0 <= next_y < self.env.size):
            return False
            
        # Kiểm tra trực tiếp từ environment
        next_cell = self.env.grid[next_y][next_x]
        if next_cell.pit or next_cell.wumpus:
            return False
            
        # Kiểm tra từ inference
        kb_info = self.inference.kb.get((next_x, next_y), {})
        
        # Không an toàn nếu:
        # - Là confirmed pit
        # - Hoặc chưa visited và có possible pit
        if (next_x, next_y) in self.inference.confirmed_pits:
            return False
            
        if not kb_info.get('visited', False) and kb_info.get('possible_pit', False):
            return False
            
        return True

    def get_truly_safe_neighbors(self):
        """Get neighbors that are definitely safe"""
        neighbors = get_neighbors((self.x, self.y), self.env.size)
        safe_neighbors = []
        
        for pos in neighbors:
            if (self.is_move_safe(pos) and 
                not self.inference.kb.get(pos, {}).get('visited', False)):
                safe_neighbors.append(pos)
        
        return safe_neighbors

    def choose_best_neighbor(self, safe_neighbors):
        """Choose the best neighbor to explore"""
        if not safe_neighbors:
            return None
            
        # Prefer neighbors that are closer to the center for better exploration
        center = (self.env.size // 2, self.env.size // 2)
        return min(safe_neighbors, key=lambda pos: heuristic(pos, center))

    def find_safe_exploration_target(self):
        """Find a safe unexplored cell to target"""
        for x in range(self.env.size):
            for y in range(self.env.size):
                pos = (x, y)
                kb_info = self.inference.kb.get(pos, {})
                if (not kb_info.get('visited', False) and 
                    self.inference.is_safe(pos) and
                    self.is_move_safe(pos)):
                    return pos
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
        """Move agent to next position"""
        # Double-check safety before moving
        if not self.is_move_safe(next_pos):
            print(f"[AGENT] Warning: Attempting unsafe move to {next_pos}")
            return False
            
        old_pos = (self.x, self.y)
        self.x, self.y = next_pos
        self.path.append(next_pos)
        
        result = self.env.move_agent(self.x, self.y)
        self.action_log.append(f"MOVE to {next_pos}")
        self.point -= 1
        
        # Check for death after moving
        if self.check_death():
            self.dead = True
            self.point -= 1000
            print(f"[AGENT] Agent died moving from {old_pos} to {next_pos}")
            
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
                path = astar_search((self.x, self.y), safe_retreat,
                                self.inference.is_safe, self.env.size)
                if path:
                    return self._execute_move(path[0])
        
        # Ưu tiên 3: Thử di chuyển đến ô có ít possible pits xung quanh nhất
        safe_moves = self._get_safest_possible_moves()
        if safe_moves:
            return self._execute_move(safe_moves[0][0])
        
        # Cuối cùng: Thử quay về (0,0)
        if (self.x, self.y) != (0, 0):
            path_home = astar_search((self.x, self.y), (0, 0),
                                self.inference.is_safe, self.env.size)
            if path_home:
                return self._execute_move(path_home[0])
            

    def _get_safest_possible_moves(self):
        from .utils import get_neighbors
        
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
                percepts = self.env.get_percepts(pos[0], pos[1])
                if not percepts.get('breeze', False):
                    visited_safe.append(pos)
        
        if not visited_safe:
            return None
            
        # Tìm ô gần nhất
        return min(visited_safe, key=lambda p: heuristic((self.x, self.y), p))


    def find_path_avoiding_pits(self, pits):
        from .planner import astar_search

        def is_safe_but_avoid_pits(pos):
            if pos in pits:
                return False
            return self.inference.is_safe(pos)

        return astar_search((self.x, self.y), (0, 0), is_safe_but_avoid_pits, self.env.size)

    def find_safest_path(self, possible_pits):
        from .planner import astar_search
        
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
            current_path = astar_search((self.x, self.y), target,
                                    self.inference.is_safe, self.env.size)
            if current_path:
                current_cost = sum(safety_cost(p) for p in current_path)
                if current_cost < min_cost:
                    min_cost = current_cost
                    path = current_path
        
        # Nếu không tìm được, thử về (0,0)
        if not path:
            path = astar_search((self.x, self.y), (0, 0),
                            self.inference.is_safe, self.env.size)
        return path
from .utils_random import get_neighbors
from .planner_random import dfs_search
import random

class AgentRandom:
    """
    Agent DFS random — dựa trên file agent gốc của bạn nhưng đổi chiến lược thăm:
    - Dùng DFS (stack = self.path) để khám phá
    - Randomize thứ tự neighbors để hành vi "đi đại"
    - Giữ nguyên logic grab/shoot/climb và update inference
    """
    def __init__(self, env, inference):
        self.env = env
        self.inference = inference
        self.x, self.y = 0, 0
        self.direction = "EAST"
        self.has_gold = False
        self.has_arrow = True
        self.point = 0
        # path dùng như stack: path[-1] == current
        self.path = [(0, 0)]
        self.visited = set([(0, 0)])
        self.action_log = []
        self.escaped = False
        self.dead = False
        # tránh back-and-forth bằng prev_pos
        self.prev_pos = None
        self.plan = []

    # ======== HÀM XOAY ======== #
    def turn_left(self):
        dirs = ["NORTH", "WEST", "SOUTH", "EAST"]
        idx = dirs.index(self.direction)
        self.direction = dirs[(idx + 1) % 4]
        # optional debug print
        # print(f"[AGENT] Turned left to {self.direction}")
        self.action_log.append("TURN_LEFT")
        return "TURN_LEFT"

    def turn_right(self):
        dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
        idx = dirs.index(self.direction)
        self.direction = dirs[(idx + 1) % 4]
        # print(f"[AGENT] Turned right to {self.direction}")
        self.action_log.append("TURN_RIGHT")
        return "TURN_RIGHT"

    def turn_towards(self, target_dir):
        """Chỉ xoay trái hoặc phải 1 bước mỗi lượt"""
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

    # ======== STEP ======== #
    def step(self):
        if self.escaped or self.dead:
            return "STAY"

        if self.check_death():
            self.dead = True
            self.point -= 1000
            return "DIE"

        percepts = self.env.get_percepts(self.x, self.y)
        try:
            self.inference.update_knowledge(
                (self.x, self.y),
                percepts,
                action_count=len(self.action_log),
                agent_pos=(self.x, self.y)
            )
        except TypeError:
            self.inference.update_knowledge((self.x, self.y), percepts)

        # Nhặt vàng
        if percepts.get('glitter', False) and not self.has_gold:
            self.has_gold = True
            self.point += 1000
            return "GRAB"

        # Nếu có vàng → về nhà
        if self.has_gold and (self.x, self.y) == (0, 0):
            self.escaped = True
            self.point += 1000
            return "CLIMB"

        # Bắn Wumpus nếu ngay trước mặt
        if self.has_arrow and percepts.get('stench', False):
            target = self.get_position_in_direction(self.direction)
            if self.is_wumpus_ahead(target):
                self.has_arrow = False
                killed = self.env.shoot_arrow(self.x, self.y, self.direction)
                if killed:
                    self.inference.mark_wumpus_dead(target)
                return "SHOOT"

        if self.plan:
            next_pos = self.plan.pop(0)
            target_dir = self.get_direction_to(next_pos)
            if self.direction != target_dir:
                return self.turn_towards(target_dir)
            moved = self.move_to(next_pos)
            if moved:
                self.visited.add(next_pos)
            return "MOVE" if moved else "STUCK"


        all_safe_unvisited = [
            (x, y)
            for x in range(self.env.size)
            for y in range(self.env.size)
            if self.is_move_safe((x, y)) and (x, y) not in self.visited
        ]
        if all_safe_unvisited:
            goal = random.choice(all_safe_unvisited)
            path = dfs_search(
                (self.x, self.y),
                goal,
                lambda pos: [
                    n for n in get_neighbors(pos, self.env.size)
                    if self.is_move_safe(n)
                ]
            )
            if path:
            
                self.plan = path[1:]
                return self.step()

      
        return "STAY"

    def check_death(self):
        current_cell = self.env.grid[self.y][self.x]
        return current_cell.pit or current_cell.wumpus

    def is_move_safe(self, next_pos):
        next_x, next_y = next_pos

        # Kiểm tra giới hạn
        if not (0 <= next_x < self.env.size and 0 <= next_y < self.env.size):
            return False

        # Kiểm tra từ inference
        kb_info = self.inference.kb.get((next_x, next_y), {})

        if (next_x, next_y) in self.inference.confirmed_pits:
            return False
        if (next_x, next_y) in self.inference.confirmed_wumpus:
            return False

        # nếu đã thăm thì coi là an toàn
        if kb_info.get('visited', False):
            return True
        # nếu inference đồng ý an toàn thì ok
        try:
            return self.inference.is_safe((next_x, next_y))
        except Exception:
            # fallback: nếu không có is_safe, dùng flags
            if not kb_info.get('possible_pit', False) and not kb_info.get('possible_wumpus', False):
                return True
        return False

    def get_truly_safe_neighbors(self):
        neighbors = get_neighbors((self.x, self.y), self.env.size)
        safe_neighbors = []
        for pos in neighbors:
            if self.is_move_safe(pos):
                safe_neighbors.append(pos)
                # giữ tương thích: mark neighbors of pos safe
                try:
                    self.inference.mark_safe_and_neighbors(pos)
                except Exception:
                    pass
        return safe_neighbors


    def find_safe_exploration_target(self):
        for x in range(self.env.size):
            for y in range(self.env.size):
                pos = (x, y)
                kb_info = self.inference.kb.get(pos, {})
                if (not kb_info.get('visited', False) and 
                    (self.inference.is_safe(pos) if hasattr(self.inference, 'is_safe') else True) and
                    self.is_move_safe(pos)):
                    return pos
        return None

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
        # Double-check safety before moving
        if not self.is_move_safe(next_pos):
            # print(f"[AGENT] Warning: Attempting unsafe move to {next_pos}")
            self.action_log.append(f"BLOCKED {next_pos}")
            return False

        old_pos = (self.x, self.y)
        self.x, self.y = next_pos
        # nếu moved vào ô chưa xuất hiện trên stack thì thêm; trong DFS core đã push trước
        if not self.path or self.path[-1] != next_pos:
            self.path.append(next_pos)
        self.prev_pos = old_pos

        result = self.env.move_agent(self.x, self.y)
        self.action_log.append(f"MOVE to {next_pos}")
        self.point -= 1

        if result.get("eaten", False):
            self.dead = True
            return False

        if self.check_death():
            self.dead = True
            self.point -= 1000
            # print(f"[AGENT] Agent died moving from {old_pos} to {next_pos}")
            return False

        return True

    def finished(self):
        return self.escaped or self.dead

    # helper: đếm neighbors chưa khám phá dùng để ưu tiên fallback moves
    def count_unexplored_neighbors(self, pos):
        neighbors = get_neighbors(pos, self.env.size)
        count = 0
        for n in neighbors:
            kb = self.inference.kb.get(n, {})
            if not kb.get('visited', False) and self.is_move_safe(n):
                count += 1
        return count

    # Keep other helper methods used by original agent (breeze handling, find_path_avoiding_pits, etc.)
    # but it's optional for DFS behavior — you can keep original implementations if present.

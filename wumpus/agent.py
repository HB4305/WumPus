from .utils import get_neighbors
from .environment import Environment

class Agent:
    def __init__(self, env, inference_engine):
        self.x, self.y = 0, 0
        self.orientation = "EAST"
        self.env = env
        self.inference = inference_engine
        self.has_gold = False
        self.visited = set()
        self.path = []
        self.position = (0, 0)
        self.point = 0

    def step(self):
        percepts = self.env.get_percepts(self.x, self.y)
        print(f"[DEBUG] Percepts at ({self.x}, {self.y}): {percepts}")
        self.inference.update_knowledge((self.x, self.y), percepts)

        if percepts["glitter"]:
            self.take_action('Grab Gold')
            print("Gold grabbed at", (self.x, self.y))
            return "GRAB"

        # Tìm ô an toàn chưa đi
        safe_neighbors = [n for n in get_neighbors((self.x, self.y), self.inference.size) if self.inference.is_safe(n)]
        print(f"[DEBUG] Safe neighbors from ({self.x}, {self.y}) --> {safe_neighbors}")
        # for nx, ny in safe_neighbors:
        #     if (nx, ny) not in self.visited:
        #         print(f"[AGENT] Moving to {(nx, ny)}")
        #         self.position = (nx, ny)
        #         self.path.append((nx, ny))         # ghi lại đường đi
        #         self.visited.add((nx, ny))         # đánh dấu đã đến
        #         return f"MOVE to {(nx, ny)}"
        
        if safe_neighbors:
            next_pos = safe_neighbors[0]
            self.position = next_pos
            self.x, self.y = next_pos  # ✅ Thêm dòng này để cập nhật vị trí thực
            self.visited.add(next_pos)
            self.path.append(next_pos)
            self.take_action('Move Forward')  # ✅ Thực hiện hành động thật sự
            return f"MOVE to {next_pos}"

        # Không còn ô an toàn → xem có nên bắn
        wumpus_locs = self.inference.get_possible_wumpus()
        certain_wumpus = [loc for loc in wumpus_locs if self.inference.is_wumpus_certain(loc)]

        if certain_wumpus:
            wx, wy = certain_wumpus[0]
            if self.can_shoot(wx, wy):
                self.take_action('Shoot')
                print("Shot arrow at", (wx, wy))
                return f"SHOOT at {(wx, wy)}"

        return "STAY"

    def can_shoot(self, wx, wy):
        return self.x == wx or self.y == wy

    def take_action(self, action):
        if action == 'Move Forward':
            self.point -= 1
        elif action == 'Grab Gold':
            self.has_gold = True
            self.point += 1000
        elif action == 'Shoot':
            self.shoot_arrow()
            self.point -= 10
        elif action == 'Climb':
            if self.has_gold:
                self.point += 0  # Bạn có thể cộng thêm điểm nếu muốn

    def shoot_arrow(self):
        # Placeholder: Gọi sang inference để xử lý Wumpus bị bắn
        pass

    def finished(self):
        return self.has_gold and (self.x, self.y) == (0, 0)
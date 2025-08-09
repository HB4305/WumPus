import random
from wumpus.environment import Environment
from wumpus.utils import get_neighbors

class EnvironmentAdvanced(Environment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action_count = 0
        # Giả sử self.wumpus_positions = [(x1,y1), (x2,y2), ...]
    
    def _increment_action_and_move_wumpus(self):
        self.action_count += 1
        if self.action_count % 5 == 0:
            self.move_wumpuses()
            # Trả về True nếu agent bị Wumpus ăn
            if (self.agent_x, self.agent_y) in self.wumpus_positions:
                return True
        return False

    def move_agent(self, x, y):
        self.agent_x, self.agent_y = x, y  # Lưu vị trí agent trong môi trường
        result = super().move_agent(x, y)
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
        return result, eaten

    def shoot_arrow(self, direction):
        result = super().shoot_arrow(direction)
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
        return result, eaten

    def grab_gold(self):
        result = super().grab_gold()
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
        return result, eaten

    def climb_out(self):
        result = super().climb_out()
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
        return result, eaten

    def turn_agent(self, *args, **kwargs):
        result = super().turn_agent(*args, **kwargs)
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
        return result, eaten

    def move_wumpuses(self):
        new_positions = []
        for (wx, wy) in self.wumpus_positions:
            neighbors = self.get_valid_wumpus_moves(wx, wy)
            if neighbors:
                chosen_pos = random.choice(neighbors)
            else:
                chosen_pos = (wx, wy)
            new_positions.append(chosen_pos)
        
        # Xoá stench cũ 
        for (wx, wy) in self.wumpus_positions:
            for nx, ny in get_neighbors((wx, wy), self.size):
                self.grid[ny][nx].stench = False

        self.wumpus_positions = new_positions

        # In ra vị trí mới của Wumpus
        print(f"[ENV_ADVANCED] Wumpus moved to: {new_positions}")

        for (wx, wy) in new_positions:
            self.grid[wy][wx].wumpus = True
            for nx, ny in get_neighbors((wx, wy), self.size):
                self.grid[ny][nx].stench = True

    def get_valid_wumpus_moves(self, x, y):
        candidates = []
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if not (0 <= nx < self.size and 0 <= ny < self.size):
                continue
            if (nx, ny) in self.wumpus_positions:
                continue
            cell = self.grid[ny][nx]
            if cell.pit:
                continue
            candidates.append((nx, ny))
        return candidates

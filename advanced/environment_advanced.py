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
            print(f"[ENV_ADVANCED] Action count {self.action_count}: Moving Wumpuses...")
            if (self.agent_x, self.agent_y) in self.wumpus_positions:
                return True
        return False
    def move_agent(self, x, y):
        self.agent_x, self.agent_y = x, y
        result = super().move_agent(x, y)
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
            result["eaten"] = True  # Add eaten flag to result dict
        return result  # Return single dict instead of tuple

    def shoot_arrow(self, direction):
        result = super().shoot_arrow(direction)
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
            result["eaten"] = True
        return result

    def grab_gold(self):
        result = super().grab_gold()
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
            result["eaten"] = True
        return result

    def climb_out(self):
        result = super().climb_out()
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
            result["eaten"] = True
        return result
    

    def turn_agent(self, *args, **kwargs):
        result = super().turn_agent(*args, **kwargs)
        eaten = self._increment_action_and_move_wumpus()
        if eaten:
            print("[ENV_ADVANCED] Agent bị Wumpus ăn khi Wumpus di chuyển!")
        return result, eaten

    def move_wumpuses(self):
         # Xoá Wumpus cũ từ grid trước
        for (wx, wy) in self.wumpus_positions:
            if 0 <= wx < self.size and 0 <= wy < self.size:
                self.grid[wy][wx].wumpus = False
                print(f"[ENV_ADVANCED] Removed Wumpus from ({wx}, {wy})")
        
                # Xóa tất cả stench cũ trước khi tính toán lại
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].stench = False
        
        
        new_positions = []
        for i, (wx, wy) in enumerate(self.wumpus_positions):
            neighbors = self.get_valid_wumpus_moves(wx, wy)
            if neighbors:
                chosen_pos = random.choice(neighbors)
                print(f"[ENV_ADVANCED] Wumpus {i} moved from ({wx}, {wy}) to {chosen_pos}")
            else:
                chosen_pos = (wx, wy)
                print(f"[ENV_ADVANCED] Wumpus {i} stayed at ({wx}, {wy}) - no valid moves")
            new_positions.append(chosen_pos)
        # # Xoá stench cũ 
        # for (wx, wy) in self.wumpus_positions:
        #     for nx, ny in get_neighbors((wx, wy), self.size):
        #         self.grid[ny][nx].stench = False

        self.wumpus_positions = new_positions

        # In ra vị trí mới của Wumpus
        print(f"[ENV_ADVANCED] Wumpus moved to: {new_positions}")

        # for (wx, wy) in new_positions:
        #     self.grid[wy][wx].wumpus = True
        #     for nx, ny in get_neighbors((wx, wy), self.size):
        #         self.grid[ny][nx].stench = True
        for (wx, wy) in new_positions:
            if 0 <= wx < self.size and 0 <= wy < self.size:
                self.grid[wy][wx].wumpus = True
                for nx, ny in get_neighbors((wx, wy), self.size):
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        self.grid[ny][nx].stench = True
                        
        print("[ENV_ADVANCED] Grid state after Wumpus movement:")
        for y in range(self.size):
            for x in range(self.size):
                cell = self.grid[y][x]
                if cell.wumpus:
                    print(f"  Wumpus at ({x}, {y})")
                if cell.stench:
                    print(f"  Stench at ({x}, {y})")

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

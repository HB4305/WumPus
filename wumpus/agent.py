from .planner import astar_search
from .algorithm import heuristic

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

    def step(self):
        if self.escaped or self.dead:
            return "STAY"

        # Check if agent died BEFORE taking action
        if self.check_death():
            self.dead = True
            self.point -= 1000
            return "DIE"

        # Get current percepts and update knowledge
        percepts = self.env.get_percepts(self.x, self.y)
        self.inference.update_knowledge((self.x, self.y), percepts)

        # If found gold, grab it
        if percepts["glitter"] and not self.has_gold:
            self.has_gold = True
            result = self.env.grab_gold()
            self.action_log.append("GRAB")
            self.point += 10
            return "GRAB"

        # If has gold and at start, climb out
        if self.has_gold and (self.x, self.y) == (0, 0):
            result = self.env.climb_out()
            self.escaped = result["escaped"]
            self.action_log.append("CLIMB")
            if self.escaped:
                self.point += 1000
            return "CLIMB"

        # If has gold, go home
        if self.has_gold:
            path_home = astar_search((self.x, self.y), (0, 0), 
                                   self.inference.is_safe, self.env.size)
            if path_home:
                next_pos = path_home[0]
                if self.is_move_safe(next_pos):
                    self.move_to(next_pos)
                    return "MOVE"
                else:
                    return "STUCK"
            else:
                return "STUCK"

        # Try to shoot wumpus if possible and beneficial
        if (self.has_arrow and percepts["stench"] and 
            self.can_shoot_wumpus_safely()):
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

        # Look for safe unvisited neighbors
        safe_neighbors = self.get_truly_safe_neighbors()
        if safe_neighbors:
            # Choose the best neighbor (closest to center or unexplored)
            best_neighbor = self.choose_best_neighbor(safe_neighbors)
            self.move_to(best_neighbor)
            return "MOVE"

        # Find path to safe unexplored area
        exploration_target = self.find_safe_exploration_target()
        if exploration_target:
            path = astar_search((self.x, self.y), exploration_target,
                              self.inference.is_safe, self.env.size)
            if path and self.is_move_safe(path[0]):
                self.move_to(path[0])
                return "MOVE"

        # If no safe moves available and no gold, try to go back to start
        if not self.has_gold and (self.x, self.y) != (0, 0):
            path_home = astar_search((self.x, self.y), (0, 0),
                                   self.inference.is_safe, self.env.size)
            if path_home and self.is_move_safe(path_home[0]):
                self.move_to(path_home[0])
                return "MOVE"

        # No safe moves available
        return "STAY"

    def check_death(self):
        """Check if agent is in a deadly cell"""
        current_cell = self.env.grid[self.y][self.x]  # Note: grid[y][x] format
        return current_cell.pit or current_cell.wumpus

    def is_move_safe(self, next_pos):
        """Check if moving to next_pos would be safe"""
        next_x, next_y = next_pos
        
        # Check bounds
        if not (0 <= next_x < self.env.size and 0 <= next_y < self.env.size):
            return False
            
        # Check if cell has known dangers
        next_cell = self.env.grid[next_y][next_x]  # Note: grid[y][x] format
        if next_cell.pit or next_cell.wumpus:
            return False
            
        # Check inference knowledge
        return self.inference.is_safe(next_pos)

    def get_truly_safe_neighbors(self):
        """Get neighbors that are definitely safe"""
        from .utils import get_neighbors
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
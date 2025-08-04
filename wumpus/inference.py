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
        
        # Current position is safe (agent is there)
        self.kb[(x, y)]['visited'] = True
        self.kb[(x, y)]['safe'] = True
        self.kb[(x, y)]['possible_pit'] = False
        self.kb[(x, y)]['possible_wumpus'] = False
        
        # Store percept
        self.percepts[(x, y)] = percept
        neighbors = get_neighbors((x, y), self.size)

        # Process breeze
        if not percept['breeze']:
            # No breeze means no pits in adjacent cells
            for nx, ny in neighbors:
                self._ensure_kb((nx, ny))
                self.kb[(nx, ny)]['possible_pit'] = False
        else:
            # There is breeze, so at least one adjacent cell has a pit
            self._mark_possible_danger(neighbors, 'possible_pit')

        # Process stench
        if not percept['stench']:
            # No stench means no wumpus in adjacent cells
            for nx, ny in neighbors:
                self._ensure_kb((nx, ny))
                self.kb[(nx, ny)]['possible_wumpus'] = False
        else:
            # There is stench, so at least one adjacent cell has wumpus
            self._mark_possible_danger(neighbors, 'possible_wumpus')

        # Update safety status
        self._update_safety()

    def _mark_possible_danger(self, neighbors, danger_type):
        """Mark neighbors as possibly dangerous if not already ruled out"""
        unvisited_neighbors = []
        for nx, ny in neighbors:
            self._ensure_kb((nx, ny))
            if not self.kb[(nx, ny)]['visited'] and not self.kb[(nx, ny)]['safe']:
                unvisited_neighbors.append((nx, ny))
        
        # Mark all unvisited neighbors as possibly dangerous
        for pos in unvisited_neighbors:
            if not self.kb[pos]['visited']:
                self.kb[pos][danger_type] = True
                self.kb[pos]['safe'] = False
        
        # If only one unvisited neighbor, it must have the danger
        if len(unvisited_neighbors) == 1:
            pos = unvisited_neighbors[0]
            self.kb[pos][danger_type] = True
            self.kb[pos]['safe'] = False

    def _update_safety(self):
        """Update safety status for all positions"""
        for pos, facts in self.kb.items():
            if facts['visited']:
                continue
            
            # A cell is safe only if it's definitely not dangerous
            if not facts['possible_pit'] and not facts['possible_wumpus']:
                self.kb[pos]['safe'] = True
            else:
                self.kb[pos]['safe'] = False

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
        facts = self.kb[pos]
        # Only consider safe if visited OR definitely safe (no possible dangers)
        return facts['visited'] or (facts['safe'] and not facts['possible_pit'] and not facts['possible_wumpus'])

    def is_definitely_safe(self, pos):
        """More strict safety check for pathfinding"""
        self._ensure_kb(pos)
        facts = self.kb[pos]
        return facts['visited'] or (not facts['possible_pit'] and not facts['possible_wumpus'])

    def get_safe_unvisited_neighbors(self, current_pos):
        neighbors = get_neighbors(current_pos, self.size)
        safe_neighbors = []
        for pos in neighbors:
            if self.is_definitely_safe(pos) and not self.kb.get(pos, {}).get('visited', False):
                safe_neighbors.append(pos)
        return safe_neighbors

    def get_kb(self):
        return self.kb
    
    def get_possible_wumpus(self):
        return [pos for pos, facts in self.kb.items() if facts.get('possible_wumpus', False)]

    def is_wumpus_certain(self, pos):
        # Simple heuristic: if only one possible wumpus location near stench
        return self.kb.get(pos, {}).get('possible_wumpus', False)
#         self.escaped = False

#     def step(self):
#         if self.escaped:
#             return "Already escaped."

#         percepts = self.env.get_percepts(self.x, self.y)
#         self.inference.update_knowledge((self.x, self.y), percepts)

#         # Nếu có gold => grab
#         if percepts["glitter"] and not self.has_gold:
#             self.has_gold = True
#             result = self.env.grab_gold()
#             self.action_log.append("GRAB")
#             return "Grabbed gold."

#         # Nếu có gold và đang ở (0,0) => climb ra
#         if self.has_gold and (self.x, self.y) == (0, 0):
#             result = self.env.climb_out()
#             self.escaped = result["escaped"]
#             self.action_log.append("CLIMB")
#             return "Climbed out with gold!" if self.escaped else "Climb failed."

#         # Nếu có gold, lên kế hoạch quay về (0,0)
#         if self.has_gold:
#             path_home = astar_search((self.x, self.y), (0, 0), self.inference.is_safe, self.env.size)
#             if path_home:
#                 next_move = path_home[0]
#                 self.move_to(next_move)
#                 return f"Move home to {next_move}"
#             else:
#                 return "No path home!"

#         # Nếu chưa có gold, tìm ô an toàn để đi tới
#         targets = self.inference.get_safe_unvisited_neighbors((self.x, self.y))
#         if targets:
#             target = targets[0]
#             path = astar_search((self.x, self.y), target, self.inference.is_safe, self.env.size)
#             if path:
#                 next_move = path[0]
#                 self.move_to(next_move)
#                 return f"Move to safe cell {next_move}"

#         # Nếu không còn ô an toàn để đi và chưa có gold
#         return "Stuck. No safe moves."

#     def move_to(self, next_pos):
#         self.x, self.y = next_pos
#         self.path.append(next_pos)
#         self.env.move_agent(self.x, self.y)
#         self.action_log.append(f"MOVE to {next_pos}")

    def can_shoot_wumpus(self, agent_pos, agent_dir):
        """Check if agent can shoot wumpus in current direction"""
        x, y = agent_pos
        dx, dy = {
            "NORTH": (0, 1),
            "EAST": (1, 0), 
            "SOUTH": (0, -1),
            "WEST": (-1, 0)
        }.get(agent_dir, (0, 0))
        
        # Check if there's a wumpus in the shooting line
        current_x, current_y = x + dx, y + dy
        while 0 <= current_x < self.size and 0 <= current_y < self.size:
            if self.kb.get((current_x, current_y), {}).get('possible_wumpus', False):
                return True
            current_x += dx
            current_y += dy
        return False

    def remove_wumpus_after_kill(self, agent_pos, agent_dir):
        """Remove wumpus from KB after successful kill"""
        x, y = agent_pos
        dx, dy = {
            "NORTH": (0, 1),
            "EAST": (1, 0),
            "SOUTH": (0, -1), 
            "WEST": (-1, 0)
        }.get(agent_dir, (0, 0))
        
        current_x, current_y = x + dx, y + dy
        while 0 <= current_x < self.size and 0 <= current_y < self.size:
            pos = (current_x, current_y)
            if pos in self.kb and self.kb[pos].get('possible_wumpus', False):
                self.kb[pos]['possible_wumpus'] = False
                self.kb[pos]['safe'] = True
                # Update neighbors that no longer have stench
                for neighbor in get_neighbors(pos, self.size):
                    self._ensure_kb(neighbor)
                break
            current_x += dx
            current_y += dy
        
        self._update_safety()



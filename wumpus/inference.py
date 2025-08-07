from collections import defaultdict
from .utils import get_neighbors

class Inference:
    def __init__(self, size):
        self.size = size
        self.kb = defaultdict(lambda: {
            'visited': False,
            'safe': False,
            'possible_pit': False,
            'possible_wumpus': False
        })
        self.percepts = {}
        self.confirmed_pits = set()
        self.confirmed_no_pits = set()  # Theo dõi ô chắc chắn không có pit
        self.breeze_cells = set()
        self.confirmed_no_pits = set()

    def update_knowledge(self, position, percept):
        x, y = position
        cell = self.kb[(x, y)]
        
        # Cập nhật trạng thái ô hiện tại
        cell.update({
            'visited': True,
            'safe': True,
            'possible_pit': False,
            'possible_wumpus': False
        })
        
        # Lưu percept
        self.percepts[(x, y)] = percept
        neighbors = get_neighbors((x, y), self.size)

        # Xử lý pit (breeze)
        self._process_pit_info((x, y), percept['breeze'], neighbors)
        
        # Xử lý Wumpus (stench)
        self._process_wumpus_info((x, y), percept['stench'], neighbors)

        # Cập nhật trạng thái an toàn
        self._update_safety()

    def _process_wumpus_info(self, position, has_stench, neighbors):
        """Xử lý thông tin Wumpus từ stench"""
        x, y = position
        
        if not has_stench:
            # Không có stench => các ô lân cận không có Wumpus
            for nx, ny in neighbors:
                self.kb[(nx, ny)]['possible_wumpus'] = False
        else:
            # Có stench => ít nhất một ô lân cận có Wumpus
            unvisited = [pos for pos in neighbors if not self.kb[pos]['visited']]
            
            if len(unvisited) == 1:
                # Nếu chỉ có 1 ô chưa visited, đó chính là Wumpus
                wumpus_pos = unvisited[0]
                self.kb[wumpus_pos].update({
                    'possible_wumpus': True,
                    'safe': False
                })

    def _process_pit_info(self, position, has_breeze, neighbors):
        x, y = position

        if has_breeze:
            self.breeze_cells.add((x, y))  

        if not has_breeze:
            # Không có breeze => các ô lân cận an toàn
            for nx, ny in neighbors:
                if not self.kb[(nx, ny)]['visited']:
                    self.kb[(nx, ny)]['possible_pit'] = False
                    self.kb[(nx, ny)]['safe'] = True
                    self.confirmed_no_pits.add((nx, ny))
            return

        # Có breeze => ít nhất 1 ô xung quanh là pit
        unvisited = [pos for pos in neighbors if not self.kb[pos]['visited']]

        # Nếu chỉ có 1 ô chưa biết, đó chắc chắn là pit
        if len(unvisited) == 1:
            pit_pos = unvisited[0]
            self._confirm_pit(pit_pos)
            return

        # Tạm đánh dấu các ô chưa biết là "possible pit" (nếu chưa bị loại trừ)
        for pos in unvisited:
            if pos not in self.confirmed_no_pits and not self.kb[pos].get('confirmed_pit', False):
                self.kb[pos]['possible_pit'] = True
                self.kb[pos]['safe'] = False

        # Gọi inference nâng cao (kiểm tra nhiều breeze để xác định pit)
        self._advanced_pit_inference()



    def _advanced_pit_inference(self):
        from collections import defaultdict
        
        # Tạo bản đồ các ô có thể là pit và số breeze chúng giải thích
        pit_candidates = defaultdict(int)
        breeze_positions = [pos for pos, percept in self.percepts.items() if percept['breeze']]
        
        for pos in self.get_possible_pits():
            for breeze_pos in breeze_positions:
                if pos in get_neighbors(breeze_pos, self.size):
                    pit_candidates[pos] += 1
        
        # Tìm ô giải thích được nhiều breeze nhất
        if pit_candidates:
            best_pit = max(pit_candidates.items(), key=lambda x: x[1])[0]
            if pit_candidates[best_pit] == len(breeze_positions):
                self._confirm_pit(best_pit)

    def _confirm_pit(self, pos):
        """Xác nhận ô có pit"""
        self.confirmed_pits.add(pos)
        self.kb[pos].update({
            'possible_pit': True,
            'safe': False
        })
        # Các ô lân cận không còn là possible pit (vì mỗi breeze chỉ cần 1 pit)
        for neighbor in get_neighbors(pos, self.size):
            if neighbor != pos and neighbor not in self.confirmed_pits:
                self.kb[neighbor]['possible_pit'] = False
                self.confirmed_no_pits.add(neighbor)


    def _pit_explains_all_breeze(self, pit_pos):
        """Kiểm tra nếu pit ở vị trí này có thể giải thích tất cả breeze đã quan sát"""
        for pos, percept in self.percepts.items():
            if percept['breeze']:
                neighbors = get_neighbors(pos, self.size)
                if pit_pos not in neighbors:
                    # Có breeze mà pit này không giải thích được
                    return False
        return True

    def _cross_check_pits(self):
        """Sử dụng tất cả percepts breeze để xác định pit chính xác hơn"""
        possible_pits = self.get_possible_pits()
        
        # Tìm các ô có thể là pit dựa trên tất cả breeze đã quan sát
        for pos in possible_pits:
            is_possible = True
            for (px, py), percept in self.percepts.items():
                if percept['breeze']:
                    # Pit phải giải thích được tất cả breeze
                    if pos not in get_neighbors((px, py), self.size):
                        is_possible = False
                        break
            
            if is_possible:
                # Nếu ô này giải thích được tất cả breeze, xác nhận là pit
                self._confirm_pit(pos)
                # Sau khi xác nhận 1 pit, các ô khác không cần xét nữa
                break

    def is_pit_certain(self, pos):
        """Kiểm tra chắc chắn có pit tại vị trí"""
        return pos in self.confirmed_pits

    def get_possible_pits(self):
        """Lấy danh sách các ô có thể có pit"""
        return [pos for pos, facts in self.kb.items() 
                if facts['possible_pit'] and not facts['visited']]
    

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
        """Cập nhật trạng thái an toàn cho tất cả ô"""
        for pos in self.kb:
            cell = self.kb[pos]
            if cell['visited']:
                cell['safe'] = True
            else:
                cell['safe'] = not (cell['possible_pit'] or cell['possible_wumpus'])

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



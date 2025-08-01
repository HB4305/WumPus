from algorithms.program import Program
from algorithms.a_star import a_star, create_graph
import copy
import heapq


# Agent class definition
# class Agent:
#     def __init__(self, map_size=10):
#         self.x = 0  # chi so cot hien tai cua agent
#         self.y = 0  # chi so hang hien tai cua agent
#         self.current_hp = 100  # luong mau default
#         #bỏ
#         self.map_size = map_size  # kich thuoc map hien tai
#         self.direction = (1, 0)

#         self.knowledge_base_pit_percept = []
#         self.knowledge_base_wumpus_percept = []
#         self.knowledge_base_poison_percept = [] # không liên quan
#         self.knowledge_base_health_percept = []  # bo cung duoc, k can thiet lam

#         self.maybe_wumpus = []  # check xem co the co wumpus trong o do khong
#         # bỏ
#         self.maybe_poison = []  # check xem co the co poison trong o do khong
#         self.maybe_pit = []  # check xem co the co pit trong o do khong
#         #bỏ 
#         self.maybe_health = []  # bo cung duoc, k can thiet lam

#         self.sure_wumpus = []  # check xem wumpus co chac trong o do khong
#         # bỏ
#         self.sure_poison = []  # check xem co poison trong do ko
#         self.sure_pit = []  # check xem co chac la pit trong do khong
#         # bỏ
#         self.sure_health = []  # bo cung duoc, k can thiet lam

#         #bỏ
#         self.healing_potion = 0  # so luong healing potion dang nam giu hien tai
#         self.point = 0  # so diem hien tai cua agent
#         self.path = []  # duong di cua agent

#         # action
#         self.grab_heal = []  # locations where healing potions were grabbed
#         self.grab_gold = []  # locations where golds were grabbed
#         self.heal = []  # locations where healing potions were used.
#         self.shoot_act = []  # shooting actions performed.

#     def check_have_wumpus(self, y, x, cell=None):
#         """
#         Check if a Wumpus might be present at the given coordinates.

#         Parameters:
#             y (int): Row index.
#             x (int): Column index.
#             cell (Cell): The cell to check for a stench, optional.

#         Returns:
#             bool: True if there might be a Wumpus at the given location, False otherwise.
#         """
#         if (y, x) == (0, 0):  # safe next cell, no wumpus at the starting position.
#             return False
#         if cell is not None:
#             if not cell.is_stench or (y, x) in self.path:
#                 return False
#         else:
#             if (y, x) in self.path:
#                 return False

#         # check neighboring cells to validate the posibility of a Wumpus.
#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for dy, dx in directions:
#             ny, nx = y + dy, x + dx
#             if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
#                 if (ny, nx) not in self.knowledge_base_wumpus_percept and (
#                     ny,
#                     nx,
#                 ) in self.path:
#                     return False
#         self.maybe_wumpus.append((y, x))  # potential wumpus location
#         return True

#     def check_have_pit(self, y, x, cell):
#         """
#         Check if a pit might be present at the given coordinates.

#         Parameters:
#             y (int): Row index.
#             x (int): Column index.
#             cell (Cell): The cell to check for a breeze.

#         Returns:
#             bool: True if there might be a pit at the given location, False otherwise.
#         """
#         if (y, x) == (
#             0,
#             0,
#         ):  # check next cell is safe -> no pit at the starting position.
#             return False  # no pit
#         if (
#             not cell.is_breeze or (y, x) in self.path
#         ):  # if the now cell (cell) is not breeze or the next cell is in the trace path
#             return False  # no pit
#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for dy, dx in directions:
#             ny, nx = y + dy, x + dx
#             if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
#                 if (ny, nx) not in self.knowledge_base_pit_percept and (
#                     ny,
#                     nx,
#                 ) in self.path:  # Kiểm tra nếu tọa độ mới (ny, nx) không nằm trong self.knowledge_base_pit_percept (tức là agent chưa biết rằng có hố tại vị trí này) và tọa độ này đã nằm trong self.path (tức là agent đã đi qua ô này trước đó).
#                     return False  # no pit
#         self.maybe_pit.append((y, x))
#         return True

#     def check_have_poison(self, y, x, cell):
#         """
#         Check if a poison gas might be present at the given coordinates.

#         Parameters:
#             y (int): Row index.
#             x (int): Column index.
#             cell (Cell): The cell to check for a whiff.

#         Returns:
#             bool: True if there might be poison gas at the given location, False otherwise.
#         """
#         if (y, x) == (0, 0):  # Safe zone, no poison gas at the starting position
#             return False  # no poison
#         if (
#             not cell.is_whiff or (y, x) in self.path
#         ):  # if the now cell is not whiff and the next cell is in the trace path
#             return False  # no poison
#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for dy, dx in directions:
#             ny, nx = y + dy, x + dx
#             if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
#                 if (ny, nx) not in self.knowledge_base_poison_percept and (
#                     ny,
#                     nx,
#                 ) in self.path:
#                     return False
#         self.maybe_poison.append((y, x))
#         return True

#     def check_have_healing(self, y, x, cell):
#         if not cell.is_glow or (y, x) in self.path:
#             return False
#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for dy, dx in directions:
#             ny, nx = y + dy, x + dx
#             if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
#                 if (ny, nx) not in self.knowledge_base_health_percept and (
#                     ny,
#                     nx,
#                 ) in self.path:
#                     return False
#         # print("May Healing at: ", y, x)
#         self.maybe_health.append((y, x))
#         return True

#     def check_no_safe(self, y, x, cell):
#         """
#         Check if a cell is unsafe (either containing a pit or a Wumpus).

#         Parameters:
#             y (int): Row index.
#             x (int): Column index.
#             cell (Cell): The cell to check for dangers.

#         Returns:
#             bool: True if the cell is unsafe, False otherwise.
#         """
#         return self.check_have_pit(y, x, cell) or self.check_have_wumpus(y, x, cell)

#     def dfs(self, program):
#         """
#         Perform a Depth-First Search (DFS) to explore the map based on current knowledge.

#         Parameters:
#             program (Program): The program object containing the map and cells.

#         Returns:
#             list: The path taken by the agent during the exploration.
#         """
#         frontier = [(self.y, self.x)]  # Initialize the frontier with the current cell

#         directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

#         while frontier:  # While there are cells to explore

#             current_y, current_x = frontier.pop()  # Pop the last cell from the frontier

#             if self.check_have_poison(
#                 current_y, current_x, program.cells[self.y][self.x]
#             ):
#                 if self.current_hp == 25:
#                     if self.healing_potion == 0:
#                         continue
#                     self.heal.append((self.y, self.x))
#                     self.healing_potion -= 1
#                     self.healing_potion = max(self.healing_potion, 0)
#                     self.current_hp += 25

#             if program.cells[current_y][current_x].is_visited:
#                 continue

#             self.y, self.x = (
#                 current_y,
#                 current_x,
#             )  # Update agent's current position, agent move to new position
#             program.cells[self.y][self.x].is_visited = True
#             self.path.append((self.y, self.x))

#             if "P_G" in program.cells[self.y][self.x].element:
#                 self.sure_poison.append((self.y, self.x))
#                 self.current_hp -= 25
#                 if self.current_hp <= 0:
#                     return []

#             if program.cells[self.y][self.x].is_breeze:
#                 self.knowledge_base_pit_percept.append((self.y, self.x))
#             if program.cells[self.y][self.x].is_stench:
#                 self.knowledge_base_wumpus_percept.append((self.y, self.x))
#             if program.cells[self.y][self.x].is_whiff:
#                 self.knowledge_base_poison_percept.append((self.y, self.x))
#             if program.cells[self.y][self.x].is_glow:
#                 self.knowledge_base_health_percept.append((self.y, self.x))

#             if "H_P" in program.cells[self.y][self.x].element:
#                 self.healing_potion += 1
#                 program.cells[self.y][self.x].element.remove("H_P")
#                 if program.cells[self.y][self.x].element == []:
#                     program.cells[self.y][self.x].element.append("-")
#                 for dy, dx in directions:
#                     ny, nx = self.y + dy, self.x + dx
#                     if (
#                         0 <= ny <= program.map_size - 1
#                         and 0 <= nx <= program.map_size - 1
#                     ):
#                         program.cells[ny][nx].is_glow = False
#                         for dyy, dxx in directions:
#                             nyy, nxx = ny + dyy, nx + dxx
#                             if (
#                                 0 <= nyy <= program.map_size - 1
#                                 and 0 <= nxx <= program.map_size - 1
#                             ):
#                                 if "H_P" in program.cells[nyy][nxx].element:
#                                     program.cells[ny][nx].is_glow = True
#                                     break

#                 self.grab_heal.append((self.y, self.x))
#                 program.MAPS.append(copy.deepcopy(program.cells))

#             if "G" in program.cells[self.y][self.x].element:
#                 self.grab_gold.append((self.y, self.x))
#                 program.cells[self.y][self.x].element.remove("G")
#                 if program.cells[self.y][self.x].element == []:
#                     program.cells[self.y][self.x].element.append("-")
#                 program.MAPS.append(copy.deepcopy(program.cells))

#             for dy, dx in directions:
#                 ny, nx = current_y + dy, current_x + dx
#                 if 0 <= ny <= program.map_size - 1 and 0 <= nx <= program.map_size - 1:
#                     if not program.cells[ny][nx].is_visited:
#                         if not self.check_no_safe(
#                             ny, nx, program.cells[current_y][current_x]
#                         ):
#                             frontier.append((ny, nx))

#         return self.path

#     def go_to_shoot(self, i, program):
#         tmp_graph = create_graph(self.path, self.map_size)
#         tmp_move = []
#         direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for dy, dx in direction:
#             ny, nx = self.sure_wumpus[i][0] + dy, self.sure_wumpus[i][1] + dx
#             if 0 <= ny < self.map_size and 0 <= nx < self.map_size:
#                 tmp_path = a_star(
#                     tmp_graph, (self.y, self.x), (ny, nx), self, program
#                 )  # start: (self.y, self.x); end: (ny, nx)
#                 if tmp_path != []:
#                     if len(tmp_path) < len(tmp_move) or tmp_move == []:
#                         tmp_move = tmp_path

#         self.path.extend(tmp_move)
#         return tmp_move[
#             -1
#         ]  # Return the last position of the calculated path, which is the shooting position

#     def shoot(self, ny, nx, program):
#         try:
#             program.cells[ny][nx].element.remove("W")
#             if program.cells[ny][nx].element == []:
#                 program.cells[ny][nx].element.append("-")
#             program.reset_percepts(ny, nx)
#             program.add_to_adjacent(ny, nx, "Shoot_wumpus")
#         except:
#             pass
#         self.point -= 100  # ban tru 100
#         return program.cells

#     def shoot_process(self, program, graph):
#         direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
#         for i, cell in enumerate(self.sure_wumpus):
#             if not self.check_have_wumpus(cell[0], cell[1]) or self.check_have_pit(
#                 cell[0], cell[1], program.cells[self.y][self.x]
#             ):
#                 continue
#             y, x = self.go_to_shoot(
#                 i, program
#             )  # agent se xac dinh o can ban sao cho path cost la ngan nhat
#             flag = True
#             while flag:
#                 self.shoot_act.append(((y, x), cell))
#                 new_map = self.shoot(cell[0], cell[1], program)
#                 program.MAPS.append(copy.deepcopy(new_map))

#                 if not program.cells[y][x].is_scream:  # check -> ban het scream -> stop
#                     flag = False

#                 program.reset_percepts(
#                     cell[0], cell[1]
#                 )  # xoa stench , scream / co 2 con wumpus trong hai o cach nhau -> chet 1 con thi sai
#                 for dy, dx in direction:
#                     ny, nx = cell[0] + dy, cell[1] + dx
#                     if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
#                         for dyy, dxx in direction:
#                             nyy, nxx = ny + dyy, nx + dxx
#                             if (
#                                 0 <= nyy <= self.map_size - 1
#                                 and 0 <= nxx <= self.map_size - 1
#                             ):
#                                 if "W" in program.cells[nyy][nxx].element:
#                                     program.cells[ny][nx].is_stench = True
#                                     break

#                 program.MAPS.append(copy.deepcopy(program.cells))

#             self.y = cell[0]
#             self.x = cell[1]  # dc di vao o do
#             graph[self.y][self.x] = 1  # ban xong -> reset 1 -> dc vao
#             self.dfs(program)  # dfs -> path change
#             for cell in self.path:
#                 graph[cell[0]][cell[1]] = 1  # o trong map

#  Kiệt
# class Agent:
#     def __init__(self, map_size=8):
#         self.x = 0
#         self.y = 0
#         self.map_size = map_size
#         self.direction = (1, 0)

#         self.knowledge_base_pit_percept = []
#         self.knowledge_base_wumpus_percept = []

#         self.maybe_wumpus = []
#         self.maybe_pit = []

#         self.sure_wumpus = []
#         self.sure_pit = []

#         self.path = []
#         self.grab_gold = []
#         self.shoot_act = []

#     def check_have_wumpus(self, y, x, cell=None):
#         if (y, x) == (0, 0):
#             return False
#         if cell is not None:
#             if not cell.is_stench or (y, x) in self.path:
#                 return False
#         else:
#             if (y, x) in self.path:
#                 return False

#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for dy, dx in directions:
#             ny, nx = y + dy, x + dx
#             if 0 <= ny < self.map_size and 0 <= nx < self.map_size:
#                 if (ny, nx) not in self.knowledge_base_wumpus_percept and (ny, nx) in self.path:
#                     return False
#         self.maybe_wumpus.append((y, x))
#         return True

#     def check_have_pit(self, y, x, cell):
#         if (y, x) == (0, 0):
#             return False
#         if not cell.is_breeze or (y, x) in self.path:
#             return False

#         directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for dy, dx in directions:
#             ny, nx = y + dy, x + dx
#             if 0 <= ny < self.map_size and 0 <= nx < self.map_size:
#                 if (ny, nx) not in self.knowledge_base_pit_percept and (ny, nx) in self.path:
#                     return False
#         self.maybe_pit.append((y, x))
#         return True

#     def check_no_safe(self, y, x, cell):
#         return self.check_have_pit(y, x, cell) or self.check_have_wumpus(y, x, cell)

#     def dfs(self, program):
#         frontier = [(self.y, self.x)]
#         directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

#         while frontier:
#             current_y, current_x = frontier.pop()
#             if program.cells[current_y][current_x].is_visited:
#                 continue

#             self.y, self.x = current_y, current_x
#             program.cells[self.y][self.x].is_visited = True
#             self.path.append((self.y, self.x))

#             if program.cells[self.y][self.x].is_breeze:
#                 self.knowledge_base_pit_percept.append((self.y, self.x))
#             if program.cells[self.y][self.x].is_stench:
#                 self.knowledge_base_wumpus_percept.append((self.y, self.x))

#             if "G" in program.cells[self.y][self.x].element:
#                 self.grab_gold.append((self.y, self.x))
#                 program.cells[self.y][self.x].element.remove("G")
#                 if not program.cells[self.y][self.x].element:
#                     program.cells[self.y][self.x].element.append("-")
#                 program.MAPS.append(copy.deepcopy(program.cells))

#             for dy, dx in directions:
#                 ny, nx = current_y + dy, current_x + dx
#                 if 0 <= ny < program.map_size and 0 <= nx < program.map_size:
#                     if not program.cells[ny][nx].is_visited:
#                         if not self.check_no_safe(ny, nx, program.cells[current_y][current_x]):
#                             frontier.append((ny, nx))

#         return self.path

#     def go_to_shoot(self, i, program):
#         tmp_graph = create_graph(self.path, self.map_size)
#         tmp_move = []
#         direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for dy, dx in direction:
#             ny, nx = self.sure_wumpus[i][0] + dy, self.sure_wumpus[i][1] + dx
#             if 0 <= ny < self.map_size and 0 <= nx < self.map_size:
#                 tmp_path = a_star(tmp_graph, (self.y, self.x), (ny, nx), self, program)
#                 if tmp_path and (not tmp_move or len(tmp_path) < len(tmp_move)):
#                     tmp_move = tmp_path
#         self.path.extend(tmp_move)
#         return tmp_move[-1] if tmp_move else (self.y, self.x)

#     def shoot(self, ny, nx, program):
#         try:
#             program.cells[ny][nx].element.remove("W")
#             if not program.cells[ny][nx].element:
#                 program.cells[ny][nx].element.append("-")
#             program.reset_percepts(ny, nx)
#             program.add_to_adjacent(ny, nx, "Shoot_wumpus")
#         except:
#             pass
#         return program.cells

#     def shoot_process(self, program, graph):
#         direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for i, cell in enumerate(self.sure_wumpus):
#             if not self.check_have_wumpus(cell[0], cell[1]) or self.check_have_pit(cell[0], cell[1], program.cells[self.y][self.x]):
#                 continue
#             y, x = self.go_to_shoot(i, program)
#             flag = True
#             while flag:
#                 self.shoot_act.append(((y, x), cell))
#                 new_map = self.shoot(cell[0], cell[1], program)
#                 program.MAPS.append(copy.deepcopy(new_map))
#                 if not program.cells[y][x].is_scream:
#                     flag = False

#                 program.reset_percepts(cell[0], cell[1])
#                 for dy, dx in direction:
#                     ny, nx = cell[0] + dy, cell[1] + dx
#                     if 0 <= ny < self.map_size and 0 <= nx < self.map_size:
#                         for dyy, dxx in direction:
#                             nyy, nxx = ny + dyy, nx + dxx
#                             if 0 <= nyy < self.map_size and 0 <= nxx < self.map_size:
#                                 if "W" in program.cells[nyy][nxx].element:
#                                     program.cells[ny][nx].is_stench = True
#                                     break
#                 program.MAPS.append(copy.deepcopy(program.cells))

#             self.y, self.x = cell
#             graph[self.y][self.x] = 1
#             self.dfs(program)
#             for cell in self.path:
#                 graph[cell[0]][cell[1]] = 1

# new Kiệt
import heapq

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # N, E, S, W

class Agent:
    def __init__(self, map_size=(4, 4)):
        if isinstance(map_size, int):
            self.size = (map_size, map_size)
        elif isinstance(map_size, tuple) and len(map_size) == 2:
            self.size = map_size
        else:
            raise ValueError("map_size must be an int or a tuple of size 2")

        self.size = map_size
        self.kb = {}
        self.percepts = {}
        self.position = (0, 0)
        self.path = []
        self.has_gold = False
        self.wumpus_alive = True
        self.arrow_used = False
        self.gold_position = None

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.kb[(x, y)] = {'safe': None, 'pit': None, 'wumpus': None, 'visited': False}

        self.kb[(0, 0)]['safe'] = True
        self.kb[(0, 0)]['visited'] = True

    def update_kb(self, pos, percepts):
        self.kb[pos]['visited'] = True
        self.percepts[pos] = percepts
        x, y = pos
        adj = self.get_adjacent(pos)

        if 'breeze' not in percepts and 'stench' not in percepts:
            for (nx, ny) in adj:
                self.kb[(nx, ny)]['safe'] = True

        if 'glitter' in percepts:
            self.gold_position = pos

        if 'scream' in percepts:
            self.wumpus_alive = False
            for cell in self.kb:
                self.kb[cell]['wumpus'] = False

        self.forward_chain()

    def forward_chain(self):
        for pos in self.kb:
            if self.kb[pos]['visited']:
                continue

            adj = self.get_adjacent(pos)
            has_breeze = any(self.percepts.get(n, {}).get('breeze') for n in adj if n in self.percepts)
            has_stench = any(self.percepts.get(n, {}).get('stench') for n in adj if n in self.percepts)

            if not has_breeze:
                self.kb[pos]['pit'] = False
            if not has_stench:
                self.kb[pos]['wumpus'] = False

    def get_adjacent(self, pos):
        x, y = pos
        return [(x + dx, y + dy) for dx, dy in DIRECTIONS if 0 <= x + dx < self.size[0] and 0 <= y + dy < self.size[1]]

    def get_safe_unvisited(self):
        return [pos for pos, facts in self.kb.items() if facts['safe'] and not facts['visited']]

    def guess_wumpus_positions(self):
        suspect = {}
        for (x, y), percept in self.percepts.items():
            if percept.get('stench'):
                for (nx, ny) in self.get_adjacent((x, y)):
                    if self.kb[(nx, ny)]['wumpus'] is None and self.kb[(nx, ny)]['safe'] is not True:
                        suspect[(nx, ny)] = suspect.get((nx, ny), 0) + 1

        if not suspect:
            return []
        max_score = max(suspect.values())
        return [pos for pos, score in suspect.items() if score == max_score]

    def in_line_of_sight(self, from_pos, to_pos):
        fx, fy = from_pos
        tx, ty = to_pos
        return fx == tx or fy == ty

    def plan_path(self, start, goal):
        return a_star(start, goal, self.kb)

    def act(self, percepts):
        self.update_kb(self.position, percepts)

        if 'glitter' in percepts:
            self.has_gold = True
            return 'Grab'

        if self.has_gold and self.position == (0, 0):
            return 'Climb'

        if self.wumpus_alive and 'stench' in percepts and not self.arrow_used:
            possible_targets = self.guess_wumpus_positions()
            for t in possible_targets:
                if self.in_line_of_sight(self.position, t):
                    self.arrow_used = True
                    return 'Shoot'

        if self.has_gold and self.position != (0, 0):
            self.path = self.plan_path(self.position, (0, 0))

        elif not self.has_gold and self.gold_position:
            self.path = self.plan_path(self.position, self.gold_position)

        elif not self.path:
            safe = self.get_safe_unvisited()
            if safe:
                self.path = self.plan_path(self.position, safe[0])

        if self.path:
            next_pos = self.path.pop(0)
            move = self.get_direction(self.position, next_pos)
            self.position = next_pos
            return move

        return 'Wait'

    def get_direction(self, current, next_pos):
        dx = next_pos[0] - current[0]
        dy = next_pos[1] - current[1]
        if dx == 1: return 'Move East'
        if dx == -1: return 'Move West'
        if dy == 1: return 'Move North'
        if dy == -1: return 'Move South'
        return 'Wait'
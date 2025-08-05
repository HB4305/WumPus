# import random
# from .utils import get_neighbors

# class Cell:
#     def __init__(self):
#         self.wumpus = False
#         self.pit = False
#         self.gold = False
#         self.visited = False
#         self.stench = False
#         self.breeze = False
#         self.glitter = False

# class Environment:
#     def __init__(self, size=4, k=2, pit_prob=0.2):
#         self.size = size
#         self.grid = [[Cell() for _ in range(size)] for _ in range(size)]
#         self.wumpus_positions = set()
#         self.agent_pos = (0, 0)
#         self.agent_dir = "EAST"
#         self.arrow_available = True
#         self.scream = False

#         self.place_entities(k, pit_prob)

#     def in_bounds(self, x, y):
#         return 0 <= x < self.size and 0 <= y < self.size

#     def place_entities(self, k, pit_prob):
#         positions = [(i, j) for i in range(self.size) for j in range(self.size) if (i, j) != (0, 0)]
#         random.shuffle(positions)

#         # place k wumpus
#         for _ in range(k):
#             x, y = positions.pop()
#             self.grid[x][y].wumpus = True
#             self.wumpus_positions.add((x, y))
#             for nx, ny in get_neighbors((x, y), self.size):
#                 self.grid[nx][ny].stench = True

#         # place pits
#         for i in range(self.size):
#             for j in range(self.size):
#                 if (i, j) != (0, 0) and random.random() < pit_prob and not self.grid[i][j].wumpus:
#                     self.grid[i][j].pit = True
#                     for nx, ny in get_neighbors((i, j), self.size):
#                         self.grid[nx][ny].breeze = True

#         # place gold, can be at (0,0)
#         gold_candidates = [
#             (i, j) for i in range(self.size) for j in range(self.size)
#             if not self.grid[i][j].wumpus and not self.grid[i][j].pit
#         ]
#         gold_x, gold_y = random.choice(gold_candidates)
#         self.grid[gold_x][gold_y].gold = True
#         self.grid[gold_x][gold_y].glitter = True

#     def get_percepts(self, x=None, y=None):
#         if x is None or y is None:
#             x, y = self.agent_pos
#         cell = self.grid[x][y]
#         return {
#             "stench": cell.stench,
#             "breeze": cell.breeze,
#             "glitter": cell.glitter,
#             "bump": False,
#             "scream": self.scream
#         }

#     def move_agent(self, new_x, new_y):
#         if not self.in_bounds(new_x, new_y):
#             return {"bump": True, **self.get_percepts()}
#         else:
#             self.agent_pos = (new_x, new_y)
#             return {"bump": False, **self.get_percepts()}

#     def rotate_agent(self, direction):
#         dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
#         idx = dirs.index(self.agent_dir)
#         if direction == "LEFT":
#             self.agent_dir = dirs[(idx - 1) % 4]
#         elif direction == "RIGHT":
#             self.agent_dir = dirs[(idx + 1) % 4]

#     def shoot_arrow(self):
#         if not self.arrow_available:
#             return {"scream": False, **self.get_percepts()}
#         self.arrow_available = False
#         x, y = self.agent_pos
#         dx, dy = {
#             "NORTH": (0, 1),
#             "EAST": (1, 0),
#             "SOUTH": (0, -1),
#             "WEST": (-1, 0)
#         }[self.agent_dir]

#         scream = False
#         while self.in_bounds(x + dx, y + dy):
#             x += dx
#             y += dy
#             if (x, y) in self.wumpus_positions:
#                 self.wumpus_positions.remove((x, y))
#                 self.grid[x][y].wumpus = False
#                 # remove stench
#                 for nx, ny in get_neighbors((x, y), self.size):
#                     self.grid[nx][ny].stench = False
#                 scream = True
#                 break
#         self.scream = scream
#         return {"scream": scream, **self.get_percepts()}
import random
from .utils import get_neighbors

# toạ độ (x, y) x là cột y là dòng
class Cell:
    def __init__(self):
        self.wumpus = False
        self.pit = False
        self.gold = False
        self.visited = False
        self.stench = False
        self.breeze = False
        self.glitter = False
    
    def __str__(self):
        symbols = []
        if self.wumpus:
            symbols.append("W")
        if self.pit:
            symbols.append("P")
        if self.gold:
            symbols.append("G")
        if self.stench:
            symbols.append("S")
        if self.breeze:
            symbols.append("B")
        if self.visited:
            symbols.append("V")
        if not symbols:
            return "_"
        return "".join(symbols)

class Environment:
    def __init__(self, size=8, k=2, pit_prob=0.2):
        self.size = size
        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]
        self.wumpus_positions = set()
        self.agent_pos = (0, 0)
        self.agent_dir = "EAST"
        self.arrow_available = True
        self.scream = False
        self.gold_collected = False
        self.agent_escaped = False

        self.place_entities(k, pit_prob)

    def in_bounds(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def place_entities(self, k, pit_prob):
        positions = [(i, j) for i in range(self.size) for j in range(self.size) if (i, j) != (0, 0)]
        random.shuffle(positions) # xáo trộn các ô N x N, i = x, j = y

        # place k wumpus
        for _ in range(k):
            x, y = positions.pop() # lấy ngẫu nhiên một ô từ danh sách
            self.grid[y][x].wumpus = True
            self.wumpus_positions.add((x, y))
            for nx, ny in get_neighbors((x, y), self.size):
                self.grid[ny][nx].stench = True

        # place pits
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) != (0, 0) and random.random() < pit_prob and not self.grid[j][i].wumpus:
                    self.grid[j][i].pit = True
                    for nx, ny in get_neighbors((i, j), self.size):
                        self.grid[ny][nx].breeze = True

        # place gold, can be at (0,0), chưa đọc tới
        gold_candidates = [
            (i, j) for i in range(self.size) for j in range(self.size)
            if not self.grid[j][i].wumpus and not self.grid[j][i].pit
        ]
        gold_x, gold_y = random.choice(gold_candidates)
        self.grid[gold_y][gold_x].gold = True
        self.grid[gold_y][gold_x].glitter = True

    def get_percepts(self, x=None, y=None):
        if x is None or y is None:
            x, y = self.agent_pos
        cell = self.grid[y][x]
        return {
            "stench": cell.stench,
            "breeze": cell.breeze,
            "glitter": cell.glitter,
            "bump": False,
            "scream": self.scream
        }

    def move_agent(self, new_x, new_y):
        if not self.in_bounds(new_x, new_y):
            return {"bump": True, **self.get_percepts()}
        else:
            self.agent_pos = (new_x, new_y)
            return {"bump": False, **self.get_percepts()}

    def rotate_agent(self, direction):
        dirs = ["NORTH", "EAST", "SOUTH", "WEST"]
        idx = dirs.index(self.agent_dir)
        if direction == "LEFT":
            self.agent_dir = dirs[(idx - 1) % 4]
        elif direction == "RIGHT":
            self.agent_dir = dirs[(idx + 1) % 4]

    def shoot_arrow(self):
        if not self.arrow_available:
            return {"scream": False, **self.get_percepts()}
        self.arrow_available = False
        x, y = self.agent_pos
        dx, dy = {
            "NORTH": (0, 1),
            "EAST": (1, 0),
            "SOUTH": (0, -1),
            "WEST": (-1, 0)
        }[self.agent_dir]

        scream = False
        while self.in_bounds(x + dx, y + dy):
            x += dx
            y += dy
            if (x, y) in self.wumpus_positions:
                self.wumpus_positions.remove((x, y))
                self.grid[y][x].wumpus = False
                # remove stench from neighbors
                for nx, ny in get_neighbors((x, y), self.size):
                    if self.in_bounds(nx, ny):
                        # Check if there are other wumpus nearby
                        has_other_wumpus = False
                        for wnx, wny in get_neighbors((nx, ny), self.size):
                            if (wnx, wny) in self.wumpus_positions:
                                has_other_wumpus = True
                                break
                        if not has_other_wumpus:
                            self.grid[ny][nx].stench = False
                scream = True
                break
        self.scream = scream
        return {"scream": scream, **self.get_percepts()}

    def grab_gold(self):
        x, y = self.agent_pos
        cell = self.grid[y][x]
        if cell.gold:
            self.gold_collected = True
            cell.gold = False
            cell.glitter = False
            return {"grab_success": True, **self.get_percepts()} # grab thì bây cho hình rương được mở hay j he
        return {"grab_success": False, **self.get_percepts()}

    def climb_out(self): # chắc để bên agent quyết định có climb hay không
        if self.agent_pos == (0, 0):
            self.agent_escaped = True
            return {"escaped": True, "has_gold": self.gold_collected}
        return {"escaped": False}


    def is_terminal(self):
        return self.agent_escaped or (self.grid[self.agent_pos[1]][self.agent_pos[0]].wumpus or self.grid[self.agent_pos[1]][self.agent_pos[0]].pit)

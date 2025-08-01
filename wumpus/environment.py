import random
from .utils import get_neighbors

class Cell:
    def __init__(self):
        self.wumpus = False
        self.pit = False
        self.gold = False
        self.visited = False
        self.stench = False
        self.breeze = False
        self.glitter = False

class Environment:
    def __init__(self, size=4, k=2, pit_prob=0.2):
        self.size = size
        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]
        self.place_entities(k, pit_prob)

    def place_entities(self, k, pit_prob):
        positions = [(i, j) for i in range(self.size) for j in range(self.size) if (i, j) != (0, 0)]
        random.shuffle(positions)

        for _ in range(k):
            x, y = positions.pop()
            self.grid[x][y].wumpus = True
            for nx, ny in get_neighbors((x, y), self.size):
                self.grid[nx][ny].stench = True

        for i in range(self.size):
            for j in range(self.size):
                if (i, j) != (0, 0) and random.random() < pit_prob and not self.grid[i][j].wumpus:
                    self.grid[i][j].pit = True
                    for nx, ny in get_neighbors((i, j), self.size):
                        self.grid[nx][ny].breeze = True

        gold_x, gold_y = positions.pop()
        self.grid[gold_x][gold_y].gold = True
        self.grid[gold_x][gold_y].glitter = True

    def get_percepts(self, x, y):
        cell = self.grid[x][y]
        return {
            "stench": cell.stench,
            "breeze": cell.breeze,
            "glitter": cell.glitter,
            "bump": False,
            "scream": False
        }
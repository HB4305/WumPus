from algorithms.program import Program
from algorithms.a_star import a_star, create_graph
import copy
import heapq


# Agent class definition
class Agent:
    def __init__(self, map_size=10):
        self.x = 0  # chi so cot hien tai cua agent
        self.y = 0  # chi so hang hien tai cua agent
        self.current_hp = 100  # luong mau default
        self.map_size = map_size  # kich thuoc map hien tai
        self.direction = (1, 0)

        self.knowledge_base_pit_percept = []
        self.knowledge_base_wumpus_percept = []
        self.knowledge_base_poison_percept = []
        self.knowledge_base_health_percept = []  # bo cung duoc, k can thiet lam

        self.maybe_wumpus = []  # check xem co the co wumpus trong o do khong
        self.maybe_poison = []  # check xem co the co poison trong o do khong
        self.maybe_pit = []  # check xem co the co pit trong o do khong
        self.maybe_health = []  # bo cung duoc, k can thiet lam

        self.sure_wumpus = []  # check xem wumpus co chac trong o do khong
        self.sure_poison = []  # check xem co poison trong do ko
        self.sure_pit = []  # check xem co chac la pit trong do khong
        self.sure_health = []  # bo cung duoc, k can thiet lam

        self.healing_potion = 0  # so luong healing potion dang nam giu hien tai
        self.point = 0  # so diem hien tai cua agent
        self.path = []  # duong di cua agent

        # action
        self.grab_heal = []  # locations where healing potions were grabbed
        self.grab_gold = []  # locations where golds were grabbed
        self.heal = []  # locations where healing potions were used.
        self.shoot_act = []  # shooting actions performed.

    def check_have_wumpus(self, y, x, cell=None):
        """
        Check if a Wumpus might be present at the given coordinates.

        Parameters:
            y (int): Row index.
            x (int): Column index.
            cell (Cell): The cell to check for a stench, optional.

        Returns:
            bool: True if there might be a Wumpus at the given location, False otherwise.
        """
        if (y, x) == (0, 0):  # safe next cell, no wumpus at the starting position.
            return False
        if cell is not None:
            if not cell.is_stench or (y, x) in self.path:
                return False
        else:
            if (y, x) in self.path:
                return False

        # check neighboring cells to validate the posibility of a Wumpus.
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                if (ny, nx) not in self.knowledge_base_wumpus_percept and (
                    ny,
                    nx,
                ) in self.path:
                    return False
        self.maybe_wumpus.append((y, x))  # potential wumpus location
        return True

    def check_have_pit(self, y, x, cell):
        """
        Check if a pit might be present at the given coordinates.

        Parameters:
            y (int): Row index.
            x (int): Column index.
            cell (Cell): The cell to check for a breeze.

        Returns:
            bool: True if there might be a pit at the given location, False otherwise.
        """
        if (y, x) == (
            0,
            0,
        ):  # check next cell is safe -> no pit at the starting position.
            return False  # no pit
        if (
            not cell.is_breeze or (y, x) in self.path
        ):  # if the now cell (cell) is not breeze or the next cell is in the trace path
            return False  # no pit
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                if (ny, nx) not in self.knowledge_base_pit_percept and (
                    ny,
                    nx,
                ) in self.path:  # Kiểm tra nếu tọa độ mới (ny, nx) không nằm trong self.knowledge_base_pit_percept (tức là agent chưa biết rằng có hố tại vị trí này) và tọa độ này đã nằm trong self.path (tức là agent đã đi qua ô này trước đó).
                    return False  # no pit
        self.maybe_pit.append((y, x))
        return True

    def check_have_poison(self, y, x, cell):
        """
        Check if a poison gas might be present at the given coordinates.

        Parameters:
            y (int): Row index.
            x (int): Column index.
            cell (Cell): The cell to check for a whiff.

        Returns:
            bool: True if there might be poison gas at the given location, False otherwise.
        """
        if (y, x) == (0, 0):  # Safe zone, no poison gas at the starting position
            return False  # no poison
        if (
            not cell.is_whiff or (y, x) in self.path
        ):  # if the now cell is not whiff and the next cell is in the trace path
            return False  # no poison
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                if (ny, nx) not in self.knowledge_base_poison_percept and (
                    ny,
                    nx,
                ) in self.path:
                    return False
        self.maybe_poison.append((y, x))
        return True

    def check_have_healing(self, y, x, cell):
        if not cell.is_glow or (y, x) in self.path:
            return False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                if (ny, nx) not in self.knowledge_base_health_percept and (
                    ny,
                    nx,
                ) in self.path:
                    return False
        # print("May Healing at: ", y, x)
        self.maybe_health.append((y, x))
        return True

    def check_no_safe(self, y, x, cell):
        """
        Check if a cell is unsafe (either containing a pit or a Wumpus).

        Parameters:
            y (int): Row index.
            x (int): Column index.
            cell (Cell): The cell to check for dangers.

        Returns:
            bool: True if the cell is unsafe, False otherwise.
        """
        return self.check_have_pit(y, x, cell) or self.check_have_wumpus(y, x, cell)

    def dfs(self, program):
        """
        Perform a Depth-First Search (DFS) to explore the map based on current knowledge.

        Parameters:
            program (Program): The program object containing the map and cells.

        Returns:
            list: The path taken by the agent during the exploration.
        """
        frontier = [(self.y, self.x)]  # Initialize the frontier with the current cell

        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

        while frontier:  # While there are cells to explore

            current_y, current_x = frontier.pop()  # Pop the last cell from the frontier

            if self.check_have_poison(
                current_y, current_x, program.cells[self.y][self.x]
            ):
                if self.current_hp == 25:
                    if self.healing_potion == 0:
                        continue
                    self.heal.append((self.y, self.x))
                    self.healing_potion -= 1
                    self.healing_potion = max(self.healing_potion, 0)
                    self.current_hp += 25

            if program.cells[current_y][current_x].is_visited:
                continue

            self.y, self.x = (
                current_y,
                current_x,
            )  # Update agent's current position, agent move to new position
            program.cells[self.y][self.x].is_visited = True
            self.path.append((self.y, self.x))

            if "P_G" in program.cells[self.y][self.x].element:
                self.sure_poison.append((self.y, self.x))
                self.current_hp -= 25
                if self.current_hp <= 0:
                    return []

            if program.cells[self.y][self.x].is_breeze:
                self.knowledge_base_pit_percept.append((self.y, self.x))
            if program.cells[self.y][self.x].is_stench:
                self.knowledge_base_wumpus_percept.append((self.y, self.x))
            if program.cells[self.y][self.x].is_whiff:
                self.knowledge_base_poison_percept.append((self.y, self.x))
            if program.cells[self.y][self.x].is_glow:
                self.knowledge_base_health_percept.append((self.y, self.x))

            if "H_P" in program.cells[self.y][self.x].element:
                self.healing_potion += 1
                program.cells[self.y][self.x].element.remove("H_P")
                if program.cells[self.y][self.x].element == []:
                    program.cells[self.y][self.x].element.append("-")
                for dy, dx in directions:
                    ny, nx = self.y + dy, self.x + dx
                    if (
                        0 <= ny <= program.map_size - 1
                        and 0 <= nx <= program.map_size - 1
                    ):
                        program.cells[ny][nx].is_glow = False
                        for dyy, dxx in directions:
                            nyy, nxx = ny + dyy, nx + dxx
                            if (
                                0 <= nyy <= program.map_size - 1
                                and 0 <= nxx <= program.map_size - 1
                            ):
                                if "H_P" in program.cells[nyy][nxx].element:
                                    program.cells[ny][nx].is_glow = True
                                    break

                self.grab_heal.append((self.y, self.x))
                program.MAPS.append(copy.deepcopy(program.cells))

            if "G" in program.cells[self.y][self.x].element:
                self.grab_gold.append((self.y, self.x))
                program.cells[self.y][self.x].element.remove("G")
                if program.cells[self.y][self.x].element == []:
                    program.cells[self.y][self.x].element.append("-")
                program.MAPS.append(copy.deepcopy(program.cells))

            for dy, dx in directions:
                ny, nx = current_y + dy, current_x + dx
                if 0 <= ny <= program.map_size - 1 and 0 <= nx <= program.map_size - 1:
                    if not program.cells[ny][nx].is_visited:
                        if not self.check_no_safe(
                            ny, nx, program.cells[current_y][current_x]
                        ):
                            frontier.append((ny, nx))

        return self.path

    def go_to_shoot(self, i, program):
        tmp_graph = create_graph(self.path, self.map_size)
        tmp_move = []
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in direction:
            ny, nx = self.sure_wumpus[i][0] + dy, self.sure_wumpus[i][1] + dx
            if 0 <= ny < self.map_size and 0 <= nx < self.map_size:
                tmp_path = a_star(
                    tmp_graph, (self.y, self.x), (ny, nx), self, program
                )  # start: (self.y, self.x); end: (ny, nx)
                if tmp_path != []:
                    if len(tmp_path) < len(tmp_move) or tmp_move == []:
                        tmp_move = tmp_path

        self.path.extend(tmp_move)
        return tmp_move[
            -1
        ]  # Return the last position of the calculated path, which is the shooting position

    def shoot(self, ny, nx, program):
        try:
            program.cells[ny][nx].element.remove("W")
            if program.cells[ny][nx].element == []:
                program.cells[ny][nx].element.append("-")
            program.reset_percepts(ny, nx)
            program.add_to_adjacent(ny, nx, "Shoot_wumpus")
        except:
            pass
        self.point -= 100  # ban tru 100
        return program.cells

    def shoot_process(self, program, graph):
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        for i, cell in enumerate(self.sure_wumpus):
            if not self.check_have_wumpus(cell[0], cell[1]) or self.check_have_pit(
                cell[0], cell[1], program.cells[self.y][self.x]
            ):
                continue
            y, x = self.go_to_shoot(
                i, program
            )  # agent se xac dinh o can ban sao cho path cost la ngan nhat
            flag = True
            while flag:
                self.shoot_act.append(((y, x), cell))
                new_map = self.shoot(cell[0], cell[1], program)
                program.MAPS.append(copy.deepcopy(new_map))

                if not program.cells[y][x].is_scream:  # check -> ban het scream -> stop
                    flag = False

                program.reset_percepts(
                    cell[0], cell[1]
                )  # xoa stench , scream / co 2 con wumpus trong hai o cach nhau -> chet 1 con thi sai
                for dy, dx in direction:
                    ny, nx = cell[0] + dy, cell[1] + dx
                    if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                        for dyy, dxx in direction:
                            nyy, nxx = ny + dyy, nx + dxx
                            if (
                                0 <= nyy <= self.map_size - 1
                                and 0 <= nxx <= self.map_size - 1
                            ):
                                if "W" in program.cells[nyy][nxx].element:
                                    program.cells[ny][nx].is_stench = True
                                    break

                program.MAPS.append(copy.deepcopy(program.cells))

            self.y = cell[0]
            self.x = cell[1]  # dc di vao o do
            graph[self.y][self.x] = 1  # ban xong -> reset 1 -> dc vao
            self.dfs(program)  # dfs -> path change
            for cell in self.path:
                graph[cell[0]][cell[1]] = 1  # o trong map

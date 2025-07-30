from algorithms.cell import Cell
import copy


class Program:
    """
    Class representing the Wumpus World program that handles the map, cell updates, and game logic.

    Attributes:
        map_size (int): The size of the map (NxN).
        tmp_map (list): Temporary storage for the map as a list of lists containing elements in each cell.
        file_path (str): Path to the file containing the map configuration.
        cells (list): A 2D list of Cell objects representing the Wumpus World grid.
    """

    def __init__(self, file_path):
        """
        Initializes the Program class with the provided file path.

        Args:
            file_path (str): The path to the map file.
        """
        self.map_size = 0  # Size of the map (NxN)
        self.tmp_map = []  # Temporary storage for map elements
        self.file_path = file_path  # File path for the map file
        self.cells = []  # 2D list to store Cell objects
        self.MAPS = []  # Store all the map case when it change
        self.read_map()  # Read the map from the file and initialize the game world

    def read_map(self):
        """
        Reads the map from the input file and initializes the cells with elements.
        """
        with open(self.file_path, "r") as file:
            # Read the first line to get the size of the map
            self.map_size = int(file.readline().strip())

            # Read the map data line by line
            for _ in range(self.map_size):
                line = file.readline().strip()
                # Split the line by '.' to get rooms, then split each room by ','
                row = [cell.split(",") for cell in line.split(".")]  # Parse each row
                self.tmp_map.append(
                    row
                )  # Append the processed row to the temporary map
        # print(self.tmp_map)
        # Initialize cells with positions and elements
        for y in range(self.map_size):
            self.cells.append([])  # Initialize a new row in cells
            for x in range(self.map_size):
                self.cells[y].append(
                    Cell(y, x)
                )  # Create a new Cell object for each position
                self.cells[y][x].element = self.tmp_map[y][
                    x
                ]  # Assign elements from the temporary map

        self.init_map_info()  # Update the map with stench, breeze, whiff, glow and scream

    def reset_percepts(self, y, x):
        self.add_to_adjacent(y, x, "Reset")
        for element in self.cells[y][x].element:
            self.add_to_adjacent(y, x, element)

    def update_percepts(self, y, x, elements):
        if "W" in elements:
            self.add_stench(y, x)
        if "P" in elements:
            self.add_breeze(y, x)
        if "P_G" in elements:
            self.add_whiff(y, x)
        if "H_P" in elements:
            self.add_glow(y, x)

    def init_map_info(self):
        """
        Iterates through the map and updates the cells with information about stench, breeze, whiff, and glow.
        """
        # Iterate through each cell in the map
        for i in range(self.map_size):
            for j in range(self.map_size):
                elements = self.tmp_map[i][j]  # Get the elements in the current cell
                self.update_percepts(
                    i, j, elements
                )  # Update adjacent cells based on these elements

    def add_stench(self, y, x):
        """
        Adds stench to adjacent cells of a Wumpus.

        Args:
            y (int): The y-coordinate of the Wumpus cell.
            x (int): The x-coordinate of the Wumpus cell.
        """
        self.add_to_adjacent(y, x, "W")  # Add stench to adjacent cells

    def add_breeze(self, y, x):
        """
        Adds breeze to adjacent cells of a Pit.

        Args:
            y (int): The y-coordinate of the Pit cell.
            x (int): The x-coordinate of the Pit cell.
        """
        self.add_to_adjacent(y, x, "P")  # Add breeze to adjacent cells

    def add_whiff(self, y, x):
        """
        Adds whiff to adjacent cells of Poisonous Gas.

        Args:
            y (int): The y-coordinate of the Poisonous Gas cell.
            x (int): The x-coordinate of the Poisonous Gas cell.
        """
        self.add_to_adjacent(y, x, "P_G")  # Add whiff to adjacent cells

    def add_glow(self, y, x):
        """
        Adds glow to adjacent cells of Healing Potions.

        Args:
            y (int): The y-coordinate of the Healing Potions cell.
            x (int): The x-coordinate of the Healing Potions cell.
        """
        self.add_to_adjacent(y, x, "H_P")  # Add glow to adjacent cells

    def add_to_adjacent(self, y, x, object_name):
        """
        Adds an effect (stench, breeze, whiff, glow) to adjacent cells based on the specified object.

        Args:
            y (int): The y-coordinate of the cell with the object.
            x (int): The x-coordinate of the cell with the object.
            object_name (str): The name of the object (e.g., "Wumpus", "Pit").
        """
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]  # Directions to adjacent cells (up, down, left, right)
        for dy, dx in directions:
            nx, ny = x + dx, y + dy  # Calculate the new coordinates
            if 0 <= nx <= self.map_size - 1 and 0 <= ny <= self.map_size - 1:
                if object_name == "W":
                    self.cells[ny][nx].is_stench = True
                elif object_name == "P":
                    self.cells[ny][nx].is_breeze = True
                elif object_name == "P_G":
                    self.cells[ny][nx].is_whiff = True
                elif object_name == "H_P":
                    self.cells[ny][nx].is_glow = True
                elif object_name == "Reset":
                    self.cells[ny][nx].is_stench = False
                    self.cells[ny][nx].is_scream = False
                elif object_name == "Shoot_wumpus":
                    self.cells[ny][nx].is_scream = True

    def display_map_test(self):
        """
        Displays the map with all information for testing purposes.
        """
        print(
            "Type: [element, stench, breeze, whiff, glow, scream]"
        )  # Header for map display
        # Iterate through each row in the map
        for i in range(self.map_size):
            for j in range(self.map_size):
                cell = self.cells[i][j]  # Get the cell at the current position
                # Display the cell's elements and effects
                print(
                    "[",
                    cell.element,
                    "T" if cell.is_stench else "F",
                    "T" if cell.is_breeze else "F",
                    "T" if cell.is_whiff else "F",
                    "T" if cell.is_glow else "F",
                    "T" if cell.is_scream else "F",
                    "]",
                    end=" ",
                )
            print()  # Move to the next line after each row

    def return_map_test(self):
        """
        Return the map with all information for testing purposes.
        """
        # print("Type: [element, stench, breeze, whiff, glow, scream]")  # Header for map display
        # Iterate through each row in the map
        map = []
        for y in range(self.map_size):
            map.append([])  # Initialize a new row in cells
            for x in range(self.map_size):
                # map[y].append(Cell(y, x))
                map[y].append([])
                map[y][x].append(self.get_cell_info(y, x))
                # map[y][x][0] = self.get_cell_info(y, x)  # Assign elements from the temporary map
        for i in range(self.map_size):
            for j in range(self.map_size):
                cell = self.cells[i][j]  # Get the cell at the current position
                # Display the cell's elements and effects
                map[i][j].append(True if cell.is_stench else False)
                map[i][j].append(True if cell.is_breeze else False)
                map[i][j].append(True if cell.is_whiff else False)
                map[i][j].append(True if cell.is_glow else False)
                map[i][j].append(True if cell.is_scream else False)
        return map

    def get_cell_info(self, y, x):
        return self.tmp_map[y][x]

    def copy(self):
        return copy.deepcopy(self)

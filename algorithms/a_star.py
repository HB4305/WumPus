import heapq


def create_graph(list_cell, map_size):
    # Initialize an empty list to represent the graph as a 2D grid.
    graph = []
    # Loop over the range of the map size to create rows of the grid.
    for i in range(map_size):
        # Append an empty list (row) to the graph.
        graph.append([])
        # For each row, append columns with the initial value of -1 (blocked cell).
        for _ in range(map_size):
            graph[i].append(-1)

    # Iterate through the list of accessible cells (list_cell).
    for cell in list_cell:
        # Set the corresponding cell in the graph to 1, marking it as accessible.
        graph[cell[0]][cell[1]] = 1

    # Return the created graph.
    return graph


def a_star(graph, start, goal, agent, program):
    # Initialize the map size (assuming a square grid)
    map_size = len(graph[0])
    # Initialize visited nodes, cost to reach nodes, and parent nodes
    visited = []
    cost = []
    parent = []

    # Temporary list to store cells where healing occurred
    tmp_heal = []

    # Initialize the 2D lists for visited, cost, and parent arrays
    for i in range(map_size):
        visited.append([])  # Track whether each cell has been visited
        cost.append([])  # Track the cost to reach each cell
        parent.append([])  # Track the parent of each cell in the path
        for _ in range(map_size):
            visited[i].append(False)  # Initially, no cells are visited
            cost[i].append(float("inf"))  # Initialize cost to infinity
            parent[i].append((-1, -1))  # Initialize parent to an invalid cell

    # Set the starting cell's cost to 0
    cost[start[0]][start[1]] = 0
    frontier = [
        (
            (
                100 if start in agent.sure_poison else 0
            ),  # Priority based on poison (path cost + heuristic)
            start,  # Current node
            agent.current_hp,  # Agent's current health
            agent.healing_potion,  # Agent's healing potions
        )
    ]
    # Define the possible directions to move (up, down, left, right)
    direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    prev = (-1, -1)  # Previous node (initially invalid)
    while frontier:
        # Pop the node with the lowest priority (f-value)
        _, current, hp, potion = heapq.heappop(frontier)
        # Skip the node if it has already been visited
        if visited[current[0]][current[1]]:
            continue
        # Mark the current node as visited
        visited[current[0]][current[1]] = True
        # Handle special conditions when moving to a new node
        if current != start:
            # If the cell is in sure_poison, reduce health or use potion
            if current in agent.sure_poison:
                if hp == 25:
                    if potion > 0:
                        potion -= 1
                        hp += 25
                        tmp_heal.append(current)
                    else:
                        continue
            # If the cell contains poisonous gas, reduce health
            if "P_G" in program.cells[current[0]][current[1]].element:
                hp -= 25
                # If health drops to 0 or below, mark the cell as blocked
                if hp <= 0:
                    graph[current[0]][current[1]] = -1  # => agent dies
                    continue

        # Explore neighbors (up, down, left, right)
        for dy, dx in direction:
            ny, nx = current[0] + dy, current[1] + dx  # Calculate new coordinates
            # Check if the new coordinates are within the grid
            if 0 <= ny < map_size and 0 <= nx < map_size:
                # If the new cell is not visited and is not blocked
                if not visited[ny][nx] and graph[ny][nx] != -1:
                    new_cost = cost[current[0]][current[1]] + 1  # Update the cost
                    # If the new cost is less than the current cost for this cell
                    if new_cost < cost[ny][nx]:
                        cost[ny][nx] = new_cost  # Update the cost
                        parent[ny][nx] = current  # Set the parent of the new cell
                        # Calculate the priority (f-value) using Manhattan distance + poison factor
                        new_f = (
                            abs(ny - goal[0])
                            + abs(nx - goal[1])
                            + (100 if (ny, nx) in agent.sure_poison else 0)
                        )
                        # Add extra cost if moving in a direction that changes orientation
                        if (prev[0] - current[0]) * (current[0] - ny) + (
                            prev[1] - current[1]
                        ) * (current[1] - nx) == 0:
                            new_f += (
                                10  # update -> huong vuong goc -> day heu -> ko uu tien
                            )
                        # Push the neighbor cell to the priority queue with the calculated f-value
                        heapq.heappush(frontier, (new_f, (ny, nx), hp, potion))
        # Check if the goal has been reached
        if visited[goal[0]][goal[1]]:
            agent.current_hp = hp  # Update agent's health
            agent.healing_potion = potion  # Update agent's potion count
            break  # Exit the loop if the goal is reached
        prev = current  # Update the previous node
    # If the goal was not reached, return an empty path
    if not visited[goal[0]][goal[1]]:
        return []
    # Backtrack to build the path from start to goal
    path = []
    while goal != start:
        path.append(goal)
        goal = parent[goal[0]][goal[1]]
    path.append(start)
    path.reverse()  # Reverse the path to start-to-goal order

    # Add healing cells to the agent's heal list if they are part of the path
    for cell in tmp_heal:
        if cell in path:
            agent.heal.append(cell)
    # Return the calculated path
    return path

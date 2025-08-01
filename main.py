from algorithms.program import Program
from algorithms.agent import Agent
from algorithms.a_star import create_graph, a_star
import copy
from ui import main_ui
from utils.write_output import write_output


# def main():
#     """
#     Main function for running the Wumpus World game simulation.

#     This function initializes the game environment based on the chosen map,
#     sets up the agent, and controls the game loop where the agent explores the map,
#     interacts with elements (like Wumpus, pits, gold, and healing potions), and
#     records its path and actions. The results are then displayed and output to a file.

#     The function involves:
#     - Setting up the game environment from a pre-defined map.
#     - Initializing the agent and simulating its decisions and actions.
#     - Managing the agent's interaction with the environment and updating its state.
#     - Outputting the results of the simulation.

#     The agent's behavior includes pathfinding using the A* algorithm, shooting the Wumpus,
#     collecting gold, healing potions, and managing its health and score.
#     """
#     # Display the menu to select a map and get the chosen map number
#     choose_map_result = main_ui.showMenu() + 1
#     file_path = f"input/map{choose_map_result}.txt"
#     output_filepath = f"output/result{choose_map_result}.txt"
#     # Initialize the Program with the selected map file
#     program = Program(file_path)
#     # Return the initial map and make a deep copy of it
#     ma = program.return_map_test()
#     map = copy.deepcopy(ma)
#     # Store the initial state of the map
#     program.MAPS.append(copy.deepcopy(program.cells))
#     # Initialize the agent with the map size
#     agent = Agent(map_size=program.map_size)
#     # Perform a depth-first search to explore the map
#     agent.dfs(program)  # 1

#     # Process possible Wumpus locations
#     for cell in agent.maybe_wumpus:
#         if cell not in agent.path and cell not in agent.sure_wumpus:
#             agent.sure_wumpus.append(cell)

#     # Process possible pit locations
#     for cell in agent.maybe_pit:
#         if cell not in agent.path and cell not in agent.sure_pit:
#             agent.sure_pit.append(cell)

#     # Create a graph of the path explored by the agent for Wumpus elimination
#     graph1 = create_graph(
#         agent.path, agent.map_size
#     )  # graph -> o agent di qua -> bieu do -> de tim path toi uu trong A* -> luu w chet

#     # Create a graph of the path for general movement and interaction
#     graph2 = create_graph(
#         agent.path, agent.map_size
#     )  # graph -> ban wumpus -> update path -> ban dau
#     agent.shoot_process(program, graph1)  # luu w -> chet
#     agent.path.append((0, 0))  # quay ve o (0,0)
#     agent.current_hp = 100
#     tmp_poition = 0
#     tmp_hp = 100
#     primary_path = []  # path -> tra ve UI
#     main_ui.showWumpusWorld(choose_map_result, map)
#     for i in range(len(agent.path) - 1):
#         path_with_info = []
#         current = agent.path[i]
#         nextt = agent.path[i + 1]
#         tmp_path = a_star(
#             graph2, current, nextt, agent, program
#         )  # goi a star -> the hien duong
#         if tmp_path == []:
#             graph2 = graph1
#             tmp_path = a_star(graph2, current, nextt, agent, program)
#         for j in range(len(tmp_path) - 1):
#             action = []
#             tmp_hp = agent.current_hp
#             if tmp_path[j] in agent.grab_gold:
#                 action.append("Grab Gold")
#                 agent.grab_gold.remove(tmp_path[j])
#             if tmp_path[j] in agent.grab_heal:
#                 action.append("Grab Heal")
#                 agent.grab_heal.remove(tmp_path[j])
#                 tmp_poition += 1
#             vect = (
#                 tmp_path[j + 1][0] - tmp_path[j][0],
#                 tmp_path[j + 1][1] - tmp_path[j][1],
#             )
#             if (vect[0] * agent.direction[0]) + (vect[1] * agent.direction[1]) == 0:
#                 if agent.direction == (1, 0):
#                     if vect == (0, 1):
#                         action.append("Turn Right")
#                     else:
#                         action.append("Turn Left")
#                 elif agent.direction == (-1, 0):
#                     if vect == (0, 1):
#                         action.append("Turn Left")
#                     else:
#                         action.append("Turn Right")
#                 elif agent.direction == (0, 1):
#                     if vect == (1, 0):
#                         action.append("Turn Left")
#                     else:
#                         action.append("Turn Right")
#                 else:
#                     if vect == (1, 0):
#                         action.append("Turn Right")
#                     else:
#                         action.append("Turn Left")
#                 agent.direction = vect
#             else:
#                 if (vect[0] * agent.direction[0]) + (
#                     vect[1] * agent.direction[1]
#                 ) == -1:
#                     action.append("Turn Left")
#                     action.append("Turn Left")
#                     agent.direction = (-1 * agent.direction[0], -1 * agent.direction[1])
#             if (tmp_path[j], tmp_path[j + 1]) in agent.shoot_act:
#                 while (tmp_path[j], tmp_path[j + 1]) in agent.shoot_act:
#                     action.append("Shoot")
#                     agent.shoot_act.remove((tmp_path[j], tmp_path[j + 1]))
#                 graph2[tmp_path[j][0]][tmp_path[j][1]] = 1

#             if tmp_hp == 25:
#                 if (
#                     tmp_path[j] in agent.heal
#                     and tmp_poition > 0
#                     and tmp_path[j + 1] in agent.sure_poison
#                 ):
#                     action.append("Heal")
#                     agent.heal.remove(tmp_path[j])
#                     tmp_poition -= 1
#                     tmp_hp += 25

#             action.append("Move Forward")

#             path_with_info.append((tmp_path[j], action, tmp_hp, tmp_poition))
#         if path_with_info != []:
#             primary_path.append((path_with_info))

#     if primary_path[-1][-1][0] == (0, 1) or primary_path[-1][-1][0] == (1, 0):
#         path_with_info = []
#         path_with_info.append(
#             ((0, 0), ["Climb"], primary_path[-1][-1][2], primary_path[-1][-1][3])
#         )
#         primary_path.append((path_with_info))
#     agent.point = 10000
#     RESULT = []
#     map_index = 0
#     for path in primary_path:
#         for cell in path:
#             for act in cell[1]:
#                 if act == "Climb":
#                     agent.point += 10
#                 elif act == "Shoot":
#                     agent.point -= 100
#                     map_index += 1
#                     RESULT.append(
#                         (cell[0], act, agent.point, cell[2], cell[3], map_index)
#                     )
#                     map_index += 1
#                     RESULT.append(
#                         (cell[0], act, agent.point, cell[2], cell[3], map_index)
#                     )
#                     continue
#                 elif act == "Grab Gold":
#                     agent.point += 5000
#                     map_index += 1
#                 elif act == "Grab Heal":
#                     agent.point -= 10
#                     map_index += 1
#                 else:
#                     agent.point -= 10
#                 RESULT.append((cell[0], act, agent.point, cell[2], cell[3], map_index))
#     maps = copy.deepcopy(program.MAPS)
#     main_ui.showAgentMove(choose_map_result, RESULT, maps, choose_map_result)
#     write_output(file_path=output_filepath, agent=agent, RES=RESULT)


# if __name__ == "__main__":
#     while True:
#         main()

# # Kiệt
# from algorithms.program import Program
# from algorithms.agent import Agent
# from algorithms.a_star import create_graph, a_star
# import copy
# from ui import main_ui
# from utils.write_output import write_output

# def main():
#     choose_map_result = main_ui.showMenu() + 1
#     file_path = f"input/map{choose_map_result}.txt"
#     output_filepath = f"output/result{choose_map_result}.txt"

#     program = Program(file_path)
#     ma = program.return_map_test()
#     map = copy.deepcopy(ma)
#     program.MAPS.append(copy.deepcopy(program.cells))

#     agent = Agent(map_size=program.map_size)
#     agent.dfs(program)

#     for cell in agent.maybe_wumpus:
#         if cell not in agent.path and cell not in agent.sure_wumpus:
#             agent.sure_wumpus.append(cell)

#     for cell in agent.maybe_pit:
#         if cell not in agent.path and cell not in agent.sure_pit:
#             agent.sure_pit.append(cell)

#     graph1 = create_graph(agent.path, agent.map_size)
#     graph2 = create_graph(agent.path, agent.map_size)
#     agent.shoot_process(program, graph1)
#     agent.path.append((0, 0))

#     primary_path = []
#     main_ui.showWumpusWorld(choose_map_result, map)

#     for i in range(len(agent.path) - 1):
#         path_with_info = []
#         current = agent.path[i]
#         nextt = agent.path[i + 1]
#         tmp_path = a_star(graph2, current, nextt, agent, program)

#         if tmp_path == []:
#             graph2 = graph1
#             tmp_path = a_star(graph2, current, nextt, agent, program)

#         for j in range(len(tmp_path) - 1):
#             action = []
#             if tmp_path[j] in agent.grab_gold:
#                 action.append("Grab Gold")
#                 agent.grab_gold.remove(tmp_path[j])

#             vect = (
#                 tmp_path[j + 1][0] - tmp_path[j][0],
#                 tmp_path[j + 1][1] - tmp_path[j][1],
#             )

#             if (vect[0] * agent.direction[0]) + (vect[1] * agent.direction[1]) == 0:
#                 if agent.direction == (1, 0):
#                     action.append("Turn Right" if vect == (0, 1) else "Turn Left")
#                 elif agent.direction == (-1, 0):
#                     action.append("Turn Left" if vect == (0, 1) else "Turn Right")
#                 elif agent.direction == (0, 1):
#                     action.append("Turn Left" if vect == (1, 0) else "Turn Right")
#                 else:
#                     action.append("Turn Right" if vect == (1, 0) else "Turn Left")
#                 agent.direction = vect
#             elif (vect[0] * agent.direction[0]) + (vect[1] * agent.direction[1]) == -1:
#                 action.extend(["Turn Left", "Turn Left"])
#                 agent.direction = (-agent.direction[0], -agent.direction[1])

#             if (tmp_path[j], tmp_path[j + 1]) in agent.shoot_act:
#                 while (tmp_path[j], tmp_path[j + 1]) in agent.shoot_act:
#                     action.append("Shoot")
#                     agent.shoot_act.remove((tmp_path[j], tmp_path[j + 1]))
#                 graph2[tmp_path[j][0]][tmp_path[j][1]] = 1

#             action.append("Move Forward")
#             path_with_info.append((tmp_path[j], action))

#         if path_with_info:
#             primary_path.append(path_with_info)

#     if primary_path[-1][-1][0] in [(0, 1), (1, 0)]:
#         primary_path.append([((0, 0), ["Climb"])])

#     agent.point = 0
#     RESULT = []
#     map_index = 0

#     for path in primary_path:
#         for cell in path:
#             for act in cell[1]:
#                 if act == "Climb":
#                     agent.point += 1000 if agent.has_gold else 0
#                 elif act == "Shoot":
#                     agent.point -= 10
#                 elif act == "Grab Gold":
#                     agent.point += 10
#                     agent.has_gold = True
#                 elif act.startswith("Turn"):
#                     agent.point -= 1
#                 elif act == "Move Forward":
#                     agent.point -= 1

#                 map_index += 1
#                 RESULT.append((cell[0], act, agent.point, map_index))

#     maps = copy.deepcopy(program.MAPS)
#     main_ui.showAgentMove(choose_map_result, RESULT, maps, choose_map_result)
#     write_output(file_path=output_filepath, agent=agent, RES=RESULT)

#  new Kiệt
from wumpus.environment import Environment
from wumpus.inference import InferenceEngine
from wumpus.agent import Agent
from wumpus.planner import a_star
from wumpus.utils import get_neighbors

def heuristic(pos):
    # Hàm ước lượng đơn giản: khoảng cách Manhattan về (0, 0)
    x, y = pos
    return x + y

def apply_map_to_environment(map_data, env):
    symbol_map = {
        'P': 'pit',
        'W': 'wumpus',
        'G': 'gold'
    }

    for i in range(env.size):
        for j in range(env.size):
            cell = env.grid[i][j]
            symbols = map_data[i][j]

            if 'P' in symbols:
                cell.pit = True
                for nx, ny in get_neighbors((i, j), env.size):
                    env.grid[nx][ny].breeze = True
            if 'W' in symbols:
                cell.wumpus = True
                for nx, ny in get_neighbors((i, j), env.size):
                    env.grid[nx][ny].stench = True
            if 'G' in symbols:
                cell.gold = True
                cell.glitter = True


def main():
    choose_map_result = main_ui.showMenu() + 1
    file_path = f"input/map{choose_map_result}.txt"
    output_filepath = f"output/result{choose_map_result}.txt"

    program = Program(file_path)
    ma = program.return_map_test()
    map_data = copy.deepcopy(ma)
    program.MAPS.append(copy.deepcopy(program.cells))

    size = program.map_size
    
    # Tạo môi trường giả lập từ map đọc được
    env = Environment(size=size)
    apply_map_to_environment(map_data, env)  


    # Khởi tạo inference engine và agent
    inference = InferenceEngine(size=size)
    agent = Agent(env, inference)

    # Lưu lại bước đi của agent
    RESULT = []
    MAX_STEP = 100
    step_count = 0

    while not agent.finished() and step_count < MAX_STEP:
        action = agent.step()
        RESULT.append(((agent.x, agent.y), action))
        step_count += 1

        if agent.has_gold:
            # Tìm đường quay về bằng A*
            return_path = a_star(start=(agent.x, agent.y),
                                 goal=(0, 0),
                                 heuristic=heuristic,
                                 is_safe=inference.is_safe,
                                 size=size)
            for pos in return_path[1:]:
                agent.x, agent.y = pos
                RESULT.append(((agent.x, agent.y), "RETURN"))
            break

    # Hiển thị bản đồ và hành trình
    program.MAPS.append(copy.deepcopy(program.cells))  # map để truyền cho UI

    maps = copy.deepcopy(program.MAPS)
    main_ui.showWumpusWorld(choose_map_result, map_data)
    main_ui.showAgentMove(choose_map_result, RESULT, maps, choose_map_result)
    write_output(file_path=output_filepath, agent=agent, RES=RESULT)

if __name__ == "__main__":
    while True:
        main()
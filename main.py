from wumpus.environment import Environment
from wumpus.inference import Inference
from wumpus.agent import Agent
from ui import main_ui
import copy


def write_output(file_path, agent, RES):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("== WUMPUS WORLD AGENT RESULT ==\n\n")
        f.write(f"Final score: {agent.point}\n")
        f.write(f"Gold collected: {'Yes' if agent.has_gold else 'No'}\n")
        f.write(f"Total steps: {len(RES)}\n\n")
        f.write("Action log:\n")

        for step, (pos, action, point, hp, potion) in enumerate(RES, 1):
            f.write(f"Step {step:>2}: Pos {pos} - Action: {action:<15} | Point: {point}\n")

import os

def write_map_to_file(file_path, grid):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("== WUMPUS WORLD MAP ==\n\n")
            for row in grid:
                f.write(" ".join(str(cell) for cell in row) + "\n")
        print(f"Map successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing map to file: {e}")

def main():
    # Get configuration from user
    config = main_ui.showMenu()
    if config is None:
        return

    size, pit_prob, wumpus_count = config

    # Create environment and agent
    env = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
    inference = Inference(size)
    agent = Agent(env, inference)

    # Xuất bản đồ vào file trong folder input
    # Debug: In nội dung env.grid
    print("Generated grid:", env.grid)
    print("Grid type:", type(env.grid))

    write_map_to_file("/Users/macbook/Documents/Năm 2/Kỳ 3/CSAI/Project 2/PumPus/input/wumpus_world_map.txt", env.grid)


    print(
        f"[MAIN] Created {size}x{size} world with {wumpus_count} Wumpus and {pit_prob} pit probability"
    )

    # Show initial map
    main_ui.showWumpusWorld(env.grid)

    # Store map states for UI
    MAPS = []
    MAPS.append(copy.deepcopy(env.grid))

    # Agent action results
    RESULT = []
    MAX_STEPS = size * size * 2  # More reasonable step limit
    step_count = 0

    # Main game loop
    while not agent.finished() and step_count < MAX_STEPS:
        print(f"\n=== STEP {step_count + 1} ===")
        print(f"Agent at ({agent.x}, {agent.y})")
        
        # Check current cell for dangers (debug info)
        current_cell = env.grid[agent.y][agent.x]
        if current_cell.wumpus:
            print(f"[MAIN] WARNING: Agent is on Wumpus cell!")
        if current_cell.pit:
            print(f"[MAIN] WARNING: Agent is on Pit cell!")

        action = agent.step()
        step_count += 1

        # Record result
        hp = 0 if (action == "DIE" or agent.dead) else 100
        RESULT.append(((agent.x, agent.y), action, agent.point, hp, 0))
        MAPS.append(copy.deepcopy(env.grid))

        print(f"[MAIN] Step {step_count}: {action}, Score: {agent.point}")

        # Check terminal conditions
        if action == "DIE" or agent.dead:
            print("[MAIN] Agent died!")
            break
        elif action == "CLIMB":
            print("[MAIN] Agent successfully escaped!")
            break
        elif action == "STAY":
            print("[MAIN] Agent has no safe moves")
            break

    # Show agent movement
    main_ui.showAgentMove(None, RESULT, MAPS, None)

    # Write output
    write_output(file_path="output/result.txt", agent=agent, RES=RESULT)

    print(f"\n=== FINAL RESULTS ===")
    print(f"Steps taken: {step_count}")
    print(f"Final score: {agent.point}")
    print(f"Gold collected: {agent.has_gold}")
    print(f"Agent escaped: {agent.finished()}")
    print(f"Agent died: {agent.dead}")


if __name__ == "__main__":
    while True:
        main()
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
# from wumpus.environment import Environment
# from wumpus.inference import InferenceEngine
# from wumpus.agent import Agent
# from wumpus.planner import a_star
# from wumpus.utils import get_neighbors

# def heuristic(pos):
#     # Hàm ước lượng đơn giản: khoảng cách Manhattan về (0, 0)
#     x, y = pos
#     return x + y

# def apply_map_to_environment(map_data, env):
#     symbol_map = {
#         'P': 'pit',
#         'W': 'wumpus',
#         'G': 'gold'
#     }

#     for i in range(env.size):
#         for j in range(env.size):
#             cell = env.grid[i][j]
#             symbols = map_data[i][j]

#             if 'P' in symbols:
#                 cell.pit = True
#                 for nx, ny in get_neighbors((i, j), env.size):
#                     env.grid[nx][ny].breeze = True
#             if 'W' in symbols:
#                 cell.wumpus = True
#                 for nx, ny in get_neighbors((i, j), env.size):
#                     env.grid[nx][ny].stench = True
#             if 'G' in symbols:
#                 cell.gold = True
#                 cell.glitter = True


# def main():
#     choose_map_result = main_ui.showMenu() + 1
#     file_path = f"input/map{choose_map_result}.txt"
#     output_filepath = f"output/result{choose_map_result}.txt"

#     program = Program(file_path)
#     ma = program.return_map_test()
#     map_data = copy.deepcopy(ma)
#     program.MAPS.append(copy.deepcopy(program.cells))

#     size = program.map_size
    
#     # Tạo môi trường giả lập từ map đọc được
#     env = Environment(size=size)
#     apply_map_to_environment(map_data, env)  


#     # Khởi tạo inference engine và agent
#     inference = InferenceEngine(size=size)
#     agent = Agent(env, inference)

#     # Lưu lại bước đi của agent
#     RESULT = []
#     MAX_STEP = 100
#     step_count = 0

#     while not agent.finished() and step_count < MAX_STEP:
#         action = agent.step()
#         RESULT.append(((agent.x, agent.y), action))
#         step_count += 1

#         if agent.has_gold:
#             # Tìm đường quay về bằng A*
#             return_path = a_star(start=(agent.x, agent.y),
#                                  goal=(0, 0),
#                                  heuristic=heuristic,
#                                  is_safe=inference.is_safe,
#                                  size=size)
#             for pos in return_path[1:]:
#                 agent.x, agent.y = pos
#                 RESULT.append(((agent.x, agent.y), "RETURN"))
#             break

#     # Hiển thị bản đồ và hành trình
#     program.MAPS.append(copy.deepcopy(program.cells))  # map để truyền cho UI

#     maps = copy.deepcopy(program.MAPS)
#     main_ui.showWumpusWorld(choose_map_result, map_data)
#     main_ui.showAgentMove(choose_map_result, RESULT, maps, choose_map_result)
#     write_output(file_path=output_filepath, agent=agent, RES=RESULT)

# if __name__ == "__main__":
#     while True:
#         main()


# Bảo thêm
from wumpus.environment import Environment
from wumpus.inference import Inference
from wumpus.agent import Agent
from wumpus.planner import astar_search
from wumpus.algorithm import heuristic
from ui import main_ui
import copy

def heuristic(pos, goal=(0, 0)):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def write_output(file_path, agent, RES):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("== WUMPUS WORLD AGENT RESULT ==\n\n")
        f.write(f"Final score: {agent.point}\n")
        f.write(f"Gold collected: {'Yes' if agent.has_gold else 'No'}\n")
        f.write(f"Total steps: {len(RES)}\n\n")
        f.write("Action log:\n")

        for step, (pos, action, point) in enumerate(RES, 1):
            f.write(f"Step {step:>2}: Pos {pos} - Action: {action:<15} | Point: {point}\n")



def main():
    # Lấy thông tin cấu hình từ người dùng
    size, pit_prob, wumpus_count = main_ui.showMenu()

    # Tạo môi trường và agent
    env = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
    inference = Inference(size)
    agent = Agent(env, inference)

    
    # Hiển thị bản đồ ban đầu
    main_ui.showWumpusWorld(env.grid)

    # Lưu trạng thái bản đồ theo từng bước (để truyền vào UI)
    MAPS = []
    MAPS.append(copy.deepcopy(env.grid))

    # Kết quả hành động [(pos), action, point, HP, potions]
    RESULT = []
    MAX_STEPS = 100
    step_count = 0
    hp = 100
    potion = 0

    while not agent.finished() and step_count < MAX_STEPS:
        action = agent.step()
        step_count += 1

        RESULT.append(((agent.x, agent.y), action, agent.point, hp, potion))
        MAPS.append(copy.deepcopy(env.grid))

        if action == "GRAB":
            return_path = astar_search(
                start=(agent.x, agent.y),
                goal=(0, 0),
                is_safe=inference.is_safe,
                size=size
            )
            for pos in return_path[1:]:
                agent.x, agent.y = pos
                agent.path.append(pos)
                agent.take_action("Move Forward")
                RESULT.append((pos, "Move Forward", agent.point, hp, potion))
                MAPS.append(copy.deepcopy(env.grid))

            agent.take_action("Climb")
            RESULT.append(((0, 0), "Climb", agent.point, hp, potion))
            MAPS.append(copy.deepcopy(env.grid))
            break

    # Gọi giao diện để hiển thị hành trình agent
    main_ui.showAgentMove(None, RESULT, MAPS, None)
    write_output(file_path="output/result.txt", agent=agent, RES=RESULT)

        


if __name__ == "__main__":
    while True:
        main()
if __name__ == "__main__":
    while True:
        main()

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
            f.write("== WUMPUS WORLD MAP WITH COORDINATES ==\n\n")
            size = len(grid)
            for y in range(size):
                row_data = []
                for x in range(size):
                    cell = grid[y][x]
                    content = str(cell)
                    row_data.append(f"{content}({x},{y})")
                f.write("  ".join(row_data) + "\n")
        print(f"Map with coordinates written to {file_path}")
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

    write_map_to_file("input/wumpus_world_map.txt", env.grid)


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
        
        # Ensure we capture the updated map state after an action
        # This is especially important after shooting a wumpus
        if action == "SHOOT_HIT":
            print("[MAIN] Wumpus killed! Updating environment...")
            # Give a small pause to ensure environment is fully updated
            # Then capture the updated state without the wumpus
            MAPS.append(copy.deepcopy(env.grid))
        else:
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

# # Bảo thêm
# from wumpus.environment import Environment
# from wumpus.inference import Inference
# from wumpus.agent import Agent
# from wumpus.planner import astar_search
# from wumpus.algorithm import heuristic
# from ui import main_ui
# import copy

# def heuristic(pos, goal=(0, 0)):
#     return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

# def write_output(file_path, agent, RES):
#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write("== WUMPUS WORLD AGENT RESULT ==\n\n")
#         f.write(f"Final score: {agent.point}\n")
#         f.write(f"Gold collected: {'Yes' if agent.has_gold else 'No'}\n")
#         f.write(f"Total steps: {len(RES)}\n\n")
#         f.write("Action log:\n")

#         for step, (pos, action, point) in enumerate(RES, 1):
#             f.write(f"Step {step:>2}: Pos {pos} - Action: {action:<15} | Point: {point}\n")



# def main():
#     # Lấy thông tin cấu hình từ người dùng
#     size, pit_prob, wumpus_count = main_ui.showMenu()

#     # Tạo môi trường và agent
#     env = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
#     inference = Inference(size)
#     agent = Agent(env, inference)

    
#     # Hiển thị bản đồ ban đầu
#     main_ui.showWumpusWorld(env.grid)

#     # Lưu trạng thái bản đồ theo từng bước (để truyền vào UI)
#     MAPS = []
#     MAPS.append(copy.deepcopy(env.grid))

#     # Kết quả hành động [(pos), action, point, HP, potions]
#     RESULT = []
#     MAX_STEPS = 100
#     step_count = 0
#     hp = 100
#     potion = 0

#     while not agent.finished() and step_count < MAX_STEPS:
#         action = agent.step()
#         step_count += 1

#         RESULT.append(((agent.x, agent.y), action, agent.point, hp, potion))
#         MAPS.append(copy.deepcopy(env.grid))

#         if action == "GRAB":
#             return_path = astar_search(
#                 start=(agent.x, agent.y),
#                 goal=(0, 0),
#                 is_safe=inference.is_safe,
#                 size=size
#             )
#             for pos in return_path[1:]:
#                 agent.x, agent.y = pos
#                 agent.path.append(pos)
#                 agent.take_action("Move Forward")
#                 RESULT.append((pos, "Move Forward", agent.point, hp, potion))
#                 MAPS.append(copy.deepcopy(env.grid))

#             agent.take_action("Climb")
#             RESULT.append(((0, 0), "Climb", agent.point, hp, potion))
#             MAPS.append(copy.deepcopy(env.grid))
#             break

#     # Gọi giao diện để hiển thị hành trình agent
#     main_ui.showAgentMove(None, RESULT, MAPS, None)
#     write_output(file_path="output/result.txt", agent=agent, RES=RESULT)

        


# if __name__ == "__main__":
#     while True:
#         main()
# if __name__ == "__main__":
#     while True:
#         main()

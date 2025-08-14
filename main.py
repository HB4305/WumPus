from wumpus.environment import Environment
from wumpus.inference import Inference
from wumpus.agent import Agent
from ui import main_ui
import copy
from advanced.agent_advanced import AgentAdvanced
from advanced.inference_advanced import InferenceAdvanced
from advanced.environment_advanced import EnvironmentAdvanced
from rand.agent_random import AgentRandom
from rand.environment_random import EnvironmentRandom
from rand.inferences_random import InferenceRandom
from rand_advanced.inferences_random_advanced import InferenceRandomAdvanced
from rand_advanced.environment_random_advanced import EnvironmentRandomAdvanced
from rand_advanced.agent_random_advanced import AgentRandomAdvanced
import os


def write_output(file_path, agent, RES):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("== WUMPUS WORLD AGENT RESULT ==\n\n")
        f.write(f"Final score: {agent.point}\n")
        f.write(f"Gold collected: {'Yes' if agent.has_gold else 'No'}\n")
        f.write(f"Total steps: {len(RES)}\n\n")
        f.write("Action log:\n")

        for step, (pos, action, point) in enumerate(RES, 1):
            f.write(f"Step {step:>2}: Pos {pos} - Action: {action:<15} | Point: {point}\n")

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

    size, pit_prob, wumpus_count, game_mode, agent_mode = config  # Updated to unpack 4 values
    if game_mode == 0:
        #NORMAL mode
        if agent_mode == 0:
            # Create environment and agent
            env = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
            inference = Inference(size, env)
            agent = Agent(env, inference)
            # Xuất bản đồ vào file trong folder input
            # Debug: In nội dung env.grid
            print("Generated grid:", env.grid)
            print("Grid type:", type(env.grid))

            write_map_to_file("input/wumpus_world_map.txt", env.grid)


            print(f"[MAIN] Created {size}x{size} world with {wumpus_count} Wumpus and {pit_prob} pit probability")
            print(f"[MAIN] Game Mode: {'Advanced' if game_mode == 1 else 'Normal'}")

            # Show initial map
            main_ui.showWumpusWorld(env.grid)

            # Store map states for UI
            MAPS = []
            MAPS.append(copy.deepcopy(env.grid))

            # Agent action results
            RESULT = []
            MAX_STEPS = size * size * 4  # More reasonable step limit
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

                # Record result với điểm số hiện tại của agent
                RESULT.append(((agent.x, agent.y), action, agent.point))
                
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
            main_ui.showAgentMove(None, RESULT, MAPS, None, None, agent_mode=0, agent_index=0)

            # Write output
            write_output(file_path="output/result.txt", agent=agent, RES=RESULT)

            print(f"\n=== FINAL RESULTS ===")
            print(f"Steps taken: {step_count}")
            print(f"Final score: {agent.point}")
            print(f"Gold collected: {agent.has_gold}")
            print(f"Agent escaped: {agent.finished()}")
            print(f"Agent died: {agent.dead}")
        else:
            #NORMAL DOUBLE AGENT
            # Tạo environment và lưu lại map gốc
            env = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
            original_grid = copy.deepcopy(env.grid)  # Lưu map gốc
            original_wumpus_positions = env.wumpus_positions.copy()

            # Agent 1 A* RUN 
            inference1 = Inference(size, env)
            agent1 = Agent(env, inference1)
            MAPS1, RESULT1 = [copy.deepcopy(env.grid)], []
            step_count1 = 0
            MAX_STEPS = size * size * 4

            print("Agent 1 result:")
            while not agent1.finished() and step_count1 < MAX_STEPS:
                print(f"\n=== STEP {step_count1 + 1} ===")
                print(f"Agent at ({agent1.x}, {agent1.y})")
                action = agent1.step()
                step_count1 += 1
                RESULT1.append(((agent1.x, agent1.y), action, agent1.point))
                MAPS1.append(copy.deepcopy(env.grid))
                if action == "DIE" or agent1.dead or action == "CLIMB" or action == "STAY":
                    break

            # Tạo lại environment cho agent 2 từ map gốc
            #Agent 2 ramdom 
            env2 = EnvironmentRandom(size=size, k=wumpus_count, pit_prob=pit_prob)
            env2.grid = copy.deepcopy(original_grid)  # Gán lại map gốc
            env2.wumpus_positions = original_wumpus_positions.copy()  # Gán lại vị trí wumpus gốc
            inference2 = InferenceRandom(size, env2)
            agent2 = AgentRandom(env2, inference2)
            MAPS2, RESULT2 = [copy.deepcopy(env2.grid)], []
            step_count2 = 0

            print("Agent 2 result:")
            while not agent2.finished() and step_count2 < MAX_STEPS:
                print(f"\n=== STEP {step_count2 + 1} ===")
                print(f"Agent at ({agent2.x}, {agent2.y})")
                action = agent2.step()
                step_count2 += 1
                RESULT2.append(((agent2.x, agent2.y), action, agent2.point))
                MAPS2.append(copy.deepcopy(env2.grid))
                if action == "DIE" or agent2.dead or action == "CLIMB" or action == "STAY":
                    break

            # Hiển thị kết quả từng agent
            
            main_ui.showAgentMove(None, RESULT1, MAPS1, None, None, agent_mode=1, agent_index=0)
            main_ui.showAgentMove(None, RESULT2, MAPS2, None, None, agent_mode=1, agent_index=1)

            # Ghi file nếu cần
            write_output(file_path="output/result_agent1.txt", agent=agent1, RES=RESULT1)
            write_output(file_path="output/result_agent2.txt", agent=agent2, RES=RESULT2)
            return
    else:
        #ADVANCED mode
        if agent_mode == 0:
            # Game mode 1 (Advanced)
            #ADVANCED SINGLE AGENT
            # env = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
            env = EnvironmentAdvanced(size=size, k=wumpus_count, pit_prob=pit_prob)
            inference = InferenceAdvanced(size, env)
            agent = AgentAdvanced(env, inference)
            
            write_map_to_file("input/wumpus_world_map_advanced.txt", env.grid)
            
            print(f"[MAIN] Created {size}x{size} world with {wumpus_count} Wumpus and {pit_prob} pit probability")
            print(f"[MAIN] Game Mode: Advanced")

            main_ui.showWumpusWorld(env.grid)

            MAPS = []
            MAPS.append(copy.deepcopy(env.grid))
            RESULT = []
            MAX_STEPS = size * size * 4
            step_count = 0
            list_env = []

            while not agent.finished() and step_count < MAX_STEPS:
                print(f"\n=== STEP {step_count + 1} ===")
                print(f"Agent at ({agent.x}, {agent.y})")

                current_cell = env.grid[agent.y][agent.x]
                if current_cell.wumpus:
                    print(f"[MAIN] WARNING: Agent is on Wumpus cell!")
                if current_cell.pit:
                    print(f"[MAIN] WARNING: Agent is on Pit cell!")

                action = agent.step()
                step_count += 1

                RESULT.append(((agent.x, agent.y), action, agent.point))
                MAPS.append(copy.deepcopy(env.grid))
                list_env.append(copy.deepcopy(env.grid))

                print(f"[MAIN] Step {step_count}: {action}, Score: {agent.point}")
                if action == "DIE" or agent.dead:
                    list_env.append(copy.deepcopy(env.grid))
                    print("[MAIN] Agent died!")
                    break
                elif action == "CLIMB":
                    list_env.append(copy.deepcopy(env.grid))
                    print("[MAIN] Agent successfully escaped!")
                    break
                elif action == "STAY":
                    list_env.append(copy.deepcopy(env.grid))
                    print("[MAIN] Agent has no safe moves")
                    break
            print(len(list_env))
            main_ui.showAgentMove(None, RESULT, MAPS, None, list_env, agent_mode = 0, agent_index = 0)

            write_map_to_file("output/wumpus_world_map_advanced.txt", env.grid)
            write_output(file_path="output/result.txt", agent=agent, RES=RESULT)

            print(f"\n=== FINAL RESULTS ===")
            print(f"Steps taken: {step_count}")
            print(f"Final score: {agent.point}")
            print(f"Gold collected: {agent.has_gold}")
            print(f"Agent escaped: {agent.finished()}")
            print(f"Agent died: {agent.dead}")
            # pass
            #########################################################################333
        else:
            # ADVANCED DOUBLE AGENT
            env = EnvironmentAdvanced(size=size, k=wumpus_count, pit_prob=pit_prob)
            original_grid = copy.deepcopy(env.grid)
            original_wumpus_positions = env.wumpus_positions.copy()

            # Agent 1 (AgentAdvanced)
            inference1 = InferenceAdvanced(size, env)
            agent1 = AgentAdvanced(env, inference1)
            MAPS1, RESULT1 = [copy.deepcopy(env.grid)], []
            step_count1 = 0
            MAX_STEPS = size * size * 4
            list_env1 = []

            print("Agent 1 (Advanced A*) result:")
            while not agent1.finished() and step_count1 < MAX_STEPS:
                print(f"\n=== STEP {step_count1 + 1} ===")
                print(f"Agent at ({agent1.x}, {agent1.y})")
                
                current_cell = env.grid[agent1.y][agent1.x]
                if current_cell.wumpus:
                    print(f"[MAIN] WARNING: Agent is on Wumpus cell!")
                if current_cell.pit:
                    print(f"[MAIN] WARNING: Agent is on Pit cell!")
                
                action = agent1.step()
                step_count1 += 1
                RESULT1.append(((agent1.x, agent1.y), action, agent1.point))
                MAPS1.append(copy.deepcopy(env.grid))
                list_env1.append(copy.deepcopy(env.grid))
                
                print(f"[MAIN] Step {step_count1}: {action}, Score: {agent1.point}")
                
                if action == "DIE" or agent1.dead:
                    list_env1.append(copy.deepcopy(env.grid))
                    print("[MAIN] Agent 1 died!")
                    break
                elif action == "CLIMB":
                    list_env1.append(copy.deepcopy(env.grid))
                    print("[MAIN] Agent 1 successfully escaped!")
                    break
                elif action == "STAY":
                    list_env1.append(copy.deepcopy(env.grid))
                    print("[MAIN] Agent 1 has no safe moves")
                    break

            # Agent 2 - tạo lại environment từ map gốc
            env2 = EnvironmentRandomAdvanced(size=size, k=wumpus_count, pit_prob=pit_prob)
            env2.grid = copy.deepcopy(original_grid)
            env2.wumpus_positions = original_wumpus_positions.copy()

            inference2 = InferenceRandomAdvanced(size, env2)
            agent2 = AgentRandomAdvanced(env2, inference2)  # Hoặc AgentAdvanced nếu muốn cả 2 đều A*

            MAPS2, RESULT2 = [copy.deepcopy(env2.grid)], []
            step_count2 = 0
            list_env2 = []

            print("Agent 2 (Random) result:")
            while not agent2.finished() and step_count2 < MAX_STEPS:
                print(f"\n=== STEP {step_count2 + 1} ===")
                print(f"Agent at ({agent2.x}, {agent2.y})")
                
                current_cell = env2.grid[agent2.y][agent2.x]
                if current_cell.wumpus:
                    print(f"[MAIN] WARNING: Agent is on Wumpus cell!")
                if current_cell.pit:
                    print(f"[MAIN] WARNING: Agent is on Pit cell!")
                
                action = agent2.step()
                step_count2 += 1
                RESULT2.append(((agent2.x, agent2.y), action, agent2.point))
                MAPS2.append(copy.deepcopy(env2.grid))

                list_env2.append(copy.deepcopy(env2.grid))
                
                print(f"[MAIN] Step {step_count2}: {action}, Score: {agent2.point}")
                
                if action == "DIE" or agent2.dead:
                    list_env2.append(copy.deepcopy(env2.grid))
                    print("[MAIN] Agent 2 died!")
                    break
                elif action == "CLIMB":
                    list_env2.append(copy.deepcopy(env2.grid))
                    print("[MAIN] Agent 2 successfully escaped!")
                    break
                elif action == "STAY":
                    list_env2.append(copy.deepcopy(env2.grid))
                    print("[MAIN] Agent 2 has no safe moves")
                    break

            # Hiển thị kết quả từng agent
            print("\n=== SHOWING AGENT 1 RESULTS ===")
            main_ui.showAgentMove(None, RESULT1, MAPS1, None, list_env1, agent_mode=1, agent_index=0)
            
            print("\n=== SHOWING AGENT 2 RESULTS ===")
            main_ui.showAgentMove(None, RESULT2, MAPS2, None, list_env2, agent_mode=1, agent_index=1)

            # Ghi file kết quả
            write_output(file_path="output/result_agent1_advanced.txt", agent=agent1, RES=RESULT1)
            write_output(file_path="output/result_agent2_advanced.txt", agent=agent2, RES=RESULT2)
            write_map_to_file("output/wumpus_world_map_advanced_double.txt", original_grid)

            print(f"\n=== FINAL COMPARISON ===")
            print(f"Agent 1 (Advanced A*): Steps: {step_count1}, Score: {agent1.point}, Gold: {agent1.has_gold}, Escaped: {agent1.finished()}")
            print(f"Agent 2 (Random): Steps: {step_count2}, Score: {agent2.point}, Gold: {agent2.has_gold}, Escaped: {agent2.finished()}")
            return


if __name__ == "__main__":
    while True:
        main()



# from wumpus.environment import Environment
# from wumpus.inference import Inference
# from wumpus.agent import Agent
# from ui import main_ui
# import copy
# from advanced.agent_advanced import AgentAdvanced
# from advanced.inference_advanced import InferenceAdvanced
# from advanced.environment_advanced import EnvironmentAdvanced
# from rand.agent_random import AgentRandom
# import os


# def write_output(file_path, agent, RES):
#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write("== WUMPUS WORLD AGENT RESULT ==\n\n")
#         f.write(f"Final score: {agent.point}\n")
#         f.write(f"Gold collected: {'Yes' if agent.has_gold else 'No'}\n")
#         f.write(f"Total steps: {len(RES)}\n\n")
#         f.write("Action log:\n")

#         for step, (pos, action, point) in enumerate(RES, 1):
#             f.write(f"Step {step:>2}: Pos {pos} - Action: {action:<15} | Point: {point}\n")

# def write_map_to_file(file_path, grid):
#     try:
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)
#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write("== WUMPUS WORLD MAP WITH COORDINATES ==\n\n")
#             size = len(grid)
#             for y in range(size):
#                 row_data = []
#                 for x in range(size):
#                     cell = grid[y][x]
#                     content = str(cell)
#                     row_data.append(f"{content}({x},{y})")
#                 f.write("  ".join(row_data) + "\n")
#         print(f"Map with coordinates written to {file_path}")
#     except Exception as e:
#         print(f"Error writing map to file: {e}")


# def main():
#     # Get configuration from user
#     config = main_ui.showMenu()
#     if config is None:
#         return

#     size, pit_prob, wumpus_count, game_mode, agent_mode = config
    
#     if game_mode == 0:
#         # NORMAL MODE
#         if agent_mode == 0:
#             # Normal Single Agent
#             env = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
#             inference = Inference(size, env)
#             agent = Agent(env, inference)
            
#             print("Generated grid:", env.grid)
#             print("Grid type:", type(env.grid))
#             write_map_to_file("input/wumpus_world_map.txt", env.grid)

#             print(f"[MAIN] Created {size}x{size} world with {wumpus_count} Wumpus and {pit_prob} pit probability")
#             print(f"[MAIN] Game Mode: Normal")

#             # Show initial map
#             main_ui.showWumpusWorld(env.grid)

#             # Store map states for UI
#             MAPS = []
#             MAPS.append(copy.deepcopy(env.grid))

#             # Agent action results
#             RESULT = []
#             MAX_STEPS = size * size * 4
#             step_count = 0

#             # Main game loop
#             while not agent.finished() and step_count < MAX_STEPS:
#                 print(f"\n=== STEP {step_count + 1} ===")
#                 print(f"Agent at ({agent.x}, {agent.y})")
                
#                 # Check current cell for dangers (debug info)
#                 current_cell = env.grid[agent.y][agent.x]
#                 if current_cell.wumpus:
#                     print(f"[MAIN] WARNING: Agent is on Wumpus cell!")
#                 if current_cell.pit:
#                     print(f"[MAIN] WARNING: Agent is on Pit cell!")

#                 action = agent.step()
#                 step_count += 1

#                 # Record result với điểm số hiện tại của agent
#                 RESULT.append(((agent.x, agent.y), action, agent.point))
                
#                 # Ensure we capture the updated map state after an action
#                 if action == "SHOOT_HIT":
#                     print("[MAIN] Wumpus killed! Updating environment...")
#                     MAPS.append(copy.deepcopy(env.grid))
#                 else:
#                     MAPS.append(copy.deepcopy(env.grid))

#                 print(f"[MAIN] Step {step_count}: {action}, Score: {agent.point}")

#                 # Check terminal conditions
#                 if action == "DIE" or agent.dead:
#                     print("[MAIN] Agent died!")
#                     break
#                 elif action == "CLIMB":
#                     print("[MAIN] Agent successfully escaped!")
#                     break
#                 elif action == "STAY":
#                     print("[MAIN] Agent has no safe moves")
#                     break

#             # Show agent movement
#             main_ui.showAgentMove(None, RESULT, MAPS, None, None, agent_mode=0, agent_index=0)

#             # Write output
#             write_output(file_path="output/result.txt", agent=agent, RES=RESULT)

#             print(f"\n=== FINAL RESULTS ===")
#             print(f"Steps taken: {step_count}")
#             print(f"Final score: {agent.point}")
#             print(f"Gold collected: {agent.has_gold}")
#             print(f"Agent escaped: {agent.finished()}")
#             print(f"Agent died: {agent.dead}")
            
#         else:
#             # Normal Double Agent
#             env = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
#             original_grid = copy.deepcopy(env.grid)

#             # Agent 1 (A* Agent)
#             inference1 = Inference(size, env)
#             agent1 = Agent(env, inference1)
#             MAPS1, RESULT1 = [copy.deepcopy(env.grid)], []
#             step_count1 = 0
#             MAX_STEPS = size * size * 4

#             print("Agent 1 (A* Agent) result:")
#             while not agent1.finished() and step_count1 < MAX_STEPS:
#                 print(f"\n=== STEP {step_count1 + 1} ===")
#                 print(f"Agent at ({agent1.x}, {agent1.y})")
#                 action = agent1.step()
#                 step_count1 += 1
#                 RESULT1.append(((agent1.x, agent1.y), action, agent1.point))
#                 MAPS1.append(copy.deepcopy(env.grid))
#                 if action == "DIE" or agent1.dead or action == "CLIMB" or action == "STAY":
#                     break

#             # Agent 2 (Random Agent) - tạo lại environment từ map gốc
#             env2 = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
#             env2.grid = copy.deepcopy(original_grid)
#             inference2 = Inference(size, env2)
#             agent2 = AgentRandom(env2, inference2)
#             MAPS2, RESULT2 = [copy.deepcopy(env2.grid)], []
#             step_count2 = 0

#             print("Agent 2 (Random Agent) result:")
#             while not agent2.finished() and step_count2 < MAX_STEPS:
#                 print(f"\n=== STEP {step_count2 + 1} ===")
#                 print(f"Agent at ({agent2.x}, {agent2.y})")
#                 action = agent2.step()
#                 step_count2 += 1
#                 RESULT2.append(((agent2.x, agent2.y), action, agent2.point))
#                 MAPS2.append(copy.deepcopy(env2.grid))
#                 if action == "DIE" or agent2.dead or action == "CLIMB" or action == "STAY":
#                     break

#             # Hiển thị kết quả từng agent
#             print("\n=== SHOWING AGENT 1 RESULTS ===")
#             main_ui.showAgentMove(None, RESULT1, MAPS1, None, None, agent_mode=1, agent_index=0)
            
#             print("\n=== SHOWING AGENT 2 RESULTS ===")
#             main_ui.showAgentMove(None, RESULT2, MAPS2, None, None, agent_mode=1, agent_index=1)

#             # Ghi file kết quả
#             write_output(file_path="output/result_agent1_normal.txt", agent=agent1, RES=RESULT1)
#             write_output(file_path="output/result_agent2_normal.txt", agent=agent2, RES=RESULT2)
#             write_map_to_file("output/wumpus_world_map_normal_double.txt", original_grid)

#             print(f"\n=== FINAL COMPARISON ===")
#             print(f"Agent 1 (A*): Steps: {step_count1}, Score: {agent1.point}, Gold: {agent1.has_gold}, Escaped: {agent1.finished()}")
#             print(f"Agent 2 (Random): Steps: {step_count2}, Score: {agent2.point}, Gold: {agent2.has_gold}, Escaped: {agent2.finished()}")
#             return

#     else:
#         # ADVANCED MODE
#         if agent_mode == 0:
#             # Advanced Single Agent
#             env = EnvironmentAdvanced(size=size, k=wumpus_count, pit_prob=pit_prob)
#             inference = InferenceAdvanced(size, env)
#             agent = AgentAdvanced(env, inference)
            
#             write_map_to_file("input/wumpus_world_map_advanced.txt", env.grid)
            
#             print(f"[MAIN] Created {size}x{size} world with {wumpus_count} Wumpus and {pit_prob} pit probability")
#             print(f"[MAIN] Game Mode: Advanced")

#             main_ui.showWumpusWorld(env.grid)

#             MAPS = []
#             MAPS.append(copy.deepcopy(env.grid))
#             RESULT = []
#             MAX_STEPS = size * size * 4
#             step_count = 0
#             list_env = []

#             while not agent.finished() and step_count < MAX_STEPS:
#                 print(f"\n=== STEP {step_count + 1} ===")
#                 print(f"Agent at ({agent.x}, {agent.y})")

#                 current_cell = env.grid[agent.y][agent.x]
#                 if current_cell.wumpus:
#                     print(f"[MAIN] WARNING: Agent is on Wumpus cell!")
#                 if current_cell.pit:
#                     print(f"[MAIN] WARNING: Agent is on Pit cell!")

#                 action = agent.step()
#                 step_count += 1

#                 RESULT.append(((agent.x, agent.y), action, agent.point))
#                 MAPS.append(copy.deepcopy(env.grid))
#                 if step_count % 5 == 0 and step_count // 5 > 1:
#                     list_env.append(copy.deepcopy(env.grid))

#                 print(f"[MAIN] Step {step_count}: {action}, Score: {agent.point}")
#                 if action == "DIE" or agent.dead:
#                     list_env.append(copy.deepcopy(env.grid))
#                     print("[MAIN] Agent died!")
#                     break
#                 elif action == "CLIMB":
#                     list_env.append(copy.deepcopy(env.grid))
#                     print("[MAIN] Agent successfully escaped!")
#                     break
#                 elif action == "STAY":
#                     list_env.append(copy.deepcopy(env.grid))
#                     print("[MAIN] Agent has no safe moves")
#                     break
                    
#             print(f"List env length: {len(list_env)}")
#             main_ui.showAgentMove(None, RESULT, MAPS, None, list_env, agent_mode=0, agent_index=0)

#             write_map_to_file("output/wumpus_world_map_advanced.txt", env.grid)
#             write_output(file_path="output/result_advanced.txt", agent=agent, RES=RESULT)

#             print(f"\n=== FINAL RESULTS ===")
#             print(f"Steps taken: {step_count}")
#             print(f"Final score: {agent.point}")
#             print(f"Gold collected: {agent.has_gold}")
#             print(f"Agent escaped: {agent.finished()}")
#             print(f"Agent died: {agent.dead}")
            
#         else:
#             # ADVANCED DOUBLE AGENT
#             env = EnvironmentAdvanced(size=size, k=wumpus_count, pit_prob=pit_prob)
#             original_grid = copy.deepcopy(env.grid)
#             original_wumpus_positions = env.wumpus_positions.copy()

#             # Agent 1 (AgentAdvanced)
#             inference1 = InferenceAdvanced(size, env)
#             agent1 = AgentAdvanced(env, inference1)
#             MAPS1, RESULT1 = [copy.deepcopy(env.grid)], []
#             step_count1 = 0
#             MAX_STEPS = size * size * 4
#             list_env1 = []

#             print("Agent 1 (Advanced A*) result:")
#             while not agent1.finished() and step_count1 < MAX_STEPS:
#                 print(f"\n=== STEP {step_count1 + 1} ===")
#                 print(f"Agent at ({agent1.x}, {agent1.y})")
                
#                 current_cell = env.grid[agent1.y][agent1.x]
#                 if current_cell.wumpus:
#                     print(f"[MAIN] WARNING: Agent is on Wumpus cell!")
#                 if current_cell.pit:
#                     print(f"[MAIN] WARNING: Agent is on Pit cell!")
                
#                 action = agent1.step()
#                 step_count1 += 1
#                 RESULT1.append(((agent1.x, agent1.y), action, agent1.point))
#                 MAPS1.append(copy.deepcopy(env.grid))
                
#                 if step_count1 % 5 == 0 and step_count1 // 5 > 1:
#                     list_env1.append(copy.deepcopy(env.grid))
                
#                 print(f"[MAIN] Step {step_count1}: {action}, Score: {agent1.point}")
                
#                 if action == "DIE" or agent1.dead:
#                     list_env1.append(copy.deepcopy(env.grid))
#                     print("[MAIN] Agent 1 died!")
#                     break
#                 elif action == "CLIMB":
#                     list_env1.append(copy.deepcopy(env.grid))
#                     print("[MAIN] Agent 1 successfully escaped!")
#                     break
#                 elif action == "STAY":
#                     list_env1.append(copy.deepcopy(env.grid))
#                     print("[MAIN] Agent 1 has no safe moves")
#                     break

#             # Agent 2 - tạo lại environment từ map gốc
#             env2 = EnvironmentAdvanced(size=size, k=wumpus_count, pit_prob=pit_prob)
#             env2.grid = copy.deepcopy(original_grid)
#             env2.wumpus_positions = original_wumpus_positions.copy()
            
#             inference2 = InferenceAdvanced(size, env2)
#             agent2 = AgentRandom(env2, inference2)  # Hoặc AgentAdvanced nếu muốn cả 2 đều A*

#             MAPS2, RESULT2 = [copy.deepcopy(env2.grid)], []
#             step_count2 = 0
#             list_env2 = []

#             print("Agent 2 (Random) result:")
#             while not agent2.finished() and step_count2 < MAX_STEPS:
#                 print(f"\n=== STEP {step_count2 + 1} ===")
#                 print(f"Agent at ({agent2.x}, {agent2.y})")
                
#                 current_cell = env2.grid[agent2.y][agent2.x]
#                 if current_cell.wumpus:
#                     print(f"[MAIN] WARNING: Agent is on Wumpus cell!")
#                 if current_cell.pit:
#                     print(f"[MAIN] WARNING: Agent is on Pit cell!")
                
#                 action = agent2.step()
#                 step_count2 += 1
#                 RESULT2.append(((agent2.x, agent2.y), action, agent2.point))
#                 MAPS2.append(copy.deepcopy(env2.grid))
                
#                 if step_count2 % 5 == 0 and step_count2 // 5 > 1:
#                     list_env2.append(copy.deepcopy(env2.grid))
                
#                 print(f"[MAIN] Step {step_count2}: {action}, Score: {agent2.point}")
                
#                 if action == "DIE" or agent2.dead:
#                     list_env2.append(copy.deepcopy(env2.grid))
#                     print("[MAIN] Agent 2 died!")
#                     break
#                 elif action == "CLIMB":
#                     list_env2.append(copy.deepcopy(env2.grid))
#                     print("[MAIN] Agent 2 successfully escaped!")
#                     break
#                 elif action == "STAY":
#                     list_env2.append(copy.deepcopy(env2.grid))
#                     print("[MAIN] Agent 2 has no safe moves")
#                     break

#             # Hiển thị kết quả từng agent

        
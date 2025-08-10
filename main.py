from wumpus.environment import Environment
from wumpus.inference import Inference
from wumpus.agent import Agent
from ui import main_ui
import copy
from advanced.agent_advanced import AgentAdvanced
from advanced.inference_advanced import InferenceAdvanced
from advanced.environment_advanced import EnvironmentAdvanced
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

    size, pit_prob, wumpus_count, game_mode = config  # Updated to unpack 4 values
    if game_mode == 0:
        # Create environment and agent
        env = Environment(size=size, k=wumpus_count, pit_prob=pit_prob)
        inference = Inference(size, env)
        agent = Agent(env, inference)
        # Xuất bản đồ vào file trong folder input
        # Debug: In nội dung env.grid
        print("Generated grid:", env.grid)
        print("Grid type:", type(env.grid))

        write_map_to_file("input/wumpus_world_map.txt", env.grid)


        print(
            f"[MAIN] Created {size}x{size} world with {wumpus_count} Wumpus and {pit_prob} pit probability"
        )
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
        main_ui.showAgentMove(None, RESULT, MAPS, None, None)

        # Write output
        write_output(file_path="output/result.txt", agent=agent, RES=RESULT)

        print(f"\n=== FINAL RESULTS ===")
        print(f"Steps taken: {step_count}")
        print(f"Final score: {agent.point}")
        print(f"Gold collected: {agent.has_gold}")
        print(f"Agent escaped: {agent.finished()}")
        print(f"Agent died: {agent.dead}")
    else:
        # Game mode 1 (Advanced)
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
            if step_count % 5 == 0 and step_count // 5 > 1:
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
        main_ui.showAgentMove(None, RESULT, MAPS, None, list_env)

        write_map_to_file("output/wumpus_world_map_advanced.txt", env.grid)
        write_output(file_path="output/result.txt", agent=agent, RES=RESULT)

        print(f"\n=== FINAL RESULTS ===")
        print(f"Steps taken: {step_count}")
        print(f"Final score: {agent.point}")
        print(f"Gold collected: {agent.has_gold}")
        print(f"Agent escaped: {agent.finished()}")
        print(f"Agent died: {agent.dead}")
        # pass


if __name__ == "__main__":
    while True:
        main()

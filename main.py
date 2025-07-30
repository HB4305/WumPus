
from agent import *
from inference_engine import visited, knowledge
from GUI import*
from environment import grid, wumpus_alive, N
max_steps = 1000
steps = 0
percept = None
done = False

def step_game():
    global percept, done

    if done:
        return True

    print(f'Agent at {agent_pos}, facing {agent_dir}')
    print(f'Percept: {percept}')
    print(f'Known: {knowledge}')

    action = agent_decide(percept)
    print(f'Action: {action}')

    draw_grid(N, agent_pos, agent_dir, visited, grid, wumpus_alive, knowledge)

    if action == 'done':
        done = True
        return True

    result = move_agent(action)

    if isinstance(result, dict):
        percept = result
    else:
        done = True
        return True

    if is_dangerous(agent_pos):
        print("Agent died!")
        done = True
        return True

    if action == 'Climb':
        if has_gold:
            print("Agent climbed out with gold! SUCCESS")
        else:
            print("Agent climbed out WITHOUT gold.")
        done = True
        return True

    return False

def run_game():
    global percept, done
    done = False
    init_environment()
    percept = get_percept(agent_pos)
    init_gui(N, step_game)
    start_gui()

if __name__ == '__main__':
    run_game()

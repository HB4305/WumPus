import random

N = 8
K = 2
PIT_PROB = 0.2
grid = []  # Mỗi ô là dict: {'pit':bool, 'wumpus':None|int, 'gold':bool}
agent_pos = (0, 0)
agent_dir = 'E'  # Hướng: 'N', 'E', 'S', 'W'
arrow_used = False
wumpus_alive = []
gold_collected = False
steps_taken = 0

def init_environment():
    global grid, wumpus_alive
    grid.clear()
    wumpus_alive.clear()
    for x in range(N):
        row = []
        for y in range(N):
            row.append({'pit': False, 'wumpus': None, 'gold': False})
        grid.append(row)
    
    # Pits
    for x in range(N):
        for y in range(N):
            if (x, y) != (0, 0) and random.random() < PIT_PROB:
                grid[x][y]['pit'] = True

    # Wumpus
    count = 0
    while count < K:
        x, y = random.randint(0, N-1), random.randint(0, N-1)
        if (x, y) != (0, 0) and not grid[x][y]['pit'] and grid[x][y]['wumpus'] is None:
            grid[x][y]['wumpus'] = count
            wumpus_alive.append(True)
            count += 1

    # Gold
    while True:
        x, y = random.randint(0, N-1), random.randint(0, N-1)
        if (x, y) != (0, 0) and not grid[x][y]['pit'] and grid[x][y]['wumpus'] is None:
            grid[x][y]['gold'] = True
            break

def get_percept(pos):
    x, y = pos
    percept = {'stench': False, 'breeze': False, 'glitter': False, 'bump': False, 'scream': False}

    if grid[x][y]['gold']:
        percept['glitter'] = True

    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < N:
            if grid[nx][ny]['wumpus'] is not None and wumpus_alive[grid[nx][ny]['wumpus']]:
                percept['stench'] = True
            if grid[nx][ny]['pit']:
                percept['breeze'] = True

    return percept

def get_dir_offset(dir):
    return {'N': (0,1), 'E': (1,0), 'S': (0,-1), 'W': (-1,0)}[dir]

def turn_left(dir):
    return {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}[dir]

def turn_right(dir):
    return {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}[dir]

def shoot_arrow():
    x, y = agent_pos
    dx, dy = get_dir_offset(agent_dir)
    while 0 <= x+dx < N and 0 <= y+dy < N:
        x += dx
        y += dy
        if grid[x][y]['wumpus'] is not None:
            wumpus_id = grid[x][y]['wumpus']
            wumpus_alive[wumpus_id] = False
            return True
    return False


def move_agent(action):
    global agent_pos, agent_dir, steps_taken, arrow_used, gold_collected
    percept = {'stench': False, 'breeze': False, 'glitter': False, 'bump': False, 'scream': False}
    x, y = agent_pos
    steps_taken += 1

    if action == 'Move':
        dx, dy = get_dir_offset(agent_dir)
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < N:
            agent_pos = (nx, ny)
        else:
            percept['bump'] = True

    elif action == 'TurnLeft':
        agent_dir = turn_left(agent_dir)

    elif action == 'TurnRight':
        agent_dir = turn_right(agent_dir)

    elif action == 'Grab':
        if grid[x][y]['gold']:
            gold_collected = True
            grid[x][y]['gold'] = False

    elif action == 'Shoot':
        if not arrow_used:
            arrow_used = True
            percept['scream'] = shoot_arrow()

    elif action == 'Climb':
        if agent_pos == (0, 0):
            return 'done'

    # Cập nhật percept tại vị trí mới
    percept.update(get_percept(agent_pos))
    return percept


def is_dangerous(pos):
    x, y = pos
    # Nếu đang đứng vào ô có pit hoặc wumpus còn sống → chết
    if grid[x][y]['pit']:
        return True
    if grid[x][y]['wumpus'] is not None:
        wid = grid[x][y]['wumpus']
        if wumpus_alive[wid]:
            return True
    return False


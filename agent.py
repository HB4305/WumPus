from environment import* 
from inference_engine import*
from planner import*

path = []  # Danh sách vị trí cần đi tới
has_gold = False

def agent_decide(percept):
    global path, has_gold
    update_knowledge(agent_pos, percept)

    if percept['glitter']:
        has_gold = True
        return 'Grab'

    if has_gold:
        path = find_path(agent_pos, (0, 0))
        if not path:
            return 'Climb'

    # Tìm các ô an toàn chưa thăm
    if not path:
        targets = [p for p in knowledge if knowledge[p] == 'safe' and p not in visited]
        for t in targets:
            p = find_path(agent_pos, t)
            if p and len(p) > 0:
                path = p
                break

    # Nếu có đường đi
    if path:
        while path and path[0] == agent_pos:
            path.pop(0)
        if path:
            next_pos = path.pop(0)
            return move_to(agent_pos, next_pos)


    return 'Climb'


def move_to(curr, target):
    if curr == target:
        return 'Climb'

    dx = target[0] - curr[0]
    dy = target[1] - curr[1]

    if dx == 1:
        desired_dir = 'E'
    elif dx == -1:
        desired_dir = 'W'
    elif dy == 1:
        desired_dir = 'N'
    elif dy == -1:
        desired_dir = 'S'
    else:
        return 'Climb'  # fallback nếu lỗi

    if agent_dir == desired_dir:
        return 'Move'
    if turn_left(agent_dir) == desired_dir:
        return 'TurnLeft'
    if turn_right(agent_dir) == desired_dir:
        return 'TurnRight'

    # Nếu phải xoay 180 độ
    return 'TurnLeft'  # tạm thời, cho agent xoay dần về hướng đúng


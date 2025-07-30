from environment import* 
knowledge = {}  # {(x, y): 'safe' / 'maybe_pit' / 'maybe_wumpus' / 'unknown'}
visited = set()

def is_safe(pos):
    if pos in knowledge:
        return knowledge[pos] == 'safe'
    return False

def get_adjacent(pos):
    x, y = pos
    directions = [(0,1), (1,0), (-1,0), (0,-1)]
    return [(x+dx, y+dy) for dx, dy in directions if 0 <= x+dx < N and 0 <= y+dy < N]


def update_knowledge(pos, percept):
    x, y = pos
    visited.add(pos)
    
    adj = get_adjacent(pos)
    
    # Nếu không có breeze → các ô xung quanh an toàn khỏi pit
    if not percept['breeze']:
        for p in adj:
            if p not in knowledge or knowledge[p] != 'safe':
                knowledge[p] = 'safe'
    
    # Nếu có breeze → có thể có pit xung quanh
    if percept['breeze']:
        for p in adj:
            if p not in knowledge:
                knowledge[p] = 'maybe_pit'
    
    # Tương tự cho stench
    if not percept['stench']:
        for p in adj:
            if p not in knowledge or knowledge[p] != 'safe':
                knowledge[p] = 'safe'
    if percept['stench']:
        for p in adj:
            if p not in knowledge:
                knowledge[p] = 'maybe_wumpus'

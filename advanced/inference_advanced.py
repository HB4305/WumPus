from collections import defaultdict
from wumpus.inference import Inference  # import class gốc
from wumpus.utils import get_neighbors

class InferenceAdvanced(Inference):
    def __init__(self, size, environment):
        super().__init__(size, environment)
        self.last_wumpus_positions = set()
        self.action_count = 0
        self.percepts = {}  

    def update_knowledge(self, position, percept, action_count=None, agent_pos=None):
        if action_count is not None:
            self.action_count = action_count
        else:
            self.action_count += 1

        # lưu percept cho ô này (đè hoặc thêm)
        # đảm bảo percept là dict
        try:
            self.percepts[position] = percept.copy() if isinstance(percept, dict) else dict(percept)
        except Exception:
            self.percepts[position] = dict(percept) if percept is not None else {}

        super().update_knowledge(position, percept)

        if self.action_count > 0 and self.action_count % 5 == 0:
            self.update_wumpus_positions_after_move(agent_pos)

    def update_wumpus_positions_after_move(self, agent_pos=None):
        """
        Cập nhật vị trí Wumpus khả dĩ sau khi Wumpus có thể đã di chuyển 1 ô.
        Nếu phát hiện Wumpus di chuyển vào ô agent_pos -> trả về True (hoặc bạn có thể raise/đặt flag)
        """
        new_possible_positions = set()
        previous_positions = self.last_wumpus_positions or self.get_possible_wumpus()

        if not previous_positions:
            previous_positions = self.get_possible_wumpus()

        candidates = set()
        for pos in previous_positions:
            candidates.add(pos)
            candidates.update(get_neighbors(pos, self.size))

        candidates = {pos for pos in candidates if getattr(self, 'environment', None) is None or self.environment.is_valid(pos)}

        # Dựa vào percepts (stench) để lựa chọn vị trí khả dĩ
        for pos in candidates:
            neighbors = get_neighbors(pos, self.size)
            stench_count = sum(1 for n in neighbors if self.percepts.get(n, {}).get('stench', False))
            # nếu có ít nhất 1 neighbor có stench, xem như khả dĩ
            if stench_count >= 1:
                new_possible_positions.add(pos)

        # Nếu không tìm được vị trí dựa trên stench (ví dụ percepts chưa có)
        if not new_possible_positions:
            new_possible_positions = set(previous_positions)

        # Cập nhật kb: xóa flag possible_wumpus ở những ô không nằm trong new_possible_positions
        for pos in list(self.get_possible_wumpus()):
            if pos not in new_possible_positions:
                self.kb.setdefault(pos, {})
                self.kb[pos]['possible_wumpus'] = False
                self.kb[pos]['safe'] = True

        for pos in new_possible_positions:
            self.kb.setdefault(pos, {})
            self.kb[pos]['possible_wumpus'] = True
            self.kb[pos]['safe'] = False

        self.last_wumpus_positions = set(new_possible_positions)

        # nếu agent_pos được truyền và Wumpus có thể trùng ô agent => báo
        if agent_pos is not None and agent_pos in self.last_wumpus_positions:
            return True

        return False

    def get_possible_wumpus(self):
        # trả các ô trong kb flagged possible_wumpus True
        return {pos for pos, info in self.kb.items() if info.get('possible_wumpus', False)}

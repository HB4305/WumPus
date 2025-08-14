from collections import defaultdict
from wumpus.inference import Inference  # import class gốc
from wumpus.utils import get_neighbors

class InferenceAdvanced(Inference):
    def __init__(self, size, environment):
        super().__init__(size, environment)
        self.last_wumpus_positions = set()
        self.action_count = 0

    def update_wumpus_positions_after_move(self, agent_pos):
        """
        Cập nhật vị trí Wumpus khả dĩ sau khi Wumpus di chuyển 1 ô.
        Nếu Wumpus di chuyển vào ô agent => báo agent chết bằng Exception.
        """
        new_possible_positions = set()
        previous_positions = self.last_wumpus_positions or self.get_possible_wumpus()

        candidates = set()
        for pos in previous_positions:
            candidates.add(pos)
            candidates.update(get_neighbors(pos, self.size))

        # Lọc vị trí hợp lệ (không phải tường, pit, hoặc chồng wumpus khác)
        candidates = {pos for pos in candidates if self.environment.is_valid(pos)}

        # Dựa vào percept stench, lọc vị trí Wumpus khả dĩ
        for pos in candidates:
            neighbors = get_neighbors(pos, self.size)
            stench_count = sum(1 for n in neighbors if self.percepts.get(n, {}).get('stench', False))
            # Wumpus tạo stench ở các neighbors => chọn vị trí có ít nhất 1 stench neighbor
            if stench_count >= 1:
                new_possible_positions.add(pos)

        # Cập nhật kb
        for pos in self.confirmed_wumpus:
            if pos not in new_possible_positions:
                self.kb[pos]['possible_wumpus'] = False
                self.kb[pos]['safe'] = True

        for pos in new_possible_positions:
            for pos in new_possible_positions:
                self.kb[pos]['possible_wumpus'] = True
                self.kb[pos]['safe'] = False

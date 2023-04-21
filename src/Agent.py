import threading
from random import choice


class Agent(threading.Thread):
    def __init__(self, current_pos, target_pos, color):
        super().__init__()
        # pos = (col, row) due to PyGame conventions
        self.current_pos = current_pos
        self.target_pos = target_pos
        self.color = color

    def compute_path_to_target(self):
        direction = None
        diff_tuple = tuple(self.target_pos[i] - self.current_pos[i] for i in range(len(self.target_pos)))
        non_zero_indexes = [i for i in range(len(diff_tuple)) if diff_tuple[i] != 0]
        if non_zero_indexes:
            index = choice(non_zero_indexes)
            if index == 0:
                if diff_tuple[index] > 0:
                    direction = (1, 0)
                else:
                    direction = (-1, 0)
            else:
                if diff_tuple[index] > 0:
                    direction = (0, 1)
                else:
                    direction = (0, -1)
        return direction

    def move(self, coord):
        self.current_pos = (self.current_pos[0] + coord[0], self.current_pos[1] + coord[1])

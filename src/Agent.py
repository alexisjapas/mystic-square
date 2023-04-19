import threading


class Agent(threading.Thread):
    def __init__(self, current_pos, target_pos, color):
        super().__init__()
        # pos = (col, row) due to PyGame conventions
        self.current_pos = current_pos
        self.target_pos = target_pos
        self.color = color

    def compute_path_to_target(self):
        pass  # TODO

    def move(self):
        pass  # TODO
        #

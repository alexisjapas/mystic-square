import threading
from random import choice, uniform
from time import sleep
from typing import ClassVar


class Agent(threading.Thread):
    n_agents: ClassVar[int] = 0
    grid_dim: ClassVar[int]

    def __init__(
        self, _id, current_pos, target_pos, color, positions, stats, heatmap, lock
    ):
        super().__init__()
        self._id = _id
        Agent.n_agents += 1
        # pos = (col, row) due to PyGame conventions
        self.current_pos = current_pos
        self.target_pos = target_pos
        self.distance = sum(
            [abs(self.target_pos[i] - self.current_pos[i]) for i in range(2)]
        )
        self.color = color
        self.positions = positions
        self.stats = stats
        self.heatmap = heatmap
        self.lock = lock
        self.err_rate = 0.1
        self._stop_event = threading.Event()

    def has_reach_target(self):
        return not any(
            [
                self.target_pos[i] - self.current_pos[i]
                for i in range(len(self.current_pos))
            ]
        )

    def is_position_valid(self, position):
        return all(
            [
                position[i] >= 0 and position[i] < Agent.grid_dim
                for i in range(len(position))
            ]
        )

    def compute_path_to_target(self):
        direction = None
        diff_tuple = tuple(
            self.target_pos[i] - self.current_pos[i]
            for i in range(len(self.target_pos))
        )
        non_zero_indexes = [
            i
            for i in range(len(diff_tuple))
            if diff_tuple[i] != 0 or self.err_rate > uniform(0, 1)
        ]
        if non_zero_indexes:
            index = choice(non_zero_indexes)
            good_decision = 1 if uniform(0, 1) > self.err_rate else -1
            if index == 0:
                if diff_tuple[index] > 0:
                    direction = (1 * good_decision, 0)
                else:
                    direction = (-1 * good_decision, 0)
            else:
                if diff_tuple[index] > 0:
                    direction = (0, 1 * good_decision)
                else:
                    direction = (0, -1 * good_decision)
        return direction

    def move(self, new_position):
        self.current_pos = new_position

    def run(self):
        while True:
            # death
            if self._stop_event.is_set():
                print(f"Agent {self._id} died :(")
                break

            # logic
            sleep(1)
            self.distance = sum(
                [abs(self.target_pos[i] - self.current_pos[i]) for i in range(2)]
            )
            direction = self.compute_path_to_target()
            if direction:
                with self.lock:
                    new_position = tuple(
                        self.current_pos[i] + direction[i]
                        for i in range(len(direction))
                    )
                    if self.is_position_valid(new_position):
                        if new_position not in self.positions:
                            self.positions[self._id] = new_position
                            self.move(new_position)
                            self.heatmap[self._id] = 0
                            self.stats["moves_count"] += 1
                        else:
                            self.heatmap[self.positions.index(new_position)] += 1

    def die(self):
        self._stop_event.set()

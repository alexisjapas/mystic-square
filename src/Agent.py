import threading
from random import choice, choices, shuffle
from time import sleep
from typing import ClassVar
from collections import Counter


class Agent(threading.Thread):
    n_agents: ClassVar[int] = 0
    sleep_duration: ClassVar[float]
    grid_dim: ClassVar[int]

    def __init__(
        self,
        _id,
        current_pos,
        target_pos,
        color,
        positions,
        stats,
        heatmap,
        lock,
        barrier,
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
        self.barrier = barrier
        self.random_mode = True
        self.active_mode = False
        self.requests_count = 0
        self.patience_max = 100
        self.patience = 100
        self._stop_event = threading.Event()

    def has_reach_target(self):
        return not any(
            [
                self.target_pos[i] - self.current_pos[i]
                for i in range(len(self.current_pos))
            ]

        )

    def is_position_valid(self, position):
        return position is not None and all(
            [
                position[i] >= 0 and position[i] < Agent.grid_dim
                for i in range(len(position))
            ]
        )

    def compute_path_to_target(self):
        new_position = None
        diff_tuple = tuple(
            self.target_pos[i] - self.current_pos[i]
            for i in range(len(self.target_pos))
        )
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
            new_position = tuple(
                self.current_pos[i] + direction[i] for i in range(len(direction))
            )
        return new_position

    def move(self, new_position):
        self.current_pos = new_position

    def get_possible_positions(self):
        pos = [
            (col, self.current_pos[1])
            for col in range(
                max(0, self.current_pos[0] - 1),
                min(self.grid_dim, self.current_pos[0] + 2),
            )
            if col != self.current_pos[0]
        ]
        pos_row = [
            (self.current_pos[0], row)
            for row in range(
                max(0, self.current_pos[1] - 1),
                min(self.grid_dim, self.current_pos[1] + 2),
            )
            if row != self.current_pos[1]
        ]
        pos.extend(pos_row)
        shuffle(pos)
        return pos

    def run(self):
        while True:
            # death
            if self._stop_event.is_set():
                break

            # stats computing
            self.distance = sum(
                [abs(self.target_pos[i] - self.current_pos[i]) for i in range(2)]
            )

            # run
            if self.random_mode:
                with self.lock:
                    if self.stats["random_moves"] < 1:
                        self.random_mode = False
                possible_positions = self.get_possible_positions()
                with self.lock:
                    free_positions = [
                        p for p in possible_positions if p not in self.positions
                    ]
                    if free_positions:
                        new_position = choice(free_positions)
                    else:
                        new_position = None

                if new_position:
                    with self.lock:
                        self.positions[self._id] = new_position  # shared
                        self.move(new_position)
                        self.stats["random_moves"] -= 1  # shared
                sleep(0.00001)
            elif not self.active_mode:
                # print(f"Agent {self._id} on duty!")
                self.active_mode = True
                self.barrier.wait()
            else:
                with self.lock:
                    if len(self.heatmap[self._id]) != self.requests_count:
                        self.patience = self.patience_max
                        self.requests_count = len(self.heatmap[self._id])
                    elif self.requests_count > 0:
                        self.patience -= 1
                    if self.patience < 1:
                        self.heatmap[self._id].clear()
                        self.requests_count = 0
                        self.patience = self.patience_max

                if len(self.heatmap[self._id]) > 13:
                    # get unique requests sorted by count
                    counts = Counter(self.heatmap[self._id])
                    sorted_counts = counts.most_common()
                    requests = [r[0] for r in sorted_counts]

                    # compute possible positions and add them to solutions
                    possible_positions = self.get_possible_positions()
                    for p in possible_positions:
                        if p not in requests:
                            requests.append(p)

                    # pick a random element with more chances for those with lower index
                    weights = [w + 1 for w in range(len(requests))]
                    total_weights = sum(weights)
                    weights = [w / total_weights for w in weights]
                    new_position = choices(requests, weights=weights)[0]
                    with self.lock:
                        for p in requests:
                            if p not in self.positions:
                                new_position = p
                        self.heatmap[self._id].pop(0)
                else:
                    new_position = self.compute_path_to_target()

                if self.is_position_valid(new_position) and (
                    self.current_pos[0] != new_position[0]
                    or self.current_pos[1] != new_position[1]
                ):
                    with self.lock:
                        if new_position not in self.positions:
                            self.positions[self._id] = new_position  # shared
                            self.move(new_position)
                            self.heatmap[self._id].clear()  # shared
                            self.stats["moves_count"] += 1  # shared
                        else:
                            self.heatmap[self.positions.index(new_position)].append(
                                self.current_pos
                            )  # SHARED
                sleep(Agent.sleep_duration)

    def die(self):
        self._stop_event.set()

from random import randrange, randint
import threading


from Agent import Agent


class Solver:
    def __init__(self, grid_dim, nb_agents):
        assert nb_agents < grid_dim * grid_dim
        self.grid_dim = grid_dim
        self.nb_agents = nb_agents
        Agent.grid_dim = grid_dim
        self.agents = self.init_agents()

    def init_agents(self):
        def _pop_random_element(lst):
            random_index = randrange(len(lst))
            return lst.pop(random_index)

        # generate random positions
        start_positions = [
            (col, row) for row in range(self.grid_dim) for col in range(self.grid_dim)
        ]
        target_positions = start_positions.copy()

        # init shared memory
        lock = threading.Lock()
        self.positions = [
            _pop_random_element(start_positions) for _ in range(self.nb_agents)
        ]
        self.stats = {"moves_count": 0}
        self.heatmap = [0 for _ in range(self.nb_agents)]

        # generate agents
        return [
            Agent(
                i,
                self.positions[i],
                _pop_random_element(target_positions),
                (randint(0, 255), randint(0, 255), randint(0, 255)),
                self.positions,
                self.stats,
                self.heatmap,
                lock,
            )
            for i in range(self.nb_agents)
        ]

    def start_agents(self):
        for agent in self.agents:
            agent.start()

    def kill_agents(self):
        for agent in self.agents:
            agent.die()

    def is_over(self):
        over = True
        for agent in self.agents:
            if not agent.has_reach_target():
                over = False
        return over

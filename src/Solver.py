from random import randrange, randint

from Agent import Agent


class Solver:
    def __init__(self, grid_dim, nb_agents):
        assert nb_agents < grid_dim * grid_dim
        self.grid_dim = grid_dim
        self.nb_agents = nb_agents
        self.agents = self.init_agents()
        self.is_over = False

    def init_agents(self):
        def _pop_random_element(lst):
            random_index = randrange(len(lst))
            return lst.pop(random_index)

        start_positions = [
            (x, y) for x in range(self.grid_dim) for y in range(self.grid_dim)
        ]
        target_positions = start_positions.copy()
        return [
            Agent(
                _pop_random_element(start_positions),
                _pop_random_element(target_positions),
                (randint(0, 255), randint(0, 255), randint(0, 255)),
            )
            for _ in range(self.nb_agents)
        ]

    def iterate(self):
        pass


if __name__ == "__main__":
    my_solver = Solver(5, 4)
    print("blabla")

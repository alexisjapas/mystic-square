from Agent import Agent
from random import randrange, randint


class Game:
    def __init__(self, grid_dim, nb_agents):
        self.grid_dim = grid_dim
        self.nb_agents = nb_agents
        self.agents = self.init_agents()

    def init_agents(self):
        def _pop_random_element(lst):
            random_index = randrange(len(lst))
            return lst.pop(random_index)

        start_positions = [(x, y) for x in range(self.grid_dim) for y in range(self.grid_dim)]
        target_positions = start_positions.copy()
        return [
            Agent(
                _pop_random_element(start_positions),
                _pop_random_element(target_positions),
                (randint(0, 255), randint(0, 255), randint(0, 255)),
            )
            for _ in range(self.nb_agents)
        ]


if __name__ == "__main__":
    myGame = Game(5, 4)
    print("blabla")

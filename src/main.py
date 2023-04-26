import pygame
import sys
import random

from Solver import Solver
from Display import Display


def main(grid_dim, nb_agents, seed=0):
    # init seed
    random.seed(seed)

    # initialize the pygame environment
    pygame.init()
    clock = pygame.time.Clock()

    # initialize front end
    display = Display()

    # start the solver
    solver = Solver(grid_dim, nb_agents)
    display.init_game_display(solver)
    solver.start_agents()

    # solver loop
    while not solver.is_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                solver.kill_agents()
                pygame.quit()
                sys.exit()

        # update the diplay
        display.update()
        clock.tick(60)

    # kill agents
    solver.kill_agents()

    # final update
    display.update()

    # stats print
    print(f"Moves count: {solver.stats['moves_count']}")

    # quit pygame and clean up resources
    pygame.quit()


if __name__ == "__main__":
    main(5, 1, seed=10)

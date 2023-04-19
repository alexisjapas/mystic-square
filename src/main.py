import pygame
import sys

from Solver import Solver
from Display import Display


def main(grid_dim, nb_agents):
    # initialize the pygame environment
    pygame.init()
    clock = pygame.time.Clock()

    # initialize front end
    display = Display()

    # start the solver
    solver = Solver(grid_dim, nb_agents)
    display.start_solver(solver)

    # solver loop
    while not solver.is_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update the solver state
        solver.iterate()

        # update the diplay
        display.update()
        clock.tick(60)

    # quit pygame and clean up resources
    pygame.quit()


if __name__ == "__main__":
    main(27, 0)

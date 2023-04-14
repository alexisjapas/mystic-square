import pygame

from Solver import Solver
from Display import Display


def main(grid_dim, nb_agents):
    # initialize the pygame environment
    pygame.init()

    # initialize back/front ends
    display = Display()

    # start the solver
    solver = Solver(grid_dim, nb_agents)
    display.start_solver(solver)

    # solver loop
    while not solver.is_over:
        # update the solver state
        solver.iterate()

        # update the diplay
        display.update()

    # quit pygame and clean up resources
    pygame.quit()


if __name__ == "__main__":
    main(5, 4)

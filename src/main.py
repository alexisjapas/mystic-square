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
    display.init_menu_display()

    # menu loop
    display.in_menu = True
    while display.in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # update the diplay
        display.update_menu()
        clock.tick(60)

    pygame.display.quit()

    # start the solver
    solver = Solver(
        display.grid_size_selector.get_value()[0][1],
        display.nb_agents_selector.get_value()[0][1],
    )
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
        display.update_game()
        clock.tick(60)

    # kill agents
    solver.kill_agents()

    # final update
    display.update_game()

    # stats print
    print(f"Moves count: {solver.positions['moves_count']}")

    # quit pygame and clean up resources
    pygame.quit()


if __name__ == "__main__":
    main(5, 19, seed=0)

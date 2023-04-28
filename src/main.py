import pygame
import sys
import random

from Solver import Solver
from Display import Display


def menu(display):
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

    pygame.display.quit()



def main():
    # initialize the pygame environment
    pygame.init()
    clock = pygame.time.Clock()

    # initialize front end
    display = Display()

    while(True): 
        menu(display)

        for i in range(display.nb_simulations_selector.get_value()[0][1]):
            # init seed
            seed = random.randint(0, 1000)
            random.seed(seed)


            # start the solver
            solver = Solver(
                display.grid_size_selector.get_value()[0][1],
                display.nb_agents_selector.get_value()[0][1],
            )
            display.init_game_display(solver)
            solver.start_agents(display.agents_sleeps_duration_selector.get_value()[0][1])

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
            print(f"Moves count: {solver.stats['moves_count']}")


if __name__ == "__main__":
    main()

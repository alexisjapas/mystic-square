import pygame


class Display:
    def __init__(self, screen_size=(600, 600), bg_color=(255, 255, 255)):
        self.screen_size = screen_size
        self.bg_color = bg_color
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Mystic Square Solver")

    def start_solver(self, solver):
        # Initialize and prepare the solver
        self.solver = solver

    def update(self):
        # Update the game display based on the game state
        self.screen.fill(self.bg_color)
        self.draw_board()
        pygame.display.flip()

    def draw_board(self):
        # Draw the game board on the screen
        pass

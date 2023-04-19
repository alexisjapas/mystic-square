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
        self.cell_size = self.screen_size[0] // solver.grid_dim
        if self.cell_size != self.screen_size[0] / solver.grid_dim:
            size = solver.grid_dim * self.cell_size
            self.screen = pygame.display.set_mode((size, size))
        self.init_board()

    def init_board(self):
        # Draw the game board on the screen
        self.board = [
            [
                pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                for x in range(self.solver.grid_dim)
            ]
            for y in range(self.solver.grid_dim)
        ]

    def draw_board(self):
        for y in range(self.solver.grid_dim):
            for x in range(self.solver.grid_dim):
                pygame.draw.rect(self.screen, (0, 0, 0), self.board[x][y], 1)

    def draw_agents(self):
        pass

    def update(self):
        # Update the game display based on the game state
        self.screen.fill(self.bg_color)
        self.draw_board()
        self.draw_agents()
        pygame.display.flip()

import pygame


class Display:
    def __init__(self, bg_color=(255, 255, 255)):
        self.screen_size = (1400, 600)
        self.bg_color = bg_color
        pygame.display.set_caption("Mystic Square Solver")

    def start_solver(self, solver):
        # initialize and prepare the solver
        self.solver = solver

        # compute cells and board size
        self.cell_size = (self.screen_size[0] - 200) // (solver.grid_dim * 2)
        self.board_size = solver.grid_dim * self.cell_size

        # change screen size if cells dont fill it
        mid_size = 200
        if (self.screen_size[0] - mid_size) % solver.grid_dim:
            mid_size -= (self.screen_size[0] - 200) % solver.grid_dim
            print(mid_size)

        # set screen size
        self.offset_x = self.board_size + mid_size
        self.screen = pygame.display.set_mode((2 * self.board_size + mid_size, self.board_size))

        # init boards
        self.board_agents = self.init_board()
        self.board_target = self.init_board(self.offset_x)

    def init_board(self, offset_x=0):
        # Draw the game board on the screen
        return [
            [
                pygame.Rect(
                    offset_x + x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                for x in range(self.solver.grid_dim)
            ]
            for y in range(self.solver.grid_dim)
        ]

    def draw_board(self, board):
        for y in range(self.solver.grid_dim):
            for x in range(self.solver.grid_dim):
                pygame.draw.rect(self.screen, (0, 0, 0), board[x][y], 1)

    def draw_agents(self, mode="current"):
        pass

    def update(self):
        # Update the game display based on the game state
        self.screen.fill(self.bg_color)
        self.draw_board(self.board_agents)
        self.draw_board(self.board_target)
        self.draw_agents()
        self.draw_agents()
        pygame.display.flip()

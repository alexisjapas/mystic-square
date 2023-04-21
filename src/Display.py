import pygame


class Display:
    def __init__(self, bg_color=(255, 255, 255)):
        self.screen_size = (1400, 600)
        self.bg_color = bg_color
        pygame.display.set_caption("Mystic Square Solver")

    def init_game_display(self, solver):
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
        self.offset_col = self.board_size + mid_size
        self.screen = pygame.display.set_mode(
            (2 * self.board_size + mid_size, self.board_size)
        )

        # init boards
        self.board_agents = self.init_board()
        self.board_target = self.init_board(self.offset_col)

    def init_board(self, offset_col=0):
        # Draw the game board on the screen
        return [
            [
                pygame.Rect(
                    offset_col + col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                for row in range(self.solver.grid_dim)
            ]
            for col in range(self.solver.grid_dim)
        ]

    def draw_board(self, board):
        for col in range(self.solver.grid_dim):
            for row in range(self.solver.grid_dim):
                pygame.draw.rect(self.screen, (0, 0, 0), board[col][row], 1)

    def draw_agents(self, mode="current"):
        assert mode == "current" or mode == "target"
        board = self.board_agents if mode == "current" else self.board_target
        for agent in self.solver.agents:
            pos = agent.current_pos if mode == "current" else agent.target_pos
            pygame.draw.rect(self.screen, agent.color, board[pos[0]][pos[1]], 0)

    def update(self):
        # Update the game display based on the game state
        self.screen.fill(self.bg_color)
        self.draw_agents("current")
        self.draw_agents("target")
        self.draw_board(self.board_agents)
        self.draw_board(self.board_target)
        pygame.display.flip()

import pygame
import pygame_menu


class Display:
    def __init__(self, bg_color=(255, 255, 255)):
        self.screen_size = (1400, 600)
        self.bg_color = bg_color
        pygame.display.set_caption("Mystic Square Solver")

    def init_menu_display(self):
        self.in_menu = True
        self.menu_size = 600
        self.menu_screen = pygame.display.set_mode((self.menu_size, self.menu_size))

    def draw_menu(self):
        def handle_selector_change(value, selector):
            self.max_agents = (value[0][1]) * (value[0][1]) - 1
            self.nb_agents_selector.update_items([(f"{i+1}", i + 1) for i in range(self.max_agents)])

        self.menu_screen.fill(self.bg_color)
        self.max_agents = 8
        self.menu = pygame_menu.Menu(
            "Edit Simulation Parameters",
            self.menu_size,
            self.menu_size,
            theme=pygame_menu.themes.THEME_DEFAULT,
        )
        self.grid_size_selector = self.menu.add.selector(
            "Grid Size: ",
            [(f"{i} x {i}", i) for i in range(3, 16)],
            onchange=handle_selector_change,
        )
        self.nb_agents_selector = self.menu.add.selector(
            "Number Of Agents: ", [(f"{i+1}", i + 1) for i in range(self.max_agents)]
        )
        self.menu.add.vertical_margin(50)

        def on_start_button_click():
            self.in_menu = False
            self.menu.disable()

        self.start_button = self.menu.add.button("Launch Simulation", on_start_button_click)

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
        self.screen = pygame.display.set_mode((2 * self.board_size + mid_size, self.board_size))

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

    def draw_text(self, font, text, center_col, center_row, color=(0, 0, 0)):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (center_col, center_row)
        self.screen.blit(text_surface, text_rect)

    def draw_simulation_info(self, offset_col=700):
        font = pygame.font.Font(None, 24)

        # grid size
        self.draw_text(font, "GRID SIZE", offset_col, 10)
        self.draw_text(font, f"{self.solver.grid_dim} x {self.solver.grid_dim}", offset_col, 30)

        # number of agents
        self.draw_text(font, "NUMBER OF AGENTS", offset_col, 70)
        self.draw_text(font, f"{int(self.solver.nb_agents)}", offset_col, 90)

        # number of moves
        self.draw_text(font, "MOVES COUNT", offset_col, 130)
        self.draw_text(font, f"{self.solver.positions['moves_count']}", offset_col, 150)

    def update_game(self):
        # Update the game display based on the game state
        self.screen.fill(self.bg_color)
        self.draw_agents("current")
        self.draw_agents("target")
        self.draw_board(self.board_agents)
        self.draw_board(self.board_target)
        self.draw_simulation_info()
        pygame.display.flip()

    def update_menu(self):
        self.draw_menu()
        self.menu.mainloop(self.menu_screen)

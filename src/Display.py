import pygame
import pygame_menu
import sys


class Display:
    def __init__(self, bg_color=(255, 255, 255)):
        self.screen_size = 800
        self.bg_color = bg_color
        pygame.display.set_caption("Mystic Square Solver")

    def init_menu_display(self):
        self.in_menu = True
        self.menu_size = 800
        self.menu_screen = pygame.display.set_mode((self.menu_size, self.menu_size))

    def draw_menu(self):
        def _handle_selector_change(value, selector):
            print(value)
            self.max_agents = (value[0][1]) * (value[0][1]) - 1
            self.nb_agents_selector.update_items(
                [(f"{i}", i) for i in range(1, self.max_agents)]
            )

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
            onchange=_handle_selector_change,
        )
        self.nb_agents_selector = self.menu.add.selector(
            "Number Of Agents: ",
            [(f"{i}", i) for i in range(1, self.max_agents)],
            default=5,
        )
        self.nb_simulations_selector = self.menu.add.selector(
            "Number Of Simulation: ",
            [(f"{i}", i) for i in range(1, 100)],
        )
        self.agents_sleeps_duration_selector = self.menu.add.selector(
            "Agents Sleep Duration (seconds): ",
            [(f"{pow(10, -(4-i))}", pow(10, -(4 - i))) for i in range(5)],
        )
        self.seed = self.menu.add.selector(
            "Seed: ", [(f"{i}", i) for i in range(2001)], default=42
        )
        self.menu.add.vertical_margin(50)

        def _on_start_button_click():
            self.in_menu = False
            self.menu.disable()

        self.start_button = self.menu.add.button(
            "Launch Simulation", _on_start_button_click
        )

        def _on_exit_button_click():
            pygame.quit()
            sys.exit()

        self.exit_button = self.menu.add.button("Exit", _on_exit_button_click)

    def init_game_display(self, solver):
        # initialize and prepare the solver
        self.solver = solver

        # compute cells and board size
        self.cell_size = (self.screen_size - 200) // (solver.grid_dim * 2)
        self.board_size = solver.grid_dim * self.cell_size

        # change screen size if cells dont fill it
        mid_size = 200
        if (self.screen_size - mid_size) % solver.grid_dim:
            mid_size -= (self.screen_size - 200) % solver.grid_dim
            print(mid_size)

        # set screen size
        self.offset_col = self.screen_size - self.board_size
        self.offset_row = self.screen_size - self.board_size
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))

        # init boards
        self.board_agents = self.init_board(offset_col=0, offset_row=mid_size // 2)
        self.board_target = self.init_board(
            offset_col=self.offset_col, offset_row=mid_size // 2
        )
        self.board_heatmap = self.init_board(offset_col=0, offset_row=self.offset_row)
        self.board_distances = self.init_board(
            offset_col=self.offset_col, offset_row=self.offset_row
        )

    def init_board(self, offset_col=0, offset_row=0):
        # Draw the game board on the screen
        return [
            [
                pygame.Rect(
                    offset_col + col * self.cell_size,
                    offset_row + row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                for row in range(self.solver.grid_dim)
            ]
            for col in range(self.solver.grid_dim)
        ]

    def draw_board(self, board, board_name):
        for col in range(self.solver.grid_dim):
            for row in range(self.solver.grid_dim):
                pygame.draw.rect(self.screen, (0, 0, 0), board[col][row], 1)

        font = pygame.font.Font(None, 24)

        if (board_name == "Agents positions") or (
            board_name == "Agents blocking heatmap"
        ):
            title_pos = (int(self.board_size / 2), (board[0][0])[1] - 15)
        else:
            title_pos = (
                self.screen_size - int(self.board_size / 2),
                (board[0][0])[1] - 15,
            )
        self.draw_text(font, f"{board_name}", title_pos[0], title_pos[1])

    def draw_agents(self, mode="current"):
        assert mode == "current" or mode == "target"
        board = self.board_agents if mode == "current" else self.board_target
        for agent in self.solver.agents:
            pos = agent.current_pos if mode == "current" else agent.target_pos
            pygame.draw.rect(self.screen, agent.color, board[pos[0]][pos[1]], 0)

    def draw_distances(self):
        board = self.board_distances
        for agent in self.solver.agents:
            pos = agent.current_pos
            normalized_distance = 255 * agent.distance / (2 * self.solver.grid_dim)
            pygame.draw.rect(
                self.screen,
                (
                    255 - normalized_distance,
                    255 - normalized_distance,
                    255 - normalized_distance,
                ),
                board[pos[0]][pos[1]],
                0,
            )

    def draw_heatmap(self):
        board = self.board_heatmap
        for agent in self.solver.agents:
            pos = agent.current_pos
            weight = 3 * len(agent.heatmap[agent._id])
            if weight <= 255:
                color = (255, 255 - (weight), 255 - (weight))
            else:
                # cell turns black if the agent occupying it has been blocking others for too many iterations.
                color = (255, 0, 0)
            pygame.draw.rect(
                self.screen,
                color,
                board[pos[0]][pos[1]],
                0,
            )

    def draw_text(self, font, text, center_col, center_row, color=(0, 0, 0)):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (center_col, center_row)
        self.screen.blit(text_surface, text_rect)

    def draw_simulation_info(self):
        font = pygame.font.Font(None, 20)
        text_center_position = int(self.screen_size * 2.3 / 4)
        offset_col = self.screen_size // 2

        # grid size
        self.draw_text(
            font,
            "GRID SIZE",
            offset_col,
            int(text_center_position - 0.15 * text_center_position),
        )
        self.draw_text(
            font,
            f"{self.solver.grid_dim} x {self.solver.grid_dim}",
            offset_col,
            int(text_center_position - 0.1 * text_center_position),
        )

        # number of agents
        self.draw_text(font, "NUMBER OF AGENTS", offset_col, text_center_position)
        self.draw_text(
            font,
            f"{int(self.solver.nb_agents)}",
            offset_col,
            int(text_center_position + 0.05 * text_center_position),
        )

        # number of moves
        self.draw_text(
            font,
            "MOVES COUNT",
            offset_col,
            int(text_center_position + 0.15 * text_center_position),
        )
        self.draw_text(
            font,
            f"{self.solver.stats['moves_count']}",
            offset_col,
            int(text_center_position + 0.2 * text_center_position),
        )

    def update_game(self):
        # Update the game display based on the game state
        self.screen.fill(self.bg_color)
        self.draw_agents("current")
        self.draw_agents("target")
        self.draw_distances()
        self.draw_heatmap()
        self.draw_board(self.board_agents, "Agents positions")
        self.draw_board(self.board_target, "Agents targets")
        self.draw_board(self.board_distances, "Agents distance from target")
        self.draw_board(self.board_heatmap, "Agents blocking heatmap")
        self.draw_simulation_info()
        pygame.display.flip()

    def update_menu(self):
        self.draw_menu()
        self.menu.mainloop(self.menu_screen)

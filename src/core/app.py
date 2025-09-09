import pygame, sys, os, random
from ui.board import BOARD_SIZE, SQUARE_SIZE
from ui.layout import render_title, render_boards, render_buttons
from algorithms import bfs_rooks, dfs_rooks
import itertools

MARGIN = 120
BG_COLOR = (221, 211, 211)

class GameApp:
    def __init__(self, all_solutions):
        self.all_solutions = all_solutions
        self.left_solution = None
        all_solutions = list(itertools.permutations(range(8)))
        self.right_solution = random.choice(all_solutions)
        self.clock = pygame.time.Clock()

        self.window_width = 2 * (BOARD_SIZE * SQUARE_SIZE) + 3 * MARGIN
        self.window_height = BOARD_SIZE * SQUARE_SIZE + 2 * MARGIN + 100

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Bàn cờ vua - 8 rooks")

        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.caption_font = pygame.font.SysFont("Arial", 20, bold=True)

        self.rook_img = pygame.image.load(os.path.join("assets", "rook.png"))
        self.rook_img = pygame.transform.scale(self.rook_img, (SQUARE_SIZE, SQUARE_SIZE))

        # BFS animation state
        self.steps = None
        self.step_index = 0
        self.running_bfs = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if self.random_btn.collidepoint(mouse_pos):
                        all_solutions = list(itertools.permutations(range(8)))
                        self.right_solution = random.choice(all_solutions)
                    elif self.reset_btn.collidepoint(mouse_pos):
                        self.left_solution = None
                        self.steps = None
                        self.running_bfs = False
                    elif self.run_bfs_btn.collidepoint(mouse_pos):
                        self.steps = bfs_rooks(BOARD_SIZE, list(self.right_solution))
                        self.step_index = 0
                        self.running_bfs = True
                    elif self.run_dfs_btn.collidepoint(mouse_pos):
                        self.steps = dfs_rooks(BOARD_SIZE, list(self.right_solution))
                        self.step_index = 0
                        self.running_bfs = True

            # update BFS animation
            if self.running_bfs and self.steps:
                if self.step_index < len(self.steps):
                    self.left_solution = self.steps[self.step_index]
                    self.step_index += 1
                else:
                    self.running_bfs = False  # xong thì dừng

            self.screen.fill(BG_COLOR)

            render_title(self.screen, self.title_font, self.window_width)
            render_boards(
                self.screen,
                self.font,
                self.caption_font,
                self.rook_img,
                self.left_solution,
                self.right_solution,
                self.window_width
            )

            (self.random_btn, 
            self.reset_btn, 
            self.run_bfs_btn, 
            self.run_dfs_btn) = render_buttons(
                self.screen, self.font, self.window_width, self.window_height
            )

            pygame.display.flip()
            self.clock.tick(10000)  # giảm fps để thấy rõ animation

        pygame.quit()
        sys.exit()

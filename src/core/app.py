import pygame, sys, os, random
from ui.board import BOARD_SIZE, SQUARE_SIZE
from ui.layout import render_title, render_boards
from ui.buttons import (
    draw_group_buttons,
    draw_algorithm_buttons,
    draw_action_buttons,
    algorithm_groups
)
from algorithms import *
import itertools

MARGIN = 120
BG_COLOR = (221, 211, 211)

class GameApp:
    def __init__(self, all_solutions):
        self.all_solutions = list(itertools.permutations(range(8)))
        self.left_solution = None
        self.right_solution = random.choice(self.all_solutions)
        self.clock = pygame.time.Clock()

        self.window_width = 1400
        self.window_height = 800

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Bàn cờ vua - 8 rooks")

        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.caption_font = pygame.font.SysFont("Arial", 20, bold=True)

        self.rook_img = pygame.image.load(os.path.join("assets", "rook.png"))
        self.rook_img = pygame.transform.scale(self.rook_img, (SQUARE_SIZE, SQUARE_SIZE))

        # Animation
        self.steps = None
        self.step_index = 0
        self.running_algorithms = False

        # ✅ State cho menu mới
        self.selected_group = -1
        self.selected_algorithm = -1

    def run(self):
        running = True
        while running:
            # =================== EVENT ===================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    # Xử lý click nút Random/Reset
                    if self.rect_random.collidepoint(mouse_pos):
                        self.right_solution = random.choice(self.all_solutions)
                    elif self.rect_reset.collidepoint(mouse_pos):
                        self.left_solution = None
                        self.steps = None
                        self.running_algorithms = False

                    # Xử lý click group
                    for i, r in enumerate(self.group_rects):
                        if r.collidepoint(mouse_pos):
                            self.selected_group = i
                            self.selected_algorithm = -1
                            break

                    # Xử lý click algorithm
                    if self.selected_group >= 0:
                        group = algorithm_groups[self.selected_group]
                        for i, r in enumerate(self.algorithm_rects):
                            if r.collidepoint(mouse_pos):
                                self.selected_algorithm = i
                                alg_name = group["algorithms"][i]["name"]
                                self.run_algorithm_by_name(alg_name)
                                break

            # =================== UPDATE ANIMATION ===================
            if self.running_algorithms and self.steps:
                if self.step_index < len(self.steps):
                    self.left_solution.append(self.steps[self.step_index])
                    self.step_index += 1
                else:
                    self.running_algorithms = False

            # =================== DRAW ===================
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

            # Vẽ menu mới
            self.group_rects = draw_group_buttons(self.screen, self.font, self.selected_group)
            self.algorithm_rects = draw_algorithm_buttons(
                self.screen, self.font,
                self.selected_group, self.selected_algorithm
            )
            self.rect_random, self.rect_reset = draw_action_buttons(
                self.screen, self.font,
                self.window_width, self.window_height
            )

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()
        sys.exit()

    def run_algorithm_by_name(self, alg_name):
        """Chạy thuật toán dựa theo tên"""
        goal = list(self.right_solution)
        if "Breadth-First" in alg_name:
            result = breadth_first_search(BOARD_SIZE, goal)
        elif "Depth-First" in alg_name:
            result = depth_first_search(BOARD_SIZE, goal)
        elif "Depth Limited" in alg_name:
            result = depth_limited_search(BOARD_SIZE, goal)
        elif "Iterative Deepening" in alg_name:
            result = iterative_deepening_search(BOARD_SIZE, goal)
        elif "Uniform Cost" in alg_name:
            result = uniform_cost_search(BOARD_SIZE, goal, placement_cost_goal)

        elif "A*" in alg_name:
            result = a_star_search(BOARD_SIZE, goal, placement_cost_goal, h_misplaced)
        elif "Greedy" in alg_name:
            result = greedy_search(BOARD_SIZE, goal, h_misplaced)
            
        elif "Simulated Annealing" in alg_name:
            result = simulated_annealing(BOARD_SIZE, goal, h_misplaced)
        else:
            print("Thuật toán chưa được gán!")
            return

        if result:
            self.steps = result
            self.step_index = 0
            self.left_solution = []
            self.running_algorithms = True

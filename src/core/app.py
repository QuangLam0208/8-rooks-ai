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
        piece_size = int(SQUARE_SIZE * 0.8)  # 80% của ô
        self.rook_img = pygame.transform.scale(self.rook_img, (piece_size, piece_size))

        self.selected_algorithm_name = None  # tên thuật toán được chọn

        # Animation
        self.steps = None
        self.step_index = 0
        self.running_algorithms = False

        # State cho menu mới
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

                    if self.rect_run.collidepoint(mouse_pos):
                        if self.selected_algorithm_name:
                            self.run_algorithm_by_name(self.selected_algorithm_name)

                    elif self.rect_visual.collidepoint(mouse_pos):
                        if self.selected_algorithm_name:
                            self.run_visualization_by_name(self.selected_algorithm_name)

                    elif self.rect_random.collidepoint(mouse_pos):
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
                                self.selected_algorithm_name = group["algorithms"][i]["name"]
                                break

            # =================== UPDATE ANIMATION ===================
            if self.running_algorithms and self.steps:
                if self.step_index < len(self.steps):
                    self.left_solution = self.steps[self.step_index]
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
            self.rect_run, self.rect_visual, self.rect_random, self.rect_reset = draw_action_buttons(
                self.screen, self.font,
                self.window_width, self.window_height
            )

            pygame.display.flip()
            self.clock.tick(3)

        pygame.quit()
        sys.exit()

    def run_visualization_by_name(self, alg_name):
        """Chạy thuật toán và lưu các bước để visualize"""
        goal = list(self.right_solution)
        if "Breadth-First" in alg_name:
            result, steps = breadth_first_search(BOARD_SIZE, goal, return_steps=True)
        elif "Depth-First" in alg_name:
            result, steps = depth_first_search(BOARD_SIZE, goal, return_steps=True)
        elif "Depth Limited" in alg_name:
            result, steps, steps_round = depth_limited_search(BOARD_SIZE, goal, return_steps=True)
        elif "Iterative Deepening" in alg_name:
            result, steps, steps_round = iterative_deepening_search(BOARD_SIZE, goal, return_steps=True)
        elif "Uniform Cost" in alg_name:
            result, steps, steps_round = uniform_cost_search(BOARD_SIZE, goal, return_steps=True)
            
        elif "A*" in alg_name:
            result, steps, steps_round = a_star_search(BOARD_SIZE, goal, return_steps=True)
        elif "Greedy" in alg_name:
            result, steps = greedy_search(BOARD_SIZE, goal, return_steps=True)

        elif "Hill Climbing" in alg_name:
            result, steps, steps_round = hill_climbing(BOARD_SIZE, goal, return_steps=True)
        elif "Simulated Annealing" in alg_name:
            result, steps, steps_round  = simulated_annealing(BOARD_SIZE, goal, return_steps=True)
        elif "Genetic Algorithm" in alg_name:
            result, steps, steps_round = genetic_algorithm(BOARD_SIZE, goal, return_steps=True)
        elif "Beam Search" in alg_name:
            result, steps, steps_round = beam_search(BOARD_SIZE, goal, return_steps=True)

        elif "And Or" in alg_name:
            result, steps = and_or_bfs(BOARD_SIZE, goal, return_steps=True)
            
        else:
            print("Thuật toán chưa được gán!")
            return
        
        if steps:
            self.steps = steps
            self.step_index = 0
            self.left_solution = []
            self.running_algorithms = True

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
            result = uniform_cost_search(BOARD_SIZE, goal)
            
        elif "A*" in alg_name:
            result = a_star_search(BOARD_SIZE, goal)
        elif "Greedy" in alg_name:
            result = greedy_search(BOARD_SIZE, goal)

        elif "Hill Climbing" in alg_name:
            result = hill_climbing(BOARD_SIZE, goal)
        elif "Simulated Annealing" in alg_name:
            result = simulated_annealing(BOARD_SIZE, goal)
        elif "Genetic Algorithm" in alg_name:
            result = genetic_algorithm(BOARD_SIZE, goal)
        elif "Beam Search" in alg_name:
            result = beam_search(BOARD_SIZE, goal)

        elif "And Or" in alg_name:
            result = and_or_bfs(BOARD_SIZE, goal)

        else:
            print("Thuật toán chưa được gán!")
            return

        if result:
            steps = [result[:i] for i in range(1, len(result)+1)]
            self.steps = steps
            self.step_index = 0
            self.left_solution = []
            self.running_algorithms = True

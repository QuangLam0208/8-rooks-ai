import pygame, sys, os, random
from ui.layout import render_boards, draw_scrollable_panel
from ui.buttons import (
    draw_group_buttons,
    draw_algorithm_buttons,
    draw_action_buttons,
    algorithm_groups
)
from ui.stats_history import draw_stats_and_history
from algorithms import *
import ui.properties as props
import itertools

BG_COLOR = (221, 211, 211)

class GameApp:
    def __init__(self, all_solutions):
        self.all_solutions = list(itertools.permutations(range(props.BOARD_SIZE)))
        self.left_solution = None
        self.right_solution = random.choice(self.all_solutions)
        self.clock = pygame.time.Clock()

        self.window_width = props.WINDOW_WIDTH
        self.window_height = props.WINDOW_HEIGHT

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("8 ROOKS")

        # ===== Load font JosefinSans =====
        font_path = os.path.join("assets", "fonts", "JosefinSans-SemiBold.ttf")
        self.font = pygame.font.Font(font_path, 18)       # font chính
        self.caption_font = pygame.font.Font(font_path, 20)  # font caption (to hơn tí)

        self.rook_img = pygame.image.load(os.path.join("assets", "pics", "rook.png"))
        piece_size = int(props.SQUARE_SIZE * 0.8)  # 80% của ô
        self.rook_img = pygame.transform.scale(self.rook_img, (piece_size, piece_size))

        self.selected_algorithm_name = None  # tên thuật toán được chọn

        # Animation
        self.steps = None
        self.step_index = 0
        self.running_algorithms = False

        # State cho menu mới
        self.selected_group = -1
        self.selected_algorithm = -1

        self.current_stats = None
        self.history = []

        self.panel_logs = []
        self.scroll_offset = 0
        self.scroll_y = 0
        self.scroll_x = 0

    def prompt_board_size(self):
        input_text = ""
        box = pygame.Rect((self.window_width - 300)//2, (self.window_height - 80)//2, 300, 80)
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit():
                        input_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not box.collidepoint(event.pos):
                        active = False

            overlay = pygame.Surface((self.window_width, self.window_height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            pygame.draw.rect(self.screen, (255, 255, 255), box, border_radius=8)
            pygame.draw.rect(self.screen, (0, 0, 0), box, 2, border_radius=8)
            txt = input_text or "Enter size (3-8)"
            self.screen.blit(self.font.render(txt, True, (0, 0, 0)), (box.x + 10, box.y + 30))
            pygame.display.flip()
            self.clock.tick(30)

        # Khi người dùng nhập xong
        if input_text.isdigit():
            new_size = int(input_text)
            if 3 <= new_size <= 8:
                props.update_board_size(new_size)  # dùng props thay vì update_board_size trực tiếp
                self.reset_after_resize()

    def reset_after_resize(self):
        """Reset lại giao diện và dữ liệu sau khi đổi kích thước."""
        import itertools, random
        from ui import layout, stats_history

        self.all_solutions = list(itertools.permutations(range(props.BOARD_SIZE)))
        self.right_solution = random.choice(self.all_solutions)
        self.left_solution = None

        # Resize quân xe
        rook_path = os.path.join("assets", "pics", "rook.png")
        rook_img = pygame.image.load(rook_path)
        piece_size = int(props.SQUARE_SIZE * 0.8)
        self.rook_img = pygame.transform.scale(rook_img, (piece_size, piece_size))

        # Reset trạng thái
        self.steps = []
        self.step_index = 0
        self.running_algorithms = False
        self.panel_logs.clear()
        self.scroll_x = 0
        self.scroll_y = 0
        self.history.clear()
        self.current_stats = {
            "name": "", "expanded": 0, "frontier": 0,
            "visited": 0, "time": 0
        }

        # Reload lại các module layout phụ thuộc props
        import importlib
        importlib.reload(layout)
        importlib.reload(stats_history)

        print(f"UI reloaded with board {props.BOARD_SIZE}x{props.BOARD_SIZE}")

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
                        if props.BOARD_SIZE > 6:
                            self.panel_logs.clear()
                            self.panel_logs.append("Visualization disabled for board size > 6.")
                            self.scroll_y = 0
                            self.scroll_x = 0
                            continue
                        if self.selected_algorithm_name:
                            self.run_visualization_by_name(self.selected_algorithm_name)

                    elif self.rect_random.collidepoint(mouse_pos):
                        # ==================== TẠO BÀN CỜ PHẢI MỚI ====================
                        self.right_solution = random.choice(self.all_solutions)

                        # ==================== RESET TRẠNG THÁI ====================
                        self.left_solution = []
                        self.steps = []
                        self.step_index = 0
                        self.running_algorithms = False

                        # ==================== RESET THỐNG KÊ & LỊCH SỬ ====================
                        self.current_stats = {
                            "name": "",
                            "expanded": 0,
                            "frontier": 0,
                            "visited": 0,
                            "time": 0
                        }
                        self.history = []  # hoặc self.history.clear(), đều được

                        print("Đã random lại bàn cờ và reset toàn bộ thống kê!")

                    elif self.rect_reset.collidepoint(mouse_pos):
                        self.left_solution = None
                        self.steps = None
                        self.running_algorithms = False
                        self.panel_logs.clear()
                        self.scroll_offset = 0

                    elif self.rect_size.collidepoint(mouse_pos):
                        # Mở hộp nhập để đổi kích thước
                        self.prompt_board_size()

                    # Xử lý click group
                    for i, r in enumerate(self.group_rects):
                        if r.collidepoint(mouse_pos):
                            # Nếu nhóm này đã được chọn, nhấn lại sẽ bỏ chọn
                            if self.selected_group == i:
                                self.selected_group = -1
                                self.selected_algorithm = -1
                                self.selected_algorithm_name = None
                            else:
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

                elif event.type == pygame.MOUSEWHEEL:
                    SCROLL_SPEED_Y = 50   # tốc độ cuộn dọc
                    SCROLL_SPEED_X = 50   # tốc độ cuộn ngang

                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        # Cuộn ngang khi giữ Shift
                        self.scroll_x -= event.y * SCROLL_SPEED_X
                        max_width = max((self.font.size(line)[0] for line in self.panel_logs), default=0)
                        
                        # Tính tổng chiều rộng panel, sau đó trừ đi padding ngang (12px trái + 15px phải)
                        total_panel_width = (props.RIGHT_BOARD_X + props.BOARD_SIZE * props.SQUARE_SIZE) - props.LEFT_BOARD_X
                        visible_width = total_panel_width - (12 + 15)
                        
                        self.scroll_x = max(0, min(self.scroll_x, max(0, max_width - visible_width)))
                    else:
                        # Cuộn dọc
                        self.scroll_y -= event.y * SCROLL_SPEED_Y
                        max_height = len(self.panel_logs) * 22
                        
                        # Chiều cao thực tế của vùng hiển thị log (trừ padding top & bottom)
                        visible_height = props.TOTAL_LIST5_HEIGHT - (12 + 15) 
                        
                        self.scroll_y = max(0, min(self.scroll_y, max(0, max_height - visible_height)))

            # =================== UPDATE ANIMATION ===================
            if self.running_algorithms and self.steps:
                if self.step_index < len(self.steps):
                    self.left_solution = self.steps[self.step_index]
                    self.step_index += 1
                else:
                    self.running_algorithms = False

            # =================== DRAW ===================
            self.screen.fill(BG_COLOR)

            render_boards(
                self.screen,
                self.font,
                self.caption_font,
                self.rook_img,
                self.left_solution,
                self.right_solution,
                self.window_width
            )

            draw_scrollable_panel(self.screen, self.font, self.panel_logs, self.scroll_y, self.scroll_x)

            draw_stats_and_history(
                self.screen,
                self.font,
                self.font,   
                getattr(self, "current_stats", None),
                getattr(self, "history", []),
                self.running_algorithms
            )

            # Vẽ menu mới
            self.group_rects = draw_group_buttons(self.screen, self.font, self.selected_group)
            self.algorithm_rects = draw_algorithm_buttons(
                self.screen, self.font,
                self.selected_group, self.selected_algorithm
            )
            self.rect_run, self.rect_visual, self.rect_random, self.rect_reset, self.rect_size = draw_action_buttons(
                self.screen, self.font,
                props.LEFT_BOARD_X, props.RIGHT_BOARD_X, props.BOARD_SIZE * props.SQUARE_SIZE
            )

            pygame.display.flip()
            self.clock.tick(3)

        pygame.quit()
        sys.exit()

    def run_visualization_by_name(self, alg_name):
        """Visualization từng bước: mỗi lần nhấn hiển thị 1 bước + log chi tiết"""
        goal = list(self.right_solution)

        # Nếu chưa có steps => chạy thuật toán 1 lần
        if not self.steps:
            if "Breadth-First" in alg_name:
                result, steps, logs = breadth_first_search_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)
            elif "Depth-First" in alg_name:
                result, steps, logs = depth_first_search_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)    
            elif "Depth Limited" in alg_name:
                result, steps, logs = depth_limited_search_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)
            elif "Iterative Deepening" in alg_name:
                result, steps, logs = iterative_deepening_search_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)
            elif "Uniform Cost" in alg_name:
                result, steps, logs = uniform_cost_search_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)

            elif "A Star" in alg_name:
                result, steps, logs = a_star_search_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)
            elif "Greedy" in alg_name:
                result, steps, logs = greedy_best_search_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)

            elif "Hill" in alg_name:
                result, steps, logs = hill_climbing_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)
            elif "Simulated" in alg_name:
                result, steps, logs = simulated_annealing_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)
            elif "Genetic" in alg_name:
                result, steps, logs = genetic_algorithm_visual(props.BOARD_SIZE, goal, pop_size=20, return_steps=True, return_logs=True)
            elif "Beam" in alg_name:
                result, steps, logs = beam_search_visual(props.BOARD_SIZE, goal, beam_width=5, return_steps=True, return_logs=True)

            elif "Nondeterministic" in alg_name:
                result, steps, logs = and_or_search_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)
            elif "Unobservable" in alg_name:
                result, steps, logs = dfs_belief_search_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)
            elif "Partial Observable" in alg_name:
                result, steps, logs = dfs_partial_obs_visual(props.BOARD_SIZE, goal, return_steps=True, return_logs=True)

            else:
                print("Chức năng visualize chưa hỗ trợ thuật toán này nhá 😚")
                return

            self.steps = steps
            self.logs = logs
            self.step_index = 0
            self.left_solution = []
            self.panel_logs.clear()
            self.panel_logs.append("Visualization ready — press again to step through.")
            self.scroll_offset = 0
            return

        # Hiển thị từng bước + log tương ứng
        if self.step_index < len(self.steps):
            current_state = self.steps[self.step_index]
            self.left_solution = current_state

            if self.step_index < len(self.logs):
                self.panel_logs.append(self.logs[self.step_index])

                # --- Auto scroll NGAY LẬP TỨC khi có log mới ---
                line_height = 22
                total_height = len(self.panel_logs) * line_height
                visible_height = props.TOTAL_LIST5_HEIGHT - (12 + 15) # Sửa ở đây
                if total_height > visible_height:
                    # Đặt scroll_y thẳng đến cuối
                    self.scroll_y = total_height - visible_height

            self.step_index += 1
        else:
            self.panel_logs.append(f"GOAL: {self.left_solution}")
            # --- Khi đạt goal, cuộn thẳng xuống cuối ---
            line_height = 22
            total_height = len(self.panel_logs) * line_height
            visible_height = props.TOTAL_LIST5_HEIGHT - (12 + 15) # Sửa ở đây
            if total_height > visible_height:
                self.scroll_y = total_height - visible_height

    def run_algorithm_by_name(self, alg_name):
        """Chạy thuật toán dựa theo tên, cập nhật bảng thống kê & lịch sử"""
        goal = list(self.right_solution)
        result, steps, stats = None, None, None

        if "Breadth-First" in alg_name:
            result, steps, stats = breadth_first_search(props.BOARD_SIZE, goal)
        elif "Depth-First" in alg_name:
            result, steps, stats = depth_first_search(props.BOARD_SIZE, goal)
        elif "Depth Limited" in alg_name:
            result, steps, stats = depth_limited_search(props.BOARD_SIZE, goal)
        elif "Iterative Deepening" in alg_name:
            result, steps, stats = iterative_deepening_search(props.BOARD_SIZE, goal)
        elif "Uniform Cost" in alg_name:
            result, steps, stats = uniform_cost_search(props.BOARD_SIZE, goal)
            
        elif "A Star" in alg_name:
            result, steps, stats = a_star_search(props.BOARD_SIZE, goal)
        elif "Greedy" in alg_name:
            result, steps, stats = greedy_best_search(props.BOARD_SIZE, goal)

        elif "Hill" in alg_name:
            result, steps, stats = hill_climbing(props.BOARD_SIZE, goal)
        elif "Simulated" in alg_name:
            result, steps, stats = simulated_annealing(props.BOARD_SIZE, goal)
        elif "Genetic" in alg_name:
            result, steps, stats = genetic_algorithm(props.BOARD_SIZE, goal)
        elif "Beam" in alg_name:
            result, steps, stats = beam_search(props.BOARD_SIZE, goal)

        elif "Nondeterministic" in alg_name:
            result, steps, stats = and_or_search(props.BOARD_SIZE, goal)
        elif "Unobservable" in alg_name:
            result, stats = dfs_belief_search(props.BOARD_SIZE, goal)
        elif "Partial Observable" in alg_name:
            result, steps, stats = dfs_partial_obs(props.BOARD_SIZE, goal)

        elif "Backtracking" in alg_name:
            result, steps, stats = backtracking_search(props.BOARD_SIZE, goal, return_steps=True, return_stats=True)
        elif "Forward Checking" in alg_name:
            result, steps, stats = forward_checking_search(props.BOARD_SIZE, goal, return_steps=True, return_stats=True)
        elif "Arc" in alg_name:
            result, steps, stats = ac3_search(props.BOARD_SIZE, goal, return_steps=True, return_stats=True)

        else:
            print("Thuật toán chưa được gán!")
            return

        # ==================== CẬP NHẬT KẾT QUẢ HIỂN THỊ ====================
        if result:
            steps = [result[:i] for i in range(1, len(result)+1)]
            self.steps = steps
            self.step_index = 0
            self.left_solution = []
            self.running_algorithms = True

        # ==================== CẬP NHẬT THỐNG KÊ & LỊCH SỬ ====================
        if stats:  # 
            self.current_stats = {
                "name": alg_name, "expanded": stats["expanded"],"frontier": stats["frontier"], 
                "visited": stats["visited"], "time": stats["time"]
            }
            self.history.append({
                "name": alg_name, "visited": stats["visited"],"time": stats["time"]
            })
        else:
            # Thuật toán chưa có thống kê (các loại khác)
            self.current_stats = {
                "name": alg_name, "expanded": 0, "frontier": 0,
                "visited": 0, "time": 0
            }

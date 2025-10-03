import pygame

WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
LIGHT_GRAY  = (200, 200, 200)
DARK_GRAY   = (64, 64, 64)
MYOSOTIS = (0x64, 0x74, 0x7B)
CADETGRAY = (0x93, 0xA8, 0xAC)
STONE = (0xA3, 0xAC, 0xA9)
COTTON = (0xE2, 0xDC, 0xD0)
ECRU = (0xBD, 0xBB, 0xA5)
SAGE = (0x8D, 0x9B, 0x86)

ALGORITHM_LIST_TOP = 380
BORDER_RADIUS = 10

algorithm_groups = [
    {
        "name": "Uninformed Search",
        "color": MYOSOTIS,
        "text_color": WHITE,
        "algorithms": [
            {"name": "Breadth-First Search", "desc": "Tìm theo chiều rộng"},
            {"name": "Depth-First Search", "desc": "Tìm theo chiều sâu"},
            {"name": "Depth Limited Search", "desc": "Giới hạn độ sâu"},
            {"name": "Iterative Deepening Search", "desc": "Lặp tăng dần độ sâu"},
            {"name": "Uniform Cost Search", "desc": "Chi phí đồng đều"}
        ]
    },
    {
        "name": "Informed Search",
        "color": CADETGRAY,
        "text_color": WHITE,
        "algorithms": [
            {"name": "A* Search", "desc": "Tối ưu với heuristic"},
            {"name": "Greedy Best-First", "desc": "Tham lam heuristic"}
        ]
    },
    {
        "name": "Local Search",
        "color": STONE,
        "text_color": WHITE,
        "algorithms": [
            {"name": "Hill Climbing", "desc": "Leo đồi tối ưu"},
            {"name": "Simulated Annealing", "desc": "Mô phỏng ủ kim loại"},
            {"name": "Genetic Algorithm", "desc": "Tiến hóa tự nhiên"},
            {"name": "Beam Search", "desc": "Giới hạn node"}
        ]
    },
    {
        "name": "Complex Environment",
        "color": COTTON,
        "text_color": DARK_GRAY,
        "algorithms": [
            {"name": "Nondeterministic", "desc": "Hành động không chắc chắn"},
            {"name": "Unobservable", "desc": "Không nhìn thấy được"},
            {"name": "Partial Observable", "desc": "Nhìn thấy một phần"}
        ]
    },
    {
        "name": "Constraint Satisfied Problem",
        "color": ECRU,
        "text_color": WHITE,
        "algorithms": [
            {"name": "Backtracking", "desc": "Thử và sai, quay lui khi vi phạm"},
            {"name": "Forward Checking", "desc": "Cắt tỉa miền giá trị sau mỗi gán"},
            {"name": "Arc Consistency (AC-3)", "desc": "Duy trì arc-consistency toàn cục"}
        ]
    },
    {
        "name": "Coming Soon",
        "color": SAGE,
        "text_color": WHITE,
        "algorithms": [
            {"name": "Q-Learning", "desc": "Học tăng cường"},
            {"name": "Neural Network Path", "desc": "Mạng neural"},
            {"name": "Random Forest Path", "desc": "Ensemble learning"}
        ]
    }
]

# ===================== DRAW FUNCTIONS =====================
def draw_group_buttons(screen, font, selected_group):
    button_width, button_height = 250, 40
    start_x, start_y = 20, 20
    spacing = 8
    rects = [] 

    for i, group in enumerate(algorithm_groups):
        x = start_x
        y = start_y + i * (button_height + spacing)

        rect = pygame.Rect(x, y, button_width, button_height)
        color = group["color"] if i == selected_group else LIGHT_GRAY
        pygame.draw.rect(screen, color, rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=BORDER_RADIUS)

        txt_color = group["text_color"] if i == selected_group else BLACK
        for j, line in enumerate(group["name"].split("\n")):
            text = font.render(line, True, txt_color)
            screen.blit(
                text,
                (x + (button_width - text.get_width()) // 2,
                 y + 8 + j * 18)
            )
        rects.append(rect)  
    return rects     

def draw_algorithm_buttons(screen, font, selected_group, selected_algorithm):
    """Vẽ các thuật toán thuộc nhóm đã chọn (nút nhỏ)"""
    if selected_group < 0:
        return []
    
    group = algorithm_groups[selected_group]

    start_x, start_y = 20, ALGORITHM_LIST_TOP
    button_width, button_height = 250, 60
    spacing = 8
    rects = []

    for i, alg in enumerate(group["algorithms"]):
        y = start_y + i * (button_height + spacing)
        rect = pygame.Rect(start_x, y, button_width, button_height)

        if i == selected_algorithm:
            pygame.draw.rect(screen, group["color"], rect, border_radius=BORDER_RADIUS)
            text_color = group["text_color"]
        else:
            pygame.draw.rect(screen, WHITE, rect, border_radius=BORDER_RADIUS)
            pygame.draw.rect(screen, group["color"], rect, 2, border_radius=BORDER_RADIUS)
            text_color = SAGE

        text = font.render(alg["name"], True, text_color)
        screen.blit(text, (start_x + 10, y + 18))
        rects.append(rect)

    return rects

def draw_action_buttons(screen, font, window_width, window_height):
    button_w, button_h = 100, 50
    spacing = 20
    y = window_height - 80

    labels = ["Run", "Visual", "Random", "Reset"]

    # Tổng chiều rộng
    total_width = button_w * len(labels) + spacing * (len(labels) - 1)
    start_x = (window_width - total_width) // 2

    rects = []

    for i, label in enumerate(labels):
        x = start_x + i * (button_w + spacing)
        rect = pygame.Rect(x, y, button_w, button_h)

        pygame.draw.rect(screen, LIGHT_GRAY, rect, border_radius=BORDER_RADIUS)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=BORDER_RADIUS)

        text = font.render(label, True, BLACK)
        screen.blit(text, text.get_rect(center=rect.center))

        rects.append(rect)

    return tuple(rects)

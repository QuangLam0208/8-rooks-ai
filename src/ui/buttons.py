import pygame

# ===================== COLORS =====================
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
GRAY        = (128, 128, 128)
LIGHT_GRAY  = (200, 200, 200)
DARK_GRAY   = (64, 64, 64)
GREEN       = (0, 255, 0)
RED         = (255, 0, 0)
BLUE        = (0, 100, 255)
YELLOW      = (255, 255, 0)
PURPLE      = (128, 0, 128)
ORANGE      = (255, 140, 0)
CYAN        = (0, 200, 200)
PINK        = (255, 192, 203)
LIGHT_BLUE  = (173, 216, 230)

# ===================== DATA =====================
algorithm_groups = [
    {
        "name": "Uninformed\nSearch",
        "color": BLUE,
        "algorithms": [
            {"name": "Breadth-First Search (BFS)", "desc": "Tìm theo chiều rộng"},
            {"name": "Depth-First Search (DFS)", "desc": "Tìm theo chiều sâu"},
            {"name": "Uniform Cost Search", "desc": "Chi phí đồng đều"}
        ]
    },
    {
        "name": "Informed\nSearch",
        "color": GREEN,
        "algorithms": [
            {"name": "A* Search", "desc": "Tối ưu với heuristic"},
            {"name": "Greedy Best-First", "desc": "Tham lam heuristic"},
            {"name": "Bidirectional Search", "desc": "Tìm hai chiều"}
        ]
    },
    {
        "name": "Dynamic\nProgramming",
        "color": PURPLE,
        "algorithms": [
            {"name": "Dijkstra's Algorithm", "desc": "Đường ngắn nhất"},
            {"name": "Floyd-Warshall", "desc": "Mọi cặp điểm"},
            {"name": "Bellman-Ford", "desc": "Trọng số âm"}
        ]
    },
    {
        "name": "Heuristic\nMethods",
        "color": RED,
        "algorithms": [
            {"name": "Hill Climbing", "desc": "Leo đồi tối ưu"},
            {"name": "Simulated Annealing", "desc": "Mô phỏng ủ kim loại"},
            {"name": "Beam Search", "desc": "Giới hạn node"}
        ]
    },
    {
        "name": "Evolutionary\nAlgorithms",
        "color": ORANGE,
        "algorithms": [
            {"name": "Genetic Algorithm", "desc": "Tiến hóa tự nhiên"},
            {"name": "Ant Colony Optimization", "desc": "Hành vi kiến"},
            {"name": "Particle Swarm Optimization", "desc": "Đàn chim"}
        ]
    },
    {
        "name": "Machine\nLearning",
        "color": CYAN,
        "algorithms": [
            {"name": "Q-Learning", "desc": "Học tăng cường"},
            {"name": "Neural Network Path", "desc": "Mạng neural"},
            {"name": "Random Forest Path", "desc": "Ensemble learning"}
        ]
    }
]

# ===================== DRAW FUNCTIONS =====================
def draw_group_buttons(screen, font, selected_group):
    button_width, button_height = 120, 50
    start_x, start_y = 20, 20
    spacing = 10
    rects = [] 

    for i, group in enumerate(algorithm_groups):
        col = i % 2
        row = i // 2
        x = start_x + col * (button_width + spacing)
        y = start_y + row * (button_height + spacing)

        rect = pygame.Rect(x, y, button_width, button_height)
        color = group["color"] if i == selected_group else LIGHT_GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        for j, line in enumerate(group["name"].split("\n")):
            text = font.render(line, True, WHITE if i == selected_group else BLACK)
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
    start_x, start_y = 20, 420
    button_width, button_height = 250, 60
    spacing = 8
    rects = []

    for i, alg in enumerate(group["algorithms"]):
        y = start_y + i * (button_height + spacing)
        rect = pygame.Rect(start_x, y, button_width, button_height)

        if i == selected_algorithm:
            pygame.draw.rect(screen, group["color"], rect)
            text_color = WHITE
        else:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, group["color"], rect, 2)
            text_color = group["color"]

        text = font.render(alg["name"], True, text_color)
        screen.blit(text, (start_x + 10, y + 18))
        rects.append(rect)

    return rects


def draw_action_buttons(screen, font, window_width, window_height):
    """
    Vẽ 2 nút Random / Reset nằm riêng biệt
    Trả về tuple (rect_random, rect_reset) để xử lý click.
    """
    button_w, button_h = 140, 50
    spacing = 20
    y = window_height - 80

    # Đặt hai nút sát cạnh nhau và căn giữa theo chiều ngang
    total_width = button_w * 2 + spacing
    start_x = (window_width - total_width) // 2

    labels = ["Random", "Reset"]
    rects = []

    for i, label in enumerate(labels):
        x = start_x + i * (button_w + spacing)
        rect = pygame.Rect(x, y, button_w, button_h)

        pygame.draw.rect(screen, LIGHT_GRAY, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

        text = font.render(label, True, BLACK)
        screen.blit(text, text.get_rect(center=rect.center))

        rects.append(rect)

    return tuple(rects)

import pygame
from .buttons import LIGHT_GRAY, DARK_GRAY, BLACK, ALG_GROUP_TOP, ALG_LEFT
from .layout import LEFT_MARGIN
from .board import BOARD_SIZE, SQUARE_SIZE

def draw_stats_and_history(screen, font, small_font, current_stats, history, running_algorithms):
    """Vẽ bảng thống kê & lịch sử chạy thuật toán cho 8 Rooks"""

    # ======= Tính vị trí động =======
    board_margin = LEFT_MARGIN - ALG_LEFT
    right_offset = LEFT_MARGIN + BOARD_SIZE * SQUARE_SIZE + 50

    stats_x = right_offset + board_margin + 70
    stats_y = ALG_GROUP_TOP

    # Background
    stats_rect = pygame.Rect(stats_x, stats_y, 300, 635)
    pygame.draw.rect(screen, LIGHT_GRAY, stats_rect)
    pygame.draw.rect(screen, BLACK, stats_rect, 2)

    # ====== PHẦN STATS HIỆN TẠI ======
    title = font.render("CURRENT RUNING", True, BLACK)
    screen.blit(title, (stats_x + 10, stats_y + 10))

    if current_stats:
        stats_info = [
            f"Algorithm: {current_stats.get('name', '---')}",
            f"Expanded: {current_stats.get('expanded', 0)}",
            f"Frontier: {current_stats.get('frontier', 0)}",
            f"Visited: {current_stats.get('visited', 0)}",
            f"Time: {current_stats.get('time', 0):.0f} ms",
            f"Status: {'Running' if running_algorithms else 'Stopped'}"
        ]
    else:
        stats_info = ["No data"]

    for i, info in enumerate(stats_info):
        text = small_font.render(info, True, BLACK)
        screen.blit(text, (stats_x + 10, stats_y + 40 + i * 22))

    # Đường phân cách
    pygame.draw.line(
        screen, DARK_GRAY,
        (stats_x + 10, stats_y + 190),
        (stats_x + 290, stats_y + 190), 2
    )

    # ====== PHẦN HISTORY ======
    history_title = font.render("HISTORY", True, BLACK)
    screen.blit(history_title, (stats_x + 10, stats_y + 210))

    if not history:
        no_data = small_font.render("No data", True, DARK_GRAY)
        screen.blit(no_data, (stats_x + 10, stats_y + 242))
    else:
        offset_y = 242
        recent_entries = list(reversed(history[-8:]))  # hiển thị tối đa 7 dòng gần nhất, mới nhất trên cùng
        for i, entry in enumerate(recent_entries):
            color = BLACK if i == 0 else DARK_GRAY  # chỉ dòng mới nhất tô đen

            name_text = small_font.render(
                f"#{len(history) - i}. {entry['name']}", True, color)
            screen.blit(name_text, (stats_x + 10, stats_y + offset_y))

            detail_text = small_font.render(
                f"Visited: {entry['visited']}  |  Time: {entry['time']:.0f}ms",
                True, color
            )
            screen.blit(detail_text, (stats_x + 10, stats_y + offset_y + 16))

            offset_y += 46

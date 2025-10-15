import pygame
from ui import properties as props

def draw_stats_and_history(screen, font, small_font, current_stats, history, running_algorithms):
    """Vẽ bảng thống kê & lịch sử chạy thuật toán cho 8 Rooks (tự cập nhật khi thay đổi BOARD_SIZE)"""

    # Tính lại vị trí động theo BOARD_SIZE hiện tại
    stats_x = props.RIGHT_BOARD_X + props.BOARD_SIZE * props.SQUARE_SIZE + 90
    stats_y = props.ALG_GROUP_TOP
    total_height = props.TOTAL_GROUP_HEIGHT + props.TOTAL_LIST5_HEIGHT + props.PARENT_CHILD_SPACING

    # Background
    stats_rect = pygame.Rect(stats_x, stats_y, 300, total_height)
    pygame.draw.rect(screen, props.LIGHT_GRAY, stats_rect)
    pygame.draw.rect(screen, props.BLACK, stats_rect, 2)

    # ====== PHẦN STATS HIỆN TẠI ======
    title = font.render("CURRENT RUNNING", True, props.BLACK)
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
        text = small_font.render(info, True, props.BLACK)
        screen.blit(text, (stats_x + 10, stats_y + 40 + i * 22))

    # Đường phân cách
    pygame.draw.line(
        screen, props.DARK_GRAY,
        (stats_x + 10, stats_y + 190),
        (stats_x + 290, stats_y + 190), 2
    )

    # ====== PHẦN HISTORY ======
    history_title = font.render("HISTORY", True, props.BLACK)
    screen.blit(history_title, (stats_x + 10, stats_y + 210))

    if not history:
        no_data = small_font.render("No data", True, props.DARK_GRAY)
        screen.blit(no_data, (stats_x + 10, stats_y + 242))
    else:
        offset_y = 242
        recent_entries = list(reversed(history[-8:]))  # hiển thị tối đa 8 dòng gần nhất
        for i, entry in enumerate(recent_entries):
            color = props.BLACK if i == 0 else props.DARK_GRAY  # dòng mới nhất tô đậm

            name_text = small_font.render(
                f"#{len(history) - i}. {entry['name']}", True, color)
            screen.blit(name_text, (stats_x + 10, stats_y + offset_y))

            detail_text = small_font.render(
                f"Visited: {entry['visited']} | Time: {entry['time']:.0f}ms | {entry.get('status', '---')}",
                True, color
            )
            screen.blit(detail_text, (stats_x + 10, stats_y + offset_y + 16))

            offset_y += 46

import pygame
from ui import properties as props
from .board import draw_board, draw_coordinates, draw_shared_numbers

def render_boards(screen, font, caption_font, rook_img,
                  left_solution, right_solution, window_width):
    """Vẽ hai bàn cờ (trái - phải) theo kích thước hiện tại."""
    # Left board
    left_offset = props.LEFT_BOARD_X
    draw_board(
        screen, rook_img, left_solution,
        x_offset=left_offset, y_offset=0,
        show_rooks=True, margin=props.ALG_GROUP_TOP
    )

    # Right board
    right_offset = props.RIGHT_BOARD_X
    draw_board(
        screen, rook_img, right_solution,
        x_offset=right_offset, y_offset=0,
        show_rooks=True, margin=props.ALG_GROUP_TOP
    )

    draw_coordinates(screen, font, x_offset=left_offset, y_offset=0,
                     margin=props.ALG_GROUP_TOP, side="left")
    draw_coordinates(screen, font, x_offset=right_offset, y_offset=0,
                     margin=props.ALG_GROUP_TOP, side="right")

    draw_shared_numbers(screen, font, left_offset, right_offset,
                        y_offset=0, margin=props.ALG_GROUP_TOP)


def draw_scrollable_panel(screen, font, logs, scroll_y=0, scroll_x=0):
    """Vẽ bảng log có thể cuộn, đọc realtime từ props."""
    # ===== Lấy kích thước hiện tại từ properties =====
    panel_y = props.ALG_LIST_TOP
    panel_height = props.TOTAL_LIST5_HEIGHT
    panel_x = props.LEFT_BOARD_X
    panel_width = (props.RIGHT_BOARD_X + props.BOARD_SIZE * props.SQUARE_SIZE) - props.LEFT_BOARD_X

    # ===== Padding =====
    pad_left = 12
    pad_top = 12
    pad_right = 15
    pad_bottom = 15

    # ===== Nền + viền =====
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(screen, (255, 255, 255), panel_rect)
    pygame.draw.rect(screen, (0, 0, 0), panel_rect, 2)

    # ===== Khu vực clip thật =====
    clip_rect = pygame.Rect(
        panel_x + pad_left,
        panel_y + pad_top,
        panel_width - (pad_left + pad_right),
        panel_height - (pad_top + pad_bottom)
    )
    old_clip = screen.get_clip()
    screen.set_clip(clip_rect)

    # ===== Layout text =====
    line_height = 22
    visible_height = clip_rect.height
    visible_width = clip_rect.width

    if not logs:
        msg = "Using the Visualization button to see the states"
        text = font.render(msg, True, (0, 0, 0))
        text_rect = text.get_rect(center=clip_rect.center)
        screen.blit(text, text_rect)
    else:
        for i, msg in enumerate(logs):
            y = clip_rect.top + i * line_height - scroll_y
            if y + line_height < clip_rect.top or y > clip_rect.bottom:
                continue
            text_surface = font.render(msg, True, (0, 0, 0))
            screen.blit(text_surface, (clip_rect.left - scroll_x, y))

    # ===== Khôi phục clip =====
    screen.set_clip(old_clip)

    # ===== Thanh scroll dọc =====
    total_height = len(logs) * line_height
    if total_height > visible_height:
        bar_height = max(panel_height * visible_height // total_height, 30)
        bar_y = panel_y + pad_top + (panel_height - pad_top - pad_bottom - bar_height) * (
            scroll_y / max(1, total_height - visible_height)
        )
        pygame.draw.rect(
            screen, (180, 180, 180),
            (panel_x + panel_width - pad_right + 3, bar_y, 6, bar_height)
        )

    # ===== Thanh scroll ngang =====
    if logs:
        max_line_width = max(font.size(line)[0] for line in logs)
        if max_line_width > visible_width:
            bar_width = max(panel_width * visible_width // max_line_width, 30)
            bar_x = panel_x + pad_left + (panel_width - pad_left - pad_right - bar_width) * (
                scroll_x / max(1, max_line_width - visible_width)
            )
            pygame.draw.rect(
                screen, (180, 180, 180),
                (bar_x, panel_y + panel_height - pad_bottom + 3, bar_width, 6)
            )

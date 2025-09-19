import pygame
from .board import draw_board, draw_coordinates, BOARD_SIZE, SQUARE_SIZE

MARGIN = 120

def render_title(screen, font, window_width):
    title_text = font.render("8 ROOKS", True, (50, 50, 50))
    title_rect = title_text.get_rect(center=(window_width // 2, 50))
    screen.blit(title_text, title_rect)

def render_boards(screen, font, caption_font, rook_img,
                  left_solution, right_solution, window_width):
    # Left board
    left_offset = MARGIN
    draw_board(screen, rook_img, left_solution, left_offset, show_rooks=True, margin=MARGIN)
    draw_coordinates(screen, font, left_offset, margin=MARGIN)

    caption_left = caption_font.render("Current Step", True, (30, 30, 30))
    caption_rect_left = caption_left.get_rect(center=(
        left_offset + BOARD_SIZE * SQUARE_SIZE // 2,
        MARGIN + BOARD_SIZE * SQUARE_SIZE + 60
    ))
    screen.blit(caption_left, caption_rect_left)

    # Right board
    right_offset = BOARD_SIZE * SQUARE_SIZE + 2 * MARGIN
    draw_board(screen, rook_img, right_solution, right_offset, show_rooks=True, margin=MARGIN)
    draw_coordinates(screen, font, right_offset, margin=MARGIN)

    caption_right = caption_font.render("Goal State", True, (30, 30, 30))
    caption_rect_right = caption_right.get_rect(center=(
        right_offset + BOARD_SIZE * SQUARE_SIZE // 2,
        MARGIN + BOARD_SIZE * SQUARE_SIZE + 60
    ))
    screen.blit(caption_right, caption_rect_right)


def render_buttons(screen, font, window_width, window_height):
    button_w, button_h = 120, 40
    gap = 30
    y = window_height - 70

    # Danh sách tên nút
    labels = ["Random", "Reset", "BFS", "DFS", "UCS", "DLS", "IDS", "GS", "A*", "SA"]
    num_buttons = len(labels)

    # Tổng chiều rộng block (tất cả nút + khoảng cách)
    total_width = num_buttons * button_w + (num_buttons - 1) * gap

    # Điểm bắt đầu để căn giữa
    start_x = (window_width - total_width) // 2

    rects = []

    for i, label in enumerate(labels):
        x = start_x + i * (button_w + gap)
        rect = pygame.Rect(x, y, button_w, button_h)
        pygame.draw.rect(screen, (200, 200, 200), rect, border_radius=8)

        text = font.render(label, True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=rect.center))

        rects.append(rect)

    return tuple(rects)  




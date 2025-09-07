import pygame

# Kích thước bàn cờ
SQUARE_SIZE = 60
BOARD_SIZE = 8

# Màu sắc các ô
WHITE = (238, 238, 210)   # ô sáng
BLACK = (118, 150, 86)    # ô tối
TEXT_COLOR = (0, 0, 0)

def draw_board(screen, rook_img, solution, x_offset, y_offset=0, show_rooks=False, margin=120):
    """Vẽ bàn cờ và quân hậu (nếu có)"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Màu ô
            color = WHITE if (row + col) % 2 == 0 else BLACK

            rect = pygame.Rect(
                x_offset + col * SQUARE_SIZE,
                margin + row * SQUARE_SIZE + y_offset,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )
            # Vẽ ô
            pygame.draw.rect(screen, color, rect)

            # Nếu cần hiển thị quân hậu
            if show_rooks and solution and solution[row] == col:
                screen.blit(rook_img, rect.topleft)

    # Vẽ viền bàn cờ
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (x_offset, margin + y_offset, BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE),
        2
    )

def draw_coordinates(screen, font, x_offset, y_offset=0, margin=120):
    """Vẽ tọa độ xung quanh bàn cờ"""
    OFFSET_TEXT = 20

    # Vẽ chữ a-h (cột)
    for col in range(BOARD_SIZE):
        letter = chr(ord("a") + col)
        text = font.render(letter, True, TEXT_COLOR)

        # Trên
        text_rect_top = text.get_rect(center=(x_offset + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                              margin - OFFSET_TEXT + y_offset))
        screen.blit(text, text_rect_top)

        # Dưới
        text_rect_bottom = text.get_rect(center=(x_offset + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                 margin + BOARD_SIZE * SQUARE_SIZE + OFFSET_TEXT + y_offset))
        screen.blit(text, text_rect_bottom)

    # Vẽ số 1–8 (hàng)
    for row in range(BOARD_SIZE):
        number = str(BOARD_SIZE - row)
        text = font.render(number, True, TEXT_COLOR)

        # Trái
        text_rect_left = text.get_rect(center=(x_offset - OFFSET_TEXT,
                                               margin + row * SQUARE_SIZE + SQUARE_SIZE // 2 + y_offset))
        screen.blit(text, text_rect_left)

        # Phải
        text_rect_right = text.get_rect(center=(x_offset + BOARD_SIZE * SQUARE_SIZE + OFFSET_TEXT,
                                                margin + row * SQUARE_SIZE + SQUARE_SIZE // 2 + y_offset))
        screen.blit(text, text_rect_right)
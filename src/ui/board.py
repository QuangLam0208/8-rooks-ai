import pygame

# Kích thước bàn cờ
SQUARE_SIZE = 50
BOARD_SIZE = 8

# Màu sắc các ô
WHITE = (238, 238, 210)   # ô sáng
BLACK = (118, 150, 86)    # ô tối
TEXT_COLOR = (0, 0, 0)

def draw_board(screen, rook_img, solution, x_offset, y_offset=0, show_rooks=False, margin=120):
    """Vẽ bàn cờ và quân xe (nếu có)"""
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

            # Nếu cần hiển thị quân xe
            if show_rooks and solution and row < len(solution) and solution[row] == col:
                # Lấy kích thước ảnh hiện tại (đã scale nhỏ)
                piece_w, piece_h = rook_img.get_size()

                # Tính lề để căn giữa trong ô
                dx = (SQUARE_SIZE - piece_w) // 2
                dy = (SQUARE_SIZE - piece_h) // 2

                # Vẽ quân cờ ở vị trí giữa ô
                screen.blit(rook_img, (rect.x + dx, rect.y + dy))

    # Vẽ viền bàn cờ
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (x_offset, margin + y_offset, BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE),
        2
    )

def draw_coordinates(screen, font, x_offset, y_offset=0, margin=120, side="left"):
    """
    Vẽ tọa độ quanh bàn cờ
    side = "left"  -> vẽ trên + trái
    side = "right" -> vẽ dưới + phải
    """
    OFFSET_TEXT = 20

    for col in range(BOARD_SIZE):
        letter = chr(ord("a") + col)
        text = font.render(letter, True, TEXT_COLOR)

        if side == "left":
            # Chỉ vẽ phía trên
            text_rect_top = text.get_rect(center=(
                x_offset + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                margin - OFFSET_TEXT + y_offset
            ))
            screen.blit(text, text_rect_top)

        elif side == "right":
            # Chỉ vẽ phía dưới
            text_rect_bottom = text.get_rect(center=(
                x_offset + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                margin + BOARD_SIZE * SQUARE_SIZE + OFFSET_TEXT + y_offset
            ))
            screen.blit(text, text_rect_bottom)

    for row in range(BOARD_SIZE):
        number = str(BOARD_SIZE - row)
        text = font.render(number, True, TEXT_COLOR)

        if side == "left":
            # Chỉ vẽ bên trái
            text_rect_left = text.get_rect(center=(
                x_offset - OFFSET_TEXT,
                margin + row * SQUARE_SIZE + SQUARE_SIZE // 2 + y_offset
            ))
            screen.blit(text, text_rect_left)

        elif side == "right":
            # Chỉ vẽ bên phải
            text_rect_right = text.get_rect(center=(
                x_offset + BOARD_SIZE * SQUARE_SIZE + OFFSET_TEXT,
                margin + row * SQUARE_SIZE + SQUARE_SIZE // 2 + y_offset
            ))
            screen.blit(text, text_rect_right)

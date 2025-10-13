import pygame
from ui import properties as props

TEXT_COLOR = props.BLACK


def draw_board(screen, rook_img, solution, x_offset, y_offset=0, show_rooks=False, margin=120):
    """Vẽ bàn cờ và quân xe (nếu có), tự động theo BOARD_SIZE & SQUARE_SIZE mới nhất"""
    board_size = props.BOARD_SIZE
    square_size = props.SQUARE_SIZE

    for row in range(board_size):
        for col in range(board_size):
            # Màu ô
            color = props.WHITE_CELL if (row + col) % 2 == 0 else props.BLACK_CELL

            rect = pygame.Rect(
                x_offset + col * square_size,
                margin + row * square_size + y_offset,
                square_size,
                square_size,
            )

            # Vẽ ô
            pygame.draw.rect(screen, color, rect)

            # Nếu cần hiển thị quân xe
            if show_rooks and solution and row < len(solution) and solution[row] == col:
                piece_w, piece_h = rook_img.get_size()
                dx = (square_size - piece_w) // 2
                dy = (square_size - piece_h) // 2
                screen.blit(rook_img, (rect.x + dx, rect.y + dy))

    # Vẽ viền bàn cờ
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (x_offset, margin + y_offset, board_size * square_size, board_size * square_size),
        2
    )


def draw_coordinates(screen, font, x_offset, y_offset=0, margin=120, side="left"):
    """
    Vẽ tọa độ quanh bàn cờ
    side = "left"  -> vẽ trên + trái
    side = "right" -> vẽ dưới + phải
    """
    board_size = props.BOARD_SIZE
    square_size = props.SQUARE_SIZE
    OFFSET_TEXT = 20

    for col in range(board_size):
        letter = chr(ord("a") + col)
        text = font.render(letter, True, TEXT_COLOR)

        if side == "left":
            text_rect_top = text.get_rect(center=(
                x_offset + col * square_size + square_size // 2,
                margin - OFFSET_TEXT + y_offset
            ))
            screen.blit(text, text_rect_top)

        elif side == "right":
            text_rect_bottom = text.get_rect(center=(
                x_offset + col * square_size + square_size // 2,
                margin - OFFSET_TEXT + y_offset
            ))
            screen.blit(text, text_rect_bottom)


def draw_shared_numbers(screen, font, left_x_offset, right_x_offset, y_offset=0, margin=120):
    """Vẽ trục số chung ở giữa hai bàn"""
    board_size = props.BOARD_SIZE
    square_size = props.SQUARE_SIZE

    middle_x = (left_x_offset + board_size * square_size + right_x_offset) // 2

    for row in range(board_size):
        number = str(board_size - row)
        text = font.render(number, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(
            middle_x,
            margin + row * square_size + square_size // 2 + y_offset
        ))
        screen.blit(text, text_rect)

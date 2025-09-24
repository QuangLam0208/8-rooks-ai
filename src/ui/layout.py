from .board import draw_board, draw_coordinates, BOARD_SIZE, SQUARE_SIZE

LEFT_MARGIN = 350   # chỉ để đẩy sang phải
TOP_MARGIN  = 120   # giữ nguyên chiều dọc

def render_title(screen, font, window_width):
    title_text = font.render("8 ROOKS", True, (50, 50, 50))
    title_rect = title_text.get_rect(center=(window_width // 2, 50))
    screen.blit(title_text, title_rect)

def render_boards(screen, font, caption_font, rook_img,
                  left_solution, right_solution, window_width):
    # Left board
    left_offset = LEFT_MARGIN
    draw_board(screen, rook_img, left_solution,
               x_offset=left_offset, y_offset=0,
               show_rooks=True, margin=TOP_MARGIN)
    draw_coordinates(screen, font,
               x_offset=left_offset, y_offset=0,
               margin=TOP_MARGIN)

    caption_left = caption_font.render("Current Step", True, (30, 30, 30))
    caption_rect_left = caption_left.get_rect(center=(
        left_offset + BOARD_SIZE * SQUARE_SIZE // 2,
        TOP_MARGIN + BOARD_SIZE * SQUARE_SIZE + 60
    ))
    screen.blit(caption_left, caption_rect_left)

    # Right board
    right_offset = LEFT_MARGIN + BOARD_SIZE * SQUARE_SIZE + 120
    draw_board(screen, rook_img, right_solution,
               x_offset=right_offset, y_offset=0,
               show_rooks=True, margin=TOP_MARGIN)
    draw_coordinates(screen, font,
               x_offset=right_offset, y_offset=0,
               margin=TOP_MARGIN)

    caption_right = caption_font.render("Goal State", True, (30, 30, 30))
    caption_rect_right = caption_right.get_rect(center=(
        right_offset + BOARD_SIZE * SQUARE_SIZE // 2,
        TOP_MARGIN + BOARD_SIZE * SQUARE_SIZE + 60
    ))
    screen.blit(caption_right, caption_rect_right)
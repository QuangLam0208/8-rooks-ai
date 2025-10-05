from .board import draw_board, draw_coordinates, draw_shared_numbers, BOARD_SIZE, SQUARE_SIZE
from .buttons import ALG_GROUP_TOP

LEFT_MARGIN = 350   # chỉ để đẩy sang phải
TOP_MARGIN  = ALG_GROUP_TOP

def render_boards(screen, font, caption_font, rook_img,
                  left_solution, right_solution, window_width):
    # Left board
    left_offset = LEFT_MARGIN
    right_offset = LEFT_MARGIN + BOARD_SIZE * SQUARE_SIZE + 50
    draw_board(screen, rook_img, left_solution,
               x_offset=left_offset, y_offset=0,
               show_rooks=True, margin=TOP_MARGIN)

    # Right board
    right_offset = LEFT_MARGIN + BOARD_SIZE * SQUARE_SIZE + 50
    draw_board(screen, rook_img, right_solution,
               x_offset=right_offset, y_offset=0,
               show_rooks=True, margin=TOP_MARGIN)
    
    draw_coordinates(screen, font, x_offset=left_offset, y_offset=0, margin=TOP_MARGIN, side="left")
    draw_coordinates(screen, font, x_offset=right_offset, y_offset=0, margin=TOP_MARGIN, side="right")
    draw_shared_numbers(screen, font, left_offset, right_offset, y_offset=0, margin=TOP_MARGIN)

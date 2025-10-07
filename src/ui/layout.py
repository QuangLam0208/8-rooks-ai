from .board import draw_board, draw_coordinates, draw_shared_numbers, BOARD_SIZE, SQUARE_SIZE
from .buttons import ALG_GROUP_TOP, ALG_LEFT, ALG_WIDTH

LEFT_BOARD_X = ALG_LEFT + ALG_WIDTH + 90 
RIGHT_BOARD_X = LEFT_BOARD_X + BOARD_SIZE * SQUARE_SIZE + 50
TOP_MARGIN  = ALG_GROUP_TOP
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

def render_boards(screen, font, caption_font, rook_img,
                  left_solution, right_solution, window_width):
    # Left board
    left_offset = LEFT_BOARD_X
    draw_board(screen, rook_img, left_solution,
               x_offset=left_offset, y_offset=0,
               show_rooks=True, margin=TOP_MARGIN)

    # Right board
    right_offset = RIGHT_BOARD_X
    draw_board(screen, rook_img, right_solution,
               x_offset=right_offset, y_offset=0,
               show_rooks=True, margin=TOP_MARGIN)
    
    draw_coordinates(screen, font, x_offset=left_offset, y_offset=0, margin=TOP_MARGIN, side="left")
    draw_coordinates(screen, font, x_offset=right_offset, y_offset=0, margin=TOP_MARGIN, side="right")
    draw_shared_numbers(screen, font, left_offset, right_offset, y_offset=0, margin=TOP_MARGIN)

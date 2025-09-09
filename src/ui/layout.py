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
    """Vẽ 3 nút: Random + Reset + Run BFS + Run DFS"""
    button_w, button_h = 120, 40
    gap = 30
    y = window_height - 70

    # Random
    random_rect = pygame.Rect(window_width // 2 - button_w*2 - gap*3, y, button_w, button_h)
    pygame.draw.rect(screen, (200, 200, 200), random_rect, border_radius=8)
    text = font.render("Random", True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=random_rect.center))

    # Reset
    reset_rect = pygame.Rect(window_width // 2 - button_w - gap, y, button_w, button_h)
    pygame.draw.rect(screen, (200, 200, 200), reset_rect, border_radius=8)
    text = font.render("Reset", True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=reset_rect.center))

    # Run BFS
    run_bfs_rect = pygame.Rect(window_width // 2 + gap, y, button_w, button_h)
    pygame.draw.rect(screen, (200, 200, 200), run_bfs_rect, border_radius=8)
    text = font.render("Run BFS", True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=run_bfs_rect.center))

    # Run DFS
    run_dfs_rect = pygame.Rect(window_width // 2 + button_w + gap*2, y, button_w, button_h)
    pygame.draw.rect(screen, (200, 200, 200), run_dfs_rect, border_radius=8)
    text = font.render("Run DFS", True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=run_dfs_rect.center))

    return random_rect, reset_rect, run_bfs_rect, run_dfs_rect


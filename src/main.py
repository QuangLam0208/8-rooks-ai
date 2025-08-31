import pygame
import sys
import os
from board import draw_board, draw_coordinates, BOARD_SIZE, SQUARE_SIZE

# Các tham số kích thước, màu sắc chung
MARGIN = 120
WINDOW_WIDTH = 2 * (BOARD_SIZE * SQUARE_SIZE) + 3 * MARGIN
WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE + 2 * MARGIN
BG_COLOR = (221, 211, 211)  # màu bg

# Một nghiệm sẵn của 8 queens
solution = [0, 4, 7, 5, 2, 6, 1, 3]

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Bàn cờ vua - 8 Queens")

# Fonts
font = pygame.font.SysFont("Arial", 18, bold=True)
title_font = pygame.font.SysFont("Arial", 32, bold=True)
caption_font = pygame.font.SysFont("Arial", 20, bold=True)

# Load ảnh quân hậu
queen_img = pygame.image.load(os.path.join("assets", "queen.png"))
queen_img = pygame.transform.scale(queen_img, (SQUARE_SIZE, SQUARE_SIZE))

# Loop chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    # Tiêu đề
    title_text = title_font.render("8 QUEENS", True, (50, 50, 50))
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    # Bàn cờ trái (Initial)
    left_offset = MARGIN
    draw_board(screen, queen_img, solution, left_offset, show_queens=False, margin=MARGIN)
    draw_coordinates(screen, font, left_offset, margin=MARGIN)

    caption_left = caption_font.render("Initial State", True, (30, 30, 30))
    caption_rect_left = caption_left.get_rect(center=(left_offset + BOARD_SIZE * SQUARE_SIZE // 2,
                                                      MARGIN + BOARD_SIZE * SQUARE_SIZE + 60))
    screen.blit(caption_left, caption_rect_left)

    # Bàn cờ phải (Final)
    right_offset = BOARD_SIZE * SQUARE_SIZE + 2 * MARGIN
    draw_board(screen, queen_img, solution, right_offset, show_queens=True, margin=MARGIN)
    draw_coordinates(screen, font, right_offset, margin=MARGIN)

    caption_right = caption_font.render("Final State", True, (30, 30, 30))
    caption_rect_right = caption_right.get_rect(center=(right_offset + BOARD_SIZE * SQUARE_SIZE // 2,
                                                        MARGIN + BOARD_SIZE * SQUARE_SIZE + 60))
    screen.blit(caption_right, caption_rect_right)

    pygame.display.flip()

pygame.quit()
sys.exit()
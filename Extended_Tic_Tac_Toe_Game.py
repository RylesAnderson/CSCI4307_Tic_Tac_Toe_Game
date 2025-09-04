import sys
import pygame
import numpy as np
from Tools.demo.sortvisu import WIDTH

pygame.init()

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (250, 0, 0)
GREEN = (0, 250, 0)
BLACK = (0, 0, 0)

WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
score_player = 0
score_ai = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extended Tic Tac Toe Game")
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

start_ticks = pygame.time.get_ticks()

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i),
                         (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0),
                         (SQUARE_SIZE * i, WIDTH), LINE_WIDTH)

def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 CROSS_WIDTH)

                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4): # Stop 4 columns from the end to allow for a 5-in-a-row check
            if all(check_board[row][col+i] == player for i in range(5)):
                return True

    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 4):
            if all(check_board[row+i][col] == player for i in range(5)):
                return True

    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS - 4):
            if all(check_board[row+i][col+i] == player for i in range(5)):
                return True

    for row in range(4, BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if all(check_board[row-i][col+i] == player for i in range(5)):
                return True
        return False

def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

def restart_game():
    global start_ticks
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

def draw_score():
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Player: {score_player}   AI: {score_ai}", True, WHITE)
    screen.blit(text, (10, 10))

def draw_timer():
    font = pygame.font.SysFont(None, 30)
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, 30 - elapsed_seconds)  # don’t go negative
    text = font.render(f"Time: {remaining}s", True, WHITE)
    screen.blit(text, (WIDTH - 120, 10))
    return remaining


draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    if player == 1:
                        score_player += 1
                    else:
                        score_ai += 1
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_win(2):
                            score_ai += 1
                            game_over = True
                        player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)

    draw_score()
    draw_timer()
    pygame.display.update()
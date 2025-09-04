import sys
import pygame
import numpy as np

pygame.init()

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (250, 0, 0)
GREEN = (0, 250, 0)
BLACK = (0, 0, 0)

WIDTH = 500
HEIGHT = 500
LINE_WIDTH = 5
BOARD_ROWS = 5
BOARD_COLS = 5
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
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
    if any(all(check_board[row][col + i] == player for i in range(5))
           for row in range(BOARD_ROWS)
           for col in range(BOARD_COLS - 4)):
        return True

    if any(all(check_board[row + i][col] == player for i in range(5))
           for col in range(BOARD_COLS)
           for row in range(BOARD_ROWS - 4)):
        return True

    if any(all(check_board[row + i][col + i] == player for i in range(5))
           for row in range(BOARD_ROWS - 4)
           for col in range(BOARD_COLS - 4)):
        return True

    if any(all(check_board[row - i][col + i] == player for i in range(5))
           for row in range(4, BOARD_ROWS)
           for col in range(BOARD_COLS - 4)):
        return True

    return False

def evaluate_board(check_board, player):
    score = 0
    opponent = 1 if player == 2 else 2

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            line = check_board[row, col:col+5]
            if np.count_nonzero(line == player) == 4 and np.count_nonzero(line == 0) == 1:
                score += 1000

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            line = check_board[row, col:col+5]
            if np.count_nonzero(line == opponent) == 4 and np.count_nonzero(line == 0) == 1:
                score += 500

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            line = check_board[row, col:col+4]
            if np.count_nonzero(line == player) == 3 and np.count_nonzero(line == 0) == 1:
                score += 100

    return score

def best_move():
    best_score = -1000
    move = (-1, -1)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                if check_win(2):
                    board[row][col] = 0
                    return (row, col)
                board[row][col] = 0

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 1
                if check_win(1):
                    board[row][col] = 0
                    return (row, col)
                board[row][col] = 0

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                current_score = evaluate_board(board, 2)
                board[row][col] = 0
                if current_score > best_score:
                    best_score = current_score
                    move = (row, col)

    if move == (-1, -1):
        if board[2][2] == 0:
            return (2, 2)
        else:
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if board[row][col] == 0:
                        return (row, col)

    return move


def restart_game():
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
    remaining = max(0, 60 - elapsed_seconds)
    text = font.render(f"Time: {remaining}s", True, WHITE)
    screen.blit(text, (WIDTH - 120, 10))
    return remaining

def display_winner():
    font = pygame.font.SysFont(None, 75)
    winner_text = ""
    text_color = GRAY

    if score_player > score_ai:
        winner_text = "You Win!"
        text_color = GREEN
    elif score_ai > score_player:
        winner_text = "Bob Wins!"
        text_color = RED
    else:
        winner_text = "Draw!"
        text_color = GRAY

    text = font.render(winner_text, True, text_color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

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
                    ai_move = best_move()
                    if ai_move:
                        mark_square(ai_move[0], ai_move[1], 2)
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

    remaining_time = draw_timer()
    if remaining_time <= 0 and not game_over:
        game_over = True

    if not game_over:
        draw_figures()
    else:
        screen.fill(BLACK)
        draw_figures()
        draw_lines(GRAY)
        display_winner()

    draw_score()
    pygame.display.update()
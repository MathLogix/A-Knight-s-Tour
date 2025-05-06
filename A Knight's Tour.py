import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (212, 194, 177)
BLACK = (140, 82, 60)
NEW_WHITE = (246, 225, 206)
NEW_BLACK = (182, 107, 78)
# ARROW_COLOR = (27, 140, 60)
ARROW_COLOR = "seagreen"

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Knight's Tour - Chessboard")
icon = pygame.image.load("Desktop/knight.png")
pygame.display.set_icon(icon)

knight_img = pygame.image.load("desktop/knight.png")
knight_img = pygame.transform.scale(knight_img, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))

knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

def is_valid(row, col, visited):
    return 0 <= row < 8 and 0 <= col < 8 and not visited[row][col]

def warnsdorff_heuristic(row, col, visited):
    moves = []
    for dr, dc in knight_moves:
        new_r, new_c = row + dr, col + dc
        if is_valid(new_r, new_c, visited):
            count = 0
            for dr2, dc2 in knight_moves:
                r2, c2 = new_r + dr2, new_c + dc2
                if is_valid(r2, c2, visited):
                    count += 1
            moves.append(((new_r, new_c), count))
    moves.sort(key=lambda x: x[1])
    return [move[0] for move in moves]

def solve_warnsdorff(row, col):
    visited = [[False for _ in range(8)] for _ in range(8)]
    path = [(row, col)]
    visited[row][col] = True
    for _ in range(63):
        next_moves = warnsdorff_heuristic(row, col, visited)
        if not next_moves:
            return []
        row, col = next_moves[0]
        path.append((row, col))
        visited[row][col] = True
    return path

def get_square_center(row, col):
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
    return (x, y)

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_scene(knight_pos=None):
    draw_board()
    for square in visited_squares:
        draw_visited_square(*square)

    for arrow in arrows:
        draw_arrow(*arrow)
    if knight_pos:
        win.blit(knight_img, knight_img.get_rect(center=knight_pos))
    elif path and index < len(path):
        draw_knight(path[index])

def draw_knight(pos):
    x, y = get_square_center(*pos)
    knight_rect = knight_img.get_rect(center=(x, y))
    win.blit(knight_img, knight_rect)

def draw_arrow(start, end):
    pygame.draw.line(win, ARROW_COLOR, start, end, 4)
    angle = math.atan2(end[1]-start[1], end[0]-start[0])
    arrow_size = 12
    tip = end
    left = (end[0] - arrow_size * math.cos(angle - math.pi / 6),
            end[1] - arrow_size * math.sin(angle - math.pi / 6))
    right = (end[0] - arrow_size * math.cos(angle + math.pi / 6),
            end[1] - arrow_size * math.sin(angle + math.pi / 6))
    pygame.draw.polygon(win, ARROW_COLOR, [tip, left, right])

def get_clicked_square(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def draw_visited_square(row, col):
    base_color = WHITE if (row + col) % 2 == 0 else BLACK

    if base_color == WHITE:
        base_color = NEW_WHITE
    elif base_color == BLACK:
        base_color = NEW_BLACK

    surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    surface.fill(base_color)
    win.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

start_selected = False
start_pos = None
path = []
visited_squares = []
arrows = []

running = True
animating = False
index = 0
clock = pygame.time.Clock()
speed = 5

while running:
    clock.tick(60)

    if animating and index < len(path)-1:
        current_square = path[index]
        next_square = path[index + 1]
        current = get_square_center(*current_square)
        next_pos = get_square_center(*next_square)

        if current_square not in visited_squares:
            visited_squares.append(current_square)

        dx = next_pos[0] - current[0]
        dy = next_pos[1] - current[1]
        dist = math.hypot(dx, dy)
        steps = max(int(dist // speed), 1)
        move_x = dx / steps
        move_y = dy / steps

        for i in range(steps):
            knight_x = current[0] + move_x * i
            knight_y = current[1] + move_y * i
            draw_scene((knight_x, knight_y))
            pygame.display.update()
            clock.tick(60)

        arrows.append((current, next_pos))
        index += 1

        if index == len(path) - 1:
            visited_squares.append(path[index])

    else:
        draw_scene()
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not start_selected:
            row, col = get_clicked_square(pygame.mouse.get_pos())
            start_pos = (row, col)
            path = solve_warnsdorff(row, col)
            if path:
                start_selected = True
                animating = True
                index = 0
                visited_squares = []
                arrows = []
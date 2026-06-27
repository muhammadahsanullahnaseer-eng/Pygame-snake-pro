import pygame
import random

# ── Setup ──────────────────────────────────────────────────────────────
pygame.init()

CELL      = 20          # size of one grid square (pixels)
COLS      = 24          # number of columns
ROWS      = 24          # number of rows
WIDTH     = COLS * CELL # 480 px
HEIGHT    = ROWS * CELL # 480 px
FPS       = 10          # moves per second (speed)

# Colours
BG        = (23,  52,   4)   # dark green background
GRID      = (29,  61,   6)   # faint grid lines
HEAD      = (151, 196,  89)  # bright green – snake head
BODY      = (99,  153,  34)  # mid green    – snake body
FOOD      = (226,  75,  74)  # red          – apple
WHITE     = (255, 255, 255)
YELLOW    = (239, 159,  39)  # gold         – bonus

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("consolas", 18, bold=True)
big    = pygame.font.SysFont("consolas", 32, bold=True)


# ── Helper: random free cell ───────────────────────────────────────────
def free_cell(snake):
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos


# ── Draw grid ──────────────────────────────────────────────────────────
def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))


# ── Draw one rounded square ────────────────────────────────────────────
def draw_cell(col, row, colour, radius=5):
    rect = pygame.Rect(col * CELL + 1, row * CELL + 1, CELL - 2, CELL - 2)
    pygame.draw.rect(screen, colour, rect, border_radius=radius)


# ── Main game function ─────────────────────────────────────────────────
def play():
    # Starting snake: 3 segments moving right
    snake  = [(12, 12), (11, 12), (10, 12)]   # list of (col, row)
    direction  = (1, 0)                         # (dx, dy)
    next_dir   = (1, 0)

    food   = free_cell(snake)
    score  = 0
    level  = 1
    speed  = FPS                                # current moves/second

    running = True
    while running:

        # ── Events ────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False                    # quit the whole program

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP,    pygame.K_w) and direction != (0,  1):
                    next_dir = (0, -1)
                if event.key in (pygame.K_DOWN,  pygame.K_s) and direction != (0, -1):
                    next_dir = (0,  1)
                if event.key in (pygame.K_LEFT,  pygame.K_a) and direction != (1,  0):
                    next_dir = (-1, 0)
                if event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    next_dir = (1,  0)

        # ── Move ──────────────────────────────────────────────────────
        direction  = next_dir
        head       = (snake[0][0] + direction[0],
                      snake[0][1] + direction[1])

        # ── Collision: wall or self ────────────────────────────────────
        if (head[0] < 0 or head[0] >= COLS or
                head[1] < 0 or head[1] >= ROWS or
                head in snake):
            return score                        # game over → return score

        snake.insert(0, head)                   # add new head

        # ── Eat food? ─────────────────────────────────────────────────
        if head == food:
            score += 10 * level                 # grow (don't pop tail)
            food   = free_cell(snake)

            # Level up every 50 points
            new_level = score // 50 + 1
            if new_level > level:
                level = new_level
                speed = min(20, FPS + level * 2)  # go faster each level
                clock.tick(speed)
        else:
            snake.pop()                         # remove tail (normal move)

        # ── Draw ──────────────────────────────────────────────────────
        screen.fill(BG)
        draw_grid()

        # Food
        draw_cell(food[0], food[1], FOOD, radius=CELL // 2)

        # Snake
        for i, (cx, cy) in enumerate(snake):
            colour = HEAD if i == 0 else BODY
            draw_cell(cx, cy, colour, radius=6 if i == 0 else 4)

        # HUD
        hud = font.render(
            f"Score: {score}   Level: {level}   (WASD / Arrow keys)", True, WHITE
        )
        screen.blit(hud, (8, 4))

        pygame.display.flip()
        clock.tick(speed)

    return score


# ── Game-over screen ───────────────────────────────────────────────────
def game_over_screen(score, hi):
    screen.fill((13, 31, 9))
    lines = [
        (big,  "GAME  OVER",          WHITE,   HEIGHT // 2 - 60),
        (font, f"Score : {score}",    YELLOW,  HEIGHT // 2 - 10),
        (font, f"Best  : {hi}",       HEAD,    HEIGHT // 2 + 20),
        (font, "Press SPACE to retry  |  ESC to quit",
                                      (150, 150, 150), HEIGHT // 2 + 60),
    ]
    for f_, text, col, y in lines:
        surf = f_.render(text, True, col)
        screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, y))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True          # play again
                if event.key == pygame.K_ESCAPE:
                    return False         # quit


# ── Entry point ────────────────────────────────────────────────────────
def main():
    hi = 0
    while True:
        result = play()
        if result is False:             # user closed the window
            break
        score = result
        hi    = max(hi, score)
        if not game_over_screen(score, hi):
            break
    pygame.quit()


if __name__ == "__main__":
    main()
 ̶ ̶ ̶ ̶ ̶ ̶
This is code of my project 
Give me a description line for my GitHub repository

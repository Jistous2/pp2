import pygame
import random
import sys

pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
HUD_HEIGHT = 40

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + HUD_HEIGHT))
pygame.display.set_caption("Snake")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 20, 20)
GRAY = (40, 40, 40)
BLUE = (50, 100, 200)
YELLOW = (255, 215, 0)

font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 40, bold=True)
clock = pygame.time.Clock()

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def generate_walls(level):
    walls = set()

    for x in range(GRID_WIDTH):
        walls.add((x, 0))
        walls.add((x, GRID_HEIGHT - 1))
    for y in range(GRID_HEIGHT):
        walls.add((0, y))
        walls.add((GRID_WIDTH - 1, y))

    if level >= 2:
        for x in range(5, 15):
            walls.add((x, 5))
    if level >= 3:
        for x in range(16, 26):
            walls.add((x, 14))
    if level >= 4:
        for y in range(7, 13):
            walls.add((7, y))
    if level >= 5:
        for y in range(7, 13):
            walls.add((22, y))

    return walls


def random_food_position(snake_body, walls):
    while True:
        pos = (random.randint(1, GRID_WIDTH - 2),
               random.randint(1, GRID_HEIGHT - 2))
        if pos not in snake_body and pos not in walls:
            return pos


def draw_cell(surface, colour, grid_pos, offset_y=HUD_HEIGHT):
    rect = pygame.Rect(grid_pos[0] * CELL_SIZE,
                       grid_pos[1] * CELL_SIZE + offset_y,
                       CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, colour, rect)
    pygame.draw.rect(surface, BLACK, rect, 1)


def draw_walls(surface, walls):
    for pos in walls:
        draw_cell(surface, BLUE, pos)


def draw_snake(surface, snake_body):
    for i, segment in enumerate(snake_body):
        colour = GREEN if i == 0 else DARK_GREEN
        draw_cell(surface, colour, segment)


def draw_food(surface, food_pos):
    draw_cell(surface, RED, food_pos)


def draw_hud(surface, score, level):
    pygame.draw.rect(surface, GRAY, (0, 0, SCREEN_WIDTH, HUD_HEIGHT))
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, YELLOW)
    surface.blit(score_text, (10, 8))
    surface.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 8))


def draw_grid_background(surface):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE + HUD_HEIGHT,
                               CELL_SIZE, CELL_SIZE)
            if (x + y) % 2 == 0:
                pygame.draw.rect(surface, (30, 30, 30), rect)
            else:
                pygame.draw.rect(surface, (25, 25, 25), rect)


def game_over_screen(surface, score, level):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT + HUD_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    centre_y = (SCREEN_HEIGHT + HUD_HEIGHT) // 2

    go_text = big_font.render("GAME OVER", True, RED)
    surface.blit(go_text, go_text.get_rect(center=(SCREEN_WIDTH // 2, centre_y - 50)))

    info1 = font.render(f"Score: {score}   Level: {level}", True, WHITE)
    surface.blit(info1, info1.get_rect(center=(SCREEN_WIDTH // 2, centre_y + 5)))

    info2 = font.render("Press R to restart or Q to quit", True, WHITE)
    surface.blit(info2, info2.get_rect(center=(SCREEN_WIDTH // 2, centre_y + 40)))

    pygame.display.flip()


def main():
    level = 1
    score = 0
    foods_eaten_this_level = 0
    FOODS_PER_LEVEL = 4
    base_speed = 8
    speed = base_speed
    max_level = 5

    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    snake_body = [(start_x, start_y),
                  (start_x - 1, start_y),
                  (start_x - 2, start_y)]
    direction = RIGHT

    walls = generate_walls(level)
    food_pos = random_food_position(set(snake_body), walls)

    running = True
    game_active = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_active:
                    if event.key == pygame.K_UP and direction != DOWN:
                        direction = UP
                    elif event.key == pygame.K_DOWN and direction != UP:
                        direction = DOWN
                    elif event.key == pygame.K_LEFT and direction != RIGHT:
                        direction = LEFT
                    elif event.key == pygame.K_RIGHT and direction != LEFT:
                        direction = RIGHT
                else:
                    if event.key == pygame.K_r:
                        main()
                        return
                    if event.key == pygame.K_q:
                        running = False

        if not game_active:
            continue

        head_x, head_y = snake_body[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        if new_head in walls:
            game_active = False
            game_over_screen(window, score, level)
            continue

        if new_head in snake_body:
            game_active = False
            game_over_screen(window, score, level)
            continue

        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_active = False
            game_over_screen(window, score, level)
            continue

        snake_body.insert(0, new_head)

        if new_head == food_pos:
            score += 10
            foods_eaten_this_level += 1

            if foods_eaten_this_level >= FOODS_PER_LEVEL:
                foods_eaten_this_level = 0
                if level < max_level:
                    level += 1
                    speed = base_speed + (level - 1) * 2
                    walls = generate_walls(level)

            food_pos = random_food_position(set(snake_body), walls)
        else:
            snake_body.pop()

        draw_grid_background(window)
        draw_walls(window, walls)
        draw_food(window, food_pos)
        draw_snake(window, snake_body)
        draw_hud(window, score, level)
        pygame.display.flip()

        clock.tick(speed)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

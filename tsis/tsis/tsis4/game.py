import pygame
import random

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
DARK_RED = (139, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BROWN = (139, 69, 19)


class SnakeGame:
    def __init__(self, settings):
        self.settings = settings
        self.reset()

    def reset(self):
        self.snake = [[COLS // 2, ROWS // 2], [COLS // 2 - 1, ROWS // 2], [COLS // 2 - 2, ROWS // 2]]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.level = 1
        self.food_eaten_in_level = 0
        self.base_speed = 10
        self.food = None
        self.food_type = 'normal'
        self.food_timer = 0
        self.powerup = None
        self.powerup_type = None
        self.powerup_timer = 0
        self.obstacles = []
        self.active_powerup = None
        self.active_powerup_end_time = 0
        self.has_shield = False
        self.is_game_over = False
        self.spawn_food()

    def get_random_empty_cell(self):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            pos = [x, y]
            if pos not in self.snake and pos not in self.obstacles:
                return pos

    def spawn_food(self):
        self.food = self.get_random_empty_cell()
        rand = random.random()
        if rand < 0.1:
            self.food_type = 'golden'
            self.food_timer = pygame.time.get_ticks() + 5000
        elif rand < 0.3:
            self.food_type = 'poison'
            self.food_timer = 0
        else:
            self.food_type = 'normal'
            self.food_timer = 0

    def spawn_powerup(self):
        if self.powerup is None and random.random() < 0.05:
            self.powerup = self.get_random_empty_cell()
            self.powerup_type = random.choice(['speed', 'slow', 'shield'])
            self.powerup_timer = pygame.time.get_ticks() + 8000

    def spawn_obstacles(self):
        self.obstacles = []
        if self.level >= 3:
            num_obstacles = self.level * 2
            for _ in range(num_obstacles):
                while True:
                    pos = self.get_random_empty_cell()
                    head_x, head_y = self.snake[0]
                    dist = abs(pos[0] - head_x) + abs(pos[1] - head_y)
                    if dist > 5:
                        self.obstacles.append(pos)
                        break

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != (0, 1):
                self.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.next_direction = (1, 0)

    def update(self):
        if self.is_game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = [head_x + self.direction[0], head_y + self.direction[1]]

        hit_wall = (new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS)
        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if hit_wall or hit_self or hit_obstacle:
            if self.has_shield:
                self.has_shield = False
                if hit_wall:
                    new_head[0] = new_head[0] % COLS
                    new_head[1] = new_head[1] % ROWS
                elif hit_obstacle:
                    self.obstacles.remove(new_head)
            else:
                self.is_game_over = True
                return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            if self.food_type == 'normal':
                self.score += 1
                self.food_eaten_in_level += 1
            elif self.food_type == 'golden':
                self.score += 5
                self.food_eaten_in_level += 2
            elif self.food_type == 'poison':
                self.score -= 1
                if len(self.snake) > 2:
                    self.snake.pop()
                    self.snake.pop()
                else:
                    self.is_game_over = True
            self.spawn_food()
            if self.food_eaten_in_level >= 5:
                self.level += 1
                self.food_eaten_in_level = 0
                self.base_speed += 2
                self.spawn_obstacles()
        else:
            self.snake.pop()

        current_time = pygame.time.get_ticks()
        if self.food_type == 'golden' and current_time > self.food_timer:
            self.spawn_food()

        if self.powerup and new_head == self.powerup:
            if self.powerup_type == 'shield':
                self.has_shield = True
            else:
                self.active_powerup = self.powerup_type
                self.active_powerup_end_time = current_time + 5000
            self.powerup = None

        if self.powerup and current_time > self.powerup_timer:
            self.powerup = None

        self.spawn_powerup()

        if self.active_powerup and current_time > self.active_powerup_end_time:
            self.active_powerup = None

    def get_current_speed(self):
        speed = self.base_speed
        if self.active_powerup == 'speed':
            speed += 5
        elif self.active_powerup == 'slow':
            speed = max(5, speed - 5)
        return speed

    def draw(self, surface):
        if self.settings['grid_overlay']:
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))

        for obs in self.obstacles:
            rect = pygame.Rect(obs[0]*CELL_SIZE, obs[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, BROWN, rect)

        if self.food:
            rect = pygame.Rect(self.food[0]*CELL_SIZE, self.food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if self.food_type == 'normal':
                pygame.draw.rect(surface, RED, rect)
            elif self.food_type == 'golden':
                pygame.draw.rect(surface, GOLD, rect)
            elif self.food_type == 'poison':
                pygame.draw.rect(surface, DARK_RED, rect)

        if self.powerup:
            rect = pygame.Rect(self.powerup[0]*CELL_SIZE, self.powerup[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if self.powerup_type == 'speed':
                pygame.draw.circle(surface, YELLOW, rect.center, CELL_SIZE//2)
            elif self.powerup_type == 'slow':
                pygame.draw.circle(surface, LIGHT_BLUE, rect.center, CELL_SIZE//2)
            elif self.powerup_type == 'shield':
                pygame.draw.circle(surface, BLUE, rect.center, CELL_SIZE//2)

        color = tuple(self.settings['snake_color'])
        for i, segment in enumerate(self.snake):
            rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if i == 0 and self.has_shield:
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, BLUE, rect, 3)
            else:
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)

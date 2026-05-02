import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
CYAN = (0, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LANE_WIDTH = 200


class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.image = pygame.Surface((50, 90))
        self.color = RED
        if color_name == 'blue': self.color = BLUE
        if color_name == 'green': self.color = GREEN
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 5
        self.has_shield = False
        self.is_nitro = False
        self.nitro_timer = 0

    def move(self):
        keys = pygame.key.get_pressed()
        current_speed = self.speed + (5 if self.is_nitro else 0)
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-current_speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(current_speed, 0)
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -current_speed)
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, current_speed)

    def update_powerups(self):
        if self.is_nitro:
            self.nitro_timer -= 1
            if self.nitro_timer <= 0:
                self.is_nitro = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.has_shield:
            pygame.draw.rect(surface, CYAN, self.rect.inflate(10, 10), 3)
        if self.is_nitro:
            pygame.draw.polygon(surface, YELLOW, [
                (self.rect.centerx - 10, self.rect.bottom),
                (self.rect.centerx + 10, self.rect.bottom),
                (self.rect.centerx, self.rect.bottom + random.randint(10, 30))
            ])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((50, 90))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        lane = random.randint(0, 3)
        self.rect.center = (100 + lane * LANE_WIDTH, -50)
        self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((70, 30))
        self.image.fill((139, 69, 19))
        self.rect = self.image.get_rect()
        lane = random.randint(0, 3)
        self.rect.center = (100 + lane * LANE_WIDTH, -50)
        self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.weight = random.choices([1, 5, 10], weights=[70, 20, 10])[0]
        size = 20
        color = YELLOW
        if self.weight == 5:
            size = 25
            color = (192, 192, 192)
        elif self.weight == 10:
            size = 30
            color = (255, 215, 0)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)
        self.rect = self.image.get_rect()
        lane = random.randint(0, 3)
        self.rect.center = (100 + lane * LANE_WIDTH, -50)
        self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.type = random.choice(['nitro', 'shield', 'repair'])
        self.image = pygame.Surface((30, 30))
        if self.type == 'nitro':
            self.image.fill(RED)
        elif self.type == 'shield':
            self.image.fill(CYAN)
        elif self.type == 'repair':
            self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        lane = random.randint(0, 3)
        self.rect.center = (100 + lane * LANE_WIDTH, -50)
        self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

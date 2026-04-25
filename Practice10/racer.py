import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 215, 0)

ROAD_LEFT = 100
ROAD_RIGHT = 300
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48, bold=True)
clock = pygame.time.Clock()
FPS = 60


class Player:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = ROAD_LEFT + ROAD_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 5

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (150, 220, 255), (self.x + 5, self.y + 5, self.width - 10, 15))
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + 5, 5, 12))
        pygame.draw.rect(surface, BLACK, (self.x + self.width, self.y + 5, 5, 12))
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + self.height - 17, 5, 12))
        pygame.draw.rect(surface, BLACK, (self.x + self.width, self.y + self.height - 17, 5, 12))

    def move(self, dx):
        self.x += dx
        if self.x < ROAD_LEFT:
            self.x = ROAD_LEFT
        if self.x + self.width > ROAD_RIGHT:
            self.x = ROAD_RIGHT - self.width

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.width)
        self.y = -self.height
        self.speed = random.randint(4, 8)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (150, 220, 255), (self.x + 5, self.y + self.height - 20, self.width - 10, 15))
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + 5, 5, 12))
        pygame.draw.rect(surface, BLACK, (self.x + self.width, self.y + 5, 5, 12))
        pygame.draw.rect(surface, BLACK, (self.x - 5, self.y + self.height - 17, 5, 12))
        pygame.draw.rect(surface, BLACK, (self.x + self.width, self.y + self.height - 17, 5, 12))

    def move(self):
        self.y += self.speed

    def off_screen(self):
        return self.y > SCREEN_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Coin:
    def __init__(self):
        self.radius = 10
        self.x = random.randint(ROAD_LEFT + self.radius, ROAD_RIGHT - self.radius)
        self.y = -self.radius
        self.speed = random.randint(3, 6)

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (200, 170, 0), (self.x, self.y), self.radius, 2)
        dollar = font.render("$", True, BLACK)
        surface.blit(dollar, dollar.get_rect(center=(self.x, self.y)))

    def move(self):
        self.y += self.speed

    def off_screen(self):
        return self.y - self.radius > SCREEN_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)


def draw_road(surface, stripe_offset):
    surface.fill(GREEN)
    pygame.draw.rect(surface, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    pygame.draw.line(surface, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, SCREEN_HEIGHT), 3)
    pygame.draw.line(surface, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 3)
    centre_x = ROAD_LEFT + ROAD_WIDTH // 2
    dash_length = 30
    gap_length = 20
    y = -dash_length + (stripe_offset % (dash_length + gap_length))
    while y < SCREEN_HEIGHT:
        pygame.draw.line(surface, WHITE, (centre_x, y), (centre_x, y + dash_length), 2)
        y += dash_length + gap_length


def draw_hud(surface, score, coins_collected):
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))
    coin_text = font.render(f"Coins: {coins_collected}", True, YELLOW)
    surface.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))


def game_over_screen(surface, score, coins_collected):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    go_text = big_font.render("GAME OVER", True, RED)
    surface.blit(go_text, go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))

    info1 = font.render(f"Score: {score}", True, WHITE)
    surface.blit(info1, info1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

    info2 = font.render(f"Coins collected: {coins_collected}", True, YELLOW)
    surface.blit(info2, info2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 35)))

    info3 = font.render("Press R to restart or Q to quit", True, WHITE)
    surface.blit(info3, info3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)))

    pygame.display.flip()


def main():
    player = Player()
    enemies = []
    coins = []
    score = 0
    coins_collected = 0
    stripe_offset = 0

    enemy_timer = 0
    coin_timer = 0
    ENEMY_INTERVAL = 1500
    COIN_INTERVAL = 3000

    running = True
    game_active = True

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                if event.key == pygame.K_q:
                    running = False

        if not game_active:
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player.speed)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed)

        enemy_timer += dt
        if enemy_timer >= ENEMY_INTERVAL:
            enemy_timer = 0
            enemies.append(Enemy())

        coin_timer += dt
        if coin_timer >= COIN_INTERVAL:
            coin_timer = 0
            coins.append(Coin())

        for enemy in enemies[:]:
            enemy.move()
            if enemy.off_screen():
                enemies.remove(enemy)
                score += 1
            elif player.get_rect().colliderect(enemy.get_rect()):
                game_active = False

        for coin in coins[:]:
            coin.move()
            if coin.off_screen():
                coins.remove(coin)
            elif player.get_rect().colliderect(coin.get_rect()):
                coins.remove(coin)
                coins_collected += 1

        stripe_offset += 5

        draw_road(screen, stripe_offset)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for coin in coins:
            coin.draw(screen)
        draw_hud(screen, score, coins_collected)
        pygame.display.flip()

        if not game_active:
            game_over_screen(screen, score, coins_collected)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

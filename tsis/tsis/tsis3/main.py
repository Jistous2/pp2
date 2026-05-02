import pygame
import sys
import random


from persistence import load_settings, save_settings, load_leaderboard, save_leaderboard
from ui import Button, draw_text
from racer import Player, Enemy, Obstacle, Coin, PowerUp


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("TSIS 3: Racer Game")
    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont("Arial", 48, bold=True)
    font_medium = pygame.font.SysFont("Arial", 32)
    font_small = pygame.font.SysFont("Arial", 24)
    settings = load_settings()
    leaderboard = load_leaderboard()
    state = "MENU"

    player = None
    enemies = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    score = 0
    coins_collected = 0
    distance = 0
    base_speed = 5
    bg_y = 0
    player_name = ""

    btn_play = Button(300, 200, 200, 50, "Play", font_medium)
    btn_leaderboard = Button(300, 270, 200, 50, "Leaderboard", font_medium)
    btn_settings = Button(300, 340, 200, 50, "Settings", font_medium)
    btn_quit = Button(300, 410, 200, 50, "Quit", font_medium)

    btn_color = Button(300, 200, 200, 50, f"Color: {settings['car_color']}", font_medium)
    btn_diff = Button(300, 270, 200, 50, f"Diff: {settings['difficulty']}", font_medium)
    btn_sound = Button(300, 340, 200, 50, f"Sound: {'On' if settings['sound'] else 'Off'}", font_medium)
    btn_back_settings = Button(300, 410, 200, 50, "Back", font_medium)

    btn_back_leaderboard = Button(300, 500, 200, 50, "Back", font_medium)

    btn_retry = Button(300, 350, 200, 50, "Retry", font_medium)
    btn_menu_go = Button(300, 420, 200, 50, "Main Menu", font_medium)

    SPAWN_ENEMY = pygame.USEREVENT + 1
    SPAWN_OBSTACLE = pygame.USEREVENT + 2
    SPAWN_COIN = pygame.USEREVENT + 3
    SPAWN_POWERUP = pygame.USEREVENT + 4

    def start_game():
        nonlocal player, enemies, obstacles, coins, powerups, all_sprites, score, coins_collected, distance, base_speed
        enemies.empty()
        obstacles.empty()
        coins.empty()
        powerups.empty()
        all_sprites.empty()
        score = 0
        coins_collected = 0
        distance = 0
        if settings['difficulty'] == 'easy': base_speed = 3
        elif settings['difficulty'] == 'normal': base_speed = 5
        elif settings['difficulty'] == 'hard': base_speed = 8
        player = Player(settings['car_color'])
        all_sprites.add(player)
        pygame.time.set_timer(SPAWN_ENEMY, 1500)
        pygame.time.set_timer(SPAWN_OBSTACLE, 2500)
        pygame.time.set_timer(SPAWN_COIN, 1000)
        pygame.time.set_timer(SPAWN_POWERUP, 10000)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "MENU":
                btn_play.check_hover(mouse_pos)
                btn_leaderboard.check_hover(mouse_pos)
                btn_settings.check_hover(mouse_pos)
                btn_quit.check_hover(mouse_pos)

                if btn_play.is_clicked(event):
                    player_name = ""
                    state = "NAME_INPUT"
                elif btn_leaderboard.is_clicked(event):
                    state = "LEADERBOARD"
                elif btn_settings.is_clicked(event):
                    state = "SETTINGS"
                elif btn_quit.is_clicked(event):
                    running = False

            elif state == "SETTINGS":
                btn_color.check_hover(mouse_pos)
                btn_diff.check_hover(mouse_pos)
                btn_sound.check_hover(mouse_pos)
                btn_back_settings.check_hover(mouse_pos)

                if btn_color.is_clicked(event):
                    colors = ['red', 'blue', 'green']
                    idx = (colors.index(settings['car_color']) + 1) % len(colors)
                    settings['car_color'] = colors[idx]
                    btn_color.text = f"Color: {settings['car_color']}"
                    save_settings(settings)
                elif btn_diff.is_clicked(event):
                    diffs = ['easy', 'normal', 'hard']
                    idx = (diffs.index(settings['difficulty']) + 1) % len(diffs)
                    settings['difficulty'] = diffs[idx]
                    btn_diff.text = f"Diff: {settings['difficulty']}"
                    save_settings(settings)
                elif btn_sound.is_clicked(event):
                    settings['sound'] = not settings['sound']
                    btn_sound.text = f"Sound: {'On' if settings['sound'] else 'Off'}"
                    save_settings(settings)
                elif btn_back_settings.is_clicked(event):
                    state = "MENU"

            elif state == "LEADERBOARD":
                btn_back_leaderboard.check_hover(mouse_pos)
                if btn_back_leaderboard.is_clicked(event):
                    state = "MENU"

            elif state == "NAME_INPUT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(player_name) > 0:
                        state = "PLAYING"
                        start_game()
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 15:
                            player_name += event.unicode

            elif state == "GAME_OVER":
                btn_retry.check_hover(mouse_pos)
                btn_menu_go.check_hover(mouse_pos)
                if btn_retry.is_clicked(event):
                    state = "PLAYING"
                    start_game()
                elif btn_menu_go.is_clicked(event):
                    state = "MENU"

            elif state == "PLAYING":
                if event.type == SPAWN_ENEMY:
                    e = Enemy(base_speed + random.randint(1, 3))
                    enemies.add(e)
                    all_sprites.add(e)
                elif event.type == SPAWN_OBSTACLE:
                    o = Obstacle(base_speed)
                    obstacles.add(o)
                    all_sprites.add(o)
                elif event.type == SPAWN_COIN:
                    c = Coin(base_speed)
                    coins.add(c)
                    all_sprites.add(c)
                elif event.type == SPAWN_POWERUP:
                    p = PowerUp(base_speed)
                    powerups.add(p)
                    all_sprites.add(p)

        screen.fill(GRAY)

        if state == "MENU":
            draw_text(screen, "RACER GAME", font_large, WHITE, SCREEN_WIDTH//2, 100, center=True)
            btn_play.draw(screen)
            btn_leaderboard.draw(screen)
            btn_settings.draw(screen)
            btn_quit.draw(screen)

        elif state == "SETTINGS":
            draw_text(screen, "SETTINGS", font_large, WHITE, SCREEN_WIDTH//2, 100, center=True)
            btn_color.draw(screen)
            btn_diff.draw(screen)
            btn_sound.draw(screen)
            btn_back_settings.draw(screen)

        elif state == "LEADERBOARD":
            draw_text(screen, "TOP 10 SCORES", font_large, WHITE, SCREEN_WIDTH//2, 50, center=True)
            y = 120
            for i, entry in enumerate(leaderboard):
                text = f"{i+1}. {entry['name']} - Score: {entry['score']} - Dist: {entry['distance']}m"
                draw_text(screen, text, font_medium, WHITE, 150, y)
                y += 35
            btn_back_leaderboard.draw(screen)

        elif state == "NAME_INPUT":
            draw_text(screen, "ENTER YOUR NAME:", font_large, WHITE, SCREEN_WIDTH//2, 200, center=True)
            draw_text(screen, player_name + "|", font_large, YELLOW, SCREEN_WIDTH//2, 300, center=True)
            draw_text(screen, "Press ENTER to start", font_medium, WHITE, SCREEN_WIDTH//2, 400, center=True)

        elif state == "PLAYING":
            current_speed = base_speed + (5 if player.is_nitro else 0)
            bg_y += current_speed
            if bg_y >= 100:
                bg_y = 0
            for i in range(5):
                pygame.draw.line(screen, WHITE, (i * 200, 0), (i * 200, SCREEN_HEIGHT), 5)
            for i in range(1, 4):
                for y in range(-100, SCREEN_HEIGHT, 100):
                    pygame.draw.line(screen, WHITE, (i * 200, y + bg_y), (i * 200, y + bg_y + 50), 2)

            player.move()
            player.update_powerups()
            for entity in all_sprites:
                if entity != player:
                    entity.move()

            distance += current_speed // 5
            score = distance + coins_collected * 10

            if distance % 1000 == 0 and distance > 0:
                base_speed += 1

            collected = pygame.sprite.spritecollide(player, coins, True)
            for c in collected:
                coins_collected += c.weight

            powers = pygame.sprite.spritecollide(player, powerups, True)
            for p in powers:
                if p.type == 'nitro':
                    player.is_nitro = True
                    player.nitro_timer = 180
                elif p.type == 'shield':
                    player.has_shield = True
                elif p.type == 'repair':
                    for obs in obstacles:
                        obs.kill()

            hit_enemies = pygame.sprite.spritecollide(player, enemies, False)
            hit_obstacles = pygame.sprite.spritecollide(player, obstacles, False)

            if hit_enemies or hit_obstacles:
                if player.has_shield:
                    player.has_shield = False
                    for h in hit_enemies + hit_obstacles:
                        h.kill()
                else:
                    state = "GAME_OVER"
                    pygame.time.set_timer(SPAWN_ENEMY, 0)
                    pygame.time.set_timer(SPAWN_OBSTACLE, 0)
                    pygame.time.set_timer(SPAWN_COIN, 0)
                    pygame.time.set_timer(SPAWN_POWERUP, 0)
                    save_leaderboard({
                        'name': player_name,
                        'score': score,
                        'distance': distance
                    })
                    leaderboard = load_leaderboard()

            for entity in all_sprites:
                entity.draw(screen) if hasattr(entity, 'draw') else screen.blit(entity.image, entity.rect)

            draw_text(screen, f"Score: {score}", font_medium, WHITE, 10, 10)
            draw_text(screen, f"Coins: {coins_collected}", font_medium, YELLOW, 10, 50)
            draw_text(screen, f"Dist: {distance}m", font_medium, WHITE, 10, 90)

            if player.has_shield:
                draw_text(screen, "SHIELD ACTIVE", font_small, CYAN, SCREEN_WIDTH - 150, 10)
            if player.is_nitro:
                draw_text(screen, f"NITRO: {player.nitro_timer//60}s", font_small, RED, SCREEN_WIDTH - 150, 40)

        elif state == "GAME_OVER":
            draw_text(screen, "GAME OVER", font_large, RED, SCREEN_WIDTH//2, 150, center=True)
            draw_text(screen, f"Score: {score}", font_medium, WHITE, SCREEN_WIDTH//2, 220, center=True)
            draw_text(screen, f"Distance: {distance}m", font_medium, WHITE, SCREEN_WIDTH//2, 270, center=True)
            btn_retry.draw(screen)
            btn_menu_go.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

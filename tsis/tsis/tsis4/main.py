import pygame
import sys

from db import init_db, save_score, get_top_10, get_personal_best
from settings_manager import load_settings, save_settings
from ui import Button, draw_text
from game import SnakeGame, WIDTH, HEIGHT

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 4: Advanced Snake with DB")

    init_db()
    settings = load_settings()

    font_large = pygame.font.SysFont("Arial", 48, bold=True)
    font_medium = pygame.font.SysFont("Arial", 32)
    font_small = pygame.font.SysFont("Arial", 24)

    state = "MENU"

    btn_play = Button(300, 200, 200, 50, "Play", font_medium)
    btn_leaderboard = Button(300, 270, 200, 50, "Leaderboard", font_medium)
    btn_settings = Button(300, 340, 200, 50, "Settings", font_medium)
    btn_quit = Button(300, 410, 200, 50, "Quit", font_medium)

    btn_color = Button(300, 200, 200, 50, "Color: Green", font_medium)
    btn_grid = Button(300, 270, 200, 50, "Grid: On", font_medium)
    btn_sound = Button(300, 340, 200, 50, "Sound: On", font_medium)
    btn_back_set = Button(300, 410, 200, 50, "Save & Back", font_medium)

    btn_back_lb = Button(300, 500, 200, 50, "Back", font_medium)

    btn_retry = Button(300, 350, 200, 50, "Retry", font_medium)
    btn_menu_go = Button(300, 420, 200, 50, "Main Menu", font_medium)

    player_name = ""
    personal_best = 0
    top_10 = []

    game = SnakeGame(settings)
    clock = pygame.time.Clock()

    def update_settings_buttons():
        color_str = "Green"
        if settings['snake_color'] == [255, 0, 0]: color_str = "Red"
        elif settings['snake_color'] == [0, 0, 255]: color_str = "Blue"
        btn_color.text = f"Color: {color_str}"
        btn_grid.text = f"Grid: {'On' if settings['grid_overlay'] else 'Off'}"
        btn_sound.text = f"Sound: {'On' if settings['sound'] else 'Off'}"

    update_settings_buttons()

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
                    top_10 = get_top_10()
                    state = "LEADERBOARD"
                elif btn_settings.is_clicked(event):
                    state = "SETTINGS"
                elif btn_quit.is_clicked(event):
                    running = False

            elif state == "NAME_INPUT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(player_name) > 0:
                        personal_best = get_personal_best(player_name)
                        game = SnakeGame(settings)
                        state = "PLAYING"
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 15:
                            player_name += event.unicode

            elif state == "SETTINGS":
                btn_color.check_hover(mouse_pos)
                btn_grid.check_hover(mouse_pos)
                btn_sound.check_hover(mouse_pos)
                btn_back_set.check_hover(mouse_pos)
                if btn_color.is_clicked(event):
                    if settings['snake_color'] == [0, 255, 0]: settings['snake_color'] = [255, 0, 0]
                    elif settings['snake_color'] == [255, 0, 0]: settings['snake_color'] = [0, 0, 255]
                    else: settings['snake_color'] = [0, 255, 0]
                    update_settings_buttons()
                elif btn_grid.is_clicked(event):
                    settings['grid_overlay'] = not settings['grid_overlay']
                    update_settings_buttons()
                elif btn_sound.is_clicked(event):
                    settings['sound'] = not settings['sound']
                    update_settings_buttons()
                elif btn_back_set.is_clicked(event):
                    save_settings(settings)
                    state = "MENU"

            elif state == "LEADERBOARD":
                btn_back_lb.check_hover(mouse_pos)
                if btn_back_lb.is_clicked(event):
                    state = "MENU"

            elif state == "PLAYING":
                game.handle_input(event)

            elif state == "GAME_OVER":
                btn_retry.check_hover(mouse_pos)
                btn_menu_go.check_hover(mouse_pos)
                if btn_retry.is_clicked(event):
                    game = SnakeGame(settings)
                    state = "PLAYING"
                elif btn_menu_go.is_clicked(event):
                    state = "MENU"

        screen.fill(BLACK)

        if state == "MENU":
            draw_text(screen, "SNAKE DB", font_large, GREEN, WIDTH//2, 100, center=True)
            btn_play.draw(screen)
            btn_leaderboard.draw(screen)
            btn_settings.draw(screen)
            btn_quit.draw(screen)

        elif state == "NAME_INPUT":
            draw_text(screen, "ENTER USERNAME:", font_large, WHITE, WIDTH//2, 200, center=True)
            draw_text(screen, player_name + "|", font_large, YELLOW, WIDTH//2, 300, center=True)
            draw_text(screen, "Press ENTER", font_medium, GRAY, WIDTH//2, 400, center=True)

        elif state == "SETTINGS":
            draw_text(screen, "SETTINGS", font_large, WHITE, WIDTH//2, 100, center=True)
            btn_color.draw(screen)
            btn_grid.draw(screen)
            btn_sound.draw(screen)
            btn_back_set.draw(screen)

        elif state == "LEADERBOARD":
            draw_text(screen, "TOP 10 SCORES", font_large, YELLOW, WIDTH//2, 50, center=True)
            y = 120
            for i, row in enumerate(top_10):
                username, score, lvl, date = row
                date_str = date.strftime("%Y-%m-%d")
                text = f"{i+1}. {username} | Score: {score} | Lvl: {lvl} | {date_str}"
                draw_text(screen, text, font_small, WHITE, WIDTH//2, y, center=True)
                y += 35
            btn_back_lb.draw(screen)

        elif state == "PLAYING":
            game.update()
            if game.is_game_over:
                save_score(player_name, game.score, game.level)
                if game.score > personal_best:
                    personal_best = game.score
                state = "GAME_OVER"
            else:
                game.draw(screen)
                draw_text(screen, f"Score: {game.score}", font_small, WHITE, 10, 10)
                draw_text(screen, f"Level: {game.level}", font_small, WHITE, 10, 40)
                draw_text(screen, f"Best: {personal_best}", font_small, YELLOW, WIDTH - 120, 10)
                if game.active_powerup == 'speed':
                    draw_text(screen, "SPEED x2", font_small, YELLOW, WIDTH//2, 20, center=True)
                elif game.active_powerup == 'slow':
                    draw_text(screen, "SLOW", font_small, (173, 216, 230), WIDTH//2, 20, center=True)
                elif game.has_shield:
                    draw_text(screen, "SHIELD", font_small, (0, 0, 255), WIDTH//2, 20, center=True)

        elif state == "GAME_OVER":
            draw_text(screen, "GAME OVER", font_large, RED, WIDTH//2, 150, center=True)
            draw_text(screen, f"Final Score: {game.score}", font_medium, WHITE, WIDTH//2, 220, center=True)
            draw_text(screen, f"Level Reached: {game.level}", font_medium, WHITE, WIDTH//2, 270, center=True)
            btn_retry.draw(screen)
            btn_menu_go.draw(screen)

        pygame.display.flip()

        if state == "PLAYING" and not game.is_game_over:
            clock.tick(game.get_current_speed())
        else:
            clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

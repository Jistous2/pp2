import pygame
import sys
import os
from player import MusicPlayer

WIDTH, HEIGHT = 700, 400
FPS = 30
MUSIC_DIR = os.path.join(os.path.dirname(__file__), "music")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont("Arial", 32)
font_medium = pygame.font.SysFont("Arial", 22)
font_small = pygame.font.SysFont("Arial", 16)

player = MusicPlayer(MUSIC_DIR)

BG = (20, 20, 30)
ACCENT = (80, 160, 255)
WHITE = (255, 255, 255)
GRAY = (140, 140, 160)

controls = [
    ("P", "Play"),
    ("S", "Stop"),
    ("N", "Next"),
    ("B", "Previous"),
    ("Q", "Quit"),
]


def draw_ui():
    screen.fill(BG)

    title = font_large.render("Music Player", True, ACCENT)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    track_surf = font_medium.render(f"Track: {player.current_track_name()}", True, WHITE)
    screen.blit(track_surf, (WIDTH // 2 - track_surf.get_width() // 2, 100))

    status_surf = font_medium.render(f"Status: {player.status()}", True, ACCENT)
    screen.blit(status_surf, (WIDTH // 2 - status_surf.get_width() // 2, 140))

    if player.playlist:
        idx_surf = font_small.render(
            f"Track {player.current_index + 1} of {len(player.playlist)}", True, GRAY
        )
        screen.blit(idx_surf, (WIDTH // 2 - idx_surf.get_width() // 2, 175))

    y = 230
    for key, action in controls:
        line = font_small.render(f"[{key}]  {action}", True, GRAY)
        screen.blit(line, (WIDTH // 2 - 60, y))
        y += 28

    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.prev_track()
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    if player.is_playing and not pygame.mixer.music.get_busy():
        player.next_track()

    draw_ui()
    clock.tick(FPS)

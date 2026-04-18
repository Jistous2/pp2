import pygame
import sys
from clock import MickeysClock

WIDTH, HEIGHT = 700, 500
FPS = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")
clock_tick = pygame.time.Clock()

mickey_clock = MickeysClock(WIDTH, HEIGHT)
BG_COLOR = (245, 235, 210)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)
    mickey_clock.draw(screen)
    pygame.display.flip()
    clock_tick.tick(FPS)

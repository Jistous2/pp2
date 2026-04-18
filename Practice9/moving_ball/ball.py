import pygame


class Ball:
    def __init__(self, screen_width, screen_height, radius=25, step=20):
        self.radius = radius
        self.step = step
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.color = (255, 0, 0)

    def move(self, direction):
        dx, dy = 0, 0
        if direction == "up":
            dy = -self.step
        elif direction == "down":
            dy = self.step
        elif direction == "left":
            dx = -self.step
        elif direction == "right":
            dx = self.step

        new_x = self.x + dx
        new_y = self.y + dy

        if self.radius <= new_x <= self.screen_width - self.radius:
            self.x = new_x
        if self.radius <= new_y <= self.screen_height - self.radius:
            self.y = new_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

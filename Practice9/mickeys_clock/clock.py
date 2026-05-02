import pygame
import math
import datetime
import os


class MickeysClock:
    def __init__(self, screen_width, screen_height):
        self.cx = screen_width // 2
        self.cy = screen_height // 2

        img_path = os.path.join(os.path.dirname(__file__), "images", "mickeyclock.jpeg")
        if os.path.exists(img_path):
            raw = pygame.image.load(img_path).convert()
            self.mickey_img = pygame.transform.smoothscale(raw, (500, 420))
        else:
            self.mickey_img = None

        self.font = pygame.font.SysFont("Arial", 40, bold=True)

    def _hand_endpoint(self, angle_deg, length):
        rad = math.radians(angle_deg - 90)
        x = self.cx + int(math.cos(rad) * length)
        y = self.cy + int(math.sin(rad) * length)
        return (x, y)

    def draw(self, surface):
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        if self.mickey_img:
            rect = self.mickey_img.get_rect(center=(self.cx, self.cy))
            surface.blit(self.mickey_img, rect)

        min_angle = minutes / 60 * 360
        sec_angle = seconds / 60 * 360

        min_end = self._hand_endpoint(min_angle, 100)
        pygame.draw.line(surface, (20, 20, 20), (self.cx, self.cy), min_end, 7)

        sec_end = self._hand_endpoint(sec_angle, 120)
        pygame.draw.line(surface, (200, 0, 0), (self.cx, self.cy), sec_end, 4)

        pygame.draw.circle(surface, (40, 40, 40), (self.cx, self.cy), 8)

        time_str = now.strftime("%H:%M:%S")
        text = self.font.render(time_str, True, (30, 30, 30))
        surface.blit(text, (self.cx - text.get_width() // 2, self.cy + 130))

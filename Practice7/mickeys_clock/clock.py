import pygame
import math
import datetime
import os


class MickeysClock:
    def __init__(self, screen_width, screen_height):
        self.cx = screen_width // 2
        self.cy = screen_height // 2

        hand_path = os.path.join(os.path.dirname(__file__), "images", "mickey_hand.png")
        if os.path.exists(hand_path):
            raw = pygame.image.load(hand_path).convert_alpha()
            self.hand_img = pygame.transform.smoothscale(raw, (40, 120))
        else:
            self.hand_img = self._make_default_hand()

        self.font = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 22)

    def _make_default_hand(self):
        surf = pygame.Surface((40, 120), pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 200, 200), (15, 10, 10, 90), border_radius=5)
        pygame.draw.circle(surf, (220, 220, 220), (20, 10), 14)
        return surf

    def _rotate_hand(self, angle_deg, length_scale=1.0):
        """Return (rotated_surface, rect) for a hand rotated around its base."""
        img = self.hand_img
        if length_scale != 1.0:
            new_h = int(img.get_height() * length_scale)
            img = pygame.transform.smoothscale(img, (img.get_width(), new_h))

        # rotate — pygame rotates counter-clockwise; we want clockwise from 12 o'clock
        rotated = pygame.transform.rotate(img, -angle_deg)
        # pivot is at bottom-center of original image; after rotation recalc offset
        orig_w, orig_h = img.get_size()
        pivot = pygame.math.Vector2(orig_w / 2, orig_h)  # base of hand
        offset = pygame.math.Vector2(orig_w / 2 - pivot.x, pivot.y - orig_h / 2)
        offset.rotate_ip(angle_deg)
        rect = rotated.get_rect(center=(self.cx + offset.x, self.cy + offset.y))
        return rotated, rect

    def draw(self, surface):
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        # 0 min/sec → pointing up (−90°), one full rotation = 360°
        min_angle = minutes / 60 * 360
        sec_angle = seconds / 60 * 360

        # Draw minute hand (right hand in task description)
        min_surf, min_rect = self._rotate_hand(min_angle, length_scale=1.0)
        surface.blit(min_surf, min_rect)

        # Draw second hand (left hand) — slightly shorter
        sec_surf, sec_rect = self._rotate_hand(sec_angle, length_scale=0.8)
        surface.blit(sec_surf, sec_rect)

        # Clock center dot
        pygame.draw.circle(surface, (50, 50, 50), (self.cx, self.cy), 10)

        # Digital time overlay
        time_str = now.strftime("%H:%M:%S")
        text = self.font.render(time_str, True, (30, 30, 30))
        surface.blit(text, (self.cx - text.get_width() // 2, self.cy + 130))

        label = self.font_small.render("Right = minutes | Left = seconds", True, (120, 120, 120))
        surface.blit(label, (self.cx - label.get_width() // 2, self.cy + 190))

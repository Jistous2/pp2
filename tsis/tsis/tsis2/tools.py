import pygame


def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    width, height = surface.get_size()
    stack = [(x, y)]
    while len(stack) > 0:
        curr_x, curr_y = stack.pop()
        if curr_x < 0 or curr_x >= width or curr_y < 0 or curr_y >= height:
            continue
        if surface.get_at((curr_x, curr_y)) == target_color:
            surface.set_at((curr_x, curr_y), new_color)
            stack.append((curr_x + 1, curr_y))
            stack.append((curr_x - 1, curr_y))
            stack.append((curr_x, curr_y + 1))
            stack.append((curr_x, curr_y - 1))


def draw_rhombus(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    points = [
        (x1 + (x2 - x1) // 2, y1),
        (x2, y1 + (y2 - y1) // 2),
        (x1 + (x2 - x1) // 2, y2),
        (x1, y1 + (y2 - y1) // 2)
    ]
    pygame.draw.polygon(surface, color, points, width)


def draw_equilateral_triangle(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    side = x2 - x1
    height = int(side * (3**0.5) / 2)
    points = [
        (x1, y2),
        (x2, y2),
        (x1 + side // 2, y2 - height)
    ]
    pygame.draw.polygon(surface, color, points, width)


def draw_right_triangle(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]
    pygame.draw.polygon(surface, color, points, width)


def draw_square(surface, color, start_pos, end_pos, width):
    x1, y1 = start_pos
    x2, y2 = end_pos
    side = max(abs(x2 - x1), abs(y2 - y1))
    if x2 < x1:
        x2 = x1 - side
    else:
        x2 = x1 + side
    if y2 < y1:
        y2 = y1 - side
    else:
        y2 = y1 + side
    rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
    rect.normalize()
    pygame.draw.rect(surface, color, rect, width)

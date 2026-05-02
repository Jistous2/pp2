import pygame
import datetime
import math

from tools import flood_fill, draw_rhombus, draw_equilateral_triangle, draw_right_triangle, draw_square

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))
pygame.display.set_caption("Extended Paint")

COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0)
}

palette_colors = [
    COLORS["black"], COLORS["red"], COLORS["green"],
    COLORS["blue"], COLORS["yellow"], COLORS["purple"], COLORS["orange"]
]

tools_list = [
    ("pencil", "Pencil"), ("line", "Line"), ("rect", "Rect"),
    ("circle", "Circle"), ("square", "Square"), ("e_triangle", "E.Tri"),
    ("r_triangle", "R.Tri"), ("rhombus", "Rhombus"), ("fill", "Fill"),
    ("text", "Text"), ("eraser", "Eraser")
]

current_color = COLORS["black"]
thickness = 2
tool = "pencil"

font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 16)
text_input = ""
text_pos = (0, 0)
typing = False

drawing = False
start_pos = (0, 0)
last_pos = (0, 0)


def save_canvas():
    now = datetime.datetime.now()
    time_str = now.strftime('%Y%m%d_%H%M%S')
    filename = f"save_{time_str}.png"
    pygame.image.save(canvas, filename)


def draw_ui(screen):
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 40))
    for i, (t_id, t_name) in enumerate(tools_list):
        rect = pygame.Rect(i * 80, 0, 80, 40)
        if t_id == tool:
            pygame.draw.rect(screen, (150, 150, 150), rect)
        pygame.draw.rect(screen, COLORS["black"], rect, 1)
        text_surf = small_font.render(t_name, True, COLORS["black"])
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    pygame.draw.rect(screen, (220, 220, 220), (0, HEIGHT - 50, WIDTH, 50))
    for i, color in enumerate(palette_colors):
        pygame.draw.rect(screen, color, (10 + i * 40, HEIGHT - 40, 30, 30))
        if color == current_color:
            pygame.draw.rect(screen, COLORS["black"], (10 + i * 40, HEIGHT - 40, 30, 30), 2)
            pygame.draw.rect(screen, COLORS["white"], (12 + i * 40, HEIGHT - 38, 26, 26), 1)

    info_text = f"Size: {thickness} (keys 1,2,3) | Ctrl+S: Save"
    info_surface = font.render(info_text, True, COLORS["black"])
    screen.blit(info_surface, (350, HEIGHT - 35))


running = True
while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if typing:
                if event.key == pygame.K_RETURN:
                    img = font.render(text_input, True, current_color)
                    canvas.blit(img, text_pos)
                    typing = False
                    text_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_input = ""
                else:
                    text_input += event.unicode
            else:
                if event.key == pygame.K_1: thickness = 2
                if event.key == pygame.K_2: thickness = 5
                if event.key == pygame.K_3: thickness = 10
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    save_canvas()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if mouse_y <= 40:
                index = mouse_x // 80
                if index < len(tools_list):
                    tool = tools_list[index][0]
                continue
            if mouse_y >= HEIGHT - 50:
                for i, color in enumerate(palette_colors):
                    rect = pygame.Rect(10 + i * 40, HEIGHT - 40, 30, 30)
                    if rect.collidepoint(mouse_x, mouse_y):
                        current_color = color
                continue
            if tool == "fill":
                flood_fill(canvas, mouse_x, mouse_y, current_color)
            elif tool == "text":
                typing = True
                text_pos = event.pos
                text_input = ""
            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if event.pos[1] > 40:
                    if tool == "pencil":
                        pygame.draw.line(canvas, current_color, last_pos, event.pos, thickness)
                        last_pos = event.pos
                    elif tool == "eraser":
                        pygame.draw.circle(canvas, COLORS["white"], event.pos, thickness * 2)

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos
                if end_pos[1] < 40:
                    end_pos = (end_pos[0], 40)
                if tool == "line":
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, thickness)
                elif tool == "rect":
                    rect_w = end_pos[0] - start_pos[0]
                    rect_h = end_pos[1] - start_pos[1]
                    rect = pygame.Rect(start_pos[0], start_pos[1], rect_w, rect_h)
                    rect.normalize()
                    pygame.draw.rect(canvas, current_color, rect, thickness)
                elif tool == "circle":
                    radius = int(math.sqrt((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2))
                    pygame.draw.circle(canvas, current_color, start_pos, radius, thickness)
                elif tool == "square":
                    draw_square(canvas, current_color, start_pos, end_pos, thickness)
                elif tool == "e_triangle":
                    draw_equilateral_triangle(canvas, current_color, start_pos, end_pos, thickness)
                elif tool == "r_triangle":
                    draw_right_triangle(canvas, current_color, start_pos, end_pos, thickness)
                elif tool == "rhombus":
                    draw_rhombus(canvas, current_color, start_pos, end_pos, thickness)
                drawing = False

    if drawing and tool not in ["pencil", "eraser", "fill", "text"]:
        curr_pos = pygame.mouse.get_pos()
        if curr_pos[1] < 40:
            curr_pos = (curr_pos[0], 40)
        if tool == "line":
            pygame.draw.line(screen, current_color, start_pos, curr_pos, thickness)
        elif tool == "rect":
            rect_w = curr_pos[0] - start_pos[0]
            rect_h = curr_pos[1] - start_pos[1]
            rect = pygame.Rect(start_pos[0], start_pos[1], rect_w, rect_h)
            rect.normalize()
            pygame.draw.rect(screen, current_color, rect, thickness)
        elif tool == "circle":
            radius = int(math.sqrt((curr_pos[0]-start_pos[0])**2 + (curr_pos[1]-start_pos[1])**2))
            pygame.draw.circle(screen, current_color, start_pos, radius, thickness)
        elif tool == "square":
            draw_square(screen, current_color, start_pos, curr_pos, thickness)
        elif tool == "e_triangle":
            draw_equilateral_triangle(screen, current_color, start_pos, curr_pos, thickness)
        elif tool == "r_triangle":
            draw_right_triangle(screen, current_color, start_pos, curr_pos, thickness)
        elif tool == "rhombus":
            draw_rhombus(screen, current_color, start_pos, curr_pos, thickness)

    if typing:
        txt_surface = font.render(text_input + "|", True, current_color)
        screen.blit(txt_surface, text_pos)

    draw_ui(screen)
    pygame.display.flip()

pygame.quit()

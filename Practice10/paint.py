import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TOOLBAR_HEIGHT = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

font = pygame.font.SysFont("Arial", 16)
clock = pygame.time.Clock()

COLORS = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, WHITE]

TOOL_PENCIL = "pencil"
TOOL_RECT = "rect"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"

TOOLS = [TOOL_PENCIL, TOOL_RECT, TOOL_CIRCLE, TOOL_ERASER]


def draw_toolbar(surface, current_tool, current_color, brush_size):
    pygame.draw.rect(surface, GRAY, (0, 0, SCREEN_WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(surface, DARK_GRAY, (0, TOOLBAR_HEIGHT), (SCREEN_WIDTH, TOOLBAR_HEIGHT), 2)

    tool_labels = {"pencil": "Pencil", "rect": "Rect", "circle": "Circle", "eraser": "Eraser"}
    x = 10
    for tool in TOOLS:
        label = tool_labels[tool]
        bg = (180, 210, 255) if tool == current_tool else (230, 230, 230)
        btn_rect = pygame.Rect(x, 5, 65, 25)
        pygame.draw.rect(surface, bg, btn_rect)
        pygame.draw.rect(surface, BLACK, btn_rect, 1)
        text = font.render(label, True, BLACK)
        surface.blit(text, (x + (65 - text.get_width()) // 2, 9))
        x += 75

    color_x = 330
    color_y = 5
    color_size = 22
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(color_x + i * (color_size + 4), color_y, color_size, color_size)
        pygame.draw.rect(surface, color, rect)
        if color == current_color:
            pygame.draw.rect(surface, RED, rect, 3)
        else:
            pygame.draw.rect(surface, BLACK, rect, 1)

    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    surface.blit(size_text, (color_x, 32))

    minus_rect = pygame.Rect(color_x + 70, 30, 20, 20)
    plus_rect = pygame.Rect(color_x + 95, 30, 20, 20)
    pygame.draw.rect(surface, (230, 230, 230), minus_rect)
    pygame.draw.rect(surface, BLACK, minus_rect, 1)
    pygame.draw.rect(surface, (230, 230, 230), plus_rect)
    pygame.draw.rect(surface, BLACK, plus_rect, 1)
    minus_text = font.render("-", True, BLACK)
    plus_text = font.render("+", True, BLACK)
    surface.blit(minus_text, (color_x + 75, 32))
    surface.blit(plus_text, (color_x + 99, 32))

    preview_rect = pygame.Rect(SCREEN_WIDTH - 50, 10, 35, 35)
    pygame.draw.rect(surface, WHITE, preview_rect)
    pygame.draw.rect(surface, BLACK, preview_rect, 1)
    pygame.draw.rect(surface, current_color, (preview_rect.x + 2, preview_rect.y + 2, 31, 31))

    return minus_rect, plus_rect


def get_tool_at(pos):
    x = 10
    for tool in TOOLS:
        btn_rect = pygame.Rect(x, 5, 65, 25)
        if btn_rect.collidepoint(pos):
            return tool
        x += 75
    return None


def get_color_at(pos):
    color_x = 330
    color_y = 5
    color_size = 22
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(color_x + i * (color_size + 4), color_y, color_size, color_size)
        if rect.collidepoint(pos):
            return color
    return None


def main():
    canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    current_tool = TOOL_PENCIL
    current_color = BLACK
    brush_size = 4
    drawing = False
    start_pos = None
    last_pos = None
    canvas_snapshot = None

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos

                    if my < TOOLBAR_HEIGHT:
                        tool = get_tool_at(event.pos)
                        if tool:
                            current_tool = tool

                        color = get_color_at(event.pos)
                        if color is not None:
                            current_color = color

                        color_x = 330
                        minus_rect = pygame.Rect(color_x + 70, 30, 20, 20)
                        plus_rect = pygame.Rect(color_x + 95, 30, 20, 20)
                        if minus_rect.collidepoint(event.pos) and brush_size > 1:
                            brush_size -= 1
                        if plus_rect.collidepoint(event.pos) and brush_size < 50:
                            brush_size += 1
                    else:
                        drawing = True
                        canvas_pos = (mx, my - TOOLBAR_HEIGHT)
                        start_pos = canvas_pos
                        last_pos = canvas_pos

                        if current_tool in (TOOL_RECT, TOOL_CIRCLE):
                            canvas_snapshot = canvas.copy()
                        elif current_tool == TOOL_PENCIL:
                            pygame.draw.circle(canvas, current_color, canvas_pos, brush_size)
                        elif current_tool == TOOL_ERASER:
                            pygame.draw.circle(canvas, WHITE, canvas_pos, brush_size + 5)

            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    mx, my = event.pos
                    canvas_pos = (mx, my - TOOLBAR_HEIGHT)

                    if current_tool == TOOL_PENCIL:
                        if last_pos:
                            pygame.draw.line(canvas, current_color, last_pos, canvas_pos, brush_size * 2)
                        pygame.draw.circle(canvas, current_color, canvas_pos, brush_size)
                        last_pos = canvas_pos

                    elif current_tool == TOOL_ERASER:
                        if last_pos:
                            pygame.draw.line(canvas, WHITE, last_pos, canvas_pos, (brush_size + 5) * 2)
                        pygame.draw.circle(canvas, WHITE, canvas_pos, brush_size + 5)
                        last_pos = canvas_pos

                    elif current_tool in (TOOL_RECT, TOOL_CIRCLE):
                        canvas.blit(canvas_snapshot, (0, 0))
                        x1, y1 = start_pos
                        x2, y2 = canvas_pos
                        rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                           abs(x2 - x1), abs(y2 - y1))
                        if current_tool == TOOL_RECT:
                            pygame.draw.rect(canvas, current_color, rect, brush_size)
                        else:
                            cx = (x1 + x2) // 2
                            cy = (y1 + y2) // 2
                            rx = abs(x2 - x1) // 2
                            ry = abs(y2 - y1) // 2
                            if rx > 0 and ry > 0:
                                pygame.draw.ellipse(canvas, current_color, rect, brush_size)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False

                    if current_tool in (TOOL_RECT, TOOL_CIRCLE) and start_pos:
                        mx, my = event.pos
                        canvas_pos = (mx, my - TOOLBAR_HEIGHT)
                        canvas.blit(canvas_snapshot, (0, 0))
                        x1, y1 = start_pos
                        x2, y2 = canvas_pos
                        rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                           abs(x2 - x1), abs(y2 - y1))
                        if current_tool == TOOL_RECT:
                            pygame.draw.rect(canvas, current_color, rect, brush_size)
                        else:
                            if abs(x2 - x1) > 0 and abs(y2 - y1) > 0:
                                pygame.draw.ellipse(canvas, current_color, rect, brush_size)

                    start_pos = None
                    last_pos = None
                    canvas_snapshot = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    canvas.fill(WHITE)

        screen.fill(WHITE)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))
        draw_toolbar(screen, current_tool, current_color, brush_size)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

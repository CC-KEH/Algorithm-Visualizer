import pygame
import random
from themes.colors import *
from algorithms.sort_algos import *
pygame.init()

SIDE_PADDING = 100  # 50 on left and 50 on right
TOP_PADDING = 150
FONT = pygame.font.SysFont("comicsans", 20)
LARGE_FONT = pygame.font.SysFont("comicsans", 40)


class DrawInformation:
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.lst = lst
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Algorithms Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        list_range = self.max_val - self.min_val
        self.bar_width = round((self.width - SIDE_PADDING) / len(lst))
        self.bar_height = round((self.height - TOP_PADDING) / (list_range))
        self.start_x = SIDE_PADDING // 2


def draw(draw_info):
    draw_info.window.fill(BACKGROUND_COLOR)
    controls = FONT.render(
        "R - Reset | SPACE - Start Sorting | O - Change Sorting Order",
        1,
        FONT_COLOR,
    )
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 5))
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info):
    lst = draw_info.lst
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * (draw_info.bar_height)
        color = GRADIENTS[i % 3]
        # Calculate Exact height dont use draw_info.height
        pygame.draw.rect(
            draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height)
        )


def generate_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        lst.append(random.randint(min_val, max_val))

    return lst


def main():
    run = True
    clock = pygame.time.Clock()
    n = 50
    min_val = 0
    max_val = 100
    lst = generate_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    while run:
        clock.tick(60)
        draw(draw_info)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
            elif event.key == pygame.K_o and not sorting:
                ascending = not ascending

    pygame.quit()


if __name__ == "__main__":
    main()

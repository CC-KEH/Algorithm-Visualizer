import math
import pygame
import random
from system import button,screen
from themes.colors import *
from sort_algos import *
pygame.init()

SIDE_PADDING = 40  # 50 on left and 50 on right
TOP_PADDING = 150
FONT = pygame.font.SysFont("comicsans", 20)
LARGE_FONT = pygame.font.SysFont("comicsans", 40)


class DrawInformation:
    def __init__(self, width, height, lst, window, color=BG_COLOR):
        self.width = width
        self.height = height
        self.lst = lst
        self.window = window
        self.bg_color = color
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        list_range = self.max_val - self.min_val
        self.bar_width = round((self.width - SIDE_PADDING) / len(lst))
        self.bar_height = math.floor((self.height - TOP_PADDING) / (list_range))
        self.start_x = SIDE_PADDING // 2

def draw(draw_info, algorithms, options, output, menu=True):
    draw_info.window.fill(BACKGROUND_COLOR)
    
    # Draw sorting visualizer
    draw_list(draw_info)
    
    if menu:
        # Fill menu portion with black color
        pygame.draw.rect(draw_info.window, BLACK, (draw_info.width, 0, draw_info.window.get_width() - draw_info.width, draw_info.window.get_height()))

        font = pygame.font.SysFont('verdana', 35)
        text = font.render("Algorithms", 1, WHITE)
        top = 0
        ht = 900
        delta = 700
        end = ht//40
        win.blit(text, ((width+delta//2.1), (end-top)/2.5))
        # Draw menu functions
        for algorithm in algorithms:
            algorithm.draw(draw_info.window, BLACK)
        
        text = font.render("Settings", 1, WHITE)
        but_height = ht//14.5
        top += (8*but_height)
        end += (1.9*(3*but_height//2)) + but_height + ht//12
        win.blit(text, (width+delta//2, ((end-top)/2) + top))
        
        for option in options:
            option.draw(draw_info.window, BLACK)
            
        output.draw(draw_info.window, BLACK)    
    pygame.display.update()


def draw_list(draw_info,color_positions={},clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (SIDE_PADDING//2,TOP_PADDING,(draw_info.width-SIDE_PADDING),(draw_info.height-TOP_PADDING))
        pygame.draw.rect(draw_info.window,BACKGROUND_COLOR,clear_rect)
        
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * (draw_info.bar_height)
        color = GRADIENTS[i % 3]
        # Calculate Exact height dont use draw_info.height
        if i in color_positions:
            color = color_positions[i]
            
        pygame.draw.rect(
            draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height)
        )
    if clear_bg:
        pygame.display.update()


def generate_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        lst.append(random.randint(min_val, max_val))

    return lst


def main(window):
    w, ht = pygame.display.get_surface().get_size()
    width = ht #Sort Display
    delta = w - width

    n = 50
    min_val = 0
    max_val = 100
    
    #* Algorithms Panel 
    top_start = ht/10
    but_height = ht//15
    but_width = delta//4
    gap_factor = 5  # * Determines the gap between the buttons
    # * Determines the coordinate from where the button start in x-axis.
    start_factor = 2.7
    algorithms = [
        button(width+delta//start_factor, top_start,
               but_width-but_height, but_height, 'Bubble Sort'),

        button(width+delta//start_factor, top_start + (3*but_height//2),
               but_width-but_height, but_height, 'Selection Sort'),
        
        button(width+delta//start_factor, top_start + (6*but_height//2),
               but_width-but_height, but_height, 'Insertion Sort'),
        
        button(width+delta//start_factor, top_start + (9*but_height//2),
               but_width-but_height, but_height, 'Tim Sort'),

        button(width+delta//start_factor + (gap_factor*but_width//4),
               top_start, but_width-but_height, but_height, "Merge Sort"),

        button(width+delta//start_factor + (gap_factor*but_width//4), top_start +
               (3*but_height//2), but_width-but_height, but_height, 'Quick Sort'),

        button(width+delta//start_factor + (gap_factor*but_width//4), top_start +
               (6*but_height//2), but_width-but_height, but_height, 'Radix Sort'),

        button(width+delta//start_factor + (gap_factor*but_width//4), top_start +
               (9*but_height//2), but_width-but_height, but_height, 'Bucket Sort'),
    ]

    top_start = top_start + (1.9*(3*but_height//2)) + but_height + ht//10
    but_height = ht//15
    but_width = delta//4
    
    #* Options Panel
    top_start = top_start + (1.3*(3*but_height//2)) + ht//10
    but_height = ht//15
    but_width = delta//10
    options = [
        button(width+delta//3, top_start-60, but_width - but_height+50, but_height, "Generate"),
        button(width+delta//3 + 130, top_start-60, but_width - but_height+20, but_height, "Slow"),
        button(width+delta//3 + 230, top_start-60, but_width - but_height+20, but_height, "Fast"),
        button(width+delta//3 + 330, top_start-60, 0, but_height, "-"),
        button(width+delta//3 + 390, top_start-60, 0, but_height, "+"),
    ]
    #* Result Screen
    sc_start = ht-240
    sc_height = 230
    sc_width = delta-delta//3.5
    output = screen(width+delta//4, sc_start, sc_width,
                    sc_height, "Choose an Algorithm")
    output.set_label1(f"Range: {n}")
    output.set_text1("1. + To Increase List Size by 5")
    output.set_text2("2. - To Decrease List Size by 5")
    output.set_text3("3. Choose the algorithm")

    run = True
    clock = pygame.time.Clock()
    lst = generate_list(n, min_val, max_val)
    
    draw_info = DrawInformation(width + 150, width, lst, window)
    
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None
    low = 0
    high = len(draw_info.lst)
    while run:
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algorithm_generator)
                
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, algorithms, options, output)
            
        draw(draw_info,algorithms,options,output)        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()

                if algorithms[0].is_hover(pos) and not sorting:
                    algorithms[0].toggle_color()
                    output.draw(win, (0, 0, 0))
                    sorting = True
                    sorting_algorithm_generator = bubble_sort(draw_info,draw_info.lst,low,high,ascending=True)
                    algorithms[0].toggle_color()
                
                elif algorithms[1].is_hover(pos) and not sorting:
                    algorithms[0].toggle_color()
                    output.draw(win, (0, 0, 0))
                    sorting = True
                    sorting_algorithm_generator = selection_sort(draw_info,draw_info.lst,low,high,ascending=True)
                    algorithms[0].toggle_color()
                
                elif algorithms[2].is_hover(pos) and not sorting:
                    algorithms[0].toggle_color()
                    output.draw(win, (0, 0, 0))
                    sorting = True
                    sorting_algorithm_generator = insertion_sort(draw_info,draw_info.lst,low,high,ascending=True)
                    algorithms[0].toggle_color()
                
                elif algorithms[3].is_hover(pos) and not sorting:
                    algorithms[0].toggle_color()
                    output.draw(win, (0, 0, 0))
                    sorting = True
                    sorting_algorithm_generator = tim_sort(draw_info,draw_info.lst,low,high,ascending=True)
                    algorithms[0].toggle_color()
                
                elif algorithms[4].is_hover(pos) and not sorting:
                    algorithms[0].toggle_color()
                    output.draw(win, (0, 0, 0))
                    sorting = True
                    sorting_algorithm_generator = merge_sort(draw_info,draw_info.lst,low,high,ascending=True)
                    algorithms[0].toggle_color()
                
                elif algorithms[5].is_hover(pos) and not sorting:
                    algorithms[0].toggle_color()
                    output.draw(win, (0, 0, 0))
                    sorting = True
                    sorting_algorithm_generator = quick_sort(draw_info,draw_info.lst,low,high,ascending=True)
                    algorithms[0].toggle_color()
                
                elif algorithms[6].is_hover(pos) and not sorting:
                    algorithms[0].toggle_color()
                    output.draw(win, (0, 0, 0))
                    sorting = True
                    sorting_algorithm_generator = radix_sort(draw_info,draw_info.lst,low,high,ascending=True)
                    algorithms[0].toggle_color()
                
                elif algorithms[7].is_hover(pos) and not sorting:
                    algorithms[0].toggle_color()
                    output.draw(win, (0, 0, 0))
                    sorting = True
                    sorting_algorithm_generator = bucket_sort(draw_info,draw_info.lst,low,high,ascending=True)
                    algorithms[0].toggle_color()
                        
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info,draw_info.lst,low,high,ascending)
            
            elif event.key == pygame.K_o and not sorting:
                ascending = not ascending

    pygame.quit()


if __name__ == "__main__":
    width = 800
    win = pygame.display.set_mode((width+700, width))
    main(win)

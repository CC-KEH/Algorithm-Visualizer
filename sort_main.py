import math
from operator import is_
from turtle import back
import pygame
import random
from system import button,screen,create_button,is_hover
from themes.colors import *
from themes.themes import *
from sort_algos import *
from sort_info import *
import main_app
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

def draw(draw_info, algorithms, back_button, options, output,theme_type, menu=True,is_uniform=False):
    draw_info.window.fill(themes[theme_type]['plane_color'])
    # Draw sorting visualizer
    draw_list(draw_info,is_uniform=is_uniform)
    
    if menu:
        # Fill menu portion with black color
        pygame.draw.rect(draw_info.window, themes[theme_type]["menu_bg_color"], (draw_info.width + 53, 0, draw_info.window.get_width() - draw_info.width, draw_info.window.get_height()))

        font = pygame.font.SysFont('verdana', 35)
        text = font.render("Sorting Algorithms", 1, WHITE)
        top = 0
        ht = 900
        width = ht
        delta = 700
        end = ht//40
        draw_info.window.blit(back_button["image"], back_button["rect"])
        draw_info.window.blit(text, ((width+delta//3.5), (end-top)/2.5))
        # Draw menu functions
        for algorithm in algorithms:
            algorithm.draw(draw_info.window)
        
        text = font.render("Settings", 1, WHITE)
        but_height = ht//14.5
        top += (8*but_height)
        end += (1.9*(3*but_height//2)) + but_height + ht//12
        draw_info.window.blit(text, (width+delta//3 + 45, (end-top) + 1.1*top))
        
        for option in options:
            option.draw(draw_info.window)
            
        output.draw(draw_info.window)    
    pygame.display.update()


# def draw_list(draw_info,color_positions={},clear_bg=False):
#     lst = draw_info.lst
#     if clear_bg:
#         clear_rect = (SIDE_PADDING//2,TOP_PADDING,(draw_info.width-SIDE_PADDING),(draw_info.height-TOP_PADDING))
#         pygame.draw.rect(draw_info.window,BACKGROUND_COLOR,clear_rect)
        
#     for i, val in enumerate(lst):
#         x = draw_info.start_x + i * draw_info.bar_width
#         y = draw_info.height - (val - draw_info.min_val) * (draw_info.bar_height)
#         color = GRADIENTS[i % 3]
#         # Calculate Exact height dont use draw_info.height
#         if i in color_positions:
#             color = color_positions[i]
            
#         pygame.draw.rect(
#             draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height)
#         )
#     if clear_bg:
#         pygame.display.update()
def draw_list(draw_info, color_positions={}, clear_bg=False, is_uniform=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (SIDE_PADDING//2, TOP_PADDING, (draw_info.width-SIDE_PADDING), (draw_info.height-TOP_PADDING))
        pygame.draw.rect(draw_info.window, BACKGROUND_COLOR, clear_rect)

    if not is_uniform:
        # Set the font and the width limit for the list area
        font = pygame.font.SysFont('verdana', 15)
        width_limit = draw_info.width - 2 * SIDE_PADDING

        # Render each element of the list, starting a new line if the width limit is exceeded
        total_width = 0
        line_height = 0
        lines = []
        elements = []
        for i, val in enumerate(lst):
            text = font.render(str(val), 1, (0,0,0))
            if total_width + text.get_width() > width_limit:  # Start a new line
                lines.append(elements)
                elements = []
                total_width = 0
                line_height += text.get_height()
            elements.append((text, total_width, line_height))
            total_width += text.get_width()
            if i < len(lst) - 1:  # Don't render comma after the last element
                comma = font.render(',', 1, (0,0,0))
                elements.append((comma, total_width, line_height))
                total_width += comma.get_width()
        lines.append(elements)  # Add the last line

        # Center align each line separately
        for elements in lines:
            total_width = sum(text.get_width() for text, _, _ in elements)
            start_x = (draw_info.width - total_width) // 2
            for text, x, y in elements:
                draw_info.window.blit(text, (start_x + x, TOP_PADDING//2 + y))

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * (draw_info.bar_height)
        color = GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(
            draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height)
        )
    if clear_bg:
        pygame.display.update()

def generate_list(n, min_val, max_val,uniform=False):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val) if not uniform else random.uniform(0, 1)
        lst.append(val)
    return lst


def main(window):
    theme_type = 'Default'
    w, ht = pygame.display.get_surface().get_size()
    width = ht #Sort Display
    delta = w - width
    
    n = 50
    min_val = 0
    max_val = 100
    
    top_start = ht/30
    but_height = ht//15
    but_width = delta//2.2
    horizontal_gap_factor = but_width-but_height  
    vertical_gap_factor = but_height
    
    back_button = {}
    back_icon = pygame.image.load('assets/back_icon.png')
    create_button(back_button,back_icon, ((1020), (900//40)/2.5))
    algorithms = [
        button(width+delta//4 +30, top_start + vertical_gap_factor,
               but_width-but_height-20, but_height, 'Bubble Sort'),
        
        button(width+delta//4+ 30, top_start + (2*vertical_gap_factor),
               but_width-but_height-20, but_height, 'Selection Sort'),

        button(width+delta//4+ 30, top_start + (3*vertical_gap_factor),
               but_width-but_height-20, but_height, 'Insertion Sort'),
        
        button(width+delta//4+ 30, top_start + (4*vertical_gap_factor), 
               but_width-but_height-20, but_height, 'Tim Sort'),
        
        button((width+delta//4 + horizontal_gap_factor+12),
               top_start + vertical_gap_factor, but_width-but_height-20, but_height, "Merge Sort"),

        button((width+delta//4 + horizontal_gap_factor+12), top_start +
                (2*vertical_gap_factor), but_width-but_height-20, but_height, 'Quick Sort'),

        button((width+delta//4 + horizontal_gap_factor+12), top_start +
               (3*vertical_gap_factor), but_width-but_height-20, but_height, 'Radix Sort'),
   
        button((width+delta//4 + horizontal_gap_factor+12), top_start +
               (4*vertical_gap_factor), but_width-but_height-20, but_height, 'Bucket Sort'),
    ]
    options_fst_hf_wdt = (but_width-but_height)//2
    options_sec_hf_st = (width+delta//4 + 30 + horizontal_gap_factor-20)
    options_sec_hf_wdt = (but_width-but_height-20)//3 + 1
    options_start_top = top_start + (8*vertical_gap_factor) + 2
    options = [
        button(width+delta//4 + 30, options_start_top, options_fst_hf_wdt, but_height, "Generate"),
        button(width+delta//4 + 30 +options_fst_hf_wdt,  options_start_top,   options_fst_hf_wdt, but_height, "Slow"),
        button(options_sec_hf_st, options_start_top, options_sec_hf_wdt, but_height, "Fast"),
        button(options_sec_hf_st + options_sec_hf_wdt, options_start_top, options_sec_hf_wdt, but_height, "-"),
        button(options_sec_hf_st + options_sec_hf_wdt*2, options_start_top, options_sec_hf_wdt, but_height, "+"),
        button(width+delta//4 + 30, options_start_top + but_height+1, (but_width-but_height-20), but_height, "Reverse Order"),
        button(options_sec_hf_st, options_start_top + but_height+1, (but_width-but_height-19), but_height, "Uniform Array"),
    ]
    #* Result Screen
    sc_y_start = ht-240
    sc_x_start = width+delta//4 + 28
    sc_height = 250
    sc_width = (but_width-but_height-17)*2
    lst = generate_list(n, min_val, max_val,uniform=False)
    
    draw_info = DrawInformation(width + 150, width, lst, window)
    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None
    
    output = screen(sc_x_start, sc_y_start, sc_width, sc_height, "Choose an Algorithm")
    output.set_label1(f"Range: {n}")
    output.set_text1(f"{sorting_algorithm_name}")
    output.set_text4(Bubble_Sort)

    run = True
    clock = pygame.time.Clock()
    low = 0
    high = len(draw_info.lst)
    speed = 60
    is_uniform = False
    while run:
        clock.tick(speed)
        if sorting:
            try:
                next(sorting_algorithm_generator)
                
            except StopIteration:
                sorting = False
        if is_uniform:  
            draw(draw_info,algorithms,back_button,options,output,theme_type,is_uniform=True)        
        else: 
            draw(draw_info,algorithms,back_button,options,output,theme_type)        
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_r:
                    lst = generate_list(n, min_val, max_val)
                    is_uniform = False
                    draw_info.set_list(lst)
                    sorting = False
                
                elif event.key == pygame.K_o and not sorting:
                    ascending = not ascending
                
                elif event.key == pygame.K_SPACE and not sorting:
                    if sorting_algorithm_generator == None:
                        sorting_algorithm = bubble_sort
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info,draw_info.lst,low,high,ascending)

            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                output.set_error_message = ""
                if is_hover(back_button,pos):
                    print("Sending to Main Menu")
                    main_app.main_menu()
                    
                elif algorithms[0].is_hover(pos):
                    algorithms[0].toggle_color()
                    sorting_algorithm = bubble_sort
                    sorting_algorithm_name = 'Bubble Sort'
                    output.set_text1(sorting_algorithm_name)
                    output.set_text4(Bubble_Sort)
                    output.draw(draw_info.window, BLACK)
                    
                elif algorithms[1].is_hover(pos):
                    algorithms[1].toggle_color()
                    sorting_algorithm = selection_sort
                    sorting_algorithm_name = 'Selection Sort'
                    output.set_text1(sorting_algorithm_name)
                    output.set_text4(Selection_Sort)
                    output.draw(draw_info.window, BLACK)
                
                elif algorithms[2].is_hover(pos):
                    algorithms[2].toggle_color()
                    sorting_algorithm = insertion_sort
                    sorting_algorithm_name = 'Insertion Sort'
                    output.set_text1(sorting_algorithm_name)
                    output.set_text4(Insertion_Sort)
                    output.draw(draw_info.window, BLACK)
                    
                elif algorithms[3].is_hover(pos):
                    algorithms[3].toggle_color()
                    sorting_algorithm = tim_sort
                    sorting_algorithm_name = 'Tim Sort'
                    output.set_text1(sorting_algorithm_name)
                    output.set_text4(Tim_Sort)
                    output.draw(draw_info.window, BLACK)

                elif algorithms[4].is_hover(pos):
                    algorithms[4].toggle_color()
                    output.draw(draw_info.window, BLACK)
                    sorting_algorithm = merge_sort
                    sorting_algorithm_name = 'Merge Sort'
                    output.set_text1(sorting_algorithm_name)
                    output.set_text4(Merge_Sort)
                    output.draw(draw_info.window, BLACK)
                    
                elif algorithms[5].is_hover(pos):
                    algorithms[5].toggle_color()
                    sorting_algorithm = quick_sort
                    sorting_algorithm_name = 'Quick Sort'
                    output.set_text1(sorting_algorithm_name)
                    output.set_text4(Quick_Sort)
                    output.draw(draw_info.window, BLACK)
                    
                elif algorithms[6].is_hover(pos):
                    algorithms[6].toggle_color()
                    sorting_algorithm = radix_sort
                    sorting_algorithm_name = 'Radix Sort'
                    output.set_text1(sorting_algorithm_name)
                    output.set_text4(Radix_Sort)
                    output.draw(draw_info.window, BLACK)

                elif algorithms[7].is_hover(pos):
                    algorithms[7].toggle_color()
                    if is_uniform:
                        sorting_algorithm = bucket_sort
                        sorting_algorithm_name = 'Bucket Sort'
                        output.set_text1(sorting_algorithm_name)
                        output.set_text4(Bucket_Sort)
                        output.draw(draw_info.window, BLACK)
                    else:
                        sorting_algorithm_name = 'Bucket Sort'
                        output.set_text1(sorting_algorithm_name)
                        output.set_error_message("Uniform Array Required")
                        output.draw(draw_info.window, BLACK)
                                        
                elif options[0].is_hover(pos):
                    options[0].toggle_color()
                    lst = generate_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                                     
                elif options[1].is_hover(pos):
                    options[1].toggle_color()
                    if speed>=20:
                        speed-=10
                        
                
                elif options[2].is_hover(pos):
                    options[2].toggle_color()
                    if speed<=90:
                        speed+=10
                        
                
                elif options[3].is_hover(pos):
                    options[3].toggle_color()
                    if n>=20:
                        n-=10
                        lst = generate_list(n, min_val, max_val)
                        draw_info.set_list(lst)
                        sorting = False
                        high = len(draw_info.lst)
                    else:
                        continue

                elif options[4].is_hover(pos):
                    options[4].toggle_color()
                    if n<100:
                        n+=10
                        lst = generate_list(n, min_val, max_val)
                        draw_info.set_list(lst)
                        sorting = False
                        high = len(draw_info.lst)
                    else:
                        continue
                        
                
                elif options[5].is_hover(pos):
                    options[5].toggle_color()
                    ascending = not ascending
                
                elif options[6].is_hover(pos):
                    options[6].toggle_color()
                    lst = generate_list(n, min_val, max_val,uniform=True)
                    is_uniform = True                    
                    draw_info.set_list(lst)
                    sorting = False
                    low = 0
                    high = len(draw_info.lst)
                                     
                
                

    pygame.quit()


if __name__ == "__main__":
    width = 800
    win = pygame.display.set_mode((width+700, width))
    main(win)
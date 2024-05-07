from grid import WIDTH
import pygame
import sys
import maze_main
import sort_main
pygame.init()
# Constants
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BTN_1 = (250, 146, 137)
ACT_BTN_1 = (231, 116, 123)
BTN_2 = (155, 141, 203)
ACT_BTN_2 = (67, 59, 106)
FONT_SIZE = 48
BUTTON_WIDTH = 500
BUTTON_HEIGHT = 300
BOTTOM_SECTION_HEIGHT = 300

# Information to display
info = """
Algorithm Visualizer

Python program that showcases various sorting and pathfinding algorithms.

Sorting Algorithms:\n
Bubble Sort
Selection Sort
Insertion Sort
Merge Sort
Quick Sort
Tim Sort
Bucket Sort
Radix Sort
Count Sort

Pathfinding Algorithms:\n
BFS Search
Bi-BFS Search
DFS Search
Dijkstra Search
A* Search
IDA* Search
Bi-A* Search
Bellman-Ford Search
"""

# Split the information into lines
lines = info.split('\n')

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Start Menu")


# Function to create text objects
def info_text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# Function to display text on screen
def display_info_text(text, x, y, color, font_size=FONT_SIZE):
    large_text = pygame.font.Font(None, font_size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.topleft = (x, y)
    window.blit(text_surf, text_rect)


# Function to create text objects
def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

# Function to display text on screen
def display_text(text, x, y, color, font_size=FONT_SIZE):
    large_text = pygame.font.Font(None, font_size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    window.blit(text_surf, text_rect)

# Function to create buttons
def button(msg, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(window, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(window, inactive_color, (x, y, width, height))

    display_text(msg, x + width // 2, y + height // 2, WHITE)

# Function to start the pathfinding visualizer
def start_pathfinding_visualizer():
    print("Starting Pathfinding Visualizer")
    width = WIDTH
    win = pygame.display.set_mode((WIDTH+700, WIDTH))
    maze_main.main(win,width)

# Function to start the sorting visualizer
def start_sorting_visualizer():
    print("Starting Sorting Visualizer")
    width = WIDTH
    pygame.display.set_mode((width+700, width))
    sort_main.main(pygame.display.set_mode((800+700, 800)))

# Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()


# Main menu loop
def main_menu():
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Start Menu")
    # Load the background image
    background = pygame.image.load('assets/bg_default.png')

    # Scale the image
    background = pygame.transform.scale(background, (WINDOW_WIDTH-500, WINDOW_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the background image
        window.blit(background, (0, 0))
        in_path_search = False
        # Display the information
        for i, line in enumerate(lines):
            if line.endswith("Visualizer"):
                display_info_text(line, 10, i * FONT_SIZE/2, BLACK, font_size=50)
            elif not in_path_search:
                display_info_text(line, 10, i * FONT_SIZE/2, BLACK,font_size=30)
            elif in_path_search:
                display_info_text(line, 10, i * FONT_SIZE/2.1, BLACK,font_size=30)
            elif line.endswith("Sorting Algorithms:"):
                display_info_text(line, 10, i * FONT_SIZE//2.1, BLACK, font_size=40)
            elif line.endswith("Pathfinding Algorithms:"):
                in_path_search = True
                display_info_text(line, 10, i * FONT_SIZE//2.1, BLACK, font_size=40)
                                

        # Create buttons
        button("Pathfinding", 2*BUTTON_WIDTH, WINDOW_HEIGHT - WINDOW_HEIGHT, BUTTON_WIDTH, WINDOW_HEIGHT//2,
               BTN_1, ACT_BTN_1, start_pathfinding_visualizer)
        
        button("Sorting", 2*BUTTON_WIDTH, WINDOW_HEIGHT - WINDOW_HEIGHT//2, BUTTON_WIDTH, WINDOW_HEIGHT//2,
               BTN_2, ACT_BTN_2, start_sorting_visualizer)
        
        pygame.display.update()

# Run the main menu loop
if __name__=="__main__":
    main_menu()
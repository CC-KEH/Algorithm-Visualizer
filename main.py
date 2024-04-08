from grid import WIDTH
import pygame
import sys
import maze_main
import sort_main
from themes.colors import DARK_GREEN, DARK_TEAL, TEAL

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
INACTIVE_BUTTON_COLOR = TEAL
ACTIVE_BUTTON_COLOR = DARK_TEAL
FONT_SIZE = 48
BUTTON_WIDTH = 500
BUTTON_HEIGHT = 300
BOTTOM_SECTION_HEIGHT = 300

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Start Menu")

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
    sort_main.main(pygame.display.set_mode((800+700, 800)))

# Function to quit the game
def quit_game():
    pygame.quit()
    sys.exit()

# Main menu loop
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill(WHITE)  # Clear screen with white color

        # Create buttons
        button("Pathfinding", 2*BUTTON_WIDTH, WINDOW_HEIGHT - WINDOW_HEIGHT, BUTTON_WIDTH, WINDOW_HEIGHT//2,
               INACTIVE_BUTTON_COLOR, ACTIVE_BUTTON_COLOR, start_pathfinding_visualizer)
        
        button("Sorting", 2*BUTTON_WIDTH, WINDOW_HEIGHT - WINDOW_HEIGHT//2, BUTTON_WIDTH, WINDOW_HEIGHT//2,
               INACTIVE_BUTTON_COLOR, ACTIVE_BUTTON_COLOR, start_sorting_visualizer)
        
        pygame.display.update()

# Run the main menu loop
main_menu()

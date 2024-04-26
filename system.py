from turtle import back, color
import pygame
from themes.colors import *
from themes.animations import *
from grid import *
from themes.themes import *
class button():
    def __init__(self, x, y,width,height, text='',theme_type='Default'):
        self.color = themes[theme_type]["inactive_button_color"]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,theme_type='Default',outline=True):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.color = themes[theme_type]["active_button_color"]
        else:
            self.color = themes[theme_type]["inactive_button_color"]
        
        if outline:
            pygame.draw.rect(win, themes[theme_type]["button_outline_color"], (self.x-2,self.y-2,self.width+4,self.height+4),0)
        
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('verdana', 20)
            text = font.render(self.text, 1, (255,255,255))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_hover(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x-self.height//2 and pos[0] < self.x + self.width+self.height//2:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
    
    def toggle_color(self):
        if(self.color == themes[theme_type]["inactive_button_color"]):
            self.color = themes[theme_type]["active_button_color"]
        else:
            self.color = themes[theme_type]["inactive_button_color"]


class screen():
    def __init__(self, x,y,width,height,text='',color=SCREEN_COLOR):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label1 = ""
        self.text1 = text
        self.text2 = ""
        self.text3 = ""
        self.text4 = ""
        self.error_message = ""
        
    def set_label1(self, label):
        self.label1 = label
    
    def set_text1(self, text):
        self.text1 = text
        
    def set_text2(self, text):
        self.text2 = text
        
    def set_text3(self, text):
        self.text3 = text
        
    def set_text4(self, text):
        self.text4 = text
    
    def set_error_message(self, text):
        self.error_message = text
        
    def get_text1(self):
        return self.text1

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        
        if self.label1 != '':
            font = pygame.font.SysFont('verdana', 20)
            label = font.render(self.label1, 1, (0,0,0))
            win.blit(label, (self.x + 10, self.y + 10))
        
        if self.text1 != '':
            font = pygame.font.SysFont('verdana', 30)
            text = font.render(self.text1, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2) - 80))
        
        if self.text2 != '':
            font = pygame.font.SysFont('verdana', 30)
            text = font.render(self.text2, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        
        if self.error_message!='':
            font = pygame.font.SysFont('verdana', 30)
            error_message = font.render(self.error_message, 1, RED)
            win.blit(error_message, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        
        
        if self.text3 != '':
            font = pygame.font.SysFont('verdana', 30)
            text = font.render(self.text3, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2) - 50 , 50 + self.y + (self.height/2 - text.get_height()/2)))
        
        if self.text4 != '':
            font = pygame.font.SysFont('verdana', 15)
            lines = self.text4.split('\n')
            for i, line in enumerate(lines):
                text = font.render(line, 1, (0,0,0))
                win.blit(text, (self.x+10, self.y + (self.height/2 - text.get_height()/2) - 45+ i*font.get_height()))
    
    def is_hover(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


def create_button(button, image, position):
    button["image"] = image
    button["rect"] = image.get_rect(topleft=position)
 
def is_hover(button, pos):
    if button["rect"].collidepoint(pos):
        return True
    else:
        return False

def draw(win, grid, rows, width, algorithms, mazes,back_button, options, output,theme_type='Default', menu = True):
    win.fill(themes[theme_type]["menu_bg_color"])
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    if menu:
        n = 17
        delta = 700
        ht = 900
        width = ht
        w = 1600
        font = pygame.font.SysFont('verdana', 35)
        text = font.render("Path Finding Algorithms", 1, WHITE)
        top = 0
        end = ht//40
        win.blit(back_button["image"], back_button["rect"])
        win.blit(text, ((width+delta//10), (end-top)/2.5))
        for algorithm in algorithms:
            algorithm.draw(win)
        
        text = font.render("Generate Maze", 1, WHITE)
        but_height = ht//15
        top += (4.3*but_height)
        end += (1.9*(3*but_height//2)) + but_height + ht//12
        win.blit(text, (width+delta//5.5, ((end-top)/2) + top))
        for maze in mazes:
            maze.draw(win)
            
        end += (1.3*(3*but_height//2)) + ht//6
        top += (1.7*but_height//2)
        
        text = font.render("Grid Settings", 1, WHITE)
        win.blit(text, (width+delta//5, ((end-top)/2) + top))
        for option in options:
            option.draw(win)
        output.draw(win)
    pygame.display.update()
    

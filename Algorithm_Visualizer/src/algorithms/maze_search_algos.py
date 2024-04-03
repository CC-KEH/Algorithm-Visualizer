import pygame
import sys
from queue import PriorityQueue
from grid import *
from themes.colors import *
from themes.animations import *
from utils import *

def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current=came_from[current]
        current.make_path()
        draw()
        
def maze_bfs(draw, grid, start, end, is_bidirectional=False):
    pass


def maze_dfs(draw, grid, start, end, is_bidirectional=False):
    pass


def maze_dijkstra(draw, grid, start, end, is_bidirectional=False):
    pass


def maze_astar(draw, grid, start, end, is_bidirectional=False):
    """_summary_

    Args:
        draw (class): lamda Draw function
        grid (class): Grid
        start (class): Start Node
        end (class): End Node
        is_bidirectional (bool, optional): Whether to search from both directions. Defaults to False.

    Returns:
        _type_: _description_
    """
    
    count=0 # This keeps the track when a node is added to set.
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    start_pos = start.get_pos()
    end_pos = end.get_pos()
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h_score(start_pos,end_pos) + g_score[end]

    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # Get Node
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current==end:
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = h_score(neighbor.get_pos(),end_pos)  + g_score[neighbor]
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.put(neighbor)
                    neighbor.make_open()
        draw()
        
        if current!=start:
            current.make_closed()
        
    return False


def maze_bellman_ford(draw, grid, start, end, is_bidirectional=False):
    pass


def maze_floyd_warshall(draw, grid, start, end, is_bidirectional=False):
    pass


def maze_jump_point(draw, grid, start, end, is_bidirectional=False):
    pass
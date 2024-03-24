import pygame  # type: ignore
import os
import sys

from themes.colors import *
from themes.themes import themes
from algorithms.maze_search_algos import *
from algorithms.maze_gen_algos import *

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
theme_type = "Default"


class Cell:
    def __init__(self, row, col, size, total_rows):
        self.row = row * size
        self.col = col * size
        self.color = WHITE
        self.y = col * size
        self.x = row * size
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.size, self.size), border_radius=3
        )

    def update_neighbors(self, grid):

        # Up
        if self.row > 1 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Down
        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.col].is_barrier()
        ):
            self.neighbors.append(grid[self.row + 1][self.col])

        # Left
        if self.col > 1 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

        # Right
        if (
            self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_barrier()
        ):
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other) -> bool:
        return False

    def get_pos(self):
        return (self.row, self.col)

    def is_closed(self) -> bool:
        return self.color == themes[theme_type]["closed_color"]

    def is_open(self) -> bool:
        return self.color == themes[theme_type]["open_color"]

    def is_barrier(self) -> bool:
        return self.color == themes[theme_type]["barrier_color"]

    def is_start(self) -> bool:
        return self.color == themes[theme_type]["start_color"]

    def is_end(self) -> bool:
        return self.color == themes[theme_type]["end_color"]

    def reset(self):
        self.color = themes[theme_type]["plane_color"]

    def make_closed(self):
        self.color = themes[theme_type]["closed_color"]

    def make_open(self):
        self.color = themes[theme_type]["open_color"]

    def make_barrier(self):
        self.color = themes[theme_type]["barrier_color"]

    def make_start(self):
        self.color = themes[theme_type]["start_color"]

    def make_end(self):
        self.color = themes[theme_type]["end_color"]

    def make_path(self):
        self.color = themes[theme_type]["path_color"]


def h(p1, p2):
    """Calculate heuristic using Manhattan distance

    Args:
        p1 (x,y): coordinates of point1
        p2 (x,y): coordinates of point2
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)


def make_grid(rows, width):
    """Makes the Grid

    Args:
        rows (int): _description_
        width (int): _description_
    """
    grid = []
    cell_size = width // rows
    for r in range(rows):
        grid.append([])
        for c in range(rows):
            cell = Cell(r, c, cell_size, rows)
            grid[r].append(cell)

    return grid


def draw_grid_lines(win, rows, width):
    """Makes the Grid Lines

    Args:
        win (): Surface
        rows (int): _description_
        width (int): _description_
    """
    cell_size = width // rows
    for r in range(rows):
        pygame.draw.line(win, GREY, (0, r * cell_size), (width, r * cell_size))
        for c in range(rows):
            pygame.draw.line(win, GREY, (c * cell_size, 0), (c * cell_size, width))


def draw(win, grid, rows, width):
    """Responsible for displaying Grid

    Args:
        win (_type_): Surface to draw on
        grid (list): 2D list of cells
        rows (_type_): rows
        width (_type_): window size
    """
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)

    # TODO Instead of drawing grid lines render the cells on a different color background.
    # So that border radius doesnt look bad
    draw_grid_lines(win, rows, width)

    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """Returns the coordinate of cell clicked on

    Args:
        pos (y,x): coordinate of mouse click, Why (y,x) ? => y is row x is col
        rows (int): rows
        width (int): window size

    Returns:
        (row,col) : coordinate of cell clicked on
    """
    cell_size = width // rows
    y, x = pos
    row = y // cell_size
    col = x // cell_size
    return (row, col)


def search_algorithm(draw, grid, start, end, algo):
    search_algos = {
        "Dijkstra": maze_dijkstra,
        "Breadth First Search": maze_bfs,
        "Depth First Search": maze_dfs,
        "A*": maze_astar,
        "Bidirectional BFS": maze_bfs,
        "Bidirectional DFS": maze_dfs,
        "Bidirectional A*": maze_astar,
        "Bellman-Ford": maze_bellman_ford,
        "Floyd-Warshall": maze_floyd_warshall,
        "Jump Point Search": maze_jump_point,
    }


def generate_maze(draw, grid, algo):
    gen_algos = {
        "Recursive Backtracker": recursive_backtracker,
        "Prim's Algorithm": prims_algorithm,
        "Kruskal's Algorithm": kruskals_algorithm,
        "Binary Tree": binary_tree,
        "Sidewinder": sidewinder,
        "Recursive Division": recursive_division,
        "Eller's Algorithm": ellers_algorithm,
    }


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    algo = "Dijkstra"
    while run:
        draw(WIN, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # No interruption from user
            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # Left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                if not start and cell != end:
                    start = cell
                    start.make_start()

                elif not end and cell != start:
                    end = cell
                    end.make_end()

                elif cell != end and cell != start:
                    cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    search_algorithm(
                        lambda: draw(win, grid, ROWS, width), grid, start, end, algo
                    )
    pygame.quit()


main(WIN, WIDTH)

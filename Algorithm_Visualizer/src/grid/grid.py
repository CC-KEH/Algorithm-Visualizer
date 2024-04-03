import pygame  # type: ignore
from src.themes.colors import *
from src.themes.themes import themes
from src.algorithms.maze_search_algos import *


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
theme_type = "Default"


class Cell:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.color = WHITE
        self.target_color = WHITE
        self.y = col * size
        self.x = row * size
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows
        self.animation_radius = 0
        self.animating = False
        self.animation_speed = 2

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.size, self.size), border_radius=3
        )

    def update_neighbors(self, grid):
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col]) 
        
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

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
        pygame.draw.line(win, LIGHT_GREY, (0, r * cell_size), (width, r * cell_size))
        for c in range(rows):
            pygame.draw.line(win, LIGHT_GREY, (c * cell_size, 0), (c * cell_size, width))


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
        # "Dijkstra": maze_dijkstra,
        # "Breadth First Search": maze_bfs,
        # "Depth First Search": maze_dfs,
        "A*": maze_astar,
        # "Bidirectional BFS": maze_bfs,
        # "Bidirectional DFS": maze_dfs,
        # "Bidirectional A*": maze_astar,
        # "Bellman-Ford": maze_bellman_ford,
        # "Floyd-Warshall": maze_floyd_warshall,
        # "Jump Point Search": maze_jump_point,
    }
    search_algos[algo](draw,grid,start,end)


# def generate_maze(draw, grid, algo):
#     gen_algos = {
#         "Recursive Backtracker": recursive_backtracker,
#         "Prim's Algorithm": prims_algorithm,
#         "Kruskal's Algorithm": kruskals_algorithm,
#         "Binary Tree": binary_tree,
#         "Sidewinder": sidewinder,
#         "Recursive Division": recursive_division,
#         "Eller's Algorithm": ellers_algorithm,
#     }


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    algo = "A*"
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
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    # search_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, algo)
                    maze_astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)

import pygame
from grid import *
from themes.colors import *
from themes.animations import *
from system import *
from maze_search_algos import *
from maze_gen_algos import *


def main(win, width):
    theme_type = "Default"
    ROWS = 50
    w, ht = pygame.display.get_surface().get_size()
    width = ht
    grid = make_grid(ROWS, width)
    delta = w - width

    top_start = ht/13
    but_height = ht//15
    but_width = delta//4
    gap_factor = 5  # * Determines the gap between the buttons
    # * Determines the coordinate from where the button start in x-axis.
    start_factor = 10

    algorithms = [
        button(width+delta//start_factor, top_start,
               but_width-but_height, but_height, 'BFS'),

        button(width+delta//start_factor, top_start + (6*but_height//2),
               but_width-but_height, but_height, 'DFS'),

        button(width+delta//start_factor, top_start + (3*but_height//2),
               but_width-but_height, but_height, 'Bi-BFS'),

        button(width+delta//start_factor + (gap_factor*but_width//4),
               top_start, but_width-but_height, but_height, "A*"),

        button(width+delta//start_factor + (gap_factor*but_width//4), top_start +
               (3*but_height//2), but_width-but_height, but_height, 'IDA*'),

        button(width+delta//start_factor + (gap_factor*but_width//4), top_start +
               (6*but_height//2), but_width-but_height, but_height, 'Bi-A*'),

        button(width+delta//start_factor + ((gap_factor * 2)*but_width//4),
               top_start, but_width-but_height, but_height, 'Dijkstra'),
    ]

    top_start = top_start + (1.9*(3*but_height//2)) + but_height + ht//10
    but_height = ht//15
    but_width = delta//4
    mazes = [
        button(width+delta//start_factor, top_start,
               but_width-but_height, but_height, "DFS Maze"),

        button(width+delta//start_factor + (gap_factor*but_width//4),
               top_start, but_width-but_height, but_height, "Random"),

        button(width+delta//start_factor + ((gap_factor*2)*but_width//4),
               top_start, but_width-but_height, but_height, "Kruskal"),

        button(width+delta//start_factor + ((gap_factor*2)*but_width//4),
               top_start, but_width-but_height, but_height, "Randomized Prim's"),
    ]
    top_start = top_start + (1.3*(3*but_height//2)) + ht//10
    but_height = ht//15
    but_width = delta//10
    options = [
        button(width+delta//5, top_start-35, but_width -
               but_height+20, but_height, "Clear"),
        button(width+delta//5 + 40 + delta//5 + (4*(but_width+50)//3),
               top_start-35, 0, but_height, "-"),
        button(width+delta//5 + 50 + delta//5 + (4*(but_width+50)//3) +
               (4*(but_width-30)//3), top_start-35, 0, but_height, "+"),
    ]
    sc_start = ht-240
    sc_height = 230
    sc_width = delta-delta//4
    output = screen(width+delta//8, sc_start, sc_width,
                    sc_height, "Choose an Algorithm")
    output.set_label1(f"Rows: {ROWS}")
    output.set_text1("     1. Choose the starting node")
    output.set_text2("    2. Choose the ending node")
    output.set_text3("3. Choose the algorithm")

    start = None
    end = None

    run = True
    started = False
    visited = []
    weighted = []
    path = False
    while run:
        if len(visited):
            visit_animation(visited)

        if path:
            path_animation(path)

        draw(win, grid, ROWS, width, algorithms, mazes, options, output)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if row >= 0 and row < ROWS and col < ROWS and col >= 0:
                    node = grid[row][col]
                    if node in visited:
                        visited.remove(node)
                    if node in weighted:
                        weighted.remove(node)
                    if path:
                        if node in path:
                            path.remove(node)
                    if not start and node != end:
                        if node in visited:
                            visited.remove(node)
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()

                elif algorithms[0].is_hover(pos):
                    algorithms[0].toggle_color()
                    output.draw(win, (0, 0, 0))
                    if len(weighted):
                        for node in weighted:
                            node.mark_weight()
                    if start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                                if not node.is_neutral() and node != start and node != end and not node.is_barrier() and not node.is_weight():
                                    node.reset()
                        visited = []
                        path = []
                        output.set_text1("......")
                        output.set_text2("")
                        output.set_text3("")
                        output.draw(win, BLACK)
                        pygame.display.update()
                        visited, path = maze_bfs(lambda: draw(
                            win, grid, ROWS, width, algorithms, mazes, options, output), grid, start, end, output, win, width,theme_type)
                        if not path:
                            output.set_text1("Path not available")
                        algorithms[0].toggle_color()

                elif algorithms[1].is_hover(pos):
                    algorithms[1].toggle_color()
                    if len(weighted):
                        for node in weighted:
                            node.mark_weight()
                    if start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                                if not node.is_neutral() and node != start and node != end and not node.is_barrier() and not node.is_weight():
                                    node.reset()
                        visited = []
                        path = []
                        output.set_text1("......")
                        output.set_text2("")
                        output.set_text3("")
                        output.draw(win, BLACK)
                        pygame.display.update()
                        visited, path = maze_dfs(lambda: draw(
                            win, grid, ROWS, width, algorithms, mazes, options, output), grid, start, end, output, win, width,theme_type)
                        if not path:
                            output.set_text1("Path not available")
                        algorithms[1].toggle_color()

                elif algorithms[2].is_hover(pos):
                    algorithms[2].toggle_color()
                    if len(weighted):
                        for node in weighted:
                            node.mark_weight()
                    if start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                                if not node.is_neutral() and node != start and node != end and not node.is_barrier() and not node.is_weight():
                                    node.reset()
                        visited = []
                        path = []
                        output.set_text1("......")
                        output.set_text2("")
                        output.set_text3("")
                        output.draw(win, BLACK)
                        pygame.display.update()
                        visited, path = maze_bi_bfs(lambda: draw(
                            win, grid, ROWS, width, algorithms, mazes, options, output), grid, start, end, output, win, width,theme_type)
                        if not path:
                            output.set_text1("Path not available")
                        algorithms[2].toggle_color()

                elif algorithms[3].is_hover(pos):
                    algorithms[3].toggle_color()
                    if len(weighted):
                        for node in weighted:
                            node.mark_weight()
                    if start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                                if not node.is_neutral() and node != start and node != end and not node.is_barrier() and not node.is_weight():
                                    node.reset()
                        visited = []
                        path = []
                        output.set_text1("......")
                        output.set_text2("")
                        output.set_text3("")
                        output.draw(win, BLACK)
                        pygame.display.update()
                        visited, path = maze_astar(lambda: draw(
                            win, grid, ROWS, width, algorithms, mazes, options, output), grid, start, end, output, win, width,theme_type)
                        if not path:
                            output.set_text1("Path not available")
                        algorithms[3].toggle_color()

                elif algorithms[4].is_hover(pos):
                    algorithms[4].toggle_color()
                    if len(weighted):
                        for node in weighted:
                            node.mark_weight()
                    if start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                                if not node.is_neutral() and node != start and node != end and not node.is_barrier() and not node.is_weight():
                                    node.reset()
                        visited = []
                        path = []
                        output.set_text1("......")
                        output.set_text2("")
                        output.set_text3("")
                        output.draw(win, BLACK)
                        pygame.display.update()
                        visited, path = maze_idastar(lambda: draw(win, grid, ROWS, width, algorithms, mazes, options, output),
                                                 win, width, output, grid, start, end, theme_type, h_score(start.get_pos(), end.get_pos()))
                        if not path:
                            output.set_text1("Path not available")
                        algorithms[4].toggle_color()

                elif algorithms[5].is_hover(pos):
                    algorithms[5].toggle_color()
                    if len(weighted):
                        for node in weighted:
                            node.mark_weight()
                    if start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                                if not node.is_neutral() and node != start and node != end and not node.is_barrier() and not node.is_weight():
                                    node.reset()
                        visited = []
                        path = []
                        output.set_text1("......")
                        output.set_text2("")
                        output.set_text3("")
                        output.draw(win, BLACK)
                        pygame.display.update()
                        visited, path = maze_bi_bfs(lambda: draw(
                            win, grid, ROWS, width, algorithms, mazes, options, output), grid, start, end, output, win, width,theme_type)
                        if not path:
                            output.set_text1("Path not available")
                        algorithms[5].toggle_color()

                elif algorithms[6].is_hover(pos):
                    algorithms[6].toggle_color()
                    if len(weighted):
                        for node in weighted:
                            node.mark_weight()
                    if start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)
                                if not node.is_neutral() and node != start and node != end and not node.is_barrier() and not node.is_weight():
                                    node.reset()
                        visited = []
                        path = []
                        output.set_text1("......")
                        output.set_text2("")
                        output.set_text3("")
                        output.draw(win, BLACK)
                        pygame.display.update()
                        visited, path = maze_dijkstra(lambda: draw(
                            win, grid, ROWS, width, algorithms, mazes, options, output), grid, start, end, output, win, width,theme_type)
                        if not path:
                            output.set_text1("Path not available")
                        algorithms[6].toggle_color()

                elif mazes[0].is_hover(pos):
                    output.set_text1("......")
                    output.set_text2("")
                    output.set_text3("")
                    output.draw(win, BLACK)
                    pygame.display.update()
                    start = None
                    end = None
                    visited = []
                    path = []
                    weighted = []
                    for row in grid:
                        for node in row:
                            if node.is_barrier() or node.is_start() or node.is_end():
                                node.reset()
                    maze_gen_dfs(lambda: draw(win, grid, ROWS, width, algorithms, mazes,
                             options, output), width, grid, start, end, 0, ROWS, 0, ROWS, win,theme_type)
                    output.set_text1("1. Pick starting node")
                    output.set_text2("2. Pick ending node")
                    output.set_text3("3. Choose an algorithm")

                elif mazes[1].is_hover(pos):
                    output.set_text1("......")
                    output.set_text2("")
                    output.set_text3("")
                    output.draw(win, BLACK)
                    pygame.display.update()
                    start = None
                    end = None
                    visited = []
                    path = []
                    weighted = []
                    for row in grid:
                        for node in row:
                            if node.is_barrier() or node.is_start() or node.is_end():
                                node.reset()
                    maze_gen_random(lambda: draw(win, grid, ROWS, width, algorithms, mazes,
                                options, output), width, grid, start, end, 0, ROWS, 0, ROWS, win,theme_type)
                    output.set_text1("1. Pick starting node")
                    output.set_text2("2. Pick ending node")
                    output.set_text3("3. Choose an algorithm")

                elif options[0].is_hover(pos):
                    output.set_text1("1. Pick starting node")
                    output.set_text2("2. Pick ending node")
                    output.set_text3("3. Choose an algorithm")
                    output.draw(win, BLACK)
                    pygame.display.update()
                    weighted = []
                    start = None
                    end = None
                    visited = []
                    path = []
                    weighted = []
                    for row in grid:
                        for node in row:
                            node.reset()

                elif options[1].is_hover(pos):
                    weighted = []
                    start = None
                    end = None
                    visited = []
                    path = []
                    weighted = []
                    for row in grid:
                        for node in row:
                            node.reset()
                    if ROWS > 5:
                        ROWS -= 1
                        grid = make_grid(ROWS, width)
                    output.set_label1(f"Number of rows: {ROWS}")

                elif options[2].is_hover(pos):
                    weighted = []
                    start = None
                    end = None
                    visited = []
                    path = []
                    weighted = []
                    for row in grid:
                        for node in row:
                            node.reset()
                    if ROWS < 100:
                        ROWS += 1
                        grid = make_grid(ROWS, width)
                    output.set_label1(f"Number of rows: {ROWS}")

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if row >= 0 and row < ROWS and col < ROWS and col >= 0:
                    node = grid[row][col]
                    if path:
                        if node in path:
                            path.remove(node)
                    if node in visited:
                        visited.remove(node)
                    if node in weighted:
                        weighted.remove(node)
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

    pygame.quit()


pygame.init()
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH+700, WIDTH))

pygame.display.set_caption("Path finding Visualizer")
main(WIN, WIDTH)

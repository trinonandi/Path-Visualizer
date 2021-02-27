import pygame
import grid
import algorithms

# initializing the constants
FPS = 60  # the pygame FPS
ROW = 35  # number of rows and cols of the grid as it is a square grid
WIDTH = 700  # screen width of the grid
WIN = pygame.display.set_mode((WIDTH, WIDTH))  # pygame windows


def main(win, width):
    clock = pygame.time.Clock()
    rows = ROW
    main_grid = grid.make_grid(rows, width)

    start = None  # holds the start node
    end = None  # holds the end node

    run = True
    while run:
        clock.tick(FPS)
        grid.draw(win, main_grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed(num_buttons=3)[0]:  # left click
                # num_buttons = 3 for 3 button mouse
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_node(pos, rows, width)
                node = main_grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_wall()

            elif pygame.mouse.get_pressed(num_buttons=3)[2]:  # right click
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_node(pos, rows, width)
                node = main_grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in main_grid:
                        for node in row:
                            node.update_neighbour(main_grid)

                    found = algorithms.a_star(lambda: grid.draw(win, main_grid, rows, width), main_grid, start, end)
                    if not found:
                        print("Not found")

                if event.key == pygame.K_r:     # reset the grid
                    start = None
                    end = None
                    main_grid = grid.make_grid(rows, width)


main(WIN, WIDTH)
pygame.quit()

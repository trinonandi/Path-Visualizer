import pygame
import grid
import algorithms
import sys
from pygame.locals import *

# initiating pygame
pygame.init()
pygame.display.set_caption('Visualizer')

# initializing the constants
FPS = 30  # the pygame FPS
ROW = 25  # number of rows and cols of the grid as it is a square grid
WIDTH = 700  # screen width of the grid
WIN = pygame.display.set_mode((WIDTH, WIDTH))  # pygame windows
FONT = pygame.font.SysFont('comicsans', 30)     # game font
MAIN_CLOCK = pygame.time.Clock()    # main clock

# menu colors
BUTTON_COLOR = (10, 4, 60)
BUTTON_HOVER_COLOR = (254, 152, 1)
MENU_BACK_COLOR = (174, 230, 230)


class Button:
    def __init__(self, x, y, width, height, text=" "):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = BUTTON_COLOR

    def set_text(self):
        text = FONT.render(self.text, True, (255, 255, 255))
        WIN.blit(text,
                 (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def draw_button(self):
        pygame.draw.rect(WIN, self.color, self.rectangle)
        self.set_text()


def draw_text(text, local_font, color, surface, x, y):
    text_obj = local_font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def main_menu():
    click = False
    while True:
        WIN.fill(MENU_BACK_COLOR)
        draw_text('Choose Algorithm', FONT, BUTTON_COLOR, WIN, 50, 50)

        mx, my = pygame.mouse.get_pos()

        button_dfs = Button(50, 100, 200, 50, "DFS")
        button_bfs = Button(50, 200, 200, 50, "BFS")
        button_astar = Button(50, 300, 200, 50, "A* Search")
        button_greedy = Button(50, 400, 200, 50, "Best First")

        if button_dfs.rectangle.collidepoint((mx, my)):
            button_dfs.color = BUTTON_HOVER_COLOR
            if click:
                game(WIN, WIDTH, algorithm=button_dfs.text)
        if button_bfs.rectangle.collidepoint((mx, my)):
            button_bfs.color = BUTTON_HOVER_COLOR
            if click:
                game(WIN, WIDTH, algorithm=button_bfs.text)
        if button_astar.rectangle.collidepoint((mx, my)):
            button_astar.color = BUTTON_HOVER_COLOR
            if click:
                game(WIN, WIDTH, algorithm=button_astar.text)
        if button_greedy.rectangle.collidepoint((mx, my)):
            button_greedy.color = BUTTON_HOVER_COLOR
            if click:
                game(WIN, WIDTH, algorithm=button_greedy.text)

        button_dfs.draw_button()
        button_bfs.draw_button()
        button_astar.draw_button()
        button_greedy.draw_button()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button
                    click = True

        pygame.display.update()
        MAIN_CLOCK.tick(FPS)


def game(win, width, algorithm):
    clock = pygame.time.Clock()
    rows = ROW
    main_grid = grid.make_grid(rows, width)

    start = None  # holds the start node
    end = None  # holds the end node

    algo_started = False

    run = True  # represents if the game loop is running or not
    while run:
        clock.tick(FPS)
        grid.draw(win, main_grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
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
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    run = False
                if (event.key == pygame.K_LEFT or event.key == pygame.K_UP) and not algo_started:
                    # decrease the grid size
                    if rows == 25:
                        rows -= 5
                    elif rows == 35:
                        rows -= 10
                    else:
                        continue
                    start = None
                    end = None
                    main_grid = grid.make_grid(rows, width)

                if (event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN) and not algo_started:
                    # increase the grid size
                    if rows == 25:
                        rows += 10
                    elif rows == 20:
                        rows += 5
                    else:
                        continue

                    start = None
                    end = None
                    main_grid = grid.make_grid(rows, width)

                if event.key == pygame.K_SPACE and start and end:
                    # start algorithm
                    algo_started = True
                    for row in main_grid:
                        for node in row:
                            node.update_neighbour(main_grid)

                    found = False
                    if algorithm == "A* Search":
                        found = algorithms.a_star(lambda: grid.draw(win, main_grid, rows, width), main_grid, start, end)
                    elif algorithm == "BFS":
                        found = algorithms.breadth_first_search(lambda: grid.draw(win, main_grid, rows, width), start,
                                                                end)
                    elif algorithm == "DFS":
                        found = algorithms.depth_first_search(lambda: grid.draw(win, main_grid, rows, width), start,
                                                              end)
                    elif algorithm == "Best First":
                        found = found = algorithms.greedy_best_first(lambda: grid.draw(win, main_grid, rows, width),
                                                                     main_grid, start, end)

                    if not found:
                        print("Not found")

                if event.key == pygame.K_r:  # reset the grid
                    algo_started = False
                    start = None
                    end = None
                    main_grid = grid.make_grid(rows, width)


main_menu()
pygame.quit()

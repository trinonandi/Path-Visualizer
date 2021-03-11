import pygame
import grid
import algorithms
import sys
from pygame.locals import *

# initiating pygame
pygame.init()
pygame.display.set_caption('Visualizer')
icon = pygame.image.load('assets/icon.ico')
pygame.display.set_icon(icon)

# initializing the constants
FPS = 30  # the pygame FPS
ROW = 25  # number of rows and cols of the grid as it is a square grid
WIDTH = 700  # screen width of the grid
WIN = pygame.display.set_mode((WIDTH, WIDTH))  # pygame windows
FONT = pygame.font.SysFont('comicsans', 30)  # game font
MAIN_CLOCK = pygame.time.Clock()  # main clock

# menu colors
BUTTON_COLOR = (10, 4, 60)
BUTTON_HOVER_COLOR = (254, 152, 1)
MENU_BACK_COLOR = (174, 230, 230)


class Button:
    """
    class to create buttons in the main menu
    -------------
    data members
    -------------
    x: the x coordinate
    y: the y coordinate
    width: width of the button
    height: height of the button
    text: the text to be written on the button
    rectangle: a pygame rectangle drawn from the x, y, width and height data members
    color: color of the button
    -------------
    methods
    -------------
    set_text: blit the text on the button
    draw_button: draws the button on the window
    """
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
    """
    draws text on the window
    :param text: the string to be written
    :param local_font: pygame font object
    :param color: text color
    :param surface: the window on which we will blit it
    :param x: x coordinate
    :param y: y coordinate
    :return: None
    """
    text_obj = local_font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def main_menu():
    """
    function to show the main menu and interact with button clicks
    it will be the only function called from this main.py
    :return: None
    """
    click = False   # checks any mouse click event
    message = None  # message in case path not found
    while True:
        WIN.fill(MENU_BACK_COLOR)
        draw_text('Choose Algorithm', FONT, BUTTON_COLOR, WIN, 50, 50)

        mx, my = pygame.mouse.get_pos()  # getting mouse coordinates

        # all the button objects
        button_dfs = Button(50, 100, 250, 50, "DFS")
        button_bfs = Button(50, 200, 250, 50, "BFS")
        button_astar = Button(50, 300, 250, 50, "A* Search")
        button_greedy = Button(50, 400, 250, 50, "Best First")
        button_bidirectional = Button(400, 100, 250, 50, "Bidirectional")
        button_astar_bi = Button(400, 200, 250, 50, "Bidirectional A*")
        button_greedy_bi = Button(400, 300, 250, 50, "Bidirectional Greedy")
        button_dijkstra = Button(400, 400, 250, 50, "Dijkstra")

        # all the button object's collision checking
        if button_dfs.rectangle.collidepoint((mx, my)):
            button_dfs.color = BUTTON_HOVER_COLOR
            if click:
                message = game(WIN, WIDTH, algorithm=button_dfs.text)
        if button_bfs.rectangle.collidepoint((mx, my)):
            button_bfs.color = BUTTON_HOVER_COLOR
            if click:
                message = game(WIN, WIDTH, algorithm=button_bfs.text)
        if button_astar.rectangle.collidepoint((mx, my)):
            button_astar.color = BUTTON_HOVER_COLOR
            if click:
                message = game(WIN, WIDTH, algorithm=button_astar.text)
        if button_greedy.rectangle.collidepoint((mx, my)):
            button_greedy.color = BUTTON_HOVER_COLOR
            if click:
                message = game(WIN, WIDTH, algorithm=button_greedy.text)

        if button_bidirectional.rectangle.collidepoint((mx, my)):
            button_bidirectional.color = BUTTON_HOVER_COLOR
            if click:
                message = game(WIN, WIDTH, algorithm=button_bidirectional.text)

        if button_astar_bi.rectangle.collidepoint((mx, my)):
            button_astar_bi.color = BUTTON_HOVER_COLOR
            if click:
                message = game(WIN, WIDTH, algorithm=button_astar_bi.text)

        if button_greedy_bi.rectangle.collidepoint((mx, my)):
            button_greedy_bi.color = BUTTON_HOVER_COLOR
            if click:
                message = game(WIN, WIDTH, algorithm=button_greedy_bi.text)
        if button_dijkstra.rectangle.collidepoint((mx, my)):
            button_dijkstra.color = BUTTON_HOVER_COLOR
            if click:
                message = game(WIN, WIDTH, algorithm=button_dijkstra.text)

        # drawing all the buttons on the window
        button_dfs.draw_button()
        button_bfs.draw_button()
        button_astar.draw_button()
        button_greedy.draw_button()
        button_bidirectional.draw_button()
        button_astar_bi.draw_button()
        button_greedy_bi.draw_button()
        button_dijkstra.draw_button()

        if message is not None:     # path not found
            text = "Search Result : " + message
            draw_text(text, FONT, BUTTON_COLOR, WIN, 50, 650)

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
    """
    function to start the game grid along with appropriate algorithm presets
    it will be called from inside the main_menu() function
    :param win: the pygame window
    :param width: the width of the screen
    :param algorithm: String. The algorithm name to be executed in the grid
    :return: String containing path not found message if path is not found else None
    """
    clock = pygame.time.Clock()
    rows = ROW
    main_grid = grid.make_grid(rows, width)     # the main grid in a list of list of Node objects format

    start = None  # holds the start node
    end = None  # holds the end node

    algo_started = False    # checks if the algorithm has started
    run = True  # represents if the game loop is running or not
    while run:
        clock.tick(FPS)
        grid.draw(win, main_grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:  # left click adds start, goal and wall respectively
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

            elif pygame.mouse.get_pressed(num_buttons=3)[2]:  # right click removes any of start, goal or wall
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

                    found = False   # holds the boolean return of the algorithm functions

                    if algorithm == "A* Search":
                        found = algorithms.a_star(lambda: grid.draw(win, main_grid, rows, width), main_grid, start, end)
                    elif algorithm == "BFS":
                        found = algorithms.breadth_first_search(lambda: grid.draw(win, main_grid, rows, width), start,
                                                                end)
                    elif algorithm == "DFS":
                        found = algorithms.depth_first_search(lambda: grid.draw(win, main_grid, rows, width), start,
                                                              end)
                    elif algorithm == "Best First":
                        found = algorithms.greedy_best_first(lambda: grid.draw(win, main_grid, rows, width),
                                                             main_grid, start, end)

                    elif algorithm == "Bidirectional":
                        found = algorithms.bidirectional_search(lambda: grid.draw(win, main_grid, rows, width),
                                                                main_grid, start, end)
                    elif algorithm == "Bidirectional A*":
                        found = algorithms.bidirectional_a_star_search(lambda: grid.draw(win, main_grid, rows, width),
                                                                       main_grid, start, end)
                    elif algorithm == "Bidirectional Greedy":
                        found = algorithms.bidirectional_greedy_search(lambda: grid.draw(win, main_grid, rows, width),
                                                                       main_grid, start, end)
                    elif algorithm == "Dijkstra":
                        found = algorithms.dijkstra(lambda: grid.draw(win, main_grid, rows, width),
                                                    main_grid, start, end)

                    if not found:   # path is not found
                        print("Not found")
                        message = "Path Not Found"
                        pygame.time.delay(1000)
                        return message

                if event.key == pygame.K_r:  # reset the grid
                    algo_started = False
                    start = None
                    end = None
                    main_grid = grid.make_grid(rows, width)


main_menu()
pygame.quit()

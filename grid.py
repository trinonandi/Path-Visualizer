import pygame

# initializing the constants
CLOSED_COLOR = (174, 230, 230)
OPEN_COLOR = (22, 165, 150)
WALL_COLOR = (128, 128, 128)
BASE_COLOR = (253, 207, 223)
START_COLOR = (254, 152, 1)
GOAL_COLOR = (204, 14, 116)
PATH_COLOR = (10, 4, 60)
WHITE = (255, 255, 255)


class Node:
    """
        This class is for each Node in the grid
        'row' and 'col' are the row and column number in the grid
        'width' and 'total_rows' are the window width and total row count in the grid
        'x' and 'y' are the (x,y) coordinates in the pygame window. It is calculated by row * width or col * width
        'neighbours[]' hold all the four neighbours of each node
        'color' holds the color of node

        we will recognize each node as a wall, start, end, open, closed, path etc by the colors
        so the get methods check the 'color' field and returns boolean
        and the make methods set the 'color' field to the respective color

        draw() method draws a rectangle along the x, y coordinates with ('width' x 'width') dimension
        and fills with the 'color'
    """

    def __init__(self, row, col, width, total_rows):

        self.row = row
        self.col = col

        self.width = width
        self.total_rows = total_rows

        self.x = row * width
        self.y = col * width

        self.neighbours = []
        self.color = BASE_COLOR

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == CLOSED_COLOR

    def is_open(self):
        return self.color == OPEN_COLOR

    def is_start(self):
        return self.color == START_COLOR

    def is_end(self):
        return self.color == GOAL_COLOR

    def is_wall(self):
        return self.color == WALL_COLOR

    def reset(self):
        self.color = BASE_COLOR

    def make_start(self):
        self.color = START_COLOR

    def make_end(self):
        self.color = GOAL_COLOR

    def make_wall(self):
        self.color = WALL_COLOR

    def make_open(self):
        self.color = OPEN_COLOR

    def make_closed(self):
        self.color = CLOSED_COLOR

    def make_path(self):
        self.color = PATH_COLOR

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbour(self, grid):

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  # bottom
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # top
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  # right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # bottom
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        # less than method used to compare objects
        return False


def make_grid(rows, width):
    """
    makes a list representation of the grid
    :param rows: number of rows we want in the grid of (row x row) dimension
    :param width: width of the pygame window
    :return: a 2d (row x row) length list of Node objects
    """
    grid = []
    gap = width // rows  # gives the dimension of each node square. 700 // 20 = 35 => each node = 35x35 px
    for i in range(rows):
        grid.append([])  # adding column list
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid_lines(win, rows, width):
    """
    draws the cell(node) distinction lines of the grid
    :param win: pygame window
    :param rows: number of rows we want in the grid of (row x row) dimension
    :param width: width of the pygame window
    :return: None
    """
    gap = width // rows
    for i in range(rows):
        # draws the top and bottom horizontal lines of each cell
        pygame.draw.line(win, WHITE, (0, i * gap), (width, i * gap))
        for j in range(rows):
            # draws the left and right vertical lines of each cell
            pygame.draw.line(win, WHITE, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    """
    converts the list represented grid to pygame visuals
    :param win: pygame window
    :param grid: 2d list of (rows x rows) dimension
    :param rows: number of rows we want in the grid of (row x row) dimension
    :param width: width of the pygame window
    :return: None
    """
    win.fill(BASE_COLOR)  # initiates the screen

    for row in grid:  # draws the cells(nodes)
        for node in row:
            node.draw(win)

    draw_grid_lines(win, rows, width)  # draws the grid lines
    pygame.display.update()  # updates pygame window


def get_clicked_node(pos, rows, width):
    """
    converts the mouse clicked screen position (x, y) to (row, col) of the grid
    :param pos: (x, y) coordinates
    :param rows: number of rows we want in the grid of (row x row) dimension
    :param width: width of the pygame window
    :return: (row, col) denoting the row and column index in the list representation of the grid
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

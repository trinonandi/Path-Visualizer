import pygame

CLOCK_DELAY = 15


def animate(path_dict, start, end, draw):
    """
    a function that animates the path by backtracking the path_dict
    :param path_dict: a dictionary that holds the node as key and its parent as value
    :param start: starting node
    :param end: goal node
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :return: None
    """
    path = [end]
    while path[-1] != start:
        node = path_dict[path[-1]]
        path.append(node)
        node.make_path()
        pygame.time.delay(CLOCK_DELAY)
        draw()


class BidirectionalSearch:
    def __init__(self, draw, grid, start, end):
        self.start = start
        self.end = end
        self.f_queue = [start]
        self.b_queue = [end]
        self.f_open_list = []
        self.b_open_list = []
        self.f_path_dict = {}
        self.b_path_dict = {}
        self.draw = draw
        self.grid = grid

    def is_intersecting(self):
        for row in self.grid:
            for node in row:
                if node in self.f_open_list and node in self.b_open_list:
                    return node

        return None

    def helper_algo(self, direction='forward'):
        if direction == 'forward':
            current = self.f_queue.pop(0)
            for neighbour in current.neighbours:
                if current not in self.f_queue:
                    if neighbour in self.f_open_list:
                        continue
                    self.f_path_dict[neighbour] = current
                    self.f_queue.append(neighbour)
                    if neighbour != self.start and neighbour != self.end:
                        neighbour.make_open()
                        self.f_open_list.append(neighbour)
            self.draw()
            if current != self.start:
                current.make_closed()

        else:
            current = self.b_queue.pop(0)
            for neighbour in current.neighbours:
                if current not in self.b_queue:
                    if neighbour in self.b_open_list:
                        continue
                    self.b_path_dict[neighbour] = current
                    self.b_queue.append(neighbour)
                    if neighbour != self.start and neighbour != self.end:
                        neighbour.make_open()
                        self.b_open_list.append(neighbour)

            self.draw()
            if current != self.end:
                current.make_closed()

    def animate_path(self, intersection):
        path = [intersection]
        i = intersection
        while i != self.start:
            path.append(self.f_path_dict[i])
            i = self.f_path_dict[i]
        path = path[::-1]
        i = intersection
        while i != self.end:
            path.append(self.b_path_dict[i])
            i = self.b_path_dict[i]

        for node in path:
            node.make_path()
            pygame.time.delay(CLOCK_DELAY)
            self.draw()

    def search(self):
        while len(self.f_queue) > 0 and len(self.b_queue) > 0:
            self.helper_algo('forward')
            self.helper_algo('backward')

            intersect = self.is_intersecting()
            if intersect is not None:
                self.animate_path(intersect)
                self.start.make_start()
                self.end.make_end()
                return True

        return False

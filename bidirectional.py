"""
It contains all the details necessary for performing both informed and uninformed bidirectional search
It acts as an auxiliary module for the following functions in algorithms.py:
    bidirectional_search()
    bidirectional_a_star_search()
    bidirectional_greedy_search()
"""
import pygame
from queue import PriorityQueue

CLOCK_DELAY = 15


class BidirectionalSearch:
    """
    a class to implement Blind Bidirectional Search By BFS algorithm
    ------------------------------------
    data fields
    ------------------------------------
    start: The starting node
    end: the ending node
    f_queue: queue for the forward search that is searching from start
    b_queue: queue for the backward search that is searching from the goal
    f_path_dict: forward path dictionary
    b_path_dict: backward path dictionary
    draw: the draw method used to update the grid state
    grid: the matrix format of the grid
    -----------------------------------
    methods
    -----------------------------------
    is_intersecting: check if the two search path intersected or not
    helper_algo: a helper that does parts of the BFS algorithm
    search: the actual BFS algorithm
    animate_path: animates path from start to goal is found

    """

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
        """
        checks if the forward and backward path collided or not
        :return: the collision node if collision occurs else None
        """
        for row in self.grid:
            for node in row:
                if node in self.f_open_list and node in self.b_open_list:
                    return node

        return None

    def helper_algo(self, direction='forward'):
        """
        performs dequeue and neighbour search operation of BFS for both the backward and forward search
        :param direction: String used to the forward or backward BFS
        :return: None
        """
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
            pygame.time.delay(CLOCK_DELAY)
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

            pygame.time.delay(CLOCK_DELAY)
            self.draw()
            if current != self.end:
                current.make_closed()

    def animate_path(self, intersection):
        """
        animates the path from start to end if found
        :param intersection: the collision node of backward and forward search
        :return: None
        """
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
        """
        The actual BFS algorithm will bw called from object to perform bidirectional search
        :return: Boolean True if path found else False
        """
        while len(self.f_queue) > 0 and len(self.b_queue) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
            self.helper_algo('forward')
            self.helper_algo('backward')

            intersect = self.is_intersecting()
            if intersect is not None:
                self.animate_path(intersect)
                self.start.make_start()
                self.end.make_end()
                return True

        return False


def h(p1, p2):
    """
    heuristic function h(x) that calculates the manhattan distance
    :param p1: point 1 having (x,y) coordinates
    :param p2: point 2 having (x,y) coordinates
    :return: the manhattan distance between them
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


class InformedBidirectionalSearch:
    """
    A class that implements bidirectional greedy and bidirectional A* search
    ----------------
    data fields
    ----------------
    all the fwd preceded data members are for forward direction search that begins from start node
    all the bkwd preceded data members are for backward direction search that begins from the goal node
    ----------------
    methods
    ----------------
    is_intersecting: check if the two search path intersected or not
    animate_path: animates path from start to goal is found
    a_star_helper_algo: it performs each iteration operations for A*. It performs for both forward and backward search
    a_star_search: the actual A* search method that is meant to be called through objects
    greedy_helper_algo: it performs each iteration tasks for greedy, Applicable for both backward and forward search
    greedy_search: the actual greedy search method that is meant to be called through objects
    """
    def __init__(self, draw, grid, start, end):
        self.start = start
        self.end = end
        self.draw = draw
        self.grid = grid

        self.bkwd_count = 0
        self.fwd_count = 0
        self.fwd_heap = PriorityQueue()
        self.fwd_heap.put((0, self.fwd_count, start))
        self.bkwd_heap = PriorityQueue()
        self.bkwd_heap.put((0, self.bkwd_count, end))

        self.fwd_open_list = []
        self.bkwd_open_list = []
        self.fwd_path_dict = {}
        self.bkwd_path_dict = {}

        self.fwd_f_score = {node: float("inf") for row in grid for node in row}
        self.fwd_f_score[start] = h(start.get_pos(), end.get_pos())
        self.fwd_g_score = {node: float("inf") for row in grid for node in row}
        self.fwd_g_score[start] = 0

        self.bkwd_f_score = {node: float("inf") for row in grid for node in row}
        self.bkwd_f_score[end] = h(end.get_pos(), start.get_pos())
        self.bkwd_g_score = {node: float("inf") for row in grid for node in row}
        self.bkwd_g_score[end] = 0

    def is_intersecting(self):
        """
        checks if the forward and backward path collided or not
        :return: the collision node if collision occurs else None
        """
        for row in self.grid:
            for node in row:
                if node in self.fwd_open_list and node in self.bkwd_open_list:
                    return node

        return None

    def a_star_helper_algo(self, direction="forward"):
        """
        helper method for A* search
        :param direction: String determining the direction of search
        :return: None
        """
        if direction == "forward":
            current = self.fwd_heap.get()[2]
            for neighbour in current.neighbours:
                if neighbour in self.fwd_open_list:
                    continue

                self.fwd_path_dict[neighbour] = current
                if neighbour != self.start:
                    self.fwd_count += 1
                    temp_g_score = self.fwd_g_score[current] + 1
                    self.fwd_g_score[neighbour] = temp_g_score
                    self.fwd_f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), self.end.get_pos())
                    self.fwd_heap.put((self.fwd_f_score[neighbour], self.fwd_count, neighbour))
                    self.fwd_open_list.append(neighbour)
                    neighbour.make_open()

            pygame.time.delay(CLOCK_DELAY)
            self.draw()
            if current != self.start:
                current.make_closed()

        else:
            current = self.bkwd_heap.get()[2]

            for neighbour in current.neighbours:
                if neighbour in self.bkwd_open_list:
                    continue
                self.bkwd_path_dict[neighbour] = current
                if neighbour != self.end:
                    self.bkwd_count += 1
                    temp_g_score = self.bkwd_g_score[current] + 1
                    self.bkwd_g_score[neighbour] = temp_g_score
                    self.bkwd_f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), self.start.get_pos())
                    self.bkwd_heap.put((self.bkwd_f_score[neighbour], self.bkwd_count, neighbour))
                    self.bkwd_open_list.append(neighbour)
                    neighbour.make_open()

            pygame.time.delay(CLOCK_DELAY)
            self.draw()
            if current != self.end:
                current.make_closed()

    def a_star_search(self):
        """
        method to perform bidirectional A* search
        :return: Boolean True if path found else False
        """

        while not self.bkwd_heap.empty() and not self.fwd_heap.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
            self.a_star_helper_algo("forward")
            self.a_star_helper_algo("backward")

            intersect = self.is_intersecting()
            if intersect is not None:
                self.animate_path(intersect)
                self.start.make_start()
                self.end.make_end()
                return True

    def animate_path(self, intersection):
        """
        animates the path from start to end if found
        :param intersection: the collision node of backward and forward search
        :return: None
        """
        path = [intersection]
        i = intersection
        while i != self.start:
            path.append(self.fwd_path_dict[i])
            i = self.fwd_path_dict[i]
        path = path[::-1]
        i = intersection
        while i != self.end:
            path.append(self.bkwd_path_dict[i])
            i = self.bkwd_path_dict[i]

        for node in path:
            node.make_path()
            pygame.time.delay(CLOCK_DELAY)
            self.draw()

    def greedy_helper_algo(self, direction="forward"):
        """
        helper function for greedy best first search
        :param direction: String determines the direction of search
        :return: None
        """
        if direction == "forward":
            current = self.fwd_heap.get()[2]
            for neighbour in current.neighbours:
                if neighbour in self.fwd_open_list:
                    continue

                self.fwd_path_dict[neighbour] = current
                if neighbour != self.start:
                    self.fwd_count += 1
                    self.fwd_f_score[neighbour] = h(neighbour.get_pos(), self.end.get_pos())
                    self.fwd_heap.put((self.fwd_f_score[neighbour], self.fwd_count, neighbour))
                    self.fwd_open_list.append(neighbour)
                    neighbour.make_open()

            pygame.time.delay(CLOCK_DELAY)
            self.draw()
            if current != self.start:
                current.make_closed()

        else:
            current = self.bkwd_heap.get()[2]

            for neighbour in current.neighbours:
                if neighbour in self.bkwd_open_list:
                    continue
                self.bkwd_path_dict[neighbour] = current
                if neighbour != self.end:
                    self.bkwd_f_score[neighbour] = h(neighbour.get_pos(), self.start.get_pos())
                    self.bkwd_heap.put((self.bkwd_f_score[neighbour], self.bkwd_count, neighbour))
                    self.bkwd_open_list.append(neighbour)
                    neighbour.make_open()

            pygame.time.delay(CLOCK_DELAY)
            self.draw()
            if current != self.end:
                current.make_closed()

    def greedy_search(self):
        """
        method to perform bidirectional greedy best first search
        :return: Boolean True if path found else False
        """
        while not self.bkwd_heap.empty() and not self.fwd_heap.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
            self.greedy_helper_algo("forward")
            self.greedy_helper_algo("backward")

            intersect = self.is_intersecting()
            if intersect is not None:
                self.animate_path(intersect)
                self.start.make_start()
                self.end.make_end()
                return True

from queue import PriorityQueue
import pygame


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(draw, grid, start, end):
    count = 0
    heap = PriorityQueue()
    heap.put((0, count, start))
    open_set = {start}
    path_dict = dict()

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    while not heap.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heap.get()[2]  # returns the Node object from the tuple
        open_set.remove(current)

        if current == end:
            reconstruct_path(path_dict, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbour]:
                path_dict[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set:
                    count += 1
                    heap.put((f_score[neighbour], count, neighbour))
                    open_set.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def reconstruct_path(path_dict, current, draw):
    while current in path_dict:
        current = path_dict[current]
        current.make_path()
        draw()

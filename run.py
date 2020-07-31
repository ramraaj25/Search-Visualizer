import pygame
from queue import PriorityQueue
import math

WIDTH = 600


pygame.init()
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.init()
pygame.display.set_caption("GRID")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node():
    def __init__(self, row, col, total_rows):
        self.row = row
        self.col = col
        self.color = WHITE
        self.width = WIDTH / total_rows
        self.x = self.col * self.width
        self.y = self.row * self.width
        self.total_rows = total_rows
        self.neighbors = []
        self.f = math.inf
        self.g = math.inf

    # def __eq__(self, other):
    #     if self.row == other.row and self.col == other.col:
    #         return True
    #     return False

    def is_start(self):
        return self.color == TURQUOISE

    def is_end(self):
        return self.color == ORANGE

    def is_barrier(self):
        return self.color == BLACK

    def is_visited(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def make_start(self):
        self.color = TURQUOISE

    def make_open(self):
        self.color = GREEN

    def make_end(self):
        self.color = ORANGE

    def make_barrier(self):
        self.color = BLACK

    def make_visited(self):
        self.color = RED

    def make_path(self):
        self.color = PURPLE

    def reset(self):
        self.color = WHITE

    def update_neighbors(self, grid):

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False


def h(node, end):
    val = abs(end.row - node.row) + abs(end.col - node.col)
    return val


def make_grid(rows):
    grid = [[None for x in range(rows)] for y in range(rows)]
    for i in range(rows):
        for j in range(rows):
            grid[i][j] = Node(i, j, rows)
    return grid


def draw(win, grid, rows):
    for i in range(rows):
        for j in range(rows):
            node = grid[i][j]
            node.draw(win)
    draw_grid_lines(win, rows)

    pygame.display.update()


def draw_grid_lines(win, rows):
    # Vertical lines
    gap = WIDTH / rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (gap * i, 0), (gap * i, WIDTH))

    # Horizontal lines
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, gap * i), (WIDTH, gap * i))


def algorithm(draw, start, end, grid, algo=2):
    if algo != 2:
        open_set = []
        open_set.append(start)
        parent = {}
        while open_set:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if algo == 0:
                curr = open_set.pop(0)
                if not curr.is_start():
                    curr.make_visited()
            else:
                curr = open_set.pop()
                if not curr.is_start():
                    curr.make_visited()
            for neighbor in curr.neighbors:
                if not neighbor.is_visited() and not neighbor.is_barrier() and not neighbor == start and not neighbor.is_open():
                    if neighbor == end:
                        parent[end] = curr
                        draw_path(parent, end, draw)
                        start.make_start()
                        return True
                    else:
                        open_set.append(neighbor)

                        neighbor.make_open()
                        parent[neighbor] = curr

            draw()
    else:
        count = 0
        open_set = PriorityQueue()
        start.g = 0
        open_set.put((0, count, start))
        start.f = h(start, end)
        open_set_hash = [start]
        came_from = {}
        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            curr = open_set.get()[2]
            if not curr.is_start():
                curr.make_visited()
            open_set_hash.remove(curr)
            for neighbor in curr.neighbors:
                temp_g = curr.g + 1
                if not neighbor.is_barrier() and not neighbor == start and not neighbor.is_visited() and not neighbor.is_start():
                    if neighbor == end:
                        came_from[end] = curr
                        draw_path(came_from, end, draw)
                        start.make_start()
                        return True
                    elif temp_g < neighbor.g:
                        neighbor.g = temp_g
                        neighbor.f = h(neighbor, end) + temp_g
                        came_from[neighbor] = curr
                        if neighbor not in open_set_hash:
                            count += 1
                            open_set.put((neighbor.f, count, neighbor))
                            open_set_hash.append(neighbor)
                            neighbor.make_open()

            draw()
        print("False")


def draw_path(came_from, current, draw):

    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def main():
    run = True
    rows = 40
    gap = WIDTH / rows
    grid = make_grid(rows)
    start = False
    end = False
    while run:
        draw(WIN, grid, rows)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                x, y = pygame.mouse.get_pos()
                row = int(y // gap)
                col = int(x // gap)
                if not start:
                    if not grid[row][col].is_start() and not grid[row][col].is_end() and not grid[row][col].is_barrier():
                        start = True
                        start_node = grid[row][col]
                        grid[row][col].make_start()
                elif not end:
                    if not grid[row][col].is_end() and not grid[row][col].is_start() and not grid[row][col].is_barrier():
                        end = True
                        end_node = grid[row][col]
                        grid[row][col].make_end()
                else:
                    if not grid[row][col].is_barrier() and not grid[row][col].is_end() and not grid[row][col].is_start():
                        grid[row][col].make_barrier()
            elif mouse[2]:
                x, y = pygame.mouse.get_pos()
                row = int(y // gap)
                col = int(x // gap)
                if grid[row][col].is_start():
                    start = False
                    grid[row][col].reset()
                elif grid[row][col].is_end():
                    end = False
                    grid[row][col].reset()
                else:
                    grid[row][col].reset()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = False
                    end = False
                    for i in range(rows):
                        for j in range(rows):
                            grid[i][j].reset()

                elif event.key == pygame.K_d:
                    for i in range(rows):
                        for j in range(rows):
                            grid[i][j].update_neighbors(grid)
                    algorithm(lambda: draw(WIN, grid, rows),
                              start_node, end_node, grid, algo=1)

                elif event.key == pygame.K_b:
                    for i in range(rows):
                        for j in range(rows):
                            grid[i][j].update_neighbors(grid)
                    algorithm(lambda: draw(WIN, grid, rows),
                              start_node, end_node, grid, algo=0)
                elif event.key == pygame.K_a:
                    for i in range(rows):
                        for j in range(rows):
                            grid[i][j].update_neighbors(grid)
                    algorithm(lambda: draw(WIN, grid, rows),
                              start_node, end_node, grid, algo=2)

    pygame.quit()


main()

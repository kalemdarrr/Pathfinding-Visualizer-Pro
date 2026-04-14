import pygame

# Muted Colors for professional look
RED = (220, 53, 69) # End Node
GREEN = (40, 167, 69) # Start Node
BLUE = (0, 123, 255) # Visited
YELLOW = (255, 193, 7) # Path
WHITE = (255, 255, 255) # Empty
BLACK = (52, 58, 64) # Wall
GREY = (200, 200, 200) # Grid lines

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
        self.distance = float("inf")
        self.previous = None

    def get_pos(self):
        return self.row, self.col

    def is_visited(self):
        return self.color == BLUE

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE
        self.distance = float("inf")
        self.previous = None

    def make_start(self):
        self.color = GREEN

    def make_wall(self):
        self.color = BLACK

    def make_end(self):
        self.color = RED

    def make_visited(self):
        self.color = BLUE
        
    def make_path(self):
        self.color = YELLOW

    def draw(self, win, x_offset=0, y_offset=0):
        pygame.draw.rect(win, self.color, (self.x + x_offset, self.y + y_offset, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

def make_grid(rows, total_width):
    grid = []
    # width is the dimension of the square grid area
    gap = total_width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, total_width, x_offset=0, y_offset=0):
    gap = total_width // rows
    for i in range(rows + 1): 
        pygame.draw.line(win, GREY, (x_offset, i * gap + y_offset), (total_width + x_offset, i * gap + y_offset))
        for j in range(rows + 1):
            pygame.draw.line(win, GREY, (j * gap + x_offset, y_offset), (j * gap + x_offset, total_width + y_offset))

def draw(win, grid, rows, total_width, x_offset=0, y_offset=0):
    for row in grid:
        for node in row:
            node.draw(win, x_offset, y_offset)
            
    draw_grid_lines(win, rows, total_width, x_offset, y_offset)
    pygame.display.update()

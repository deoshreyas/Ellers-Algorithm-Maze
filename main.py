import pygame
from pygame.locals import *
import random

pygame.init()

# WINDOW
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eller's Algorithm")

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# CELL CLASS
CELL_SIZE = 20
LINE_WIDTH = 2
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.set = None
        self.walls = [True, True, True, True]

    def show(self):
        x = self.x * CELL_SIZE
        y = self.y * CELL_SIZE
        if self.walls[0]:
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), LINE_WIDTH)
        if self.walls[1]:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), LINE_WIDTH)
        if self.walls[2]:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), LINE_WIDTH)
        if self.walls[3]:
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x, y), LINE_WIDTH)

# SET UP MAZE
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
maze = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]

# ELLER'S ALGORITHM 
DELAY = 100
def ellersAlgo():
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x].set is None:
                maze[y][x].set = f"{y}-{x}"
        for x in range(COLS - 1):
            if maze[y][x].set != maze[y][x + 1].set and random.choice([True, False]):
                maze[y][x].walls[1] = False
                maze[y][x + 1].walls[3] = False
                old_set = maze[y][x + 1].set
                for row in maze:
                    for cell in row:
                        if cell.set == old_set:
                            cell.set = maze[y][x].set
        sets = {}
        for x in range(COLS):
            if maze[y][x].set not in sets:
                sets[maze[y][x].set] = [x]
            else:
                sets[maze[y][x].set].append(x)
        for s in sets.values():
            down_paths = random.sample(s, k=random.randint(1, len(s)))
            for x in down_paths:
                if y < ROWS - 1:
                    maze[y][x].walls[2] = False
                    maze[y + 1][x].walls[0] = False
                    maze[y + 1][x].set = maze[y][x].set
        drawMaze()
        pygame.display.flip()
        pygame.time.wait(DELAY)
        if y == ROWS - 1:
            for x in range(COLS - 1):
                if maze[y][x].set != maze[y][x + 1].set:
                    maze[y][x].walls[1] = False
                    maze[y][x + 1].walls[3] = False
                    old_set = maze[y][x + 1].set
                    for cell in maze[y]:
                        if cell.set == old_set:
                            cell.set = maze[y][x].set

# DRAW MAZE
def drawMaze():
    screen.fill(WHITE)
    for row in maze:
        for cell in row:
            cell.show()

# MAIN LOOP
running = True
mazeGenerated = False  # Flag to check if maze has been generated

while running:
    drawMaze()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not mazeGenerated:
                ellersAlgo() 
                mazeGenerated = True 

    pygame.display.flip()
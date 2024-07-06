import pygame
from pygame.locals import *
import random
import heapq

pygame.init()

# WINDOW
WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eller's Algorithm")

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# SPECIAL CELLS 
START = None # Start cell 
END = None # End cell

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
            pygame.draw.line(window, BLACK, (x, y), (x + CELL_SIZE, y), LINE_WIDTH)
        if self.walls[1]:
            pygame.draw.line(window, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), LINE_WIDTH)
        if self.walls[2]:
            pygame.draw.line(window, BLACK, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), LINE_WIDTH)
        if self.walls[3]:
            pygame.draw.line(window, BLACK, (x, y + CELL_SIZE), (x, y), LINE_WIDTH)

# SET UP MAZE
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
maze = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]

# ELLER'S ALGORITHM 
DELAY = 100
def ellers_algo():
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
        draw_maze()
        pygame.display.update()
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
def draw_maze():
    window.fill(WHITE)
    for row in maze:
        for cell in row:
            cell.show()
            if (cell.x, cell.y) == START:
                pygame.draw.rect(window, BLUE, (cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if (cell.x, cell.y) == END:
                pygame.draw.rect(window, RED, (cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if (cell.x, cell.y) in final_path:
                pygame.draw.rect(window, GREEN, (cell.x * CELL_SIZE, cell.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# A* PATHFINDING ALGORITHM
def astar(start, end):
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end), 0, "", start)) 
    came_from = {}
    g_score = {(cell.x, cell.y): float("inf") for row in maze for cell in row}
    g_score[start] = 0

    while open_set:
        current = heapq.heappop(open_set)[3]
        if current != start and current != end:
            pygame.draw.rect(window, YELLOW, (current[0] * CELL_SIZE, current[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            pygame.time.wait(10)
        if current == end:
            reconstruct_path(came_from, current)
            return
        for direction, (dx, dy) in [("U", (0, -1)), ("D", (0, 1)), ("L", (-1, 0)), ("R", (1, 0))]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < COLS and 0 <= neighbor[1] < ROWS and not is_wall_between(current, neighbor):
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    if neighbor not in [i[3] for i in open_set]:
                        heapq.heappush(open_set, (f_score, tentative_g_score, direction, neighbor))

def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

final_path = []
def reconstruct_path(came_from, current):
    global final_path
    while current in came_from:
        pygame.draw.rect(window, GREEN, (current[0] * CELL_SIZE, current[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        current = came_from[current]
        final_path.append(current)
        pygame.display.update()
        pygame.time.wait(50)

def is_wall_between(current, neighbor):
    current_cell = maze[current[1]][current[0]]
    dx, dy = neighbor[0] - current[0], neighbor[1] - current[1]
    if dx == 1:  # Right
        return current_cell.walls[1]
    if dx == -1:  # Left
        return current_cell.walls[3]
    if dy == 1:  # Down
        return current_cell.walls[2]
    if dy == -1:  # Up
        return current_cell.walls[0]
    return True  # In case something goes wrong

# MAIN LOOP
running = True
mazeGenerated = False  # Flag to check if maze has been generated

while running:
    draw_maze()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE and not mazeGenerated:
                ellers_algo() 
                mazeGenerated = True 
            elif event.key == K_c and mazeGenerated:
                maze = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]
                START = None
                END = None
                mazeGenerated = False
                final_path = []
            elif event.key == K_RETURN and mazeGenerated and START and END:
                astar(START, END)
    
    # SET START AND END CELLS
    if pygame.mouse.get_pressed()[0] and mazeGenerated:
        x, y = pygame.mouse.get_pos()
        x, y = x // CELL_SIZE, y // CELL_SIZE
        if START is None:
            START = (x, y)
        if END is None and (x, y) != START:
            END = (x, y)

    pygame.display.update()
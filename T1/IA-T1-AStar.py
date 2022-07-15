import os
import pygame
import math
from queue import PriorityQueue

# matrix 82 x 300

WIN_WIDTH = 300*4
WIN_HEIGHT = 82*7
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Trabalho 1 de IA")

RED = (255, 0, 0)
FOREST = (0, 150, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
SAND = (194, 178, 128)
BROWN = (125,82,42)
PINK = (193, 95, 190)

class Square:
    def __init__(self, row, col, width, height, cost, color, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = col*width
        self.y = row*height
        self.cost = cost
        self.color = color
        self.neighbors = []
        self.height = height
        self.width = width
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_pos(self):
        return self.row, self.col

    def get_cost(self):
        return self.cost
    
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        return self.color == WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1:
            self.neighbors.append(grid[self.row + 1][self.col]) # vizinho sul

        if self.row > 0:
            self.neighbors.append(grid[self.row - 1][self.col]) # vizinho norte

        if self.col < self.total_cols - 1:
            self.neighbors.append(grid[self.row][self.col + 1]) # vizinho leste

        if self.col > 0:
            self.neighbors.append(grid[self.row][self.col - 1]) # vizinho oeste
    
    def __lt__(self, other):
        return False


def create_map(file):
    here = os.path.dirname(os.path.abspath(__file__))   # here é o diretório onde se encontra o map
    filename = os.path.join(here, file) # concatena o diretorio com o nome do arquivo
    arq = open(filename,'r')        
    aux = arq.readlines() 
    map = []
    for linha in aux:
        if list(linha)[-1] == '\n':
            map.append(list(linha[0:-1]))
        else:
            map.append(list(linha))
    return map  

def get_points_stages(map):   # guarda as coordenadas no map de cada etapa, ou seja, 'stages' guarda as 32 posições das etapas  
    stages = []

    for i in range(32):
        stages.append(0)

    for i in range(len(map)):          # i anda pelas linhas de map
        for j in range(len(map[i])):   # j anda pelas colunas de map
            elem = map[i][j]           # elem é uma posição do map, que possui como valor um tipo de terreno
            if elem == '0':
                stages[0] = [i,j]
            elif elem == '1':
                stages[1] = [i,j]
            elif elem == '2':
                stages[2] = [i,j]
            elif elem == '3':
                stages[3] = [i,j]
            elif elem == '4':
                stages[4] = [i,j]
            elif elem == '5':
                stages[5] = [i,j]
            elif elem == '6':
                stages[6] = [i,j]
            elif elem == '7':
                stages[7] = [i,j]
            elif elem == '8':
                stages[8] = [i,j]
            elif elem == '9':
                stages[9] = [i,j]
            elif elem == 'B':
                stages[10] = [i,j]
            elif elem == 'C':
                stages[11] = [i,j]
            elif elem == 'D':
                stages[12] = [i,j]
            elif elem == 'E':
                stages[13] = [i,j]
            elif elem == 'G':
                stages[14] = [i,j]
            elif elem == 'H':
                stages[15] = [i,j]
            elif elem == 'I':
                stages[16] = [i,j]
            elif elem == 'J':
                stages[17] = [i,j]
            elif elem == 'K':
                stages[18] = [i,j]
            elif elem == 'L':
                stages[19] = [i,j]
            elif elem == 'N':
                stages[20] = [i,j]
            elif elem == 'O':
                stages[21] = [i,j]
            elif elem == 'P':
                stages[22] = [i,j]
            elif elem == 'Q':
                stages[23] = [i,j]
            elif elem == 'S':
                stages[24] = [i,j]
            elif elem == 'T':
                stages[25] = [i,j]
            elif elem == 'U':
                stages[26] = [i,j]
            elif elem == 'V':
                stages[27] = [i,j]
            elif elem == 'W':
                stages[28] = [i,j]
            elif elem == 'X':
                stages[29] = [i,j]
            elif elem == 'Y':
                stages[30] = [i,j]
            elif elem == 'Z':
                stages[31] = [i,j]
    return stages


def manhattan(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {square: float("inf") for row in grid for square in row}
	g_score[start] = 0
	f_score = {square: float("inf") for row in grid for square in row}
	f_score[start] = manhattan(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + neighbor.get_cost()

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + manhattan(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def make_grid(width, height, map):
    grid = []
    s_height = height // len(map)
    s_width = width // len(map[0]) 

    for i in range(len(map)):
        grid.append([])
        for j in range(len(map[0])):
            if map[i][j] == ".":
                cost = 1
                color = SAND
            elif map[i][j] == "R":
                cost = 5
                color = BROWN
            elif map[i][j] == "F":
                cost = 10
                color = FOREST
            elif map[i][j] == "A":
                cost = 15
                color = BLUE
            elif map[i][j] == "M":
                cost = 200
                color = GREY
 
            square = Square(i, j, s_width, s_height, cost, color, len(map), len(map[0]))
            grid[i].append(square)

    return grid


def draw(win, grid):
	win.fill(WHITE)

	for row in grid:
		for square in row:
			square.draw(win)

	pygame.display.update()


def AStarSearchInMap(win, width, height, map, points):
    grid = make_grid(width, height, map)
    i = 0

    run = True

    while run or i < 32:
        row_or, col_or = points[i]
        row_dt, col_dt = points[i+1]
        start = grid[row_or][col_or]
        end = grid[row_dt][col_dt]
        draw(win, grid)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for row in grid:
            for square in row:
                square.update_neighbors(grid)
        algorithm(lambda: draw(win, grid), grid, start, end)
        i += 1
        grid = make_grid(width, height, map)

    pygame.quit()


map = create_map('mapa.txt')
stage_points = get_points_stages(map) 
AStarSearchInMap(WIN, WIN_WIDTH, WIN_HEIGHT, map, stage_points)

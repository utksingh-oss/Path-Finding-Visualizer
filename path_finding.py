#pip install pygame
#python -m pip install pygame

import pygame 
import math 
from queue import PriorityQueue 

WIDTH = 800 #width of the screen
WIN = pygame.display.set_mode((WIDTH , WIDTH)) #seting up the display
pygame.display.set_caption("A* Path Finding Algorithm") #adding caption

#COLORS 
RED = (255 , 0 , 0)
BLUE = (0 , 255 , 0)
GREEN = (0 , 0 , 255)
YELLOW = (255 , 255 , 0)
WHITE = (255 , 255 , 255)
BLACK = (0 , 0 , 0)
PURPLE = (128 , 0 , 128)
ORANGE = (125 , 165 , 0)
GREY = (128 , 128 , 128)
TURQUOISE = (64 , 224 , 208)


class Spot : #node
	def __init__(self, row , col , width , total_rows):
		self.row = row
		self.col = col 
		self.x = row * width #starting coordinate positions
		self.y = col * width #starting coordinate positions
		self.color = WHITE
		self.neighbours = []
		self.width = width 
		self.total_rows = total_rows

	def get_pos(self): #returning the position of node
		return self.row , self.col   

	def is_closed(self): #is it already considered
		return self.color == RED 

	def is_open(self): #is the node in open set
		return self.color == GREEN		

	def is_barrier(self): #is node allowed to be visited
		return self.color == BLACK 	

	def is_start(self): #is the node starting point
		return self.color == ORANGE

	def is_end(self): #is the node ending point
		return self.color == TURQUOISE

	def reset(self): #function to reset the node
		self.color = WHITE

	#functions to change the state of nodes
	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED 

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self , win): #win --> where do we want to draw it
		pygame.draw.rect(win , self.color , (self.x , self.y , self.width , self.width))

	def update_neighbours(self , grid):
		#check up down left right and check if it is not barrier
		self.neighbours = []
		if self.row < self.total_rows-1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbours.append(grid[self.row + 1][self.col]) #append the next row down
		
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
			self.neighbours.append(grid[self.row - 1][self.col]) #UP
		
		if self.col < self.total_rows-1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbours.append(grid[self.row][self.col + 1]) #RIGHT
		
		if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
			self.neighbours.append(grid[self.row][self.col-1]) #LEFT


	def __lt__(self , other): #lt=less than: how do we compare two nodes
		return False #other node is always greater than the current node

def h(p1 , p2): #heurestic function for point 1 and point 2
	#manhattan distance formula
	x1 , y1  = p1 #splliting values
	x2 , y2  = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from , current , draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

#main algorithms (A* Path Finding Algorithm)
def algorithm(draw , grid , start , end):
	#draw is a lambda function here
	count = 0 
	open_set = PriorityQueue()
	open_set.put((0 , count , start)) #adding the start node 
	#count here is basically a tie breaker in case if two nodes have same f-values
	came_from = {} 
	g_score = {spot : float("inf") for row in grid for spot in row}
	g_score[start] = 0 #g_score of the start node is 0
	f_score = {spot : float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos() , end.get_pos()) #heurestic : how far away is the end node

	open_set_hash = {start} #to check if some value is in the PQ or not

	while not open_set.empty() : #while set is not empty
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] #get 2nd element just the node
		open_set_hash.remove(current) #pop from the set

		if current == end :
			reconstruct_path(came_from , end , draw)
			end.make_end() 
			return True

		for neighbour in current.neighbours:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbour]:
				came_from[neighbour] = current
				g_score[neighbour] = temp_g_score
				f_score[neighbour] = temp_g_score + h(neighbour.get_pos() , end.get_pos())
				if neighbour not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbour] , count , neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open() #so we know we have already considered 
		draw()

		if current != start :
			current.make_closed()

	return None # if no path was found



def make_grid(rows , width):
	grid = []
	gap = width // rows #gap between each node(square)
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i , j , gap , rows)
			grid[i].append(spot) 

	return grid

def draw_grid(win , rows , width):
	gap = width // rows 
	for i in range(rows):
		pygame.draw.line(win, GREY , (0 , i * gap),(width , i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY , (j*gap , 0),(j*gap, width))

def draw(win , grid , rows , width):
	win.fill(WHITE)

	for row in grid:
		for spot in row :
			spot.draw(win) #spot function

	draw_grid(win , rows , width)
	pygame.display.update()

def get_clicked_pos(pos , rows , width):
	gap = width // rows 
	y , x = pos 

	row = y // gap 
	col = x // gap 

	return row , col 

#main loop
def main(win , width):
	ROWS = 50 
	grid = make_grid(ROWS , width) #returns 2d list of spots

	start = None 
	end = None 

	run = True
	started = False 

	while run :
		draw(win , grid , ROWS , width) 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if started : #if started user should not be able to click on anything except quit 
				continue

			if pygame.mouse.get_pressed()[0]: #if left mouse button is clicked
				pos = pygame.mouse.get_pos()
				row , col = get_clicked_pos(pos , ROWS , width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot 
					start.make_start()

				elif not end and spot != start:
					end = spot 
					end.make_end()
				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2] : #if right mouse button is clicked
				pos = pygame.mouse.get_pos()
				row , col = get_clicked_pos(pos , ROWS , width)
				spot = grid[row][col]
				spot.reset() #make the spot white
				if spot == start :
					start = None 
				elif spot == end :
					end = None 

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid :
						for spot in row :
							spot.update_neighbours(grid)
					algorithm(lambda: draw( win , grid , ROWS , width) , grid , start , end) #passing draw function to algorithm function

				if event.key == pygame.K_c: #restart 
					start = None
					end = None
					grid = make_grid(ROWS , width)

	pygame.quit()

main(WIN , WIDTH)

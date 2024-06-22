import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))

class Character:
	def __init__(self, x, y, size, rect, obstacles: list[int]) -> None:
		self.beginX = x
		self.beginY = y

		self.endX = x+size
		self.endY = y+size

		self.rect = rect
		self.obstacles = obstacles
	
	def draw(self, surface):
		surface.fill((255,255,255))

	def move(self, dir: int, amt = 5):
		# Note that dir is either the integer 1, meaning right, or -1, meaning left
		self.x = self.x + dir*amt
	
	def checkUnder(self) -> bool:
		allUnder = []
		for obstacle in obstacle:
			# Basically check if this obj is under by checking X coords to see if X is on platform then Y to see if y is on platform
			allUnder.append(obstacle[0][0] >= self.endX >= obstacle[1][0] and \
				obstacle[0][0] >= self.beginX >= obstacle[1][0] and \
				obstacle[0][1] >= self.endY >= obstacle[1][1])
		
		return any(allUnder) # Returns true if any of the obstacles are under the player

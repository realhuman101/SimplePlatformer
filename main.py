import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))

OBSTACLES = [((350, 200), (400, 300))]

class Character:
	def __init__(self, x, y, size, obstacles: list[int]) -> None:
		self.beginX = x-(size/2)
		self.beginY = y-(size/2)

		self.endX = x+(size/2)
		self.endY = y+(size/2)

		self.rect = self.updateRect()
		self.obstacles = obstacles

		self.jumpCount = 0

	def updateRect(self):
		self.rect = pygame.Rect((self.beginX, self.endX), (self.beginY, self.endY))
		return self.rect
	
	def draw(self, surface):
		self.updateRect()
		pygame.draw.rect(surface, (255, 0, 0), self.rect)

	def move(self, dir: int, amt = 5):
		# Note that dir is either the integer 1, meaning right, or -1, meaning left
		self.beginX = self.beginX + dir*amt
		self.endX = self.endX + dir*amt

		self.updateRect()
	
	def checkUnder(self) -> bool:
		allUnder = []
		for obstacle in obstacle:
			# Basically check if this obj is under by checking X coords to see if X is on platform then Y to see if y is on platform
			allUnder.append(obstacle[0][0] >= self.endX >= obstacle[1][0] and \
				obstacle[0][0] >= self.beginX >= obstacle[1][0] and \
				obstacle[0][1] >= self.endY >= obstacle[1][1])
		
		return any(allUnder) # Returns true if any of the obstacles are under the player
	
	def jump(self, amt = 5):
		if self.checkUnder(): #Making sure not double jumping - basically chck if on platform
			if self.jumpCount > 0:
				self.beginY += amt
				self.beginX += amt

				self.jumpCount -= 1

		self.updateRect()


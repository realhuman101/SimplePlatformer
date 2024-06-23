import pygame
import time

pygame.init()

screen = pygame.display.set_mode((500, 500))

OBSTACLES = [((350+50, 200+50), (550, 300)), ((0, 100), (50, 120))]

class Character:
	def __init__(self, x, y, size, obstacles: list[int]) -> None:
		self.size = size

		self.beginX = x-(size/2)
		self.beginY = y-(size/2)

		self.endX = x+(size/2)
		self.endY = y+(size/2)

		self.rect = self.updateRect()
		self.obstacles = obstacles

		self.jumpCount = 0

	def updateRect(self):
		self.rect = pygame.Rect((self.beginX, self.beginY), (self.size, self.size))
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
		for obstacle in self.obstacles:
			# Basically check if this obj is under by checking X coords to see if X is on platform then Y to see if y is on platform
			allUnder.append(obstacle[0][0] >= self.endX >= obstacle[1][0] and \
				obstacle[0][0] >= self.beginX >= obstacle[1][0] and \
				obstacle[0][1] >= self.endY >= obstacle[1][1])
		
		return any(allUnder) # Returns true if any of the obstacles are under the player
	
	def jump(self, amt = 5):
		if self.checkUnder(): #Making sure not double jumping - basically chck if on platform
			if self.jumpCount > 0:
				if self.beginY > 0:
					self.beginY -= amt
				if self.endX > 0:
					self.endY -= amt

				self.jumpCount -= 1

		self.updateRect()
	
	def gravity(self, amt = 5):
		if not self.checkUnder(): # NOthing underneath
			if self.endY != 500:
				self.endY += amt
			if self.beginY != 500:
				self.beginY += amt
		
		self.updateRect()

def drawObstacles(surface, obstacles, color = (0,0,0)):
	for obstacle in obstacles:
		obstRect = pygame.Rect((obstacle[0][0], obstacle[0][1]), (obstacle[1][0]-obstacle[0][0], obstacle[1][1]-obstacle[0][1]))

		pygame.draw.rect(surface, color, obstRect)

player = Character(250, 350, 50, OBSTACLES)

while True:
	screen.fill((255,255,255))

	player.gravity()

	player.jump()
	player.draw(screen)

	drawObstacles(screen, OBSTACLES)

	events = pygame.event.get()

	for event in events:
		if event.type == pygame.QUIT:  # Allow user to quit
			raise SystemExit
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP or event.key == pygame.K_SPACE:  # jump
				player.jumpCount = 10
			elif event.key == pygame.K_LEFT: # move left
				player.move(-1)
			elif event.key == pygame.K_RIGHT: # move right
				player.move(1)
	
	pygame.display.flip() # Refresh frame
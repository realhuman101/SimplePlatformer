import pygame
import time

pygame.init()

screen = pygame.display.set_mode((1000, 500))

OBSTACLES = [
    ((200, 375), (350, 410)),
    ((0, 100), (50, 120)),
    ((400, 300), (450, 330)),
    ((100, 200), (150, 230)),
    ((600, 400), (650, 430)),
    ((800, 100), (900, 130)),
    ((500, 350), (550, 500)),
    ((50, 450), (300, 470)),
    ((750, 50), (780, 300)),
    ((250, 50), (400, 80))
]

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

	def move(self, dir: int, amt = 0.25):
		# Note that dir is either the integer 1, meaning right, or -1, meaning left
		self.beginX = self.beginX + dir*amt
		self.endX = self.endX + dir*amt

		self.updateRect()
	
	def checkUnder(self) -> bool:
		allUnder = []
		for obstacle in self.obstacles:
			# Basically check if this obj is under by checking X coords to see if X is on platform then Y to see if y is on platform
			allUnder.append((obstacle[0][0] <= self.endX <= obstacle[1][0] or \
				obstacle[0][0] <= self.beginX <= obstacle[1][0]) and \
				obstacle[0][1] <= self.endY <= obstacle[1][1])
		
		return any(allUnder) # Returns true if any of the obstacles are under the player
	
	def jump(self, amt = 100):
		if self.jumpCount > 0:
			if self.checkUnder(): #Making sure not double jumping - basically chck if on platform
				if self.beginY > 0:
					self.beginY -= amt # - = up, + = down
				if self.endY > 0:
					self.endY -= amt

			self.jumpCount -= 1

		self.updateRect()
	
	def gravity(self, amt = 0.1):
		if not self.checkUnder(): # NOthing underneath
			if self.endY != 500:
				self.endY += amt
			if self.beginY != 500:
				self.beginY += amt
		
		self.updateRect()

def drawObstacles(surface, obstacles, color = (0,0,0)):
	for obstacle in obstacles:
		obstRect = pygame.Rect((obstacle[0][0], obstacle[0][1]), \
						 		(obstacle[1][0]-obstacle[0][0], \
								obstacle[1][1]-obstacle[0][1]))

		pygame.draw.rect(surface, color, obstRect)

player = Character(250, 350, 50, OBSTACLES)

movements = {
	'left': False,
	'right': False
}

while True:
	screen.fill((255,255,255))

	player.gravity()

	player.jump()
	player.draw(screen)

	# While keys down
	if movements['left']:
		player.move(-1)
	if movements['right']:
		player.move(1)

	drawObstacles(screen, OBSTACLES)

	events = pygame.event.get()

	for event in events:
		if event.type == pygame.QUIT:  # Allow user to quit
			raise SystemExit
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP or event.key == pygame.K_SPACE:  # jump
				if player.checkUnder():
					player.jumpCount = 50
			elif event.key == pygame.K_LEFT: # move left
				movements['left'] = True
			elif event.key == pygame.K_RIGHT: # move right
				movements['right'] = True
			elif event.key == pygame.K_r: # If r key pressed
				player = Character(250, 350, 50, OBSTACLES)
		
		# check if key up
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				movements['left'] = False
			if event.key == pygame.K_RIGHT:
				movements['right'] = False
	
	pygame.display.flip() # Refresh frame

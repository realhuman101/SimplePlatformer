import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))

class Character:
	def __init__(self, x, y, rect) -> None:
		self.x = x
		self.y = y
		self.rect = rect
	
	def draw(self, surface):
		surface.fill((255,255,255))

	def move(self, dir: int, amt = 5):
		# Note that dir is either the integer 1, meaning right, or -1, meaning left
		self.x = self.x + dir*amt
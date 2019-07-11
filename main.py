import random
import pygame

pygame.init()

pygame.display.set_caption('Raiden Fighters')
playerSkin = pygame.image.load('skins/player.png')
playerSkin = pygame.transform.scale(playerSkin, (50,50))
clock = pygame.time.Clock()

class Player:
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def draw(self,skin):
		screen.window.blit(skin, (self.x,self.y))

class Screen:
	def __init__(self,backgroundPath):
		self.background = pygame.image.load(backgroundPath)
		self.image_y = 0
		self.gameScreenHeight = self.background.get_rect().height
		self.gameScreenWidth = self.background.get_rect().width
		self.window = pygame.display.set_mode((self.gameScreenWidth,self.gameScreenHeight))

	def scrollScreen(self):
		relative_y = self.image_y % self.gameScreenHeight
		self.window.blit(self.background,(0,relative_y - self.gameScreenHeight))
		if relative_y < self.gameScreenHeight:
			self.window.blit(self.background, (0,relative_y))
		self.image_y += 1

player = Player(225,300,50,50)
screen = Screen('skins/bg.png')

while True:
	clock.tick(27)
	screen.scrollScreen()
	player.draw(playerSkin)
	pygame.display.update()

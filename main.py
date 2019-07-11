import random
import pygame

pygame.init()

run = True

pygame.display.set_caption('Raiden Fighters')
playerSkin = pygame.image.load('skins/player.png')
playerSkin = pygame.transform.scale(playerSkin, (50,50))
clock = pygame.time.Clock()

def eventListener():
	getEvents()
	player.keyListener()

def getEvents():
	global run
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


class Player:
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.velocity = 7

	def keyListener(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and self.x > self.velocity:
			self.x -= self.velocity
		if keys[pygame.K_RIGHT] and self.x < 450 - self.width :
			self.x += self.velocity
		if keys[pygame.K_UP] and self.y > self.velocity:
			self.y -= self.velocity
		if keys[pygame.K_DOWN] and self.y < 550 - self.height - 5:
			self.y += self.velocity

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

while run:
	clock.tick(27)
	eventListener()
	screen.scrollScreen()
	player.draw(playerSkin)
	pygame.display.update()


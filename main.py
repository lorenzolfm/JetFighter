import random
import pygame

pygame.init()

pygame.display.set_caption('Raiden Fighters')
gameScreen = pygame.display.set_mode((450,550))
background = pygame.image.load('skins/bg.png')
playerSkin = pygame.image.load('skins/player.png')
playerSkin = pygame.transform.scale(playerSkin, (50,50))
clock = pygame.time.Clock()

class Player:
	def __init__(self,x,y,widht,height):
		self.x = x
		self.y = y
		self.widht = widht
		self.height = height

	def draw(self,skin):
		gameScreen.blit(skin, (self.x,self.y))

player = Player(225,300,50,50)

while True:
	clock.tick(27)
	gameScreen.blit(background,(0,0))
	player.draw(playerSkin)
	pygame.display.update()

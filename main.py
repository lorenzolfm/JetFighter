import random
import pygame

pygame.init()

pygame.display.set_caption('Raiden Fighters')
gameScreen = pygame.display.set_mode((450,550))
background = pygame.image.load('skins/bg.png')

while True:
	gameScreen.blit(background,(0,0))
	pygame.display.update()

import random
import pygame

pygame.init()

run = True

pygame.display.set_caption('Raiden Fighters')
clock = pygame.time.Clock()


def eventListener():
	getEvents()
	player.keyListener()

def getEvents():
	global run
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == player.reloadingEvent:
			player.reloading = True
			pygame.time.set_timer(player.reloadingEvent,0)
		if event.type == enemies.respawnEvent:
			enemies.respawn = True
			pygame.time.set_timer(enemies.respawnEvent,0)

class Player:
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.velocity = 7
		self.bullets = []
		self.reloading = True
		self.reloadingEvent = pygame.USEREVENT + 1
		self.skin = pygame.image.load('skins/player.png')
		self.skin = pygame.transform.scale(self.skin, (50,50))	

	def keyListener(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			if self.reloading:
				self.bullets.append(Projectile((round(self.x + self.width // 2)), (round(self.y, + self.height // 2)),(255,0,0),7))
				self.reloading = False
				pygame.time.set_timer(self.reloadingEvent,500)
		if keys[pygame.K_LEFT] and self.x > self.velocity:
			self.x -= self.velocity
		if keys[pygame.K_RIGHT] and self.x < 450 - self.width :
			self.x += self.velocity
		if keys[pygame.K_UP] and self.y > self.velocity:
			self.y -= self.velocity
		if keys[pygame.K_DOWN] and self.y < 550 - self.height - 5:
			self.y += self.velocity

	def draw(self):
		screen.window.blit(self.skin, (self.x,self.y))

	def bulletMover(self):
		for bullet in self.bullets:
			if bullet.y < screen.gameScreenHeight and bullet.y > 0:
				bullet.y -= bullet.velocity
			else:
				self.bullets.pop(self.bullets.index(bullet))

class Enemy:
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.velocity = 5
		self.skin = pygame.image.load('skins/enemy.png')
		self.skin = pygame.transform.scale(self.skin, (50,50))

	def draw(self):
		screen.window.blit(self.skin, (self.x,self.y))

	def move(self):
		self.y += self.velocity

	def hit(self):
		pass
	

class Enemies:
	def __init__(self):
		self.enemies = []
		self.respawnEvent = pygame.USEREVENT + 2
		self.respawn = True

	def control(self):
		if self.respawn:
			self.enemies.append(Enemy(random.randrange(400),20,50,50))
			self.respawn = False
			pygame.time.set_timer(self.respawnEvent,2000)
		for enemy in self.enemies:
			if enemy.y > 550:
				self.enemies.pop(self.enemies.index(enemy))
			else:
				enemy.draw()
				enemy.move()
			#if hit:
				#pop

class Projectile:
	def __init__(self,x,y,color,velocity):
		self.x = x
		self.y = y
		self.color = color
		self.velocity = velocity
		self.radius = 6

	def draw(self):
		pygame.draw.circle(screen.window, self.color, (self.x,self.y), self.radius)

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
enemy = Enemy(100,100,50,50)
screen = Screen('skins/bg.png')
enemies = Enemies()

while run:
	clock.tick(27)
	eventListener()
	screen.scrollScreen()
	for bullet in player.bullets:
		bullet.draw()
	player.bulletMover()
	player.draw()
	enemies.control()
	pygame.display.update()


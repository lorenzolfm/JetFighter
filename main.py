import random
import pygame

pygame.mixer.pre_init(22050,-16, 2, 512)
pygame.init()

run = True
newGame = True
gameOver = False
pause = False

clock = pygame.time.Clock()
font = pygame.font.SysFont('arial',20, True)
shootSound = pygame.mixer.Sound('soundEffects/tiro.wav')
crahsSound = pygame.mixer.Sound('soundEffects/batida.wav')
upgradeSound = pygame.mixer.Sound('soundEffects/upgrade.wav')

def redrawScreen():
	screen.scrollScreen()
	displayObjects()
	displayInfo()
	pygame.display.update()

def displayObjects():
	player.draw()
	player.drawBullets()
	enemies.drawBullets()
	enemies.draw()
	enemies.drawUpgrades()

def displayInfo():
	text = font.render('Score: ' + str(player.score), 1, (0,0,0))
	screen.window.blit(text,(50,10))
	pygame.draw.rect(screen.window, (255,0,0), (200,10,50,10))
	pygame.draw.rect(screen.window, (0,255,0), (200,10,50 - ((0.25*50)*(5-player.hp)),10))

def gameControl():
	clock.tick(27)
	runStaticRoutine()
	eventListener()
	player.bulletMover()
	player.detectCollisions()
	player.addUpgrade()
	enemies.control()

def runStaticRoutine():
	global newGame,gameOver,pause
	while newGame:
		startGameRoutine()
	while gameOver:
		gameOverRoutine()
	while pause:
		pauseRoutine()

def startGameRoutine():
	staticEventListener()
	drawStaticScreen('Raiden Fighters',"'J' para jogar","'X' para sair.","'P' para pausar")

def gameOverRoutine():
	staticEventListener()
	drawStaticScreen('Fim de Jogo!',"'J' para jogar","'X' para sair.")

def pauseRoutine():
	staticEventListener('p')
	drawStaticScreen('Jogo pausado!',"'C' para continuar","'X' para sair")

def staticEventListener(*args):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			endGame()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_x:
				endGame()
			if args == ():
				if event.key == pygame.K_j:
					restartGame()
			if args:
				if event.key == pygame.K_c:
					pause = False

def endGame():
	global run,gameOver,newGame,pause
	run = gameOver = newGame = pause = False

def restartGame():
	global gameOver,newGame

	gameOver = False
	newGame = False
	player.hp = 5
	player.score = 0
	player.x = 212
	player.y = 400
	enemies.enemies.clear()
				
def drawStaticScreen(*strings):
	screen.window.fill((99, 78, 78))
	width = 0
	height = 10
	for string in strings:
		text = font.render(string,1,(255, 87, 51))
		screen.window.blit(text,((screen.width/2)-70,height))
		height += 100
	screen.window.blit(player.skin,(212,400))
	pygame.display.update()

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
		if event.type == player.hitEvent:
			player.hitCooldown = True
			pygame.time.set_timer(player.hitEvent,0)
		if event.type == enemies.respawnEvent:
			enemies.respawn = True
			pygame.time.set_timer(enemies.respawnEvent,0)
		if event.type == enemy.deleteUpgradeEvent:
			for upgrade in enemies.upgrades:
				upgrade.bool = False
				enemies.upgrades.pop(enemies.upgrades.index(upgrade))
				pygame.time.set_timer(enemy.deleteUpgradeEvent,0)

class Player:
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.velocity = 7
		self.hp = 5
		self.score = 0
		self.reloadSpeed = 1000
		self.bullets = []
		self.reloading = True
		self.hitCooldown = True
		self.reloadingEvent = pygame.USEREVENT + 1
		self.hitEvent = pygame.USEREVENT +2
		self.skin = pygame.image.load('skins/player.png')
		self.skin = pygame.transform.scale(self.skin, (50,50))

	def keyListener(self):
		global pause
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			if self.reloading:
				self.bullets.append(Projectile((round(self.x + self.width // 2)), (round(self.y, + self.height // 2)),(255,0,0),7))
				self.reloading = False
				pygame.mixer.Sound.play(shootSound)
				pygame.time.set_timer(self.reloadingEvent,player.reloadSpeed)
		if keys[pygame.K_LEFT] and self.x > self.velocity:
			self.x -= self.velocity
		if keys[pygame.K_RIGHT] and self.x < 450 - self.width :
			self.x += self.velocity
		if keys[pygame.K_UP] and self.y > self.velocity:
			self.y -= self.velocity
		if keys[pygame.K_DOWN] and self.y < 550 - self.height - 5:
			self.y += self.velocity
		if keys[pygame.K_p]:
			pause = True

	def draw(self):
		screen.window.blit(self.skin, (self.x,self.y))
		self.hitbox = (self.x+13,self.y,25,50)

	def bulletMover(self):
		for bullet in self.bullets:
			if bullet.y < screen.height and bullet.y > 0:
				bullet.y -= bullet.velocity
			else:
				self.bullets.pop(self.bullets.index(bullet))

	def detectCollisions(self):
		for enemy in enemies.enemies:
			if self.hitbox[1] <= enemy.hitbox[1] + enemy.hitbox[3] and self.hitbox[1] + self.hitbox[3] >= enemy.hitbox[1]:
				if self.hitbox[0] <= enemy.hitbox[0] + enemy.hitbox[2] and self.hitbox[0] + self.hitbox[2] >= enemy.hitbox[0]:
					if enemy.visible:
						player.hit()
			for bullet in enemy.bullets:
				if self.hitbox[1] <= bullet.y + bullet.radius and self.hitbox[1] + self.hitbox[3] >= bullet.y - bullet.radius:
					if self.hitbox[0] <= bullet.x + bullet.radius and self.hitbox[0] + self.hitbox[2] >= bullet.x - bullet.radius:
						player.hit()

	def hit(self):
		global gameOver
		if self.hitCooldown and self.hp >= 2:
			self.hitCooldown = False
			self.hp -= 1
			if player.reloadSpeed < 1000:
				player.reloadSpeed += 200
			pygame.mixer.Sound.play(crahsSound)
			pygame.time.set_timer(self.hitEvent,500)
		elif self.hitCooldown and self.hp < 2:
			gameOver = True


	def addUpgrade(self):
		for upgrade in enemies.upgrades:
			if upgrade.y + upgrade.height > self.y and upgrade.y < self.y + self.height and upgrade.x < self.x + self.width and upgrade.x + upgrade.width > self.x:
				enemies.upgrades.pop(enemies.upgrades.index(upgrade))
				if upgrade.heal:
					self.hp += 1
					upgrade.bool = False
				else:
					if player.reloadSpeed > 200:
						player.reloadSpeed -= 200
					upgrade.bool = False

	def drawBullets(self):
		for bullet in self.bullets:
			bullet.draw()

class Enemy:
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.velocity = 5
		self.bullets = []
		self.visible = True
		self.hitbox = (self.x+13,self.y,25,50)
		self.skin = pygame.image.load('skins/enemy.png')
		self.skin = pygame.transform.scale(self.skin, (50,50))
		self.deleteUpgradeEvent = pygame.USEREVENT + 3
		if random.randrange(10) <= 3:
			self.hasUpgrade = True
		else:
			self.hasUpgrade = False

	def draw(self):
		if self.visible:
			screen.window.blit(self.skin, (self.x,self.y))
			self.hitbox = (self.x+13,self.y,25,50)

	def move(self):
		self.y += self.velocity

	def detectCollisions(self):
		for bullet in player.bullets:
			if self.visible:
				if bullet.y + bullet.radius < self.hitbox[1] + self.hitbox[3] and bullet.y - bullet.radius > self.hitbox[1] and bullet.x + bullet.radius > self.hitbox[0] and bullet.x - bullet.radius < self.hitbox[0] + self.hitbox[2]:
					player.bullets.pop(player.bullets.index(bullet))
					self.visible = False
					player.score += 1
					if self.hasUpgrade and len(enemies.upgrades) < 1 and not enemies.bool:
						enemies.bool = False
						enemies.upgrades.append(Upgrade(self.x,self.y))
						pygame.time.set_timer(self.deleteUpgradeEvent,3000)
	
	def shoot(self):
		if self.visible:
			if random.randrange(100) < 3:
				self.bullets.append(Projectile((round(self.x + self.width // 2)), (round(self.y, + self.height // 2)),(255,0,0),8))
		for bullet in self.bullets:
			if bullet.y < screen.height and bullet.y > 0:
				bullet.y += bullet.velocity
			else:
				self.bullets.pop(self.bullets.index(bullet))

class Enemies:
	def __init__(self):
		self.enemies = []
		self.upgrades = []
		self.respawnEvent = pygame.USEREVENT + 2
		self.respawn = True
		self.bool = False

	def control(self):
		if self.respawn:
			self.enemies.append(Enemy(random.randrange(400),20,50,50))
			self.respawn = False
			pygame.time.set_timer(self.respawnEvent,1500)
		for enemy in self.enemies:
			if enemy.y > 550:
				self.enemies.pop(self.enemies.index(enemy))
			else:
				enemy.move()
				enemy.detectCollisions()
				enemy.shoot()

	def draw(self):
		for enemy in self.enemies:
			enemy.draw()

	def drawBullets(self):
		for enemy in self.enemies:
			for bullet in enemy.bullets:
				bullet.draw()

	def drawUpgrades(self):
		for upgrade in self.upgrades:
			upgrade.draw()

class Projectile:
	def __init__(self,x,y,color,velocity):
		self.x = x
		self.y = y
		self.color = color
		self.velocity = velocity
		self.radius = 6
	
	def draw(self):
		pygame.draw.circle(screen.window, self.color, (self.x,self.y), self.radius)

class Upgrade:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.width = 12
		self.height = 12
		if random.randrange(10) < 5 and player.hp < 5:
			self.heal = True
		else:
			self.heal = False
		self.deleteUpgrade = True
		pygame.mixer.Sound.play(upgradeSound)
		
	def draw(self):
		if self.heal:
			pygame.draw.rect(screen.window,(0,255,0),(self.x+20,self.y,self.width,self.height),0)
		else:
			pygame.draw.rect(screen.window,(0,0,255),(self.x+20,self.y,self.width,self.height),0)

class Screen:
	def __init__(self,backgroundPath):
		self.background = pygame.image.load(backgroundPath)
		self.image_y = 0
		self.height = self.background.get_rect().height
		self.width = self.background.get_rect().width
		self.window = pygame.display.set_mode((self.width,self.height))
		pygame.display.set_caption('Raiden Fighters')

	def scrollScreen(self):
		relative_y = self.image_y % self.height
		self.window.blit(self.background,(0,relative_y - self.height))
		if relative_y < self.height:
			self.window.blit(self.background, (0,relative_y))
		self.image_y += 1

player = Player(225,300,50,50)
enemy = Enemy(100,100,50,50)
screen = Screen('skins/bg.png')
enemies = Enemies()

while run:
	gameControl()
	redrawScreen()

pygame.quit()
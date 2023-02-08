import pygame, time
from utils import *

class Player(pygame.sprite.Sprite):

	def __init__(self):
		# init super class
		super().__init__()

		# initialize spaceship
		self.init_spaceship()

		# score, life
		self.score = 0
		self.lifes = 3

		# layer field is to indicate the z index, for example we want the player over the planet
		self._layer = 1

		# collision sound
		self.burst_sound = pygame.mixer.Sound("sounds/burst.ogg")

	# called each tick
	def update(self):
		# if we are death no action is allowed
		if self.status == PLAYER_STATUS_DEATH:
			return # this is to avoid do more actions
		# if we are landing over a planet then the spaceship is moved automaticly to the center
		if self.status == PLAYER_STATUS_LANDING:
			self.land()
			return # this is to avoid do more actions
		# if we are collisioned then we restart the image
		elif self.status == PLAYER_STATUS_COLLIDED:
			time.sleep(2) # wait 2 seconds to show correctly the burst
			self.init_spaceship()

		keys = pygame.key.get_pressed()

		# when key_up is pressed then go up
		if keys[pygame.K_UP]:
			self.up()
		# when key_down is pressed then go down
		elif keys[pygame.K_DOWN]:
			self.down()
		else:
			self.speed = 5 # restart acceleration when no key is pressed
	
	def up(self):
		self.rect.y -= self.speed
		self.speed *= 1.1 # speed up

		# check if position is valid (top margin)
		if self.rect.y < 0:
			self.rect.y = 0
			self.speed = 5

	def down(self):
		self.rect.y += self.speed
		self.speed *= 1.1 # speed up

		# check if position is valid (bottom margin)
		if self.rect.y + self.rect.height >= SCREEN_HEIGHT:
			self.rect.y = SCREEN_HEIGHT - self.rect.height - 1
			self.speed = 5

	def land (self):
		# if we are on top we down to the center
		if self.rect.y < SCREEN_HEIGHT // 2 - self.rect.height:
			self.rect.y += 1
		# if we are on bottom we up to the center
		elif self.rect.y > SCREEN_HEIGHT // 2 - self.rect.height:
			self.rect.y -= 1
		# if we are forwarding to planet, in pixel 100 we rotate and forward the spaceship
		elif self.rect.x == 400:
			self.image = pygame.transform.rotate(self.image, 180)
			self.rect.x += 5 # if we dont forward we keep rotating in loop
		# if we are on left we go to right
		elif self.rect.x < SCREEN_WIDTH * 3 / 4 + self.rect.width:
			self.rect.x += 5
		# in other case we are landed correctly
		else:
			self.status = PLAYER_STATUS_LANDED

	def checkCollision(self, asteroids):
		# when collision the asteroid is removed and return true (when we are flying obviously)
		if self.status == PLAYER_STATUS_FLYING and pygame.sprite.spritecollide(self, asteroids, True):
         # sound of collision
			self.burst_sound.play()

			# update lifes and status
			self.lifes -= 1
			if self.lifes > 0:
				self.status = PLAYER_STATUS_COLLIDED
			else:
				self.status = PLAYER_STATUS_DEATH

			# collision image
			self.image = pygame.image.load("images/burst.png").convert()
			self.image.set_colorkey(BLACK)

	def init_spaceship(self):
		# load image with transparent background
		self.image = pygame.image.load("images/spaceship.png").convert_alpha()

		# this define a rect that is a rectange with size and positions of the player image
		self.rect = self.image.get_rect()

		# spaceship mode
		self.status = PLAYER_STATUS_FLYING

		# initial speed and position
		self.speed = 5
		self.rect.x = 10
		self.rect.y = (SCREEN_HEIGHT // 2) - self.rect.height # start in the middle

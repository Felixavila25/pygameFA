import pygame
from utils import *

class Asteroid(pygame.sprite.Sprite):

   def __init__(self, position, size, speed):
      # init super class
      super().__init__()

      # load image with transparent background
      image = pygame.image.load("images/asteroid.png").convert_alpha()
      self.image = pygame.transform.scale(image, (size, size)) # scale image to the specified asteroid size

      # this define a rect that is a rectange with size and positions of the asteroid image
      self.rect = self.image.get_rect()

      # speed and initial position
      self.speed = speed
      self.rect.x = position.x
      self.rect.y = position.y

	# called each tick
   def update(self):
      # go to the left
      self.rect.x -= self.speed

import pygame
from utils import *

class Planet(pygame.sprite.Sprite):

   def __init__(self, type):
      # init super class
      super().__init__()

      # load image with transparent background
      image = pygame.image.load("images/planet_" + str(type) + ".png").convert_alpha()
      self.image = pygame.transform.scale(image, (900, 900))

      # this define a rect that is a rectange with size and positions of the planet image
      self.rect = self.image.get_rect()

      # initial position
      self.rect.x = SCREEN_WIDTH
      self.rect.y = -100

	# called each tick
   def update(self):
      # go to the left
      if self.rect.x > SCREEN_WIDTH * 3 / 4:
         self.rect.x -= 2

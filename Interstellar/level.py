import pygame, sys, time
from asteroid import Asteroid
from planet import Planet
from random import randrange
from utils import *

GENERATE_ASTEROID_EVENT = pygame.USEREVENT
APPEAR_PLANET_EVENT = pygame.USEREVENT + 1

def generate_random_asteroid(level):
   random_speed = randrange(level * 2, level * 4)
   random_size = randrange(30, level * 50)
   random_y = randrange(SCREEN_HEIGHT - random_size)
   return Asteroid(pygame.math.Vector2(SCREEN_WIDTH, random_y), random_size, random_speed)
         
class Level:
   def __init__(self, level, player):
      # save player
      self.player = player

      # define sprites
      self.all_asteroid_list = pygame.sprite.Group()
      self.all_sprite_list = pygame.sprite.LayeredUpdates()
      self.all_sprite_list.add(self.player)

      # define background, music and difficulty
      bg_img = pygame.image.load("images/level_" + str(level) + ".jpg")
      self.bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
      self.music = pygame.mixer.Sound("sounds/level_" + str(level) + ".ogg")
      self.music.play(-1).set_volume(0.2)
      self.level = level

      # custom event to generate an asteroid each x seconds
      pygame.time.set_timer(GENERATE_ASTEROID_EVENT, 1000 // self.level) # when level is bigger then generate more asteroids (1000 miliseconds / level)
      pygame.time.set_timer(APPEAR_PLANET_EVENT, 60000) # after 60 seconds appear the planet (60000 miliseconds)

   def process_events(self):
      # listen events in game (mouse-position, buttons, ...)
      for event in pygame.event.get():
         # when close the exit button
         if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         # when a generate asteroid event is launched
         elif event.type == GENERATE_ASTEROID_EVENT:
            # when an asteroid is generated the score is incremented taking into account the level
            self.player.score += self.level
            asteroid = generate_random_asteroid(self.level)
            self.all_asteroid_list.add(asteroid)
            self.all_sprite_list.add(asteroid)
         # when appear planet is launched
         elif event.type == APPEAR_PLANET_EVENT:
            # when the planet appears we increment the score (in this point the level is finished, it is no necessary wait to land)
            self.player.score += self.level * 10
            # change status to landing
            self.player.status = PLAYER_STATUS_LANDING
            # no more asteroids or planet events will be generated
            pygame.time.set_timer(GENERATE_ASTEROID_EVENT, 0)
            pygame.time.set_timer(APPEAR_PLANET_EVENT, 0) 
            self.all_sprite_list.add(Planet(self.level))

   def run(self):
      # if we are death then game over
      if self.player.status == PLAYER_STATUS_DEATH:
         self.music.stop()
         return LEVEL_STATUS_GAME_OVER
      # if we have landed then level completed and init the spaceship position
      if self.player.status == PLAYER_STATUS_LANDED:
         self.music.stop()
         time.sleep(2) # wait 2 seconds to show correctly the burst
         self.player.init_spaceship()
         return LEVEL_STATUS_COMPLETED
      # when we are collided we clean all asteroids
      elif self.player.status == PLAYER_STATUS_COLLIDED:
         # when collided we update the score with -5 points
         self.player.score = self.player.score - 5 if self.player.score >= 5 else 0
         for sprite in self.all_asteroid_list:
            sprite.kill()
   
      # update positions
      self.all_sprite_list.update() # this call update method in all sprites of the list (asteroids, player and planet)
      self.player.checkCollision(self.all_asteroid_list) # check collisions

      return LEVEL_STATUS_PLAYING

   def display(self, screen):
      # draw background image
      screen.blit(self.bg_img, (0, 0))

      # draw sprites 
      self.all_sprite_list.draw(screen)

      # draw level, lifes and score
      draw_text(screen, "Level: " + str(self.level), 25, (SCREEN_WIDTH - 150, 10))
      draw_text(screen, "Lifes: " + str(self.player.lifes), 25, (SCREEN_WIDTH - 150, 40))
      draw_text(screen, "Score: " + str(self.player.score), 25, (SCREEN_WIDTH - 150, 70))

      # load draws
      pygame.display.flip()
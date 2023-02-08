import pygame
from database import *
from level import Level
from player import Player
from utils import *
from score_screen import Score_Screen
	 
if __name__ == '__main__':
	# init database
	init_database()

	# initialize pygame library
	pygame.init()

	# screen options
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()

	level_idx = 1
	while level_idx <= 3:
		# show home
		if level_idx == 1:
			# create player
			player = Player()
			show_home_screen(screen)

		# show screen with confirmation to continue (if no press enter after 20 seconds then go to home)
		if not show_go_screen(screen, level_idx):
			level_idx = 1 # this is for start the loop again in 1
			continue # this is for go to the next iteration of the loop

		level = Level(level_idx, player)
		levelStatus = LEVEL_STATUS_PLAYING
		while levelStatus == LEVEL_STATUS_PLAYING:
			level.process_events() # process the posible events from pygame
			levelStatus = level.run() # run the logic of the game
			level.display(screen) # paint the game
			clock.tick(60) # 60fps

		if levelStatus == LEVEL_STATUS_GAME_OVER:
			show_game_over_screen(screen, player)
			level_idx = 3

		if level_idx == 3:
			Score_Screen().show(screen, player)
			level_idx = 1 # for restart the game
		else:
			level_idx += 1 # for continue to the next level
		
		


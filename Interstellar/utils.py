import pygame, time
from database import *

# settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# level status
LEVEL_STATUS_PLAYING = 0
LEVEL_STATUS_GAME_OVER = 1
LEVEL_STATUS_COMPLETED = 2

# player status
PLAYER_STATUS_FLYING = 0
PLAYER_STATUS_COLLIDED = 1
PLAYER_STATUS_LANDING = 2
PLAYER_STATUS_LANDED = 3
PLAYER_STATUS_DEATH = 4

def draw_text(screen, text, size, position, color = WHITE):
	font = pygame.font.SysFont("serif", size)
	text_screen = font.render(text, True, color)
	screen.blit(text_screen, position)

def show_home_screen(screen):
	accept_sound = pygame.mixer.Sound("sounds/accept.ogg")
	screen.fill(BLACK)
	draw_text(screen, "INTERSTELLAR", 80, (SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 4))
	draw_text(screen, "Solo tienes una misión: DIVIERTETE!", 30, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
	draw_text(screen, "Félix Ávila Jiménez presents:", 30, (SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 6))
	draw_text(screen, "Press enter to continue", 20, (SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT * 3/4))
	pygame.display.flip()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				accept_sound.play()
				return

def show_go_screen(screen, level):
	initial_time = time.time()
	accept_sound = pygame.mixer.Sound("sounds/accept.ogg")

	while True:
		remaining_time = 30 - int((time.time() - initial_time) % 60)
		screen.fill(BLACK)
		draw_text(screen, "INTERSTELLAR", 80, (SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 4))
		draw_text(screen, "Level " + str(level), 30, (SCREEN_WIDTH // 2 - 45, SCREEN_HEIGHT // 2))
		draw_text(screen, "Press enter to start (" + str(remaining_time) + "s)", 20, (SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT * 3/4))
		pygame.display.flip()

		if remaining_time <= 0:
			return False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				accept_sound.play()
				return True

def show_game_over_screen(screen, player):
	accept_sound = pygame.mixer.Sound("sounds/accept.ogg")
	screen.fill(BLACK)
	draw_text(screen, "GAME OVER", 80, (SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT // 4))
	draw_text(screen, "You died!", 25, (SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2.5), RED)
	draw_text(screen, "Total score", 30, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))
	draw_text(screen, "{:04d}".format(player.score), 30, (SCREEN_WIDTH // 2 - 35, SCREEN_HEIGHT // 2 + 40))
	draw_text(screen, "Press enter to continue", 20, (SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT * 3/4))
	pygame.display.flip()
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			# when some key is pressed then go out of the game over screen
			elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
				accept_sound.play()
				return

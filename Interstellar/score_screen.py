import pygame
from database import *
from utils import *
import pygame_textinput

class Score_Screen():
   
   def __init__(self):
      # Create Score Input-object (it is used to write the name of the user)
      font = pygame.font.SysFont("serif", 50)
      manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 3)
      self.score_input = pygame_textinput.TextInputVisualizer(manager=manager, font_object=font)
      self.score_input.font_color = WHITE
      self.score_input.cursor_color = WHITE

      # create connection for get scores and insert the new score
      self.conn = create_connection()

   def draw_score_row(self, screen, position, score):
      draw_text(screen, str(position + 1) + ". " + score[1], 50, (SCREEN_WIDTH // 2.5 - 50, SCREEN_HEIGHT // 3 + position * 60))
      draw_text(screen, "{:04d}".format(score[2]), 50, (SCREEN_WIDTH // 2.5 + 220, SCREEN_HEIGHT // 3 + position * 60))

   def draw_score_table(self, screen, scores, player):
      player_is_in_table = False
      best_5_scores = scores
      
      # if there is less than 5 scores on database then show user = --- and score = 0
      while len(best_5_scores) < 5:
         best_5_scores.append((-1, "---", 0))

      for i in range(5):
         # if the player score is better than the current best score then show the input for the user
         if player.score > best_5_scores[i][2] and not player_is_in_table:
            self.draw_score_row(screen, i, (-1, "", player.score))
            screen.blit(self.score_input.surface, (SCREEN_WIDTH // 2.5, SCREEN_HEIGHT // 3 + i * 60))
            player_is_in_table = True # now we set this to true to avoid show the input more than once
            # imagine that the player score is better than the first 2 scores, then we enter in this conditional 2 times
         elif player_is_in_table: # if player is in table the i have is one position over the next best score, because we have incremented i when we add the player score
            self.draw_score_row(screen, i, best_5_scores[i - 1])
         else:
            self.draw_score_row(screen, i, best_5_scores[i])

      return player_is_in_table

   def show(self, screen, player):
      accept_sound = pygame.mixer.Sound("sounds/accept.ogg")
      # connect to database and get scores
      scores = get_scores(self.conn)

      while True:
         screen.fill(BLACK)
         events = pygame.event.get()

         # Feed it with events every frame
         self.score_input.update(events)

         draw_text(screen, "BEST SCORES", 80, (SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT // 8))
         player_is_in_table = self.draw_score_table(screen, scores, player)
               
         if player_is_in_table:
            if len(self.score_input.value) < 3:
               draw_text(screen, "Write your name", 20, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT * 3/4 + 50))
            else:
               draw_text(screen, "Press enter to save and restart", 20, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT * 3/4 + 50))
         else:
            draw_text(screen, "Press enter to restart the game", 20, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT * 3/4 + 50))

         for event in events:
            if event.type == pygame.QUIT:
               exit()

            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
               if len(self.score_input.value) == 3:
                  accept_sound.play()
                  insert_score(self.conn, (self.score_input.value, player.score))
                  return 
               elif not player_is_in_table:
                  accept_sound.play()
                  return

         pygame.display.update()

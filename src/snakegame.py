import pygame
import sys
from time import sleep

from button import Button
from player import Player
from fruit import Fruit
from scorelabel import Scorelabel
from highscore import Highscore
from bonus_fruit import BonusFruit


class Game:
    """Main gameclass for the Snake Game."""

    def __init__(self):
        """Initialize game attributes."""
        
        pygame.init()
        self.clock = pygame.time.Clock()   
        self.fps = 60
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Snakegame!")      
        self.points = 0
        self.score = 0

        self.play_button = Button(self, "Play!")
        self.player = Player(self)
        self.scorelabel = Scorelabel(self)
        self.player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        self.fruit = Fruit(self)
        self.highscore = Highscore(self)
        self.bonus_fruit = BonusFruit(self)

        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/intro.mp3'))   
        self.title_screen = pygame.image.load("images/title_screen.png")  
        self.title_screen_rect = self.title_screen.get_rect()
        self.score_screen = pygame.image.load("images/score_screen.png")
        self.score_screen_rect = self.score_screen.get_rect()

        self.game_active = False
        self.fruit_visible = True
        self.bonus_fruit_visible = False
        self.score_screen_visible = False
        self.new_high_score = False

        self.scorelabel.prep_score(self.score)
        self.key_buffer = []
        
    def run_game(self):  
        #Main game loop.    
        while True:
            self._check_events()
            if self.game_active:
                self.player.update()
                self.scorelabel.prep_score(self.score)
                self.check_fruit()
                self.bonus_fruit.check_bonus()
            self._update_screen()  
            self.clock.tick(self.fps/20)
            self.key_buffer = []

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            if self.game_active:
                if event.type == pygame.KEYDOWN and len(self.key_buffer) == 0:
                    if event.key == pygame.K_UP and not self.player.direction == "s":
                        self.player.direction = "n"
                        self.key_buffer.append("n")
                    if event.key == pygame.K_DOWN and not self.player.direction == "n":
                        self.player.direction = "s"
                        self.key_buffer.append("s")
                    if event.key == pygame.K_LEFT and not self.player.direction == "e":
                        self.player.direction = "w"
                        self.key_buffer.append("w")
                    if event.key == pygame.K_RIGHT and not self.player.direction == "w":
                        self.player.direction = "e"
                        self.key_buffer.append("e")
                            
    def _check_play_button(self, mouse_pos):
        """Start a new game if the player clicks Play."""
        if not self.game_active:
            if self.play_button.rect.collidepoint(mouse_pos):
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/button.mp3'))
                sleep(1)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound/playing.mp3'))
                self.player.reset_stats()
                self.game_active = True
                pygame.mouse.set_visible(False)
                self.new_high_score = False
                self.bonus_fruit_visible = False

    def hit(self):
        #Actions when the snake collides with itself.
        pygame.mixer.Channel(0).stop()
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('sound/end.mp3'))
        sleep(0.2)
        pygame.mixer.Channel(3).play(pygame.mixer.Sound('sound/end_2.mp3'))
        sleep(0.2)
        self.game_active = False
        self.score_screen_visible = True

    def check_points(self):
        #Raise speed via fps, when a certain amount of pickups is collected.
        if self.points % 6 == 0:
            self.fps += 10
            pygame.mixer.Channel(4).play(pygame.mixer.Sound('sound/speedup.mp3'))

    def check_fruit(self):
        if self.game_active:
            self.fruit_rect = pygame.Rect(self.fruit.x, self.fruit.y, self.fruit.width, self.fruit.height)
            self.player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)

            if self.player_rect.colliderect(self.fruit_rect):
                self.get_points_value()         
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound/pickup_1.mp3'))
                self.fruit_visible = False
                self.fruit.get_new_fruit()
                self.player.add_segment()
                self.points += 1
                self.check_points()

    def get_points_value(self):
        if self.points == 0:
            self.player.head_color = self.fruit.fruit_color

        if self.points > 0:
            self.player.body_color = self.fruit.fruit_color

        if self.points < 12:
            self.score += 100
        elif self.points >= 12 and self.points < 24:
            self.score += 200
        elif self.points >= 24 and self.points < 36:
            self.score += 300
        elif self.points >= 36 and self.points < 48:
            self.score += 400
        elif self.points >= 48:
            self.score += 500  

    def end_screen(self):
        #Shows the endscreen with the highscore and the play-button.
        self.screen.blit(self.score_screen, self.score_screen_rect)
        self.check_high_score()
        self.highscore.prep_high_score()
        self.play_button = Button(self, "Play again?")
        self.play_button.draw_button()
        pygame.mouse.set_visible(True)

    def check_high_score(self):
        if self.points > 1:
            if self.score > self.highscore.high_score:
                self.highscore.high_score = self.score
                self.new_high_score = True               
            self.highscore.prep_high_score()
            
            if self.new_high_score == True:
                self.highscore.prep_grats()

    def _update_screen(self):
        self.screen.fill((0, 0, 0))
        if not self.game_active and self.score_screen_visible:  
            self.end_screen()

        if not self.game_active and self.score_screen_visible == False:      
            self.screen.blit(self.title_screen, self.title_screen_rect)
            self.play_button.draw_button()
            pygame.mouse.set_visible(True)

        if self.game_active:
            self.scorelabel.draw_score() 
            if self.fruit_visible:
                self.fruit.draw_fruit()
            if self.bonus_fruit_visible:
                self.bonus_fruit.draw_bonus_fruit()
            self.player.drawme()   

        pygame.display.flip()

pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()


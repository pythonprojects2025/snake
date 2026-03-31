import pygame
from random import randint


class Fruit:
    """This class generates the randomly spawned collectible."""

    def __init__(self, game):
        """Initialize fruit attributes."""
        
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.player = game.player
        self.scorelabel = game.scorelabel
        self.width = 20
        self.height = 20
        self.x = randint(0, self.screen_rect.right - 20)
        self.y = randint(0, self.screen_rect.bottom - 20)
        self.fruit_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.fruit_color = (randint(41, 255), randint(41, 255), randint(41, 255))
        self.bonus_fruit = False

    def get_new_fruit(self):
        #Build a pickup with random position.
        self.fruit_color = (randint(41, 255), randint(40, 255), randint(41, 255))
        self.x = randint(0, self.screen_rect.right - 20)
        self.y = randint(0, self.screen_rect.bottom - 20)
        self.fruit_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        place = self.check_space() and self.check_scorelabel() and self.check_bonus()
        if place:
            self.draw_fruit()
            self.game.fruit_visible = True
        else:
            self.get_new_fruit()

    def check_space(self):
        #Prevent pickup from spawning in the snake.
        l = len(self.game.player.seg_rects)
        for i in range(0, l):               
            if self.fruit_rect.colliderect(self.game.player.seg_rects[i]):
                return False
        return True

    def check_scorelabel(self):
        #Prevent pickup from spawning in the score area.
        labelrect = self.scorelabel.score_rect
        if not self.fruit_rect.colliderect(labelrect):
            return True
    
    def check_bonus(self):
        #Prevent pickup from spawning in an existing bonus pickup.
        if not self.fruit_rect.colliderect(self.game.bonus_fruit.rect):
            return True
         
    def draw_fruit(self):
        if not self.bonus_fruit:
            pygame.draw.rect(self.screen, self.fruit_color, (self.fruit_rect))
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x + 14, self.y + 2, 4, 4))
       
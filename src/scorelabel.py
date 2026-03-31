import pygame.font


class Scorelabel:
    """This class gets the score and prepares the image to blit."""

    def __init__(self, game):
        """Initialize score attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.score_rect = pygame.rect.Rect(0, 0, 0, 0)
        
        # Font settings
        self.label_color = (0, 0, 0)   
        self.text_color = (30, 230, 230)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score(0)
       
    def prep_score(self, score):
        # Get a rendered image with the score.
        self.score = score
        score_str = f"Score: {self.score}"
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.label_color)
        
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def draw_score(self):
        self.screen.blit(self.score_image, self.score_rect)
       


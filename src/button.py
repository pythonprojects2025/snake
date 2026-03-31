import pygame.font


class Button:
    """A class to build buttons for the game."""

    def __init__(self, game, msg):
        """Initialize button attributes."""

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.width = 160
        self.height = 80
        self.button_color = (96, 21, 95)

        # Set the dimensions and properties of the button.
        if msg == "Play!":
            self.width, self.height = 160, 80
            self.button_color = (96, 21, 95)
        elif msg == "Play again?":
            self.width, self.height = 300, 80
            self.button_color = (55, 23, 100)

        self.text_color = (255, 55, 255)
        self.font = pygame.font.SysFont(None, 60)

        # Build the button's rect object and set position.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if msg == "Play!":
            self.width, self.height = 160, 80      
            self.rect.center = self.screen_rect.center
        elif msg == "Play again?":
            self.rect.x = 20
            self.rect.y = 300
        
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # Get a rendered image of the buttontext.
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.border = pygame.draw.rect(self.screen, (255, 255, 255), (self.rect), 2)
        self.screen.blit(self.msg_image, self.msg_image_rect)
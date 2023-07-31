import pygame

class Results:
    """ A class to manage the results of the game """

    def __init__(self, ai_game):
        """ Create a instance of results """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.font = pygame.font.SysFont(None, 48)

        self.press_p_text = self.font.render("Press p to start", True,
                                             self.settings.text_color)
        self.press_p_rect = self.press_p_text.get_rect()
        self.press_p_rect.centerx = self.screen_rect.centerx
        self.press_p_rect.centery = 1.25 * self.screen_rect.centery

        self.prep()

    def prep(self, first_line="", second_line=""):
        """ Prepare the text """
        self.first = self.font.render(first_line, True, self.settings.text_color)
        self.first_rect = self.first.get_rect() 
        self.first_rect.centerx = self.screen_rect.centerx
        self.first_rect.centery = 0.5 * self.screen_rect.centery

        self.second = self.font.render(second_line, True, self.settings.text_color)
        self.second_rect = self.second.get_rect() 
        self.second_rect.centerx = self.screen_rect.centerx
        self.second_rect.centery = 0.75 * self.screen_rect.centery

    def update(self):
        """ Blit the text on the screen """
        self.screen.blit(self.first, self.first_rect)
        self.screen.blit(self.second, self.second_rect)
        self.screen.blit(self.press_p_text, self.press_p_rect)

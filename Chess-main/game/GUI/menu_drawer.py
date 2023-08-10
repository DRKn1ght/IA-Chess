import pygame
from settings import Settings
from GUI.draw_utils import make_button_surface, make_gradient_background

BACKGROUND_COLOR_OUTER = pygame.Color('#003366')
BACKGROUND_COLOR_INNER = pygame.Color('#005b96')
BUTTON_COLOR = pygame.Color('#FFA469')

class Menu_Drawer:
    button_font_size = 25
    header_font_size = 90

    def __init__(self, window):
        self.settings = Settings()

        self.window = window
        self.button_font = pygame.font.SysFont('Comic Sans MS', self.button_font_size)
        self.header_font = pygame.font.SysFont('Calibri', self.header_font_size, bold=True)
        self.background_surface = make_gradient_background(BACKGROUND_COLOR_OUTER, BACKGROUND_COLOR_INNER)

        self.player_vs_ai_button = None
        self.player_vs_ai_button_surface = None
        self.ai_vs_ai_button = None
        self.ai_vs_ai_button_surface = None
        self.quit_button = None
        self.quit_button_surface = None

        self.top = self.__make_top()

        self.__make_buttons()

    def draw(self):
        self.window.blit(self.background_surface, (0, 0))
        self.window.blit(self.quit_button_surface, (0, 0))
        self.window.blit(self.player_vs_ai_button_surface, (0, 0))
        self.window.blit(self.ai_vs_ai_button_surface, (0, 0))
        self.window.blit(self.top, (0, 0))

        pygame.display.update()
    
    def __make_buttons(self):
        width = self.settings.screen_width // 4
        height = self.settings.screen_height // 8

        x = self.settings.screen_width // 2 - (width // 2)
        y = self.settings.screen_height // 2 - 80
        self.player_vs_ai_button = pygame.Rect(x, y, width, height)
        self.player_vs_ai_button_surface = \
            make_button_surface(self.button_font, self.player_vs_ai_button, "Player vs AI", BUTTON_COLOR)

        y += 1.5*height
        self.ai_vs_ai_button = pygame.Rect(x, y, width, height)
        self.ai_vs_ai_button_surface = \
            make_button_surface(self.button_font, self.ai_vs_ai_button, "IA vs IA", BUTTON_COLOR)

        y += 1.5*height
        self.quit_button = pygame.Rect(x, y, width, height)
        self.quit_button_surface = \
            make_button_surface(self.button_font, self.quit_button, "Quit", BUTTON_COLOR)
        
    def __make_top(self):
        result = pygame.Surface((self.settings.screen_width, self.settings.screen_width), pygame.SRCALPHA, 32)
        text_surface = self.header_font.render("Supimpadrez", True, pygame.Color('#FFFFFF'))
        text_rect = text_surface.get_rect()

        top_surface = pygame.Surface(((text_rect.width), text_rect.height), pygame.SRCALPHA, 32)
        top_rect = top_surface.get_rect()
        top_rect.center = (self.settings.screen_width // 2, 90)
        text_rect.center = (((top_rect.width) // 2), top_rect.height // 2 + 12)

        top_surface.blit(text_surface, text_rect)
        result.blit(top_surface, top_rect)

        return result
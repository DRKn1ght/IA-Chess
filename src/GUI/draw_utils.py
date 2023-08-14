import pygame
from Game.settings import Settings

settings = Settings()

def make_button_surface(font, button, text, color):
    result = pygame.Surface((settings.screen_width, settings.screen_height), pygame.SRCALPHA, 32)
    pygame.draw.rect(result, color, button)
    text_surface = font.render(text, True, pygame.Color('#ffffff'))
    text_rect = text_surface.get_rect()
    text_rect.center = (button.centerx, button.centery)
    result.blit(text_surface, text_rect)

    return result

# creates a tiny surface, fills it with 2 colors and stretches it
# using pygame.transform.smoothscale() to achieve a color gradient
def make_gradient_background(color1, color2):
    result = pygame.Surface((4, 4))

    result.fill(color1)
    pygame.draw.rect(result, color2, pygame.Rect(1, 1, 2, 2))
    result = pygame.transform.smoothscale(result, (settings.screen_width, settings.screen_height))

    return result
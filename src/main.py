import pygame
from Game.settings import Settings
from GUI.menu import Menu
from resource import resource

def main():
    settings = Settings()


    pygame.init()

    icon = pygame.image.load(resource("Assets\icone.ico"))

    pygame.display.set_icon(icon)

    window = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("Chess Game")
    
    menu = Menu(window)
    menu.start()
    
if __name__ == "__main__":
    main()
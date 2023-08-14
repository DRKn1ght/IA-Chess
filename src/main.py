import pygame
from Game.settings import Settings
from GUI.menu import Menu

def main():
    settings = Settings()

    pygame.init()

    window = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("Chess Game")
    
    menu = Menu(window)
    menu.start()
    
if __name__ == "__main__":
    main()
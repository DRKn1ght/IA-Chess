import pygame
from Game.settings import Settings
from GUI.menu_drawer import Menu_Drawer
from Game.chess import ChessGame

class Menu:
    def __init__(self, window):
        self.settings = Settings()

        self.window = window
        self.menu_drawer = Menu_Drawer(self.window)

        self.player_vs_ai_button = self.menu_drawer.player_vs_ai_button
        self.ai_vs_ai_button = self.menu_drawer.ai_vs_ai_button
        self.quit_button = self.menu_drawer.quit_button

        self.running = True

        self.clock = pygame.time.Clock()

    def start(self):
        while self.running:
            self.menu_drawer.draw()

            self.clock.tick(self.settings.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.__handle_lmb_up()

    def __handle_lmb_up(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.player_vs_ai_button.collidepoint(mouse_pos):
            game = ChessGame()
            game.run_game("human")
            pass
        if self.ai_vs_ai_button.collidepoint(mouse_pos):
            game = ChessGame()
            game.run_game("AI")
            pass
        if self.quit_button.collidepoint(mouse_pos):
            self.running = False
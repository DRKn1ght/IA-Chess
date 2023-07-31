import pygame

class Board:
    """ A class to manage the board """

    def __init__(self, ai_game):
        """ Create a new board """
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.square_size = self.settings.square_size

        self.array = []
        for i in range(8):
            if i%2:
                self.array.append([1 if j%2 else 0 for j in range(8)])
            else:
                self.array.append([0 if j%2 else 1 for j in range(8)])

    def update(self):
        """ Draw the board on the screen """
        for i in range(8):
            for j in range(8):
                pygame.draw.rect(self.screen, 
                                 self.settings.light_color if self.array[i][j] else self.settings.dark_color, 
                                 (i*self.square_size, j*self.square_size, self.square_size, self.square_size))

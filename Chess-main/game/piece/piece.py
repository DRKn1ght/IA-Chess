import pygame
from pygame.sprite import Sprite

class Piece(Sprite):
    """ A class parent for pieces """

    def __init__(self, ai_game, square, image):
        """ Create a new piece """
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.square = square

        self.image = pygame.image.load(f"Assets/{image}.png")
        self.image = pygame.transform.scale(self.image, (self.settings.square_size,
                                                         self.settings.square_size))
        self.rect = self.image.get_rect()
        self.movement(self.square)

        self.already_moved = False
        self.active = False

    def movement(self, destination_square):
        """ Move the piece """
        self.rect.topleft = (destination_square[0] * self.settings.square_size,
                             destination_square[1] * self.settings.square_size) 
        self.square = destination_square

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the piece """
        pass

    def possible_movements(self, white_pieces, black_pieces, king):
        """ Return the possible movements of the piece """
        real_square = self.square
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        possible_movements = []
        for movement in self.theoretical_movements(white_pieces, black_pieces):
            self.movement(movement)

            # If there are a capture delete the piece temporarily
            capture = pygame.sprite.spritecollideany(self, enemy_pieces)
            if capture:
                enemy_pieces.remove(capture)

            if not king.check(white_pieces, black_pieces):
                possible_movements.append(movement)

            if capture:
                enemy_pieces.add(capture)
            self.movement(real_square)

        return possible_movements

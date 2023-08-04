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
        capture = self.ai_game.get_piece_at_square(destination_square)
        old_x, old_y = self.square
        new_x, new_y = destination_square
        self.rect.topleft = (destination_square[0] * self.settings.square_size,
                             destination_square[1] * self.settings.square_size) 
        self.ai_game.square[old_x][old_y] = None
        self.ai_game.square[new_x][new_y] = self
        self.square = destination_square
        return capture

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the piece """
        pass

    def possible_movements(self, white_pieces, black_pieces, king):
        """ Return the possible movements of the piece """
        real_square = self.square
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        possible_movements = []
        for movement in self.theoretical_movements(white_pieces, black_pieces):
            capture = self.movement(movement)

            # If there are a capture delete the piece temporarily
            if capture:
                enemy_pieces.remove(capture)

            if not king.check(white_pieces, black_pieces):
                if movement[0] >= 0 and movement[0] < 8 and movement[1] >= 0 and movement[1] < 8:
                    possible_movements.append(movement)

            if capture:
                enemy_pieces.add(capture)
            self.movement(real_square)
            self.ai_game.square[movement] = capture

        return possible_movements

    def possible_captures(self, white_pieces, black_pieces, king):
        """ Return the possible movements of the piece """
        real_square = self.square
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        possible_movements = []
        for movement in self.theoretical_movements(white_pieces, black_pieces):
            capture = self.movement(movement)

            # If there are a capture delete the piece temporarily
            if capture:
                enemy_pieces.remove(capture)

            if not king.check(white_pieces, black_pieces):
                    possible_movements.append((movement, None))

            if capture:
                enemy_pieces.add(capture)
                possible_movements.append((movement, capture))
            self.movement(real_square)
            self.ai_game.square[movement] = capture

        return possible_movements
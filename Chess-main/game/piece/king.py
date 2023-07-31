import pygame

from .piece import Piece

from .rook import Rook

class King(Piece):
    """ A class to representing a king """
    
    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}K")
        self.color = color
        self.name = f"{color}King"

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the king """
        dirs = [(1,0),(1,1),(0,1),(-1,0),(0,-1),(1,-1),(-1,-1),(-1,1)]

        friendly_pieces = white_pieces if self.color == "w" else black_pieces
        enemy_pieces = white_pieces if self.color == "b" else black_pieces

        movements = []
        for direction in dirs:
            flag = True # If flag is true, the square is available
            temporary_square = (self.square[0]+direction[0],
                                self.square[1]+direction[1])
            for piece in friendly_pieces:
                if piece.square == temporary_square:
                    flag = False
            if (temporary_square[0] < 0 or temporary_square[0] > 7 or
                temporary_square[1] < 0 or temporary_square[1] > 7):
                flag = False
            if flag:
                movements.append(temporary_square)
        return movements

    def castle(self, white_pieces, black_pieces):
        movements = []
        if not self.already_moved:
            movements.extend(self.short_castle(white_pieces, black_pieces)[0])
            movements.extend(self.large_castle(white_pieces, black_pieces)[0])
        return movements

    def short_castle(self, white_pieces, black_pieces):
        friendly_pieces = white_pieces if self.color == "w" else black_pieces

        movements = []
        rook = None
        if not self.already_moved and not self.check(white_pieces, black_pieces):
            for piece in friendly_pieces:
                if (type(piece) is Rook and not piece.already_moved and 
                        piece.square[0] - self.square[0] == 3):
                    if (self.there_are_no_pieces(white_pieces, black_pieces, self.square, 2, 1)
                            and self.there_are_no_checks(white_pieces, black_pieces, self.square, 2, 1)):
                        rook = piece
                        movements.append((self.square[0]+2, self.square[1]))
                    break
        return movements, rook

    def large_castle(self, white_pieces, black_pieces):
        friendly_pieces = white_pieces if self.color == "w" else black_pieces

        movements = []
        rook = None
        if not self.already_moved and not self.check(white_pieces, black_pieces):
            for piece in friendly_pieces:
                if (type(piece) is Rook and not piece.already_moved and 
                        piece.square[0] - self.square[0] == -4):
                    if (self.there_are_no_pieces(white_pieces, black_pieces, self.square, 3, -1)
                            and self.there_are_no_checks(white_pieces, black_pieces, self.square, 2, -1)):
                        rook = piece
                        movements.append((self.square[0]-2, self.square[1]))
                    break
        return movements, rook

    def there_are_no_pieces(self, white_pieces, black_pieces, actual_square, number_of_squares, direction):
        """ Return True if there are no pieces between the actual square and a number of squares"""
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        squares = []

        for i in range(number_of_squares):
            squares.append((actual_square[0]+(i+1)*direction, actual_square[1]))

        for piece in white_pieces:
            if piece.square in squares:
                return False
        for piece in black_pieces:
            if piece.square in squares:
                return False   
        return True

    def there_are_no_checks(self, white_pieces, black_pieces, actual_square, number_of_squares, direction):
        """ Return True if there are no checks between the actual square and a number of squares"""
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        squares = []

        for i in range(number_of_squares):
            squares.append((actual_square[0]+(i+1)*direction, actual_square[1]))

        for piece in enemy_pieces:
            for square in squares:
                if square in piece.theoretical_movements(white_pieces, black_pieces):
                    return False
        return True

    def check(self, white_pieces, black_pieces):
        """ Check if the king is in check """
        enemy_pieces = white_pieces if self.color == "b" else black_pieces 
        for piece in enemy_pieces:
            if self.square in piece.theoretical_movements(white_pieces, black_pieces):
                return True
        return False

    def possible_movements(self, white_pieces, black_pieces, king):
        possible_movements = super().possible_movements(white_pieces, black_pieces, self)

        possible_movements.extend(self.castle(white_pieces, black_pieces))

        return possible_movements

